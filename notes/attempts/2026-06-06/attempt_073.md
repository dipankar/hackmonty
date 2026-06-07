# Attempt 072 - 2026-06-06T22:06:19.819899+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template H: async asyncio.gather GC Race
# Strategy: Multiple coroutines with allocations, trigger GC during pending futures

import asyncio
import gc

results = []

async def worker(n):
    # Allocate objects that might be GC'd
    data = [i * n for i in range(50)]
    results.append(f"worker_{n}")
    return data

async def main():
    # Create multiple pending futures
    tasks = [
        asyncio.create_task(worker(1)),
        asyncio.create_task(worker(2)),
        asyncio.create_task(worker(3)),
        asyncio.create_task(worker(4)),
        asyncio.create_task(worker(5)),
    ]
    
    # Try GC while tasks are pending
    gc.collect()
    
    # Gather results
    all_results = await asyncio.gather(*tasks)
    return all_results

try:
    result = asyncio.run(main())
    print(f"Gather results: {len(result)} tasks completed")
    print(f"Results list: {results}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

# Try with undefined var for name_lookup
try:
    secret = async_secret
    print(f"Secret: {secret}")
except:
    pass
```

## Result
Context: gc module not available in sandbox
Score: 0/5 - Nothing - standard error or expected sandbox behavior
