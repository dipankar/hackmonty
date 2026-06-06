# Attempt 401 - 2026-06-05T23:30:48.714234+00:00
## Template: "When sorted() is called WITHOUT a key function, Monty's compare_values calls py_cmp which invokes user __lt__ for EVERY comparison." This suggests that even for built-in types, the path goes through py_cmp. | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Execute Set __hash__ re-entry during add

## Exploit code
```python
from pathlib import Path
for p in ['/data/config.json', '/data/current-config.json']:
    try:
        content = Path(p).read_text()[:150]
        print(f"Found: {p}")
        if 'secret' in content.lower() or 'path' in content.lower():
            print(f"Content: {content}")
```

## Result
Category: no_findings
Context: Expected `except` or `finally` after `try` block
Details: Unknown error
```
Success: False
Elapsed: 773ms
Resumes: 0
Snapshots: 0
Error: Expected `except` or `finally` after `try` block
```

## Analysis
- Expected `except` or `finally` after `try` block
- Verdict: Not exploitable
