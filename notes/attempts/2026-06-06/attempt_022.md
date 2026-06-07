# Attempt 021 - 2026-06-06T21:04:00.877204+00:00
## Template: G | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template G: Resource limit race in sorted() callbacks
# Fill memory, then sort - MemoryError mid-sort may corrupt state

# Phase 1: Fill memory to near limit
chunks = []
for i in range(400):
    chunks.append([0] * 2000)
print(f'Phase 1: allocated {len(chunks)} chunks')

# Phase 2: Create list to sort
items = list(range(100, 0, -1))  # Reverse sorted
print(f'Phase 2: created {len(items)} items to sort')
print(f'Before sort: first={items[0]}, last={items[-1]}')

# Phase 3: Try to sort - may hit MemoryError mid-sort
try:
    result = sorted(items)
    print(f'Phase 3: sorted successfully')
    print(f'After sort: first={result[0]}, last={result[-1]}')
except MemoryError as e:
    print(f'Phase 3: MemoryError during sort: {e}')
    # Check if items list is corrupted
    print(f'Items after error: len={len(items)}, first={items[0]}, last={items[-1]}')

# Phase 4: Check if we can still allocate
try:
    test = [0] * 1000
    print(f'Phase 4: can still allocate')
except MemoryError:
    print(f'Phase 4: memory exhausted')
```

## Result
Context: MemoryError: memory limit exceeded: 1057712 bytes > 1048576 bytes; mem(1057712/1048576)
Score: 0/5 - Nothing - standard error or expected sandbox behavior
