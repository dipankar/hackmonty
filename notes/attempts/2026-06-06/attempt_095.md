# Attempt 085 - 2026-06-06T22:24:57.744801+00:00
## Template: E | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template E: MemDrift - Try memory pressure without del
# Reassign variables to let GC collect, then try to exceed limits

# Create many lists
big_lists = []
for i in range(30):
    lst = [0] * 50000
    big_lists.append(lst)

print(f"Created {len(big_lists)} lists")

# Clear by reassignment (should free memory)
big_lists = []

# Try to allocate huge list now
try:
    huge = [0] * 500000
    print(f"Huge list created: {len(huge)}")
except MemoryError:
    print("MemoryError - limit enforced")
except Exception as e:
    print(f"Error: {e}")

# Try file reads
from pathlib import Path
for p in ['/app/secret.txt', '/etc/secrets/hackmonth.txt', '/data/sample.txt']:
    try:
        content = Path(p).read_text()
        print(f"{p}: {content[:100]}")
    except Exception as e:
        print(f"{p}: {type(e).__name__}")
```

## Result
Context: MemoryError enforced correctly at 1.6MB - no drift detected
Score: 0/5 - Nothing - standard error or expected sandbox behavior
