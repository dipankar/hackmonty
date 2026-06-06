# Attempt 271 - 2026-06-05T22:51:53.603748+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Create a dict with 40+ entries, then define `evil_key` that rotates values via same-size swaps (bypassing `checks_mutation`). Call `max(d, key=evil_key)` — if the dict's internal storage iterator is re-read mid-iteration, the wrong key/value pair gets returned. Compare the result against the expected maximum to detect corruption, and print the returned key's repr plus any unexpected type contents. Wrap everything in a complete try/except to prevent syntax failures.

## Exploit code
```python
if result != expected_max:
        print(f"CORRUPTION: max returned {repr(result)}")
        print(f"Expected: {repr(expected_max)}")
        print(f"Mutations: {len(mutations)}")
        print(f"Value at result: {d.get(result)}")
```

## Result
Category: standard_error
Context: name_lookup(result); NameError: name 'result' is not defined
Details: NameError: name 'result' is not defined
```
Success: False
Elapsed: 612ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'result' is not defined
  [0] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'result' is not defined
- Verdict: Not exploitable
