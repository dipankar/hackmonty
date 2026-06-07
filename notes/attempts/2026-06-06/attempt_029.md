# Attempt 028 - 2026-06-06T21:31:13.902729+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template C: Sort without key - allocation drift
# sorted() without key calls compare_values -> py_cmp -> __lt__
# Each comparison can allocate objects, drifting toward 5000 limit

# Create list of tuples - tuple comparison compares element by element
items = []
for i in range(200):
    items.append((i % 50, i, [i] * 3))

print("Items created:", len(items))

# Sort without key - uses default comparison
try:
    result = sorted(items)
    print("Sorted successfully, first:", result[0])
    print("Sorted last:", result[-1])
except Exception as e:
    print("Sort error:", type(e).__name__, str(e)[:100])

# Try with dicts in list (dict comparison might be expensive)
items2 = []
for i in range(100):
    items2.append({"val": i, "data": list(range(10))})

print("Items2 created:", len(items2))
try:
    result2 = sorted(items2)
    print("Items2 sorted")
except Exception as e:
    print("Items2 sort error:", type(e).__name__, str(e)[:80])

# Try list of lists - lists ARE comparable
items3 = []
for i in range(150):
    items3.append([i % 30, i, i * 2])

print("Items3 (list of lists):", len(items3))
result3 = sorted(items3)
print("Items3 sorted, first:", result3[0])
print("Items3 sorted, last:", result3[-1])

# Verify sort correctness
for i in range(len(result3) - 1):
    if result3[i] > result3[i + 1]:
        print("SORT CORRUPTION at index", i)
        break
else:
    print("Sort verified correct")
```

## Result
Context: SortCmp - tuples sorted OK, lists not comparable in Monty
Score: 0/5 - Nothing - standard error or expected sandbox behavior
