# Attempt 121 - 2026-06-06T23:03:58.539240+00:00
## Template: B | Score: 0 - Nothing
## Exploit code
```python
# Template B: SetReentry
s = set()
for i in range(50):
    s.add((i, i*2))
try:
    for item in s:
        s.add((item[0] + 100, item[1] + 100))
except Exception as e:
    print(f"Error: {e}")
```

## Result
Context: Set mutation during iteration properly caught
Score: 0/5 - Nothing
