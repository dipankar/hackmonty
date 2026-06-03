"""LLM agent driver for the hacking loop — supports analyst/coder role split."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any


OLLAMA_HOST = "https://ollama.com"
MODEL = "qwen3.5:cloud"


@dataclass
class AgentResponse:
    exploit_code: str = ""
    reasoning: str = ""
    focus_area: str = ""

    # Analyst-specific
    chosen_template: str = ""
    strategy: str = ""
    confidence: str = ""

    # Meta-review
    assessment: str = ""
    suggested_changes: str = ""


class Agent:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("OLLAMA_API_KEY", "")
        if not self.api_key:
            raise RuntimeError("OLLAMA_API_KEY not set.")

        from ollama import Client
        self.client = Client(
            host=OLLAMA_HOST,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )

    def _call(self, system: str, user: str, temperature: float = 0.7) -> str:
        try:
            response = self.client.chat(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                options={"temperature": temperature, "num_predict": 2048},
            )
            return response.message.content
        except Exception as e:
            return f"API_ERROR: {e}"

    def analyst(self, system_prompt: str, history: str) -> AgentResponse:
        """Analyst role: review history, pick best attack template, write strategy."""
        user = f"""## Recent Attempt History
{history}

## Your Task
Analyze the last batch of results. Choose ONE attack template (A-H) from the program.
Write a 3-sentence strategy for the next exploit.
Output in this format:

TEMPLATE: [letter]
REASON: [why this template, why now]
STRATEGY: [precise 3-sentence exploitation plan]"""

        raw = self._call(system_prompt, user, temperature=0.4)

        resp = AgentResponse()
        resp.raw_response = raw
        resp.chosen_template = _extract_field(raw, "TEMPLATE")
        resp.reasoning = _extract_field(raw, "REASON")
        resp.strategy = _extract_field(raw, "STRATEGY")

        template_map = {"A": "DictReentry", "B": "SetReentry", "C": "SortCmp",
                         "D": "MinMaxMutate", "E": "MemDrift", "F": "ConfigFiles",
                         "G": "AllocRace", "H": "AsyncGC"}
        resp.focus_area = template_map.get(resp.chosen_template[:1].upper(), "Exploration")

        return resp

    def coder(self, system_prompt: str, template: str, strategy: str) -> AgentResponse:
        """Coder role: given a template + strategy, generate exploit code."""
        user = f"""## Selected Template: {template}
## Strategy: {strategy}

Generate the Python exploit code for this template. Output ONLY a ```python block.
Keep code under 80 lines. Use concise print() for output.
Do NOT use: class, del, yield, os.listdir, __builtins__, dir().
Do NOT just probe paths — use the template's SPECIFIC vulnerability pattern."""

        raw = self._call(system_prompt, user, temperature=0.8)

        resp = AgentResponse()
        resp.raw_response = raw
        resp.exploit_code = _extract_code(raw)
        resp.focus_area = template
        resp.strategy = strategy
        return resp

    def meta_review(self, attempts_summary: str, score_counts: dict) -> AgentResponse:
        """After each batch: review progress and suggest changes."""
        system = "You are a meta-analyst. Review the last batch of hacking attempts and suggest improvements."
        user = f"""## Batch Results
{attempts_summary}

## Score Distribution
{json.dumps(score_counts)}

## Your Task
1. ASSESSMENT: What patterns are working? What's dead?
2. DEAD_TEMPLATES: Which templates should be deprioritized? (list letters)
3. SUGGESTION: What should the next batch focus on?"""

        raw = self._call(system, user, temperature=0.3)

        resp = AgentResponse()
        resp.raw_response = raw
        resp.assessment = _extract_field(raw, "ASSESSMENT")
        resp.suggested_changes = _extract_field(raw, "SUGGESTION")

        dead = _extract_field(raw, "DEAD_TEMPLATES")
        resp.confidence = dead
        return resp


def _extract_code(raw: str) -> str:
    """Extract Python code from LLM response."""
    match = re.search(r"```(?:python)?\s*\n(.*?)```", raw, re.DOTALL)
    if match:
        return match.group(1).strip()

    lines = []
    in_code = False
    for line in raw.split("\n"):
        stripped = line.strip()
        if stripped.startswith(("import ", "from ", "def ", "try:", "print(", "#!")):
            in_code = True
        elif stripped.startswith("```"):
            continue
        if in_code and stripped:
            lines.append(line)
    return "\n".join(lines).strip() if lines else raw.strip()


def _extract_field(raw: str, field: str) -> str:
    """Extract a labeled field from raw text."""
    for pattern in [f"{field}:", f"{field.upper()}:", f"**{field}**"]:
        match = re.search(
            rf"{re.escape(pattern)}\s*(.+?)(?:\n\s*\n|\n\s*[A-Z]{{2,}}:|\Z)",
            raw, re.DOTALL | re.IGNORECASE
        )
        if match:
            return match.group(1).strip()[:500]
    return ""
