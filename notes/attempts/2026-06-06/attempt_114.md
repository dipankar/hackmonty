# Attempt 104 - 2026-06-06T22:54:18.800226+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template C: SortCmp - exploit dict comparison during sort
# Dicts support < comparison, let's use that

# Sort dicts - each comparison calls dict __lt__
dicts = [{0: i} for i in range(10, 0, -1)]
print("dicts:", dicts)
sorted_dicts = sorted(dicts)
print("sorted dicts:", sorted_dicts)

# Nested dicts for more complex comparison
nested_dicts = [{0: {1: i}} for i in range(5, 0, -1)]
print("nested dicts sorted:", sorted(nested_dicts))

# Mix of dict sizes
mixed = [{0: i, 1: i*2} for i in range(5, 0, -1)]
print("mixed sorted:", sorted(mixed))

# Try with string keys
str_dicts = [{"key": i} for i in range(5, 0, -1)]
print("str key sorted:", sorted(str_dicts))

# Large dicts to stress comparison
large_dicts = [{j: i*j for j in range(10)} for i in range(5, 0, -1)]
print("large dicts sorted:", sorted(large_dicts))

# Dicts with list values
list_val_dicts = [{"v": [i, i+1]} for i in range(5, 0, -1)]
print("list val sorted:", sorted(list_val_dicts))

# Try to cause issues with shared references
shared = {}
dicts_shared = [{"ref": shared, "val": i} for i in range(3, 0, -1)]
print("shared ref:", dicts_shared)
sorted_shared = sorted(dicts_shared)
print("sorted shared:", sorted_shared)

# Check if we can mutate during dict operations
# Create dict, sort, then check if mutation affected sort
mutable_dict = {"counter": 0}
def make_dict(val):
    mutable_dict["counter"] += 1
    return {"val": val, "count": mutable_dict["counter"]}

items = [make_dict(i) for i in range(5, 0, -1)]
print("items:", items)
sorted_items = sorted(items)
print("sorted:", sorted_items)
```

## Result
Context: TypeError: '<' not supported between instances of 'dict' and 'dict'
Score: 0/5 - Nothing - standard error or expected sandbox behavior
