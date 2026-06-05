# Attempt 057 - 2026-06-05T20:55:33.753461+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Create a dict with many keys, then call `max(dict, key=evil_key)` where `evil_key` performs same-size mutations (updating existing values, swapping key-value pairs) during each key callback invocation. Since `checks_mutation` only catches size changes, the iterator will walk stale entries and potentially return a key that maps to freed/corrupted memory. Additionally, craft a variant where `sorted()` with a key callback reorders the dict in-place using same-size mutations to confuse the sort's in

## Exploit code
```python
def sort_key(x):
    c = mut_count[0]
    if c < 30:
        idx = c % 50
```

## Result
Category: no_findings
Context: no detail
Details: Completed with no notable findings
```
Success: True
Elapsed: 611ms
Resumes: 0
Snapshots: 0
Print: 
```

## Analysis
- Completed with no findings
- Verdict: Try different template
