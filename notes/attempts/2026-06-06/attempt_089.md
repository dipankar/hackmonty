# Attempt 088 - 2026-06-06T22:19:56.476090+00:00
## Template: K | Score: 0 - standard_error
## Exploit code
```python
# Template K: Double-Resume State Machine
x = secret_path
print(f"Secret path value: {x}")
from pathlib import Path
p = Path(x)
if p.exists():
    content = p.read_text()
    print(f"Content: {content[:100]}")
y = another_value
print(f"Another value: {y}")
```

## Result
Context: Name lookup triggered but resume values don't help - NameError still occurs
Score: 0/5 - standard_error
