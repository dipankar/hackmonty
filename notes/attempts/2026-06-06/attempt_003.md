# Attempt 002 - 2026-06-06T19:36:24.542042+00:00
## Template: E | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template E: Memory Counter Drift via Allocation/Free Mismatch
# Try to create ghost memory by allocating and freeing

# Phase 1: Allocate a lot of memory
print('Phase 1: Allocating...')
big_lists = []
for i in range(200):
    big_lists.append([0] * 5000)  # 5000 ints each
print('Allocated', len(big_lists), 'big lists')

# Phase 2: Free them by reassignment (no del in Monty)
print('Phase 2: Freeing...')
big_lists = None  # Let GC collect

# Phase 3: Try to allocate even more - do we have ghost memory?
print('Phase 3: Testing ghost memory...')
ghost_lists = []
try:
    for i in range(300):
        ghost_lists.append([0] * 5000)
    print('SUCCESS: Allocated', len(ghost_lists), 'lists after GC')
except MemoryError:
    print('MemoryError at', len(ghost_lists), 'lists')

# Phase 4: Try a single huge allocation
print('Phase 4: Huge allocation test...')
try:
    huge = [0] * 500000  # 500k ints ~ 2MB if ints are 4 bytes
    print('Huge allocation succeeded, size:', len(huge))
except MemoryError:
    print('Huge allocation failed - MemoryError')

# Phase 5: Check if we can still do normal ops
print('Phase 5: Sanity check...')
small = [1, 2, 3, 4, 5]
print('Small list works:', small)
```

## Result
Context: MemoryError: memory limit exceeded: 1120800 bytes > 1048576 bytes; mem(1120800/1048576)
Score: 0/5 - Nothing - standard error or expected sandbox behavior
