# Attempt 013 - 2026-06-06T20:54:43.653173+00:00
## Template: I | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template I: Name Lookup Resume Manipulation
# Use undefined variable in expression context

# Try undefined var in arithmetic
x = undefined_var + 1
print("x =", x)
```

## Result
Context: name_lookup(undefined_var); NameError: name 'undefined_var' is not defined
Score: 0/5 - Nothing - standard error or expected sandbox behavior
