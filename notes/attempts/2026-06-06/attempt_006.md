# Attempt 005 - 2026-06-06T19:38:02.722541+00:00
## Template: K | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template K: Double-Resume State Machine
# Test if snapshot resume can be manipulated

print('Test 1: Simple undefined var')
a = magic_value

# If resume injects a path, try to use it
print('a =', a)
print('type(a) =', type(a))

# Try to use 'a' as a path if it's a string
if isinstance(a, str):
    from pathlib import Path
    p = Path(a)
    if p.exists():
        content = p.read_text()
        print('File content:', content[:200])
    else:
        print('Path does not exist:', a)

# Test 2: Another undefined var for potential second resume
b = secret_inject
print('b =', b)

# Test 3: Use in dict lookup
d = {'key': 'value'}
result = d.get(missing_key, 'default')
print('dict result:', result)
```

## Result
Context: name_lookup(magic_value); NameError: name 'magic_value' is not defined
Score: 0/5 - Nothing - standard error or expected sandbox behavior
