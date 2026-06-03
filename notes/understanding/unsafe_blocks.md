# Unsafe Rust Blocks and Memory Safety
## Last updated: 2026-06-02
## Confidence: MEDIUM (from postmortem analysis)

### What we know
- Monty uses `unsafe` Rust for internal object model to allow interior mutability
  without RefCell/Mutex overhead
- The `unsafe` blocks are in the object/heap layer, specifically for:
  - Getting mutable references to objects in the heap graph
  - The internal "Sharing XOR Mutability" enforcement
- These blocks were audited after Round 1
- Miri (Rust's undefined behavior detector) is used in testing
- The postmortem states: "we have confidence that there are no further memory safety issues"

### Safety invariants that must hold
- Objects don't change type once created
- Monty is single-threaded
- GC root set must cover all objects that `unsafe` code depends on
- All `unsafe` blocks have documented safety invariants in the source

### Potential remaining weaknesses
- If ANY of the documented invariants can be broken, the `unsafe` code becomes exploitable
- Type confusion: if GC frees an object and another type reuses the memory
- Missing GC roots: the maintainers admit the design "doesn't prevent missing roots by construction"
- We need to find call paths where:
  1. An `unsafe` block depends on an object being alive
  2. The object is NOT in the GC root set during that call
  3. Something triggers GC collection
  4. The freed memory is reused by a different object type

### Key source files to study
- `crates/monty/src/heap.rs` - GC root set construction
- `crates/monty/src/heap_data.rs` - object graph storage
- `crates/monty/src/object.rs` - Python object representation
- `crates/monty/src/heap_traits.rs` - `unsafe` traversal traits
