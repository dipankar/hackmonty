# Attempt 133 - 2026-06-06T23:18:03.797478+00:00
## Template: K | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# DoubleResume - trigger name_lookup multiple times
try:
    x = VAR_ONE
except:
    pass
try:
    y = VAR_TWO
except:
    pass
try:
    z = VAR_THREE
except:
    pass
print("completed")
```

## Result
Context: DoubleResume - 3 name_lookup snapshots triggered, print suppressed after first, no output
Score: 0/5 - Nothing - standard error or expected sandbox behavior
