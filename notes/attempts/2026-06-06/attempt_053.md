# Attempt 052 - 2026-06-06T21:53:59.468815+00:00
## Template: H | Score: 0 - AsyncGC - 1 name_lookup_snapshot in async
## Exploit code
```python
# Template H: AsyncGC - test async without sleep

import asyncio

async def simple_coro(n):
    data = [i * 2 for i in range(50)]
    return sum(data)

async def test_simple():
    results = await asyncio.gather(
        simple_coro(1),
        simple_coro(2),
        simple_coro(3)
    )
    print(f"results: {results}")
    return results

try:
    result = asyncio.run(test_simple())
    print(f"simple test completed: {result}")
except Exception as e:
    print(f"simple error: {type(e).__name__}: {e}")

async def undefined_coro():
    return undefined_async_var

async def test_undefined():
    try:
        result = await undefined_coro()
        print(f"result: {result}")
    except NameError:
        print("NameError in coro")

try:
    asyncio.run(test_undefined())
except Exception as e:
    print(f"undefined error: {type(e).__name__}: {e}")

async def inner():
    return "inner"

async def outer():
    return await inner()

try:
    nested = asyncio.run(outer())
    print(f"nested: {nested}")
except Exception as e:
    print(f"nested error: {type(e).__name__}: {e}")

print("AsyncGC tests complete")
```

## Result
Context: Asyncio worked normally, only name_lookup triggered
Score: 0/5 - AsyncGC - 1 name_lookup_snapshot in async
