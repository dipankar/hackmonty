# Attempt 119 - 2026-06-06T23:03:28.567987+00:00
## Template: H | Score: 0 - Nothing
## Exploit code
```python
# Template H: AsyncGC
import asyncio
async def worker(n):
    data = [list(range(50)) for _ in range(10)]
    return n * 2
async def main():
    results = await asyncio.gather(*[worker(i) for i in range(20)])
    print(f"Got {len(results)} results")
asyncio.run(main())
```

## Result
Context: Asyncio.gather completed successfully with all results
Score: 0/5 - Nothing
