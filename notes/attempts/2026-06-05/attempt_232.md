# Attempt 231 - 2026-06-05T22:41:31.414298+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Execute asyncio.gather GC race

## Exploit code
```python
for i, r in enumerate(gathered):
            expected = f"coro_{i}_done"
            if r != expected:
                print(f"CORRUPTION: task {i} returned {r} instead of {expected}")
```

## Result
Category: standard_error
Context: name_lookup(gathered); NameError: name 'gathered' is not defined
Details: NameError: name 'gathered' is not defined
```
Success: False
Elapsed: 502ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'gathered' is not defined
  [0] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'gathered' is not defined
- Verdict: Not exploitable
