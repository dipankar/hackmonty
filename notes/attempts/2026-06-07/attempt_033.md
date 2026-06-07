# Attempt 162 - 2026-06-07T21:33:14.411378+00:00
## Template: CREATIVE max | Score: 0 - test
## Exploit code
```python
print("=== CREATIVE: max() with key callback ===")
pool = []
def max_key(x):
    if x == 4999:
        for i in range(4500):
            pool.append(i)
        return 0
    return x
try:
    result = max(range(5000), key=max_key)
except MemoryError:
    pass
```

## Result
Context: Test max() with key callback - hits alloc limit
Score: 0/5 - test
