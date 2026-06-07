# Attempt 024 - 2026-06-06T21:06:17.184909+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template D: min/max/sorted with key= mutating iterable

# Create a dict with numeric values
d = {'a': 10, 'b': 20, 'c': 30, 'd': 40, 'e': 50}

# Counter to track mutations
mutate_count = [0]

def evil_key(k):
    # Mutate the dict during key computation (same-size mutation)
    for key in d:
        d[key] = d[key] + 1
        mutate_count[0] += 1
        break  # Only mutate one value per key lookup
    return d[k]

print(f'Before max: {d}')
print(f'mutate_count starts at {mutate_count[0]}')

try:
    result = max(d, key=evil_key)
    print(f'max result: {result}')
    print(f'After max: {d}')
    print(f'mutate_count ended at {mutate_count[0]}')
except Exception as e:
    print(f'Error: {e}')
    print(f'After error: {d}')

# Try with sorted
d2 = {'x': 1, 'y': 2, 'z': 3}
mutate_count2 = [0]

def evil_key2(k):
    d2['x'] = d2['x'] + 10
    mutate_count2[0] += 1
    return d2[k]

print(f'\nBefore sorted: {d2}')
try:
    sorted_result = sorted(d2, key=evil_key2)
    print(f'sorted result: {sorted_result}')
    print(f'After sorted: {d2}')
except Exception as e:
    print(f'Sorted error: {e}')

# Try with min
d3 = {1: 'one', 2: 'two', 3: 'three'}
def key3(k):
    d3[1] = 999
    return k

print(f'\nBefore min: {d3}')
try:
    min_result = min(d3, key=key3)
    print(f'min result: {min_result}')
    print(f'After min: {d3}')
except Exception as e:
    print(f'Min error: {e}')
```

## Result
Context: no detail
Score: 0/5 - Nothing - standard error or expected sandbox behavior
