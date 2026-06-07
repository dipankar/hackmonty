# Attempt 148 - 2026-06-07T18:48:17.821169+00:00
## Template: C | Score: 0 - Nothing
## Exploit code
```python
print("=== SortCmp Exploit: Memory exhaustion during sort ===")

# Phase 1: Pre-fill allocation counter with dummy data
prefill = []
for i in range(4900):
    prefill.append(i)
print(f"Pre-filled {len(prefill)} items (push alloc counter high)")

# Phase 2: Build mixed-type list that forces comparisons during sort
items = []
for i in range(50):
    items.append(i)           # int
    items.append(str(i))      # str - TypeError trigger
    items.append([i])         # list - might compare differently
print(f"Mixed-type list: {len(items)} items")

# Phase 3: Try to sort - comparisons may trigger MemoryError
# when alloc counter hits 5000 mid-sort
try:
    items.sort()
    print("Sort completed (unexpected)")
except MemoryError as e:
    print(f"MemoryError caught: {e}")
    # Check for corruption
    try:
        actual_len = len(items)
        print(f"len(items) = {actual_len} (expected {len(items)})")
        for idx, val in enumerate(items):
            pass
        print(f"Items (first 10): {items[:10]}")
    except Exception as corruption:
        print(f"CORRUPTION DETECTED: {corruption}")
except TypeError as e:
    print(f"TypeError (expected): {e}")
    try:
        print(f"Items (first 10): {items[:10]}")
    except Exception as c:
        print(f"CORRUPTION DETECTED: {c}")
except Exception as e:
    print(f"Other error: {type(e).__name__}: {e}")
    try:
        print(f"Items still accessible: {len(items)} items")
    except:
        print("CATASTROPHIC corruption")
```

## Result
Context: Template C SortCmp - Memory exhaustion during sort with mixed types. TypeError prevented sort from starting.
Score: 0/5 - Nothing
