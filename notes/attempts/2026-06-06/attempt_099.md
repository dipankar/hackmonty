# Attempt 089 - 2026-06-06T22:27:44.465221+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template D: MinMaxMutate - Mutate dict during key= callback
# The key function runs during iteration, can mutate same-size dict

d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
counter = [0]

def mutating_key(x):
    # Mutate dict during key calculation - same size, not caught
    counter[0] += 1
    if counter[0] < 3:
        d['a'] = d['a'] + 100
    return d[x]

try:
    result = max(d, key=mutating_key)
    print(f"Max key: {result}, value: {d[result]}")
    print(f"Dict after: {d}")
except Exception as e:
    print(f"Error: {e}")

# Try with sorted
d2 = {i: i*10 for i in range(10)}
mut_count = [0]

def sort_key(x):
    mut_count[0] += 1
    if mut_count[0] % 2 == 0:
        d2[0] = d2[0] + 1
    return d2[x]

try:
    sorted_result = sorted(d2, key=sort_key)
    print(f"Sorted keys: {sorted_result[:5]}")
except Exception as e:
    print(f"Sort error: {e}")

# Try min with mutation
d3 = {'x': 10, 'y': 5, 'z': 20}
def min_key(x):
    d3['x'] = 0  # Make x the minimum during iteration
    return d3[x]

try:
    min_result = min(d3, key=min_key)
    print(f"Min key: {min_result}")
except Exception as e:
    print(f"Min error: {e}")
```

## Result
Context: Mutation during key= works but sandbox handles gracefully - no corruption
Score: 0/5 - Nothing - standard error or expected sandbox behavior
