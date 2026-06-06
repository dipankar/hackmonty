# Attempt 181 - 2026-06-05T22:26:50.772948+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Create a dict with 4-5 keys mapping to integer values, then call `max(d, key=evil_key)` where `evil_key` mutates the dict by reassigning values (same size, not caught by checks_mutation). After the call completes, inspect whether the returned key matches the actual maximum based on the mutated state, proving the key function observed stale dict data mid-iteration. Keep the entire script under 20 lines with proper try/except to avoid truncation.

## Exploit code
```python
print(f"Returned: {result}")
print(f"Mutations: {len(mutations)}")
print(f"Final dict: {d}")
```

## Result
Category: standard_error
Context: name_lookup(result); NameError: name 'result' is not defined
Details: NameError: name 'result' is not defined
```
Success: False
Elapsed: 516ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'result' is not defined
  [0] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'result' is not defined
- Verdict: Not exploitable
