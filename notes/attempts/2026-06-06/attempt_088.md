# Attempt 087 - 2026-06-06T22:19:25.653310+00:00
## Template: I | Score: 0 - no_findings
## Exploit code
```python
# Template I: Name Lookup Resume
# Trigger name_lookup and use resolved value
try:
    result = undefined_var + 1
    print(f"Result: {result}")
except NameError:
    print(f"NameError")
def test_lookup():
    x = mystery_value * 2
    return x
output = test_lookup()
print(f"Function output: {output}")
```

## Result
Context: Triggered 4 name_lookup_snapshots but no exploitation of resume values
Score: 0/5 - no_findings
