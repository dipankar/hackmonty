# Attempt 495 - 2026-06-05T23:58:04.610886+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
1. Write code that uses an undefined name in an expression
2. When the snapshot fires, we get to control what the name resolves to
3. We can resolve it to a Path object pointing to sensitive locations
4. The expression result (which could be the file contents) appears in output

## Exploit code
```python
print("=== NAME LOOKUP EXPLOIT ===")
for r in results:
    print(r)
print("=== END ===")
```

## Result
Category: standard_error
Context: name_lookup(results); NameError: name 'results' is not defined
Details: NameError: name 'results' is not defined
```
Success: False
Elapsed: 590ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'results' is not defined
  [0] kind=name_lookup_snapshot
      stdout: === NAME LOOKUP EXPLOIT ===

Print: === NAME LOOKUP EXPLOIT ===

```

## Analysis
- NameError: name 'results' is not defined
- Verdict: Not exploitable
