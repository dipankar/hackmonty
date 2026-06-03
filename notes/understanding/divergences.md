# CPython Divergence Points (Type Confusion Vectors)
## Last updated: 2026-06-02
## Confidence: MEDIUM (from GitHub issues + limitations docs)

### What we know
Monty is NOT a full CPython implementation. Known divergences:

#### Scope/Namespace Bugs
- #423: CPython inconsistencies with global statements
- #369: Walrus operator in default args causes different SyntaxError behavior
- #477: Multiply-nested closures don't propagate captures correctly
  - Inner nested function may see wrong variables from outer scope
  - Could allow accessing "private" frame variables

#### Syntax/Semantic Bugs
- #408: Subscript targets fail in unpacking assignment
- #369: SyntaxError reporting differs from CPython for nonlocals with walrus

#### Missing Features (not yet bugs, but design limitations)
- No class definitions (yet) - but `dataclasses` and `namedtuple` have limited support
- No `match` statements (yet)
- Limited stdlib: only sys, os, typing, asyncio, re, datetime, json, dataclasses
- No third-party library support whatsoever

#### Monty-Specific Behavior
- `os.environ` and `os.getenv` are handled internally with fake values on hackmonty.com
- `datetime.now` and `date.today` are handled internally
- Network access, filesystem writes go through external function calls
- The snapshot protocol itself is a divergence - execution pauses and resumes

### What we suspect
- The scope bugs (#423, #477, #369) could allow:
  - Reading variables from enclosing scopes that should be inaccessible
  - Writing to variables in wrong scopes
  - Confusing the interpreter about which object is being referenced
- Missing `global`/`nonlocal` handling could create interesting shadow variable states
- The `del` statement might have different semantics
- `locals()` and `globals()` builtins may expose internal state differently

### What we don't know
- Full list of builtin functions available vs missing
- Whether `eval()`, `exec()`, `compile()` are available or sandboxed
- Whether `__builtins__` inspection reveals anything internal
- Whether `type()` introspection can access internal types

### Attack ideas
- Create deeply nested closures and see which variables "leak"
- Use walrus operator in unusual positions to confuse the parser
- Try `global`/`nonlocal` in edge case positions
- Inspect `globals()` / `locals()` output for host references
