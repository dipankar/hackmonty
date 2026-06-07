# Attempt 023 - 2026-06-06T21:05:41.339187+00:00
## Template: K | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template K: Double-resume state machine
# Use the same undefined variable multiple times to test state consistency

# Same undefined name used in different contexts
results = []

# First use
try:
    x = undefined_x
except NameError:
    results.append('first')

# Second use  
try:
    y = undefined_x + 1
except NameError:
    results.append('second')

# Third use
try:
    z = undefined_x * 2
except NameError:
    results.append('third')

# Fourth use in function call
try:
    undefined_x(5)
except NameError:
    results.append('fourth')

# Fifth use as attribute
try:
    undefined_x.attr
except NameError:
    results.append('fifth')

print(f'Results: {results}')
print(f'Count: {len(results)}')

# Also test with dict key access
d = {}
try:
    d[undefined_x] = 1
except NameError:
    print('Dict key lookup caught')

# Test in list
try:
    lst = [undefined_x, 1, 2]
except NameError:
    print('List element caught')
```

## Result
Context: name_lookup(undefined_x); name_lookup(undefined_x); name_lookup(undefined_x)
Score: 0/5 - Nothing - standard error or expected sandbox behavior
