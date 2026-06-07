# Attempt 031 - 2026-06-06T21:32:45.178929+00:00
## Template: I | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template I: Name Lookup Resume Manipulation
# Use undefined variable to trigger name_lookup_snapshot
# Resume can inject arbitrary values

# Trigger name lookup for undefined variable
try:
    result = undefined_secret_var
    print("Got value:", result)
except NameError as e:
    print("NameError:", str(e)[:60])

# Try in expression context (not print)
try:
    x = undefined_x + 5
    print("x =", x)
except NameError as e:
    print("NameError x:", str(e)[:60])

# Try with function call
def use_val(v):
    return v * 2

try:
    output = use_val(undefined_func_arg)
    print("Output:", output)
except NameError as e:
    print("NameError func:", str(e)[:60])

# Try dict access with undefined key variable
d = {"real": 42}
try:
    val = d[undefined_key]
    print("Dict val:", val)
except NameError as e:
    print("NameError dict:", str(e)[:60])

# Try in conditional
try:
    if undefined_cond:
        print("True branch")
    else:
        print("False branch")
except NameError as e:
    print("NameError cond:", str(e)[:60])
```

## Result
Context: NameLookup - 5 name_lookup_snapshots triggered, no exploitation
Score: 0/5 - Nothing - standard error or expected sandbox behavior
