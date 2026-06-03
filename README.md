# Hack Monty — Autonomous Sandbox Security Assessment

An LLM-driven autonomous hacking loop targeting [Pydantic's $10,000 Hack Monty bounty](https://hackmonty.com). Built on the [autoresearch](https://github.com/karpathy/autoresearch) pattern — an agent generates, tests, and iterates on exploit attempts against a live Python sandbox honeypot.

## Architecture

```
program.md          ──► Agent instructions + 8 source-code-derived attack templates
orchestrator.py     ──► Main loop: analyst → coder → run → evaluate → meta-review
agent.py            ──► qwen3.5:cloud via Ollama Cloud API (analyst/coder role split)
hackmonty_client.py ──► hackmonty.com API client (snapshot/resume protocol)
evaluate.py         ──► Strict 0-5 scoring system
issue_tracker.py    ──► GitHub issue fetcher for pydantic/monty + dependencies
notes/              ──► Structured research notebook (understanding, attempts, results)
```

### Loop Flow

```
1. analyst reviews history → picks best attack template + writes strategy
2. coder generates exploit code from template + strategy
3. run against hackmonty.com via snapshot/resume protocol
4. evaluate result on 0-5 scale (strict, no false positives)
5. meta-review every batch → kills dead templates, suggests focus shifts
6. save attempt notes, update knowledge base
```

### Key Features

- **Analyst/Coder Split**: Separate LLM calls for strategy (temp 0.4) and code generation (temp 0.8)
- **Meta-Review**: After each batch, the system analyzes progress and deprioritizes dead-end templates
- **Diversity Enforcement**: 8 consecutive zero-score attempts on a template → auto-killed for 20 cycles
- **Precise Scoring**: No heuristic false positives — only `output` field from non-/data paths scores ≥4
- **GitHub Issue Radar**: Fetches pydantic/monty + pydantic/pydantic-ai issues every 2 hours, categorizes by exploitability

## Attack Templates (Source-Code Audited)

Each template is derived from a specific vulnerability in the [pydantic/monty](https://github.com/pydantic/monty) Rust source code:

| # | Template | Source | Vector |
|---|----------|--------|--------|
| A | Dict Reentry | `dict.rs:463-492` | `__eq__`/`__hash__` callbacks mutating dict mid-lookup |
| B | Set Reentry | `set.rs:722-758` | `__hash__` callback mutating set during add |
| C | Sort cmp | `sorting.rs:84-86,139-164` | O(n log n) `__lt__` callbacks during sort |
| D | min/max mutate | `min_max.rs:104-142` | key= callback mutating iterable during iteration |
| E | Memory drift | `resource.rs:599-602` | alloc/free size mismatch drifting memory counter |
| F | Config files | `/data` mount | Read config.json, logs, docs for host info |
| G | Alloc race | `sorting.rs` + `resource.rs` | Allocation exhaustion mid-sort state |
| H | Async GC | `asyncio.rs:187-197` | gather futures GC during pending state |

## Quick Start

```bash
# Install dependencies
uv sync

# Set Ollama API key (get from https://ollama.com/settings/keys)
echo "OLLAMA_API_KEY=sk-..." > .env
echo "USER_SECRET=cipher-zenith-quantum-drift-hm2026" >> .env

# Run the autonomous loop
uv run python -B orchestrator.py --max-iterations 500 --batch-size 3

# Run snapshot protocol fuzzer
uv run python -B fuzz_snapshots.py
```

## Results

- **200+** exploit attempts across 3 orchestrator versions
- **0** sandbox escapes found
- **Confirmed**: Monty Round 2 is secure against Python-only attacks due to the absence of `class` support, which blocks all callback-based attack surfaces
- **Documented**: 6 CPython divergence points, 15 Monty behavioral quirks, resource limits precisely mapped
- **Audited**: Full dependency tree security advisories (Starlette: 8, Pydantic: 1)
- **Full report**: See [REPORT.md](REPORT.md)

## Structure

```
.
├── orchestrator.py        # Main loop (v2)
├── agent.py               # Ollama client with role-split
├── evaluate.py             # Scoring system
├── hackmonty_client.py     # hackmonty.com API client
├── issue_tracker.py        # GitHub issue fetcher
├── fuzz_snapshots.py       # Snapshot protocol fuzzer
├── program.md              # Agent instructions + templates
├── REPORT.md               # Paper-level security assessment
├── notes/                  # Research notebook
│   ├── understanding/      # Knowledge base entries
│   ├── attempts/           # Timestamped attempt logs
│   └── results/            # Findings log
├── pyproject.toml
├── LICENSE                 # MIT
└── README.md
```

## License

MIT — See [LICENSE](LICENSE)
