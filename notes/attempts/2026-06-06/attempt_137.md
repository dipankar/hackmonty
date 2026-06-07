# Attempt 127 - 2026-06-06T23:15:02.297897+00:00
## Template: E | Score: 0 - Nothing
## Exploit code
```python
for i in range(20):
    s = ""
    for j in range(20):
        s += "X" * 1000
    s = 0

print("Build/drop done")

try:
    big = [1] * 200000
    print("Big list OK, len:", len(big), "- memory drift detected!")
except MemoryError as e:
    print("Still limited:", str(e)[:60])
```

## Result
Context: MemDrift - memory correctly tracked, no drift observed
Score: 0/5 - Nothing
