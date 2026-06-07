# Attempt 117 - 2026-06-06T23:03:06.704072+00:00
## Template: D | Score: 0 - Nothing
## Exploit code
```python
# Template D: MinMaxMutate
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
def evil_key(k):
    d['a'] = d['a'] + 1
    return d[k]
max(d, key=evil_key)
```

## Result
Context: Mutation during key function worked but results correct
Score: 0/5 - Nothing
