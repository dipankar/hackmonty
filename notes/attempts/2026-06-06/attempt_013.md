# Attempt 012 - 2026-06-06T20:53:43.275459+00:00
## Template: G | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template G: Resource Limit Race in sorted() callbacks
# Fill memory near limit, then sort to trigger mid-sort MemoryError

# First allocate to near limit (1MB = 1048576 bytes)
# Each list of 1000 zeros is ~8KB, so ~100 lists = ~800KB
data = []
for i in range(80):
    data.append([0] * 1000)
print("Allocated 80 lists")

# Create a list to sort - numbers that need comparison
to_sort = list(range(200, 0, -1))
print("Created list of", len(to_sort), "items to sort")

# Try to sort - this may trigger MemoryError mid-sort
try:
    result = sorted(to_sort)
    print("Sort completed, length:", len(result))
    print("First 5:", result[:5])
    print("Last 5:", result[-5:])
except MemoryError as e:
    print("MemoryError during sort:", e)
except Exception as e:
    print("Sort error:", type(e).__name__, e)

# Check if original list is still intact
print("Original to_sort length:", len(to_sort))

# Try with smaller list
small_sort = list(range(50, 0, -1))
try:
    result = sorted(small_sort)
    print("Small sort OK, length:", len(result))
except Exception as e:
    print("Small sort error:", type(e).__name__, e)
```

## Result
Context: MemoryError: memory limit exceeded: 1059296 bytes > 1048576 bytes; mem(1059296/1048576)
Score: 0/5 - Nothing - standard error or expected sandbox behavior
