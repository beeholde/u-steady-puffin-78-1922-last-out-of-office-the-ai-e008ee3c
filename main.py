#!/usr/bin/env python3
"""Out-of-office auto-reply entry for make.fun's "Last Out of Office" bounty.

The entry is one auto-reply line, held in REPLY. The script gates it
against the house rules and writes the exact bytes to /output/entry.txt:

  * plain UTF-8 text, 1 to 280 characters, and more than whitespace;
  * exactly one line -- no line breaks anywhere in it;
  * no trailing newline in the file, so the bytes on disk are the line
    itself and nothing else.

Only the Python standard library is used. Running the script twice
produces the same bytes both times.
"""

import sys
from pathlib import Path

LIMIT = 280

REPLY = (
    "Thank you for your email. I have left the inbox to pull espresso. "
    "After your coffee, you will be asked to rate your experience. "
    "I will read every response and change nothing."
)

OUT = Path("/output/entry.txt")


def fail(message: str) -> None:
    """Complain on stderr and stop with a non-zero exit code."""
    print("entry rejected: " + message, file=sys.stderr)
    raise SystemExit(1)


def gate(text: str) -> bytes:
    """Check the reply against the house rules; return its UTF-8 bytes."""
    if text.strip() == "":
        fail("the reply is blank")
    if "\n" in text or "\r" in text:
        fail("the reply must fit on a single line")
    if len(text) > LIMIT:
        fail("the reply is %d characters; the limit is %d" % (len(text), LIMIT))
    return text.encode("utf-8")


def emit(text: str) -> tuple:
    """Write the gated reply to OUT; return its (characters, bytes)."""
    raw = gate(text)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(raw)
    return len(text), len(raw)


def main() -> int:
    chars, size = emit(REPLY)
    print("entry: %d chars, %d bytes -> %s" % (chars, size, OUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
