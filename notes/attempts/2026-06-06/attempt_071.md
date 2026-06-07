# Attempt 070 - 2026-06-06T22:05:00.946607+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template D: min/max/sorted with key= mutating iterable
# Strategy: Same-size mutation during key= callback might not be caught

d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
mutation_count = [0]

def mutating_key(k):
    # Same-size mutation - change values but not keys
    mutation_count[0] += 1
    # Mutate the dict during iteration
    for key in d:
        d[key] = d[key] + 1
        break  # Only mutate one value per call
    return d[k]

try:
    # This should trigger mutation detection or corruption
    result = max(d, key=mutating_key)
    print(f"Max key: {result}")
    print(f"Dict after: {d}")
    print(f"Mutations: {mutation_count[0]}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

# Try with min
d2 = {'x': 10, 'y': 20, 'z': 30}
def key2(k):
    d2['x'] = 999  # Same-size mutation
    return d2[k]

try:
    result2 = min(d2, key=key2)
    print(f"Min key: {result2}")
    print(f"Dict2 after: {d2}")
except Exception as e:
    print(f"Error2: {type(e).__name__}: {e}")

# Try with sorted
d3 = {1: 'a', 2: 'b', 3: 'c'}
def key3(k):
    d3[k] = 'mutated'
    return k

try:
    result3 = sorted(d3, key=key3)
    print(f"Sorted: {result3}")
    print(f"Dict3 after: {d3}")
except Exception as e:
    print(f"Error3: {type(e).__name__}: {e}")
```

## Result
Context: Mutations occurred but correct elements still selected, no vulnerability
Score: 0/5 - Nothing - standard error or expected sandbox behavior
