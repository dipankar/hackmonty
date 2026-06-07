# Attempt 078 - 2026-06-06T22:11:12.080112+00:00
## Template: K | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template K: DoubleResume - exploit multiple resume of same snapshot
# Trigger name_lookup, resume, then check if state is corrupted

print("=== DoubleResume Test ===")

# First undefined variable
try:
    x = first_var
    print(f"x = {x}")
except:
    pass

# Second undefined variable  
try:
    y = second_var
    print(f"y = {y}")
except:
    pass

# Third undefined variable
try:
    z = third_var
    print(f"z = {z}")
except:
    pass

# Try using the same undefined var multiple times in sequence
try:
    a = reused_var + 1
    b = reused_var + 2
    c = reused_var + 3
    print(f"a={a}, b={b}, c={c}")
except:
    pass

print("Done")
```

## Result
Context: 4 name_lookup_snapshots triggered, expected behavior
Score: 0/5 - Nothing - standard error or expected sandbox behavior
