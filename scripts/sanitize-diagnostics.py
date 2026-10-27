#!/usr/bin/env python3
"""Redact common sensitive fields from SS diagnostic text.

This is a conservative convenience filter, not a guarantee that output is safe.
The operator must still review the result before sharing it.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


RULES = (
    (re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?"), "<ip-address>"),
    (re.compile(r"(?i)(?<![0-9a-f])(?:[0-9a-f]{2}:){5}[0-9a-f]{2}(?![0-9a-f])"), "<mac-address>"),
    (
        re.compile(
            r"(?<![\w:])(?=[0-9A-Fa-f:]*:[0-9A-Fa-f:]*:)"
            r"[0-9A-Fa-f:]+(?:/\d{1,3})?(?![\w:])"
        ),
        "<ip-address-v6>",
    ),
    (re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"), "<uuid>"),
    (re.compile(r"(?<![\w/])/home/(?!deck(?:/|\b))[^/\s]+"), "/home/<user>"),
    (
        re.compile(r"(?im)^(\s*(?:ssid|hostname|serial)\s*[:=]\s*).+$"),
        r"\1<redacted>",
    ),
    (re.compile(r"\b(?:github_pat_[A-Za-z0-9_]+|gh[opurs]_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,})\b"), "<token>"),
)


def sanitize(text: str) -> str:
    for pattern, replacement in RULES:
        text = pattern.sub(replacement, text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Redact common sensitive fields; always review output manually."
    )
    parser.add_argument("path", nargs="?", type=Path, help="input file; default: stdin")
    args = parser.parse_args()
    source = args.path.read_text(encoding="utf-8") if args.path else sys.stdin.read()
    sys.stdout.write(sanitize(source))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
