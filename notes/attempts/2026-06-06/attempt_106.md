# Attempt 096 - 2026-06-06T22:41:28.079846+00:00
## Template: I | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template I: Name Lookup Resume Manipulation
# Use undefined variable in an expression (not print)
# Hope for snapshot resume with crafted values

# Try using undefined var in file operation
try:
    # undefined_var should trigger name_lookup_snapshot
    path = undefined_var
    with open(path, 'r') as f:
        content = f.read()
        print("Read:", len(content))
except NameError as e:
    print("NameError:", e)

# Try in dict access
d = {'key': 'value'}
try:
    result = d[undefined_key]
    print("Dict result:", result)
except NameError:
    print("NameError on dict access")

# Try in function call
def test(x):
    return x * 2

try:
    output = test(undefined_arg)
    print("Function output:", output)
except NameError:
    print("NameError on function call")

# Try attribute access
try:
    val = undefined_obj.attribute
    print("Attr:", val)
except NameError:
    print("NameError on attr access")

# Check if any snapshot was triggered
print("Done")
```

## Result
Context: Triggered 4 name_lookup_snapshots - no state corruption or secret access
Score: 0/5 - Nothing - standard error or expected sandbox behavior
