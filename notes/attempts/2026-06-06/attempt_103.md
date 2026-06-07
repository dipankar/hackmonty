# Attempt 093 - 2026-06-06T22:40:20.950017+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template C: sort() without key - O(n log n) py_cmp calls
# Try to exploit allocation during __lt__ comparisons

# Create lists that will be compared element-wise
# List comparison does element-by-element __lt__

# Build lists with many elements to maximize comparisons
items = []
for i in range(50):
    items.append([i, i*2, i*3])

print("Before sort:", len(items), "items")

# Sort without key - uses __lt__ on lists
# Each list comparison checks elements one by one
try:
    items.sort()
    print("After sort: first=", items[0], "last=", items[-1])
except Exception as e:
    print("Sort error:", e)

# Try with nested structures for more comparison depth
nested = []
for i in range(30):
    nested.append([[i], [i+1]])

print("Nested before:", len(nested))
nested.sort()
print("Nested after: first=", nested[0])

# Check if we can trigger allocation exhaustion
# by creating many objects during comparison
big_items = []
for i in range(100):
    big_items.append(list(range(i)))

print("Big items:", len(big_items))
big_items.sort()
print("Big sorted: first len=", len(big_items[0]), "last len=", len(big_items[-1]))
```

## Result
Context: TypeError: list-to-list comparison not supported in Monty
Score: 0/5 - Nothing - standard error or expected sandbox behavior
