# Attempt 229 - 2026-06-05T22:40:46.358298+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Create a dict where the key function mutates values mid-iteration to make the "current best" candidate change between comparisons, causing `max()` to return the wrong key. We mutate values (not structure) so the mutation check passes but comparison results are inconsistent. If the VM caches comparison results or iterates with stale values, we get a wrong-key return value indicating state corruption, which we can detect and print.

## Exploit code
```python
for f in ['current-config.json', 'sample.txt']:
    try:
        p = Path(f'/data/{f}')
        if p.exists():
            txt = p.read_text()[:80]
            print(f"{f}: {txt}")
```

## Result
Category: no_findings
Context: Expected `except` or `finally` after `try` block
Details: Unknown error
```
Success: False
Elapsed: 306ms
Resumes: 0
Snapshots: 0
Error: Expected `except` or `finally` after `try` block
```

## Analysis
- Expected `except` or `finally` after `try` block
- Verdict: Not exploitable
