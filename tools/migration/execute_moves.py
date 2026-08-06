#!/usr/bin/env python3
"""Execute manifest moves with git mv, rollback, and recovery reports.

Phase 4/5 machinery, hardened in Phase 2.  Reads
catalog/moved-paths.json and performs ``git mv`` for the entries of an
EXPLICITLY APPROVED, FROZEN batch, then flips those entries to
"moved" and records the executing batch id.  Pure moves only: no file
content is touched here, so Git rename detection stays intact and
reviewers can separate relocation from later reference rewrites.

Approval model: classifier confidence is NOT operational approval.
Every executable batch is a committed JSON file under
``catalog/batches/`` that freezes the exact old_path -> new_path
mappings it approves (see tools/migration/batch_contract.py):

    {
      "batch_id": "...",
      "approved_by": "...",
      "approved_at": "YYYY-MM-DD",
      "base_sha": "...",
      "manifest_sha256": "...",
      "mapping_sha256": "...",
      "member_count": N,
      "moves": [{"old_path": "...", "new_path": "..."}, ...]
    }

Before the FIRST git mv, this tool verifies (refusing outright on any
failure):

  - approved_at is present;
  - the batch base_sha resolves in this repository;
  - member_count equals the number of recorded mappings;
  - no duplicate sources or destinations;
  - the batch mapping_sha256 matches its own moves (batch unaltered
    since approval);
  - every batch mapping equals the CURRENT manifest mapping
    (manifest has not drifted since approval).

Additional safety contract (independently re-verified here):

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

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from batch_contract import validate_batch as contract_validate

ROOT = pathlib.Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog"
BATCH_DIR = CATALOG / "batches"


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                          text=True)


def _resolve_committed_batch_path(batch_id: str | None,
                                  batch_file: str | None) -> pathlib.Path:
    """Resolve the batch file, enforcing the committed-approval model.

    An executable batch must be a committed artifact under
    ``catalog/batches/``.  ``--batch-id`` names a file there directly.
    An explicit ``--batch-file`` is accepted only if it resolves inside
    ``catalog/batches/``, stays inside the repository, and is tracked
    by git (``git ls-files --error-unmatch``).  External or untracked
    batch files are refused.
    """
    if batch_id is not None:
        return BATCH_DIR / f"{batch_id}.json"
    raw = pathlib.Path(batch_file)
    path = (raw if raw.is_absolute()
            else (ROOT / raw)).resolve()
    batch_dir = BATCH_DIR.resolve()
    try:
        path.relative_to(batch_dir)
    except ValueError:
        raise SystemExit(
            f"refusing batch file outside catalog/batches/: {path}. "
            "Executable batches must be committed artifacts under "
            "catalog/batches/.")
    try:
        path.relative_to(ROOT.resolve())
    except ValueError:
        raise SystemExit(
            f"refusing batch file outside the repository: {path}.")
    rel = path.relative_to(ROOT.resolve()).as_posix()
    proc = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel], cwd=ROOT,
        capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(
            f"refusing untracked batch file: {rel}. Commit the batch "
            "under catalog/batches/ before executing it.")
    return path


def load_batch(batch_id: str | None,
               batch_file: str | None) -> tuple[dict, pathlib.Path]:
    """Load and structurally validate a frozen batch definition."""
    path = _resolve_committed_batch_path(batch_id, batch_file)
    if not path.exists():
        raise SystemExit(
            f"batch file not found: {path}. Create a committed frozen "
            "batch under catalog/batches/ (batch_id, approved_by, "
            "approved_at, base_sha, manifest_sha256, mapping_sha256, "
            "member_count, moves).")
    batch = json.loads(path.read_text(encoding="utf-8"))
    for field in ("batch_id", "approved_by", "approved_at", "base_sha",
                  "moves", "member_count", "mapping_sha256"):
        if field not in batch:
            raise SystemExit(
                f"batch file missing required field: {field} ({path})")
    if not batch["moves"]:
        raise SystemExit(f"batch {batch['batch_id']} has no moves")
    if not isinstance(batch["moves"], list):
        raise SystemExit("batch moves must be a list of mappings")
    return batch, path


def validate_batch_geometry(batch: list[dict], manifest: dict) -> list:
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
        dp = pathlib.PurePosixPath(dst)
        sp = pathlib.PurePosixPath(src)
        if ".." in dp.parts or dp.is_absolute():
            problems.append(f"invalid destination path: {dst}")
        if not sp.name or not dp.name:
            problems.append(f"malformed move entry: {src} -> {dst}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--batch-id", default=None,
                       help="name of a committed batch file under "
                            "catalog/batches/ (without .json)")
    group.add_argument("--batch-file", default=None,
                       help="explicit path to a batch file; must "
                            "resolve inside catalog/batches/, stay "
                            "inside the repository, and be git-tracked")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    batch_def, batch_path = load_batch(args.batch_id, args.batch_file)

    manifest_path = CATALOG / "moved-paths.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_moves = manifest["moves"]
    by_src = {m["old_path"]: m for m in manifest_moves}

    # 1. Frozen-contract validation — refusal before the first git mv.
    contract_problems = contract_validate(batch_def, ROOT,
                                          manifest_moves)
    if contract_problems:
        print("BATCH CONTRACT VIOLATION — refusing before the first "
              "git mv:")
        for p in contract_problems:
            print("  -", p)
        return 2

    # 2. Geometry validation.
    geometry_problems = validate_batch_geometry(batch_def["moves"],
                                                manifest)
    if geometry_problems:
        print("GEOMETRY VALIDATION FAILED — no moves performed:")
        for p in geometry_problems:
            print("  -", p)
        return 1

    # 3. Build the execution list; already-moved members are skipped,
    #    not re-moved.
    batch = []
    for bm in batch_def["moves"]:
        m = by_src[bm["old_path"]]
        if m["status"] == "moved":
            print(f"skipping already-moved: {bm['old_path']}")
            continue
        batch.append(m)

    if not batch:
        print("nothing to move (all batch members already moved)")
        return 0

    dirty = git("status", "--porcelain").stdout.strip()
    if dirty and not args.dry_run:
        print("refusing: working tree is dirty; commit or stash first")
        print(dirty[:500])
        return 1

    errors = []
    for m in batch:
        src = ROOT / m["old_path"]
        dst = ROOT / m["new_path"]
        if not src.exists():
            errors.append(f"missing source: {m['old_path']}")
        if dst.exists():
            errors.append(f"destination exists: {m['new_path']}")
        if not dst.parent.exists() and not args.dry_run:
            try:
                dst.parent.relative_to(ROOT)
            except ValueError:
                errors.append(
                    f"destination escapes repo: {m['new_path']}")
    if errors:
        print("PRE-FLIGHT FAILED — no moves performed:")
        for e in errors:
            print("  -", e)
        return 1

    print(f"batch {batch_def['batch_id']!r} approved by "
          f"{batch_def['approved_by']!r} "
          f"(base {str(batch_def['base_sha'])[:12]}, approved "
          f"{batch_def['approved_at']}), {len(batch)} members")

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
            "batch": {k: v for k, v in batch_def.items()
                      if k != "moves"},
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
        m["executed_batch"] = batch_def["batch_id"]
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(f"\nmoved: {len(performed)} files; manifest updated "
          f"(executed_batch={batch_def['batch_id']!r})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
