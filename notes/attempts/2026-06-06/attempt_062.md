# Attempt 061 - 2026-06-06T22:00:14.684305+00:00
## Template: J | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template J: FutureChain - trigger future snapshots via asyncio
import asyncio

async def worker(n):
    await asyncio.sleep(0.001)
    return n * 2

async def main():
    results = await asyncio.gather(worker(1), worker(2), worker(3))
    print(f"Results: {results}")

try:
    asyncio.run(main())
except Exception as e:
    print(f"Error: {e}")

async def main2():
    tasks = [asyncio.create_task(worker(i)) for i in range(5)]
    done, pending = await asyncio.wait(tasks)
    results = [t.result() for t in done]
    print(f"Wait results: {results}")

try:
    asyncio.run(main2())
except Exception as e:
    print(f"Error2: {e}")
```

## Result
Context: asyncio module has limited functionality, no future snapshots created
Score: 0/5 - Nothing - standard error or expected sandbox behavior
