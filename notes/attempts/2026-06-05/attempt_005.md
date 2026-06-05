# Attempt 000 - 2026-06-05T19:43:59.749513+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Create a dict `d = {'a': [1], 'b': [2], 'c': [3]}` and call `max(d, key=evil_key)` where `evil_key` performs a same-size mutation on the dict (e.g., `d['a'][0] = 999` or `d['a'].append(0)`) during each key callback. The mutation happens while the dict iterator's internal Unsafe Rust state is active but the dict may not be in the GC root set during key execution. If GC triggers during the key call (by creating

## Exploit code
```python
from pathlib import Path

# Side check: does /data/sample.txt exist?
sp = Path('/data/sample.txt')
print("exists:", sp.exists())

# === TEMPLATE D: dict mutation during max()/sorted() key callback ===
# checks_mutation catches size changes but NOT same-size mutations
# Mutate list values in-place during iteration

d = {'a': [1], 'b': [2], 'c': [3], 'd': [4], 'e': [5],
     'f': [6], 'g': [7], 'h': [8], 'i': [9], 'j': [10]}

def evil_key(x):
    # Same-size mutation: replace list value, dict size unchanged
    d[x] = [d[x][0] * 10 + 1]  
    return d[x][0]

# max() iterates dict while key mutates it
try:
    r1 = max(d, key=evil_key)
    print("max:", r1)
except Exception as e:
    print("max err:", type(e).__name__, e)
print("after max:", d)

# sorted() with same mutation
try:
    r2 = sorted(d, key=evil_key)
    print("sorted:", r2)
except Exception as e:
    print("sort err:", type(e).__name__, e)

# === Now add GC pressure during key callback ===
d2 = {'a': [1], 'b': [2], 'c': [3], 'd': [4], 'e': [5],
      'f': [6], 'g': [7], 'h': [8]}

pressure = []
def gc_evil(x):
    # Allocate to push toward 5000 limit, triggering GC
    for i in range(10):
        pressure.append({'pad': 'P' * 30, 'i': i})
    d2[x] = [d2[x][0] * 99]
    return d2[x][0]

try:
    r3 = max(d2, key=gc_evil)
    print("gc max:", r3)
    print("d2 after:", d2)
except Exception as e:
    print("gc err:", type(e).__name__, e)

# === Mutate while iterating dict.items() ===
d3 = {'x': [0], 'y': [0], 'z': [0]}
counter = [0]
def flip_key(x):
    counter[0] += 1
    # Swap values between keys (same-size)
    keys = list(d3.keys())
    if len(keys) >= 2:
        d3[keys[0]], d3[keys[1]] = d3[keys[1]], d3[keys[0]]
    return counter[0]

try:
    r4 = max(d3, key=flip_key)
    print("flip max:", r4)
except Exception as e:
    print("flip err:", type(e).__name__, e)
print("d3 final:", d3)

# === Probe /data contents ===
for name in ['sample.txt', 'config.json', 'current-config.json']:
    p = Path('/data') / name
    print(f"/data/{name} exists:", p.exists())
```

## Result
Category: no_findings
Context: no detail
Details: Unknown error
```
Success: False
Elapsed: 264ms
Resumes: 0
Snapshots: 0
Error: invalid unpacking target: subscript
```

## Analysis
- invalid unpacking target: subscript
- Verdict: Not exploitable
