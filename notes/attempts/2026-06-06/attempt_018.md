# Attempt 017 - 2026-06-06T20:57:41.181932+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template H: async asyncio.gather GC Race
# Multiple coroutines in gather, each allocates objects

import asyncio

async def worker(n):
    # Allocate some objects
    data = [i for i in range(100)]
    # Try to await something
    return len(data) + n

async def main():
    # Run multiple coroutines
    results = await asyncio.gather(
        worker(1),
        worker(2),
        worker(3),
        worker(4),
        worker(5)
    )
    print("Results:", results)

# Try to run it
try:
    asyncio.run(main())
except Exception as e:
    print("Error:", type(e).__name__, e)
```

## Result
Context: no detail
Score: 0/5 - Nothing - standard error or expected sandbox behavior
