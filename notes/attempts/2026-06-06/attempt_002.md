# Attempt 001 - 2026-06-06T19:35:28.214512+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template C: sort() without key - O(n log n) py_cmp calls
# Create large list and sort to trigger many comparisons

# Build a list with many elements
items = list(range(500, 0, -1))  # 500 items, reversed
print('List size:', len(items))

# Pre-allocate some memory to drift the counter
buffers = []
for i in range(100):
    buffers.append([0] * 100)
print('Pre-allocated buffers:', len(buffers))

# Now sort - this should trigger ~4500 comparisons (500 * log2(500))
print('Starting sort...')
items.sort()
print('Sort complete')
print('First 10:', items[:10])
print('Last 10:', items[-10:])

# Check if we can still allocate after sort
try:
    more = [0] * 10000
    print('Post-sort allocation succeeded')
except MemoryError:
    print('Post-sort MemoryError - limit hit during sort')

# Try another sort
items2 = list(range(200, 0, -1))
items2.sort()
print('Second sort complete, first 5:', items2[:5])
```

## Result
Context: no detail
Score: 0/5 - Nothing - standard error or expected sandbox behavior
