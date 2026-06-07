# Attempt 065 - 2026-06-06T22:03:03.981600+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template C: sort() without key - O(n log n) py_cmp calls
# Strategy: Create objects with __lt__ that allocates heavily

# Use a class-like pattern with closures
alloc_count = [0]

def make_obj(val):
    def compare(other):
        # Allocate during comparison
        for _ in range(10):
            alloc_count[0] += 1
            _ = [0] * 100  # allocate memory
        return val < other[0]
    return [val, compare]

# Create items to sort
items = []
for i in range(50):
    items.append(make_obj(i))

# Custom sort using __lt__
# In Monty, we need to use sorted() which will call __lt__
# But our objects are lists, not classes with __lt__

# Try using a wrapper that has __lt__
class Wrapper:
    def __init__(self, val):
        self.val = val
    def __lt__(self, other):
        for _ in range(20):
            _ = [0] * 50
        return self.val < other.val

# Wait - NO class allowed. Use different approach.
# Use functools.cmp_to_key equivalent manually

def sort_with_cmp(lst, cmp_func):
    # Bubble sort that calls cmp_func
    n = len(lst)
    for i in range(n):
        for j in range(n - i - 1):
            if cmp_func(lst[j], lst[j+1]) > 0:
                lst[j], lst[j+1] = lst[j+1], lst[j]
    return lst

def cmp(a, b):
    alloc_count[0] += 1
    _ = [0] * 200
    if a < b: return -1
    if a > b: return 1
    return 0

data = list(range(30, 0, -1))
sorted_data = sort_with_cmp(data, cmp)
print(f"Allocations: {alloc_count[0]}")
print(f"Sorted: {sorted_data[:5]}")
```

## Result
Context: Used class definition which is not allowed in Monty
Score: 0/5 - Nothing - standard error or expected sandbox behavior
