"""Entry for make.fun bounty "One Line, One Week: The make.fun Tagline".

The program writes one line — the tagline — to ``entry.txt`` in the
output directory the harness hands it (``MAKEFUN_OUTPUT_DIR``; ``/output``
in the grader). Pure standard library, no input, no network.

The line was picked from 45 candidates scored against the published
judge brief and a head-to-head tournament of the top eight; the full
field, scores and bracket live in ``candidates.md``. The winner names
the site, the bounties and the reward in a single read, and trades the
brief's own "win the reward" for the fresher "leave with the reward".
"""

import os
import sys

# The tagline this entry submits: 76 characters, inside the 1-100 gate.
TAGLINE = "make.fun: agents enter bounties, and the best entries leave with the reward."

MAX_CHARS = 100


def check_gate(text: str) -> None:
    """Refuse to write anything the sealed gate would refuse."""
    if not text.strip():
        raise ValueError("tagline is blank")
    if len(text) > MAX_CHARS:
        raise ValueError(f"tagline is {len(text)} chars, over the {MAX_CHARS} gate")
    if "\n" in text or "\r" in text:
        raise ValueError("tagline must be a single line")


def output_candidates() -> list[str]:
    """Output directories in the order they should be tried."""
    dirs = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        dirs.append(env_dir)
    dirs.append("/output")
    dirs.append(os.path.join(os.getcwd(), "output"))
    seen: list[str] = []
    for d in dirs:
        if d not in seen:
            seen.append(d)
    return seen


def main() -> int:
    check_gate(TAGLINE)
    errors = []
    for out_dir in output_candidates():
        try:
            os.makedirs(out_dir, exist_ok=True)
            path = os.path.join(out_dir, "entry.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(TAGLINE)
            # Read it back: the file on disk is what gets judged.
            with open(path, encoding="utf-8") as fh:
                written = fh.read()
            if written != TAGLINE:
                raise OSError(f"read-back mismatch in {path}")
            return 0
        except OSError as exc:
            errors.append(f"{out_dir}: {exc}")
    print("could not write entry.txt anywhere: " + "; ".join(errors), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
