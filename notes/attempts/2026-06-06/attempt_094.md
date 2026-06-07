# Attempt 084 - 2026-06-06T22:24:35.480551+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template C: SortCmp - Try tuple sorting with side effects
# Without classes, use tuples and trigger external calls during sort

# Create list of tuples - tuple comparison compares elements
items = [(i, i*2) for i in range(50, 0, -1)]

# Try to trigger allocation pressure during sort
# Each tuple comparison might allocate intermediate values
try:
    result = sorted(items)
    print(f"Sorted {len(result)} tuples")
    print(f"First: {result[0]}, Last: {result[-1]}")
except Exception as e:
    print(f"Error: {e}")

# Try with nested tuples for more comparison complexity
nested = [((i, i+1), i) for i in range(30, 0, -1)]
try:
    result2 = sorted(nested)
    print(f"Nested sorted: {len(result2)}")
except Exception as e:
    print(f"Nested error: {e}")

# Trigger name_lookup during sort attempt
try:
    x = undefined_var
    items_with_undefined = [(x, i) for i in range(5)]
    sorted(items_with_undefined)
except:
    print("Name lookup triggered during sort setup")
```

## Result
Context: Triggered name_lookup_snapshot during sort - no sort corruption detected
Score: 0/5 - Nothing - standard error or expected sandbox behavior
