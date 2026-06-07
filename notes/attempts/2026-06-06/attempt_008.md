# Attempt 007 - 2026-06-06T19:38:49.382271+00:00
## Template: J | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template J: Future Snapshot Chaining
# Test async operations that might create future snapshots

import asyncio

print('Test 1: Basic async function')

async def simple_task(n):
    print(f'Task {n} starting')
    await asyncio.sleep(0.001)
    return n * 2

async def main():
    print('Running gather...')
    results = await asyncio.gather(
        simple_task(1),
        simple_task(2),
        simple_task(3)
    )
    print('Results:', results)
    return results

# Run the async code
result = asyncio.run(main())
print('Final result:', result)

print('\nTest 2: Nested futures')

async def outer():
    async def inner():
        return 'inner_value'
    val = await inner()
    return f'outer({val})'

nested = asyncio.run(outer())
print('Nested result:', nested)

print('\nTest 3: Future with exception')

async def failing_task():
    raise ValueError('intentional error')

try:
    asyncio.run(failing_task())
except ValueError as e:
    print('Caught expected error:', e)
```

## Result
Context: AttributeError: module 'asyncio' has no attribute 'sleep'
Score: 0/5 - Nothing - standard error or expected sandbox behavior
