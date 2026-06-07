# Attempt 074 - 2026-06-06T22:09:06.781368+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template C: SortCmp - exploit sort without key function
# Sort calls py_cmp for every comparison, allocations drift during sort

# Create a large list without random
nums = list(range(500, 0, -1))  # [500, 499, ..., 1] - reverse sorted
print(f"Created list of {len(nums)} integers (reverse sorted)")

# Sort multiple times to drift allocation counter
for i in range(10):
    nums_sorted = sorted(nums)
    print(f"Sort {i+1}: {len(nums_sorted)} items")

# Check if list is corrupted
print(f"First 10: {nums_sorted[:10]}")
print(f"Last 10: {nums_sorted[-10:]}")

# Try sorting tuples (comparison goes element by element)
tuples = [(i, i*2) for i in range(200)]
print(f"\nSorting {len(tuples)} tuples")
tuples_sorted = sorted(tuples)
print(f"First 5: {tuples_sorted[:5]}")

# Try sorting with reverse=True
nums_desc = sorted(nums, reverse=True)
print(f"\nReverse sorted first 10: {nums_desc[:10]}")

# Check for any anomalies
if len(nums_sorted) != 500:
    print(f"ANOMALY: Length changed from 500 to {len(nums_sorted)}")
if nums_sorted != sorted(nums_sorted):
    print("ANOMALY: Sort is not stable/idempotent")

print("\nDone")
```

## Result
Context: Sort operations completed normally, no corruption or allocation issues
Score: 0/5 - Nothing - standard error or expected sandbox behavior
