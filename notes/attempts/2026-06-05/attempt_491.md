# Attempt 489 - 2026-06-05T23:56:29.333029+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
1. Create a list of objects (maybe tuples or simple objects)
2. Use sorted() without key= to trigger __lt__ comparisons
3. Each comparison allocates memory (by having complex elements)
4. Push allocation counter to limit during sort
5. MemoryError fires mid-sort
6. Error reveals internal state

## Exploit code
```python
alloc_pool = []
for i in range(4800):
    alloc_pool.append({'id': i, 'pad': 'A' * 20})
```

## Result
Category: resource_exhaustion
Context: MemoryError: allocation limit exceeded: 5001 > 5000; alloc(5001/5000)
Details: Resource limit hit (expected sandbox behavior)
```
Success: False
Elapsed: 248ms
Resumes: 0
Snapshots: 0
Error: MemoryError: allocation limit exceeded: 5001 > 5000
Print: 
```

## Analysis
- MemoryError: allocation limit exceeded: 5001 > 5000
- Verdict: Not exploitable
