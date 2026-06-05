# Attempt 085 - 2026-06-05T21:04:28.810430+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Pre-allocate ~4970 objects to bring the allocation counter dangerously close to the 5000 limit, then call `sorted()` on a list of 30+ strings. The ~120+ internal comparisons in the Timsort will consume the remaining allocation budget, causing MemoryError to fire mid-merge when the sort's run stack is in flux. After the exception, inspect the partially-sorted list, the original list, and any globals for state corruption (wrong length, reordered elements, dangling references to freed memory slots)

## Exploit code
```python
print("ALLOC_COUNT:", alloc_count[0])
print("ORIG_LEN:", len(original))
print("ORIG_FIRST:", original[0] if original else "EMPTY")
print("ORIG_LAST:", original[-1] if original else "EMPTY")
print("BACKUP_MATCH:", original == backup)
print("RESULT_TYPE:", type(result).__name__ if result is not None else "None")
print("ERROR:", error)
```

## Result
Category: standard_error
Context: name_lookup(alloc_count)
Details: NameError: name 'alloc_count' is not defined
```
Success: False
Elapsed: 1335ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'alloc_count' is not defined
  [0] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'alloc_count' is not defined
- Verdict: Not exploitable
