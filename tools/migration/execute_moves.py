#!/usr/bin/env python3
"""Execute manifest moves with git mv, rollback, and recovery reports.

Phase 4/5 machinery.  Reads catalog/moved-paths.json and performs
``git mv`` for entries whose status matches --status, then flips those
entries to "moved".  Pure moves only: no file content is touched here,
so Git rename detection stays intact and reviewers can separate
relocation from later reference rewrites.

Safety contract (independently re-verified here, not trusted from the
builder):

  - status gating: "review_required" entries are REFUSED with a clear
    error; only "approved", "pilot", or an explicit --batch name list
    may execute;
  - unique sources and unique FINAL destinations within the batch;
  - no source/destination overlap cycles inside the batch;
  - every source exists, every destination is free, every destination
    parent path is valid;
  - the manifest carries no collision, double-move, or overlap-cycle
    reports;
  - moves execute in deterministic order; on ANY failure the moves
    already performed in this invocation are rolled back with
    ``git mv`` in reverse order, the manifest is left unmodified, and
    a recovery report is written to
    catalog/recovery-<timestamp>.json.

Nothing runs on a dirty tree.
"""

from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog"

EXECUTABLE_STATUSES = {"approved", "pilot"}


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                          text=True)


def validate_batch(batch: list[dict], manifest: dict) -> list[str]:
    """Independently re-verify the batch; return a list of problems."""
    problems = []
    if manifest.get("collision_report"):
        problems.append("manifest carries unresolved collisions")
    if manifest.get("double_move_report"):
        problems.append("manifest carries unresolved double-moves")
    if manifest.get("overlap_cycle_report"):
        problems.append("manifest carries unresolved overlap cycles")

    seen_src, seen_dst = set(), set()
    for m in batch:
        src, dst = m["old_path"], m["new_path"]
        if src in seen_src:
            problems.append(f"duplicate source in batch: {src}")
        seen_src.add(src)
        if dst in seen_dst:
            problems.append(f"duplicate destination in batch: {dst}")
        seen_dst.add(dst)
        if dst in seen_src and dst != src:
            problems.append(
                f"overlap cycle: {dst} is both destination and source")
        sp = pathlib.PurePosixPath(src)
        dp = pathlib.PurePosixPath(dst)
        if ".." in dp.parts or dp.is_absolute():
            problems.append(f"invalid destination path: {dst}")
        if not sp.name or not dp.name:
            problems.append(f"malformed move entry: {src} -> {dst}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", default=None,
                    help="manifest status to execute; one of "
                         + ", ".join(sorted(EXECUTABLE_STATUSES)))
    ap.add_argument("--batch", nargs="*", default=None,
                    help="explicit old_path list (must already be "
                         "approved/pilot status)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.status is None and args.batch is None:
        ap.error("provide --status or --batch")
    if args.status == "review_required":
        print("REFUSED: review_required entries are proposals only. "
              "Promote them to approved after human review, then "
              "re-run.")
        return 2

    manifest_path = CATALOG / "moved-paths.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    moves = manifest["moves"]
    by_src = {m["old_path"]: m for m in moves}

    if args.batch is not None:
        batch = []
        for src in args.batch:
            m = by_src.get(src)
            if m is None:
                print(f"REFUSED: {src} is not in the manifest")
                return 2
            if m["status"] not in EXECUTABLE_STATUSES | {"moved"}:
                print(f"REFUSED: {src} has status {m['status']!r}; "
                      "only approved/pilot entries may execute")
                return 2
            if m["status"] == "moved":
                print(f"skipping already-moved: {src}")
                continue
            batch.append(m)
    else:
        if args.status not in EXECUTABLE_STATUSES:
            ap.error(f"--status must be one of "
                     f"{sorted(EXECUTABLE_STATUSES)}")
        batch = [m for m in moves if m["status"] == args.status]

    if not batch:
        print("nothing to move")
        return 0

    problems = validate_batch(batch, manifest)
    if problems:
        print("VALIDATION FAILED — no moves performed:")
        for p in problems:
            print("  -", p)
        return 1

    dirty = git("status", "--porcelain").stdout.strip()
    if dirty and not args.dry_run:
        print("refusing: working tree is dirty; commit or stash first")
        print(dirty[:500])
        return 1

    # Pre-flight against the working tree.
    errors = []
    for m in batch:
        src = ROOT / m["old_path"]
        dst = ROOT / m["new_path"]
        if not src.exists():
            errors.append(f"missing source: {m['old_path']}")
        if dst.exists():
            errors.append(f"destination exists: {m['new_path']}")
        if not dst.parent.exists() and not args.dry_run:
            # parent dirs are created at move time; validate the
            # intended parent chain is inside the repo
            try:
                dst.parent.relative_to(ROOT)
            except ValueError:
                errors.append(f"destination escapes repo: {m['new_path']}")
    if errors:
        print("PRE-FLIGHT FAILED — no moves performed:")
        for e in errors:
            print("  -", e)
        return 1

    performed = []
    try:
        for m in sorted(batch, key=lambda x: x["new_path"]):
            dst = ROOT / m["new_path"]
            if args.dry_run:
                print(f"dry-run: {m['old_path']} -> {m['new_path']}")
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            proc = git("mv", m["old_path"], m["new_path"])
            if proc.returncode != 0:
                raise RuntimeError(
                    f"git mv failed for {m['old_path']}: "
                    f"{proc.stderr.strip()}")
            performed.append(m)
    except Exception as exc:  # noqa: BLE001 - rollback on any failure
        print(f"FAILURE mid-batch: {exc}")
        print(f"rolling back {len(performed)} performed moves ...")
        rollback_errors = []
        for m in reversed(performed):
            proc = git("mv", m["new_path"], m["old_path"])
            if proc.returncode != 0:
                rollback_errors.append(
                    {"move": m, "error": proc.stderr.strip()})
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        report_path = CATALOG / f"recovery-{stamp}.json"
        report_path.write_text(json.dumps({
            "invocation": vars(args),
            "failure": str(exc),
            "performed_before_failure": [m["old_path"] for m in
                                         performed],
            "rolled_back": [m["old_path"] for m in performed
                            if not any(r["move"] is m for r in
                                       rollback_errors)],
            "rollback_errors": rollback_errors,
            "manifest_modified": False,
        }, indent=2) + "\n", encoding="utf-8")
        print(f"recovery report: {report_path}")
        if rollback_errors:
            print("MANUAL INTERVENTION REQUIRED for:")
            for r in rollback_errors:
                print("  ", r["move"]["new_path"], "->",
                      r["move"]["old_path"], ":", r["error"])
        return 1

    if args.dry_run:
        print(f"\ndry-run complete: {len(batch)} moves would execute")
        return 0

    for m in performed:
        m["status"] = "moved"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(f"\nmoved: {len(performed)} files; manifest updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
