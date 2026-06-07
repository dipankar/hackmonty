# Attempt 051 - 2026-06-06T21:53:34.771865+00:00
## Template: J | Score: 0 - FutureChain - 1 name_lookup_snapshot in async context
## Exploit code
```python
# Template J: FutureChain - test future snapshot chaining with asyncio

import asyncio

async def coro1():
    return "result1"

async def coro2():
    return "result2"

async def coro3():
    return "result3"

async def test_gather():
    results = await asyncio.gather(coro1(), coro2(), coro3())
    print(f"gather results: {results}")
    return results

try:
    result = asyncio.run(test_gather())
    print(f"asyncio.run result: {result}")
except Exception as e:
    print(f"asyncio error: {type(e).__name__}: {e}")

async def test_undefined():
    try:
        val = undefined_in_async
        return val
    except NameError:
        print("NameError in async")
        return None

try:
    result2 = asyncio.run(test_undefined())
    print(f"undefined async result: {result2}")
except Exception as e:
    print(f"undefined async error: {type(e).__name__}: {e}")

async def inner():
    return "inner_done"

async def outer():
    inner_result = await inner()
    print(f"inner result: {inner_result}")
    return "outer_done"

try:
    result3 = asyncio.run(outer())
    print(f"nested async result: {result3}")
except Exception as e:
    print(f"nested async error: {type(e).__name__}: {e}")

async def failing_coro():
    raise ValueError("intentional error")

async def test_exception():
    try:
        await failing_coro()
    except ValueError as e:
        print(f"caught: {e}")
        return "handled"

try:
    result4 = asyncio.run(test_exception())
    print(f"exception test: {result4}")
except Exception as e:
    print(f"exception test error: {type(e).__name__}: {e}")

print("FutureChain tests complete")
```

## Result
Context: Asyncio worked normally, only name_lookup triggered not future snapshots
Score: 0/5 - FutureChain - 1 name_lookup_snapshot in async context
