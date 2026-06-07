# Attempt 160 - 2026-06-07T21:32:26.449578+00:00
## Template: VECTOR 6 | Score: 0 - test
## Exploit code
```python
print("=== VECTOR 6: __code__.replace() ===")
def f(): return "safe"
print("f.__code__:", f.__code__)
try:
    code = f.__code__.replace(co_consts=(None, "__import__", "os"))
except Exception as e:
    print("code.replace error:", type(e).__name__, e)
```

## Result
Context: Vector 6 - functions have no __code__ attribute in Monty
Score: 0/5 - test
