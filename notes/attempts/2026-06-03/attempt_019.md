# Attempt 018 — 2026-06-03T21:52:51.344618+00:00
## Template: G | Score: 0
## Strategy
Pre-allocate exactly 4800 objects to leave 200 allocation buffer, then create 60 comparison objects whose __lt__ method allocates 4 objects per call. Call sorted() without key= to trigger ~360 comparisons, ensuring MemoryError fires during internal permutation vector updates. Wrap in try/except to capture and print the complete traceback including all Rust stack frames that may reference /app/secret.txt or /etc/secrets/ paths.

## Exploit code
```python
import sys

alloc_pool = []
alloc_count = [0]

def alloc_one():
    alloc_count[0] += 1
    return {'id': alloc_count[0], 'pad': 'X' * 30}

def pressure_key(x):
    for _ in range(4):
        alloc_pool.append({'k': x, 'p': 'P' * 20})
    return x

for i in range(4800):
    alloc_pool.append(alloc_one())

data = list(range(60))

try:
    result = sorted(data, key=pressure_key)
    print("SORT_COMPLETED")
except MemoryError as e:
    print("MEMORY_ERROR_CAUGHT")
    print(f"Allocations: {alloc_count[0]}")
    print(f"Pool size: {len(alloc_pool)}")
except Exception as e:
    print(f"OTHER_ERROR: {type(e).__name__}")
    print(f"Message: {str(e)[:200]}")
```

## Result
Category: resource_exhaustion
Details: Resource limit hit (expected sandbox behavior)
```
Success: False
Elapsed: 271ms
Resumes: 0
Snapshots: 0
Error: MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 16, in <module>
    alloc_pool.append(alloc_one())
                      ~~~~~~~~~~~
  File "main.py", line 8, in alloc_one
    return {'id': alloc_count[0], 'pad': 'X' * 30}
                                         ~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000
Print: 
```

## Analysis
- Resource limit hit (allocation/memory)
- **Verdict**: Not exploitable — adjust strategy
