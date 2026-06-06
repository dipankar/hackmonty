# Attempt 156 - 2026-06-05T22:21:44.427620+00:00
## Template: J | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Create multiple coroutines that each allocate objects and then await. The asyncio.gather machinery creates futures and coroutine frames. If these frames aren't in the GC root set during an await suspension point, and if the await triggers GC, the coroutine frames could be freed while still referenced by the gather future.

## Exploit code
```python
async def stress_gather():
    print("=== ASYNC GC ROOT TEST ===")
    tasks = [alloc_then_await(i) for i in range(6)]
    print(f"Created {len(tasks)} coroutines")
    results = await asyncio.gather(*tasks)
    print(f"Results: {results}")
    print(f"Frame states: {frame_states}")
    print(f"Allocations: {alloc_tracker[0]}")
    if len(frame_states) != 12:
        print("CORRUPTION: Missing frame state entries!")
    if results != [0, 1, 2, 3, 4, 5]:
        print("CORRUPTION: Wrong results order!")
```

## Result
Category: no_findings
Context: no detail
Details: Completed with no notable findings
```
Success: True
Elapsed: 614ms
Resumes: 0
Snapshots: 0
Print: 
```

## Analysis
- Completed with no findings
- Verdict: Try different template
