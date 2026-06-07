# Attempt 059 - 2026-06-06T21:59:33.820636+00:00
## Template: K | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template K: DoubleResume - trigger snapshot and test resume behavior
try:
    x = first_undefined
    print(f"x = {x}")
except NameError:
    print("First NameError")

try:
    y = second_undefined
    print(f"y = {y}")
except NameError:
    print("Second NameError")

try:
    z = first_undefined
    print(f"z = {z}")
except NameError:
    print("Third NameError")
```

## Result
Context: 3 name_lookup_snapshots triggered, no state corruption from double-resume
Score: 0/5 - Nothing - standard error or expected sandbox behavior
