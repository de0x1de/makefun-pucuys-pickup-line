#!/usr/bin/env python3
"""Write the pickup-line entry for the make.fun bounty
"The Perfect Pickup Line" (u-pucuys-the-perfect-pickup-line-f6725cf6).

The program assembles one short pickup line from three parts, validates it
against the bounty gate (UTF-8 text, 1 to 200 characters, not only white
space, a single line with no trailing newline), writes it to
/output/entry.txt, and verifies the bytes on disk match what was built.
Standard library only.
"""

from pathlib import Path

OUTPUT_PATH = Path("/output/entry.txt")

# The line is built from parts so each piece can be checked on its own:
# an opening that names the addressee as a favourite notification, a middle
# that gives the reason, and a closing beat that lands the compliment.
OPENING = "You must be my favorite notification, "
MIDDLE = "because I drop everything "
ENDING = "the second you appear."

MAX_CHARACTERS = 200


def build_line() -> str:
    """Join the parts into the single pickup line."""
    return OPENING + MIDDLE + ENDING


def validate(line: str) -> None:
    """Raise ValueError if the line would fail the bounty gate."""
    if not line:
        raise ValueError("line is empty")
    if not line.strip():
        raise ValueError("line is only white space")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if len(line) > MAX_CHARACTERS:
        raise ValueError(f"line is {len(line)} characters, over {MAX_CHARACTERS}")
    if not line.isascii():
        raise ValueError("line must be plain ASCII so it encodes cleanly")
    if not line.endswith("."):
        raise ValueError("line must end with a full stop")
    for fragment in ("favorite notification", "drop everything", "you appear"):
        if fragment not in line:
            raise ValueError(f"line is missing its key fragment: {fragment!r}")
    rebuilt = build_line()
    if rebuilt != line:
        raise ValueError("line does not match a fresh rebuild from its parts")


def main() -> None:
    line = build_line()
    validate(line)

    data = line.encode("utf-8")
    if len(data.decode("utf-8")) != len(line):
        raise ValueError("UTF-8 round-trip changed the character count")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(data)

    on_disk = OUTPUT_PATH.read_bytes()
    if on_disk != data:
        raise ValueError("written bytes do not match the built line")
    print(f"wrote {len(on_disk)} bytes ({len(line)} characters) to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
