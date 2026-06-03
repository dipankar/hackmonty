# Available Builtins and Standard Library Surface
## Last updated: 2026-06-02
## Confidence: MEDIUM (mixed sources)

### What we know
Monty supports a subset of Python stdlib:

#### Confirmed Available
- `sys` (sandboxed)
- `os` (sandboxed - environ/getenv faked on hackmonty)
- `typing`
- `asyncio`
- `re` (regex)
- `datetime`
- `json`
- `dataclasses` (limited, no full class support)
- `pathlib.Path`
- `print()`, `len()`, `range()`, etc (core builtins)

#### Confirmed Unavailable
- Full class definitions
- Most stdlib modules beyond the list above
- Third-party libraries (pydantic, requests, numpy, etc.)

#### Unknown Status (needs probing)
- `eval()`, `exec()`, `compile()` - may be blocked or available
- `import` of internal modules
- `__import__()` builtin
- `open()` builtin - exists but sandboxed
- `input()` - probably mocked/blocked
- `help()` - may reveal internals
- `dir()` - standard introspection, should work
- `vars()`, `locals()`, `globals()` - standard, should work
- `type()`, `isinstance()`, `issubclass()` - standard
- `getattr()`, `setattr()`, `delattr()`, `hasattr()` - standard
- `id()`, `hash()` - standard
- `memoryview`, `bytearray`, `bytes` - should work
- `__builtins__` module - should be inspectable
- `sys.modules` - may reveal loaded modules
- `os.system()`, `os.popen()`, `subprocess` - almost certainly blocked
- `ctypes` - almost certainly not available

### Attack ideas
- Enumerate `dir(__builtins__)` to see full available surface
- Check `sys.modules.keys()` for any loaded internal modules
- Try importing unexpected modules like `code`, `codeop`, `inspect`
- Test `eval()` with various strings
- Check if `compile()` can produce code objects from strings
- Inspect `type(print)` or `type(len)` to see internal type names
