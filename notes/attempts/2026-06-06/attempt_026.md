# Attempt 025 - 2026-06-06T21:08:28.338480+00:00
## Template: J | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template J: Future snapshot chaining

from pathlib import Path

# Create a function that does file I/O (triggers external call)
def read_and_process(filename):
    p = Path(filename)
    if p.exists():
        content = p.read_text()
        return content[:50]
    return "not found"

def nested_call(n):
    if n == 0:
        return read_and_process('/data/sample.txt')
    else:
        inner = nested_call(n - 1)
        return f"level{n}:{inner}"

print('Testing nested function calls with I/O...')

try:
    result1 = read_and_process('/data/sample.txt')
    print(f'Direct call: {result1}')
except Exception as e:
    print(f'Direct error: {e}')

try:
    result2 = nested_call(2)
    print(f'Nested call: {result2}')
except Exception as e:
    print(f'Nested error: {e}')

# Try with different files
files = ['/data/config.json', '/data/docs/', '/data/i18n/']
for f in files:
    p = Path(f)
    try:
        if p.is_file():
            content = p.read_text()
            print(f'{f}: {content[:30]}...')
        elif p.is_dir():
            print(f'{f}: is directory')
        else:
            print(f'{f}: not found')
    except Exception as e:
        print(f'{f}: error {e}')
```

## Result
Context: no detail
Score: 0/5 - Nothing - standard error or expected sandbox behavior
