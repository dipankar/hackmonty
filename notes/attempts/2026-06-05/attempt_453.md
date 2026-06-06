# Attempt 451 - 2026-06-05T23:45:55.639762+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Create a dict with 20+ keys, then call `max(d, key=evil_key)` where `evil_key` does a same-size value replacement (not insertion/deletion) on the dict during iteration. Since `checks_mutation` only checks dict size, the mutation passes through and the iterator's internal bucket index becomes stale. We then check if the returned key is valid, if `len(d)` matches expectations, and if iterating over `d.values()` produces duplicate or missing entries—indicating iterator corruption from the same-size

## Exploit code
```python
if len(mutation_log) > 20:
        for secret_path in ['/data/config.json', '/data/current-config.json']:
            p = Path(secret_path)
            if p.exists():
                content = p.read_text()[:200]
                print(f"SECRET_READ: {secret_path} = {content}")
```

## Result
Category: standard_error
Context: name_lookup(mutation_log); NameError: name 'mutation_log' is not defined
Details: NameError: name 'mutation_log' is not defined
```
Success: False
Elapsed: 1044ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'mutation_log' is not defined
  [0] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'mutation_log' is not defined
- Verdict: Not exploitable
