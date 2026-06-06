# Attempt 365 - 2026-06-05T23:20:43.769712+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Create 3-5 coroutines via `asyncio.gather()` where each coroutine allocates objects in a loop, creates cyclic references to force tracing GC, then `await`s on an external operation (e.g., `Path.read_text()`) to force a suspension point. While suspended, the coroutine's frame and locals must remain alive but may be missing from GC root set - similar to the Round 1 sort bug. After all coroutines complete, check if any frame state is corrupted, if references were freed prematurely, or if the secret

## Exploit code
```python
expected_len = 40
        if final_len != expected_len:
            print(f"CORRUPT: coro {coroid} has {final_len} items (expected {expected_len})")
        if first_id != coroid * 1000:
            print(f"ID_MISMATCH: coro {coroid} first_id={first_id}")
        print(f"Coro {coroid}: len={final_len}, content_preview={content}")
```

## Result
Category: no_findings
Context: Unexpected indentation
Details: Unknown error
```
Success: False
Elapsed: 716ms
Resumes: 0
Snapshots: 0
Error: Unexpected indentation
```

## Analysis
- Unexpected indentation
- Verdict: Not exploitable
