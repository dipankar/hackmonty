# Attempt 129 - 2026-06-06T23:16:28.998643+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# SortCmp - allocation exhaustion during sort
pool = []
for i in range(4900):
    pool.append(i * 1000)
items = list(range(200))
try:
    items.sort()
    print("sort ok, len:", len(items))
except Exception as e:
    print("Error:", e)
print("pool size:", len(pool))
```

## Result
Context: SortCmp - allocation prefill then sort, no MemoryError
Score: 0/5 - Nothing - standard error or expected sandbox behavior
