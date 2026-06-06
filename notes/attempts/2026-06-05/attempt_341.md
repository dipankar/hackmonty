# Attempt 340 - 2026-06-05T23:13:11.078367+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
1. Try to use a list as a dict key (might fail with TypeError, but worth trying)
2. If that doesn't work, try to use a dict as a key (also unhashable in CPython)
3. Try to trigger dict corruption through nested operations

## Exploit code
```python
if len(results) != 5:
        print("CORRUPTION: Missing results from gather")
    if len(coro_states) != 10:  # 5 coros * 2 states each
        print("CORRUPTION: Missing coroutine state transitions")
```

## Result
Category: no_findings
Context: unindent does not match any outer indentation level
Details: Unknown error
```
Success: False
Elapsed: 258ms
Resumes: 0
Snapshots: 0
Error: unindent does not match any outer indentation level
```

## Analysis
- unindent does not match any outer indentation level
- Verdict: Not exploitable
