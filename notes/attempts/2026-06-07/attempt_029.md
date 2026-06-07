# Attempt 158 - 2026-06-07T21:32:10.671601+00:00
## Template: VECTOR 9 | Score: 0 - test
## Exploit code
```python
print("=== VECTOR 9: Generator Materialization (GH#364) ===")
g = (i for i in [1, 2, 3])
print("type(g):", type(g))
```

## Result
Context: Vector 9 - GH#364 confirmed: genexps materialized to lists
Score: 0/5 - test
