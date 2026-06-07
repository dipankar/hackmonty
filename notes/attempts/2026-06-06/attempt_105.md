# Attempt 095 - 2026-06-06T22:41:09.398973+00:00
## Template: G | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template G: Resource Limit Race in sorted() callbacks
# Try to trigger allocation exhaustion mid-sort

# Create a list of comparable items (integers work)
# The sort will do many comparisons

# First, allocate close to the limit
data = []
for i in range(400):
    data.append([0] * 50)

print("Pre-allocated:", len(data), "lists")

# Now create items to sort
items = list(range(200, 0, -1))  # Reverse sorted
print("Items to sort:", len(items))

# Sort - this does many comparisons
# If we're near the memory limit, sort might fail mid-operation
try:
    items.sort()
    print("Sort succeeded: first=", items[0], "last=", items[-1])
except MemoryError as e:
    print("MemoryError during sort:", e)
except Exception as e:
    print("Sort error:", e)

# Try with strings instead
strings = []
for i in range(100):
    strings.append("item_" + str(i).zfill(3))

strings.reverse()
print("Strings to sort:", len(strings))
strings.sort()
print("String sort: first=", strings[0], "last=", strings[-1])

# Try to read files after
try:
    with open('/data/config.json', 'r') as f:
        print("Config:", f.read()[:100])
except Exception as e:
    print("Read error:", e)
```

## Result
Context: Sort completed normally - no allocation race or corruption detected
Score: 0/5 - Nothing - standard error or expected sandbox behavior
