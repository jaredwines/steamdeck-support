#!/usr/bin/env python3
"""Create a compact, content-free summary of SS collector output."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PROFILE = re.compile(r"^# Profile: (.+)$", re.MULTILINE)
SECTION = re.compile(r"^## (.+)$", re.MULTILINE)
UNAVAILABLE = "[command unavailable or returned a non-zero status]"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize collector coverage without copying diagnostic values."
    )
    parser.add_argument("path", nargs="?", type=Path, help="collector output; default: stdin")
    args = parser.parse_args()
    text = args.path.read_text(encoding="utf-8") if args.path else sys.stdin.read()
    if "# SS read-only diagnostic collection" not in text:
        print("Input is not recognized as SS collector output.", file=sys.stderr)
        return 2
    profiles = list(dict.fromkeys(PROFILE.findall(text)))
    sections = SECTION.findall(text)
    unavailable = text.count(UNAVAILABLE)
    print("SS diagnostic session summary")
    print(f"Profiles: {', '.join(profiles)}")
    print(f"Command sections: {len(sections)}")
    print(f"Unavailable or non-zero commands: {unavailable}")
    print("Review status: manual privacy review still required before sharing details")
    return 1 if unavailable else 0


if __name__ == "__main__":
    raise SystemExit(main())
