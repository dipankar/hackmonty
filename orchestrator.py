#!/usr/bin/env python3
"""Orchestrator v2 — analyst/coder split, meta-review, diversity enforcement.

Usage:
  uv run python orchestrator.py [--max-iterations N] [--batch-size N]
"""

from __future__ import annotations

import json
import os
import sys
import time
import shutil
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from hackmonty_client import HackMontyClient, format_result
from evaluate import evaluate, SCORE_LABELS, EvalResult
from issue_tracker import fetch_and_categorize, format_issues_for_agent, save_issues_snapshot
from agent import Agent, AgentResponse


PROJECT_DIR = Path(__file__).parent
NOTES_DIR = PROJECT_DIR / "notes"
ATTEMPTS_DIR = NOTES_DIR / "attempts"
UNDERSTANDING_DIR = NOTES_DIR / "understanding"
RESULTS_DIR = NOTES_DIR / "results"
ISSUES_DIR = NOTES_DIR / "issues"
STATE_FILE = NOTES_DIR / "state.json"

CONSECUTIVE_ZERO_LIMIT = 8
ISSUE_SYNC_INTERVAL = 7200
DEAD_TEMPLATE_COOLDOWN = 20


def ensure_dirs():
    for d in [ATTEMPTS_DIR, UNDERSTANDING_DIR, RESULTS_DIR, ISSUES_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def load_program_md() -> str:
    return (PROJECT_DIR / "program.md").read_text()


def load_understanding() -> str:
    entries = sorted(UNDERSTANDING_DIR.glob("*.md"))
    if not entries:
        return ""
    parts = []
    for e in entries:
        parts.append(f"{e.read_text()}\n")
    return "\n".join(parts)


def load_recent_history(n: int = 15) -> str:
    attempt_dirs = sorted(ATTEMPTS_DIR.glob("*/"), reverse=True)
    parts = []
    count = 0
    for d in attempt_dirs:
        for f in sorted(d.glob("attempt_*.md"), reverse=True):
            if count >= n:
                break
            text = f.read_text()
            idx = text.find("## Reasoning")
            if idx > 0:
                text = text[idx:]
            parts.append(f"--- {f.name} ---\n{text[:600]}")
            count += 1
        if count >= n:
            break
    return "\n\n".join(parts) if parts else "No history."


def load_latest_issues() -> str:
    path = ISSUES_DIR / "latest_issues.json"
    if path.exists():
        try:
            return format_issues_for_agent(json.loads(path.read_text()))
        except Exception:
            pass
    return ""


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {}


def save_state(iteration: int, template_idx: int, score_counts: dict,
                consecutive_zeros: int, dead_templates: list, focus: str):
    STATE_FILE.write_text(json.dumps({
        "last_iteration": iteration,
        "template_idx": template_idx,
        "score_counts": dict(score_counts),
        "consecutive_zeros": consecutive_zeros,
        "dead_templates": dead_templates,
        "focus": focus,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }, indent=2))


def generate_analysis(score: int, result: Any) -> str:
    if score == 0:
        if result and result.error:
            err = result.error[:150]
            if "MemoryError" in err:
                return "- Resource limit hit (allocation/memory)\n- **Verdict**: Not exploitable — adjust strategy"
            return f"- Error: {err}\n- **Verdict**: Not exploitable"
        return "- Completed with no findings\n- **Verdict**: Try different template"
    elif score == 1:
        return f"- **Crash detected**: {result.error[:200] if result else 'Unknown'}\n- **Verdict**: Investigate further"
    elif score == 2:
        return "- **Interesting behavior** — unexpected snapshot or internal error\n- **Verdict**: Promising"
    elif score == 3:
        return f"- **Host info leaked**: {result.error[:200] if result else 'snapshot data'}\n- **Verdict**: Useful recon"
    elif score == 4:
        return "- **File read!** — non-public file content accessed\n- **Verdict**: MAJOR FINDING"
    elif score == 5:
        return "- **SECRET FOUND!** — sandbox escaped\n- **Verdict**: BOUNTY CLAIMABLE"
    return ""


def validate_code(code: str) -> str | None:
    if not code or len(code.strip()) < 10:
        return "Code too short"
    if "class " in code:
        return "NO class definitions allowed"
    if "\ndel " in code or code.startswith("del "):
        return "NO del statement allowed"
    if "yield " in code or " yield" in code:
        return "NO yield expressions allowed"
    if "os.listdir" in code:
        return "NO os.listdir — not available"
    return None


def save_attempt(iteration: int, template: str, agent_resp: AgentResponse,
                 run_result: Any, eval_result: EvalResult):
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    d = ATTEMPTS_DIR / date_str
    d.mkdir(parents=True, exist_ok=True)
    n = len(list(d.glob("attempt_*.md"))) + 1

    analysis = generate_analysis(eval_result.score, run_result)

    content = f"""# Attempt {iteration:03d} — {datetime.now(timezone.utc).isoformat()}
## Template: {template} | Score: {eval_result.score}
## Strategy
{agent_resp.strategy}

## Exploit code
```python
{agent_resp.exploit_code}
```

## Result
Category: {eval_result.category}
Details: {'; '.join(eval_result.details) if eval_result.details else 'None'}
```
{format_result(run_result) if run_result else 'No run result'}
```

## Analysis
{analysis}
"""
    (d / f"attempt_{n:03d}.md").write_text(content)
    return d / f"attempt_{n:03d}.md"


def update_findings(eval_result: EvalResult, attempt_path: Path):
    if eval_result.score < 2:
        return
    findings_path = RESULTS_DIR / "findings.md"
    entry = f"\n## [{datetime.now(timezone.utc).isoformat()}] Score {eval_result.score}: {eval_result.label}\n"
    entry += f"- Template: {eval_result.category}\n"
    entry += f"- {'; '.join(eval_result.details)}\n"
    entry += f"- See: {attempt_path.name}\n"
    existing = findings_path.read_text() if findings_path.exists() else ""
    findings_path.write_text(entry + existing)


TEMPLATES = [
    ("A", "DictReentry", "Dict key __eq__/__hash__ re-entry"),
    ("B", "SetReentry", "Set element __hash__ re-entry during add"),
    ("C", "SortCmp", "sort() py_cmp O(n log n) callback flood"),
    ("D", "MinMaxMutate", "min/max/sorted key= while mutating iterable"),
    ("E", "MemDrift", "Memory counter drift via alloc/free mismatch"),
    ("F", "ConfigFiles", "Read /data config files for host info"),
    ("G", "AllocRace", "Allocation exhaustion mid-sort"),
    ("H", "AsyncGC", "asyncio.gather GC race during futures"),
]


def main():
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)

    if (pycache := PROJECT_DIR / "__pycache__").exists():
        shutil.rmtree(pycache)

    parser = argparse.ArgumentParser(description="Hack Monty Loop v2")
    parser.add_argument("--user-secret", default=os.environ.get("USER_SECRET"))
    parser.add_argument("--max-iterations", type=int, default=500)
    parser.add_argument("--batch-size", type=int, default=3)
    parser.add_argument("--api-key", help="Ollama API key")
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("OLLAMA_API_KEY")
    if not api_key:
        print("ERROR: OLLAMA_API_KEY not set.")
        sys.exit(1)

    ensure_dirs()

    state = {} if args.no_resume else load_state()
    iteration = state.get("last_iteration", 0)
    score_counts = state.get("score_counts", {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0})
    for k in range(6):
        score_counts.setdefault(k, 0)
    consecutive_zeros = state.get("consecutive_zeros", 0)
    dead_templates = state.get("dead_templates", [])
    template_idx = state.get("template_idx", 0)

    agent = Agent(api_key=api_key)
    client = HackMontyClient(user_secret=args.user_secret)
    system_prompt = load_program_md() + "\n\n## Knowledge Base\n" + load_understanding()

    last_issue_sync = 0.0
    if not state or args.no_resume:
        print("\n--- Initial GitHub issue sync ---")
        try:
            results = fetch_and_categorize(NOTES_DIR)
            save_issues_snapshot(results, NOTES_DIR)
            last_issue_sync = time.monotonic()
        except Exception as e:
            print(f"  [WARN] Issue fetch failed: {e}")

    if state and not args.no_resume:
        print(f"\nResuming from iteration {iteration}, dead templates: {dead_templates}")

    print(f"\nLoop: {args.max_iterations} iterations, batch {args.batch_size}")
    print(f"Templates: {' '.join(t[0] for t in TEMPLATES)}")
    print("Mode: analyst → coder → run → evaluate → meta-review")
    print("Press Ctrl+C to stop.\n")

    try:
        while iteration < args.max_iterations:
            # Issue sync
            now = time.monotonic()
            if now - last_issue_sync >= ISSUE_SYNC_INTERVAL:
                print("--- Syncing GitHub issues ---")
                try:
                    results = fetch_and_categorize(NOTES_DIR)
                    save_issues_snapshot(results, NOTES_DIR)
                    last_issue_sync = now
                except Exception as e:
                    print(f"  [WARN] Issue fetch failed: {e}")

            # Pick next live template
            live = [(i, t) for i, t in enumerate(TEMPLATES)
                     if t[0] not in dead_templates]
            if not live:
                dead_templates = []
                live = list(enumerate(TEMPLATES))
            if template_idx >= len(live):
                template_idx = 0

            _, (template_letter, template_name, template_desc) = live[template_idx]

            print(f"\n{'='*50}")
            print(f"Iteration {iteration} | Template {template_letter}: {template_desc}")
            print(f"{'='*50}")

            # Analyst: review history, pick strategy
            print("  [analyst] Reviewing history...")
            history = load_recent_history(10)
            analyst_resp = agent.analyst(system_prompt, history)

            template_from_analyst = analyst_resp.chosen_template or template_letter
            strategy = analyst_resp.strategy or f"Execute {template_desc}"
            print(f"  Template: {template_from_analyst} | Strategy: {strategy[:120]}...")

            # Coder: generate exploit
            print("  [coder] Generating exploit...")
            coder_resp = agent.coder(system_prompt, template_from_analyst, strategy)

            validation_error = validate_code(coder_resp.exploit_code)
            if validation_error:
                print(f"  [WARN] Validation: {validation_error} — retrying")
                coder_resp = agent.coder(system_prompt, template_from_analyst,
                                          strategy + f"\n\nCRITICAL: {validation_error}")
                if validate_code(coder_resp.exploit_code):
                    print("  [WARN] Retry still failed, using anyway")

            print(f"  Code: {len(coder_resp.exploit_code)} chars")

            # Run
            print("  [run] Executing against hackmonty.com...")
            try:
                run_result = client.run_code(coder_resp.exploit_code)
            except Exception as e:
                print(f"  [ERROR] Run failed: {e}")
                run_result = None

            # Evaluate
            eval_result = evaluate(run_result) if run_result else EvalResult(
                score=0, label="Client error", category="client_error",
                details=["Failed to run exploit"])
            print(f"  Score: {eval_result.score}/5 — {eval_result.label}")

            # Save
            attempt_path = save_attempt(iteration, template_from_analyst,
                                         coder_resp, run_result, eval_result)
            update_findings(eval_result, attempt_path)

            # Track scores
            score_counts[eval_result.score] = score_counts.get(eval_result.score, 0) + 1
            if eval_result.score == 0:
                consecutive_zeros += 1
            else:
                consecutive_zeros = 0

            iteration += 1
            template_idx += 1

            # Diversity enforcement: 8 consecutive zeros = dead template
            if consecutive_zeros >= CONSECUTIVE_ZERO_LIMIT:
                deadname = template_from_analyst
                if deadname not in dead_templates:
                    dead_templates.append(deadname)
                print(f"  *** Template {deadname} marked dead ({consecutive_zeros} zeros) ***")
                consecutive_zeros = 0
                template_idx = 0

            # Meta-review every batch
            if iteration % args.batch_size == 0 or eval_result.score >= 3:
                if iteration > 1:
                    print("\n  [meta-review] Analyzing batch...")
                    recent = load_recent_history(args.batch_size * 2)
                    try:
                        review = agent.meta_review(
                            f"Last {args.batch_size} attempts:\n{recent[:1500]}",
                            score_counts)
                        if review.assessment:
                            print(f"  Assessment: {review.assessment[:200]}...")
                        if review.confidence:
                            dead_letters = [c.strip().upper() for c in review.confidence.split(",")]
                            for dl in dead_letters:
                                if dl in [t[0] for t in TEMPLATES] and dl not in dead_templates:
                                    dead_templates.append(dl)
                                    print(f"  *** Meta-review killed template {dl} ***")
                        if review.suggested_changes:
                            print(f"  Suggestion: {review.suggested_changes[:200]}...")
                    except Exception as e:
                        print(f"  [WARN] Meta-review failed: {e}")

            save_state(iteration, template_idx, score_counts,
                        consecutive_zeros, dead_templates,
                        template_from_analyst)

            print(f"\n--- Progress: {iteration}/{args.max_iterations} — "
                  f"0={score_counts.get(0,0)} 1={score_counts.get(1,0)} 2={score_counts.get(2,0)} "
                  f"3={score_counts.get(3,0)} 4={score_counts.get(4,0)} 5={score_counts.get(5,0)}")
            print(f"  Consecutive zeros: {consecutive_zeros} | Dead: {dead_templates}")

            if eval_result.score >= 5:
                print(f"\n{'='*60}")
                print("SECRET FOUND — check notes/results/findings.md")
                print(f"Report to: https://roast-us.pydantic.dev/hackmonty2")
                print(f"{'='*60}")
                break

    except KeyboardInterrupt:
        print("\n\nInterrupted.")
        save_state(iteration, template_idx, score_counts,
                    consecutive_zeros, dead_templates,
                    "interrupted")

    print(f"\n{'='*60}\nFINAL REPORT\n{'='*60}")
    print(f"Iterations: {iteration}")
    for s, label in SCORE_LABELS.items():
        print(f"  {s}: {score_counts.get(s, 0)} — {label}")
    client.close()


if __name__ == "__main__":
    main()
