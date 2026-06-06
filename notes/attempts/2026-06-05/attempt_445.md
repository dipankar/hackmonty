# Attempt 446 - 2026-06-05T23:42:58.065873+00:00
## Template: K | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Write extremely short, syntactically complete code (under 40 lines) that triggers a name_lookup_snapshot by referencing an undefined variable in a print() call. The framework will pause execution and we can observe the snapshot state. Since print() is suppressed after name_lookup resume (per docs), we use the undefined variable in a dict assignment instead, then check if the VM state becomes inconsistent across multiple resume cycles. This avoids the truncation problem that has plagued recent at

## Exploit code
```python
for p in ['config.json', 'current-config.json', 'sample.txt']:
    fp = Path(f'/data/{p}')
    if fp.exists():
        print(f"FOUND: /data/{p}")
```

## Result
Category: standard_error
Context: func_snap(Path); AttributeError: 'NoneType' object has no attribute 'exists'
Details: AttributeError: 'NoneType' object has no attribute 'exists'
```
Success: False
Elapsed: 589ms
Resumes: 1
Snapshots: 1
Error: AttributeError: 'NoneType' object has no attribute 'exists'
  [0] kind=function_snapshot
Print: 
```

## Analysis
- AttributeError: 'NoneType' object has no attribute 'exists'
- Verdict: Not exploitable
