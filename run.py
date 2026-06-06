#!/usr/bin/env python3
"""Hack Monty — Python SDK Showcase

Uses the tokenworm Python SDK to drive the autonomous security assessment loop.
Demonstrates:
  - Native Ollama Cloud API (ollama_native provider)
  - Inline skills + filesystem skills
  - MCP boundary tools (stdin/stdout to hackmonty_mcp_server.py)
  - Progress hooks for CLI logging
  - Streaming events with readable output

For production overnight runs, use:  ./run.sh 500
For interactive REPL mode:          ./run.sh --interactive

Usage:
  uv run python run.py [max_iterations]
"""

import asyncio, os, sys, json
from pathlib import Path

from tokenworm import Agent, InlineSkill
from tokenworm import (
    IterationStartEvent, ToolCallEvent, TextEvent,
    DoneEvent, ErrorEvent, CompactionEvent,
)

WORKSPACE = Path(__file__).parent
SKILLS_DIR = WORKSPACE / "skills"

def load_skill_body(name: str) -> str:
    """Read a SKILL.md from the skills directory, stripping YAML frontmatter."""
    path = SKILLS_DIR / name / "SKILL.md"
    if not path.exists():
        return ""
    text = path.read_text()
    if text.startswith("---"):
        parts = text.split("---", 2)
        return parts[2].strip() if len(parts) > 2 else text
    return text

def main():
    orchestrator_content = load_skill_body("orchestrator")

    agent = Agent(
        provider="ollama",
        model="qwen3.5:cloud",
        api_key=os.environ.get("OLLAMA_API_KEY", ""),
        workspace=str(WORKSPACE),
        max_iterations=int(sys.argv[1]) if len(sys.argv) > 1 else 500,
        ask_approval="never",

        # Inline skills + filesystem skills
        skills=[InlineSkill(
            name="orchestrator",
            description="Drive the autonomous hackmonty.com security assessment loop",
            content=orchestrator_content,
            auto_include=True,
        )] if orchestrator_content else [],
        skill_dirs=[str(SKILLS_DIR)],

        # MCP boundary tools
        mcp_servers={
            "hackmonty": {
                "command": "uv",
                "args": ["run", "python", "-B",
                         str(WORKSPACE / "hackmonty_mcp_server.py")],
                "transport": "stdio",
                "auto_start": True,
                "timeout_ms": 120000,
            }
        },

        # Progress logging hooks
        hooks={
            "on_iteration_start": "echo '{\"iter\": $ITERATION}'",
            "on_tool_call_complete": "echo '{\"tool\": \"$TOOL_NAME\", \"ms\": $DURATION_MS}'",
        },

        sandbox={"enabled": True, "network": True},
    )

    async def stream():
        async for event in agent.run("/orchestrator"):
            if isinstance(event, IterationStartEvent):
                print(f"\n--- #{event.iteration} ---", flush=True)
            elif isinstance(event, ToolCallEvent):
                short_name = event.name.split(":")[-1]
                print(f"  [{short_name}]", flush=True)
            elif isinstance(event, TextEvent):
                print(str(event), end="", flush=True)
            elif isinstance(event, CompactionEvent):
                print(f"  [compacted {event.old_count} -> {event.new_count} msgs]", flush=True)
            elif isinstance(event, ErrorEvent):
                print(f"\n  ERROR (code={event.code}): {event.message}")
                break
            elif isinstance(event, DoneEvent):
                print("\n\nDone.")
        agent.close()

    asyncio.run(stream())

if __name__ == "__main__":
    main()
