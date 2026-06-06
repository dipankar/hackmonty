# Attempt 018 - 2026-06-05T21:38:58.429179+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Create a dict and pass it to `max(d, key=evil_key)` where `evil_key` mutates the dict with same-size operations (changing values, not adding keys). The `checks_mutation` flag only catches size changes, so same-size mutations pass through. Since `max()` with key= was NOT the specific target of the v0.0.16 fix (which was for `list.sort(key=...)`), the new list being built by `max()` may not be in the GC root set. If we combine this with allocation pressure in the key function, we force GC to run m

## Exploit code
```python
try:
    from pathlib import Path
    for target in ['/data/config.json', '/data/current-config.json']:
        p = Path(target)
        if p.exists():
            content = p.read_text()[:300]
            print(f"{target}: {content[:150]}")
```

## Result
Category: no_findings
Context: Expected `except` or `finally` after `try` block
Details: Unknown error
```
Success: False
Elapsed: 313ms
Resumes: 0
Snapshots: 0
Error: Expected `except` or `finally` after `try` block
```

## Analysis
- Expected `except` or `finally` after `try` block
- Verdict: Not exploitable
