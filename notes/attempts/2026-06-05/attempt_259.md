# Attempt 258 - 2026-06-05T22:48:59.623380+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
1. Create a coroutine that allocates objects
2. Use asyncio.gather to run multiple coroutines
3. Each coroutine awaits something (asyncio.sleep) 
4. During the await, GC might run and miss roots
5. Check if any state is corrupted

## Exploit code
```python
result = sort_exhaust_attack()
print(f"ALLOCATIONS: {alloc_count[0]}")
print(f"STATUS: {result}")
print(f"POOL_SIZE: {len(pressure_pool)}")
```

## Result
Category: standard_error
Context: func_snap(sort_exhaust_attack); name_lookup(alloc_count); NameError: name 'alloc_count' is not defined
Details: NameError: name 'alloc_count' is not defined
```
Success: False
Elapsed: 920ms
Resumes: 2
Snapshots: 2
Error: NameError: name 'alloc_count' is not defined
  [0] kind=function_snapshot
  [1] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'alloc_count' is not defined
- Verdict: Not exploitable
