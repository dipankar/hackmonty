"""UCB1 bandit for template selection + novelty tracking.

Replaces LLM-based template selection with mathematically-grounded
exploration/exploitation balance. Penalizes near-duplicate exploit code.

Usage:
    bandit = Bandit(templates=TEMPLATES)
    template = bandit.select()         # Pick best template
    bandit.update(template, score)     # Update with result
    novelty = bandit.check_novelty(code)  # Check for duplicates
"""

from __future__ import annotations

import math
import hashlib


class Bandit:
    def __init__(self, templates: list[tuple[str, str, str]]):
        self.templates = templates
        self.stats: dict[str, dict] = {}
        for letter, name, desc in templates:
            self.stats[letter] = {
                "name": name,
                "desc": desc,
                "attempts": 0,
                "total_score": 0.0,
                "zero_streak": 0,
                "dead_until": 0,  # iteration # until which template is dead
            }
        self.total_attempts = 0
        self.code_hashes: dict[str, int] = {}
        self.ZERO_LIMIT = 10
        self.DEAD_COOLDOWN = 25
        self._explore_idx = 0  # round-robin for unexplored templates

    def select(self) -> tuple[str, str]:
        live = [l for l, s in self.stats.items()
                if s["dead_until"] <= self.total_attempts]

        # Round-robin through unexplored templates first
        unexplored = [l for l in live if self.stats[l]["attempts"] == 0]
        if unexplored:
            idx = self._explore_idx % len(unexplored)
            self._explore_idx += 1
            return unexplored[idx], self.stats[unexplored[idx]]["name"]

        # UCB1 bandit for explored templates
        best_ucb = -1.0
        best_letter = None

        for letter, s in self.stats.items():
            if s["dead_until"] > self.total_attempts:
                continue
            if s["attempts"] == 0:
                continue  # Already handled above

            mean = s["total_score"] / s["attempts"]
            exploration = math.sqrt(
                2.0 * math.log(max(1, self.total_attempts)) / s["attempts"]
            )
            ucb = mean + exploration
            if ucb > best_ucb:
                best_ucb = ucb
                best_letter = letter

        if best_letter is None:
            best_letter = self.templates[0][0]
        return best_letter, self.stats[best_letter]["name"]

    def update(self, template: str, score: float):
        s = self.stats.get(template)
        if not s:
            return
        s["attempts"] += 1
        s["total_score"] += score

        if score == 0:
            s["zero_streak"] += 1
            if s["zero_streak"] >= self.ZERO_LIMIT:
                s["dead_until"] = self.total_attempts + self.DEAD_COOLDOWN
                s["zero_streak"] = 0
        else:
            s["zero_streak"] = 0

        self.total_attempts += 1

    def check_novelty(self, code: str) -> float:
        h = self._norm_hash(code)
        count = self.code_hashes.get(h, 0)
        self.code_hashes[h] = count + 1
        penalty = 1.0 / (1.0 + count * 0.7)
        if len(self.code_hashes) % 50 == 0:
            self._prune_cache()
        return penalty

    def kill_template(self, letter: str):
        s = self.stats.get(letter)
        if s:
            s["dead_until"] = self.total_attempts + self.DEAD_COOLDOWN

    def live_templates(self) -> list[str]:
        return [l for l, s in self.stats.items()
                if s["dead_until"] <= self.total_attempts]

    def summary(self) -> str:
        lines = []
        for l, s in sorted(self.stats.items(),
                           key=lambda x: x[1]["total_score"] / max(1, x[1]["attempts"]),
                           reverse=True):
            mean = s["total_score"] / max(1, s["attempts"])
            dead = " 💀" if s["dead_until"] > self.total_attempts else ""
            lines.append(
                f"  {l}: {s['attempts']:3d} attempts, "
                f"mean={mean:.2f}, zero_streak={s['zero_streak']}{dead}"
            )
        return "\n".join(lines)

    def _norm_hash(self, code: str) -> str:
        lines = sorted(
            l.strip() for l in code.split("\n")
            if l.strip() and not l.strip().startswith("#")
        )
        return hashlib.blake2b("\n".join(lines).encode()).hexdigest()[:12]

    def _prune_cache(self):
        if len(self.code_hashes) > 500:
            items = sorted(self.code_hashes.items(), key=lambda x: x[1])
            self.code_hashes = dict(items[-400:])
