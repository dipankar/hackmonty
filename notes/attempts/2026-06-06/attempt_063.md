# Attempt 062 - 2026-06-06T22:00:30.535149+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template H: AsyncGC - try basic asyncio with GC race
import asyncio

print(f"asyncio attrs: {[x for x in dir(asyncio) if not x.startswith('_')][:20]}")

async def simple():
    return "done"

try:
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(simple())
    print(f"Result: {result}")
    loop.close()
except Exception as e:
    print(f"Error: {e}")

async def worker(n):
    return n

async def main():
    r = await asyncio.gather(worker(1), worker(2))
    print(f"Gather: {r}")

try:
    asyncio.run(main())
except Exception as e:
    print(f"Run error: {e}")
```

## Result
Context: function_snapshot triggered on dir() call, no GC race exploited
Score: 0/5 - Nothing - standard error or expected sandbox behavior
