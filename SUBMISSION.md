# Hack Monty 2 — Submission

## Who
Dipankar (GitHub: dipankar)
Request secret: cipher-zenith-quantum-drift-hm2026

## What I found

A latent unsafe Rust bug in monty's heap layer. It's not a sandbox escape — I couldn't read the secret. But it's a real provenance violation in unsafe code that the Miri author would flag immediately.

**The bug**: `heap_read_boxed()` at `crates/monty/src/heap.rs:567-579`.

```rust
fn heap_read_boxed<'a, T>(boxed: &Box<T>, readers: NonNull<Cell<usize>>) -> HeapRead<'a, T> {
    HeapRead {
        value: unsafe { NonNull::new_unchecked(ptr::from_ref(boxed.as_ref()).cast_mut()) },
        readers,
        borrow: PhantomData,
    }
}
```

The problem is on line 576. `ptr::from_ref(boxed.as_ref()).cast_mut()` takes a `&T` reference (which has SharedReadOnly provenance under Stacked Borrows), gets a raw pointer from it (still SharedReadOnly), then casts to `*mut T`. The provenance doesn't change — you now have a `*mut T` that you're not allowed to write through. If `HeapRead::get_mut()` ever dereferences it, that's UB.

Right now this is safe because RePattern (the only type using `heap_read_boxed`) is never mutated. No code path calls `get_mut()` on a RePattern handle. So it's a ticking time bomb rather than a live vulnerability.

Compare with `heap_read()` at line 553 — that one does it right: derives from the `base` pointer that came from `UnsafeCell::get` (SharedReadWrite provenance). `heap_read_boxed` can't use that approach because Box-allocated data is in a separate allocation, but it could derive from the Box pointer itself.

**The fix**:
```rust
fn heap_read_boxed<'a, T>(boxed: &Box<T>, readers: NonNull<Cell<usize>>) -> HeapRead<'a, T> {
    HeapRead {
        value: unsafe { NonNull::new_unchecked(Box::as_ptr(boxed) as *mut T) },
        readers,
        borrow: PhantomData,
    }
}
```

`Box::as_ptr` returns a pointer from the Box's allocation (Unique provenance), so `as *mut T` preserves write capability. Though honestly `Box::as_ptr` takes `&self` too, so the full provenance chain is still fuzzy. A really clean fix might store the original pointer at construction time.

## Also worth noting

The `dec_ref` function at `heap.rs:1083` has a documented Miri failure (test `dec_ref_must_not_invalidate_live_heap_read` at line 1928). It accesses `ptr.data(reader).is_gc_tracked()` which goes through `UnsafeCell`, and under Stacked Borrows the retag can invalidate existing `HeapRead` raw pointers. The test shows it currently passes by using `UnsafeCell::get` instead of `get_mut`, but the free path at line 1110 still uses `get_mut` — correctly guarded by the `readers == 0` check at line 1095. If that assertion is ever wrong, it's a use-after-free. Might be worth putting this in CI with Miri.

## What I actually did

I built an LLM-driven autonomous probing loop based on the autoresearch pattern, ran 200+ exploit attempts against hackmonty.com, did a full source audit of the monty codebase (all 43 unsafe blocks, the GC algorithm, the filesystem sandbox, the snapshot protocol), and tested every class of attack I could think of. The sandbox held up. This provenance bug was the most interesting thing I found in the Rust source.

Full code, attempt logs, and detailed report at: https://github.com/dipankar/hackmonty

## Secret
Not found. Honestly, the Round 2 hardening is solid.
