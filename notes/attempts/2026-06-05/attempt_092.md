# Attempt 089 - 2026-06-05T22:00:51.021941+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Execute Future snapshot chaining

## Exploit code
```python
r1 = await nested_future(100, 0)
    r2 = await nested_future(200, 0)
    print(f"C1: {r1.get('id')} C2: {r2.get('id')}")
```

## Result
Category: no_findings
Context: Unexpected indentation
Details: Unknown error
```
Success: False
Elapsed: 331ms
Resumes: 0
Snapshots: 0
Error: Unexpected indentation
```

## Analysis
- Unexpected indentation
- Verdict: Not exploitable
