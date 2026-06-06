# Attempt 330 - 2026-06-05T23:09:58.965411+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Execute sort() py_cmp callback flood

## Exploit code
```python
pressure = []
for i in range(4850):
    pressure.append({'id': i, 'pad': 'P' * 15})
```

## Result
Category: resource_exhaustion
Context: MemoryError: allocation limit exceeded: 5001 > 5000; alloc(5001/5000)
Details: Resource limit hit (expected sandbox behavior)
```
Success: False
Elapsed: 316ms
Resumes: 0
Snapshots: 0
Error: MemoryError: allocation limit exceeded: 5001 > 5000
Print: 
```

## Analysis
- MemoryError: allocation limit exceeded: 5001 > 5000
- Verdict: Not exploitable
