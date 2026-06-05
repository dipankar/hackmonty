# Hack Monty — Autonomous Sandbox Security Assessment

An LLM-driven autonomous hacking loop targeting [Pydantic's $10,000 Hack Monty bounty](https://hackmonty.com). Built on the [autoresearch](https://github.com/karpathy/autoresearch) pattern, evolved with XBOW-style parallelism and bandit selection.

## Architecture

```
                      ┌──────────────────────────────────────┐
                      │          orchestrator.py (v3)         │
                      │          4-worker async swarm         │
                      │                                      │
program.md ──────────►│  ┌─worker 0──┐ ┌─worker 1──┐       │
notes/ ──────────────►│  │ bandit→A  │ │ bandit→C  │  ...  │
issue_tracker.py ────►│  │ →coder    │ │ →coder    │       │
source_scanner.py ───►│  │ →run→eval │ │ →run→eval │       │
                      │  │ →validate │ │ →validate │       │
                      │  └───────────┘ └───────────┘       │
                      │          │              │            │
                      │     shared bandit + score_counts    │
                      │     meta-review every 12 iterations  │
                      └──────────────────────────────────────┘
```

### Loop Flow (per worker)

```
1. bandit (UCB1) selects template with highest exploration/exploitation score
2. analyst (minimax-m3:cloud) reviews history → writes 3-sentence strategy
3. coder (minimax-m3:cloud) generates exploit from template + strategy
4. POST to hackmonty.com → handle snapshot/resume chain
5. evaluate on 0-5 scale with snapshot diff enrichment
6. re-validate (3x re-run, ≥2/3 output hash match to confirm)
7. bandit update with novelty penalty for near-duplicates
8. meta-review every 12 iterations → kill dead templates
```

### Key Features

- **4-worker async swarm**: `asyncio.create_task` workers run in parallel via `httpx.AsyncClient` connection pool
- **UCB1 bandit selection**: Math-driven template choice replaces LLM meta-review for picking; the LLM only provides tactical strategy within a template
- **Re-validation**: Score ≥ 2 triggers 3x independent re-runs; flaky results demoted to score 1
- **Novelty hashing**: blake2b hash of normalized code penalizes near-duplicate exploits
- **Snapshot context enrichment**: Analyst sees allocation counts, snapshot kinds, and path denials — not just scores
- **Analyst/Coder split**: Separate LLM calls for strategy (temp 0.4) and code generation (temp 0.8)
- **Strict scoring**: No heuristic false positives — only `output` field from non-/data paths scores ≥ 4
- **GitHub issue radar**: Fetches pydantic/monty + pydantic/pydantic-ai issues every 2 hours
- **Source scanner**: Static analysis of monty Rust source — 41 unsafe blocks mapped across 4 files

## Attack Templates (Source-Code Audited)

Templates A-H are derived from specific vulnerabilities in the [pydantic/monty](https://github.com/pydantic/monty) Rust source. Templates I-K probe the snapshot/resume protocol layer.

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
| I | Name lookup | Snapshot protocol | Resume name_lookup with crafted values |
| J | Future chain | Snapshot protocol | Multi-level future snapshot chaining |
| K | Double resume | Snapshot protocol | Same snapshot resumed 3× with different values |

## Quick Start

```bash
# Install dependencies
uv sync

# Set credentials (API key from https://ollama.com/settings/keys)
echo "OLLAMA_API_KEY=sk-..." > .env
echo "USER_SECRET=your-unique-passphrase" >> .env

# Run the autonomous swarm (4 workers, 500 iterations)
OLLAMA_API_KEY=sk-... USER_SECRET=your-passphrase \
  uv run python -B orchestrator.py --max-iterations 500 --workers 4

# Run source scanner (one-time)
uv run python -B source_scanner.py

# Run snapshot protocol fuzzer
uv run python -B fuzz_snapshots.py
```

## Results

- **250+** exploit attempts across 3 orchestrator versions
- **0** sandbox escapes found
- **Confirmed**: Monty Round 2 is secure against Python-only attacks — the absence of `class` support blocks all callback-based attack surfaces
- **1 latent unsafe bug** found: `heap_read_boxed` provenance mismatch in RePattern handler
- **43 unsafe blocks** audited across 100+ Rust source files
- **9 GHSA advisories** reviewed across the dependency tree (all mitigated)
- **6 CPython divergences** documented, 15 Monty behavioral quirks mapped
- **Full report**: [REPORT.md](REPORT.md) | **Bounty submission**: [SUBMISSION.md](SUBMISSION.md)

## Structure

```
.
├── orchestrator.py        # V3 async swarm (4 workers, bandit, re-validation)
├── agent.py               # minimax-m3:cloud driver (analyst/coder/meta-review)
├── bandit.py              # UCB1 template selection + novelty hashing
├── evaluate.py            # 0-5 scoring + snapshot context enrichment
├── hackmonty_client.py    # Sync + async API clients (snapshot/resume protocol)
├── issue_tracker.py       # GitHub issue fetcher via gh CLI
├── source_scanner.py      # Monty Rust source static analysis
├── fuzz_snapshots.py      # Snapshot protocol fuzzer (44 boundary tests)
├── exploit_campaign.py    # Second-order attack campaign suite
├── program.md             # Agent instructions + 11 attack templates
├── REPORT.md              # 12-section paper-level security assessment
├── SUBMISSION.md          # Bounty submission (unsafe provenance bug)
├── notes/
│   ├── understanding/     # Knowledge base (heap, fs, builtins, GC, unsafe)
│   ├── attempts/          # Timestamped attempt logs with auto-analysis
│   ├── results/           # Findings log
│   └── source_scan.json   # Automated unsafe block scan results
├── pyproject.toml
├── LICENSE                # MIT
└── README.md
```

## License

MIT — See [LICENSE](LICENSE)
