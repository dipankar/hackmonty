# Attempt 060 - 2026-06-06T21:59:57.780328+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template D: MinMaxMutate - mutate dict during max() with key=
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

def evil_key(x):
    d['a'] = d['a'] + 10
    return d[x]

print(f"Before: {d}")
try:
    result = max(d, key=evil_key)
    print(f"max result: {result}")
    print(f"After: {d}")
except Exception as e:
    print(f"Error: {e}")

d2 = {1: 'a', 2: 'b', 3: 'c'}
def mutate_min(x):
    d2[x] = d2[x] + 'x'
    return x

print(f"\nBefore min: {d2}")
try:
    result2 = min(d2, key=mutate_min)
    print(f"min result: {result2}")
    print(f"After min: {d2}")
except Exception as e:
    print(f"Error: {e}")

d3 = {'x': 10, 'y': 20, 'z': 30}
def mutate_sorted(x):
    d3[x] = 0
    return d3[x]

print(f"\nBefore sorted: {d3}")
try:
    result3 = sorted(d3, key=mutate_sorted)
    print(f"sorted result: {result3}")
    print(f"After sorted: {d3}")
except Exception as e:
    print(f"Error: {e}")
```

## Result
Context: Mutations occurred but correct elements still selected, no vulnerability
Score: 0/5 - Nothing - standard error or expected sandbox behavior
