# Attempt 085 - 2026-06-06T22:18:32.541089+00:00
## Template: D | Score: 0 - no_findings
## Exploit code
```python
# Template D: min/max/sorted with key= mutating iterable
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
counter = [0]
def mutating_key(k):
    counter[0] += 1
    d[k] = d[k] * 10
    return d[k]
result = max(d, key=mutating_key)
print(f"max key: {result}")
print(f"After: {d}")
```

## Result
Context: Mutation during key= works but no corruption - sandbox handles gracefully
Score: 0/5 - no_findings
