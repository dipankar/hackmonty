# Attempt 101 - 2026-06-06T22:43:34.431231+00:00
## Template: F | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template F: Config File Enumeration
# Explore /data directory for useful info

from pathlib import Path

# List /data contents
data_dir = Path('/data')
print("Data dir exists:", data_dir.exists())

# Try to list contents
try:
    items = list(data_dir.iterdir())
    print("Contents:", [str(i) for i in items])
except Exception as e:
    print("List error:", e)

# Read known files
files_to_try = [
    '/data/config.json',
    '/data/current-config.json',
    '/data/sample.txt',
    '/data/docs/README.md',
    '/data/i18n/en.json',
    '/data/logs/app.log',
]

for f in files_to_try:
    p = Path(f)
    if p.exists():
        try:
            content = p.read_text()
            print(f"=== {f} ({len(content)} bytes) ===")
            print(content[:500])
        except Exception as e:
            print(f"Read error {f}:", e)
    else:
        print(f"Not found: {f}")

# Try subdirectories
subdirs = ['/data/docs', '/data/i18n', '/data/logs']
for sd in subdirs:
    p = Path(sd)
    if p.exists():
        try:
            items = list(p.iterdir())
            print(f"{sd} contents:", [str(i.name) for i in items])
        except Exception as e:
            print(f"List error {sd}:", e)
```

## Result
Context: Enumerated /data files - only basic config, no secrets found
Score: 0/5 - Nothing - standard error or expected sandbox behavior
