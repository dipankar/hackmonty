# Attempt 090 - 2026-06-06T22:28:09.804834+00:00
## Template: J | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template J: FutureChain - Async without sleep
# Try basic async/await to trigger future snapshots

import asyncio

async def simple_coro(val):
    return val * 2

async def gather_test():
    # gather should create multiple futures
    results = await asyncio.gather(
        simple_coro(1),
        simple_coro(2),
        simple_coro(3)
    )
    return results

try:
    result = asyncio.run(gather_test())
    print(f"Gather result: {result}")
except Exception as e:
    print(f"Error: {e}")

# Try wait instead of sleep
async def with_wait():
    task = asyncio.create_task(simple_coro(5))
    result = await task
    return result

try:
    wait_result = asyncio.run(with_wait())
    print(f"Wait result: {wait_result}")
except Exception as e:
    print(f"Wait error: {e}")

# Try as_completed
async def with_as_completed():
    tasks = [simple_coro(i) for i in range(3)]
    results = []
    for coro in asyncio.as_completed(tasks):
        results.append(await coro)
    return results

try:
    ac_result = asyncio.run(with_as_completed())
    print(f"As completed: {ac_result}")
except Exception as e:
    print(f"As completed error: {e}")
```

## Result
Context: Async gather works but no future snapshots - create_task/as_completed not available
Score: 0/5 - Nothing - standard error or expected sandbox behavior
