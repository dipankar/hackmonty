# Attempt 055 - 2026-06-06T21:57:24.636992+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template C: SortCmp - try to trigger allocation pressure during sort
items = list(range(100))

def alloc_key(x):
    temp = [i for i in range(50)]
    return x

print("Sorting with allocating key...")
try:
    result = sorted(items, key=alloc_key)
    print(f"Sort succeeded, len={len(result)}")
except Exception as e:
    print(f"Error: {e}")

items2 = list(range(50, 0, -1))
items2.sort()
print(f"Int sort: {items2[:10]}")
```

## Result
Context: Sort operations completed normally, no allocation pressure or corruption triggered
Score: 0/5 - Nothing - standard error or expected sandbox behavior
