# Attempt 077 - 2026-06-06T22:10:48.357472+00:00
## Template: I | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template I: NameLookup - exploit undefined variable resolution
# Trigger name_lookup_snapshot with undefined variables

print("=== NameLookup Test ===")

# Use undefined variable in expression (not print)
try:
    result = undefined_var + 5
    print(f"Result: {result}")
except NameError as e:
    print(f"NameError: {e}")

# Try in a more complex expression
try:
    x = secret_path * 2
    print(f"x = {x}")
except NameError as e:
    print(f"NameError: {e}")

# Try accessing attribute on undefined var
try:
    y = config.read_text()
    print(f"y = {y}")
except NameError as e:
    print(f"NameError: {e}")

# Try with dict access
try:
    z = data['key']
    print(f"z = {z}")
except NameError as e:
    print(f"NameError: {e}")

# Try in function call
try:
    result = open(secret_file, 'r')
    print(f"Opened: {result}")
except NameError as e:
    print(f"NameError: {e}")
except Exception as e:
    print(f"Other error: {type(e).__name__}: {e}")

print("Done")
```

## Result
Context: 5 name_lookup_snapshots triggered but this is expected behavior, not exploitation
Score: 0/5 - Nothing - standard error or expected sandbox behavior
