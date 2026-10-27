#!/usr/bin/env python3
"""List stored non-Steam shortcut IDs without modifying Steam data."""

from __future__ import annotations

import argparse
import struct
import sys
import tempfile
from pathlib import Path


class VDFError(ValueError):
    """Raised when a binary Valve Data Format file cannot be read safely."""


class BinaryVDFReader:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.offset = 0

    def read_byte(self) -> int:
        if self.offset >= len(self.data):
            raise VDFError("unexpected end of file")
        value = self.data[self.offset]
        self.offset += 1
        return value

    def read_cstring(self) -> str:
        end = self.data.find(b"\0", self.offset)
        if end < 0:
            raise VDFError("unterminated string")
        raw = self.data[self.offset:end]
        self.offset = end + 1
        return raw.decode("utf-8", errors="replace")

    def read_int32(self) -> int:
        end = self.offset + 4
        if end > len(self.data):
            raise VDFError("truncated 32-bit integer")
        value = struct.unpack_from("<i", self.data, self.offset)[0]
        self.offset = end
        return value

    def read_object(self) -> dict[str, object]:
        result: dict[str, object] = {}
        while True:
            value_type = self.read_byte()
            if value_type == 8:
                return result
            key = self.read_cstring()
            if value_type == 0:
                result[key] = self.read_object()
            elif value_type == 1:
                result[key] = self.read_cstring()
            elif value_type == 2:
                result[key] = self.read_int32()
            else:
                raise VDFError(
                    f"unsupported value type {value_type} for key {key!r}"
                )


def parse_shortcuts(path: Path) -> list[dict[str, object]]:
    data = path.read_bytes()
    if len(data) > 16 * 1024 * 1024:
        raise VDFError("file is unexpectedly larger than 16 MiB")
    reader = BinaryVDFReader(data)
    root = reader.read_object()
    if reader.offset != len(reader.data):
        raise VDFError("unexpected data after the root object")

    shortcuts = root.get("shortcuts")
    if not isinstance(shortcuts, dict):
        raise VDFError("missing shortcuts object")

    records: list[dict[str, object]] = []
    for index, record in shortcuts.items():
        if not isinstance(record, dict):
            raise VDFError(f"shortcut {index!r} is not an object")
        app_id = record.get("appid")
        name = record.get("AppName")
        executable = record.get("exe")
        if not isinstance(app_id, int) or not isinstance(name, str):
            raise VDFError(f"shortcut {index!r} lacks an App ID or name")
        records.append(
            {
                "app_id": app_id & 0xFFFFFFFF,
                "name": name,
                "executable": executable if isinstance(executable, str) else "",
            }
        )
    return records


def default_paths() -> list[Path]:
    steam_userdata = Path.home() / ".local/share/Steam/userdata"
    return sorted(steam_userdata.glob("*/config/shortcuts.vdf"))


def sanitize(value: object) -> str:
    return "".join(
        character if character >= " " and character != "\x7f" else " "
        for character in str(value)
    )


def record_matches(record: dict[str, object], query: str | None) -> bool:
    if query is None:
        return True
    searchable = f"{record['name']}\n{record['executable']}"
    return query.casefold() in searchable.casefold()


def encode_string(key: str, value: str) -> bytes:
    return b"\x01" + key.encode() + b"\0" + value.encode() + b"\0"


def encode_int32(key: str, value: int) -> bytes:
    return b"\x02" + key.encode() + b"\0" + struct.pack("<i", value)


def encode_object(key: str, value: bytes) -> bytes:
    return b"\x00" + key.encode() + b"\0" + value + b"\x08"


def run_self_test() -> None:
    expected_id = 3_104_267_125
    signed_id = expected_id - (1 << 32)
    shortcut = b"".join(
        (
            encode_int32("appid", signed_id),
            encode_string("AppName", "Fixture Launcher"),
            encode_string("exe", '"/home/deck/Applications/fixture"'),
        )
    )
    fixture = encode_object("shortcuts", encode_object("0", shortcut)) + b"\x08"
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "shortcuts.vdf"
        path.write_bytes(fixture)
        records = parse_shortcuts(path)
    expected = {
        "app_id": expected_id,
        "name": "Fixture Launcher",
        "executable": '"/home/deck/Applications/fixture"',
    }
    if records != [expected]:
        raise AssertionError(f"self-test mismatch: {records!r}")
    if not record_matches(expected, "fixture") or record_matches(expected, "missing"):
        raise AssertionError("self-test filtering failed")
    if sanitize("unsafe\nname\t") != "unsafe name ":
        raise AssertionError("self-test output sanitization failed")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List App IDs stored in Steam non-Steam shortcut files."
    )
    parser.add_argument("paths", nargs="*", type=Path, help="shortcuts.vdf files")
    parser.add_argument(
        "--match",
        help="show only records whose name or executable contains this text",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        print("non-Steam shortcut inspector self-test passed")
        return 0

    paths = args.paths or default_paths()
    if not paths:
        print("No Steam shortcuts.vdf files found.", file=sys.stderr)
        return 1

    print("steam_user_id\tapp_id\tname\texecutable")
    failed = False
    matches = 0
    for path in paths:
        try:
            records = parse_shortcuts(path)
        except (OSError, VDFError) as exc:
            print(f"ERROR: {path}: {exc}", file=sys.stderr)
            failed = True
            continue
        user_id = path.parent.parent.name
        for record in records:
            if not record_matches(record, args.match):
                continue
            values = (
                user_id,
                str(record["app_id"]),
                str(record["name"]),
                str(record["executable"]),
            )
            print("\t".join(sanitize(value) for value in values))
            matches += 1
    if args.match and matches == 0:
        print(f"No shortcut matched {args.match!r}.", file=sys.stderr)
        failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
