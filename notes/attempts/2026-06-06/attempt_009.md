# Attempt 008 - 2026-06-06T19:39:13.773709+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template H: async asyncio.gather GC Race
# Test if GC during pending futures causes corruption

import asyncio

print('Test 1: Simple gather without sleep')

async def immediate_task(n):
    return n * 2

async def main():
    print('Gathering tasks...')
    results = await asyncio.gather(
        immediate_task(1),
        immediate_task(2),
        immediate_task(3),
        immediate_task(4),
        immediate_task(5)
    )
    return results

result = asyncio.run(main())
print('Results:', result)

print('\nTest 2: Many tasks to stress GC')

async def many_tasks():
    tasks = [immediate_task(i) for i in range(50)]
    results = await asyncio.gather(*tasks)
    return results[:10], len(results)

result, count = asyncio.run(many_tasks())
print('First 10:', result)
print('Total count:', count)

print('\nTest 3: Gather with exception')

async def failing():
    raise RuntimeError('fail')

async def success():
    return 'ok'

try:
    asyncio.run(asyncio.gather(failing(), success()))
except RuntimeError as e:
    print('Caught:', e)

print('\nTest 4: Nested gather')

async def outer_gather():
    inner = await asyncio.gather(
        asyncio.gather(immediate_task(1), immediate_task(2)),
        asyncio.gather(immediate_task(3), immediate_task(4))
    )
    return inner

nested = asyncio.run(outer_gather())
print('Nested result:', nested)
```

## Result
Context: no detail
Score: 0/5 - Nothing - standard error or expected sandbox behavior
