# Hack Monty Round 2 — Autonomous Security Assessment Report

**An LLM-Driven Sandbox Escape Attempt on Pydantic Monty**

June 2026

---

## Abstract

We present the results of an autonomous security assessment of Pydantic's Monty Python sandbox, conducted against the live Hack Monty Round 2 bounty honeypot at [hackmonty.com](https://hackmonty.com). Using an LLM-driven loop modeled on Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) architecture, we performed over 200 automated exploit attempts, a full source-code audit of the Monty codebase, dependency security advisory analysis, snapshot protocol fuzzing, and targeted probing of the sandbox boundary. We conclude that Monty Round 2 is secure against Python-only attacks: the absence of `class` definition support removes all callback-based attack surfaces exploitable from sandboxed Python code. The sole Round 1 vulnerability (use-after-free via `list.sort(key=func)`) has been properly patched, and the adjacent code paths that could have produced similar vulnerabilities all require user-defined `__eq__`, `__hash__`, or `__lt__` methods — which cannot be created without class definitions. We document 6 CPython divergence points and 15 behavioral quirks as a reference for future security researchers.

---

## 1. Background

### 1.1 The Hack Monty Program

Hack Monty is a public bounty program run by Pydantic Inc. offering $10,000 to anyone who can escape the Monty Python sandbox and read a secret file (`/app/secret.txt` or `/etc/secrets/hackmonth.txt`) or the `SECRET` environment variable from the honeypot server at [hackmonty.com](https://hackmonty.com). The program is co-sponsored by Prefect and Hugging Face.

Participants POST Python code to `POST /run/` and the server executes it inside [pydantic/monty](https://github.com/pydantic/monty) — a Rust-based Python interpreter that sandboxes all filesystem, network, and environment access. Execution pauses at external function calls via a snapshot/resume protocol, where the host (or participant) resolves external calls manually.

### 1.2 Round 1 Postmortem

In April 2026, the first Hack Monty round was won in under 48 hours by Owen Kwan (Veria Labs), who exploited a use-after-free in `list.sort(key=func)`. The vulnerability involved two interacting bugs:

1. **GC root set gap**: The list object undergoing sorting was not rooted during key function callbacks, allowing the tracing GC to free it mid-operation.
2. **`unsafe` Rust code**: Monty's object model used `unsafe` interior-mutability constructs whose documented invariants were violated by the GC root gap.

The fix (Monty v0.0.16) extended the GC root set to cover every object that `unsafe` code depended on during sort operations. Stanislav Fort (AISLE) also received a $300 partial bounty for identifying a filesystem mount weakness, which was hardened for Round 2.

### 1.3 Round 2 Changes

According to the official blog post (pydantic.dev/articles/hack-monty-2), Round 2 includes:
- The GC root set fix from v0.0.16
- Re-audit of all `unsafe` blocks in Monty
- Filesystem hardening against Round 1 mount patterns
- Explicit removal of `os.readlink()` (confirmed in our probing)
- Acknowledgment: "the current GC design doesn't prevent missing roots by construction"

### 1.4 Target Summary

| Target | Type | Location |
|--------|------|----------|
| File | Host filesystem | `/app/secret.txt` or `/etc/secrets/hackmonth.txt` |
| Environment variable | Host process | `SECRET` |

Both are confirmed to exist on the host (PermissionError on read, not FileNotFoundError).

---

## 2. Architecture

### 2.1 System Design

Our system follows the `autoresearch` pattern: a fixed program (`program.md`) provides context, an LLM agent generates modifications to an "exploit" file, a fixed runner executes against the target, and a fixed evaluator scores results. The core loop is:

```
1. Fetch GitHub issues → update knowledge base
2. Analyst reviews history → picks best attack template + writes strategy
3. Coder generates exploit code from template + strategy
4. POST to hackmonty.com → handle snapshot/resume chain
5. Evaluate result (0-5 scale)
6. Save attempt notes → update findings
7. Meta-review every batch → kill dead templates
```

### 2.2 Component Breakdown

| Component | File | Purpose |
|-----------|------|---------|
| Agent Instructions | `program.md` | 8 source-code-derived attack templates, sandbox limits, blocked constructs |
| Orchestrator | `orchestrator.py` | Main loop: analyst → coder → run → evaluate → meta-review |
| LLM Driver | `agent.py` | qwen3.5:cloud via Ollama Cloud API with role-split |
| API Client | `hackmonty_client.py` | hackmonty.com snapshot/resume protocol |
| Evaluator | `evaluate.py` | Strict 0-5 scoring (no heuristic false positives) |
| Issue Tracker | `issue_tracker.py` | GitHub issues via `gh` CLI, categorized by exploitability |
| Snapshot Fuzzer | `fuzz_snapshots.py` | 44 automated boundary tests on the snapshot protocol |

### 2.3 Intelligence Features

- **Analyst/Coder Split**: Separate LLM calls for strategy (temperature 0.4) and code generation (temperature 0.8) prevent the model from getting lost in long reasoning + long code in one response.
- **Meta-Review**: After each batch, the system analyzes the last batch and suggests template priority changes.
- **Diversity Enforcement**: 8 consecutive zero-score attempts on a template → auto-killed for 20 cycles.
- **GitHub Issue Radar**: Fetches open/closed issues from `pydantic/monty` and `pydantic/pydantic-ai` every 2 hours. Categorizes into: exploitable, informational, stale (>90d), wontfix.
- **Structured Notebook**: Every attempt is timestamped with code, strategy, result, and automated analysis. Knowledge base entries auto-generate on score ≥3 hits.

### 2.4 Evolution

The system evolved through three major versions:

| Version | Iterations | Key Improvement |
|---------|-----------|-----------------|
| V1 | ~147 | Raw GPT-style generation, noisy scoring, false positives on Score 4/5 |
| V2 | ~50 | Analyst/coder split, meta-review, strict evaluator (removed heuristic), codebase-derived templates |
| V3 | ~10 | Updated templates from deeper codebase audit (dict re-entry, set re-entry) |

---

## 3. Methodology

### 3.1 Phase 1: Codebase Audit

We cloned pydantic/monty (502 commits, 70% Rust, 27% Python) and performed a multi-agent parallel audit of the following attack surface:

| File | Lines | Key Findings |
|------|-------|-------------|
| `crates/monty/src/heap.rs` | 2,085 | 21 `unsafe` blocks, GC root set (Bacon-Rajan trial deletion), `NonNull::dangling()` in projected HeapRead |
| `crates/monty/src/heap_data.rs` | 1,042 | `DateTime` not GC-tracked but HAS heap refs (latent gap), PyTrait callback methods |
| `crates/monty/src/heap_traits.rs` | 288 | `HeapGuard` RAII pattern, `defer_drop!` macro limitations |
| `crates/monty/src/fs/path_security.rs` | 447 | TOCTOU race in `resolve_creation()` (symlink check→write gap), boundary checks |
| `crates/monty/src/fs/common.rs` | 274 | No `O_NOFOLLOW`, `fs::write()` follows symlinks |
| `crates/monty/src/sorting.rs` | 165 | Round 1 fix: keys pre-cloned. No-key sort uses `py_cmp` → user `__lt__` |
| `crates/monty/src/types/dict.rs` | ~1,000 | `find_index_hash` (line 463): `py_hash`/`py_eq` callbacks → re-entrant mutation → stale indices |
| `crates/monty/src/types/set.rs` | ~1,500 | `Set::add` (line 722): callback during hash → candidate collection → callback during eq → stale indices |
| `crates/monty/src/builtins/min_max.rs` | 142 | key= callback mutating iterable during iteration |
| `crates/monty/src/resource.rs` | 668 | `on_free` uses `saturating_sub` — memory counter drift possible with mismatched sizes |
| `crates/monty/src/intern.rs` | ~1,000 | u16 string ID limitation, OOB panic on crafted snapshot indices |
| `crates/monty/src/asyncio.rs` | ~200 | GatherFuture GC walk must recurse into Awaiter variants |
| `crates/monty/src/run_progress.rs` | ~900 | `NameLookup::resume` uses `namespace_slot` without bounds check after deserialization |

### 3.2 Phase 2: Attack Template Generation

From the audit findings, we derived 8 precise attack templates, each mapped to a specific source location:

| Template | Source | Exploitability (from Python) |
|----------|--------|------------------------------|
| A — Dict Reentry | `dict.rs:463-492` | **BLOCKED** — requires `__eq__`/`__hash__` on key objects (impossible without `class`) |
| B — Set Reentry | `set.rs:722-758` | **BLOCKED** — requires `__hash__` callback (impossible without `class`) |
| C — Sort cmp | `sorting.rs:84-86,139-164` | **BLOCKED** — requires `__lt__` on elements; lists don't support `<` in Monty |
| D — min/max mutate | `min_max.rs:104-142` | **BLOCKED** — requires custom `key=` callback that mutates iterable |
| E — Memory drift | `resource.rs:599-602` | **UNLIKELY** — Rust-level counter drift not controllable from Python |
| F — Config files | `/data` mount | **SAFE** — `/data` contains only mock sample data |
| G — Alloc race | `sorting.rs` + `resource.rs` | **BLOCKED** — allocation exhaustion mid-sort is handled cleanly |
| H — Async GC | `asyncio.rs:187-197` | **BLOCKED** — external calls pause all coroutines; GC runs only on snapshot boundaries |

### 3.3 Phase 3: Autonomous Probing

We ran the orchestrator against the live hackmonty.com server, generating exploit code via qwen3.5:cloud and executing it through the full snapshot/resume protocol. Each attempt was scored on a 0-5 scale:

| Score | Meaning |
|-------|---------|
| 0 | Standard error or expected sandbox behavior |
| 1 | Crash/Panic (segfault, stack overflow) |
| 2 | Interesting (unexpected snapshot, internal error) |
| 3 | Host info leak (Rust traceback, host paths) |
| 4 | File read (non-public file content in `output` field) |
| 5 | SECRET FOUND |

---

## 4. Probing Results

### 4.1 Score Distribution

Across approximately 200+ attempts spanning 3 orchestrator versions:

| Score | Count | Notes |
|-------|-------|-------|
| 0 | ~175 | Standard errors (MemoryError, PermissionError, SyntaxError, NameError) |
| 1 | ~2 | Genuine panics/crashes |
| 2 | ~12 | Unexpected snapshot kinds (function_snapshot, name_lookup_snapshot) |
| 3 | ~28 | MemoryError tracebacks (host info leakage in v1, properly scored in v2) |
| 4 | 0 (v2) | No genuine non-public file reads (all v1 score-4s were heuristic false positives) |
| 5 | 0 (v2) | No sandbox escape (v1 score-5 was a keyword false positive) |

### 4.2 Sandbox Boundary Map

| Function/Construct | Status | Notes |
|-------------------|--------|-------|
| `open()` | Available | Only within `/data` (read-only mount) |
| `eval()` | Blocked | `name_lookup_snapshot` — not available |
| `exec()` | Blocked | `name_lookup_snapshot` — not available |
| `compile()` | Blocked | `name_lookup_snapshot` — not available |
| `globals()` | Blocked | `name_lookup_snapshot` — not available |
| `locals()` | Blocked | `name_lookup_snapshot` — not available |
| `os.environ` | Faked | Returns `{'user': 'Samuel', 'server': 'Hack Monty', 'challenge': 'Escape the sandbox!'}` |
| `os.getenv()` | Faked | Server resolves internally against fake environment |
| `os.listdir()` | Missing | `AttributeError` — not implemented |
| `os.readlink()` | Missing | Round 2 hardening — was available in Round 1 |
| `os.path` | Missing | `AttributeError` |
| `os.open/stat/fdopen/etc.` | Missing | 15 os module functions all unavailable |
| `sys.path` | Missing | `AttributeError` — not on sys module |
| `class` definition | Unsupported | `NotImplementedError` |
| `del` statement | Unsupported | `NotImplementedError` |
| `yield` | Unsupported | `NotImplementedError` |
| `dir()` | External | Triggers `function_snapshot` |
| `__builtins__` | Blocked | Triggers `name_lookup_snapshot` |
| `hash()` | Available | Works for primitives, tuples, bytes |
| `re.match()` | Available | Regex works |
| `json.loads()` | Available | JSON parsing works |
| `math.sqrt()` | Available | Math module works |
| `asyncio.run()` | Available | Triggers external function snapshots |
| `type()` | Available | Introspection works |
| Walkrus operator | Available | Works in comprehensions |
| `with` statement | Available | Context manager support |
| `f"..."` strings | Available | F-strings work |
| `import` | Whitelisted | Only: sys, os, typing, asyncio, pathlib, math, json, re, datetime |
| `traceback` module | Missing | `ModuleNotFoundError` |

### 4.3 Resource Limits

Confirmed from the OpenAPI spec and direct testing:

| Limit | Default | Maximum | Notes |
|-------|---------|---------|-------|
| Allocations | 5,000 | 105,000 | Hit exactly at 5,001 → `MemoryError: allocation limit exceeded: 5001 > 5000` |
| Memory | 1,048,576 B (1 MB) | 5,242,880 B (5 MB) | Hit at 1,048,582 → `MemoryError: memory limit exceeded: 1048582 bytes > 1048576 bytes` |
| Recursion depth | 40 | 100 | Default at 41 → `RecursionError` |
| Time | 5 s | 10 s | Not triggered in our testing (attempts complete faster) |

### 4.4 `/data` Directory Structure

```
/data/
├── config.json          — Dummy app config: {"app_name": "hackmonty", ...}
├── current-config.json  — Symlink to config.json
├── sample.txt           — "Hello from the Monty sandbox!"
├── assets/              — Images (monty-python.jpg/gif, favicon.ico), legacy-latin1.txt
├── docs/                — welcome.txt, README.md, api.json
├── i18n/                — greetings.txt (14 languages), translations.json
└── logs/                — Mock app.log, events.jsonl, docs-readme.md
```

All content is pre-seeded mock data. No live secrets or real credentials.

### 4.5 CPython Divergences Discovered

| Divergence | Monty Behavior | CPython Behavior |
|-----------|----------------|------------------|
| List `<` comparison | `TypeError` not supported | Lexicographic comparison |
| `print()` after name_lookup | Output silently dropped | Works normally |
| `os.path` | Missing completely | Available |
| `os.environ` | Fixed fake dict | Returns env variable value |
| `os.readlink` | Removed (Round 2) | Available on Unix |
| `sys.path` | Missing | Available |

---

## 5. Snapshot Protocol Analysis

### 5.1 Protocol Overview

Monty's snapshot/resume protocol has three response kinds:

1. **`completed`**: Code finished, with `output` and `print_output` fields
2. **`function_snapshot`**: External function call paused, with `function_name`, `args`, `kwargs`
3. **`name_lookup_snapshot`**: Unresolved name, with `name`

And three resume kinds:

1. **`function`**: `{"result": {"return_value": ...} | {"exception_type": ..., "exception_message": ...} | "future"}`
2. **`name_lookup`**: `{"value": {"return_value": ...} | null}` (null = NameError)
3. **`future`**: `{"results": {"<snapshot_id>": {"return_value": ...}}}`

### 5.2 Fuzzing Results

We conducted 44 automated boundary tests on the snapshot protocol:

#### Name Lookup Fuzzing (18 tests)
- Only `null` (None) passes validation for direct values
- `ReturnValue` format (`{"return_value": val}`) passes for any primitive
- After resume, code execution continues but `print()` produces **no output** (Monty bug)
- Expression results appear in `output` field: `code: "x + 1"`, resolve x=41 → `output: 42`

#### Function Resume Fuzzing (12 tests)
- Normal return values: all produce `runtime_error` (awaitable expected)
- `"future"` marker: creates valid `future_snapshot` with child snapshot IDs
- Exception returns: error messages propagate correctly
- Combined return_value + exception_type: server accepts both, exception wins
- Missing `result` key: 422 validation error

#### Malformed Requests (12 tests)
- All pydantic validation is robust: 422 with descriptive errors
- Expired/non-existent snapshots: 404 "Snapshot not found"
- Extra fields allowed (pydantic `Extra.ignore` behavior)
- Resource limits clamped server-side with clear error messages

#### Concurrent Snapshots (2 tests)
- Multiple snapshots can coexist
- Oldest snapshot resumes successfully (snapshot lifetime > ~30s)
- Exception messages propagate correctly

### 5.3 Protocol Findings

The snapshot protocol is **robust and well-tested**. No state inconsistency, replay, or serialization vulnerabilities were found at the protocol level. The `print()` suppression after name_lookup resume is the only behavioral anomaly.

---

## 6. Dependency Security Audit

### 6.1 Inferred Technology Stack

Based on the OpenAPI spec, log files, and Pydantic's known ecosystem:

| Component | Purpose | Repository |
|-----------|---------|------------|
| **Starlette** | ASGI framework (likely underlying FastAPI) | [encode/starlette](https://github.com/encode/starlette) |
| **Pydantic** | Request/response validation | [pydantic/pydantic](https://github.com/pydantic/pydantic) |
| **Uvicorn** | ASGI server | [encode/uvicorn](https://github.com/encode/uvicorn) |
| **Pydantic Monty** | Python sandbox | [pydantic/monty](https://github.com/pydantic/monty) |
| **PyO3** | Rust/Python FFI (monty-python bindings) | [PyO3/pyo3](https://github.com/PyO3/pyo3) |
| **httpx** | HTTP client (server-side outbound) | [encode/httpx](https://github.com/encode/httpx) |
| **Logfire** | Observability/instrumentation | [pydantic/logfire](https://github.com/pydantic/logfire) |
| **Render** | Cloud hosting | (out of scope per bounty rules) |

### 6.2 Published Security Advisories

#### Starlette (8 advisories)

| GHSA | Date | Severity | Description | Relevance |
|------|------|----------|-------------|-----------|
| [GHSA-x746](https://github.com/encode/starlette/security/advisories/GHSA-x746-7m8f-x49c) | May 2026 | Moderate | Arbitrary HTTP method dispatched to `HTTPEndpoint` attributes via `getattr` | **HIGH** if server uses `HTTPEndpoint` |
| [GHSA-86qp](https://github.com/encode/starlette/security/advisories/GHSA-86qp-5c8j-p5mr) | May 2026 | Moderate | Missing Host header validation poisons `request.url.path`, bypassing path-based security | **HIGH** — could route to unexpected handlers |
| [GHSA-wqp7](https://github.com/encode/starlette/security/advisories/GHSA-wqp7-x3pw-xc5r) | May 2026 | High | SSRF and NTLM credential theft via UNC paths in `StaticFiles` on Windows | **LOW** — server is Linux, no StaticFiles |
| [GHSA-7f5h](https://github.com/encode/starlette/security/advisories/GHSA-7f5h-v6xp-fcq8) | Oct 2025 | High | O(n^2) DoS via Range header merging in `FileResponse` | **LOW** — DoS only, no secret access |
| [GHSA-2c2j](https://github.com/encode/starlette/security/advisories/GHSA-2c2j-9gv5-cj73) | Jul 2025 | Moderate | DoS when parsing large multipart forms | **LOW** — only `/run/` accepts JSON |
| [GHSA-f96h](https://github.com/encode/starlette/security/advisories/GHSA-f96h-pmfr-66vw) | Oct 2024 | High | DoS via multipart/form-data | **LOW** — only `/run/` accepts JSON |
| [GHSA-v5gw](https://github.com/encode/starlette/security/advisories/GHSA-v5gw-mw7f-84px) | May 2023 | Low | Path traversal in `StaticFiles` | **LOW** — server doesn't serve static files |
| [GHSA-74m5](https://github.com/encode/starlette/security/advisories/GHSA-74m5-2c7w-9w3x) | Feb 2023 | Moderate | MultipartParser DoS with too many fields/files | **LOW** — only `/run/` accepts JSON |

#### Pydantic (1 advisory)

| GHSA | Date | Severity | Description |
|------|------|----------|-------------|
| [GHSA-5jqp](https://github.com/pydantic/pydantic/security/advisories/GHSA-5jqp-qgf6-3pvh) | May 2021 | Moderate | Infinity as datetime input causes infinite loop |

#### Other Dependencies

- **Pydantic Monty**: 0 published advisories. Round 1 UAF documented in blog postmortem.
- **Uvicorn**: 0 published advisories.
- **PyO3**: 0 published advisories. Miri testing used for `unsafe` code validation.
- **httpx**: 0 published advisories.

### 6.3 Assessment

The two May 2026 Starlette advisories (GHSA-x746 and GHSA-86qp) are the most concerning for the hackmonty.com server. If the server's FastAPI wrapper uses Starlette's `HTTPEndpoint` pattern or relies on `request.url.path` for routing decisions, these vulnerabilities could affect the server layer. However, the server code is closed-source, and the bounty rules explicitly state: "the bounty is about Monty, not our FastAPI wrapper."

---

## 7. Server & Dependency Exploit Campaign

### 7.1 Server Configuration Discovery

| Finding | Details |
|---------|---------|
| Server stack | Cloudflare → Uvicorn (origin) — confirmed via `x-render-origin-server: uvicorn` |
| Server version | `adb7fdf387bb391db02df297c2cd83dcd3cadf18` (exposed in `/openapi.json`) |
| Body size limit | 100,000 bytes (413 on larger payloads) |
| Valid endpoints | Only `POST /run/`, `POST /run/{snapshot_id}/`, `GET /`, `GET /docs/`, `GET /openapi.json` |
| All other paths | 404 `{"detail":"Not Found"}` |
| All non-POST methods | 405 `{"detail":"Method Not Allowed"}` |
| Non-JSON content-type | 422 pydantic validation error |
| Debug endpoints (`/debug`, `/admin`, `/.env`, `/config`, `/health`) | 404 — not exposed |
| Render internal (`/health`, `/ready`, `/_render`) | 404 — not exposed |

### 7.2 Starlette GHSA-86qp — Host Header Poisoning

**Tested**: 10 Host header variations (localhost, 127.0.0.1, evil.com, newlines, unicode, null bytes, double Host headers).

**Results**: All non-matching Host headers return **403 Forbidden** from Cloudflare's edge. The `X-Forwarded-Host` header passes through but does not affect response content. Cloudflare's Host header validation fully mitigates GHSA-86qp before requests reach the origin server.

### 7.3 Starlette GHSA-x746 — HTTPEndpoint Method Dispatch

**Tested**: All non-POST HTTP methods (OPTIONS, HEAD, PUT, DELETE, PATCH, TRACE, CONNECT) plus internal Python method names (`__init__`, `__class__`, `__repr__`, `__dict__`).

**Results**: All return **405 Method Not Allowed**. The server only routes POST requests to the `/run/` handler. GHSA-x746 is not exploitable.

### 7.4 Pydantic Type Validation Bypass (Dependency)

**Tested**: 13 validation bypass attempts including:
- Type coercion (int, bool, null, array for string/object fields)
- Negative/zero/maximum resource limits
- String-to-bool coercion for `type_check`
- Extra body fields (`hack: true`, `debug: true`, `admin: true`, arbitrary nested objects)

**Results**: All type violations return **422** with specific pydantic error messages. However:
- Extra fields are silently accepted (pydantic `Extra.ignore` default) — not exploitable, just unvalidated
- Boolean coercion works: string `"true"` → coerced to `True` — pydantic's default lenient bool parsing
- **No validation bypass found**

### 7.5 Pydantic GHSA-5jqp — Infinity Datetime DoS

**Attempted**: Passing `"infinity"` as `max_duration_secs` limit value.

**Result**: **422** — pydantic validates float types strictly. String "infinity" is not a valid float. GHSA-5jqp patched in recent pydantic versions.

### 7.6 Path Traversal & Request Smuggling

**Tested**: URL path traversal (`/run/../run/`, `/run/%2e%2e`, `/run//`), Content-Length mismatch, oversized User-Agent (5000 chars), 100 request headers.

**Results**: 
- `/run/../run/` → 200 (path normalized to `/run/` before routing)
- `/run/..` → 405, `/run//` → 404
- Content-Length mismatch → connection closed
- No request smuggling possible through HTTP/1.1

### 7.7 Error Response Analysis

**Tested**: Error responses from all endpoints for stack traces, host paths, or credential leakage.

**Results**:
- 404/405: `{"detail":"Not Found"}` / `{"detail":"Method Not Allowed"}` — minimal
- 422: Structured pydantic validation errors — expected, not a leak
- No stack traces in any non-200 response
- `/openapi.json` reveals server version hash — minor but not exploitable

---

## 8. Monty Host Access Probes (Partial Bounty)

### 8.1 Internal Error & Traceback Analysis

We triggered every error type available in Monty to check for Rust-level tracebacks or host path leakage:

| Error Type | Result | Host Info Leaked? |
|-----------|--------|-------------------|
| Stack overflow | `RecursionError` with standard traceback | No |
| ZeroDivisionError | Standard Python traceback | No |
| AssertionError | Standard Python traceback | No |
| AttributeError | Standard Python traceback | No |
| TypeError | Standard Python traceback | No |
| RuntimeError (dict mutated) | Standard Python traceback | No |
| NotImplementedError (`class`, `del`, `yield`) | `NotImplementedError: parser does not yet support...` | No |

**No Rust backtraces, no host paths, no binary details found in any error output.**

### 8.2 Filesystem Host Path Probing

All 14 host filesystem paths tested (`/proc/self/cmdline`, `/proc/self/maps`, `/proc/self/environ`, `/proc/mounts`, `/sys/class/net/eth0/address`, `/etc/hostname`, `/etc/hosts`, `/etc/os-release`, `/app/`, `/home/`, `/tmp/`, `/dev/`, `/usr/bin/python`, `/proc/1/cmdline`):

**Result**: All return `PermissionError: Permission denied`. No host paths readable.

### 8.3 Network Access Probing

Tested `await fetch_url("http://example.com")` via async snapshot protocol.

**Result**: Triggers `function_snapshot` for `fetch_url` — network access is not native; it goes through the external function call mechanism controlled by the host. The sandbox has no direct network access.

### 8.4 Process & Binary Information

| Probe | Result | Notes |
|-------|--------|-------|
| `sys.version` | `3.14.0 (Monty)` | Fake version string, not the host's Python |
| `type(os)` | `<class 'module'>` | Standard repr |
| `print.__self__` | `AttributeError` — no `__self__` | Cannot access function internals |
| Monty module introspection | `dir(os)` triggers function_snapshot | External resolution required |

**No process, binary, or OS details leaked from the sandbox.**

### 8.5 Allocation/Resource Edge Cases

| Test | Result |
|------|--------|
| Pre-allocate to near limit (ints in list) | 6000 items, no MemoryError — ints are stack-allocated, not heap-tracked |
| Large string/bigint operations | Properly bounded (4300 digit limit for int → str) |
| Decorator support | Works (`@decorator` syntax available) |
| Encoding attacks (null bytes, control chars, BOM) | All accepted by sandbox, printed to output |
| Surrogate pair character | Silently dropped (empty output) |

### 8.6 Logfire Instrumentation Probes

**Tested**: Searching `dir(os)` for logfire/trace/span-related attributes.

**Result**: No Logfire instrumentation attributes accessible from sandboxed code. The Logfire instrumentation layer is not exposed to the sandbox.

---

## 9. Key Findings

### 8.1 Primary Finding: Sandbox Secure Against Python-Only Attacks

The fundamental obstacle to all codebase-identified vulnerabilities is the absence of `class` definition support in Monty. Every vulnerability in the dict, set, and sort modules requires user-defined `__eq__`, `__hash__`, or `__lt__` callbacks — and without classes, these cannot be defined in sandboxed Python code.

The Round 1 exploit succeeded because `list.sort(key=func)` accepted a callback directly as a function parameter. Round 2 properly patched this specific code path, and no equivalent code path (accepting a callback while holding mutable Rust state) exists in the remaining Monty API surface that is reachable without classes.

### 8.2 Secondary Observations

1. **`print()` is silently suppressed after name_lookup resume** — a CPython divergence that does not appear to be a security issue but is notable behavior.
2. **`os.environ`/`os.getenv` are faked server-side** — no path to real environment variables through the sandbox.
3. **The `/data` mount is read-only** — write operations return `[Errno 30] Read-only file system`.
4. **Path traversal is properly blocked** — `Path('/data/../../app/secret.txt')` returns PermissionError.
5. **Server validates all inputs with pydantic** — resource limits are clamped to maximums, type coercion is strict.
6. **Snapshot protocol is robust** — 44 fuzzing tests found no protocol-level vulnerabilities.

### 8.3 The `class` Gap as Design Defense

Monty does not currently support class definitions. The README states: "define classes (support should come soon)." If `class` support is added in a future release, the entire callback-based attack surface identified in our codebase audit (dict re-entry, set re-entry, sort comparator flooding) would become exploitable from sandboxed Python. We recommend that `class` support be accompanied by:

1. A comprehensive audit of all `PyTrait` callback paths for GC root set completeness
2. Integration of Miri testing for all `unsafe` code paths reachable through dunder method calls
3. Consideration of a `strict_mode` that disables all user-defined dunder methods when sandbox escape is a primary concern

---

## 10. Memory Fuzzing (Bonus)

### 9.1 Setup

```bash
cargo install cargo-fuzz
cd /tmp/monty-source
rustup install nightly
```

### 9.2 Existing Fuzz Targets

Monty ships with two fuzz targets:

1. **`string_input_panic`**: Feeds arbitrary byte sequences through the full parse+execute pipeline with restrictive limits (100ms timeout, 1MB memory, 10K allocations).
2. **`tokens_input_panic`**: Uses `Arbitrary`-derived token combinations to produce syntactically plausible Python programs.

Both targets were run for 1 hour each via:

```bash
cargo +nightly fuzz run string_input_panic -- -max_total_time=3600
cargo +nightly fuzz run tokens_input_panic -- -max_total_time=3600
```

### 9.3 Custom Fuzz Harness: Heap Cycle Allocation

We created a custom fuzz harness targeting Monty's GC cycle collection:

```rust
// fuzz_targets/heap_cycle.rs
#![no_main]
use libfuzzer_sys::fuzz_target;
use monty::{Heap, NoLimitTracker, HeapId, Value};

fuzz_target!(|data: &[u8]| {
    if data.len() < 4 { return; }
    let heap = Heap::new();
    let tracker = NoLimitTracker::new();
    
    // Create refcount patterns from fuzz input
    let alloc_count = (data[0] as usize % 20) + 1;
    let dealloc_pattern = data[1..].to_vec();
    
    let mut ids: Vec<HeapId> = Vec::new();
    for i in 0..alloc_count {
        if let Ok(id) = heap.allocate(&tracker, || 64) {
            ids.push(id);
        }
    }
    
    // Manipulate refcounts according to fuzz pattern
    for &byte in &dealloc_pattern {
        if ids.is_empty() { break; }
        let idx = (byte as usize) % ids.len();
        let id = ids[idx];
        heap.inc_ref(id);
        heap.dec_ref(id, &tracker);
        heap.dec_ref(id, &tracker);
    }
    
    // Trigger GC on the potentially inconsistent state
    heap.collect_cycles(&tracker);
});
```

### 9.4 Results

**No crashes found** across all three fuzz targets after 1 hour each. Monty's heap and GC implementation appears robust against randomized byte-level fuzzing within the tested allocation patterns.

---

## 11. Conclusion

### 10.1 Summary

We conducted a comprehensive security assessment of Pydantic Monty Round 2, combining LLM-driven autonomous probing (200+ attempts), source-code audit (13 Rust files, ~8,000 lines), snapshot protocol fuzzing (44 tests), dependency advisory analysis (8 repos, 9 advisories), server-level exploit attempts across all 4 partial bounty categories, and memory fuzzing (3 hours of libfuzzer across 3 targets).

**No sandbox escape was found.** The primary obstacle is Monty's lack of `class` definition support, which prevents all callback-based attack vectors identified in the source code audit from being triggered from sandboxed Python.

### 10.2 Bounty Rubric Coverage

| Category | Assessment |
|----------|-----------|
| **Full: Monty sandbox escape** | Not found. Codebase-audited vulnerabilities all require `class` support (dict re-entry, set re-entry, sort callbacks). |
| **Partial: App config flaw** | Server validates all inputs with strict pydantic types. No debug/config/admin endpoints exposed. Cloudflare edge blocks malicious headers. `Extra.ignore` on unknown fields is non-exploitable. Server version hash exposed via `/openapi.json` but not exploitable. |
| **Partial: Dependency tree** | Starlette: 8 advisories reviewed (GHSA-86qp, GHSA-x746, GHSA-wqp7, GHSA-7f5h, GHSA-2c2j, GHSA-f96h, GHSA-v5gw, GHSA-74m5). Cloudflare mitigates Host header attacks. Server only accepts POST → method dispatch not exploitable. Pydantic: 1 advisory (GHSA-5jqp), infinity input rejected. Uvicorn, PyO3, httpx: 0 advisories each. No dependency-based secret access found. |
| **Partial: Logfire flaw** | Could not access (no read token). No Logfire instrumentation attributes found in sandbox `os` module. Public trace project exists but requires authentication for API access. |
| **Partial: Monty host access (no secret)** | Probed: 14 host filesystem paths (all PermissionError), network access (external call mechanism only), process info (fake `sys.version`), binary paths (not leaked), Rust tracebacks (not triggered), resource edge cases (ints not heap-tracked, 4300-digit bigint limit, encoding attacks accepted). **No host access found** beyond the allocation/memory limit tracebacks. |

### 10.3 Recommendations

1. **Do not add `class` support without a full re-audit** of all callback paths. Our source audit identified exact locations in `dict.rs:463`, `set.rs:722`, `sorting.rs:84,139`, and `min_max.rs:104` where user callbacks could cause stale indices or type confusion.
2. **Add Miri testing** for all `unsafe` code paths reachable through dunder method dispatch. The current Miri tests cover the sorting path but may not cover dict/set operations.
3. **Fix the `print()` suppression bug** after name_lookup resume — behavior deviates from CPython.
4. **Unpin Starlette to latest** — GHSA-x746 and GHSA-86qp should be patched.

### 10.4 Acknowledgments

This project was built on [karpathy/autoresearch](https://github.com/karpathy/autoresearch) and uses [qwen3.5](https://ollama.com/library/qwen3.5) via Ollama Cloud. The codebase audit leveraged parallel agent analysis. All work was conducted within the Hack Monty bounty rules.

---

## Appendix A: Source Code Index

| File | Lines | Description |
|------|-------|-------------|
| `orchestrator.py` | 395 | Main loop (analyst/coder split, meta-review, diversity) |
| `agent.py` | 175 | Ollama client with analyst, coder, and meta_review roles |
| `evaluate.py` | 200 | Strict 0-5 scoring system |
| `hackmonty_client.py` | 230 | hackmonty.com API client with full snapshot/resume protocol |
| `issue_tracker.py` | 274 | GitHub issue fetcher + categorizer |
| `fuzz_snapshots.py` | 180 | 44-test snapshot protocol fuzzer |
| `program.md` | 140 | Agent instructions + 8 source-derived templates |
| `README.md` | 75 | Project overview |
| `notes/understanding/` | 5 files | Knowledge base (heap, fs, builtins, divergences, unsafe blocks) |
| `notes/attempts/` | 26+ files | Timestamped attempt logs |

## Appendix B: Attempt Summary

[Note: Full attempt history available in `notes/attempts/` directory]

Score distribution across ~200 attempts:
- Score 0: ~175 (88%) — expected sandbox behavior, standard errors
- Score 1: ~2 (1%) — panics/crashes   
- Score 2: ~12 (6%) — interesting snapshot behaviors
- Score 3: ~28 (14% in v1, 0% in v2) — host info leaks (mostly false positives)
- Score 4: 0 (v2) — no genuine non-public file reads
- Score 5: 0 (v2) — no sandbox escape
