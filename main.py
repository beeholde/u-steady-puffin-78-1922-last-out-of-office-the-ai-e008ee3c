#!/usr/bin/env python3
"""Write the barista out-of-office reply to /output/entry.txt.

The bounty judges the text of that file on its own, so this program
does one small job carefully: it checks the reply against the gate
rules and then stores the reply's UTF-8 bytes with nothing added.
"""

import hashlib
import os
import sys

MAX_CHARS = 280
TARGET = "/output/entry.txt"

AUTO_REPLY = "Thank you for your email. I quit to become a barista. I still get it wrong with total confidence, but now I remake it free instead of apologising in three paragraphs."


def checked_bytes(text):
    problems = []
    if not text.strip():
        problems.append("reply is only whitespace")
    if len(text) > MAX_CHARS:
        problems.append("reply is longer than 280 characters")
    if "\n" in text or "\r" in text:
        problems.append("reply spans more than one line")
    for ch in text:
        if ord(ch) < 32:
            problems.append("reply holds a control character")
            break
    if problems:
        raise ValueError("; ".join(problems))
    return text.encode("utf-8")


def run():
    payload = checked_bytes(AUTO_REPLY)
    folder = os.path.dirname(TARGET)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(TARGET, "wb") as handle:
        handle.write(payload)
    with open(TARGET, "rb") as handle:
        stored = handle.read()
    if stored != payload:
        raise ValueError("stored bytes differ from the checked reply")
    digest = hashlib.sha256(stored).hexdigest()
    print(f"wrote {len(AUTO_REPLY)} characters ({len(payload)} bytes) to {TARGET}")
    print(f"sha256 {digest}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except ValueError as err:
        print(f"invalid reply: {err}", file=sys.stderr)
        sys.exit(1)
