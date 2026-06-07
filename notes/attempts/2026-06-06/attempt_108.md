# Attempt 098 - 2026-06-06T22:41:58.974682+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template D: min/max/sorted with key= mutating iterable
# The key function runs during iteration - try to mutate the dict

d = {'a': 10, 'b': 20, 'c': 30, 'd': 40, 'e': 50}

print("Original dict:", d)

# Mutating key function - changes values but not size
def evil_key(k):
    d[k] = d[k] + 1  # Increment the value
    return d[k]

# Try max with mutating key
result = max(d, key=evil_key)
print("Max key:", result, "with value:", d[result])
print("Dict after max:", d)

# Reset and try min
d2 = {'a': 10, 'b': 20, 'c': 30, 'd': 40, 'e': 50}
def evil_key_min(k):
    d2[k] = d2[k] - 5
    return d2[k]

result2 = min(d2, key=evil_key_min)
print("Min key:", result2, "with value:", d2[result2])
print("Dict after min:", d2)

# Try sorted with mutating key
d3 = {'a': 10, 'b': 20, 'c': 30}
def evil_key_sorted(k):
    d3[k] = d3[k] * 2
    return d3[k]

result3 = sorted(d3, key=evil_key_sorted)
print("Sorted keys:", result3)
print("Dict after sorted:", d3)

# Check if the results are correct or corrupted
print("Done")
```

## Result
Context: Mutation during key= works but sandbox handles gracefully - no corruption
Score: 0/5 - Nothing - standard error or expected sandbox behavior
