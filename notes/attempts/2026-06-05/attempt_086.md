# Attempt 087 - 2026-06-05T21:04:35.781895+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Build a dict with several entries, then call `max(dict, key=evil_key)` where evil_key mutates the dict with same-size assignments (e.g., `d['a'] = d.get('a',0) + 1` — length stays the same, checks_mutation doesn't fire) while iterating. Since the dict's internal storage is mutated during key callback execution without the iteration state being updated, we should observe either a wrong max key returned, a duplicate key, or the VM panicking on stale internal indices. Combine with `sorted(d, key=ev

## Exploit code
```python
try:
    result = max(d, key=evil_key)
    print(f"max={result} calls={calls[0]} dict={d}")
```

## Result
Category: no_findings
Context: no detail
Details: Unknown error
```
Success: False
Elapsed: 298ms
Resumes: 0
Snapshots: 0
Error: Expected `except` or `finally` after `try` block
```

## Analysis
- Expected `except` or `finally` after `try` block
- Verdict: Not exploitable
