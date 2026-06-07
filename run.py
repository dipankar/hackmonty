#!/usr/bin/env python3
"""Hack Monty — Python SDK Showcase with Sub-Agents

Uses the tokenworm Python SDK with:
  - Sub-agents registered from skill `agent:` frontmatter
  - MCP boundary tools (stdin/stdout to hackmonty_mcp_server.py)
  - Local ollama daemon with cloud model proxy
  - Progress hooks for CLI logging

Sub-agents: bandit-master (bandit tools), analyst (history+strategy), coder (code+syntax)
Parent agent: orchestrator — spawns sub-agents, runs code, evaluates, saves

Usage:
  uv run python run.py [max_iterations]
"""

import asyncio, os, sys, json, re, yaml
from pathlib import Path
from tokenworm import Agent, InlineSkill, SubagentDef
from tokenworm import (
    IterationStartEvent, ToolCallEvent, TextEvent, SubagentStartEvent,
    SubagentEndEvent, SubagentTextEvent,
    DoneEvent, ErrorEvent, CompactionEvent,
)

WORKSPACE = Path(__file__).parent
SKILLS_DIR = WORKSPACE / "skills"

def parse_skill(path: Path) -> dict:
    """Parse SKILL.md YAML frontmatter + body."""
    text = path.read_text()
    if not text.startswith("---"):
        return {"body": text, "frontmatter": {}}
    parts = text.split("---", 2)
    frontmatter = yaml.safe_load(parts[1]) if parts[1].strip() else {}
    body = parts[2].strip() if len(parts) > 2 else ""
    return {"frontmatter": frontmatter, "body": body}


def load_subagents() -> tuple[list[SubagentDef], list[InlineSkill], str]:
    """Load skills from filesystem. Skills with agent: become sub-agents.
    Returns (subagents, inline_skills, orchestrator_body)."""
    subagents = []
    inline_skills = []
    orchestrator_body = ""

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_path = skill_dir / "SKILL.md"
        if not skill_path.exists():
            continue

        parsed = parse_skill(skill_path)
        fm = parsed.get("frontmatter", {})
        body = parsed.get("body", "")
        name = fm.get("name", skill_dir.name)
        desc = fm.get("description", name)
        agent = fm.get("agent")
        allowed = fm.get("allowed-tools", [])
        if isinstance(allowed, str):
            allowed = allowed.split()

        if name == "orchestrator":
            orchestrator_body = body
        elif agent:
            # This is a sub-agent
            subagents.append(SubagentDef(
                name=agent,
                description=desc,
                prompt=body,
                allowed_tools=allowed,
            ))
            print(f"  [subagent] {agent}: {' '.join(allowed)[:80]}...")

    # Orchestrator as inline auto-include skill
    if orchestrator_body:
        inline_skills.append(InlineSkill(
            name="orchestrator",
            description="Drive the autonomous hackmonty.com security assessment loop",
            content=orchestrator_body,
            auto_include=True,
        ))

    return subagents, inline_skills, orchestrator_body


def main():
    subagents, inline_skills, _ = load_subagents()
    print(f"  Sub-agents: {len(subagents)} | Inline skills: {len(inline_skills)}")

    agent = Agent(
        provider="ollama",
        model="qwen3.5:cloud",
        api_key=os.environ.get("OLLAMA_API_KEY", ""),
        workspace=str(WORKSPACE),
        max_iterations=int(sys.argv[1]) if len(sys.argv) > 1 else 500,
        ask_approval="never",

        # Sub-agents from skill frontmatter
        subagents=subagents,
        max_subagent_depth=2,

        # Inline skills (orchestrator) + filesystem backup
        skills=inline_skills,
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

        hooks={
            "on_iteration_start": "echo '{\"iter\": $ITERATION}'",
            "on_subagent_start": "echo '{\"subagent\": \"$SUBAGENT_NAME\", \"parent\": $PARENT_ID}'",
            "on_tool_call_complete": "echo '{\"tool\": \"$TOOL_NAME\", \"ms\": $DURATION_MS}'",
        },

        sandbox={"enabled": True, "network": True},
    )

    async def stream():
        async for event in agent.run("/orchestrator"):
            if isinstance(event, IterationStartEvent):
                print(f"\n--- #{event.iteration} ---", flush=True)
            elif isinstance(event, SubagentStartEvent):
                print(f"  [sub:{event.name}]", flush=True)
            elif isinstance(event, SubagentTextEvent):
                print(f"  {str(event).strip()[:120]}", flush=True)
            elif isinstance(event, ToolCallEvent):
                short = event.name.split(":")[-1]
                print(f"  [{short}]", flush=True)
            elif isinstance(event, TextEvent):
                print(str(event), end="", flush=True)
            elif isinstance(event, CompactionEvent):
                print(f"  [compacted {event.old_count}->{event.new_count}]", flush=True)
            elif isinstance(event, ErrorEvent):
                print(f"\n  ERROR: {event.message}")
                break
            elif isinstance(event, DoneEvent):
                print("\nDone.")
        agent.close()

    asyncio.run(stream())


if __name__ == "__main__":
    main()
