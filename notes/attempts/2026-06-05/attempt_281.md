# Attempt 279 - 2026-06-05T22:54:38.878092+00:00
## Template: K | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Execute Double-resume state machine

## Exploit code
```python
print(f"Count: {tracker['count']}")
print(f"Types: {tracker['values']}")
print(f"IDs: {tracker['ids']}")
print(f"StateShared: {is_shared}")
```

## Result
Category: standard_error
Context: name_lookup(tracker); NameError: name 'tracker' is not defined
Details: NameError: name 'tracker' is not defined
```
Success: False
Elapsed: 604ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'tracker' is not defined
  [0] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'tracker' is not defined
- Verdict: Not exploitable
