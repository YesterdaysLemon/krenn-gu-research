#!/usr/bin/env python3
"""Build the deterministic migration manifest from the classification.

Phase 2.  Reads catalog/layout-classification.json and emits
catalog/moved-paths.json with, for every classified file:

  { "old_path", "new_path", "reason", "status", "claim_family",
    "confidence" }

plus a collision report, destination-subtree counts, and the estimated
post-migration root entry count.  Statuses:

  "moved"           -> already executed by execute_moves.py;
  "pilot"           -> the disjoint mixed-star H22 pilot package
                       (approved and executed in the first PR);
  "proposed_high_confidence"
                    -> classifier says high confidence; NOT executable
                       without a committed batch file;
  "review_required" -> medium/low confidence proposal;
  "unclassified"    -> not in this manifest at all; see
                       catalog/unclassified-files.json.

The ``counts`` summary section is always DERIVED from the move records
via :func:`recompute_manifest_summary`, both at build time and after
``execute_moves.py`` flips statuses (which calls the same function).
This keeps summary and records internally consistent by construction.

Guarantees enforced here (checked AFTER every destination
transformation, including the pilot layout rules):
  - no duplicate destination paths;
  - no source appears twice;
  - no source/destination overlap cycles (a file cannot move onto a
    path that is itself a source being moved);
  - destination paths normalized (posix, no '.'/'..', no duplicate
    '/');
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

# Root entries retained by the target architecture (used by the
# moved-only root projection; observed values always win in reports).
FIXED_ROOT = {"README.md", "LICENSE", "CONTRIBUTING.md",
              "CITATION.cff", "pyproject.toml", "requirements.txt",
              "requirements.lock.txt", "Containerfile",
              ".gitignore"}
FIXED_DIRS = {".github", "claims", "docs", "src", "tools", "tests",
              "catalog", "research_snapshots", "research_figures"}

# Only high-confidence classifications are auto-approved.  Medium and
# low confidence stay review_required until a human promotes them.
AUTO_APPROVE_CONFIDENCE = {"high"}


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


def tracked_files(ref: str | None = None) -> set[str]:
    cmd = (["git", "ls-tree", "-r", "--name-only", ref] if ref
           else ["git", "ls-files"])
    out = subprocess.run(
        cmd, cwd=ROOT, capture_output=True, text=True, check=True)
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


def status_for(e: dict, is_pilot: bool, already_moved: set[str]) -> str:
    """Confidence-gated status assignment."""
    if e["old_path"] in already_moved:
        return "moved"
    if is_pilot:
        return "pilot"
    if e.get("confidence") in AUTO_APPROVE_CONFIDENCE:
        return "proposed_high_confidence"
    return "review_required"


def recompute_manifest_summary(manifest: dict, root: pathlib.Path,
                               classification: dict | None = None) -> dict:
    """Derive the manifest's ``counts`` section from its move records.

    Single source of truth for the summary: after ``execute_moves.py``
    flips statuses it calls this function, so summary and records agree
    by construction.  Root-projection inputs come from the
    classification when available (build time), else are re-derived
    from the base ref recorded in the manifest (post-execution).
    """
    records = manifest["moves"]
    moved = [r for r in records if r["status"] == "moved"]
    pilot = [r for r in records if r["status"] == "pilot"]
    proposed = [r for r in records
                if r["status"] == "proposed_high_confidence"]
    review = [r for r in records if r["status"] == "review_required"]

    # Base root tree is ALWAYS derived from git at the recorded
    # starting commit, never from classification entries (which contain
    # only classified files, not the full base root).  This makes the
    # projection independent of how many files are classified.
    start = manifest.get("starting_commit")
    out = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", start], cwd=root,
        capture_output=True, text=True, check=True)
    tree = [l for l in out.stdout.splitlines() if l.strip()]
    base_files = sorted(f for f in tree if "/" not in f)
    base_dirs = sorted({f.split("/")[0] for f in tree if "/" in f})
    if classification is not None:
        unclassified = classification["unclassified_count"]
    else:
        unclassified = manifest.get("counts", {}).get("unclassified", 0)

    def remaining_root_if(moves: set) -> int:
        left = [f for f in base_files if f not in moves]
        dirs = set(base_dirs)
        for m in moves:
            dirs.discard(m.split("/")[0])
        new_dirs = {r["new_path"].split("/")[0] for r in records
                    if r["old_path"] in moves}
        return len(left) + len(dirs | new_dirs | FIXED_DIRS)

    mechanically_moved = {r["old_path"] for r in moved + pilot}
    all_proposed = mechanically_moved | {r["old_path"] for r in proposed}
    all_classified = all_proposed | {r["old_path"] for r in review}

    subtree = collections.Counter(
        r["new_path"].split("/", 2)[0] if "/" in r["new_path"]
        else r["new_path"] for r in records)
    manifest["destination_subtree_counts"] = dict(
        sorted(subtree.items(), key=lambda kv: -kv[1]))

    counts = {
        "total_classified_moves": len(records),
        "moved": len(moved),
        "pilot": len(pilot),
        "proposed_high_confidence": len(proposed),
        "review_required": len(review),
        "unclassified": unclassified,
        "root_files_before": len(base_files),
        "root_dirs_before": len(base_dirs),
        "root_entries_before": len(base_files) + len(base_dirs),
        "projected_root_if_moved_only":
            remaining_root_if(mechanically_moved),
        "projected_root_if_high_confidence_batches_executed":
            remaining_root_if(all_proposed),
        "projected_root_if_all_classified_executed":
            remaining_root_if(all_classified),
        "projection_note": "unclassified files are not members of any "
                           "move set, so every projection already "
                           "leaves them at the root; do not add "
                           "unclassified again",
    }
    # Preserve collision/cycle tallies set at build time.
    for key in ("collisions", "double_moves", "overlap_cycles"):
        if key in manifest.get("counts", {}):
            counts[key] = manifest["counts"][key]
    manifest["counts"] = counts
    return manifest


def validate_records(records: list) -> tuple:
    """Post-transformation validation of final destinations.

    Returns (collisions, double_moves, cycles).  Checked on the FINAL
    new_path values, after every layout transformation.
    """
    collisions, double_moves, cycles = [], [], []
    seen_src, seen_dst = set(), {}
    for r in records:
        old, dst = r["old_path"], r["new_path"]
        if old in seen_src:
            double_moves.append(old)
        seen_src.add(old)
        if dst in seen_dst:
            collisions.append({"new_path": dst,
                               "sources": [seen_dst[dst], old]})
        else:
            seen_dst[dst] = old
    for r in records:
        if (r["new_path"] in seen_src
                and r["new_path"] != r["old_path"]):
            cycles.append({"source": r["old_path"],
                           "destination_is_also_source": r["new_path"]})
    return collisions, double_moves, cycles


def main() -> int:
    cls_path = CATALOG / "layout-classification.json"
    classification = json.loads(cls_path.read_text(encoding="utf-8"))
    entries = classification["entries"]

    # Sources are validated against the classification's base ref,
    # because old_path names the pre-migration location.  The executor
    # independently re-verifies executability against HEAD.
    base_ref = classification.get("starting_commit")
    tracked = tracked_files(base_ref)

    # Preserve any moves already executed (status moved) so a rebuild
    # does not re-plan them.  Moves that are already physically applied
    # at HEAD (source gone, destination present) are recorded as moved
    # even if a prior manifest never tracked them.
    head_tracked = tracked_files(None)
    already_moved = set()
    prior_executed_batch = {}
    manifest_path = CATALOG / "moved-paths.json"
    if manifest_path.exists():
        prior = json.loads(manifest_path.read_text(encoding="utf-8"))
        for m in prior.get("moves", []):
            if m.get("status") in ("moved", "pilot"):
                already_moved.add(m["old_path"])
                if m.get("executed_batch"):
                    prior_executed_batch[m["old_path"]] = (
                        m["executed_batch"])

    records, seen_src = [], set()
    collisions, double_moves, cycles = [], [], []

    for e in entries:
        old = e["old_path"]
        if old in seen_src:
            double_moves.append(old)
            continue
        seen_src.add(old)
        if old not in tracked:
            raise ValueError(f"source not tracked at base ref: {old}")
        is_pilot = e.get("claim_family") == PILOT_FAMILY
        # Compute the FINAL destination: base proposal, then any
        # pilot-layout transformation, then normalization.  Collision
        # checks run on this final value only.
        dst = normalize(e["proposed_path"])
        if is_pilot:
            dst = normalize(pilot_destination(
                old, str(pathlib.PurePosixPath(dst).parent)))
        rec = {
            "old_path": old,
            "new_path": dst,
            "reason": (f"pilot: {e['category']} in {PILOT_FAMILY}"
                       if is_pilot else
                       f"{e['category']} -> {e.get('claim_family')}"),
            "status": status_for(e, is_pilot, already_moved),
            "claim_family": e.get("claim_family"),
            "confidence": e.get("confidence"),
        }
        if rec["status"] == "moved" and old in prior_executed_batch:
            rec["executed_batch"] = prior_executed_batch[old]
        if (rec["status"] != "moved"
                and rec["old_path"] not in head_tracked
                and rec["new_path"] in head_tracked):
            rec["status"] = "moved"
            rec["reason"] += " [already applied at HEAD]"
        records.append(rec)

    # Final-destination uniqueness and overlap-cycle checks run on the
    # FINAL new_path values (post pilot-layout transformation).
    collisions, double_moves2, cycles = validate_records(records)
    double_moves.extend(d for d in double_moves2 if d not in
                        double_moves)

    manifest = {
        "generated_by": "tools/migration/build_manifest.py",
        "classification_source": "catalog/layout-classification.json",
        "starting_commit": classification["starting_commit"],
        "inspected_ref": classification.get("inspected_ref"),
        "pilot_package": PILOT_DIR,
        "status_model": {
            "moved": "already executed",
            "pilot": "the executed pilot batch",
            "proposed_high_confidence": "classifier says high "
                                        "confidence, but this is NOT "
                                        "operational approval; a human "
                                        "must promote members into a "
                                        "named batch file before "
                                        "execution",
            "review_required": "medium/low confidence proposal; needs "
                               "human review before it may even be "
                               "batched",
        },
        "approval_model": {
            "rule": "no classification confidence is executable on its "
                    "own; execute_moves.py runs only batches listed in "
                    "catalog/batches/*.json with reviewer, base SHA, "
                    "and member list",
            "batch_directory": "catalog/batches",
        },
        "counts": {
            "collisions": len(collisions),
            "double_moves": len(double_moves),
            "overlap_cycles": len(cycles),
        },
        "collision_report": collisions,
        "double_move_report": double_moves,
        "overlap_cycle_report": cycles,
        "moves": sorted(records, key=lambda r: r["new_path"]),
    }
    manifest = recompute_manifest_summary(manifest, ROOT, classification)

    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")

    if collisions or double_moves or cycles:
        print("PROBLEMS DETECTED — manifest written for inspection; "
              "do not execute moves.")
        for c in collisions:
            print("  collision:", c)
        for d in double_moves:
            print("  double-move:", d)
        for c in cycles:
            print("  overlap-cycle:", c)
        return 1

    c = manifest["counts"]
    print(f"moves={c['total_classified_moves']} moved={c['moved']} "
          f"pilot={c['pilot']} "
          f"proposed_high_confidence={c['proposed_high_confidence']} "
          f"review_required={c['review_required']} "
          f"collisions=0 double_moves=0 cycles=0")
    print(f"root entries: before={c['root_entries_before']}")
    print(f"projected if moved-only: "
          f"{c['projected_root_if_moved_only']}")
    print(f"projected if high-confidence batches executed: "
          f"{c['projected_root_if_high_confidence_batches_executed']}")
    print(f"projected if all classified executed: "
          f"{c['projected_root_if_all_classified_executed']}")
    print(f"(every projection already leaves the {c['unclassified']} "
          f"unclassified files at the root)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
