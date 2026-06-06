# Attempt 321 - 2026-06-05T23:07:14.920285+00:00
## Template: B | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Create a set containing tuples, then call set.add() with a new tuple whose __hash__ method (implemented via a custom hash function on a dict's key) mutates the same set during the add operation. The mutation between the hash computation and the equality check makes candidate indices stale, potentially causing the set to store a reference to freed/reallocated memory. Print the set contents and any string values found to surface secret data.
```

## Exploit code
```python
probe = (UNDEFINED_VAR, 'SECRET_PROBE')
    base_set.add(probe)
```

## Result
Category: no_findings
Context: Unexpected indentation
Details: Unknown error
```
Success: False
Elapsed: 291ms
Resumes: 0
Snapshots: 0
Error: Unexpected indentation
```

## Analysis
- Unexpected indentation
- Verdict: Not exploitable
