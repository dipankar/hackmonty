# Attempt 031 — 2026-06-03T22:15:02.458187+00:00
## Template: G | Score: 0
## Strategy
Pre-allocate exactly 4950 objects to approach the limit, then create 50 wrapper objects where __lt__ allocates exactly 1 object per comparison. When sorted() is called, the remaining ~50 allocations will be consumed in ~10 comparisons, firing MemoryError while the sort's internal index permutation is mid-update. Capture the resulting Rust panic traceback which should leak internal file paths from the corrupted sort state before the exception terminates.

## Exploit code
```python
import sys
pool = []
count = [0]
def alloc():
    count[0] += 1
    return {'n': count[0], 'p': 'X' * 40}
# Pre-allocate 4940 objects to approach 5000 limit
for _ in range(4940):
    pool.append(alloc())
# 50 items to sort - sorted() with key= calls key
```

## Result
Category: resource_exhaustion
Details: Resource limit hit (expected sandbox behavior)
```
Success: False
Elapsed: 569ms
Resumes: 0
Snapshots: 0
Error: MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 9, in <module>
    pool.append(alloc())
                ~~~~~~~
  File "main.py", line 6, in alloc
    return {'n': count[0], 'p': 'X' * 40}
                                ~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000
Print: 
```

## Analysis
- Resource limit hit (allocation/memory)
- **Verdict**: Not exploitable — adjust strategy
