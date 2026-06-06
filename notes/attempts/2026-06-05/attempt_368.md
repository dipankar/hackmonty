# Attempt 366 - 2026-06-05T23:20:55.711416+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Create 3-5 coroutines via `asyncio.gather()` where each allocates cyclical dict objects then awaits an external snapshot trigger. During the await suspension, force GC pressure by creating self-referential dicts in the main coroutine. When the gathered coroutines resume, check if their local state was corrupted by use-after-free during the GC window. If object memory was reused, the resumed coroutine will access freed/reallocated memory, potentially leaking heap layout or triggering a panic that

## Exploit code
```python
async def main():
    workers = [worker(i) for i in range(4)]
    pressure = gc_pressure()
    results = await asyncio.gather(*workers)
    await pressure
    print(f"Results: {results}")
    print(f"GC events: {len(gc_events)}")
    for evt in gc_events:
        print(evt)
```

## Result
Category: no_findings
Context: no detail
Details: Completed with no notable findings
```
Success: True
Elapsed: 265ms
Resumes: 0
Snapshots: 0
Print: 
```

## Analysis
- Completed with no findings
- Verdict: Try different template
