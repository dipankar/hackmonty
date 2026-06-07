#!/usr/bin/env python3
"""Hack Monty MCP Server — boundary tools for tokenworm agent harness.

16 tools exposed via FastMCP @mcp.tool() decorators.
Communication via stdio JSON-RPC.
"""

from __future__ import annotations

import json, os, sys, asyncio, sqlite3
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

PROJECT_DIR = Path(__file__).parent
NOTES_DIR = PROJECT_DIR / "notes"
ATTEMPTS_DIR = NOTES_DIR / "attempts"
RESULTS_DIR = NOTES_DIR / "results"
STATE_FILE = NOTES_DIR / "state.json"
KG_DB = NOTES_DIR / "knowledge.db"

mcp = FastMCP("hackmonty-mcp")


# ── Knowledge Graph SQLite Backend ──────────────────────────────

def _kg_connect():
    """Get a connection to the knowledge graph database."""
    db = sqlite3.connect(str(KG_DB))
    db.row_factory = sqlite3.Row
    return db

def _kg_init():
    """Initialize knowledge graph schema."""
    db = _kg_connect()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            iteration INTEGER NOT NULL,
            vector TEXT NOT NULL,
            template TEXT DEFAULT '',
            code TEXT NOT NULL DEFAULT '',
            score INTEGER NOT NULL DEFAULT 0,
            label TEXT DEFAULT '',
            context TEXT DEFAULT '',
            reason TEXT NOT NULL DEFAULT '',
            snapshot_kinds TEXT DEFAULT '[]',
            timestamp TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS discoveries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT DEFAULT 'finding',
            what TEXT NOT NULL,
            details TEXT DEFAULT '',
            refs TEXT DEFAULT '[]',
            confidence TEXT DEFAULT 'confirmed',
            score INTEGER DEFAULT 0,
            timestamp TEXT DEFAULT (datetime('now'))
        );
        CREATE VIEW IF NOT EXISTS vector_status AS
        SELECT vector,
               COUNT(*) as attempts,
               MAX(score) as best_score,
               CASE WHEN MAX(score) = 0 AND COUNT(*) >= 2 THEN 'dead'
                    WHEN MAX(score) > 0 THEN 'promising'
                    WHEN COUNT(*) = 0 THEN 'untried'
                    ELSE 'active' END as status
        FROM attempts GROUP BY vector;
        CREATE VIEW IF NOT EXISTS recent_attempts AS
        SELECT id, iteration, vector, score, reason, timestamp
        FROM attempts ORDER BY id DESC LIMIT 50;
    """)
    db.commit()
    db.close()

def _kg_record(iteration: int, vector: str, code: str, score: int,
               label: str, context: str, reason: str,
               template: str = "", snapshot_kinds: list = None):
    """Record an attempt in the knowledge graph."""
    db = _kg_connect()
    db.execute(
        "INSERT INTO attempts (iteration, vector, template, code, score, label, context, reason, snapshot_kinds) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (iteration, vector, template, code, score, label, context, reason,
         json.dumps(snapshot_kinds or []))
    )
    db.commit()
    db.close()

# Initialize on import
_kg_init()




# ── Execution Layer ────────────────────────────────────────────

@mcp.tool()
async def hackmonty_run(code: str, reason: str = "") -> str:
    """Run Python code in sandbox. 'reason' is REQUIRED — explain WHY you're trying this.

    Returns JSON: success, error, output, print_output, num_snapshots,
    snapshot_kinds, elapsed_ms, total_resumes, context.
    Automatically records the attempt to the knowledge graph.
    """
    from hackmonty_client import AsyncHackMontyClient
    from evaluate import enrich_context, evaluate, SCORE_LABELS

    client = AsyncHackMontyClient(
        user_secret=os.environ.get("USER_SECRET", ""), concurrency=1
    )
    try:
        result = await client.run_code(code)
        kinds = [s.kind for s in result.snapshots]
        raw = {
            "success": result.success,
            "error": (result.error or "")[:500],
            "output": str(result.raw_response.get("output", ""))[:500],
            "print_output": result.raw_response.get("print_output", "")[:500],
            "num_snapshots": len(result.snapshots),
            "snapshot_kinds": kinds,
            "elapsed_ms": result.elapsed_ms,
            "total_resumes": result.total_resumes,
            "context": enrich_context(result),
        }
        # Auto-evaluate and record to knowledge graph
        er = evaluate(result)
        state = json.loads(state_read()) if STATE_FILE.exists() else {}
        iteration = state.get("last_iteration", 0) + 1
        _kg_record(
            iteration=iteration,
            vector=reason.split(":")[0] if reason else "unknown",
            code=code,
            score=er.score,
            label=SCORE_LABELS.get(er.score, ""),
            context=raw["context"],
            reason=reason or "no reason given",
            snapshot_kinds=kinds,
        )
        return json.dumps(raw)
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


# ── Attempt & State Layer ──────────────────────────────────────

@mcp.tool()
def attempt_save(iteration: int, template: str, code: str,
                 score: int, label: str, context: str, reason: str = "") -> str:
    """Save an attempt to disk. 'reason' is REQUIRED — document why this was attempted.
    Auto-records to knowledge graph. Returns {path}."""
    from datetime import datetime, timezone
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    d = ATTEMPTS_DIR / date_str
    d.mkdir(parents=True, exist_ok=True)
    n = len(list(d.glob("attempt_*.md"))) + 1

    content = f"""# Attempt {iteration:03d} - {datetime.now(timezone.utc).isoformat()}
## Template: {template} | Score: {score} - {label}
## Reason: {reason}
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

    # Auto-record to knowledge graph
    _kg_record(
        iteration=iteration, vector=template, code=code,
        score=score, label=label, context=context,
        reason=reason or "no reason given"
    )

    return json.dumps({"path": str(path)})


@mcp.tool()
def state_read() -> str:
    """Read orchestrator state: iteration, score_counts."""
    if STATE_FILE.exists():
        return STATE_FILE.read_text()
    return json.dumps({"last_iteration": 0, "score_counts": {}})


@mcp.tool()
def state_write(iteration: int, score_counts_json: str):
    """Save orchestrator state for resume."""
    from datetime import datetime, timezone
    sc = json.loads(score_counts_json)
    STATE_FILE.write_text(json.dumps({
        "last_iteration": iteration, "score_counts": sc,
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


# ── Knowledge Graph Tools ──────────────────────────────────────

@mcp.tool()
def kg_discover(category: str, what: str, details: str = "",
                refs_json: str = "[]", confidence: str = "confirmed") -> str:
    """Record a discovery in the knowledge graph.
    category: blocked, available, technique, cve, finding
    refs_json: JSON array of {url, title} from web research.
    """
    db = _kg_connect()
    db.execute(
        "INSERT INTO discoveries (category, what, details, refs, confidence) VALUES (?, ?, ?, ?, ?)",
        (category, what, details, refs_json, confidence)
    )
    db.commit()
    db.close()
    return json.dumps({"ok": True, "discovery": what})

@mcp.tool()
def kg_dashboard() -> str:
    """Full knowledge graph dashboard: vector_status + recent attempts."""
    db = _kg_connect()
    vectors = [dict(r) for r in db.execute("SELECT * FROM vector_status ORDER BY status, best_score DESC").fetchall()]
    recent = [dict(r) for r in db.execute("SELECT * FROM recent_attempts").fetchall()]
    discoveries = [dict(r) for r in db.execute(
        "SELECT category, what, details, refs, confidence FROM discoveries ORDER BY id DESC LIMIT 20"
    ).fetchall()]
    db.close()
    return json.dumps({
        "vectors": vectors,
        "recent_attempts": recent,
        "discoveries": discoveries,
    }, indent=2)

@mcp.tool()
def kg_dead_vectors() -> str:
    """Return JSON list of vectors with status='dead'."""
    db = _kg_connect()
    rows = [dict(r) for r in db.execute(
        "SELECT vector, attempts, best_score FROM vector_status WHERE status='dead' ORDER BY vector"
    ).fetchall()]
    db.close()
    return json.dumps(rows)

@mcp.tool()
def kg_recent(n: int = 50) -> str:
    """Return last N attempts from the knowledge graph."""
    db = _kg_connect()
    rows = [dict(r) for r in db.execute(
        "SELECT id, iteration, vector, score, reason, timestamp FROM attempts ORDER BY id DESC LIMIT ?", (n,)
    ).fetchall()]
    db.close()
    return json.dumps(rows)

@mcp.tool()
def kg_query(sql: str) -> str:
    """Run a read-only SQL query against the knowledge graph."""
    if not sql.strip().upper().lstrip().startswith("SELECT"):
        return json.dumps({"error": "Only SELECT queries allowed"})
    db = _kg_connect()
    try:
        rows = [dict(r) for r in db.execute(sql).fetchall()]
        db.close()
        return json.dumps(rows)
    except Exception as e:
        db.close()
        return json.dumps({"error": str(e)})

@mcp.tool()
def kg_bootstrap(force: bool = False) -> str:
    """One-time migration of all existing data into the knowledge graph.
    Set force=true to re-import even if DB already has data.
    Imports: attempt_*.md files, findings.md, understanding/*.md, state.json.
    """
    db = _kg_connect()
    count = db.execute("SELECT COUNT(*) as n FROM attempts").fetchone()["n"]
    if count > 0 and not force:
        db.close()
        return json.dumps({"ok": True, "note": f"Already has {count} attempts", "count": count})

    if force:
        db.execute("DELETE FROM attempts")
        db.execute("DELETE FROM discoveries")
        db.commit()

    state = json.loads(state_read())
    last_iteration = state.get("last_iteration", 0)
    imported_attempts = 0
    imported_discoveries = 0
    date_dirs = 0

    # 1. Import ALL attempt files from ALL date directories
    for attempt_dir in sorted(ATTEMPTS_DIR.glob("*")):
        if not attempt_dir.is_dir():
            continue
        date_dirs += 1
        for f in sorted(attempt_dir.glob("attempt_*.md")):
            try:
                text = f.read_text()[:3000]
                template = ""
                score = 0
                label = ""
                context = ""
                code = ""
                in_code = False
                code_lines = []
                for line in text.split("\n"):
                    if "Template:" in line and "Score:" in line:
                        parts = line.split("|")
                        template = parts[0].split(":")[-1].strip() if len(parts) > 0 else ""
                        try:
                            score_part = parts[1].split(":")[-1].strip() if len(parts) > 1 else "0"
                            score = int(score_part.split()[0])
                        except:
                            pass
                    if "```python" in line:
                        in_code = True
                        continue
                    if in_code:
                        if "```" in line:
                            in_code = False
                        else:
                            code_lines.append(line)
                # Extract context + reason
                if "Context:" in text:
                    ctx_start = text.index("Context:") + 9
                    context = text[ctx_start:].split("\n")[0].strip()[:500]
                if "Score:" in text and "/5" in text:
                    parts = text.split("Score:")[-1].split("/5")[0].strip()
                    label = parts if parts else ""

                db.execute(
                    "INSERT INTO attempts (iteration, vector, template, code, score, label, context, reason) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (last_iteration, template, template,
                     "\n".join(code_lines[-50:]), score, label,
                     context or "Imported", f"Imported from {f.name}")
                )
                imported_attempts += 1
            except Exception:
                pass
    db.commit()

    # 2. Import findings.md into discoveries
    findings_file = RESULTS_DIR / "findings.md"
    if findings_file.exists():
        try:
            ft = findings_file.read_text()
            for block in ft.split("## ["):
                if not block.strip():
                    continue
                lines = block.strip().split("\n")
                header = lines[0].rstrip("]") if lines else ""
                body = "\n".join(lines[1:]).strip()[:2000]
                if header and body:
                    db.execute(
                        "INSERT INTO discoveries (category, what, details, refs, confidence) VALUES (?, ?, ?, ?, ?)",
                        ("finding", f"Finding: {header}", body, "[]", "confirmed")
                    )
                    imported_discoveries += 1
        except Exception:
            pass
        db.commit()

    # 3. Import understanding files as discoveries
    ud = NOTES_DIR / "understanding"
    if ud.exists():
        for f in sorted(ud.glob("*.md")):
            try:
                name = f.stem.replace("_", " ").title()
                content = f.read_text()[:5000]
                db.execute(
                    "INSERT INTO discoveries (category, what, details, confidence) VALUES (?, ?, ?, ?)",
                    ("analysis", f"Understanding: {name}", content, "medium")
                )
                imported_discoveries += 1
            except Exception:
                pass
        db.commit()

    db.close()
    return json.dumps({
        "ok": True,
        "imported_attempts": imported_attempts,
        "imported_discoveries": imported_discoveries,
        "date_directories": date_dirs,
        "last_iteration": last_iteration,
    })

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
