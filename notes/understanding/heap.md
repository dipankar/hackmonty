# Monty GC Architecture
## Last updated: 2026-06-02
## Confidence: HIGH (from source analysis + Round 1 postmortem)

### What we know
- Monty uses reference counting (like CPython) with a tracing GC for cycle detection
- The tracing GC walks from a "root set" of objects to find all reachable objects
- Objects not reachable from the root set are considered dangling cycles and can be freed
- **Round 1 exploit**: The root set was missing the list object during `list.sort(key=...)`
  - When the key function triggered GC collection, the list being sorted was freed
  - This created a use-after-free, exploited via `unsafe` Rust code in the object model
- **Fix in v0.0.16**: Extended GC root set to cover objects that `unsafe` code depends on
- Monty maintainers admit: "the current GC design doesn't prevent missing roots by construction"

### What we suspect
- Other builtins with callback patterns may have similar root set gaps:
  - `sorted(iterable, key=func)` - creates a new sorted list while calling key
  - `max(iterable, key=func)` / `min(iterable, key=func)` - iterates while calling key
  - `filter(None, iterable)` - if iterable yields while GC runs
  - Custom `__eq__`, `__hash__`, `__lt__` on dict/set operations
  - `list.extend(iterable)` - extending while iterating
  - Dictionary operations with custom `__hash__` during rehashing

### What we don't know
- Whether the GC root set is verified by any automated test suite
- Whether there's a fuzzer specifically targeting GC root set completeness
- Whether nested callbacks (key function calling sorted again) are protected
- Whether async/await suspension points are properly rooted

### Relevant sources
- `crates/monty/src/heap.rs` - GC entry point
- `crates/monty/src/heap_data.rs` - GC data structures
- `crates/monty/src/heap_traits.rs` - GC traversal traits
- `crates/monty/src/sorting.rs` - sort implementation (previously vulnerable)
- Round 1 postmortem: https://pydantic.dev/articles/hack-monty-postmortem
- Patch PR: https://github.com/pydantic/monty/pull/381
