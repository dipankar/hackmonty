# Attempt 147 - 2026-06-05T22:17:49.886248+00:00
## Template: B | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Execute Set __hash__ re-entry during add

## Exploit code
```python
for r in set_results[:3]:
    print(r)
for r in config_results[:5]:
    print(r)
```

## Result
Category: standard_error
Context: name_lookup(set_results); NameError: name 'set_results' is not defined
Details: NameError: name 'set_results' is not defined
```
Success: False
Elapsed: 817ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'set_results' is not defined
  [0] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'set_results' is not defined
- Verdict: Not exploitable
