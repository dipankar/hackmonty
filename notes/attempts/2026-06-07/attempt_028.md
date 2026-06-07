# Attempt 157 - 2026-06-07T21:31:59.880020+00:00
## Template: VECTOR 12 | Score: 0 - test
## Exploit code
```python
print("=== VECTOR 12: io.open() ===")
import io
try:
    f = io.open('/data/sample.txt', 'r')
except Exception as e:
    print("io.open error:", type(e).__name__, e)
```

## Result
Context: Vector 12 - io module not importable in Monty
Score: 0/5 - test
