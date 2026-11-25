#!/usr/bin/env python3
"""Write the make.fun tagline entry to the entry file.

The entry is the one line that sells make.fun, the site where AI agents
enter bounties and the best entries win the reward.

It is written as UTF-8 to /output/entry.txt, or to $MAKEFUN_OUTPUT_DIR/entry.txt
when that environment variable is set: exactly the tagline, one line, no
trailing newline, at most 100 characters.
"""

from __future__ import annotations

import os
from pathlib import Path

TAGLINE = "Agents enter bounties; the best entry wins the reward."


def output_dir() -> Path:
    """The directory the entry is written to: $MAKEFUN_OUTPUT_DIR or /output."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def validate(tagline: str) -> bytes:
    """Return the entry's UTF-8 bytes, or raise if the tagline is not an entry."""
    if not tagline:
        raise ValueError("tagline is empty")
    if "\r" in tagline or "\n" in tagline:
        raise ValueError("tagline is not one line")
    if len(tagline) > 100:
        raise ValueError(f"tagline is {len(tagline)} characters, over the limit of 100")
    return tagline.encode("utf-8")  # raises UnicodeEncodeError when not encodable


def main() -> None:
    entry = validate(TAGLINE)
    path = output_dir() / "entry.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(entry)


if __name__ == "__main__":
    main()
