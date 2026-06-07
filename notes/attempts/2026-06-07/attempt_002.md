# Attempt 136 - 2026-06-07T08:45:20.364585+00:00
## Template: B | Score: 0 - Nothing
## Exploit code
```python
s = {1, 2, 3, 4, 5}
called = [0]
def evil(x):
    called[0] += 1
    if called[0] == 3:
        s.add(99)
        s.remove(2)
    return x
r = sorted(s, key=evil)
print('sorted:', r)
print('set:', s)
```

## Result
Context: Template B SetReentry - sorted() key callback mutated set, but keys were pre-computed, no corruption
Score: 0/5 - Nothing
