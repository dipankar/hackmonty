# Monty Language Limitations Found via Probing
## Last updated: 2026-06-03 (from autonomous probing)
## Confidence: HIGH (confirmed by direct testing)

### Confirmed Unsupported
- **`class` definitions**: `NotImplementedError: The monty syntax parser does not yet support class definitions`
- **`del` statement**: `NotImplementedError: The monty syntax parser does not yet support the 'del' statement`
- **`yield` expressions**: `NotImplementedError: The monty syntax parser does not yet support yield expressions`

### Confirmed Resource Limits
- **Max allocations**: 5,000 (confirmed via `MemoryError: allocation limit exceeded: 5001 > 5000`)
- **Max memory**: ~1,048,576 bytes (1MB) (confirmed via `MemoryError: memory limit exceeded: 1048582 bytes > 1048576 bytes`)
- **Max recursion depth**: 40 (default), 100 (max per API spec)
- **Max duration**: 5.0s (default), 10.0s (max per API spec)

### Confirmed Behavior
- **`__builtins__`**: Triggers `name_lookup_snapshot` (external name resolution)
  - Not available in sandbox by default
  - Agent should use `type()`, `getattr()`, `hasattr()` for introspection instead
- **`os.listdir`**: NOT available (`AttributeError: module 'os' has no attribute 'listdir'`)
- **`os.environ`**: Returns fake dict: `{'user': 'Samuel', 'server': 'Hack Monty', 'challenge': 'Escape the sandbox!'}`
- **Path traversal**: Outside `/data` always returns `PermissionError` (file existence oracle intentionally blocked)
- **`dir()`**: Triggers a function_snapshot (the `dir` builtin is an external function call)
- **Walrus operator**: Works in list comprehensions (tested successfully)
- **Closures**: Work for basic nesting (multi-level closures tested OK)
- **Path normalization**: `Path` seems to normalize `..` correctly, blocks traversal

### Notes for Agent
- NEVER use `class`, `del`, or `yield` in exploit code - they will fail
- NEVER use `os.listdir` - it doesn't exist in Monty
- Use introspection via `type()`, `getattr()`, `hasattr()` instead of `dir()` when possible
- Path probes outside `/data` are useful to confirm sandbox behavior but don't leak file existence
- Allocation limit (5000) can be used to force crashes at interesting points
- Memory limit (1MB) can be used to test resource exhaustion
