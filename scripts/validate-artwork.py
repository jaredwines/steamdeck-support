#!/usr/bin/env python3
"""Validate SS artwork dimensions, color type, integrity, and logo alpha."""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def paeth(left: int, above: int, upper_left: int) -> int:
    estimate = left + above - upper_left
    distances = (
        abs(estimate - left),
        abs(estimate - above),
        abs(estimate - upper_left),
    )
    return (left, above, upper_left)[distances.index(min(distances))]


def read_png(path: Path) -> tuple[int, int, int, bytes]:
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("invalid PNG signature")
    position = len(PNG_SIGNATURE)
    compressed = bytearray()
    header: tuple[int, int, int] | None = None
    seen_end = False
    while position < len(data):
        if position + 12 > len(data):
            raise ValueError("truncated PNG chunk")
        length = struct.unpack_from(">I", data, position)[0]
        if position + 12 + length > len(data):
            raise ValueError("PNG chunk extends beyond the file")
        chunk_type = data[position + 4 : position + 8]
        chunk_data = data[position + 8 : position + 8 + length]
        stored_crc = struct.unpack_from(">I", data, position + 8 + length)[0]
        actual_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            raise ValueError(f"bad {chunk_type.decode(errors='replace')} checksum")
        position += 12 + length
        if chunk_type == b"IHDR":
            if header is not None or length != 13:
                raise ValueError("invalid PNG header")
            (
                width,
                height,
                bit_depth,
                color_type,
                compression,
                filtering,
                interlace,
            ) = struct.unpack(">IIBBBBB", chunk_data)
            if width == 0 or height == 0:
                raise ValueError("PNG dimensions must be positive")
            if (
                bit_depth != 8
                or compression != 0
                or filtering != 0
                or interlace != 0
            ):
                raise ValueError("expected 8-bit, non-interlaced PNG")
            if color_type not in (2, 6):
                raise ValueError("expected RGB or RGBA PNG")
            header = (width, height, color_type)
        elif chunk_type == b"IDAT":
            if header is None:
                raise ValueError("image data appears before the PNG header")
            compressed.extend(chunk_data)
        elif chunk_type == b"IEND":
            if length != 0 or position != len(data):
                raise ValueError("invalid PNG end chunk")
            seen_end = True
            break
    if header is None or not seen_end or not compressed:
        raise ValueError("PNG is missing its header, image data, or end chunk")

    width, height, color_type = header
    channels = 3 if color_type == 2 else 4
    stride = width * channels
    raw = zlib.decompress(bytes(compressed))
    if len(raw) != height * (stride + 1):
        raise ValueError("unexpected decompressed image size")
    for row in range(height):
        if raw[row * (stride + 1)] > 4:
            raise ValueError("unsupported PNG filter")
    if color_type == 2:
        return width, height, color_type, b""

    rows = bytearray()
    previous = bytearray(stride)
    offset = 0
    for _ in range(height):
        filter_type = raw[offset]
        encoded = raw[offset + 1 : offset + 1 + stride]
        offset += stride + 1
        decoded = bytearray(stride)
        for index, value in enumerate(encoded):
            left = decoded[index - channels] if index >= channels else 0
            above = previous[index]
            upper_left = previous[index - channels] if index >= channels else 0
            if filter_type == 0:
                predictor = 0
            elif filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = above
            elif filter_type == 3:
                predictor = (left + above) // 2
            elif filter_type == 4:
                predictor = paeth(left, above, upper_left)
            else:
                raise ValueError(f"unsupported PNG filter {filter_type}")
            decoded[index] = (value + predictor) & 0xFF
        rows.extend(decoded)
        previous = decoded
    return width, height, color_type, bytes(rows)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    specifications = {
        "wide-cover.png": (920, 430, 2),
        "portrait-cover.png": (600, 900, 2),
        "hero-background.png": (1920, 620, 2),
        "title-logo.png": (1200, 300, 6),
    }
    failures: list[str] = []
    artwork_root = root / "steam/artworks"
    collections = sorted(path for path in artwork_root.iterdir() if path.is_dir())
    if not collections:
        failures.append("no artwork collections found")
    for collection in collections:
        readme = collection / "README.md"
        required_evidence = (
            "## Evidence and provenance",
            "| Source or creation method |",
            "| Redistribution status |",
            "| Repository format and visual validation |",
            "| SteamOS build |",
            "| Wide, portrait, hero, logo, and Gaming Mode verification |",
        )
        if not readme.is_file():
            failures.append(f"{collection.relative_to(root)} is missing README.md")
        else:
            readme_text = readme.read_text(encoding="utf-8")
            for evidence in required_evidence:
                if evidence not in readme_text:
                    failures.append(
                        f"{readme.relative_to(root)} is missing evidence field {evidence!r}"
                    )
        actual_names = {path.name for path in collection.glob("*.png")}
        if actual_names != set(specifications):
            failures.append(
                f"{collection.relative_to(root)} has unexpected artwork inventory: "
                f"{sorted(actual_names)}"
            )
            continue
        for name, expected in specifications.items():
            path = collection / name
            try:
                width, height, color_type, pixels = read_png(path)
                if (width, height, color_type) != expected:
                    raise ValueError(
                        f"expected width, height, color type {expected}; "
                        f"found {(width, height, color_type)}"
                    )
                if color_type == 6:
                    alpha = pixels[3::4]
                    if not any(value == 0 for value in alpha):
                        raise ValueError("logo has no fully transparent pixels")
                    if not any(value > 0 for value in alpha):
                        raise ValueError("logo has no visible pixels")
            except (OSError, ValueError, zlib.error) as exc:
                failures.append(f"{path.relative_to(root)}: {exc}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("Artwork content validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
