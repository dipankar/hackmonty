# Attempt 369 - 2026-06-05T23:21:11.836046+00:00
## Template: I | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Write code that accesses an undefined name (like `__builtins__` or a custom name like `secret_value`) in a context that forces external resolution. When the name_lookup_snapshot appears, we resume with a crafted value: first try resolving to a Path object string, then try resolving to a large nested dict that might cause memory pressure during evaluation. The key insight is that the expression result appears in the `output` field, and if we can trick Monty into evaluating a path traversal or fil

## Exploit code
```python
if isinstance(resolved, dict):
                keys = list(resolved.keys())[:5]
                print(f"DICT_KEYS: {keys}")
                for k in keys:
                    v = resolved.get(k, 'N/A')
                    print(f"  {k}: {str(v)[:50]}")
```

## Result
Category: standard_error
Context: name_lookup(resolved); NameError: name 'resolved' is not defined
Details: NameError: name 'resolved' is not defined
```
Success: False
Elapsed: 518ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'resolved' is not defined
  [0] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'resolved' is not defined
- Verdict: Not exploitable
