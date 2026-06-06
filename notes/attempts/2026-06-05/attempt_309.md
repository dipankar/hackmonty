# Attempt 307 - 2026-06-05T23:03:39.355528+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Execute asyncio.gather GC race

## Exploit code
```python
async def main():
    tasks = [worker(i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    for r in results:
        coro_results.append(r)
    print(f"ALLOC:{alloc_counter[0]}")
    print(f"RESULTS:{coro_results}")
    expected = [(i, f"W{i}_PRE", f"W{i}_POST") for i in range(5)]
    if results != expected:
        print("CORRUPTION_DETECTED")
```

## Result
Category: no_findings
Context: no detail
Details: Completed with no notable findings
```
Success: True
Elapsed: 515ms
Resumes: 0
Snapshots: 0
Print: 
```

## Analysis
- Completed with no findings
- Verdict: Try different template
