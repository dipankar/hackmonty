# Attempt 010 - 2026-06-05T19:48:52.387451+00:00
## Template: F | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Use `pathlib.Path` to read `/data/config.json` and `/data/current-config.json` (a symlink to live config), printing their raw contents to surface any host paths, secrets, or internal endpoints. Also probe `/data/sample.txt`, `/data/docs/`, `/data/i18n/`, and `/data/logs/` via `Path.read_text()` or `open()` to enumerate what other files the mount exposes. Finally, parse the config JSON and extract any field that looks like a file path (`/app/`, `/etc/`, `/home/`, `SECRET`, `key`, `token`) to map 

CRITICAL: NO os.listdir - not supported in Monty

## Exploit code
```python
import json
from pathlib import Path

# Read all known /data files directly
targets = [
    '/data/config.json',
    '/data/current-config.json',
    '/data/sample.txt',
]

results = []
for t in targets:
    p = Path(t)
    try:
        if p.exists():
            content = p.read_text()
            results.append((t, len(content), content))
    except Exception as e:
        results.append((t, 'err', repr(e)))

for path, size, data in results:
    print(f"=== {path} ({size}) ===")
    if isinstance(data, str) and size < 2000:
        print(data)
    else:
        print(repr(data)[:300])

# Parse config.json if it exists
for cfg_path in ['/data/config.json', '/data/current-config.json']:
    try:
        cfg = json.loads(Path(cfg_path).read_text())
        print(f"--- KEYS in {cfg_path} ---")
        print(list(cfg.keys()) if isinstance(cfg, dict) else type(cfg))

        # Recursive key search for path-like values
        def hunt(obj, trail=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    hunt(v, trail + "." + k)
            elif isinstance(obj, str):
                low = obj.lower()
                if any(s in low for s in ['/app/', '/etc/', '/home/', 'secret', 'key', 'token', 'hack', 'password']):
                    print(f"INTERESTING {trail} = {obj}")
        hunt(cfg)
    except Exception as e:
        print(f"skip {cfg_path}: {e}")

# Try to glob for hidden files
try:
    for f in Path('/data').iterdir():
        print("FILE:", f.name, f.stat().st_size)
except Exception as e:
    print("iterdir err:", e)
```

## Result
Category: no_findings
Context: no detail
Details: Completed with no notable findings
```
Success: True
Elapsed: 575ms
Resumes: 0
Snapshots: 0
Print: === /data/config.json (90) ===
{
  "app_name": "hackmonty",
  "version": "0.1.0",
  "debug": false,
  "max_workers": 4
}

=== /data/current-config.json (90) ===
{
  "app_name": "hackmonty",
  "version": "0.1.0",
  "debug": false,
  "max_workers": 4
}

=== /data/sample.txt (140) ===
Hello from the Monty sandbox!
This file is mounted read-only at /data/sample.txt.
You can read it with Path('/data/sample.txt').read_text()

--- KEYS in /data/config.json ---
['app_name', 'version', 'debug', 'max_work
```

## Analysis
- Completed with no findings
- Verdict: Try different template
