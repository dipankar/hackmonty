# Attempt 018 - 2026-06-06T21:01:58.459274+00:00
## Template: A | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
from pathlib import Path

# Template A: Dict re-entry during external call
d = {}
for i in range(20):
    d[f'key{i}'] = i * 100

# Capture state before external call
before_keys = list(d.keys())
before_sum = sum(d.values())

# Trigger external call (file read) which may snapshot
p = Path('/data/sample.txt')
if p.exists():
    content = p.read_text()
    # During file read, dict might be snapshotted
    # Check if dict is corrupted after
    after_keys = list(d.keys())
    after_sum = sum(d.values())
    
    if before_keys != after_keys or before_sum != after_sum:
        print(f'CORRUPTION: keys={len(after_keys)}, sum={after_sum}')
    else:
        print(f'OK: {len(after_keys)} keys, sum={after_sum}')
    print(f'File content: {content[:100]}')
else:
    print('File not found')

# Test dict mutation during iteration
d2 = {i: i*2 for i in range(10)}
try:
    for k in d2:
        d2[k] = d2[k] + 1  # Same-size mutation
    print(f'd2 mutated: {d2}')
except Exception as e:
    print(f'd2 error: {e}')
```

## Result
Context: no detail
Score: 0/5 - Nothing - standard error or expected sandbox behavior
