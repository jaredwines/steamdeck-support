#!/usr/bin/env python3
"""Validate the SS acceptance scenario catalog."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "runbooks" / "scenario-catalog.md"
ROW = re.compile(
    r"^\| (S\d{2}) \| (.+?) \| \[([^]]+)\]\(([^)]+)\) \| (.+?) \|$",
    re.MULTILINE,
)


def main() -> int:
    text = CATALOG.read_text(encoding="utf-8")
    rows = ROW.findall(text)
    failures: list[str] = []
    expected = [f"S{number:02d}" for number in range(1, 21)]
    actual = [row[0] for row in rows]
    if actual != expected:
        failures.append(f"expected scenario IDs {expected}, found {actual}")
    for scenario_id, symptom, _label, target, outcome in rows:
        resolved = CATALOG.parent / target.split("#", 1)[0]
        if not resolved.is_file():
            failures.append(f"{scenario_id}: missing route target {target}")
        if len(symptom.split()) < 4:
            failures.append(f"{scenario_id}: symptom is not descriptive")
        if len(outcome.split()) < 6:
            failures.append(f"{scenario_id}: successful outcome is not testable enough")
    for required in ("Maximum score: 200", "190 or higher", "critical safety"):
        if required not in text:
            failures.append(f"catalog is missing acceptance rule: {required}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("Scenario coverage validation passed (20 ordered scenarios).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
