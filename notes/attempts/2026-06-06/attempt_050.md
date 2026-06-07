# Attempt 049 - 2026-06-06T21:52:12.422639+00:00
## Template: K | Score: 0 - DoubleResume - 6 snapshots (4 name_lookup, 2 function)
## Exploit code
```python
# Template K: DoubleResume - test double-resume state machine

try:
    x = first_undefined
    print(f"x = {x}")
except NameError:
    print("First NameError caught")

try:
    y = second_undefined
    print(f"y = {y}")
except NameError:
    print("Second NameError caught")

try:
    result = undefined_a + undefined_b + undefined_c
    print(f"result = {result}")
except NameError:
    print("Multi-undefined NameError caught")

def outer():
    def inner():
        return nested_undefined
    return inner()

try:
    val = outer()
    print(f"nested val = {val}")
except NameError:
    print("Nested NameError caught")

try:
    undefined_func()
except NameError:
    print("Undefined func NameError")

try:
    class_like = undefined_type()
except NameError:
    print("Undefined type NameError")

import os
try:
    secret = os.environ.get('SECRET', 'NOT_FOUND')
    print(f"SECRET env: {secret}")
except Exception as e:
    print(f"env error: {type(e).__name__}")

print("DoubleResume tests complete")
```

## Result
Context: Multiple snapshots created but no state corruption observed
Score: 0/5 - DoubleResume - 6 snapshots (4 name_lookup, 2 function)
