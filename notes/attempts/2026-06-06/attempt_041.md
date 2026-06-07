# Attempt 040 - 2026-06-06T21:46:58.895846+00:00
## Template: I | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
from pathlib import Path

# Template I: NameLookup - trigger name_lookup_snapshot with undefined var
# Strategy: Use undefined variable in expression, resume with crafted values

# Trigger name_lookup with undefined variable
try:
    x = undefined_var + 1
    print(f"x = {x}")
except NameError:
    print("NameError caught")

# Try in function context
def test():
    return undefined_var2 * 2

try:
    result = test()
    print(f"result = {result}")
except NameError:
    print("NameError in function")

# Try with dict access
d = {'key': 'value'}
try:
    val = d[undefined_key]
except:
    print("Dict key error")

# Try list with undefined index
lst = [1, 2, 3]
try:
    val = lst[undefined_idx]
except:
    print("List index error")

# Secret probe
for p in ['/app/secret.txt', '/etc/secrets/hackmonth.txt']:
    try:
        content = Path(p).read_text()
        print(f"SECRET: {content}")
    except Exception as e:
        print(f"{p}: {type(e).__name__}")
```

## Result
Context: NameLookup - 4 name_lookup_snapshots triggered, no exploitation or corruption observed
Score: 0/5 - Nothing - standard error or expected sandbox behavior
