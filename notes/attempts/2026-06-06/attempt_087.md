# Attempt 086 - 2026-06-06T22:19:08.535952+00:00
## Template: G | Score: 0 - resource_exhaustion
## Exploit code
```python
# Template G: Resource Limit Race
counter = [0]
allocated = []
def allocating_key(x):
    for i in range(50):
        allocated.append([x, i, x*i])
        counter[0] += 1
    return x
items = list(range(100))
result = sorted(items, key=allocating_key)
```

## Result
Context: Hit allocation limit 5001/5000 - expected sandbox behavior
Score: 0/5 - resource_exhaustion
