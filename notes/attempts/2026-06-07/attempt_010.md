# Attempt 140 - 2026-06-07T15:15:41.538038+00:00
## Template: A | Score: 0 - Nothing - standard error
## Exploit code
```python
import sys

inner = [1, 2, 3]
key = (inner, "x")
d = {key: 42}

def key_fn(k):
    inner[0] += 1
    d["_"] = 1
    return 0

try:
    sorted(d, key=key_fn)
    print("no crash")
    print(f"len={len(d)}")
except RuntimeError as e:
    print(f"re-entry: {e}")
except Exception as e:
    print(f"error: {e}")
```

## Result
Context: Template A DictReentry - tuples unhashable in Monty. TypeError.
Score: 0/5 - Nothing - standard error
