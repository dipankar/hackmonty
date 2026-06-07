# Attempt 151 - 2026-06-07T21:30:10.204719+00:00
## Template: VECTOR 2 | Score: 0 - test
## Exploit code
```python
print("=== VECTOR 2: Async Coroutine Frames ===")
async def f():
    pass
c = f()
try:
    print("cr_frame:", c.cr_frame)
except AttributeError as e:
    print("No cr_frame:", e)
try:
    print("cr_code:", c.cr_code)
except AttributeError as e:
    print("No cr_code:", e)
try:
    c.close()
except:
    pass
```

## Result
Context: Vector 2 - Async coroutine frames: cr_frame and cr_code not available
Score: 0/5 - test
