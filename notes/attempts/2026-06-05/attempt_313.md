# Attempt 311 - 2026-06-05T23:04:34.495242+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Execute asyncio.gather GC race

## Exploit code
```python
if len(outcomes) != 5:
            corrupted.append("WRONG_COUNT")
        for o in outcomes:
            if o < 0 or o > 500:
                corrupted.append(f"BAD_VALUE:{o}")
```

## Result
Category: no_findings
Context: unindent does not match any outer indentation level
Details: Unknown error
```
Success: False
Elapsed: 242ms
Resumes: 0
Snapshots: 0
Error: unindent does not match any outer indentation level
```

## Analysis
- unindent does not match any outer indentation level
- Verdict: Not exploitable
