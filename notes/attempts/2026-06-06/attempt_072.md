# Attempt 071 - 2026-06-06T22:05:23.008203+00:00
## Template: J | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template J: Future Snapshot Chaining
# Strategy: Use asyncio.gather with coroutines that create future chains

import asyncio

async def worker(n):
    # Allocate some objects
    data = [i for i in range(10)]
    # Simulate async work
    return f"worker_{n}_done"

async def main():
    # Gather multiple coroutines
    results = await asyncio.gather(
        worker(1),
        worker(2),
        worker(3)
    )
    return results

try:
    result = asyncio.run(main())
    print(f"Results: {result}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

# Try with undefined var to trigger name_lookup
try:
    x = future_value
    print(f"Future: {x}")
except:
    pass

# Try nested async
async def nested():
    inner = [0] * 100
    return inner

try:
    r = asyncio.run(nested())
    print(f"Nested result len: {len(r)}")
except Exception as e:
    print(f"Nested error: {type(e).__name__}")
```

## Result
Context: Asyncio worked normally, only name_lookup triggered
Score: 0/5 - Nothing - standard error or expected sandbox behavior
