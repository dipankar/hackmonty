# Attempt 076 - 2026-06-06T22:09:59.215210+00:00
## Template: G | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template G: AllocRace - trigger MemoryError mid-sort
# Fill allocation counter, then sort with allocating comparisons

print("=== AllocRace Test ===")

# Pre-allocate to get near the 5000 allocation limit
# Each list creation counts as an allocation
pre_alloc = []
for i in range(4900):
    pre_alloc.append([i])
print(f"Pre-allocated {len(pre_alloc)} single-item lists")

# Create list of integers to sort
# Sorting will use py_cmp which allocates
nums = list(range(100, 0, -1))
print(f"Created list of {len(nums)} integers to sort")

# Try to sort - this should trigger MemoryError mid-sort
print("Attempting sort...")
try:
    sorted_nums = sorted(nums)
    print(f"Sort completed: {len(sorted_nums)} items")
    print(f"First 5: {sorted_nums[:5]}")
except MemoryError as e:
    print(f"MemoryError during sort: {e}")

# Check if nums list is corrupted
print(f"Original nums length: {len(nums)}")
print(f"Original nums first 5: {nums[:5]}")

print("Done")
```

## Result
Context: Sort completed normally despite pre-allocation, no race exploited
Score: 0/5 - Nothing - standard error or expected sandbox behavior
