#!/usr/bin/env python3
"""Orchestrator v3 — 4-worker async swarm with bandit selection.

Usage:
  uv run python -B orchestrator.py [--max-iterations N] [--workers N]
"""

from __future__ import annotations

import asyncio, json, os, sys, time, shutil, argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from hackmonty_client import AsyncHackMontyClient, RunResult, format_result
from evaluate import evaluate, EvalResult, SCORE_LABELS, enrich_context, output_hash
from issue_tracker import fetch_and_categorize, save_issues_snapshot
from agent import Agent, AgentResponse, code_hash
from bandit import Bandit


PROJECT_DIR = Path(__file__).parent
NOTES_DIR = PROJECT_DIR / "notes"
ATTEMPTS_DIR = NOTES_DIR / "attempts"
RESULTS_DIR = NOTES_DIR / "results"
UNDERSTANDING_DIR = NOTES_DIR / "understanding"
ISSUES_DIR = NOTES_DIR / "issues"
STATE_FILE = NOTES_DIR / "state.json"

ISSUE_SYNC_INTERVAL = 7200
META_REVIEW_EVERY = 12

TEMPLATES = [
    ("A", "DictReentry", "Dict __eq__/__hash__ re-entry"),
    ("B", "SetReentry", "Set __hash__ re-entry during add"),
    ("C", "SortCmp", "sort() py_cmp callback flood"),
    ("D", "MinMaxMutate", "min/max/sorted key= while mutating"),
    ("E", "MemDrift", "Memory counter drift via alloc/free mismatch"),
    ("F", "ConfigFiles", "Read /data config files for host info"),
    ("G", "AllocRace", "Allocation exhaustion mid-sort"),
    ("H", "AsyncGC", "asyncio.gather GC race"),
    ("I", "NameLookup", "Name lookup resume manipulation"),
    ("J", "FutureChain", "Future snapshot chaining"),
    ("K", "DoubleResume", "Double-resume state machine"),
]

VALIDATION_KW = ("class ", "\ndel ", "yield ", " yield", "os.listdir")


def syntax_check(code: str) -> str | None:
    """Check if Python code can be compiled. Returns error message or None."""
    try:
        compile(code, "<exploit>", "exec")
        return None
    except SyntaxError as e:
        return f"Python syntax error at line {e.lineno}: {e.msg}"


def ensure_dirs():
    for d in [ATTEMPTS_DIR, UNDERSTANDING_DIR, RESULTS_DIR, ISSUES_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def load_program_md() -> str:
    p = PROJECT_DIR / "program.md"
    return p.read_text() if p.exists() else ""


def load_understanding() -> str:
    entries = sorted(UNDERSTANDING_DIR.glob("*.md"))
    return "\n".join(e.read_text() + "\n" for e in entries) if entries else ""


def load_recent_history(n: int = 12) -> str:
    attempts = sorted(ATTEMPTS_DIR.glob("*/*.md"), reverse=True)[:n]
    return "\n\n".join(f.read_text()[:500] for f in attempts) if attempts else "No history."


def load_state() -> dict:
    if STATE_FILE.exists():
        try: return json.loads(STATE_FILE.read_text())
        except: pass
    return {}


def save_state(iteration: int, score_counts: dict, bandit: Bandit):
    STATE_FILE.write_text(json.dumps({
        "last_iteration": iteration,
        "score_counts": dict(score_counts),
        "bandit_total": bandit.total_attempts,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }, indent=2))


def validate_code(code: str) -> str | None:
    if not code or len(code.strip()) < 10:
        return "Code too short"
    for kw in VALIDATION_KW:
        if kw in code:
            return f"NO {kw.strip()} - not supported in Monty"
    return None


def save_attempt(iteration: int, template: str, agent_resp: AgentResponse,
                 run_result: Any, eval_result: EvalResult, context: str):
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    d = ATTEMPTS_DIR / date_str
    d.mkdir(parents=True, exist_ok=True)
    n = len(list(d.glob("attempt_*.md"))) + 1

    label = SCORE_LABELS.get(eval_result.score, "Unknown")
    code_block = f"```python\n{agent_resp.exploit_code}\n```"
    run_block = f"```\n{format_result(run_result) if run_result else 'No run result'}\n```"
    details = "; ".join(eval_result.details) if eval_result.details else "None"

    content = f"""# Attempt {iteration:03d} - {datetime.now(timezone.utc).isoformat()}
## Template: {template} | Score: {eval_result.score} - {label}
## Strategy
{agent_resp.strategy}

## Exploit code
{code_block}

## Result
Category: {eval_result.category}
Context: {context}
Details: {details}
{run_block}

## Analysis
{quick_analysis(eval_result.score, run_result)}
"""
    (d / f"attempt_{n:03d}.md").write_text(content)
    return d / f"attempt_{n:03d}.md"


def quick_analysis(score: int, result: Any) -> str:
    if score == 0:
        if result and result.error:
            return f"- {result.error[:150]}\n- Verdict: Not exploitable"
        return "- Completed with no findings\n- Verdict: Try different template"
    elif score == 1: return "- Crash detected\n- Verdict: Investigate further"
    elif score == 2: return "- Interesting behavior\n- Verdict: Promising"
    elif score == 3: return "- Host info leaked\n- Verdict: Useful recon"
    elif score == 4: return "- File read\n- Verdict: MAJOR FINDING"
    elif score == 5: return "- SECRET FOUND\n- Verdict: BOUNTY CLAIMABLE"
    return ""


def update_findings(eval_result: EvalResult, attempt_path: Path):
    if eval_result.score < 2:
        return
    entry = f"\n## [{datetime.now(timezone.utc).isoformat()}] Score {eval_result.score}: {eval_result.label}\n"
    entry += f"- Template: {eval_result.category}\n- {'; '.join(eval_result.details)}\n- See: {attempt_path.name}\n"
    fp = RESULTS_DIR / "findings.md"
    existing = fp.read_text() if fp.exists() else ""
    fp.write_text(entry + existing)


async def re_validate(client: AsyncHackMontyClient, code: str,
                       original_result: RunResult, original_score: int) -> int:
    if original_score < 2:
        return original_score
    orig_hash = output_hash(original_result)
    matches = 0
    for _ in range(3):
        try:
            r = await client.run_code(code)
            if output_hash(r) == orig_hash:
                matches += 1
        except Exception:
            pass
    return original_score if matches >= 2 else 1


async def worker(wid: int, agent: Agent, client: AsyncHackMontyClient,
                 bandit: Bandit, state: dict, lock: asyncio.Lock,
                 system_prompt: str):
    while state["iteration"] < state["max_iterations"]:
        template_letter, template_name = bandit.select()
        template_desc = next((d for l, n, d in TEMPLATES if l == template_letter), template_name)

        async with lock:
            it = state["iteration"]
            if it >= state["max_iterations"]:
                break
            state["iteration"] += 1

        print(f"  [W{wid}] #{it:04d} | T{template_letter}: {template_desc}")

        try:
            # Analyst
            history = load_recent_history(8)
            ar = await agent.analyst(system_prompt, history)
            t = ar.chosen_template or template_letter
            s = ar.strategy or f"Execute {template_desc}"

            # Coder — retry up to 3x, with syntax checking
            cr = await agent.coder(system_prompt, t, s)
            for retry in range(3):
                kw_err = validate_code(cr.exploit_code)
                syn_err = syntax_check(cr.exploit_code) if not kw_err else None

                if not kw_err and not syn_err:
                    break  # Code is valid

                err_msg = kw_err or syn_err
                if retry < 2:
                    cr = await agent.coder(
                        system_prompt, t,
                        s + f"\n\nCRITICAL: Code rejected — {err_msg}."
                            f" Fix the error and regenerate. Output ONLY correct Python code."
                    )
                else:
                    print(f"    [W{wid}] Syntax validation failed after {retry + 1} retries: {err_msg}")
            if validate_code(cr.exploit_code) or syntax_check(cr.exploit_code):
                print(f"    [W{wid}] Using code with known issues, proceeding anyway")

            # Run
            rr = await client.run_code(cr.exploit_code)

            # Evaluate
            er = evaluate(rr)
            sp_detail = enrich_context(rr)

            # Re-validate
            er.score = await re_validate(client, cr.exploit_code, rr, er.score)

            # Novelty
            novelty = bandit.check_novelty(cr.exploit_code)
            bandit.update(t, er.score * novelty)

            # Meta-review
            if it > 1 and it % META_REVIEW_EVERY == 0:
                try:
                    mr = await agent.meta_review(
                        f"Last batch at iteration {it}\n" + load_recent_history(6)[:1200],
                        state["score_counts"]
                    )
                    if mr.confidence:
                        for dl in mr.confidence.split(","):
                            dl = dl.strip().upper()
                            if dl in [x[0] for x in TEMPLATES]:
                                bandit.kill_template(dl)
                                print(f"    [meta] Killed template {dl}: {mr.assessment[:100]}")
                except Exception as e:
                    print(f"    [meta] Review failed: {e}")

            # Save
            ap = save_attempt(it, t, cr, rr, er, sp_detail)
            update_findings(er, ap)

            # Track scores
            async with lock:
                state["score_counts"][er.score] = state["score_counts"].get(er.score, 0) + 1

            sc = state["score_counts"]
            print(f"    -> Score {er.score}/5 ({SCORE_LABELS.get(er.score,'?')}) | "
                  f"0={sc.get(0,0)} 1={sc.get(1,0)} 2={sc.get(2,0)} "
                  f"3={sc.get(3,0)} 4={sc.get(4,0)}")
            if sp_detail:
                print(f"    -> {sp_detail}")

            if er.score >= 5:
                print(f"\n{'='*60}\nSECRET FOUND\nReport: https://roast-us.pydantic.dev/hackmonty2\n{'='*60}")
                state["found"] = True
                return

            save_state(it, state["score_counts"], bandit)

        except Exception as e:
            print(f"    [W{wid}] ERROR: {e}")
            await asyncio.sleep(2)


async def main():
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)

    if (pyc := PROJECT_DIR / "__pycache__").exists():
        shutil.rmtree(pyc)

    parser = argparse.ArgumentParser(description="Hack Monty Loop v3 - Async Swarm")
    parser.add_argument("--user-secret", default=os.environ.get("USER_SECRET"))
    parser.add_argument("--max-iterations", type=int, default=500)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--api-key", help="Ollama API key")
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("OLLAMA_API_KEY")
    if not api_key:
        print("ERROR: OLLAMA_API_KEY not set.")
        sys.exit(1)

    ensure_dirs()

    state_data = {} if args.no_resume else load_state()
    iteration = state_data.get("last_iteration", 0)
    score_counts = state_data.get("score_counts", {})
    for k in range(6):
        score_counts.setdefault(k, 0)

    agent = Agent(api_key=api_key)
    client = AsyncHackMontyClient(user_secret=args.user_secret, concurrency=args.workers)
    bandit = Bandit(templates=TEMPLATES)
    if "bandit_total" in state_data:
        bandit.total_attempts = state_data["bandit_total"]

    system_prompt = load_program_md() + "\n\n## Knowledge Base\n" + load_understanding()

    last_issue_sync = 0.0
    if not state_data or args.no_resume:
        print("--- Initial GitHub issue sync ---")
        try:
            results = fetch_and_categorize(NOTES_DIR)
            save_issues_snapshot(results, NOTES_DIR)
            last_issue_sync = time.monotonic()
        except Exception as e:
            print(f"  [WARN] Issue fetch failed: {e}")

    print(f"\nV3 Swarm: {args.max_iterations} iterations, {args.workers} workers")
    print(f"Analyst: minimax-m3:cloud | Coder: kimi-k2.6:cloud")
    print(f"Templates: {' '.join(t[0] for t in TEMPLATES)}")
    print(f"Mode: bandit→analyst→coder→run→eval→revalidate")
    print("Press Ctrl+C to stop.\n")

    shared_state = {
        "iteration": iteration,
        "max_iterations": args.max_iterations,
        "score_counts": score_counts,
        "found": False,
    }
    lock = asyncio.Lock()

    try:
        workers = [
            asyncio.create_task(
                worker(i, agent, client, bandit, shared_state, lock, system_prompt)
            )
            for i in range(args.workers)
        ]
        await asyncio.gather(*workers)
    except KeyboardInterrupt:
        print("\n\nInterrupted.")
    finally:
        save_state(shared_state["iteration"], shared_state["score_counts"], bandit)
        await client.close()

    print(f"\n{'='*60}\nFINAL REPORT\n{'='*60}")
    print(f"Iterations: {shared_state['iteration']}")
    print(bandit.summary())
    for s, label in SCORE_LABELS.items():
        print(f"  {s}: {score_counts.get(s, 0)} - {label}")


if __name__ == "__main__":
    asyncio.run(main())
