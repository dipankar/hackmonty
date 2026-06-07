# Attempt 125 - 2026-06-06T23:13:18.732428+00:00
## Template: A | Score: 0 - Nothing
## Exploit code
```python
# DictReentry test - frozenset keys with function elements
d = {}

def a_fn():
    pass

def b_fn():
    pass

k1 = frozenset([a_fn, 1])
k2 = frozenset([a_fn, 2])

d[k1] = 'a'
d[k2] = 'b'

print("len:", len(d))
print("hash k1:", hash(k1))
print("hash k2:", hash(k2))

for i in range(50):
    d[frozenset([a_fn, i])] = 'val_' + str(i)

print("after 50 inserts:", len(d))

try:
    r = d.get(k1)
    print("got k1:", r)
except Exception as e:
    print("error:", e)

print("final len:", len(d))
```

## Result
Context: DictReentry with frozenset keys - no reentry triggered
Score: 0/5 - Nothing
