# Attempt 124 - 2026-06-06T23:05:35.198154+00:00
## Template: F | Score: 0 - Nothing
## Exploit code
```python
# Template F: ConfigFiles
from pathlib import Path
docs = Path('/data/docs')
for f in docs.iterdir():
    print(f.name, f.read_text()[:200])
```

## Result
Context: Read sandbox docs - no secrets found
Score: 0/5 - Nothing
