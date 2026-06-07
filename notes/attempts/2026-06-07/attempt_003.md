# Attempt 137 - 2026-06-07T08:52:22.169770+00:00
## Template: C | Score: 0 - Nothing
## Exploit code
```python
filler = [(i,) for i in range(4893)]
data = [i for i in range(100)]
try:
    data.sort()
    print("NO_ERROR")
except MemoryError:
    print("MEM_ERROR during sort")
    print("data len:", len(data))
    sorted_check = all(data[i] <= data[i+1] for i in range(len(data)-1))
    print("properly sorted:", sorted_check)
```

## Result
Context: Template C SortCmp - pre-filled to 4995 allocs, list.sort() completed normally. Not enough allocs consumed during sort to trigger MemoryError.
Score: 0/5 - Nothing
