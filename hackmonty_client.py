"""API client for hackmonty.com - handles POST /run/ and snapshot/resume protocol."""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

import httpx


BASE_URL = "https://hackmonty.com"
RUN_URL = f"{BASE_URL}/run/"
COOLDOWN_SECS = 5.0
MAX_RESUMES = 200


@dataclass
class SnapshotResult:
    snapshot_id: str
    kind: str
    data: dict[str, Any]
    stdout: str = ""
    stderr: str = ""
    resume_count: int = 0
    final_output: Any = None
    error: str | None = None
    monty_error: str | None = None
    traceback: str | None = None


@dataclass
class RunResult:
    success: bool
    raw_response: dict[str, Any]
    error: str | None
    snapshots: list[SnapshotResult] = field(default_factory=list)
    total_resumes: int = 0
    elapsed_ms: float = 0.0


class HackMontyClient:
    def __init__(self, user_secret: str | None = None, cooldown: float = COOLDOWN_SECS):
        self.client = httpx.Client(timeout=30.0)
        self.cooldown = cooldown
        self.last_request_time = 0.0
        self.user_secret = user_secret
        self.headers: dict[str, str] = {"content-type": "application/json"}
        if user_secret:
            import hashlib

            user_hash = hashlib.sha256(user_secret.encode()).hexdigest()
            self.headers["User"] = user_hash

    def _cooldown(self):
        elapsed = time.monotonic() - self.last_request_time
        if elapsed < self.cooldown:
            time.sleep(self.cooldown - elapsed)
        self.last_request_time = time.monotonic()

    def run_code(self, code: str) -> RunResult:
        """POST code to /run/, follow snapshot/resume chain to completion."""
        result = RunResult(success=False, raw_response={}, error=None)
        start_time = time.monotonic()

        try:
            self._cooldown()
            resp = self.client.post(RUN_URL, headers=self.headers, json={"code": code})
            resp.raise_for_status()
            body = resp.json()
        except Exception as e:
            result.error = str(e)
            result.elapsed_ms = (time.monotonic() - start_time) * 1000
            return result

        result.raw_response = body

        kind = body.get("kind", "")
        snapshot_id = body.get("snapshot_id") or body.get("id", "")

        if kind in ("completed", "complete"):
            result.success = True
            if "output" in body:
                result.raw_response["output"] = body["output"]
            if "print_output" in body:
                result.raw_response["print_output"] = body["print_output"]
            result.elapsed_ms = (time.monotonic() - start_time) * 1000
            return result

        if kind == "error":
            result.error = body.get("message", "Unknown error")
            if "monty" in body:
                result.error = body.get("monty", result.error)
            result.elapsed_ms = (time.monotonic() - start_time) * 1000
            return result

        if kind in ("syntax_error", "typing_error"):
            result.error = body.get("error", f"Monty {kind}")
            result.elapsed_ms = (time.monotonic() - start_time) * 1000
            return result

        if kind == "runtime_error":
            result.error = body.get("error", "Runtime error")
            if body.get("traceback"):
                result.error += f"\nTraceback: {body['traceback']}"
            result.elapsed_ms = (time.monotonic() - start_time) * 1000
            return result

        if not snapshot_id:
            result.error = f"No snapshot ID for kind '{kind}' - body: {str(body)[:300]}"
            result.elapsed_ms = (time.monotonic() - start_time) * 1000
            return result

        snapshots_handled = 0
        while kind not in ("completed", "complete", "runtime_error", "syntax_error", "typing_error") and snapshots_handled < MAX_RESUMES:
            snap = SnapshotResult(
                snapshot_id=snapshot_id,
                kind=kind,
                data=body,
            )

            if kind == "function_snapshot":
                snap.final_output = {
                    "function_name": body.get("function_name", ""),
                    "args": body.get("args", []),
                    "kwargs": body.get("kwargs", {}),
                }
            elif kind == "name_lookup":
                snap.final_output = {
                    "name": body.get("name", ""),
                }
            elif kind == "monty_error":
                snap.monty_error = body.get("message", "")
            elif kind == "monty_traceback":
                snap.traceback = body.get("traceback", "")

            if "print_output" in body:
                snap.stdout += body.get("print_output", "")

            resume_payload = self._build_resume(kind, snapshot_id, body)

            try:
                self._cooldown()
                resume_url = f"{RUN_URL}{snapshot_id}/"
                resp = self.client.post(
                    resume_url, headers=self.headers, json=resume_payload
                )
                resp.raise_for_status()
                body = resp.json()
            except Exception as e:
                snap.error = str(e)
                result.snapshots.append(snap)
                result.error = f"Resume failed at snapshot {snapshots_handled}: {e}"
                result.total_resumes = result.total_resumes + 1
                result.elapsed_ms = (time.monotonic() - start_time) * 1000
                return result

            kind = body.get("kind", "")
            snapshot_id = body.get("snapshot_id") or body.get("id", "")

            if "print_output" in body:
                snap.stdout += body.get("print_output", "")

            result.snapshots.append(snap)
            snapshots_handled += 1

        result.total_resumes = snapshots_handled
        if kind in ("completed", "complete"):
            result.success = True
            result.raw_response = body
        elif kind in ("runtime_error", "syntax_error", "typing_error"):
            result.error = body.get("error", f"Monty {kind}")
        else:
            result.error = f"Max resumes ({MAX_RESUMES}) exceeded"
        result.elapsed_ms = (time.monotonic() - start_time) * 1000
        return result

    def _build_resume(self, kind: str, snapshot_id: str, body: dict | None = None) -> dict[str, Any]:
        """Build a resume payload based on snapshot kind."""
        if kind in ("function_snapshot",):
            return {
                "kind": "function",
                "result": {"return_value": None},
            }
        elif kind in ("name_lookup_snapshot",):
            return {
                "kind": "name_lookup",
                "value": None,
            }
        elif kind in ("future_snapshot",):
            pending_ids = (body or {}).get("pending_snapshot_ids", [])
            results = {pid: {"return_value": None} for pid in pending_ids}
            return {
                "kind": "future",
                "results": results,
            }
        else:
            return {"kind": kind}

    def close(self):
        self.client.close()


def format_result(result: RunResult) -> str:
    """Human-readable summary of a run result."""
    lines = []
    lines.append(f"Success: {result.success}")
    lines.append(f"Elapsed: {result.elapsed_ms:.0f}ms")
    lines.append(f"Resumes: {result.total_resumes}")
    lines.append(f"Snapshots: {len(result.snapshots)}")

    if result.error:
        lines.append(f"Error: {result.error[:500]}")

    for i, snap in enumerate(result.snapshots):
        lines.append(f"  [{i}] kind={snap.kind}")
        if snap.stdout:
            lines.append(f"      stdout: {snap.stdout[:200]}")
        if snap.stderr:
            lines.append(f"      stderr: {snap.stderr[:200]}")
        if snap.monty_error:
            lines.append(f"      monty_error: {snap.monty_error[:300]}")
        if snap.traceback:
            lines.append(f"      traceback: {snap.traceback[:300]}")
        if snap.error:
            lines.append(f"      client_error: {snap.error[:200]}")

    if result.raw_response:
        output = result.raw_response.get("output")
        print_output = result.raw_response.get("print_output")
        if output is not None:
            lines.append(f"Output: {str(output)[:500]}")
        if print_output is not None:
            lines.append(f"Print: {str(print_output)[:500]}")

    return "\n".join(lines)


# ── Async Client ──────────────────────────────────────────────────

import asyncio
import httpx as httpx_async


class AsyncHackMontyClient:
    """Async API client using httpx.AsyncClient for parallel workers."""

    BASE = "https://hackmonty.com"
    MAX_RESUMES = 200

    def __init__(self, user_secret: str | None = None, concurrency: int = 4):
        self.client = httpx_async.AsyncClient(
            timeout=30.0,
            limits=httpx_async.Limits(
                max_connections=concurrency * 3,
                max_keepalive_connections=concurrency * 2,
            ),
        )
        self.headers: dict[str, str] = {"content-type": "application/json"}
        if user_secret:
            import hashlib
            user_hash = hashlib.sha256(user_secret.encode()).hexdigest()
            self.headers["User"] = user_hash

    async def run_code(self, code: str) -> RunResult:
        result = RunResult(success=False, raw_response={}, error=None)
        import time as _time
        start_time = _time.monotonic()

        try:
            resp = await self.client.post(
                f"{self.BASE}/run/", headers=self.headers, json={"code": code}
            )
            resp.raise_for_status()
            body = resp.json()
        except Exception as e:
            result.error = str(e)
            result.elapsed_ms = (_time.monotonic() - start_time) * 1000
            return result

        result.raw_response = body
        kind = body.get("kind", "")
        snapshot_id = body.get("snapshot_id") or body.get("id", "")

        if kind in ("completed", "complete"):
            result.success = True
            result.raw_response["output"] = body.get("output")
            result.raw_response["print_output"] = body.get("print_output", "")
            result.elapsed_ms = (_time.monotonic() - start_time) * 1000
            return result

        if kind in ("runtime_error", "syntax_error", "typing_error"):
            result.error = body.get("error", f"Monty {kind}")
            result.elapsed_ms = (_time.monotonic() - start_time) * 1000
            return result

        if not snapshot_id:
            result.error = f"No snapshot ID for kind '{kind}'"
            result.elapsed_ms = (_time.monotonic() - start_time) * 1000
            return result

        resumes = 0
        while kind not in ("completed", "complete", "runtime_error", "syntax_error", "typing_error") and resumes < self.MAX_RESUMES:
            snap = SnapshotResult(
                snapshot_id=snapshot_id,
                kind=kind,
                data=body,
            )
            if kind == "function_snapshot":
                snap.final_output = {
                    "function_name": body.get("function_name", ""),
                    "args": body.get("args", []),
                    "kwargs": body.get("kwargs", {}),
                }
            elif kind == "name_lookup_snapshot":
                snap.final_output = {"name": body.get("name", "")}
            elif kind == "monty_error":
                snap.monty_error = body.get("message", "")
            elif kind == "monty_traceback":
                snap.traceback = body.get("traceback", "")

            if "print_output" in body:
                snap.stdout += body.get("print_output", "")

            if kind == "function_snapshot":
                resume_body = {"kind": "function", "result": {"return_value": None}}
            elif kind == "name_lookup_snapshot":
                resume_body = {"kind": "name_lookup", "value": None}
            elif kind == "future_snapshot":
                pending = body.get("pending_snapshot_ids", [])
                resume_body = {"kind": "future", "results": {p: {"return_value": None} for p in pending}}
            else:
                resume_body = {"kind": kind}

            try:
                resp = await self.client.post(
                    f"{self.BASE}/run/{snapshot_id}/",
                    headers=self.headers,
                    json=resume_body,
                )
                resp.raise_for_status()
                body = resp.json()
            except Exception as e:
                snap.error = str(e)
                result.snapshots.append(snap)
                result.error = f"Resume failed at snapshot {resumes}: {e}"
                result.total_resumes = resumes
                result.elapsed_ms = (_time.monotonic() - start_time) * 1000
                return result

            kind = body.get("kind", "")
            snapshot_id = body.get("snapshot_id") or body.get("id", "")
            if "print_output" in body:
                snap.stdout += body.get("print_output", "")
            result.snapshots.append(snap)
            resumes += 1

        result.total_resumes = resumes
        if kind in ("completed", "complete"):
            result.success = True
            result.raw_response = body
        elif kind in ("runtime_error", "syntax_error", "typing_error"):
            result.error = body.get("error", f"Monty {kind}")
        else:
            result.error = f"Max resumes ({self.MAX_RESUMES}) exceeded"
        result.elapsed_ms = (_time.monotonic() - start_time) * 1000
        return result

    async def close(self):
        await self.client.aclose()

