# Attempt 123 - 2026-06-06T23:04:46.627048+00:00
## Template: D | Score: 0 - Nothing
## Exploit code
```python
# Template D: MinMaxMutate
d = {i: i*10 for i in range(10)}
def logging_key(k):
    val = d.pop(k)
    d[k + 100] = val
    return val
max(d.keys(), key=logging_key)
```

## Result
Context: Dict mutation during iteration - max still returned valid result
Score: 0/5 - Nothing
