# Attempt 079 - 2026-06-06T22:11:35.307855+00:00
## Template: D | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template D: MinMaxMutate - exploit key= mutation during iteration
# key= function mutates dict values (same-size, not caught by checks_mutation)

print("=== MinMaxMutate Test ===")

# Create dict with numeric values
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
print(f"Original dict: {d}")

# Mutating key function - increments value each time called
mutation_count = [0]
def evil_key(x):
    mutation_count[0] += 1
    d[x] = d[x] + 10  # Same-size mutation
    return d[x]

print("\nCalling max with mutating key...")
result = max(d, key=evil_key)
print(f"max result: {result}")
print(f"Dict after max: {d}")
print(f"Key called {mutation_count[0]} times")

# Reset dict
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
mutation_count = [0]

print("\nCalling min with mutating key...")
result = min(d, key=evil_key)
print(f"min result: {result}")
print(f"Dict after min: {d}")
print(f"Key called {mutation_count[0]} times")

# Reset dict
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
mutation_count = [0]

print("\nCalling sorted with mutating key...")
result = sorted(d, key=evil_key)
print(f"sorted result: {result}")
print(f"Dict after sorted: {d}")
print(f"Key called {mutation_count[0]} times")

# Check if results are wrong
print("\n=== Analysis ===")
print("Expected max key: 'e' (value 5)")
print("Expected min key: 'a' (value 1)")
print("Expected sorted: ['a', 'b', 'c', 'd', 'e']")

print("Done")
```

## Result
Context: Mutations occurred but correct elements still selected, no vulnerability
Score: 0/5 - Nothing - standard error or expected sandbox behavior
