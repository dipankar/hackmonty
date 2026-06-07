# Attempt 033 - 2026-06-06T21:33:28.708092+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template D: min/max/sorted with key= mutating iterable
# Key function runs during iteration - can mutate values (same-size not caught)

# Test with dict
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
print("Original dict:", d)

def mutating_key(x):
    d[x] = d[x] + 10
    return d[x]

try:
    result = max(d, key=mutating_key)
    print("Max key:", result)
    print("Dict after max:", d)
except Exception as e:
    print("Error:", type(e).__name__, str(e)[:60])

# Test with list
items = [10, 20, 30, 40, 50]
print("\nOriginal list:", items)

def list_mutating_key(x):
    idx = items.index(x)
    items[idx] = x + 100
    return items[idx]

try:
    result = sorted(items, key=list_mutating_key)
    print("Sorted result:", result)
    print("List after sort:", items)
except Exception as e:
    print("Error:", type(e).__name__, str(e)[:60])

# Test min with mutation
d2 = {1: 100, 2: 200, 3: 50}
print("\nOriginal d2:", d2)

def min_mutating_key(x):
    d2[x] = d2[x] - 10
    return d2[x]

try:
    result = min(d2, key=min_mutating_key)
    print("Min key:", result)
    print("d2 after min:", d2)
except Exception as e:
    print("Error:", type(e).__name__, str(e)[:60])
```

## Result
Context: MinMaxMutate - mutation worked but correct element still selected
Score: 0/5 - Nothing - standard error or expected sandbox behavior
