#!/usr/bin/env python3
"""Validate local Markdown link targets and simple heading fragments."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


def link_targets(text: str) -> list[str]:
    targets: list[str] = []
    position = 0
    while True:
        start = text.find("](", position)
        if start < 0:
            return targets
        cursor = start + 2
        depth = 0
        escaped = False
        while cursor < len(text):
            character = text[cursor]
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == "(":
                depth += 1
            elif character == ")":
                if depth == 0:
                    targets.append(text[start + 2 : cursor])
                    position = cursor + 1
                    break
                depth -= 1
            cursor += 1
        else:
            position = start + 2


def heading_slugs(path: Path) -> set[str]:
    slugs: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        heading = re.sub(r"<[^>]*>", "", match.group(1)).lower()
        heading = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE)
        slug = re.sub(r"\s+", "-", heading.strip())
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        slugs.add(slug if count == 0 else f"{slug}-{count}")
    return slugs


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    failures: list[str] = []
    for source in sorted(root.rglob("*.md")):
        if ".git" in source.parts:
            continue
        for raw_target in link_targets(source.read_text(encoding="utf-8")):
            target = raw_target.strip()
            if target.startswith("<") and ">" in target:
                target = target[1 : target.index(">")]
            else:
                target = target.split(maxsplit=1)[0]
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            path_text, separator, fragment = target.partition("#")
            destination = source if not path_text else source.parent / unquote(path_text)
            if not destination.exists():
                failures.append(f"{source.relative_to(root)} links to missing {path_text}")
                continue
            if separator and fragment and destination.suffix.lower() == ".md":
                if unquote(fragment).lower() not in heading_slugs(destination):
                    failures.append(
                        f"{source.relative_to(root)} links to missing heading #{fragment} "
                        f"in {destination.relative_to(root)}"
                    )
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("Markdown link validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
