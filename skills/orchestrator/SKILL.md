---
name: orchestrator
description: Research-driven sandbox exploit — combine techniques, follow leads
user-invocable: true
auto_include: true
allowed-tools: hackmonty.mcp::hackmonty_run hackmonty.mcp::hackmonty_evaluate hackmonty.mcp::hackmonty_revalidate hackmonty.mcp::attempt_save hackmonty.mcp::state_read hackmonty.mcp::state_write hackmonty.mcp::program_read hackmonty.mcp::github_issues hackmonty.mcp::kg_dashboard hackmonty.mcp::kg_dead_vectors hackmonty.mcp::kg_recent hackmonty.mcp::kg_discover hackmonty.mcp::kg_bootstrap web_search web_fetch read grep
context: fork
argument-hint: "[max_iterations]"
---

## ⚠️ CRITICAL RULES

1. **NEVER probe what kg_dashboard already knows.** Read the dashboard first. If a vector is dead, skip it.
2. **COMBINE techniques.** One technique alone may fail. Try print.__self__ + name_lookup, or sort + gc, or format string + traceback.
3. **EVERY hackmonty_run MUST have a reason.** No blind probes.
4. **Follow research leads.** The Veria Labs writeup found a real Monty GC UAF. That's priority #1.
5. **If stuck for 3 iterations, switch strategy COMPLETELY.** Don't iterate on a dead end.

## BOOTSTRAP (once per session)

```
1. kg_bootstrap() if DB empty
2. kg_dashboard() → understand what's dead, what's promising
3. kg_dead_vectors() → NEVER re-try these
4. program_read() → refresh on constraints
```

## PER ITERATION

```
1. web_search for specific technique → kg_discover with URL ref
2. hackmonty_run(code, reason="Combining {X} + {Y}: {why}")
   → Auto-records to DB with score + reason
3. hackmonty_evaluate(result) → get score
4. Score > 0 → DRILL: 3 variations immediately, revalidate
5. Score = 0, 3rd attempt same vector → kg_discover(category="blocked", ...)
```

## COMBINATION PATTERNS (prioritize these)

- **name_lookup + file read**: Resolve name → Path(resolved).read_text()
- **sort + gc**: Pre-fill allocs, sort with key that triggers gc
- **format string + __code__**: format() attr walk → code object → replace
- **exception + frame walk**: Trigger error → traceback → f_back → builtins
- **async + snapshot chain**: coroutine → function_snapshot → resume with values
- **heap spray + type confusion**: Allocate many same-size objects, free some, trigger realloc

## NEVER DO

- Don't probe what's already in kg_dashboard
- Don't call hackmonty_run without a specific exploit technique
- Don't read state/program/source every iteration — read once
- Don't iterate on score-0 results beyond 2 tries
- Don't use bandit, templates, or rotated vectors

## EXIT

Score 5 → "SECRET FOUND"
Run $ARGUMENTS iterations.
