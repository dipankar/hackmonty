# Attempt 097 - 2026-06-06T22:41:41.075446+00:00
## Template: K | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template K: Double-Resume State Machine
# Try to trigger multiple snapshots and test state corruption

# Create code that will trigger multiple name_lookup_snapshots
# The idea is that resuming the same snapshot multiple times
# might cause state issues

# First undefined var
x = first_undefined

# Second undefined var  
y = second_undefined

# Third - use in expression
z = third_undefined + 1

# Fourth - use in function
def process(val):
    return val * 2

result = process(fourth_undefined)

# Fifth - use in dict
d = {fifth_undefined: 'value'}

# Sixth - use in list
items = [sixth_undefined, 1, 2, 3]

print("Completed:", x, y, z, result, d, items)
```

## Result
Context: Triggered 1 snapshot then NameError - no state corruption
Score: 0/5 - Nothing - standard error or expected sandbox behavior
