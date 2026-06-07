# Attempt 032 - 2026-06-06T21:33:08.078576+00:00
## Template: K | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template K: Double-Resume State Machine
# Snapshots can be resumed multiple times - test state corruption

# Trigger multiple name lookups in sequence
try:
    a = undefined_a
    b = undefined_b
    c = undefined_c
    print("Values:", a, b, c)
except NameError as e:
    print("NameError:", str(e)[:60])

# Try with same undefined var used multiple times
try:
    x = undefined_x
    y = undefined_x + 1
    z = undefined_x * 2
    print("x,y,z:", x, y, z)
except NameError as e:
    print("NameError x:", str(e)[:60])

# Try in loop
results = []
for i in range(5):
    try:
        val = undefined_loop_var
        results.append(val)
    except NameError:
        results.append(None)
print("Loop results:", results)

# Nested try blocks
try:
    outer = undefined_outer
    try:
        inner = undefined_inner
        print("Both:", outer, inner)
    except NameError as e2:
        print("Inner error:", str(e2)[:40])
except NameError as e1:
    print("Outer error:", str(e1)[:40])
```

## Result
Context: DoubleResume - 8 name_lookup_snapshots, no state corruption observed
Score: 0/5 - Nothing - standard error or expected sandbox behavior
