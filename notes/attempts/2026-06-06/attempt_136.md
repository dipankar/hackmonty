# Attempt 126 - 2026-06-06T23:14:15.051135+00:00
## Template: C | Score: 0 - Nothing
## Exploit code
```python
pool = []

for i in range(4999):
    pool.append(i)

print("pool:", len(pool))

items = [9999999999 - i for i in range(20)]

try:
    r = sorted(items)
    print("sort OK, len:", len(r))
except MemoryError:
    print("MemoryError during sort!")
    print("items intact:", items[:5])
    print("pool:", len(pool))
except Exception as e:
    print("Error:", type(e).__name__, str(e)[:80])

print("pool:", len(pool))
```

## Result
Context: SortCmp - allocation exhaustion test, sort completed without MemoryError
Score: 0/5 - Nothing
