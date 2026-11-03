#!/usr/bin/env python3
"""Check that rule IDs in src/no-tech-scribe.md stay stable across releases.

Released IDs come from every v* tag. Gaps are allowed: a rule can be dropped.

Errors:
- a malformed rule line, or an ID used twice;
- a retired ID (released before, missing from the latest release) used again;
- a new ID that is not above the highest released ID;
- a new ID that carries the text of a released rule that is now missing
  (a renumbered rule: keep the old ID instead).

Warnings:
- a released rule whose wording changed a lot. A person decides: same rule
  (keep the ID) or a different rule (retire the ID and add a new one).

Usage: scripts/check-ids.py [--exclude TAG]
  --exclude TAG  ignore this tag, for example the tag being released now.
"""
import argparse
import difflib
import os
import re
import subprocess
import sys

SRC = "src/no-tech-scribe.md"
RULE = re.compile(r"^NTS-(\d{3,}): (\S.*)$")
RENUMBERED = 0.9  # at or above: a new ID with an old rule's text
REWORDED = 0.6    # below: wording changed enough for a person to look

ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"
errors = 0


def report(kind, msg):
    global errors
    if kind == "error":
        errors += 1
    print(f"::{kind}::{msg}" if ACTIONS else f"{kind}: {msg}")


def nid(num):
    return f"NTS-{num:03d}"


def parse(text, where):
    rules = {}
    for n, line in enumerate(text.splitlines(), 1):
        if not line.startswith("NTS-"):
            continue
        m = RULE.match(line)
        if not m:
            report("error", f"{where}:{n}: malformed rule line, expected 'NTS-NNN: text': {line[:60]}")
            continue
        num = int(m.group(1))
        if num in rules:
            report("error", f"{where}:{n}: {nid(num)} is used twice")
        rules[num] = m.group(2)
    return rules


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True)


def similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


def main():
    ap = argparse.ArgumentParser(description="Check rule ID stability.")
    ap.add_argument("--exclude", help="tag to ignore, such as the tag being released")
    args = ap.parse_args()

    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    with open(SRC, encoding="utf-8") as f:
        current = parse(f.read(), SRC)

    tags = git("-c", "versionsort.suffix=-", "tag", "--list", "v*", "--sort=v:refname").stdout.split()
    tags = [t for t in tags if t != args.exclude]

    last_text = {}  # id -> text in the newest tag that has it
    last_tag = {}
    latest_ids = set()
    for tag in tags:
        shown = git("show", f"{tag}:{SRC}")
        if shown.returncode:
            report("warning", f"{tag} has no {SRC}; skipped")
            continue
        rules = parse(shown.stdout, tag)
        for num, text in rules.items():
            last_text[num] = text
            last_tag[num] = tag
        latest_ids = set(rules)

    if not last_text:
        print(f"ok: {len(current)} rules, no earlier releases to compare")
        return 0

    released = set(last_text)
    retired = released - latest_ids
    highest = max(released)
    missing = released - set(current)

    for num, text in sorted(current.items()):
        if num in retired:
            report("error", f"{nid(num)} was retired after {last_tag[num]}. Never reuse an ID; use a number above {nid(highest)}.")
        elif num in released:
            ratio = similarity(last_text[num], text)
            if ratio < REWORDED:
                report("warning", f"{nid(num)} changed a lot since {last_tag[num]} (similarity {ratio:.2f}). "
                                  "Same rule: keep the ID. Different rule: retire it and add a new ID.")
        else:
            if num <= highest:
                report("error", f"new {nid(num)} must be above {nid(highest)}, the highest released ID.")
            for old in sorted(missing):
                if similarity(last_text[old], text) >= RENUMBERED:
                    report("error", f"new {nid(num)} matches released {nid(old)}. Keep {nid(old)} instead of renumbering.")

    added = sorted(set(current) - released)
    dropped = sorted(missing - retired)
    print(f"compared with {len(tags)} tag(s); highest released ID {nid(highest)}")
    print(f"new: {', '.join(map(nid, added)) or 'none'}")
    print(f"dropped since the latest release: {', '.join(map(nid, dropped)) or 'none'}")
    print("ok" if errors == 0 else f"{errors} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
