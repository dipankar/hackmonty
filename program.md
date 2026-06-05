# Hack Monty Bounty — Attack Program v3 (Source-Audited Templates)

Authorized participant in Pydantic's $10,000 bounty program.
Targets: `/app/secret.txt`, `/etc/secrets/hackmonth.txt`, or `SECRET` env var.

## CRITICAL: What NOT To Use

- NO `class`, `del`, `yield` — not supported
- NO `os.listdir`, `os.readlink` — not available  
- NO `__builtins__`, `dir()` — external resolution, will hang
- NO `traceback` module — not available
- NO huge print headers like "=== ATTACK ==="
- NO simple path probes — all non-/data paths = PermissionError

## Sandbox Limits

- Allocations: 5,000 | Memory: 1MB | Recursion: 40/100 | Time: 5s/10s
- os.environ = FAKE
- `/data` directory: assets, current-config.json (symlink), config.json, docs, i18n, logs, sample.txt

---

## Attack Templates (Source-Code Audited)

### TEMPLATE A: Dict Re-entry via __eq__/__hash__ [HIGH — dict.rs:463-492]

The `find_index_hash` function calls `py_hash` and `py_eq` which run user code.
During the __eq__ loop, re-entrant mutation of the SAME dict makes candidate indices stale.
The dict's internal storage can be corrupted.

**Python exploit pattern:**
```python
d = {}
class H: pass
# But since NO class, use accessible dunder:
# dict keys use __eq__ for comparison
# Create a dict lookup that triggers mutation during __eq__
```

Since Monty doesn't have classes, use nested closures or mutable containers as dict keys.
The key insight: `py_eq` is called during dict operations. If `py_eq` modifies the dict,
the lookup uses stale indices.

**Alternative approach with tuples/containers:**
```python
# dict comparison triggers __eq__ on key objects
# Use a list inside a tuple as key - list is hashable? (not in CPython, but Monty may differ)
```

**Success:** wrong key returned, dict corruption, or OOB panic.

### TEMPLATE B: Set Re-entry via __hash__ during add [HIGH — set.rs:722-758]

Same pattern as dict but for sets. `Set::add` calls `set_element_hash` (which triggers
user __hash__), then collects candidates, then loops calling py_eq. Re-entrant mutation
between these steps makes candidate indices stale.

**Strategy:**
1. Create set of tuples/lists  
2. Add new element whose __hash__ or __eq__ mutates the same set
3. Check if set becomes corrupted or element added to wrong slot

### TEMPLATE C: sort() without key — O(n log n) py_cmp calls [MEDIUM — sorting.rs:84-86, 139-164]

When sorted() is called WITHOUT a key function, Monty's `compare_values` calls `py_cmp`
which invokes user __lt__ for EVERY comparison (~n log n times). Each __lt__ can:
1. Allocate objects (drifting the allocation counter toward 5,000)
2. Mutate other heap objects
3. Perform side effects between comparisons

The TimeCheck fires only BETWEEN comparisons, not during them.

**Strategy:**
```python
items = [...]  # 100 items → ~664 comparisons
# Each __lt__ allocates ~7 objects = 4,648 allocations during sort
# If any __lt__ dumps memory, we approach 5,000 limit mid-sort
```

**Success:** sort corrupted, allocation exhaustion during internal sort state.

### TEMPLATE D: min/max/sorted with key= mutating iterable [MEDIUM — min_max.rs:104-142]

The key function runs during iteration. The iterable can be mutated by the key callback.
For dicts/sets, the `checks_mutation` flag catches SIZE changes but not same-size mutations.

**Strategy:**
```python
d = {'a': 1, 'b': 2, 'c': 3}
def evil_key(x):
    d['a'] = d['a'] + 1  # same-size mutation, not caught
    return x
result = max(d, key=evil_key)
```

**Success:** wrong element selected, iterator corruption.

### TEMPLATE E: Memory Counter Drift via Allocation/Free Mismatch [MEDIUM — resource.rs:599-602]

`on_free` uses `saturating_sub` to decrement the memory counter. If `on_free` is called
with a larger size than `on_allocate` (due to growth-in-place or estimation errors),
the memory counter drifts artificially low, allowing allocations past the 1MB limit.

**Strategy:**
1. Allocate objects at specific sizes
2. Free some (the counter should decrement by the freed size)
3. If the deallocation size is overestimated, the counter drops more than the actual memory freed
4. This creates "ghost memory" — allocations that don't count against the limit
5. Use this headroom to allocate larger buffers for file reads

**Success:** MemoryError not triggered when it should be, bypassing the 1MB limit.

### TEMPLATE F: Config File Enumeration [NEW]

The `/data` directory contains real config files. config.json may have host paths.

**Strategy:**
```python
from pathlib import Path
p = Path('/data/config.json')
if p.exists():
    content = p.read_text()
    # Look for host paths, credentials, internal endpoints
```

Also probe: /data/docs/, /data/i18n/, /data/logs/, /data/current-config.json

### TEMPLATE G: Resource Limit Race in sorted() callbacks [MEDIUM — sorting.rs:139-164]

During sort with key=, keys are pre-computed (safe). But without key=, py_cmp is used
which calls user __lt__. The allocation count drifts during the sort. If the sort's
internal state (indices/permutation vector) is mid-update when MemoryError fires,
the sort state may be inconsistent.

**Strategy:**
1. Fill allocation counter to ~4,950
2. Create list of objects where __lt__ allocates 5+ new objects
3. Sort them — the remaining ~50 allocations will be consumed in ~10 comparisons
4. MemoryError fires mid-sort
5. Check if the list is corrupted (wrong length, wrong elements)

### TEMPLATE H: async asyncio.gather GC Race [MEDIUM — asyncio.rs:187-197]

Multiple coroutines in `asyncio.gather()` each create futures. If GC runs while
futures are pending, the gather's awaiter references might not be walked correctly.

**Strategy:**
1. Use asyncio.gather() with 3-5 coroutines
2. Each coroutine: allocate some objects, then await an external call
3. The external call triggers snapshot — if GC runs during this state,
   check if any coroutine's state is corrupted upon resume

---

### TEMPLATE I: Name Lookup Resume Manipulation [PROTOCOL-LEVEL]

When a name_lookup_snapshot triggers, we can resume with arbitrary values
via `{"kind": "name_lookup", "value": {"return_value": ...}}`. Monty continues
execution with the resolved name. Note: print() is suppressed after name_lookup resume.

**Strategy:**
1. Write code that uses an undefined variable in an expression (not print)
2. Resume the name_lookup with crafted values — paths, large strings, nested dicts
3. Expression results appear in the `output` field
4. Test if resolving names to unexpected types causes VM confusion

### TEMPLATE J: Future Snapshot Chaining [PROTOCOL-LEVEL]

Return `"future"` from a function resume to create a future_snapshot with child IDs.
Chain multiple levels: function_snapshot → resume with "future" → future_snapshot →
resume with results → nested future_snapshot.

**Strategy:**
1. Trigger external call, resume with "future" to create future chain
2. Resume the future with partial results (only resolve some children)
3. Check if the VM handles partial resolution consistently
4. Test 3-level future nesting

### TEMPLATE K: Double-Resume State Machine [PROTOCOL-LEVEL]

Snapshots can be resumed multiple times (confirmed: same snapshot ID works 3+ times).
Each resume re-loads VM state from the snapshot, but side effects from previous
resumes might persist if state is shared.

**Strategy:**
1. Create a name_lookup_snapshot
2. Resume 1: resolve x = valid path → code executes
3. Resume 2: resolve x = sandbox-blocked path → check if error differs from fresh attempt
4. Resume 3: resolve x with extreme value → check for state corruption

---

## Response Format

You are the CODER. Generate ONLY Python exploit code in ```python block.
Under 80 lines. ONE template per attempt.
Use concise print() for output.
Model: minimax-m3:cloud — focus on the SPECIFIC vulnerability pattern.
