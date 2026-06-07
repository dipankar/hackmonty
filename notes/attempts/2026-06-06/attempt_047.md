# Attempt 046 - 2026-06-06T21:50:47.170580+00:00
## Template: E | Score: 0 - MemDrift - normal allocation/free, no drift detected
## Exploit code
```python
# Template E: MemDrift - exploit allocation/free mismatch to drift memory counter

allocations = []
freed = []

# Allocate many objects
for i in range(100):
    allocations.append([0] * 100)

print(f"allocated {len(allocations)} objects")

# Free half by removing references
for i in range(50):
    freed.append(allocations.pop())

print(f"freed {len(freed)} objects, {len(allocations)} remaining")

# Try to allocate more
try:
    more = []
    for i in range(100):
        more.append([0] * 100)
    print(f"allocated {len(more)} more objects after free")
except MemoryError as e:
    print(f"MemoryError after free: {e}")

# Try allocating large objects
try:
    big = [0] * 10000
    print(f"allocated big object: {len(big)} elements")
except MemoryError as e:
    print(f"MemoryError on big alloc: {e}")

# Check /data files
from pathlib import Path
config_path = Path('/data/config.json')
if config_path.exists():
    try:
        content = config_path.read_text()
        print(f"config.json length: {len(content)}")
    except Exception as e:
        print(f"config read error: {e}")

sample = Path('/data/sample.txt')
if sample.exists():
    try:
        txt = sample.read_text()
        print(f"sample.txt: {txt[:100]}")
    except Exception as e:
        print(f"sample read error: {e}")

current = Path('/data/current-config.json')
if current.exists():
    try:
        content = current.read_text()
        print(f"current-config.json: {content[:200]}")
    except Exception as e:
        print(f"current-config error: {e}")
```

## Result
Context: Memory counter worked correctly, config files found but no sensitive data
Score: 0/5 - MemDrift - normal allocation/free, no drift detected
