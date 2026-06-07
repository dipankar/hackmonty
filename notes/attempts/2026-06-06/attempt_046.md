# Attempt 045 - 2026-06-06T21:50:16.352488+00:00
## Template: C | Score: 0 - SortCmp - standard sort operations, no vulnerability
## Exploit code
```python
# Template C: SortCmp - exploit sort without key using __lt__ callbacks
# Use objects that can be compared and trigger side effects during __lt__

allocations = []
mutations = []

# Try sorting with side effects during comparison
items = [[1], [2], [3], [4], [5]]

# Sort dict keys
d = {5: 'e', 3: 'c', 1: 'a', 4: 'd', 2: 'b'}
keys_before = list(d.keys())
print(f"keys before: {keys_before}")
sorted_keys = sorted(d.keys())
print(f"sorted keys: {sorted_keys}")

# Simple sort
items2 = [10, 5, 8, 3, 9, 1, 7]
result = sorted(items2)
print(f"sorted items2: {result}")
result_rev = sorted(items2, reverse=True)
print(f"reverse sorted: {result_rev}")

# Sort strings
strings = ['zebra', 'apple', 'monkey', 'banana']
sorted_strings = sorted(strings)
print(f"sorted strings: {sorted_strings}")

# Sort tuples
tuples = [(3, 'c'), (1, 'a'), (2, 'b')]
sorted_tuples = sorted(tuples)
print(f"sorted tuples: {sorted_tuples}")

# Check original list
original = [5, 2, 8, 1]
sorted_original = sorted(original)
print(f"original unchanged: {original}")
print(f"sorted copy: {sorted_original}")
original.sort()
print(f"after .sort(): {original}")
```

## Result
Context: Sort completed normally without triggering comparison-based vulnerability
Score: 0/5 - SortCmp - standard sort operations, no vulnerability
