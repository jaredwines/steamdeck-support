#!/usr/bin/env python3
"""Check SS compatibility records for parseable and reviewable dates."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATE_ROW = re.compile(r"^\|\s*(20\d{2}-\d{2}-\d{2})\s*\|", re.MULTILINE)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", type=dt.date.fromisoformat, default=dt.date.today())
    parser.add_argument("--max-age-days", type=int, default=180)
    args = parser.parse_args()
    failures: list[str] = []
    warnings: list[str] = []
    checked = 0

    for path in sorted((ROOT / "runbooks").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if "## Compatibility record" not in text:
            continue
        checked += 1
        section = text.split("## Compatibility record", 1)[1]
        dates = [dt.date.fromisoformat(value) for value in DATE_ROW.findall(section)]
        if not dates:
            failures.append(f"{path.relative_to(ROOT)}: compatibility record has no dated row")
            continue
        newest = max(dates)
        if newest > args.as_of:
            failures.append(f"{path.relative_to(ROOT)}: review date {newest} is in the future")
        age = (args.as_of - newest).days
        if age > args.max_age_days:
            warnings.append(f"{path.relative_to(ROOT)}: newest evidence is {age} days old")

    dashboard = ROOT / "runbooks" / "compatibility-status.md"
    dashboard_text = dashboard.read_text(encoding="utf-8") if dashboard.exists() else ""
    if "## Current evidence" not in dashboard_text or "## Evidence ladder" not in dashboard_text:
        failures.append("runbooks/compatibility-status.md: incomplete dashboard")

    for warning in warnings:
        print(f"REVIEW: {warning}", file=sys.stderr)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print(f"Compatibility status validation passed ({checked} dated records, {len(warnings)} review warning(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
