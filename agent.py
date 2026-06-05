"""LLM agent driver — async with Ollama Cloud API.

Supports analyst (strategy), coder (exploit generation), and meta_review roles.
All Ollama calls are wrapped in asyncio.to_thread for non-blocking concurrency.

Models:
  ANALYST_MODEL = "minimax-m3:cloud"     — strategy & meta-review (reasoning)
  CODER_MODEL   = "kimi-k2.6:cloud"     — exploit code generation
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import hashlib
from dataclasses import dataclass, field
from typing import Any


OLLAMA_HOST = "https://ollama.com"
ANALYST_MODEL = "minimax-m3:cloud"
CODER_MODEL   = "kimi-k2.6:cloud"


@dataclass
class AgentResponse:
    exploit_code: str = ""
    reasoning: str = ""
    focus_area: str = ""
    chosen_template: str = ""
    strategy: str = ""
    raw_response: str = ""

    # Meta-review
    assessment: str = ""
    suggested_changes: str = ""
    confidence: str = ""


class Agent:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("OLLAMA_API_KEY", "")
        if not self.api_key:
            raise RuntimeError("OLLAMA_API_KEY not set.")

        from ollama import Client
        self._client = Client(
            host=OLLAMA_HOST,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )

    def _call_sync(self, system: str, user: str, temperature: float = 0.7,
                   model: str | None = None, num_predict: int = 2048) -> str:
        effective_model = model or ANALYST_MODEL
        try:
            response = self._client.chat(
                model=effective_model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                options={"temperature": temperature, "num_predict": num_predict},
            )
            msg = response.message
            result = msg.content or ""
            if not result and hasattr(msg, "thinking") and msg.thinking:
                result = msg.thinking
            # For coder with thinking models: strip excessive reasoning, keep code blocks
            if effective_model == CODER_MODEL and len(result) > 2000 and '```' in result:
                blocks = re.findall(r'```(?:python)?\s*\n(.*?)```', result, re.DOTALL)
                if blocks:
                    result = '\n'.join(b.strip() for b in blocks if b.strip())
            return result
        except Exception as e:
            return f"API_ERROR: {e}"

    async def _call(self, system: str, user: str, temperature: float = 0.7,
                    model: str | None = None, num_predict: int = 2048) -> str:
        return await asyncio.to_thread(self._call_sync, system, user, temperature,
                                       model, num_predict)

    async def analyst(self, system_prompt: str, history: str) -> AgentResponse:
        user = f"""## Recent Attempt History
{history}

## Your Task
Analyze the results. Pick ONE attack template (A-H for sandbox, I-K for protocol).
Write a 3-sentence strategy. Output in this format:

TEMPLATE: [letter]
REASON: [why this template now]
STRATEGY: [precise 3-sentence exploitation plan]"""

        raw = await self._call(system_prompt, user, temperature=0.4)

        resp = AgentResponse()
        resp.raw_response = raw
        resp.chosen_template = _extract_field(raw, "TEMPLATE")
        resp.reasoning = _extract_field(raw, "REASON")
        resp.strategy = _extract_field(raw, "STRATEGY")

        template_map = {
            "A": "DictReentry", "B": "SetReentry", "C": "SortCmp",
            "D": "MinMaxMutate", "E": "MemDrift", "F": "ConfigFiles",
            "G": "AllocRace", "H": "AsyncGC",
            "I": "NameLookup", "J": "FutureChain", "K": "DoubleResume",
        }
        resp.focus_area = template_map.get(resp.chosen_template[:1].upper(), "Exploration")

        return resp

    async def coder(self, system_prompt: str, template: str, strategy: str) -> AgentResponse:
        user = f"""## Selected Template: {template}
## Strategy: {strategy}

Generate Python exploit code. Output ONLY a ```python block. No thinking, no reasoning, just the code block.
Under 80 lines. Do NOT use: class, del, yield, os.listdir, __builtins__, dir().
Focus on the SPECIFIC vulnerability pattern."""

        raw = await self._call(system_prompt, user, temperature=0.3, model=CODER_MODEL,
                               num_predict=1024)

        resp = AgentResponse()
        resp.raw_response = raw
        resp.exploit_code = _extract_code(raw)
        resp.focus_area = template
        resp.strategy = strategy
        return resp

    async def meta_review(self, attempts_summary: str, score_counts: dict) -> AgentResponse:
        system = "You are a meta-analyst reviewing a batch of hacking attempts."
        user = f"""## Batch Results
{attempts_summary}

## Score Distribution
{json.dumps(score_counts)}

## Your Task
1. ASSESSMENT: What's working? What's dead?
2. DEAD_TEMPLATES: Which templates should be deprioritized? (list letters)
3. SUGGESTION: What should the next batch focus on?"""

        raw = await self._call(system, user, temperature=0.3)

        resp = AgentResponse()
        resp.raw_response = raw
        resp.assessment = _extract_field(raw, "ASSESSMENT")
        resp.suggested_changes = _extract_field(raw, "SUGGESTION")
        resp.confidence = _extract_field(raw, "DEAD_TEMPLATES")
        return resp


def _extract_code(raw: str) -> str:
    match = re.search(r"```(?:python)?\s*\n(.*?)```", raw, re.DOTALL)
    if match:
        return match.group(1).strip()
    lines = []
    in_code = False
    for line in raw.split("\n"):
        s = line.strip()
        if s.startswith(("import ", "from ", "def ", "try:", "print(", "async ", "await ")):
            in_code = True
        elif s.startswith("```"):
            continue
        if in_code and s:
            lines.append(line)
    return "\n".join(lines).strip() if lines else raw.strip()


def _extract_field(raw: str, field: str) -> str:
    for pat in [f"{field}:", f"{field.upper()}:", f"**{field}**"]:
        match = re.search(
            rf"{re.escape(pat)}\s*(.+?)(?:\n\s*\n|\n\s*[A-Z]{{2,}}:|\Z)",
            raw, re.DOTALL | re.IGNORECASE
        )
        if match:
            return match.group(1).strip()[:500]
    return ""


def code_hash(code: str) -> str:
    return hashlib.blake2b(code.encode()).hexdigest()[:16]
