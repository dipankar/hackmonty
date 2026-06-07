# Attempt 084 - 2026-06-06T22:18:05.237409+00:00
## Template: B | Score: 0 - no_findings
## Exploit code
```python
# Template B: Set Re-entry
s = set()
s.add((1, 2))
s.add((3, 4))
counter = [0]
def side_effect(x):
    counter[0] += 1
    if counter[0] == 2:
        s.add(('injected',))
    return x
s2 = {side_effect(x) for x in range(10)}
print(f"s2: {s2}")
print(f"'injected' in s: {('injected',) in s}")
```

## Result
Context: Set operations work normally, no corruption detected
Score: 0/5 - no_findings
