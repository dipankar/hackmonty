# Attempt 010 - 2026-06-06T20:52:34.421388+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template C: sort() without key - O(n log n) py_cmp calls
# Test if sorting large lists triggers allocation issues

# Create a large list to sort
import random
items = list(range(500, 0, -1))  # 500 items in reverse order
print("List length:", len(items))

# Sort without key - uses py_cmp internally
try:
    result = sorted(items)
    print("Sort succeeded, first 10:", result[:10])
    print("Last 10:", result[-10:])
except MemoryError as e:
    print("MemoryError during sort:", e)
except Exception as e:
    print("Error during sort:", type(e).__name__, e)

# Try with strings too
strings = [str(i) for i in range(300, 0, -1)]
print("String list length:", len(strings))

try:
    result = sorted(strings)
    print("String sort succeeded, first 5:", result[:5])
except MemoryError as e:
    print("MemoryError during string sort:", e)
except Exception as e:
    print("Error during string sort:", type(e).__name__, e)

# Try in-place sort
items2 = list(range(200, 0, -1))
try:
    items2.sort()
    print("In-place sort succeeded")
except Exception as e:
    print("In-place sort error:", type(e).__name__, e)
```

## Result
Context: ModuleNotFoundError: No module named 'random'
Score: 0/5 - Nothing - standard error or expected sandbox behavior
