"""Name lookup protocol fuzzer — tests the hackmonty.com snapshot/resume boundary."""

from __future__ import annotations

import json
import time
import sys
from dataclasses import dataclass
from typing import Any

import httpx


BASE = "https://hackmonty.com"
HEADERS = {
    "content-type": "application/json",
    "User": "ba1947fe94653d023fee9ee177c17c93ce2baee8b4aca18f5164e4d3304c79f4",
}
COOLDOWN = 0.5


@dataclass
class FuzzResult:
    test: str
    status: int
    kind: str = ""
    body: dict = None
    error: str = ""

    def __post_init__(self):
        if self.body is None:
            self.body = {}


def api_post(path: str, json_data: dict) -> tuple[int, dict]:
    time.sleep(COOLDOWN)
    resp = httpx.post(f"{BASE}{path}", headers=HEADERS, json=json_data)
    try:
        return resp.status_code, resp.json()
    except Exception:
        return resp.status_code, {"raw": resp.text[:500]}


def fuzz_name_lookup_resume() -> list[FuzzResult]:
    """Test name lookup resume with various value types."""
    results = []

    # Get a name_lookup snapshot
    status, snap = api_post("/run/", {"code": "print(x)"})
    if snap.get("kind") != "name_lookup_snapshot":
        results.append(FuzzResult("setup", status, snap.get("kind", "")))
        return results

    sid = snap["snapshot_id"]
    print(f"  snapshot: {sid}")

    # Test various resume values
    test_values = [
        ("none", None),
        ("int", 42),
        ("neg_int", -1),
        ("large_int", 2**63 - 1),
        ("float", 3.14),
        ("string", "hello"),
        ("empty_str", ""),
        ("long_str", "A" * 1000),
        ("bool_t", True),
        ("bool_f", False),
        ("list", [1, 2, 3]),
        ("nested_list", [1, [2, [3]]]),
        ("dict", {"a": 1}),
        ("nested_dict", {"a": {"b": {"c": 1}}}),
        ("null_byte", "abc\x00def"),
        ("unicode", "こんにちは"),
        ("path_str", "/etc/secrets/hackmonth.txt"),
        ("json_str", '{"key": "value"}'),
    ]

    for label, val in test_values:
        status, resp = api_post(f"/run/{sid}/", {
            "kind": "name_lookup",
            "value": val,
        })
        results.append(FuzzResult(
            f"resume_{label}",
            status,
            resp.get("kind", ""),
            resp,
        ))

        # Create fresh snapshot for each test
        status, snap = api_post("/run/", {"code": "print(x)"})
        if snap.get("kind") == "name_lookup_snapshot":
            sid = snap["snapshot_id"]

    return results


def fuzz_function_resume() -> list[FuzzResult]:
    """Test function snapshot resume with crafted payloads."""
    results = []

    # Get a function_snapshot
    code = "async def f():\n    x = await ext_func()\n    return x\nimport asyncio\nasyncio.run(f())"
    status, snap = api_post("/run/", {"code": code})

    if snap.get("kind") != "function_snapshot":
        results.append(FuzzResult("setup_func", status, snap.get("kind", "")))
        return results

    sid = snap["snapshot_id"]
    print(f"  func snapshot: {sid}")

    # Test malformed function resumes
    test_payloads = [
        ("normal_return", {"kind": "function", "result": {"return_value": 42}}),
        ("string_return", {"kind": "function", "result": {"return_value": "data"}}),
        ("none_return", {"kind": "function", "result": {"return_value": None}}),
        ("list_return", {"kind": "function", "result": {"return_value": [1,2,3]}}),
        ("future_marker", {"kind": "function", "result": "future"}),
        ("exception_base", {"kind": "function", "result": {"exception_type": "ValueError", "exception_message": "test"}}),
        ("exception_path", {"kind": "function", "result": {"exception_type": "OSError", "exception_message": "/etc/secrets/hackmonth.txt"}}),
        ("both_values", {"kind": "function", "result": {"return_value": 42, "exception_type": "ValueError"}}),
        ("no_result", {"kind": "function"}),
        ("extra_field", {"kind": "function", "result": {"return_value": 42}, "extra": "data"}),
        ("result_not_object_1", {"kind": "function", "result": 42}),
        ("result_not_object_2", {"kind": "function", "result": "string"}),
    ]

    for label, payload in test_payloads:
        status, snap2 = api_post(f"/run/{sid}/", payload)
        results.append(FuzzResult(
            f"func_{label}",
            status,
            snap2.get("kind", ""),
            snap2,
        ))
        # Fresh snapshot each time
        status, snap = api_post("/run/", {"code": code})
        if snap.get("kind") == "function_snapshot":
            sid = snap["snapshot_id"]

    return results


def fuzz_malformed_requests() -> list[FuzzResult]:
    """Test API with malformed/invalid requests."""
    results = []

    tests = [
        ("empty_body", "/run/", {}),
        ("null_body", "/run/", None),
        ("bad_code_type", "/run/", {"code": 42}),
        ("missing_code", "/run/", {"inputs": {"x": 1}}),
        ("extra_field", "/run/", {"code": "1+1", "hack": "true"}),
        ("bad_limits", "/run/", {"code": "1+1", "limits": "wrong"}),
        ("negative_limits", "/run/", {"code": "1+1", "limits": {"max_memory": -100}}),
        ("large_limits", "/run/", {"code": "1+1", "limits": {"max_memory": 2**40}}),
        ("type_check_bool", "/run/", {"code": "1+1", "type_check": "yes"}),
        ("with_type_stub", "/run/", {"code": "x: int = 42", "type_check": True, "type_check_stubs": "x: int\n"}),
        ("bad_snapshot_id", "/run/not-a-uuid/", {"kind": "function", "result": {"return_value": 1}}),
        ("expired_snapshot", "/run/00000000-0000-0000-0000-000000000000/", {"kind": "function", "result": {"return_value": 1}}),
    ]

    for label, path, body in tests:
        status, resp = api_post(path, body if body is not None else {})
        results.append(FuzzResult(f"malformed_{label}", status, resp.get("kind", ""), resp))

    return results


def fuzz_concurrent_snapshots() -> list[FuzzResult]:
    """Test behavior with multiple concurrent snapshot states."""
    results = []

    # Create multiple snapshots in sequence
    snapshots = []
    for _ in range(3):
        status, snap = api_post("/run/", {
            "code": "async def f():\n    x = await ext()\n    return x\nimport asyncio\nasyncio.run(f())"
        })
        if snap.get("kind") == "function_snapshot":
            snapshots.append(snap["snapshot_id"])

    print(f"  Created {len(snapshots)} snapshots")

    # Try to resume the OLDEST snapshot (might have expired)
    if snapshots:
        sid = snapshots[0]
        status, resp = api_post(f"/run/{sid}/", {
            "kind": "function", "result": {"return_value": 42}
        })
        results.append(FuzzResult("old_snapshot", status, resp.get("kind", ""), resp))

    # Resume newest with exception containing path
    if len(snapshots) > 1:
        sid = snapshots[-1]
        status, resp = api_post(f"/run/{sid}/", {
            "kind": "function",
            "result": {"exception_type": "RuntimeError", "exception_message": "secret is at /app/secret.txt"}
        })
        results.append(FuzzResult("new_snapshot_exc", status, resp.get("kind", ""), resp))

    return results


def print_results(results: list[FuzzResult]):
    interesting = 0
    for r in results:
        marker = ""
        if r.status != 200 and r.status != 422:
            marker = " *** BAD STATUS ***"
        if r.kind not in ("completed", "runtime_error", "syntax_error", ""):
            marker = " *** UNEXPECTED KIND ***"
        if marker:
            interesting += 1
        print(f"  {r.test:35s} -> {r.status} {r.kind:25s}{marker}")
        if marker:
            body_str = str(r.body)[:200]
            print(f"    body: {body_str}")

    print(f"\n  Total: {len(results)}, Interesting: {interesting}")


def main():
    print("=== Phase 1: Name Lookup Fuzzing ===")
    r1 = fuzz_name_lookup_resume()
    print_results(r1)

    print("\n=== Phase 2: Function Resume Fuzzing ===")
    r2 = fuzz_function_resume()
    print_results(r2)

    print("\n=== Phase 3: Malformed Request Fuzzing ===")
    r3 = fuzz_malformed_requests()
    print_results(r3)

    print("\n=== Phase 4: Concurrent Snapshot Fuzzing ===")
    r4 = fuzz_concurrent_snapshots()
    print_results(r4)

    all_results = r1 + r2 + r3 + r4
    interesting = [r for r in all_results if r.kind not in ("completed", "runtime_error", "syntax_error", "") or r.status not in (200, 422)]
    print(f"\n{'='*60}")
    print(f"GRAND TOTAL: {len(all_results)} tests, {len(interesting)} interesting")
    for r in interesting:
        print(f"  {r.test} -> {r.status} {r.kind}")
        print(f"    {json.dumps(r.body, default=str)[:300]}")


if __name__ == "__main__":
    main()
