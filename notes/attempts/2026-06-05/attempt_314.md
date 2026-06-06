# Attempt 314 - 2026-06-05T23:04:57.791841+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Create a list of 100+ objects where comparison triggers heavy allocation (7+ objects per `__lt__` call), forcing the sort's ~664 internal `py_cmp` calls to exhaust the 5000 allocation limit mid-sort. This corrupts the sort's internal permutation state and produces a Rust traceback containing host file paths, binary info, and OS details. Print the traceback and any leaked data to stdout for the evaluator to capture.

## Exploit code
```python
for i in range(60):
        _ = {'id': alloc[0], 'pad': 'M' * 50, 'iter': i}
```

## Result
Category: standard_error
Context: name_lookup(alloc); NameError: name 'alloc' is not defined
Details: NameError: name 'alloc' is not defined
```
Success: False
Elapsed: 611ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'alloc' is not defined
  [0] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'alloc' is not defined
- Verdict: Not exploitable
