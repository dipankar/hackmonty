# Attempt 048 - 2026-06-05T21:48:36.988743+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Execute asyncio.gather GC race

## Exploit code
```python
for i in range(50):
        obj = {'coro': cor_id, 'iter': i, 'pad': 'X' * 30}
        alloc_pool.append(obj)
```

## Result
Category: standard_error
Context: name_lookup(cor_id); NameError: name 'cor_id' is not defined
Details: NameError: name 'cor_id' is not defined
```
Success: False
Elapsed: 713ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'cor_id' is not defined
  [0] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'cor_id' is not defined
- Verdict: Not exploitable
