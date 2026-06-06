# Attempt 204 - 2026-06-05T22:34:46.315933+00:00
## Template: C | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
1. Use asyncio.gather() with 3-5 coroutines
2. Each coroutine allocates objects to create GC pressure
3. One coroutine awaits an external call (like open/read or os.getenv)
4. When the external call triggers, GC may run while futures are pending
5. Check if any coroutine state is corrupted upon resume

## Exploit code
```python
if trigger_external:
        from pathlib import Path
        p = Path('/data/sample.txt')
        if p.exists():
            _ = p.read_text()
```

## Result
Category: standard_error
Context: name_lookup(trigger_external); NameError: name 'trigger_external' is not defined
Details: NameError: name 'trigger_external' is not defined
```
Success: False
Elapsed: 1233ms
Resumes: 1
Snapshots: 1
Error: NameError: name 'trigger_external' is not defined
  [0] kind=name_lookup_snapshot
Print: 
```

## Analysis
- NameError: name 'trigger_external' is not defined
- Verdict: Not exploitable
