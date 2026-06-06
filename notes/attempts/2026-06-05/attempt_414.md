# Attempt 416 - 2026-06-05T23:34:02.406749+00:00
## Template: K | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Trigger a name_lookup_snapshot by accessing `__builtins__` or any undefined name in a non-print context. Then resume the snapshot twice with different values: first with a valid path string that executes successfully, second with an object of a different type (e.g., a dict containing crafted data) to test if the VM's name resolution cache or frame state becomes corrupted between resumes. If the second resume succeeds with unexpected behavior, it could leak host information or bypass sandbox chec

## Exploit code
```python
if isinstance(val, str):
        p = Path(val)
        if p.exists():
            results.append(f"STR_PATH:{val[:25]}")
```

## Result
Category: standard_error
Context: name_lookup(val); NameError: name 'val' is not defined
Details: NameError: name 'val' is not defined
```
Success: False
Elapsed: 933ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'val' is not defined
  [0] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'val' is not defined
- Verdict: Not exploitable
