# Attempt 015 - 2026-06-06T20:55:59.816815+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template D: min/max/sorted with key= mutating iterable
# Key function mutates dict values during iteration (same-size, not caught)

d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
print("Original dict:", d)

counter = [0]  # Use list for mutable counter

def evil_key(k):
    # Mutate the dict during key computation
    counter[0] += 1
    # Change values (same-size mutation)
    for key in d:
        d[key] = d[key] + 1
        break  # Just mutate one value per key lookup
    return d[k]

try:
    result = max(d, key=evil_key)
    print("max result:", result)
    print("Dict after max:", d)
    print("Key function called:", counter[0], "times")
except Exception as e:
    print("Error:", type(e).__name__, e)
    print("Dict after error:", d)

# Try with min too
d2 = {'x': 10, 'y': 20, 'z': 5}
print("\nSecond dict:", d2)

counter2 = [0]
def evil_key2(k):
    counter2[0] += 1
    d2['x'] = 1000  # Mutate during iteration
    return d2[k]

try:
    result = min(d2, key=evil_key2)
    print("min result:", result)
    print("Dict after min:", d2)
except Exception as e:
    print("Error:", type(e).__name__, e)
```

## Result
Context: no detail
Score: 0/5 - Nothing - standard error or expected sandbox behavior
