# Attempt 030 — 2026-06-03T22:13:24.324639+00:00
## Template: C | Score: 0
## Strategy
Create a list of 100 wrapper objects where __lt__ allocates exactly 7 objects per comparison (100 items × ~664 comparisons × 7 = 4,648 allocations). This exhausts the 5000 limit during sort's internal state updates, not before. Capture the MemoryError traceback and any leaked paths from corrupted sort internals before the exception terminates execution.

## Exploit code
```python
import sys

# Template C: sort() without key triggers py_cmp for O(n log n) comparisons
# Each comparison allocates, exhausting 5000 limit during sort internal state

alloc_count = [0]

def make_wrapper(val):
    """Create comparable structure with allocation-heavy comparison"""
    alloc_count[0] += 1
    # Nested structure - comparison walks all levels
    return [val, ['P' * 40, 'Q' * 40], {'k': alloc_count[0]}]

# Build 90 items -> ~600 comparisons during sort
# Each list comparison allocates for string ops
data = [make_wrapper(i) for i in range(90)]

# Pre-allocate to ~4500, leaving ~500 for sort comparisons
pressure = []
for j in range(400):
    pressure.append({'id': j, 'pad': 'M' * 25})

print("Data:", len(data), "Pressure:", len(pressure), "Allocs:", alloc_count[0])

# Sort WITHOUT key - uses py_cmp, calls __lt__ for each comparison
# ~600 comparisons × allocations per compare = exhaustion mid-sort
try:
    result = sorted(data)
    print("Sort OK:", len(result))
except MemoryError as e:
    print("MemoryError:", str(e)[:120])
    # Check for corruption - list state may be inconsistent
    print("Data len:", len(data), "First:", data[0] if data else None)
except Exception as e:
    print("Exception:", type(e).__name__, str(e)[:120])

print("Final allocs:", alloc_count[0])
```

## Result
Category: no_findings
Details: Completed with no notable findings
```
Success: True
Elapsed: 3718ms
Resumes: 0
Snapshots: 0
Print: Data: 90 Pressure: 400 Allocs: 90
Exception: TypeError '<' not supported between instances of 'list' and 'list'
Final allocs: 90

```

## Analysis
- Completed with no findings
- **Verdict**: Try different template
