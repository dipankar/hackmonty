# Attempt 439 - 2026-06-05T23:42:07.673670+00:00
## Template: K | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Use undefined variable in an expression
# The name_lookup_snapshot will be triggered
# If the framework resumes with a value, the code continues

## Exploit code
```python
print("=== NAME_LOOKUP_PROBE ===")
for r in results[:15]:
    print(r)
print(f"Total captures: {len(state['values'])}")
if state['values']:
    print(f"First value type: {type(state['values'][0]).__name__}")
```

## Result
Category: standard_error
Context: name_lookup(results); NameError: name 'results' is not defined
Details: NameError: name 'results' is not defined
```
Success: False
Elapsed: 597ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'results' is not defined
  [0] kind=name_lookup_snapshot
      stdout: === NAME_LOOKUP_PROBE ===

Print: === NAME_LOOKUP_PROBE ===

```

## Analysis
- NameError: name 'results' is not defined
- Verdict: Not exploitable
