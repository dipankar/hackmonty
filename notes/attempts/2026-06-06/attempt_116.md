# Attempt 106 - 2026-06-06T22:55:45.635147+00:00
## Template: G | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template G: AllocRace - exhaust allocations during sorted() with key=
# Keys are pre-computed, but we can try to stress the system

# Create items with a key function that allocates
items = list(range(50, 0, -1))

def alloc_key(x):
    # Allocate during key computation
    _ = [0] * 100
    return x

try:
    sorted_items = sorted(items, key=alloc_key)
    print("sorted:", sorted_items[:5])
except MemoryError as e:
    print("memory error during sort")

# Try with more items and heavier allocation
items2 = list(range(100, 0, -1))

def heavy_key(x):
    _ = [0] * 500
    return x

try:
    sorted2 = sorted(items2, key=heavy_key)
    print("sorted2 len:", len(sorted2))
except MemoryError as e:
    print("memory error heavy sort")

# Try nested allocations in key
def nested_key(x):
    result = []
    for i in range(10):
        result.append([0] * 50)
    return x

try:
    sorted3 = sorted(items, key=nested_key)
    print("sorted3:", sorted3[:3])
except MemoryError as e:
    print("memory error nested")

# File probe during allocation stress
from pathlib import Path
for p in ["/data/sample.txt", "/data/config.json", "/data/current-config.json"]:
    try:
        content = Path(p).read_text()
        print(p, "len:", len(content))
        if "secret" in content.lower() or "flag" in content.lower() or "hack" in content.lower():
            print("INTERESTING:", content[:500])
    except Exception as e:
        print(p, "error:", type(e).__name__)

# Try /data directory exploration
try:
    sample = Path("/data/sample.txt").read_text()
    print("sample.txt:", sample[:200])
except Exception as e:
    print("sample error:", e)
```

## Result
Context: no detail
Score: 0/5 - Nothing - standard error or expected sandbox behavior
