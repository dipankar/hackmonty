# Hack Monty — Autonomous Sandbox Security Assessment

An LLM-driven autonomous hacking loop targeting [Pydantic's $10,000 Hack Monty bounty](https://hackmonty.com). Built on the [autoresearch](https://github.com/karpathy/autoresearch) pattern, evolved through four versions to XBOW-style parallel swarms and finally to a [tokenworm](https://github.com/tokenworm/tokenworm) + MCP architecture.

## Architecture (V4)

```
                    ┌──────────────────────────────────────┐
                    │   tokenworm (LLM agent harness)       │
                    │                                       │
                    │  Provider: ollama_native              │
                    │  Skills: 4 role-focused SKILL.md      │
                    │  Sandbox: bwrap + network             │
                    │                                       │
                    │         MCP Client (stdio)             │
                    └───────────────┬──────────────────────┘
                                    │
                    ┌───────────────▼──────────────────────┐
                    │    hackmonty_mcp_server.py            │
                    │    17 boundary tools                  │
                    │    (run, evaluate, bandit, state)     │
                    └───────────────┬──────────────────────┘
                                    │
                    ┌───────────────▼──────────────────────┐
                    │  hackmonty.com    Ollama Cloud       │
                    │  GitHub Issues    Filesystem (notes) │
                    └──────────────────────────────────────┘
```

## Quick Start

### Production (tokenworm Zig binary)
```bash
# Requires: ollama daemon running (ollama serve)
# Cloud models work transparently — no pull needed
export USER_SECRET=your-passphrase

./run.sh            # 500 iterations
./run.sh 20         # 20 iterations (test)
./run.sh -i         # interactive REPL
```

### Python SDK showcase
```bash
# Install tokenworm Python SDK
cd /home/dipankar/Github/tokenworm/bindings/python && pip install -e .

# Run the demo (Uses InlineSkill, MCP, native Ollama Cloud API)
cd /home/dipankar/Github/hackmonty
uv run python run.py         # 500 iterations
uv run python run.py 20      # 20 iterations
```

### MCP server (SSE remote mode)
```bash
uv run python -B hackmonty_mcp_server.py --sse --port 8765
```

## Results

- **750+** exploit attempts across 4 orchestrator versions
- **0** sandbox escapes found
- **1 latent unsafe bug** found: `heap_read_boxed` provenance mismatch
- **43 unsafe blocks** audited, **9 GHSA advisories** reviewed, **6 CPython divergences** documented
- **Full report**: [REPORT.md](REPORT.md) | **Bounty submission**: [SUBMISSION.md](SUBMISSION.md)
- **MCP documentation**: [MCP.md](MCP.md)

## Files

| File | Purpose |
|------|---------|
| `run.sh` | Production launcher (tokenworm Zig binary) |
| `run.py` | Python SDK showcase (tokenworm Python SDK) |
| `hackmonty_mcp_server.py` | MCP server — 17 boundary tools |
| `orchestrator.py` | V3 async swarm (standalone, no MCP) |
| `tokenworm/config.json` | Self-contained config (provider, MCP, skills, hooks, sandbox) |
| `skills/` | 4 SKILL.md files (orchestrator, bandit-master, analyst, coder) |
| `program.md` | Agent instructions + attack template documentation |
| `agent.py` | LLM driver (minimax + deepseek-v4-flash for V3) |
| `bandit.py` | UCB1 bandit selection |
| `evaluate.py` | 0-5 scoring + context enrichment |
| `hackmonty_client.py` | hackmonty.com API client (sync + async) |
| `fuzz_snapshots.py` | Snapshot protocol fuzzer (44 tests) |
| `source_scanner.py` | Monty Rust source static analysis |
| `REPORT.md` | 12-section paper-level security assessment |
| `SUBMISSION.md` | Bounty submission (unsafe provenance bug) |
| `MCP.md` | MCP server documentation |

## License

MIT — See [LICENSE](LICENSE)
