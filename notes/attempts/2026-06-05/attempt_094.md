# Attempt 093 - 2026-06-05T22:01:47.015222+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Create an `async main()` that uses `asyncio.gather()` with 3-4 coroutines, each allocating ~150 dict objects with string padding to consume allocations mid-gather. Inside each coroutine, yield control (`await asyncio.sleep(0)`) after partial allocation so the event loop can interleave coroutines while the gather future is still building. If the gather's internal state machine or future coroutine references aren't in the GC root set, one coroutine's frame may be freed prematurely, leading to a us

## Exploit code
```python
local_allocs = []
    for i in range(iterations):
        obj = {'worker': id, 'iter': i, 'pad': 'X' * 40}
        local_allocs.append(obj)
        alloc_pool.append(obj)
```

## Result
Category: no_findings
Context: Unexpected indentation
Details: Unknown error
```
Success: False
Elapsed: 616ms
Resumes: 0
Snapshots: 0
Error: Unexpected indentation
```

## Analysis
- Unexpected indentation
- Verdict: Not exploitable
