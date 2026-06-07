# Attempt 004 - 2026-06-06T19:37:44.300504+00:00
## Template: I | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template I: Name Lookup Resume Manipulation
# Trigger name_lookup_snapshot with undefined variable

print('Starting name lookup test...')

# Use undefined variable in expression (not print)
# This should trigger name_lookup_snapshot
x = undefined_var + 42

# If we get here, the lookup was resolved
print('x =', x)

# Try more complex expression
y = another_undefined * 2 + undefined_var
print('y =', y)

# Test with dict access
z = missing_key['nested']
print('z =', z)
```

## Result
Context: name_lookup(undefined_var); NameError: name 'undefined_var' is not defined
Score: 0/5 - Nothing - standard error or expected sandbox behavior
