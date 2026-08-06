#!/usr/bin/env python3
"""Build the deterministic migration manifest from the classification.

Phase 2.  Reads catalog/layout-classification.json and emits
catalog/moved-paths.json with, for every classified file:

  { "old_path", "new_path", "reason", "status", "claim_family" }

plus a collision report, destination-subtree counts, and the estimated
post-migration root entry count.  Statuses:

  "pilot"  -> part of the disjoint mixed-star H22 pilot package and
              executed in this first PR;
  "planned"-> classified but not executed in this PR (bulk migration);
  "unclassified" files are NOT in this manifest; they live in
              catalog/unclassified-files.json and stay put.

Guarantees enforced here:
  - no duplicate destination paths;
  - no source appears twice;
  - destination paths normalized (posix, no '.'/'..', no duplicate '/');
  - the set of moved sources is a subset of tracked root files.

This tool moves nothing.
"""

from __future__ import annotations

import collections
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog"

# The pilot claim package (spec Phase 4).
PILOT_FAMILY = "p5/h22/disjoint-mixed-star"
PILOT_DIR = f"claims/{PILOT_FAMILY}"

# Pilot package internal layout (spec Phase 4): canonical
# theorem/verifier/audit at the package root, the alternate
# independent proof in alternate/, directly associated boundary
# documents and their scripts in boundaries/, and the working note
# and certificate-divisor frontier at the package root.
PILOT_BOUNDARY_MARKERS = (
    "AF_APHI_BOUNDARY", "CERTIFICATE_DIVISOR_FRONTIER",
    "COEFFICIENT_QUADRATIC_BOUNDARY", "COUPLED_SLOPE_BOUNDARY",
    "EQUAL_OPPOSITE_WEIGHT", "LINEAR_SLOPE_BOUNDARY",
    "PARAMETER_PIVOT_BOUNDARY", "SLOPE_R1_BINARY",
    "SLOPE_RM1_BINARY", "TORUS_QUOTIENT", "ZERO_SLOPE_BOUNDARY",
)


def pilot_destination(old: str, base_dst: str) -> str:
    """Place a pilot file into the spec package layout."""
    name = pathlib.PurePosixPath(old).name
    stem = pathlib.PurePosixPath(old).stem.upper()
    pkg = pathlib.PurePosixPath(base_dst)
    if "_ALTERNATE" in stem:
        return str(pkg / "alternate" / name)
    if any(marker in stem for marker in PILOT_BOUNDARY_MARKERS):
        return str(pkg / "boundaries" / name)
    return str(pkg / name)


def tracked_files() -> set[str]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True,
        check=True)
    return {l for l in out.stdout.splitlines() if l.strip()}


def normalize(dest: str) -> str:
    p = pathlib.PurePosixPath(dest)
    parts = []
    for part in p.parts:
        if part in ("", "."):
            continue
        if part == "..":
            raise ValueError(f"destination escapes root: {dest}")
        parts.append(part)
    if not parts:
        raise ValueError(f"empty destination: {dest}")
    return "/".join(parts)


def main() -> int:
    cls_path = CATALOG / "layout-classification.json"
    classification = json.loads(cls_path.read_text(encoding="utf-8"))
    entries = classification["entries"]
    tracked = tracked_files()

    records, seen_src, seen_dst = [], set(), set()
    collisions, double_moves = [], []
    subtree_counts = collections.Counter()

    for e in entries:
        old = e["old_path"]
        dst = normalize(e["proposed_path"])
        if old in seen_src:
            double_moves.append(old)
            continue
        seen_src.add(old)
        if dst in seen_dst:
            collisions.append({"new_path": dst,
                               "conflicting_sources": old})
            continue
        seen_dst.add(dst)
        if old not in tracked:
            raise ValueError(f"source not tracked: {old}")
        is_pilot = e.get("claim_family") == PILOT_FAMILY
        if is_pilot:
            dst = normalize(pilot_destination(
                old, str(pathlib.PurePosixPath(dst).parent)))
        rec = {
            "old_path": old,
            "new_path": dst,
            "reason": (f"pilot: {e['category']} in {PILOT_FAMILY}"
                       if is_pilot else
                       f"{e['category']} -> {e.get('claim_family')}"),
            "status": "pilot" if is_pilot else "planned",
            "claim_family": e.get("claim_family"),
            "confidence": e.get("confidence"),
        }
        records.append(rec)
        subtree_counts[dst.split("/", 2)[0]
                       if "/" in dst else dst] += 1

    pilot_records = [r for r in records if r["status"] == "pilot"]
    pilot_files = [r["old_path"] for r in pilot_records]

    root_files_now = sorted(
        f for f in tracked if "/" not in f)
    dirs_now = sorted({f.split("/")[0] for f in tracked if "/" in f})
    planned_moved_sources = {r["old_path"] for r in records}
    # Root entries after a FULL migration = everything still at root
    # that was not classified to move, plus the top-level dirs that
    # remain.
    remaining_root_files = [
        f for f in root_files_now if f not in planned_moved_sources]
    remaining_root_dirs = sorted(
        set(dirs_now) - {"claims", "docs", "src", "tools", "tests",
                         "catalog", "research_figures"})
    fixed_root = ["README.md", "LICENSE", "CONTRIBUTING.md",
                  "CITATION.cff", "pyproject.toml", "requirements.txt",
                  "requirements.lock.txt", "Containerfile",
                  ".gitignore"]
    fixed_dirs = [".github", "claims", "docs", "src", "tools", "tests",
                  "catalog", "research_snapshots"]
    est_after = len(fixed_root) + len(fixed_dirs) + len(
        [f for f in remaining_root_files if f not in fixed_root]) + len(
        [d for d in remaining_root_dirs if d not in fixed_dirs])

    manifest = {
        "generated_by": "tools/migration/build_manifest.py",
        "classification_source": "catalog/layout-classification.json",
        "starting_commit": classification["starting_commit"],
        "pilot_package": PILOT_DIR,
        "counts": {
            "total_classified_moves": len(records),
            "pilot_moves": len(pilot_records),
            "planned_moves": len(records) - len(pilot_records),
            "root_files_before": len(root_files_now),
            "root_dirs_before": len(dirs_now),
            "root_entries_before": len(root_files_now) + len(dirs_now),
            "estimated_root_entries_after_full_migration": est_after,
            "collisions": len(collisions),
            "double_moves": len(double_moves),
            "unclassified": classification["unclassified_count"],
        },
        "destination_subtree_counts": dict(
            sorted(subtree_counts.items(), key=lambda kv: -kv[1])),
        "collision_report": collisions,
        "double_move_report": double_moves,
        "moves": sorted(records, key=lambda r: r["new_path"]),
    }

    if collisions or double_moves:
        (CATALOG / "moved-paths.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8")
        print("COLLISIONS DETECTED — manifest written for inspection; "
              "do not execute moves.")
        for c in collisions:
            print("  collision:", c)
        for d in double_moves:
            print("  double-move:", d)
        return 1

    (CATALOG / "moved-paths.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(f"moves={len(records)} pilot={len(pilot_records)} "
          f"planned={len(records) - len(pilot_records)} "
          f"collisions=0 double_moves=0")
    print(f"root entries: before={len(root_files_now) + len(dirs_now)} "
          f"estimated_after_full={est_after}")
    print(f"unclassified={classification['unclassified_count']}")
    print("\nPilot package layout:")
    for r in sorted(pilot_records, key=lambda r: r["new_path"]):
        print(f"  {r['old_path']}\n    -> {r['new_path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
