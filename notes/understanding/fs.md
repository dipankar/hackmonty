# Monty Filesystem Sandbox
## Last updated: 2026-06-02
## Confidence: MEDIUM (from docs + GitHub issues)

### What we know
- Monty has a virtual filesystem layer that mediates all I/O
- `/data` is a real read-only host mount on hackmonty.com
- All filesystem access goes through `crates/monty/src/fs/`:
  - `path_security.rs` - path validation and boundary checking
  - `common.rs` - actual filesystem operations
- Path validation uses canonicalization + boundary checks
- Write operations have a TOCTOU race (#455): validation and write are not atomic
  - Specifically in `resolve_creation()`: validates → returns path → caller writes
  - Exploit requires external actor creating symlink between validation and write
  - Monty does NOT expose `os.symlink()` so this needs concurrent host access
- Mount identity can be corrupted (#380): shared mounts swapped after run()

### What we suspect
- Path traversal via `..` might be blocked, but edge cases could exist:
  - `Path('/data/../../../etc/secrets/hackmonth.txt')`
  - Unicode normalization tricks
  - Null byte injection in paths
  - Double encoding
- The read-only mount at `/data` might have an imperfect boundary check
- `os.listdir()` on root may reveal unexpected directories
- `open()` builtin might have different validation than `Path.read_text()`
- `/proc/self/` on Linux might leak host info if accessible

### What we don't know
- Whether non-`/data` paths are purely virtual or backed by real directories
- What the full virtual filesystem layout looks like
- Whether `/tmp` or `/dev` exist in the virtual filesystem
- The exact `os` module builtins available (os.listdir, os.scandir, os.stat, os.walk)

### Relevant sources
- `crates/monty/src/fs/path_security.rs`
- `crates/monty/src/fs/common.rs`
- Issue #455: TOCTOU race in write path
- Issue #380: Shared mount identity corruption
- Hack Monty rules mention `/data` as real read-only mount
- `limitations/filesystem.md`, `limitations/os.md`, `limitations/open.md`
