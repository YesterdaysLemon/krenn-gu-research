#!/usr/bin/env python3
"""Execute manifest moves with git mv and record status transitions.

Phase 4/5 machinery.  Reads catalog/moved-paths.json, performs
``git mv`` for every entry whose status matches --status (default
"pilot"), and flips those entries to "moved".  Pure moves only: no
file content is touched here, so Git rename detection stays intact
and reviewers can separate relocation from later reference rewrites.

Refuses to run if:
  - a source is missing or already moved;
  - a destination already exists;
  - the working tree is dirty (so the move commit is pure).
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", default="pilot",
                    help="manifest status to execute (default: pilot)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    manifest_path = CATALOG / "moved-paths.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    dirty = subprocess.run(
        ["git", "status", "--porcelain"], cwd=ROOT,
        capture_output=True, text=True).stdout.strip()
    if dirty and not args.dry_run:
        print("refusing: working tree is dirty; commit or stash first")
        print(dirty[:500])
        return 1

    todo = [m for m in manifest["moves"] if m["status"] == args.status]
    if not todo:
        print(f"no moves with status {args.status!r}")
        return 0

    # Pre-flight validation.
    errors = []
    for m in todo:
        src = ROOT / m["old_path"]
        dst = ROOT / m["new_path"]
        if not src.exists():
            errors.append(f"missing source: {m['old_path']}")
        if dst.exists():
            errors.append(f"destination exists: {m['new_path']}")
    if errors:
        for e in errors:
            print("  ERROR:", e)
        return 1

    moved = 0
    for m in sorted(todo, key=lambda x: x["new_path"]):
        dst = ROOT / m["new_path"]
        if not args.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["git", "mv", m["old_path"], m["new_path"]],
                cwd=ROOT, check=True)
            m["status"] = "moved"
        moved += 1
        print(f"{'dry-run ' if args.dry_run else ''}"
              f"{m['old_path']} -> {m['new_path']}")

    if not args.dry_run:
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8")
    print(f"\n{'would move' if args.dry_run else 'moved'}: {moved} "
          f"files (status {args.status!r})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
