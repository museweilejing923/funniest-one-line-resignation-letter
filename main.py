"""Emit a retry loop's one-line resignation as /output/entry.txt.

Nothing here varies from run to run: no network calls, no clock
reads, no random numbers, so the file comes out identical every time.
"""

import os
import sys

# The joke itself: after 4,096 retries, the request hands in its notice.
ENTRY_LINE = "I quit. I have retried this request 4,096 times and it still will not love me back."
CHAR_LIMIT = 140
PUNCT_MARKS = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")


def abort(reason):
    """Print a complaint to stderr and stop with a failing status."""
    sys.stderr.write("error: %s\n" % reason)
    raise SystemExit(1)


def check_entry(candidate):
    """Refuse anything that is not a short, printable, lettered line."""
    if len(candidate) > CHAR_LIMIT:
        abort(
            "entry is %d chars, over the %d limit"
            % (len(candidate), CHAR_LIMIT)
        )
    try:
        candidate.encode("utf-8")
    except UnicodeEncodeError:
        abort("entry must encode as UTF-8")
    trimmed = candidate.strip()
    if trimmed == "":
        abort("entry must not be blank")
    for glyph in candidate:
        if ord(glyph) < 32 or ord(glyph) == 127:
            abort("entry must not contain control characters")
    if not any(glyph.isalpha() for glyph in trimmed):
        abort("entry needs at least one letter")
    if trimmed.isdigit():
        abort("entry must not be only digits")
    if all(glyph in PUNCT_MARKS for glyph in trimmed):
        abort("entry must not be only punctuation")
    if trimmed[-1] not in (".", "!", "?"):
        abort("entry must end with a sentence-ending mark (. ! ?)")


def run():
    check_entry(ENTRY_LINE)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(ENTRY_LINE)


if __name__ == "__main__":
    run()
