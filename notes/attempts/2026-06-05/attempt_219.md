# Attempt 219 - 2026-06-05T22:37:59.717328+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Execute asyncio.gather GC race

## Exploit code
```python
if state_corruption:
        print(f"CORRUPTION DETECTED: {len(state_corruption)} workers")
        for c in state_corruption:
            print(f"  {c}")
```

## Result
Category: standard_error
Context: name_lookup(state_corruption); NameError: name 'state_corruption' is not defined
Details: NameError: name 'state_corruption' is not defined
```
Success: False
Elapsed: 680ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'state_corruption' is not defined
  [0] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'state_corruption' is not defined
- Verdict: Not exploitable
