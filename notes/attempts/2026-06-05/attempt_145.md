# Attempt 145 - 2026-06-05T22:17:37.659043+00:00
## Template: B | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
1. Pre-allocate objects to fill counter to ~4,950
2. Create a list of objects with __lt__ that allocates 5+ objects per call
3. Call sorted() on them (without key=, to use py_cmp path)
4. MemoryError fires mid-sort
5. Check if anything weird happens

## Exploit code
```python
pool = []
for i in range(4900):
    pool.append({'id': i, 'pad': 'A' * 25})
```

## Result
Category: resource_exhaustion
Context: MemoryError: allocation limit exceeded: 5001 > 5000; alloc(5001/5000)
Details: Resource limit hit (expected sandbox behavior)
```
Success: False
Elapsed: 252ms
Resumes: 0
Snapshots: 0
Error: MemoryError: allocation limit exceeded: 5001 > 5000
Print: 
```

## Analysis
- MemoryError: allocation limit exceeded: 5001 > 5000
- Verdict: Not exploitable
