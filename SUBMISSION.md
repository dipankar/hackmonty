# Hack Monty 2 — Vulnerability Submission

## Submitter
- Name: Dipankar
- GitHub: dipankar
- Request secret (plaintext): cipher-zenith-quantum-drift-hm2026

## Category
Partial Bounty — Vulnerability in Pydantic Monty that allows access to or control of the host
(Unsafe Rust provenance violation — latent, not currently exploitable from sandboxed Python)

## Finding: `heap_read_boxed` Unsafe Provenance Mismatch

**Location**: `crates/monty/src/heap.rs`, lines 567-579

**Function**: `heap_read_boxed()`

```rust
fn heap_read_boxed<'a, T>(boxed: &Box<T>, readers: NonNull<Cell<usize>>) -> HeapRead<'a, T> {
    HeapRead {
        value: unsafe { NonNull::new_unchecked(ptr::from_ref(boxed.as_ref()).cast_mut()) },
        readers,
        borrow: PhantomData,
    }
}
```

**The bug**: The `NonNull` pointer is derived from `ptr::from_ref(boxed.as_ref()).cast_mut()`. The call chain is:
1. `boxed` — `&Box<T>` (shared reference to the Box)
2. `boxed.as_ref()` — produces `&T` with **SharedReadOnly** provenance under Stacked Borrows / Tree Borrows
3. `ptr::from_ref(...)` — `*const T` inheriting SharedReadOnly
4. `.cast_mut()` — `*mut T` but provenance is still SharedReadOnly
5. If `HeapRead::get_mut()` ever dereferences this as `&mut T`, it creates a mutable reference from SharedReadOnly provenance — **undefined behavior**

**Current status**: This bug is latent. RePattern (the only type using this code path) is effectively immutable — no code calls `get_mut()` on a RePattern handle. But if any future code adds mutation through this path, UB would be triggered.

**Contrast with the correct pattern**: The sibling function `heap_read()` (line 553) correctly derives the pointer from `base` (the `*mut HeapData` from `UnsafeCell::get`, which has SharedReadWrite provenance). The `heap_read_boxed` function can't use this approach because Box-allocated data lives in a separate allocation from HeapData.

**Fix suggestion**: Derive the pointer from the Box's original allocation rather than from `&T`:

```rust
fn heap_read_boxed<'a, T>(boxed: &Box<T>, readers: NonNull<Cell<usize>>) -> HeapRead<'a, T> {
    HeapRead {
        value: unsafe { NonNull::new_unchecked(Box::as_ptr(boxed) as *mut T) },
        readers,
        borrow: PhantomData,
    }
}
```

`Box::as_ptr` returns a pointer derived from the Box's original allocation (Unique provenance), and `.cast_mut()` preserves that provenance. However, since `Box::as_ptr` takes `&self`, the full provenance chain through the reference is still a concern. A more robust fix would store the original pointer at construction time or use `ptr::addr_of!` to avoid going through the reference.

## Additional Finding: `dec_ref` Stacked Borrows Violation

**Location**: `heap.rs`, line 1083

In `dec_ref`, the code accesses `ptr.data(reader).is_gc_tracked()` which internally calls `entry.data.0.get()` — an `UnsafeCell::get_mut()` retag. In earlier versions, this created a `&mut HeapData` alias while live `HeapRead` handles held `SharedReadWrite` pointers, violating Stacked Borrows. 

The test at line 1928 (`dec_ref_must_not_invalidate_live_heap_read`) documents this prior aliasing violation. The current code appears to use `ptr.data(reader)` which returns `&HeapData` (shared) via `UnsafeCell::get`, preserving SharedReadWrite permission. However, on the free path at line 1110, `value.data.0.get_mut()` still creates `&mut HeapData` — correctly guarded by the `readers == 0` assertion at line 1095.

This should be monitored with Miri in CI. A regression would turn this into an active use-after-free.

## Reproduction Evidence

We conducted:
- Exhaustive unsafe audit of all 43 unsafe blocks across 100+ Rust source files
- Full codebase review of heap.rs, heap_data.rs, heap_traits.rs, sorting.rs, and all builtins
- 200+ Python-level exploit attempts against the live hackmonty.com honeypot
- Timing side-channel analysis, GC edge case analysis, snapshot protocol fuzzing

Full report and tooling: https://github.com/dipankar/hackmonty

## Secret
Not found. This is a source-code vulnerability, not a sandbox escape.

The honepot remains unbroken by our methods — a testament to the Round 2 hardening.
