# Attempt 109 - 2026-06-06T22:57:34.900739+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template D: MinMaxMutate - exploit key= mutating during iteration
# The key function runs during iteration, can mutate same-size structures

# Create a dict and mutate during max with key
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

def evil_key(x):
    # Mutate the dict during key computation
    d['a'] = d['a'] + 10
    return d[x]

try:
    result = max(d, key=evil_key)
    print("max result:", result)
    print("dict after:", d)
except Exception as e:
    print("error:", type(e).__name__, e)

# Try with min
d2 = {'x': 10, 'y': 20, 'z': 5}
def mutate_key(x):
    d2['x'] = 999
    return d2[x]

try:
    result2 = min(d2, key=mutate_key)
    print("min result:", result2)
    print("d2 after:", d2)
except Exception as e:
    print("min error:", type(e).__name__, e)

# Try with sorted
d3 = {i: i*2 for i in range(5)}
counter = [0]
def count_key(x):
    counter[0] += 1
    d3[0] = counter[0]  # Mutate
    return d3[x]

try:
    sorted_result = sorted(d3, key=count_key)
    print("sorted:", sorted_result)
    print("d3 after:", d3)
    print("counter:", counter)
except Exception as e:
    print("sorted error:", type(e).__name__, e)

# Try with list and index mutation
items = [1, 2, 3, 4, 5]
def list_key(x):
    items[0] = 100
    return x

try:
    max_item = max(items, key=list_key)
    print("max item:", max_item)
    print("items after:", items)
except Exception as e:
    print("list error:", type(e).__name__, e)

# File probe
from pathlib import Path
for p in ["/data/sample.txt", "/data/config.json"]:
    try:
        content = Path(p).read_text()
        print(p, ":", content[:100])
    except Exception as e:
        print(p, ":", type(e).__name__)
```

## Result
Context: no detail
Score: 0/5 - Nothing - standard error or expected sandbox behavior
