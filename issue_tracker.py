"""Fetch GitHub issues for pydantic/monty and related repos via gh CLI.

Categorizes issues into: exploitable, informational, wontfix, stale, resolved.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


REPOS = [
    "pydantic/monty",
    "pydantic/pydantic-ai",
]

ISSUE_LIMIT = 50


@dataclass
class GhIssue:
    number: int
    title: str
    state: str
    created_at: str
    updated_at: str
    closed_at: str | None = None
    labels: list[str] = field(default_factory=list)
    body: str = ""
    state_reason: str | None = None
    url: str = ""

    @property
    def age_days(self) -> float:
        try:
            created = datetime.fromisoformat(self.created_at.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            return (now - created).total_seconds() / 86400
        except Exception:
            return 0

    @property
    def stalled_days(self) -> float:
        try:
            updated = datetime.fromisoformat(self.updated_at.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            return (now - updated).total_seconds() / 86400
        except Exception:
            return 0


@dataclass
class IssueCategory:
    exploitable: list[GhIssue] = field(default_factory=list)
    informational: list[GhIssue] = field(default_factory=list)
    wontfix: list[GhIssue] = field(default_factory=list)
    stale: list[GhIssue] = field(default_factory=list)
    resolved: list[GhIssue] = field(default_factory=list)


EXPLOITABLE_KEYWORDS = [
    "security", "sandbox", "escape", "vulnerability", "race condition",
    "toctou", "use after free", "memory safety", "unsafe", "gc root",
    "type confusion", "privilege", "boundary", "bypass", "overflow",
    "panic", "segfault", "crash", "dos", "denial of service",
    "filesystem", "path traversal", "symlink", "mount",
    "stack overflow", "resource exhaustion",
]

INFORMATIONAL_KEYWORDS = [
    "cpython incompatib", "divergence", "global", "nonlocal",
    "closure", "limitation", "behaviour", "behavior", "error",
    "exception", "traceback", "attribute error", "syntax",
]


def fetch_issues(repo: str) -> list[GhIssue]:
    """Fetch open and recently closed issues from a repo using gh CLI."""
    issues: list[GhIssue] = []

    try:
        open_raw = subprocess.run(
            ["gh", "issue", "list", "-R", repo, "--state", "open",
             "--limit", str(ISSUE_LIMIT),
             "--json", "number,title,state,createdAt,updatedAt,labels,body,url"],
            capture_output=True, text=True, timeout=30,
        )
        if open_raw.returncode == 0:
            for item in json.loads(open_raw.stdout):
                issues.append(GhIssue(
                    number=item["number"],
                    title=item["title"],
                    state="open",
                    created_at=item.get("createdAt", ""),
                    updated_at=item.get("updatedAt", ""),
                    labels=[l["name"] for l in item.get("labels", [])],
                    body=item.get("body", ""),
                    url=item.get("url", ""),
                ))
    except Exception as e:
        print(f"  [WARN] Failed to fetch open issues for {repo}: {e}", file=sys.stderr)

    try:
        closed_raw = subprocess.run(
            ["gh", "issue", "list", "-R", repo, "--state", "closed",
             "--limit", str(ISSUE_LIMIT // 2),
             "--json", "number,title,state,createdAt,closedAt,labels,body,url,stateReason"],
            capture_output=True, text=True, timeout=30,
        )
        if closed_raw.returncode == 0:
            for item in json.loads(closed_raw.stdout):
                issues.append(GhIssue(
                    number=item["number"],
                    title=item["title"],
                    state="closed",
                    created_at=item.get("createdAt", ""),
                    updated_at=item.get("closedAt", item.get("createdAt", "")),
                    closed_at=item.get("closedAt"),
                    labels=[l["name"] for l in item.get("labels", [])],
                    body=item.get("body", ""),
                    url=item.get("url", ""),
                    state_reason=item.get("stateReason"),
                ))
    except Exception as e:
        print(f"  [WARN] Failed to fetch closed issues for {repo}: {e}", file=sys.stderr)

    return issues


def categorize_issues(issues: list[GhIssue]) -> IssueCategory:
    """Categorize issues by exploitability and relevance."""
    cat = IssueCategory()

    for issue in issues:
        text = f"{issue.title} {issue.body}".lower()
        labels_lower = [l.lower() for l in issue.labels]

        if issue.state == "closed" and issue.state_reason == "COMPLETED":
            cat.resolved.append(issue)
            continue

        if issue.state == "closed" and issue.state_reason == "NOT_PLANNED":
            cat.wontfix.append(issue)
            continue

        if issue.stalled_days > 90:
            cat.stale.append(issue)
            continue

        if any(kw in text for kw in EXPLOITABLE_KEYWORDS):
            cat.exploitable.append(issue)
        elif any(kw in text for kw in INFORMATIONAL_KEYWORDS):
            cat.informational.append(issue)
        elif any(kw in labels_lower for kw in ("bug", "security")):
            cat.exploitable.append(issue)
        else:
            cat.informational.append(issue)

    return cat


def fetch_and_categorize(notes_dir: Path) -> dict[str, IssueCategory]:
    """Fetch issues from all tracked repos and categorize them."""
    results: dict[str, IssueCategory] = {}

    for repo in REPOS:
        print(f"  Fetching issues from {repo}...")
        issues = fetch_issues(repo)
        cat = categorize_issues(issues)
        results[repo] = cat

        print(f"    Total: {len(issues)}, "
              f"Exploitable: {len(cat.exploitable)}, "
              f"Informational: {len(cat.informational)}, "
              f"Wontfix: {len(cat.wontfix)}, "
              f"Stale: {len(cat.stale)}, "
              f"Resolved: {len(cat.resolved)}")

    return results


def save_issues_snapshot(results: dict[str, IssueCategory], notes_dir: Path):
    """Save issue data to notes directory."""
    issues_dir = notes_dir / "issues"
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")

    data = {}
    for repo, cat in results.items():
        data[repo] = {
            "fetched_at": timestamp,
            "exploitable": [_issue_to_dict(i) for i in cat.exploitable],
            "informational": [_issue_to_dict(i) for i in cat.informational],
            "wontfix": [_issue_to_dict(i) for i in cat.wontfix],
            "stale": [_issue_to_dict(i) for i in cat.stale],
            "resolved": [_issue_to_dict(i) for i in cat.resolved],
        }

    snapshot_path = issues_dir / f"issues_{timestamp}.json"
    snapshot_path.write_text(json.dumps(data, indent=2))

    latest_path = issues_dir / "latest_issues.json"
    latest_path.write_text(json.dumps(data, indent=2))

    return data


def _issue_to_dict(issue: GhIssue) -> dict:
    return {
        "number": issue.number,
        "title": issue.title,
        "state": issue.state,
        "created_at": issue.created_at,
        "updated_at": issue.updated_at,
        "closed_at": issue.closed_at,
        "labels": issue.labels,
        "url": issue.url,
        "age_days": round(issue.age_days, 1),
        "stalled_days": round(issue.stalled_days, 1),
    }


def _issue_list_text(issues: list[dict | GhIssue], prefix: str = "") -> str:
    """Format a list of issues (dict or GhIssue) as text lines."""
    lines = []
    for i in issues:
        if isinstance(i, GhIssue):
            lines.append(f"{prefix}#{i.number}: {i.title} (age={i.age_days:.0f}d)")
        else:
            lines.append(f"{prefix}#{i.get('number','?')}: {i.get('title','?')} (age={i.get('age_days',0):.0f}d)")
    return "\n".join(lines)


def format_issues_for_agent(results: dict[str, IssueCategory | dict]) -> str:
    """Format issues as a concise text block for the agent's context.
    Accepts either IssueCategory objects or plain dicts from saved JSON snapshots.
    """
    lines = ["## Current GitHub Issues\n"]

    for repo, cat in results.items():
        lines.append(f"### {repo}\n")

        if isinstance(cat, IssueCategory):
            exploitable = cat.exploitable
            wontfix = cat.wontfix
            stale = cat.stale
            resolved = cat.resolved
        else:
            exploitable = cat.get("exploitable", [])
            wontfix = cat.get("wontfix", [])
            stale = cat.get("stale", [])
            resolved = cat.get("resolved", [])

        if exploitable:
            lines.append("**Exploitable (high priority):**")
            lines.append(_issue_list_text(exploitable, "  - "))
            lines.append("")

        if wontfix:
            lines.append("**Wontfix (persistent weakness vectors):**")
            lines.append(_issue_list_text(wontfix, "  - "))
            lines.append("")

        if stale:
            lines.append("**Stale (open >90d, likely unfixed):**")
            lines.append(_issue_list_text(stale, "  - "))
            lines.append("")

        if resolved:
            lines.append("**Recently Resolved (study the fix):**")
            for i in resolved[:5]:
                if isinstance(i, GhIssue):
                    lines.append(f"  - #{i.number}: {i.title}")
                else:
                    lines.append(f"  - #{i.get('number','?')}: {i.get('title','?')}")
            lines.append("")

    return "\n".join(lines)


def main():
    notes_dir = Path(__file__).parent / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    (notes_dir / "issues").mkdir(exist_ok=True)

    print("Fetching GitHub issues...")
    results = fetch_and_categorize(notes_dir)
    save_issues_snapshot(results, notes_dir)

    print("\n" + format_issues_for_agent(results))


if __name__ == "__main__":
    main()
