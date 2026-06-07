# Attempt 050 - 2026-06-06T21:52:57.267341+00:00
## Template: D | Score: 0 - MinMaxMutate - mutations occurred but correct results
## Exploit code
```python
# Template D: MinMaxMutate - exploit min/max/sorted with key= that mutates iterable

d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
mutation_log = []

def mutating_key(x):
    mutation_log.append(f'key({x})')
    if x != 'e':
        d['a'] = d['a'] + 1
    return d[x]

print(f"dict before max: {d}")
try:
    result = max(d, key=mutating_key)
    print(f"max result: {result}, value: {d[result]}")
except Exception as e:
    print(f"max error: {type(e).__name__}: {e}")

print(f"dict after max: {d}")
print(f"mutation log: {mutation_log}")

# Try with min
d2 = {'x': 10, 'y': 5, 'z': 20}
mutation_log2 = []

def mutating_key_min(x):
    mutation_log2.append(f'key({x})')
    d2['x'] = 1
    return d2[x]

print(f"\ndict2 before min: {d2}")
try:
    result2 = min(d2, key=mutating_key_min)
    print(f"min result: {result2}, value: {d2[result2]}")
except Exception as e:
    print(f"min error: {type(e).__name__}: {e}")

print(f"dict2 after min: {d2}")
print(f"mutation log2: {mutation_log2}")

# Try with sorted
d3 = {1: 'one', 2: 'two', 3: 'three', 4: 'four'}
mutation_log3 = []

def mutating_key_sorted(x):
    mutation_log3.append(f'key({x})')
    d3[1] = 999
    return x

print(f"\ndict3 before sorted: {d3}")
try:
    result3 = sorted(d3, key=mutating_key_sorted)
    print(f"sorted result: {result3}")
except Exception as e:
    print(f"sorted error: {type(e).__name__}: {e}")

print(f"dict3 after sorted: {d3}")
print(f"mutation log3: {mutation_log3}")

# Try list mutation during sorted
items = [1, 2, 3, 4, 5]
item_mutation_log = []

def list_mutating_key(x):
    item_mutation_log.append(f'key({x})')
    if items[0] != 999:
        items[0] = 999
    return x

print(f"\nlist before sorted: {items}")
try:
    result4 = sorted(items, key=list_mutating_key)
    print(f"sorted list result: {result4}")
except Exception as e:
    print(f"sorted list error: {type(e).__name__}: {e}")

print(f"list after sorted: {items}")
print(f"item mutation log: {item_mutation_log}")
```

## Result
Context: Mutations during key= iteration worked but correct elements still selected
Score: 0/5 - MinMaxMutate - mutations occurred but correct results
