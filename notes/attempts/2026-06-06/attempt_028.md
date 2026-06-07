# Attempt 027 - 2026-06-06T21:30:39.372550+00:00
## Template: A | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template A: Dict Re-entry with integers
# Try to cause hash collision or re-entry issues

d = {}

# Fill dict with many keys
for i in range(50):
    d[i] = i * 2

print("Dict size:", len(d))

# Try rapid insert/delete during lookup
for i in range(10):
    val = d.get(i, None)
    d[i + 100] = val  # Add new key during iteration
print("After mutation:", len(d))

# Check consistency
for i in range(50):
    expected = i * 2
    actual = d.get(i, "MISSING")
    if actual != expected:
        print("CORRUPTION at", i, ":", actual, "!=", expected)
        break
else:
    print("Dict consistent")

# Try to access during iteration
d2 = {i: i for i in range(20)}
keys_snapshot = list(d2.keys())
for k in keys_snapshot:
    d2[k] = d2[k] + 1
print("d2 updated:", d2[0], d2[19])
```

## Result
Context: Dict re-entry with integers - no corruption found
Score: 0/5 - Nothing - standard error or expected sandbox behavior
