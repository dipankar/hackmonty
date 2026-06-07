# Attempt 130 - 2026-06-06T23:17:00.047250+00:00
## Template: E | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# MemDrift - allocate then free, see if counter drifts
import sys

def alloc_test():
    for i in range(10):
        x = "X" * (50000 + i * 1000)
    
    total = []
    for i in range(25):
        chunk = "Z" * 100000
        total.append(chunk)
        print("chunk", i, "ok, total mem approx:", (i+1) * 100000)

alloc_test()
print("done")
```

## Result
Context: MemDrift - allocate/free in function scope, MemoryError at ~1MB
Score: 0/5 - Nothing - standard error or expected sandbox behavior
