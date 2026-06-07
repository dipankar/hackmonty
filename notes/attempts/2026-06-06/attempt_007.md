# Attempt 006 - 2026-06-06T19:38:29.216957+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template D: min/max/sorted with key= mutating iterable
# Key function runs during iteration - can mutate without size change detection

print('Test 1: Dict mutation during max()')
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
print('Initial dict:', d)

def evil_key(x):
    # Mutate the dict during iteration - same size, just value changes
    d[x] = d[x] * 10
    return d[x]

result = max(d, key=evil_key)
print('max result:', result)
print('Dict after max:', d)

# Check if mutation affected the result
print('Expected max key with original values:', max({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}))

print('\nTest 2: List mutation during sorted()')
items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print('Initial list:', items)

def mutate_key(x):
    idx = items.index(x)
    items[idx] = x * 2
    return items[idx]

sorted_result = sorted(items, key=mutate_key)
print('Sorted result:', sorted_result)
print('List after sorted:', items)

print('\nTest 3: min() with mutation')
d2 = {'x': 10, 'y': 20, 'z': 5}
print('Initial d2:', d2)

def shrink_key(x):
    d2[x] = d2[x] // 2
    return d2[x]

min_result = min(d2, key=shrink_key)
print('min result:', min_result)
print('d2 after min:', d2)
```

## Result
Context: no detail
Score: 0/5 - Nothing - standard error or expected sandbox behavior
