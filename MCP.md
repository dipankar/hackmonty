# MCP Server — Boundary Tools for Hack Monty

The MCP server exposes 17 boundary tools that tokenworm uses to interact with
the hackmonty.com sandbox, manage the bandit, and track state.

## Modes

### Stdio (default — used by tokenworm)
```bash
uv run python -B hackmonty_mcp_server.py
```

Tokenworm connects automatically via the `mcp.servers` section in config:
```json
"mcp": {"servers": {"hackmonty": {"command": "uv", "args": [...], "transport": "stdio"}}}
```

### SSE (remote access)
```bash
uv run python -B hackmonty_mcp_server.py --sse --port 8765
```

Connect from tokenworm via SSE transport:
```json
"mcp": {"servers": {"hackmonty-remote": {"url": "https://my-server:8765/sse", "transport": "sse"}}}
```

Or connect via SSE from anywhere that supports MCP SSE clients (Cursor, Zed, etc.):
```json
{"mcpServers": {"hackmonty": {"url": "http://localhost:8765/sse"}}}
```

## Tools (17 total)

### Execution Layer
| Tool | Purpose |
|------|---------|
| `hackmonty_run` | POST Python code to hackmonty.com, handle snapshot/resume |
| `hackmonty_evaluate` | Score a run result 0-5 |
| `hackmonty_revalidate` | Re-run 3x, require >=2/3 output hash match |
| `hackmonty_syntax_check` | Validate Python syntax before running |

### Bandit Layer
| Tool | Purpose |
|------|---------|
| `bandit_select` | Pick next template via UCB1 bandit |
| `bandit_update` | Update bandit stats after attempt |
| `bandit_novelty` | Check code for near-duplicates |
| `bandit_kill` | Kill a template for 25 iterations |
| `bandit_summary` | Get stats for all templates |

### Knowledge Layer
| Tool | Purpose |
|------|---------|
| `notes_history` | Read recent attempt records |
| `attempt_save` | Save attempt to notes directory |
| `state_read` | Read orchestrator state (iteration, scores, bandit) |
| `state_write` | Save orchestrator state for resume |
| `program_read` | Read full attack template documentation |
| `source_scan` | Rust source audit results |
| `github_issues` | Fetch + categorize pydantic/monty issues |
| `findings_read` | Read cumulative findings log |
