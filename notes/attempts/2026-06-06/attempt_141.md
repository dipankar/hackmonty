# Attempt 131 - 2026-06-06T23:17:18.466152+00:00
## Template: G | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# AllocRace - fill allocation counter then sort to trigger MemoryError mid-sort
pool = []
for i in range(4990):
    pool.append(("x", i))

items = [(1,), (2,), (3,), (4,), (5,)] * 20
try:
    items.sort()
    print("sort completed, len:", len(items))
except Exception as e:
    print("Error:", e)
```

## Result
Context: AllocRace - pre-fill alloc counter to 4990 then sort, completed normally
Score: 0/5 - Nothing - standard error or expected sandbox behavior
