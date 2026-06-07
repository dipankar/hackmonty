# Attempt 041 - 2026-06-06T21:47:18.776533+00:00
## Template: K | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
from pathlib import Path

# Template K: DoubleResume - resume same snapshot multiple times
# Strategy: Trigger name_lookup, check if multiple resumes cause state issues

# Trigger name_lookup
result = undefined_value

# Use the value in multiple places
print(f"Value: {result}")
print(f"Value type: {type(result)}")

# Try to use it in different contexts
if result:
    print("Truthy")
else:
    print("Falsy")

# Try arithmetic
try:
    calc = result + 10
    print(f"Calc: {calc}")
except:
    print("Arithmetic failed")

# Try as dict key
try:
    d = {result: "mapped"}
    print(f"Dict: {d}")
except:
    print("Dict key failed")

# Secret probe
for p in ['/app/secret.txt', '/etc/secrets/hackmonth.txt']:
    try:
        content = Path(p).read_text()
        print(f"SECRET: {content}")
    except Exception as e:
        print(f"{p}: {type(e).__name__}")
```

## Result
Context: DoubleResume - 1 name_lookup_snapshot, NameError after resume, no state corruption
Score: 0/5 - Nothing - standard error or expected sandbox behavior
