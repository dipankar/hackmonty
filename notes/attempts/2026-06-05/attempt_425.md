# Attempt 424 - 2026-06-05T23:37:39.188592+00:00
## Template: K | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Execute Double-resume state machine

## Exploit code
```python
print(f"Resumes: {state['count']}")
print(f"Types: {state['types']}")
if state['leaks']:
    print(f"LEAK: {state['leaks'][0]}")
```

## Result
Category: standard_error
Context: name_lookup(state); NameError: name 'state' is not defined
Details: NameError: name 'state' is not defined
```
Success: False
Elapsed: 616ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'state' is not defined
  [0] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'state' is not defined
- Verdict: Not exploitable
