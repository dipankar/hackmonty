# Attempt 080 - 2026-06-06T22:11:50.646884+00:00
## Template: J | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template J: FutureChain - exploit future snapshot chaining
# Create async coroutines that return futures

print("=== FutureChain Test ===")

import asyncio

async def coro1():
    print("coro1 running")
    return "result1"

async def coro2():
    print("coro2 running")
    return "result2"

async def coro3():
    print("coro3 running")
    return "result3"

async def main():
    print("Starting gather...")
    results = await asyncio.gather(coro1(), coro2(), coro3())
    print(f"Results: {results}")
    return results

try:
    result = asyncio.run(main())
    print(f"Final result: {result}")
except Exception as e:
    print(f"Exception: {type(e).__name__}: {e}")

# Try with nested futures
async def nested():
    async def inner():
        return "inner_result"
    return await inner()

try:
    result = asyncio.run(nested())
    print(f"Nested result: {result}")
except Exception as e:
    print(f"Exception: {type(e).__name__}: {e}")

print("Done")
```

## Result
Context: Asyncio worked normally, no future snapshots created
Score: 0/5 - Nothing - standard error or expected sandbox behavior
