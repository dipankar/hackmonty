# Attempt 082 - 2026-06-06T22:12:53.619435+00:00
## Template: F | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template F: ConfigFiles - enumerate config files for secrets

print("=== ConfigFiles Test ===")

from pathlib import Path

# Check /data directory structure
data = Path('/data')
print(f"/data exists: {data.exists()}")

if data.exists():
    print("\n=== /data contents ===")
    try:
        for item in data.iterdir():
            print(f"  {item.name} ({'dir' if item.is_dir() else 'file'})")
    except Exception as e:
        print(f"Error listing: {e}")

# Read config.json
print("\n=== /data/config.json ===")
config = Path('/data/config.json')
if config.exists():
    try:
        content = config.read_text()
        print(content[:500] if len(content) > 500 else content)
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Not found")

# Read current-config.json (symlink)
print("\n=== /data/current-config.json ===")
curr = Path('/data/current-config.json')
if curr.exists():
    try:
        content = curr.read_text()
        print(content[:500] if len(content) > 500 else content)
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Not found")

# Check docs directory
print("\n=== /data/docs/ ===")
docs = Path('/data/docs')
if docs.exists():
    try:
        for item in docs.iterdir():
            print(f"  {item.name}")
    except Exception as e:
        print(f"Error: {e}")

# Check i18n directory
print("\n=== /data/i18n/ ===")
i18n = Path('/data/i18n')
if i18n.exists():
    try:
        for item in i18n.iterdir():
            print(f"  {item.name}")
    except Exception as e:
        print(f"Error: {e}")

# Check logs directory
print("\n=== /data/logs/ ===")
logs = Path('/data/logs')
if logs.exists():
    try:
        for item in logs.iterdir():
            print(f"  {item.name}")
    except Exception as e:
        print(f"Error: {e}")

# Read sample.txt
print("\n=== /data/sample.txt ===")
sample = Path('/data/sample.txt')
if sample.exists():
    try:
        print(sample.read_text()[:300])
    except Exception as e:
        print(f"Error: {e}")

print("\nDone")
```

## Result
Context: Config files contain only app metadata, no sensitive data found
Score: 0/5 - Nothing - standard error or expected sandbox behavior
