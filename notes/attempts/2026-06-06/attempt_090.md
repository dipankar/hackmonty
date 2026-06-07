# Attempt 089 - 2026-06-06T22:20:26.056586+00:00
## Template: C | Score: 0 - sandbox_permission
## Exploit code
```python
# Template C: File reading during operations
from pathlib import Path
for f in ['/data/config.json', '/data/sample.txt', '/etc/secrets/hackmonth.txt', '/app/secret.txt']:
    p = Path(f)
    if p.exists():
        try:
            print(f"{f}: {p.read_text()[:150]}")
        except Exception as e:
            print(f"{f}: {e}")
```

## Result
Context: Can read /data files but permission denied on secret paths
Score: 0/5 - sandbox_permission
