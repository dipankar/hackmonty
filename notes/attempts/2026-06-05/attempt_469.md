# Attempt 468 - 2026-06-05T23:50:24.734865+00:00
## Template: G | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
1. Create a dict with several items
2. Define a key function that mutates the dict (same-size: changes values, not adds/removes keys)
3. Call max(d, key=evil_key) or sorted(d, key=evil_key)
4. The iterator may return stale values, or the key function may be called with wrong keys
5. Print the result and the dict state after

## Exploit code
```python
if len(sort_items) != 30:
        corrupted = True
        print(f"CORRUPTION: sort_items length = {len(sort_items)}")
    if len(pressure) < 4950:
        corrupted = True
        print(f"CORRUPTION: pressure list shrunk to {len(pressure)}")
```

## Result
Category: no_findings
Context: unindent does not match any outer indentation level
Details: Unknown error
```
Success: False
Elapsed: 408ms
Resumes: 0
Snapshots: 0
Error: unindent does not match any outer indentation level
```

## Analysis
- unindent does not match any outer indentation level
- Verdict: Not exploitable
