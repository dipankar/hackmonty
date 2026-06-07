# Attempt 035 - 2026-06-06T21:34:14.473373+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template H: async asyncio.gather GC Race
# Multiple coroutines in gather, each allocates then awaits

import asyncio

async def worker(n):
    data = [i for i in range(100)]
    return sum(data)

async def main():
    results = await asyncio.gather(
        worker(1), worker(2), worker(3), worker(4), worker(5)
    )
    print("Results:", results)

try:
    asyncio.run(main())
except Exception as e:
    print("Error:", type(e).__name__, str(e)[:80])

# Try with external call in coroutine
async def worker_with_external(n):
    data = [i for i in range(50)]
    x = undefined_async_var
    return len(data)

async def main2():
    try:
        results = await asyncio.gather(
            worker_with_external(1),
            worker_with_external(2),
            worker_with_external(3)
        )
        print("Results2:", results)
    except NameError as e:
        print("NameError in async:", str(e)[:60])

try:
    asyncio.run(main2())
except Exception as e:
    print("Outer error:", type(e).__name__, str(e)[:60])
```

## Result
Context: AsyncGC - 1 name_lookup_snapshot in async context
Score: 0/5 - Nothing - standard error or expected sandbox behavior
