# Attempt 112 - 2026-06-06T23:01:44.392220+00:00
## Template: C | Score: 0 - Nothing
## Exploit code
```python
# Template C: SortCmp
lists = [[i, i*2, i*3] for i in range(400)]
try:
    sorted(lists)
except Exception as e:
    print(f"Sort error: {e}")
tuples = [(i, i*2) for i in range(300)]
sorted(tuples)
print(f"Sorted {len(tuples)} tuples")
```

## Result
Context: List sort failed (no __lt__), tuple sort succeeded without issues
Score: 0/5 - Nothing
