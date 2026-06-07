# Attempt 108 - 2026-06-06T22:57:11.683782+00:00
## Template: K | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template K: DoubleResume - test snapshot resume manipulation
# Create name_lookup_snapshot and see if we can exploit multiple resumes

# Trigger undefined variable lookup
try:
    x = undefined_variable
    print("x =", x)
except NameError:
    print("name error caught")

# Try in expression context
result = None
try:
    result = another_undefined + 5
    print("result =", result)
except NameError:
    print("expression name error")

# Try with file operations that might trigger snapshots
from pathlib import Path

# Read files and use in expressions with undefined vars
try:
    content = Path("/data/sample.txt").read_text()
    combined = content + undefined_text
    print("combined:", combined[:50])
except Exception as e:
    print("file error:", type(e).__name__)

# Try nested undefined lookups
def nested_lookup():
    a = undefined_a
    b = undefined_b
    return a + b

try:
    nested_lookup()
except NameError:
    print("nested name error")

# Try to trigger multiple lookups in one expression
try:
    multi = undefined_1 + undefined_2 + undefined_3
    print("multi =", multi)
except NameError:
    print("multi name error")

# Check if we can access any special variables
special = ["__name__", "__doc__", "__file__", "__builtins__"]
for s in special:
    try:
        val = eval(s)
        print(s, "=", str(val)[:100])
    except Exception as e:
        print(s, "error:", type(e).__name__)
```

## Result
Context: name_lookup(undefined_variable); name_lookup(another_undefined); name_lookup(undefined_text)
Score: 0/5 - Nothing - standard error or expected sandbox behavior
