# Attempt 156 - 2026-06-07T21:31:59.876216+00:00
## Template: VECTOR 8 | Score: 0 - test
## Exploit code
```python
print("=== VECTOR 8: Stack Overflow (GH#440) ===")
def recurse(n):
    return recurse(n+1) if n < 5000 else n
try:
    result = recurse(0)
except RecursionError as e:
    print("RecursionError:", e)
```

## Result
Context: Vector 8 - Stack overflow has RecursionError protection in Monty
Score: 0/5 - test
