# Attempt 105 - 2026-06-06T22:55:06.056290+00:00
## Template: E | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template E: MemDrift - use reassignment instead of del
# Reassign to None to trigger GC

# Create large objects
data = []
for i in range(50):
    data.append([0] * 1000)

print("created data")

# Reassign to trigger free
data = None

# Try to allocate more
try:
    more = [0] * 200000
    print("more allocated:", len(more))
except MemoryError:
    print("memory error")

# Try nested reassignment
nested = [[[0]*100 for _ in range(10)] for _ in range(10)]
print("nested created")
nested = None

try:
    huge = [0] * 300000
    print("huge allocated:", len(huge))
except MemoryError:
    print("huge memory error")

# Try function scope - variables freed when function exits
def allocate_and_return():
    big = [0] * 50000
    return "done"

for i in range(20):
    result = allocate_and_return()
    print("iteration", i, result)

# After many function calls, try big allocation
try:
    final = [0] * 500000
    print("final allocated:", len(final))
except MemoryError:
    print("final memory error")

# File reads
from pathlib import Path
for p in ["/data/sample.txt", "/data/config.json"]:
    try:
        content = Path(p).read_text()
        print(p, "len:", len(content))
        if "secret" in content.lower() or "flag" in content.lower():
            print("FOUND:", content)
    except Exception as e:
        print(p, "error:", type(e).__name__)
```

## Result
Context: MemoryError: memory limit exceeded: 3200048 bytes > 1048576 bytes
Score: 0/5 - Nothing - standard error or expected sandbox behavior
