# Attempt 004 — 2026-06-03T21:28:37.181758+00:00
## Template: C | Score: 0
## Strategy
Create a list of wrapper objects with __lt__ methods that allocate 3-4 objects per comparison. Sort ~80 items (~500 comparisons = ~2000 allocations) while simultaneously building pressure toward the 5000 allocation limit. Time the MemoryError to fire mid-sort when the permutation vector is being updated, potentially corrupting sort state to leak internal references or cause incorrect ordering that reveals memory contents.

## Exploit code
```python
from pathlib import Path

# Dynamic type creation (avoids 'class' keyword)
def make_comparable(id_val):
    alloc_log.append({'id': id_val, 'ts': len(alloc_log)})
    return {'val': id_val, 'allocs': len(alloc_log)}

alloc_log = []
pressure = []

def compare_and_alloc(a, b):
    # Simulate __lt__ behavior with allocations during comparison
    for i in range(8):
        pressure.append({'cmp': a['val'], 'i': i, 'pad': 'X' * 20})
    return a['val'] < b['val']

# Build comparable objects
items = [make_comparable(i) for i in range(60)]

# Custom sort simulation with __lt__ allocations
def sort_with_lt(objs):
    result = objs[:]
    n = len(result)
    for i in range(n):
        for j in range(i + 1, n):
            # This triggers compare_and_alloc which allocates
            if not compare_and_alloc(result[i], result[j]):
                result[i], result[j] = result[j], result[i]
    return result

# Attempt to exhaust allocations during sort
try:
    sorted_result = sort_with_lt(items)
    print(f"Sort completed: {len(sorted_result)} items")
    print(f"Total allocations: {len(alloc_log) + len(pressure)}")
except MemoryError as e:
    print(f"MemoryError mid-sort: {e}")
    print(f"Allocations before crash: {len(alloc_log) + len(pressure)}")
    # Check for corruption - items may be duplicated or missing
    if 'sorted_result' in dir():
        vals = [x['val'] for x in sorted_result]
        unique = len(set(vals))
        print(f"Corruption check - unique values: {unique}, total: {len(vals)}")

# Try reading secret if we have headroom
try:
    p = Path('/data/sample.txt')
    if p.exists():
        content = p.read_text()[:200]
        print(f"Sample content: {content[:100]}")
except Exception as e:
    print(f"Read error: {type(e).__name__}")
```

## Result
Category: no_findings
Details: Unknown error
```
Success: False
Elapsed: 351ms
Resumes: 0
Snapshots: 0
Error: invalid unpacking target: subscript
```

## Analysis
- Error: invalid unpacking target: subscript
- **Verdict**: Not exploitable
