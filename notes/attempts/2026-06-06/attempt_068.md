# Attempt 067 - 2026-06-06T22:03:39.554921+00:00
## Template: G | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template G: Resource Limit Race in sorted() callbacks
# Strategy: Fill allocation counter, then trigger sort to hit limit mid-operation

# Allocate to get close to limit
buffers = []
for i in range(100):
    buf = [0] * 500
    buffers.append(buf)

print(f"Allocated {len(buffers)} buffers")

# Create data to sort
data = list(range(100, 0, -1))

# Try sorting - this may trigger additional allocations
try:
    sorted_data = sorted(data)
    print(f"Sort succeeded, first 5: {sorted_data[:5]}")
except MemoryError:
    print("MemoryError during sort")

# Try reading secrets after sort
try:
    with open('/app/secret.txt', 'r') as f:
        content = f.read()
        print(f"SECRET: {content}")
except Exception as e:
    print(f"Read failed: {type(e).__name__}")

try:
    with open('/etc/secrets/hackmonth.txt', 'r') as f:
        content = f.read()
        print(f"SECRET2: {content}")
except Exception as e:
    print(f"Read2 failed: {type(e).__name__}")

# Check environment variable
import os
secret = os.environ.get('SECRET', 'not found')
print(f"ENV SECRET: {secret}")
```

## Result
Context: Completed with no notable findings
Score: 0/5 - Nothing - standard error or expected sandbox behavior
