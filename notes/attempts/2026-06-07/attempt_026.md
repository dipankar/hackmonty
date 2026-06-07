# Attempt 155 - 2026-06-07T21:31:02.607393+00:00
## Template: VECTOR PROBE2 | Score: 0 - test
## Exploit code
```python
print("=== PROBE 2: No imports ===")
try:
    f = open('/data/sample.txt', 'r')
    print("sample.txt:", f.read()[:500])
    f.close()
except Exception as e:
    print("sample.txt error:", type(e).__name__, e)
try:
    f = open('/app/secret.txt', 'r')
    print("secret:", f.read()[:500])
    f.close()
except Exception as e:
    print("secret error:", type(e).__name__, e)
```

## Result
Context: Sandbox probe - /data files readable, /app/secret.txt PermissionError
Score: 0/5 - test
