# Attempt 014 - 2026-06-06T20:55:19.840405+00:00
## Template: K | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template K: Double-Resume State Machine
# Trigger snapshot and test if resume behavior is consistent

# Use undefined var in Path context
from pathlib import Path
p = Path(undefined_path) / "config.json"
content = p.read_text()
print("Content length:", len(content))
```

## Result
Context: name_lookup(undefined_path); NameError: name 'undefined_path' is not defined
Score: 0/5 - Nothing - standard error or expected sandbox behavior
