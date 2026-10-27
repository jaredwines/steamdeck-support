#!/usr/bin/env python3
"""Validate the minimum operational structure of SS runbooks."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RUNBOOKS = ROOT / "runbooks"
EXCLUDED = {
    "README.md",
    "index.md",
    "compatibility-status.md",
    "coverage-matrix.md",
    "readiness-scorecard.md",
    "scenario-catalog.md",
    "support-session-record-template.md",
}
COMPATIBILITY_EXEMPT = {"support-session.md", "verification.md", "triage.md"}


def has_heading(text: str, words: tuple[str, ...]) -> bool:
    headings = re.findall(r"^## (.+)$", text, flags=re.MULTILINE)
    return any(any(word in heading.lower() for word in words) for heading in headings)


def main() -> int:
    failures: list[str] = []
    files = sorted(path for path in RUNBOOKS.glob("*.md") if path.name not in EXCLUDED)
    for path in files:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        if len(re.findall(r"^# ", text, flags=re.MULTILINE)) != 1:
            failures.append(f"{relative}: expected exactly one level-one heading")
        if not has_heading(text, ("purpose",)):
            failures.append(f"{relative}: missing purpose section")
        if not has_heading(text, ("approval", "authority", "before making", "before using")):
            failures.append(f"{relative}: missing approval/prerequisite section")
        if not has_heading(text, ("verification", "verify and hand off", "evidence required")):
            failures.append(f"{relative}: missing verification section")
        if not has_heading(text, ("quick path", "thirty-second route")):
            failures.append(f"{relative}: missing quick operational summary")
        if path.name not in COMPATIBILITY_EXEMPT and "## Compatibility record" not in text:
            failures.append(f"{relative}: missing compatibility record")
        if "sudo " in text and "approval" not in text.lower():
            failures.append(f"{relative}: contains sudo without an approval boundary")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print(f"Runbook structure validation passed ({len(files)} operational runbooks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
