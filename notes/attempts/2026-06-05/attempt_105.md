# Attempt 104 - 2026-06-05T22:05:03.278428+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Create a dict `d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}` and define `evil_key` that performs a same-size mutation on `d` (e.g., `d['a'] = d['a'] + 1` swapping values rather than adding/removing keys), then call `max(d, key=evil_key)` to trigger iteration-during-callback. If the dict's internal storage isn't in the GC root set during key evaluation, we can create a use-after-free by triggering GC pressure inside `evil_key` via `gc_pressure()` (cyclical dict refs + allocations), potentially ca

## Exploit code
```python
def gc_pressure(n=80):
    cycles = []
    for i in range(n):
        a = {'next': None, 'data': 'X' * 25}
        b = {'prev': a, 'data': 'Y' * 25}
```

## Result
Category: no_findings
Context: no detail
Details: Completed with no notable findings
```
Success: True
Elapsed: 271ms
Resumes: 0
Snapshots: 0
Print: 
```

## Analysis
- Completed with no findings
- Verdict: Try different template
