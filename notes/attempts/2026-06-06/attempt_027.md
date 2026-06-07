# Attempt 026 - 2026-06-06T21:08:58.149423+00:00
## Template: H | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template H: async asyncio.gather GC race

import asyncio
from pathlib import Path

async def worker(n):
    # Allocate some objects before await
    data = [i * n for i in range(50)]
    
    # External call (file read) - may trigger snapshot
    p = Path('/data/sample.txt')
    if p.exists():
        content = p.read_text()
        return f'worker{n}: {len(content)} bytes, data_sum={sum(data)}'
    return f'worker{n}: file not found'

async def main():
    print('Starting asyncio.gather with 5 coroutines...')
    
    # Create tasks
    tasks = [worker(i) for i in range(5)]
    
    # Gather all - each does I/O which may snapshot
    try:
        results = await asyncio.gather(*tasks)
        print(f'Results: {results}')
    except Exception as e:
        print(f'Gather error: {e}')
    
    # Try with same coroutine passed twice (issue #409)
    print('\nTesting duplicate coroutine...')
    task = worker(99)
    try:
        dup_results = await asyncio.gather(task, task)
        print(f'Dup results: {dup_results}')
    except Exception as e:
        print(f'Dup error: {e}')

# Run the async code
asyncio.run(main())

# Also test basic async
async def simple():
    return 'simple result'

result = asyncio.run(simple())
print(f'Simple async: {result}')
```

## Result
Context: no detail
Score: 0/5 - Nothing - standard error or expected sandbox behavior
