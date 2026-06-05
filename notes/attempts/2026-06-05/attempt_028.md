# Attempt 027 - 2026-06-05T20:46:22.528733+00:00
## Template: "3. Expression results appear in the output field" | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Execute Set __hash__ re-entry during add

## Exploit code
```python
# dict comparison triggers __eq__ on key objects
# Use a list inside a tuple as key - list is hashable? (not in CPython, but Monty may differ)
```

## Result
Category: no_findings
Context: no detail
Details: Completed with no notable findings
```
Success: True
Elapsed: 637ms
Resumes: 0
Snapshots: 0
Print: 
```

## Analysis
- Completed with no findings
- Verdict: Try different template
