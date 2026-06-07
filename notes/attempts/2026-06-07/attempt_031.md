# Attempt 159 - 2026-06-07T21:32:26.462514+00:00
## Template: VECTOR 10 | Score: 0 - test
## Exploit code
```python
print("=== VECTOR 10: TOCTOU Write Race (GH#455) ===")
from pathlib import Path
p = Path('/data/tmp_test.txt')
try:
    p.write_text('test content')
except Exception as e:
    print("write error:", type(e).__name__, e)
```

## Result
Context: Vector 10 - /data is read-only FS, write fails with PermissionError
Score: 0/5 - test
