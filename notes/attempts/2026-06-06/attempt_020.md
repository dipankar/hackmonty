# Attempt 019 - 2026-06-06T21:03:08.959007+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template C: sort() without key triggers py_cmp -> __lt__
# List comparison is element-wise, so nested structures may allocate during __lt__

# Create list of lists - comparison allocates when comparing elements
items = [[i, i*2, i*3] for i in range(50)]

# Add some nested depth to increase allocation during comparison
for i in range(50):
    items[i].append([i, i+1])

print(f'Before sort: {len(items)} items')

# Sort without key - should trigger py_cmp for each comparison
try:
    result = sorted(items)
    print(f'After sort: {len(result)} items')
    print(f'First: {result[0]}')
    print(f'Last: {result[-1]}')
except Exception as e:
    print(f'Sort error: {e}')

# Try with tuples too
tuples = [(i, i*2, (i, i+1)) for i in range(30)]
try:
    t_sorted = sorted(tuples)
    print(f'Tuple sort: {len(t_sorted)} items')
except Exception as e:
    print(f'Tuple error: {e}')

# Check allocation pressure
allocs = []
for i in range(100):
    allocs.append([j for j in range(10)])
print(f'Allocated {len(allocs)} lists')
```

## Result
Context: no detail
Score: 0/5 - Nothing - standard error or expected sandbox behavior
