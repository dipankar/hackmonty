# Attempt 111 - 2026-06-06T23:01:09.529502+00:00
## Template: A | Score: 0 - Nothing
## Exploit code
```python
# Template A: Dict Re-entry without classes
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
mutation_count = [0]
def evil_key(k):
    mutation_count[0] += 1
    d[str(mutation_count[0])] = mutation_count[0]
    return k
try:
    result = sorted(d.keys(), key=evil_key)
    print(f"sorted: {len(result)} keys")
    print(f"dict size now: {len(d)}")
except Exception as e:
    print(f"Error: {e}")
```

## Result
Context: Dict mutation during sorted() allowed but no corruption
Score: 0/5 - Nothing
