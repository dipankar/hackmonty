# Attempt 022 - 2026-06-06T21:04:35.876725+00:00
## Template: I | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template I: Name lookup resume manipulation
# Use undefined variables in expressions, not just print

# Try arithmetic with undefined var
try:
    x = undefined_num + 5
except NameError as e:
    print(f'Arithmetic error: {e}')

# Try string concat with undefined var  
try:
    s = undefined_str + "hello"
except NameError as e:
    print(f'String error: {e}')

# Try dict access with undefined var as key
d = {'a': 1, 'b': 2}
try:
    v = d[undefined_key]
except NameError as e:
    print(f'Dict key error: {e}')

# Try calling undefined function
try:
    result = undefined_func(1, 2, 3)
except NameError as e:
    print(f'Func call error: {e}')

# Try undefined in list comprehension
try:
    lc = [undefined_lc for i in range(3)]
except NameError as e:
    print(f'List comp error: {e}')

# Try attribute access on undefined
try:
    attr = undefined_obj.some_attr
except NameError as e:
    print(f'Attr error: {e}')

# Try undefined in condition
try:
    if undefined_cond:
        print('true')
    else:
        print('false')
except NameError as e:
    print(f'Condition error: {e}')
```

## Result
Context: name_lookup(undefined_num); name_lookup(undefined_str); name_lookup(undefined_key)
Score: 0/5 - Nothing - standard error or expected sandbox behavior
