#!/usr/bin/env python3
"""Tag notes with outdated schema-version as needs-review.

Usage:
    python3 scripts/schema-upgrade.py [--dry-run] [--version X.Y]

Reads the current schema version from vault/00-system/SCHEMA-CHANGELOG.md
(first ## vX.Y heading), then scans all vault .md files. Any note whose
schema-version frontmatter field differs from the current version is tagged:
    status: needs-review
    review-reason: "schema change — migrating from vOLD to vNEW"
    review-confidence: 0.9

Run `make check` after to confirm frontmatter is still valid.
"""

import argparse
import json
import re
import sys
from pathlib import Path

VERSION_RE = re.compile(r"^## v(\d+\.\d+)", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

_config_path = Path("scripts/validate-skip.json")
_config = json.loads(_config_path.read_text()) if _config_path.exists() else {}
SKIP_ROOTS = set(_config.get("skip_roots", []))
SKIP_DIRS = set(_config.get("skip_dirs", [".git"]))


def current_schema_version(changelog_path: Path) -> str:
    text = changelog_path.read_text(encoding="utf-8")
    match = VERSION_RE.search(text)
    if not match:
        sys.exit(f"error: could not find a version heading in {changelog_path}")
    return match.group(1)


def should_skip(path: Path) -> bool:
    if path.name in SKIP_ROOTS:
        return True
    return any(part in SKIP_DIRS for part in path.parts)


def parse_schema_version(text: str) -> str | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    for line in match.group(1).splitlines():
        if line.startswith("schema-version:"):
            return line.partition(":")[2].strip()
    return None


def tag_note(path: Path, old_version: str, new_version: str, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return False

    fm_block = match.group(1)
    reason = f"schema change — migrating from v{old_version} to v{new_version}"

    def set_field(block: str, key: str, value: str) -> str:
        pattern = re.compile(rf"^{re.escape(key)}:.*$", re.MULTILINE)
        replacement = f"{key}: {value}"
        if pattern.search(block):
            return pattern.sub(replacement, block)
        return block + f"\n{replacement}"

    updated_fm = fm_block
    updated_fm = set_field(updated_fm, "status", "needs-review")
    updated_fm = set_field(updated_fm, "schema-version", new_version)

    # add or update review fields
    for key, val in [
        ("review-reason", f'"{reason}"'),
        ("review-confidence", "0.9"),
    ]:
        updated_fm = set_field(updated_fm, key, val)

    new_text = text.replace(match.group(1), updated_fm, 1)

    if dry_run:
        print(f"  [dry-run] would tag: {path}")
        return True

    path.write_text(new_text, encoding="utf-8")
    print(f"  tagged: {path}")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="show what would change without writing")
    parser.add_argument("--version", metavar="X.Y", help="target schema version (default: read from SCHEMA-CHANGELOG.md)")
    args = parser.parse_args()

    changelog = Path("vault/00-system/SCHEMA-CHANGELOG.md")
    if not changelog.exists():
        sys.exit(f"error: {changelog} not found — run from repo root")

    target_version = args.version or current_schema_version(changelog)
    print(f"target schema version: {target_version}")

    tagged = 0
    skipped = 0

    for md in sorted(Path(".").rglob("*.md")):
        if should_skip(md):
            continue
        text = md.read_text(encoding="utf-8")
        note_version = parse_schema_version(text)
        if note_version is None or note_version == target_version:
            continue
        if tag_note(md, note_version, target_version, args.dry_run):
            tagged += 1
        else:
            skipped += 1

    label = "would tag" if args.dry_run else "tagged"
    print(f"\n{label}: {tagged} note(s)  |  skipped (no frontmatter): {skipped}")
    if tagged and not args.dry_run:
        print("run `make check` to verify frontmatter validity")


if __name__ == "__main__":
    main()
