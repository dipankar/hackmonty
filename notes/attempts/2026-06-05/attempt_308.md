# Attempt 306 - 2026-06-05T23:03:10.988273+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Execute asyncio.gather GC race

## Exploit code
```python
coro_states.append(f"W{id}_PRE_AWAIT")
    await asyncio.sleep(0)
    coro_states.append(f"W{id}_POST_AWAIT")
```

## Result
Category: no_findings
Context: Unexpected indentation
Details: Unknown error
```
Success: False
Elapsed: 308ms
Resumes: 0
Snapshots: 0
Error: Unexpected indentation
```

## Analysis
- Unexpected indentation
- Verdict: Not exploitable
