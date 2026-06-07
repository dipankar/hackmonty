# Attempt 144 - 2026-06-07T15:22:43.224241+00:00
## Template: I | Score: 0 - Nothing - no findings
## Exploit code
```python
import os

try:
    # Trigger name_lookup_snapshot - undefined_var not defined
    # Sandbox pauses, orchestrator provides crafted value (e.g., "/etc/passwd")
    # Expression completes and result leaks into output field
    result = "Path: " + undefined_var
    
    # This print may be suppressed after resume, but result is captured
    print(f"Result: {result}")
except NameError as e:
    print(f"NameError: {e}")
except Exception as e:
    print(f"Error: {e}")
```

## Result
Context: Template I NameLookup - name_lookup_snapshot triggered, auto-resolved to None, output None
Score: 0/5 - Nothing - no findings
