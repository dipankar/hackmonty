# Attempt 064 - 2026-06-06T22:02:23.553547+00:00
## Template: A | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template A: Dict Re-entry Attack
# Exploit: mutate dict during key comparison in lookup

d = {1: 'a', 2: 'b', 3: 'c'}

# Use a mutable container as part of tuple key
# Tuple comparison calls __eq__ on elements
state = {'mutated': False}

def make_key(n):
    return (n, state)

# Build dict with tuple keys
for i in range(5):
    d[make_key(i)] = f'val{i}'

# Now trigger lookup that compares tuples
# When comparing (0, state) == (1, state), list/dict __eq__ is called
target = (0, state)

# Force comparison by checking membership
found = target in d

# Try mutation during iteration
keys_to_check = list(d.keys())
for k in keys_to_check:
    if isinstance(k, tuple) and len(k) == 2:
        # Mutate state during iteration
        state['mutated'] = True
        # Try to inject new key
        d[('injected', state)] = 'evil'

print(f"Keys: {len(d)}")
print(f"State: {state}")
print(f"Dict: {d}")
```

## Result
Context: Tuples are not hashable in this sandbox, cannot use as dict keys
Score: 0/5 - Nothing - standard error or expected sandbox behavior
