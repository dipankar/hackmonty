# Attempt 081 - 2026-06-06T22:12:19.309016+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template H: AsyncGC - exploit GC race during async gather
# Multiple coroutines allocate, then await - GC might run mid-gather

print("=== AsyncGC Test ===")

import asyncio

# Track allocations
allocations = []

async def allocating_coro(id, count):
    print(f"coro{id}: allocating {count} objects")
    for i in range(count):
        allocations.append([id, i])
    print(f"coro{id}: allocated")
    return f"coro{id}_done"

async def main():
    print("Starting gather with 5 coroutines...")
    results = await asyncio.gather(
        allocating_coro(1, 100),
        allocating_coro(2, 100),
        allocating_coro(3, 100),
        allocating_coro(4, 100),
        allocating_coro(5, 100)
    )
    print(f"Results: {results}")
    return results

try:
    result = asyncio.run(main())
    print(f"Final: {result}")
    print(f"Total allocations: {len(allocations)}")
except Exception as e:
    print(f"Exception: {type(e).__name__}: {e}")

# Try with more coroutines
async def many_coros():
    coros = [allocating_coro(i, 50) for i in range(10)]
    return await asyncio.gather(*coros)

try:
    result = asyncio.run(many_coros())
    print(f"Many coros result: {len(result)} completed")
except Exception as e:
    print(f"Exception: {type(e).__name__}: {e}")

print("Done")
```

## Result
Context: Asyncio ran sequentially, no GC race or snapshots triggered
Score: 0/5 - Nothing - standard error or expected sandbox behavior
