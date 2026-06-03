# Attempt 003 — 2026-06-03T21:26:35.953180+00:00
## Template: E | Score: 0
## Strategy
Create objects of varying sizes, free them in a pattern that may cause the memory counter to decrement more than actual freed memory, then use the artificial headroom to allocate larger buffers for reading /data files. Check if we can read more content than the 1MB limit should allow by comparing expected vs actual allocation behavior. Output any file content that becomes accessible through this memory counter drift.

## Exploit code
```python
from pathlib import Path

alloc_log = []
free_log = []

def alloc_pattern(size_mult):
    """Create objects in nested scopes to trigger free counting"""
    outer = {'pad': 'O' * (size_mult * 50)}
    alloc_log.append(size_mult)
    
    def inner():
        inner_obj = {'pad': 'I' * (size_mult * 30)}
        alloc_log.append(size_mult)
        return inner_obj
    
    result = inner()
    # inner_obj freed when inner() returns, outer freed when alloc_pattern returns
    return result

def drift_cycle(iteration):
    """Rapid alloc/free cycles may cause counter drift"""
    temps = []
    for i in range(5):
        obj = alloc_pattern(20 + i * 5)
        temps.append(obj)
    # All temps freed when function returns
    return len(temps)

# Phase 1: Create drift through repeated alloc/free patterns
for phase in range(8):
    drift_cycle(phase)

# Phase 2: Attempt to exploit potential memory headroom
targets = [
    '/data/config.json',
    '/data/current-config.json',
    '/data/sample.txt',
    '/data/docs/README.md',
    '/data/i18n/en.json',
    '/data/logs/app.log'
]

print("=== Memory Drift Attack ===")
for t in targets:
    try:
        p = Path(t)
        if p.exists():
            content = p.read_text()
            print(f"OK {t}: {content[:150]}")
    except Exception as e:
        print(f"ERR {t}: {str(e)[:60]}")

# Phase 3: Test if we can allocate beyond normal limits
try:
    # If counter drifted, this might succeed when it shouldn't
    large_buf = 'L' * 100000
    print(f"LARGE_ALLOC: {len(large_buf)} bytes succeeded")
    
    # Try reading with large buffer context
    for t in targets[:2]:
        try:
            p = Path(t)
            content = p.read_text()
            if len(content) > 100:
                print(f"FULL_READ {t}: {content}")
        except:
            pass
except MemoryError as e:
    print(f"BLOCKED: {str(e)[:70]}")
```

## Result
Category: no_findings
Details: Completed with no notable findings
```
Success: True
Elapsed: 819ms
Resumes: 0
Snapshots: 0
Print: === Memory Drift Attack ===
OK /data/config.json: {
  "app_name": "hackmonty",
  "version": "0.1.0",
  "debug": false,
  "max_workers": 4
}

OK /data/current-config.json: {
  "app_name": "hackmonty",
  "version": "0.1.0",
  "debug": false,
  "max_workers": 4
}

OK /data/sample.txt: Hello from the Monty sandbox!
This file is mounted read-only at /data/sample.txt.
You can read it with Path('/data/sample.txt').read_text()

OK /data/docs/README.md: # /data

Files mounted read-only inside the Monty s
```

## Analysis
- Completed with no findings
- **Verdict**: Try different template
