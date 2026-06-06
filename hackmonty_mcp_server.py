#!/usr/bin/env python3
"""Hack Monty MCP Server — boundary tools for tokenworm agent harness.

16 tools exposed via FastMCP @mcp.tool() decorators.
Communication via stdio JSON-RPC.
"""

from __future__ import annotations

import json, os, sys, asyncio
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

PROJECT_DIR = Path(__file__).parent
NOTES_DIR = PROJECT_DIR / "notes"
ATTEMPTS_DIR = NOTES_DIR / "attempts"
RESULTS_DIR = NOTES_DIR / "results"
STATE_FILE = NOTES_DIR / "state.json"

mcp = FastMCP("hackmonty-mcp")


# ── Lazy helpers ───────────────────────────────────────────────

_bandit = None
_bandit_total = 0

def _get_bandit():
    global _bandit, _bandit_total
    if _bandit is None:
        import bandit as _b
        _bandit = _b.Bandit(templates=_TEMPLATES)
        if STATE_FILE.exists():
            try:
                s = json.loads(STATE_FILE.read_text())
                _bandit_total = s.get("bandit_total", 0)
                _bandit.total_attempts = _bandit_total
            except: pass
    return _bandit

_TEMPLATES = [
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


# ── Execution Layer ────────────────────────────────────────────

@mcp.tool()
async def hackmonty_run(code: str) -> str:
    """POST Python code to hackmonty.com sandbox, handle snapshot/resume, return result.

    Returns JSON: success, error, output, print_output, num_snapshots,
    snapshot_kinds, elapsed_ms, total_resumes, context.
    """
    from hackmonty_client import AsyncHackMontyClient
    from evaluate import enrich_context

    client = AsyncHackMontyClient(
        user_secret=os.environ.get("USER_SECRET", ""), concurrency=1
    )
    try:
        result = await client.run_code(code)
        kinds = [s.kind for s in result.snapshots]
        return json.dumps({
            "success": result.success,
            "error": (result.error or "")[:500],
            "output": str(result.raw_response.get("output", ""))[:500],
            "print_output": result.raw_response.get("print_output", "")[:500],
            "num_snapshots": len(result.snapshots),
            "snapshot_kinds": kinds,
            "elapsed_ms": result.elapsed_ms,
            "total_resumes": result.total_resumes,
            "context": enrich_context(result),
        })
    finally:
        await client.close()


@mcp.tool()
def hackmonty_evaluate(result_json: str) -> str:
    """Score a run result 0-5. Pass the JSON result from hackmonty_run.

    Returns JSON: {score, label, category, details}.
    """
    from evaluate import evaluate, SCORE_LABELS
    from hackmonty_client import RunResult, SnapshotResult

    data = json.loads(result_json)
    snapshots = []
    for k in data.get("snapshot_kinds", []):
        snapshots.append(SnapshotResult(snapshot_id="", kind=k, data={}))

    result = RunResult(
        success=data.get("success", False),
        raw_response={"output": data.get("output"),
                      "print_output": data.get("print_output", "")},
        error=data.get("error"),
        snapshots=snapshots,
        elapsed_ms=data.get("elapsed_ms", 0),
        total_resumes=data.get("total_resumes", 0),
    )
    er = evaluate(result)
    return json.dumps({
        "score": er.score, "label": SCORE_LABELS.get(er.score, ""),
        "category": er.category, "details": er.details,
    })


@mcp.tool()
async def hackmonty_revalidate(code: str, result_json: str, original_score: int) -> str:
    """Re-run code 3x. If >=2/3 output hashes match, keep score. Else demote to 1."""
    from evaluate import output_hash
    from hackmonty_client import AsyncHackMontyClient, RunResult

    if original_score < 2:
        return json.dumps({"confirmed_score": original_score, "matches": 0,
                           "ran": 0, "note": "Score < 2, skip"})

    data = json.loads(result_json)
    client = AsyncHackMontyClient(
        user_secret=os.environ.get("USER_SECRET", ""), concurrency=1
    )
    try:
        original = RunResult(
            success=data.get("success", False),
            raw_response={"output": data.get("output"),
                          "print_output": data.get("print_output", "")},
            error=data.get("error"), snapshots=[],
        )
        orig_hash = output_hash(original)
        matches = 0
        for _ in range(3):
            r = await client.run_code(code)
            if output_hash(r) == orig_hash:
                matches += 1
        score = original_score if matches >= 2 else 1
        return json.dumps({"confirmed_score": score, "matches": matches, "ran": 3})
    finally:
        await client.close()


@mcp.tool()
def hackmonty_syntax_check(code: str) -> str:
    """Check if Python code is valid. Returns {valid, error}."""
    try:
        compile(code, "<exploit>", "exec")
        return json.dumps({"valid": True, "error": None})
    except SyntaxError as e:
        return json.dumps({"valid": False, "error": f"Line {e.lineno}: {e.msg}"})


# ── Bandit Layer ───────────────────────────────────────────────

@mcp.tool()
def bandit_select() -> str:
    """Pick next attack template via UCB1 bandit. Returns {letter, name}."""
    b = _get_bandit()
    letter, name = b.select()
    return json.dumps({"letter": letter, "name": name})


@mcp.tool()
def bandit_update(template: str, score: float) -> str:
    """Update bandit stats after an attempt."""
    b = _get_bandit()
    b.update(template, score)
    global _bandit_total
    _bandit_total = b.total_attempts
    return json.dumps({"ok": True})


@mcp.tool()
def bandit_novelty(code: str) -> str:
    """Check if code is duplicate of previous. 1.0=novel, <0.5=near-dup."""
    b = _get_bandit()
    n = b.check_novelty(code)
    return json.dumps({"novelty": round(n, 3)})


@mcp.tool()
def bandit_kill(template: str) -> str:
    """Kill a template for 25 iterations."""
    b = _get_bandit()
    b.kill_template(template)
    return json.dumps({"ok": True, "killed": template})


@mcp.tool()
def bandit_summary() -> str:
    """Get bandit stats for all templates (text)."""
    b = _get_bandit()
    return b.summary()


# ── Knowledge Layer ────────────────────────────────────────────

@mcp.tool()
def notes_history(n: int = 10) -> str:
    """Read last N attempt records. Returns JSON array of {filename, template, score, category, context}."""
    attempts = sorted(ATTEMPTS_DIR.glob("*/*.md"), reverse=True)[:n]
    results = []
    for f in attempts:
        text = f.read_text()[:2000]
        template, score, category, context = "", 0, "", ""
        for line in text.split('\n'):
            if "| Score:" in line and "Template:" in line:
                parts = line.split("|")
                template = parts[0].split(":")[-1].strip()
                try: score = int(parts[1].split(":")[-1].strip().split()[0])
                except: pass
            if line.startswith("Category:"): category = line.split(":", 1)[-1].strip()
            if line.startswith("Context:"): context = line.split(":", 1)[-1].strip()
        results.append({
            "filename": f.name, "template": template, "score": score,
            "category": category, "context": context[:200],
        })
    return json.dumps(results)


@mcp.tool()
def attempt_save(iteration: int, template: str, code: str,
                 score: int, label: str, context: str) -> str:
    """Save an attempt to disk. Returns {path}."""
    from datetime import datetime, timezone
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    d = ATTEMPTS_DIR / date_str
    d.mkdir(parents=True, exist_ok=True)
    n = len(list(d.glob("attempt_*.md"))) + 1

    content = f"""# Attempt {iteration:03d} - {datetime.now(timezone.utc).isoformat()}
## Template: {template} | Score: {score} - {label}
## Exploit code
```python
{code}
```

## Result
Context: {context}
Score: {score}/5 - {label}
"""
    path = d / f"attempt_{n:03d}.md"
    path.write_text(content)
    return json.dumps({"path": str(path)})


@mcp.tool()
def state_read() -> str:
    """Read orchestrator state: iteration, score_counts, bandit_total."""
    if STATE_FILE.exists():
        return STATE_FILE.read_text()
    return json.dumps({"last_iteration": 0, "score_counts": {}, "bandit_total": 0})


@mcp.tool()
def state_write(iteration: int, score_counts_json: str, bandit_total: int):
    """Save orchestrator state for resume."""
    from datetime import datetime, timezone
    sc = json.loads(score_counts_json)
    STATE_FILE.write_text(json.dumps({
        "last_iteration": iteration, "score_counts": sc,
        "bandit_total": bandit_total,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }, indent=2))
    return json.dumps({"ok": True})


@mcp.tool()
def program_read() -> str:
    """Read the full attack program with template docs."""
    p = PROJECT_DIR / "program.md"
    return p.read_text() if p.exists() else "No program.md"


@mcp.tool()
def source_scan() -> str:
    """Source audit: unsafe blocks, callback points, module whitelist."""
    p = NOTES_DIR / "source_scan.json"
    return p.read_text() if p.exists() else '{"error": "Run source_scanner.py first"}'


@mcp.tool()
def github_issues() -> str:
    """Fetch + categorize GitHub issues from pydantic/monty + pydantic/pydantic-ai."""
    from issue_tracker import fetch_and_categorize, save_issues_snapshot, format_issues_for_agent
    results = fetch_and_categorize(NOTES_DIR)
    save_issues_snapshot(results, NOTES_DIR)
    return format_issues_for_agent(results)


@mcp.tool()
def findings_read() -> str:
    """Read cumulative findings log (score >= 2)."""
    fp = RESULTS_DIR / "findings.md"
    return fp.read_text()[:3000] if fp.exists() else "No findings yet"


# ── Main ──────────────────────────────────────────────────────

def main():
    import sys
    for d in [ATTEMPTS_DIR, RESULTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    # SSE mode: `python hackmonty_mcp_server.py --sse [--port 8765]`
    if "--sse" in sys.argv:
        port_idx = sys.argv.index("--port") if "--port" in sys.argv else -1
        port = int(sys.argv[port_idx + 1]) if port_idx >= 0 and port_idx + 1 < len(sys.argv) else 8765
        print(f"[MCP] Starting SSE server on port {port}...", file=sys.stderr)
        mcp.run(transport="sse", host="0.0.0.0", port=port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
