# Attempt 122 - 2026-06-06T23:04:17.974323+00:00
## Template: D | Score: 0 - Nothing
## Exploit code
```python
# Template D: MinMaxMutate
d = {1: 100, 2: 200, 3: 50, 4: 300, 5: 10}
def track_key(k):
    d[k] = d[k] - 50
    return d[k]
max(d.keys(), key=track_key)
```

## Result
Context: Mutation during key function - results still correct
Score: 0/5 - Nothing
