# Attempt 141 - 2026-06-07T15:17:02.204265+00:00
## Template: C | Score: 0 - Nothing - standard error
## Exploit code
```python
import functools

# Pre-fill allocation counter to ~4950
# Each tuple is 1 allocation
prefill = [(i, i+1) for i in range(4940)]

# Comparison function that allocates ~7 objects per call
def cmp_func(a, b):
    x = (a, b)
    y = [a, b]
    z = {a: b}
    w = (a, b, 1)
    v = [a, b, 1]
    u = {a: 1, b: 2}
    t = (a,)
    if a < b:
        return -1
    elif a > b:
        return 1
    return 0

# Create key function using cmp_to_key
key_func = functools.cmp_to_key(cmp_func)

# Create list of 150 items
items = list(range(150))

try:
    items.sort(key=key_func)
    print("Sort completed (unexpected)")
except MemoryError:
    print("MemoryError caught: exploit successful")
except Exception as e:
    print(f"Error: {e}")
```

## Result
Context: Template C SortCmp - functools module not available in Monty
Score: 0/5 - Nothing - standard error
