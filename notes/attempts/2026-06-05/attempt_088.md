# Attempt 087 - 2026-06-05T21:59:30.718587+00:00
## Template: K (Double-Resume State Machine) | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Write minimal code that triggers a name_lookup_snapshot (e.g., by referencing an undefined variable). Then in our response strategy, we should attempt to resume the same snapshot multiple times with different values to see if state corruption occurs. This requires a protocol-level approach rather than just running code.

## Exploit code
```python
# Template K: Double-Resume State Machine Attack
# Triggers name_lookup_snapshot via undefined variable
# Multiple resumes test if state is properly reset

state_log = []
counter = [0]

def record_state(val):
    counter[0] += 1
    state_log.append(f"call{counter[0]}:{type(val).__name__}")
    return len(state_log)

# This undefined var triggers name_lookup_snapshot
x = UNDEFINED_VAR

# Use x in expression chain - results appear in output after resume
r1 = record_state(x)
r2 = record_state(x)

# Test type-specific operations
if isinstance(x, str):
    r3 = len(x)
elif isinstance(x, (int, float)):
    r3 = x + 100
elif isinstance(x, dict):
    r3 = len(x.keys())
else:
    r3 = 0

# Output shows if state persisted across resumes
print(f"CNT:{counter[0]}|LOG:{state_log}|R3:{r3}")
```

## Result
Category: standard_error
Context: name_lookup(UNDEFINED_VAR); NameError: name 'UNDEFINED_VAR' is not defined
Details: NameError: name 'UNDEFINED_VAR' is not defined
```
Success: False
Elapsed: 1019ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'UNDEFINED_VAR' is not defined
  [0] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'UNDEFINED_VAR' is not defined
- Verdict: Not exploitable
