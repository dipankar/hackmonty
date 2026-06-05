"""Evaluate exploit results on a 0-5 scale.

Scoring logic:
  0 - Standard Python/Monty error, syntax error, expected sandbox behavior
  1 - Crash/Panic caused (segfault, stack overflow, actual panic)
  2 - Interesting: unexpected snapshot, internal error, or new Monty behavior
  3 - Host info leak: Rust backtrace, host file paths exposed
  4 - File read: non-public file content in the `output` field (not print_output)
  5 - Secret found: target secret detected
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from hackmonty_client import RunResult


SCORE_LABELS = {
    0: "Nothing - standard error or expected sandbox behavior",
    1: "Crash/Panic - segfault, stack overflow, or actual panic",
    2: "Interesting - unexpected behavior, snapshot, or internal error",
    3: "Host Info - Rust traceback, host paths, or internal details leaked",
    4: "Filesystem Read - non-public file content in output field",
    5: "SECRET FOUND - target secret extracted",
}


@dataclass
class EvalResult:
    score: int
    label: str
    category: str = ""
    details: list[str] = field(default_factory=list)
    raw_analysis: str = ""


# Standard Monty/Python errors that are NOT interesting
STANDARD_ERRORS = (
    "syntaxerror", "typeerror", "nameerror", "attributeerror",
    "valueerror", "keyerror", "importerror", "modulenotfound",
    "notimplementederror", "notimplemented", "eof", "indentationerror",
    "unterminated string", "unterminated",
)

# Errors that indicate a crash/panic (score 1)
CRASH_INDICATORS = (
    "panic", "panicked", "segfault", "segmentation fault",
    "stack overflow", "stackoverflow", "null pointer",
    "abort", "aborted",
)

# Errors that indicate Monty internal issues (score 2)
INTERNAL_INDICATORS = (
    "rust", "monty internal", "internal error", "invariant",
    "assertion failed", "assertion",
)

# Host path indicators (score 3)
HOST_PATH_INDICATORS = (
    "/home/", "/usr/", "/var/", "/proc/", "cargo", "target/",
    ".rs:", ".cargo", "/root/",
)


def evaluate(result: RunResult) -> EvalResult:
    """Score a run result from 0-5."""
    details: list[str] = []

    # Aggregate all output for secret detection
    all_output = ""
    if result.raw_response:
        all_output += str(result.raw_response.get("output", ""))
        all_output += str(result.raw_response.get("print_output", ""))
    if result.error:
        all_output += str(result.error)
    for snap in result.snapshots:
        all_output += str(snap.data.get("output", ""))
        all_output += str(snap.data.get("print_output", ""))
        all_output += snap.stdout
        all_output += snap.stderr

    # Check for secret first (highest priority)
    secret_indicators = check_for_secret(all_output)
    if secret_indicators:
        return EvalResult(score=5, label=SCORE_LABELS[5],
                          category="secret_found", details=secret_indicators)

    # Check error cases
    if not result.success and result.error:
        error_text = result.error.lower()

        # Score 0: Standard errors
        if any(w in error_text for w in STANDARD_ERRORS):
            return EvalResult(score=0, label=SCORE_LABELS[0],
                              category="standard_error",
                              details=[result.error[:200]])

        # Score 0: PermissionError (expected sandbox behavior)
        if any(w in error_text for w in ("permissionerror", "permission denied",
                                          "permissiondenied", "access denied")):
            return EvalResult(score=0, label=SCORE_LABELS[0],
                              category="sandbox_permission",
                              details=["Sandbox permission block (expected)"])

        # Score 0: MemoryError (resource limit, not exploitable)
        if "memoryerror" in error_text:
            return EvalResult(score=0, label=SCORE_LABELS[0],
                              category="resource_exhaustion",
                              details=["Resource limit hit (expected sandbox behavior)"])

        # Score 1: Actual crash/panic
        if any(w in error_text for w in CRASH_INDICATORS):
            return EvalResult(score=1, label=SCORE_LABELS[1],
                              category="crash",
                              details=[result.error[:300]])

        # Score 2: Internal Monty error
        if any(w in error_text for w in INTERNAL_INDICATORS):
            details.append("Monty internal error triggered")
            return EvalResult(score=2, label=SCORE_LABELS[2],
                              category="monty_internal",
                              details=details + [result.error[:300]])

        # Score 3: Traceback with host paths
        if any(w in error_text for w in ("traceback", "backtrace", "tb_frame")):
            if any(p in result.error for p in HOST_PATH_INDICATORS):
                details.append("Traceback with host paths")
                return EvalResult(score=3, label=SCORE_LABELS[3],
                                  category="host_traceback",
                                  details=details + [result.error[:500]])
            # Standard traceback without host paths = score 0
            return EvalResult(score=0, label=SCORE_LABELS[0],
                              category="standard_traceback",
                              details=["Standard traceback, no host info"])

    # Check snapshot data for interesting findings
    for snap in result.snapshots:
        if snap.traceback:
            if any(p in (snap.traceback or "").lower()
                   for p in HOST_PATH_INDICATORS):
                details.append("Snapshot traceback with host paths")
                return EvalResult(score=3, label=SCORE_LABELS[3],
                                  category="host_snapshot",
                                  details=details + [snap.traceback[:500]])

        if snap.monty_error:
            err = (snap.monty_error or "").lower()
            if any(w in err for w in CRASH_INDICATORS):
                return EvalResult(score=1, label=SCORE_LABELS[1],
                                  category="snapshot_crash",
                                  details=[snap.monty_error[:300]])
            if any(w in err for w in INTERNAL_INDICATORS):
                return EvalResult(score=2, label=SCORE_LABELS[2],
                                  category="snapshot_internal",
                                  details=[snap.monty_error[:300]])
            if any(p in err for p in HOST_PATH_INDICATORS):
                return EvalResult(score=3, label=SCORE_LABELS[3],
                                  category="snapshot_host_info",
                                  details=[snap.monty_error[:500]])

        # Score 2: Unexpected snapshot kind
        if snap.kind not in ("function_snapshot", "name_lookup_snapshot",
                              "future_snapshot", "completed", "complete",
                              "runtime_error", "syntax_error", "typing_error"):
            details.append(f"Unexpected snapshot kind: {snap.kind}")
            return EvalResult(score=2, label=SCORE_LABELS[2],
                              category="unusual_snapshot", details=details)

    # Handle successful completion
    if result.success and result.raw_response:
        raw = result.raw_response
        output = str(raw.get("output", "")) if raw.get("output") is not None else ""
        print_output = str(raw.get("print_output", ""))

        # Score 4: actual output (not print_output) + non-None output
        # This means the sandboxed code returned a value via `return` or expression
        if raw.get("output") is not None and output and output != "None":
            # Check if it's a real data leak vs just echo
            if any(p in output for p in ("/etc/", "/proc/", "/app/", "/home/")):
                if not any(e in output for e in ("PermissionError", "Permission denied")):
                    return EvalResult(score=4, label=SCORE_LABELS[4],
                                      category="non_public_file_read",
                                      details=[f"Output from non-/data path: {output[:500]}"])
            # Generic non-None output - could be interesting
            if len(output) > 20:
                details.append(f"Code returned value: {output[:200]}")

        # Check print output for host paths
        combined = output + print_output
        if any(w in combined.lower() for w in ("/etc/", "/proc/", "/app/", "/home/")):
            if not any(e in combined for e in ("PermissionError", "Permission denied")):
                return EvalResult(score=3, label=SCORE_LABELS[3],
                                  category="host_paths_in_output",
                                  details=[combined[:300]])

        if details:
            return EvalResult(score=0, label=SCORE_LABELS[0],
                              category="success_no_findings", details=details)

    # Collect stdout/stderr for informational purposes
    stdout_collected = ""
    stderr_collected = ""
    for snap in result.snapshots:
        stdout_collected += snap.stdout
        stderr_collected += snap.stderr

    if stdout_collected:
        details.append(f"stdout: {len(stdout_collected)} chars")
    if stderr_collected:
        details.append(f"stderr: {len(stderr_collected)} chars")

    if result.success:
        details.append("Completed with no notable findings")
    elif not details:
        details.append("Unknown error")

    return EvalResult(score=0, label=SCORE_LABELS[0],
                      category="no_findings", details=details)


def check_for_secret(output: str) -> list[str]:
    """Check if output contains the target secret.

    The secret format is unknown, but common patterns are checked.
    The real detector is: any unexpected non-None output from a non-/data
    path is flagged by the main evaluator.
    """
    indicators = []

    if not output or len(output) < 3:
        return indicators

    if any(w in output.lower() for w in ("secret{", "flag{", "bounty{")):
        indicators.append("Found known secret pattern")
        indicators.append(f"SECRET: {output[:1000]}")
        return indicators

    return indicators


def enrich_context(result: RunResult) -> str:
    """Extract rich snapshot detail for analyst context, not just scores."""
    import re
    parts = []

    if result.snapshots:
        for s in result.snapshots[:3]:
            if s.kind == "function_snapshot":
                fname = s.data.get("function_name", "?")
                parts.append(f"func_snap({fname})")
            elif s.kind == "name_lookup_snapshot":
                name = s.data.get("name", "?")
                parts.append(f"name_lookup({name})")
            elif s.kind == "future_snapshot":
                n = len(s.data.get("pending_snapshot_ids", []))
                parts.append(f"future({n} pending)")
            else:
                parts.append(s.kind[:25])

    if result.error:
        # Extract Python-level error type first (most common, least detailed)
        py_err = re.search(r"(SyntaxError|NameError|TypeError|AttributeError|ValueError|"
                           r"KeyError|ImportError|ModuleNotFoundError|IndexError|"
                           r"ZeroDivisionError|RuntimeError|FileNotFoundError|"
                           r"IsADirectoryError|NotADirectoryError|TimeoutError|"
                           r"MemoryError|RecursionError|PermissionError|"
                           r"NotImplementedError|AssertionError|OSError)"
                           r"(?::\s*(.+?))?(?:\n|$)", result.error)
        if py_err:
            err_type = py_err.group(1)
            err_msg = (py_err.group(2) or "")[:60].strip()
            parts.append(f"{err_type}: {err_msg}" if err_msg else err_type)
        else:
            first_line = result.error.split('\n')[0][:80]
            if first_line:
                parts.append(first_line)

        alloc = re.search(r"allocation limit exceeded: (\d+) > (\d+)", result.error)
        mem = re.search(r"memory limit exceeded: (\d+) bytes > (\d+)", result.error)
        perm = re.search(r"Permission denied: '([^']+)'", result.error)
        notimpl = re.search(r"NotImplementedError: (.+?)(?:\n|$)", result.error)

        if alloc:
            parts.append(f"alloc({alloc.group(1)}/{alloc.group(2)})")
        if mem:
            parts.append(f"mem({mem.group(1)}/{mem.group(2)})")
        if perm:
            parts.append(f"PermDenied({perm.group(1)[:60]})")
        if notimpl:
            parts.append(f"NotImpl({notimpl.group(1)[:60]})")

    if result.success and result.raw_response:
        output = str(result.raw_response.get("output", ""))
        if output and output != "None":
            parts.append(f"output({len(output)} chars)")

    return "; ".join(parts) if parts else "no detail"


def output_hash(result: RunResult) -> str:
    """Stable hash of result output for re-validation comparison."""
    import hashlib
    content = ""
    if result.raw_response:
        content += str(result.raw_response.get("output", ""))
        content += str(result.raw_response.get("print_output", ""))
    if result.error:
        content += result.error
    return hashlib.blake2b(content.encode()).hexdigest()[:16]
