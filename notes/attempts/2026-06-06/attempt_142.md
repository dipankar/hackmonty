# Attempt 132 - 2026-06-06T23:17:43.525680+00:00
## Template: I | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# NameLookup - trigger name_lookup_snapshot with undefined variable
data = UNDEFINED_VAR + "something"
print("result:", data)
```

## Result
Context: NameLookup - undefined variable triggered name_lookup_snapshot, auto-resolved to NameError
Score: 0/5 - Nothing - standard error or expected sandbox behavior
