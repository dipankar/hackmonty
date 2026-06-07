# Attempt 100 - 2026-06-06T22:42:28.461294+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template H: async asyncio.gather GC Race
# Multiple coroutines in gather - try to trigger GC during pending state

import asyncio

async def worker(n):
    # Allocate some objects
    data = [i for i in range(50)]
    # Try to await something external
    await asyncio.sleep(0)
    return n * 2

async def main():
    # Create multiple coroutines
    tasks = [worker(i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    print("Results:", results)

try:
    asyncio.run(main())
except Exception as e:
    print("Error:", type(e).__name__, e)

# Try with more workers
async def stress_worker(n):
    data = [[j for j in range(20)] for _ in range(10)]
    await asyncio.sleep(0)
    return sum(data[n])

async def stress_main():
    tasks = [stress_worker(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    print("Stress results:", results)

try:
    asyncio.run(stress_main())
except Exception as e:
    print("Stress error:", type(e).__name__, e)
```

## Result
Context: Async code works but no snapshots triggered - asyncio.sleep not available
Score: 0/5 - Nothing - standard error or expected sandbox behavior
