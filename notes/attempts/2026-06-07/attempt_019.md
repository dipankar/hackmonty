# Attempt 150 - 2026-06-07T18:53:27.468352+00:00
## Template: G | Score: 0 - Nothing
## Exploit code
```python
print("=== AllocRace Exploit ===")
import sys

# Phase 1: Prefill allocation counter to ~4980
pool = []
try:
    for i in range(4980):
        pool.append([i])
    before = len(pool)
    print(f"Prefilled {before} items")
    try:
        result = sorted(range(30), key=lambda x: [x])
        print(f"Sort completed: {len(result)} items")
    except MemoryError as e:
        print(f"MemoryError caught: {e}")
    except Exception as e:
        print(f"Other error: {type(e).__name__}: {e}")
except MemoryError as e:
    print(f"MemoryError in prefill: {e}")
except Exception as e:
    print(f"Setup error: {type(e).__name__}: {e}")
print("=== Done ===")
```

## Result
Context: Template G AllocRace - MemoryError uncatchable, killed execution. No traceback leak.
Score: 0/5 - Nothing
