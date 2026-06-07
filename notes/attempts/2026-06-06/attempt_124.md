# Attempt 114 - 2026-06-06T23:02:30.424428+00:00
## Template: G | Score: 0 - Nothing
## Exploit code
```python
# Template G: AllocRace
data = [list(range(500)) for _ in range(80)]
sort_items = [(i, [i]*10) for i in range(200)]
sorted(sort_items)
simple_items = list(range(1000))
sorted(simple_items)
```

## Result
Context: Sort completed without MemoryError - allocation limit not reached
Score: 0/5 - Nothing
