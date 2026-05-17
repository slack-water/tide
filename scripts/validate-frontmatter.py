#!/usr/bin/env python3
"""Validate that all vault notes have required frontmatter fields and valid values."""

import json
import sys
import re
from pathlib import Path

REQUIRED_FIELDS = ["title", "created", "updated", "folder", "type", "status", "schema-version"]
VALID_TYPES = {"note", "project", "log", "reference", "output", "template"}
VALID_STATUSES = {"active", "incubating", "complete", "archived", "needs-review"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

_config_path = Path(__file__).parent / "validate-skip.json"
_config = json.loads(_config_path.read_text()) if _config_path.exists() else {}
SKIP_ROOTS = set(_config.get("skip_roots", []))
SKIP_DIRS = set(_config.get("skip_dirs", [".git"]))


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip()
    data = {}
    for line in block.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            data[key.strip()] = val.strip()
    return data


def validate(path, errors):
    fm = parse_frontmatter(path)
    if fm is None:
        errors.append(f"{path}: missing frontmatter")
        return

    for field in REQUIRED_FIELDS:
        if field not in fm or fm[field] == "":
            errors.append(f"{path}: missing required field '{field}'")

    for datefield in ("created", "updated"):
        val = fm.get(datefield, "")
        if val and not DATE_RE.match(val):
            errors.append(f"{path}: '{datefield}' must be YYYY-MM-DD, got '{val}'")

    type_val = fm.get("type", "")
    if type_val and type_val not in VALID_TYPES:
        errors.append(f"{path}: invalid type '{type_val}' (must be one of {sorted(VALID_TYPES)})")

    status_val = fm.get("status", "")
    if status_val and status_val not in VALID_STATUSES:
        errors.append(f"{path}: invalid status '{status_val}' (must be one of {sorted(VALID_STATUSES)})")


def should_skip(path):
    if path.name in SKIP_ROOTS:
        return True
    for part in path.parts:
        if part in SKIP_DIRS:
            return True
    return False


def main():
    root = Path(".")
    errors = []
    checked = 0

    for md in sorted(root.rglob("*.md")):
        if should_skip(md):
            continue
        validate(md, errors)
        checked += 1

    if errors:
        print(f"frontmatter validation failed ({len(errors)} error(s)):\n")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print(f"frontmatter ok ({checked} files checked)")


if __name__ == "__main__":
    main()
