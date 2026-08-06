#!/usr/bin/env python3
"""Build the deterministic migration manifest from the classification.

Phase 2.  Reads catalog/layout-classification.json and emits
catalog/moved-paths.json with, for every classified file:

  { "old_path", "new_path", "reason", "status", "claim_family",
    "confidence" }

Statuses (confidence-gated; only explicitly approved batches are
executable):

  "moved"           -> already executed by execute_moves.py;
  "pilot"           -> the disjoint mixed-star H22 pilot package
                       (approved and executed in the first PR);
  "approved"        -> high-confidence classification, approved for
                       execution as a named batch;
  "review_required" -> medium- or low-confidence classification; a
                       PROPOSAL only. execute_moves.py refuses to move
                       these until a human promotes them to
                       "approved";
  "unclassified"    -> not in this manifest at all; see
                       catalog/unclassified-files.json.

Sources are validated against the classification's base ref (its
starting_commit), because old_path names the pre-migration location;
the executor independently re-verifies executability against HEAD.

Guarantees enforced here (checked AFTER every destination
transformation, including the pilot layout rules):
  - no duplicate final destination paths;
  - no source appears twice;
  - no source/destination overlap cycles (a file cannot move onto a
    path that is itself a source being moved);
  - destination paths normalized (posix, no '.'/'..', no duplicate
    '/').

The projected post-migration root count is split into mechanically
approved moves, review-required proposals, and truly unclassified
files, so the estimate is honest about what still needs human review.

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
    """Confidence-gated status assignment.

    No confidence level is operational approval: high confidence
    yields "proposed_high_confidence", which a human must promote into
    a named batch before execution.
    """
    if e["old_path"] in already_moved:
        return "moved"
    if is_pilot:
        return "pilot"
    if e.get("confidence") in AUTO_APPROVE_CONFIDENCE:
        return "proposed_high_confidence"
    return "review_required"


def validate_records(records: list[dict]) -> tuple[list, list, list]:
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
    # does not re-plan them.
    # Moves that are already physically applied at HEAD (source gone,
    # destination present) are recorded as moved even if a prior
    # manifest never tracked them (e.g. the infrastructure-phase
    # ledger relocation).
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
    subtree_counts = collections.Counter()

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
        subtree_counts[dst.split("/", 2)[0]
                       if "/" in dst else dst] += 1

    # Final-destination uniqueness (post-transformation).
    seen_dst = {}
    for r in records:
        if r["new_path"] in seen_dst:
            collisions.append({
                "new_path": r["new_path"],
                "sources": [seen_dst[r["new_path"]], r["old_path"]],
            })
        else:
            seen_dst[r["new_path"]] = r["old_path"]

    # Source/destination overlap cycles: a destination that is itself
    # a source scheduled to move would be clobbered mid-batch.
    sources = {r["old_path"] for r in records}
    for r in records:
        if r["new_path"] in sources and r["new_path"] != r["old_path"]:
            cycles.append({
                "source": r["old_path"],
                "destination_is_also_source": r["new_path"],
            })

    moved = [r for r in records if r["status"] == "moved"]
    pilot_records = [r for r in records if r["status"] == "pilot"]
    proposed = [r for r in records
                if r["status"] == "proposed_high_confidence"]
    review = [r for r in records if r["status"] == "review_required"]

    # Honest projected root counts, split by gate.  Root counts are
    # measured at the base ref (pre-migration state).
    root_files_base = sorted(f for f in tracked if "/" not in f)
    dirs_base = sorted({f.split("/")[0] for f in tracked if "/" in f})

    fixed_root = {"README.md", "LICENSE", "CONTRIBUTING.md",
                  "CITATION.cff", "pyproject.toml", "requirements.txt",
                  "requirements.lock.txt", "Containerfile",
                  ".gitignore", ".gitignore"}
    fixed_dirs = {".github", "claims", "docs", "src", "tools", "tests",
                  "catalog", "research_snapshots", "research_figures"}

    def remaining_root_if(moves: set[str]) -> int:
        left = [f for f in root_files_base if f not in moves]
        dirs = set(dirs_base)
        for m in moves:
            top = m.split("/")[0]
            dirs.discard(top)
        new_dirs = {r["new_path"].split("/")[0] for r in records
                    if r["old_path"] in moves}
        return len(left) + len(dirs | new_dirs | fixed_dirs)

    mechanically_moved = {r["old_path"] for r in moved + pilot_records}
    all_proposed = mechanically_moved | {r["old_path"]
                                         for r in proposed}
    all_classified = all_proposed | {r["old_path"] for r in review}
    unclassified_count = classification["unclassified_count"]

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
            "total_classified_moves": len(records),
            "moved": len(moved),
            "pilot": len(pilot_records),
            "proposed_high_confidence": len(proposed),
            "review_required": len(review),
            "unclassified": unclassified_count,
            "root_files_before": len(root_files_base),
            "root_dirs_before": len(dirs_base),
            "root_entries_before": len(root_files_base) + len(dirs_base),
            "projected_root_if_moved_only":
                remaining_root_if(mechanically_moved),
            "projected_root_if_high_confidence_batches_executed":
                remaining_root_if(all_proposed),
            "projected_root_if_all_classified_executed":
                remaining_root_if(all_classified),
            "projection_note": "unclassified files are not members of "
                               "any move set, so every projection "
                               "already leaves them at the root; do "
                               "not add unclassified_count again",
            "collisions": len(collisions),
            "double_moves": len(double_moves),
            "overlap_cycles": len(cycles),
        },
        "collision_report": collisions,
        "double_move_report": double_moves,
        "overlap_cycle_report": cycles,
        "destination_subtree_counts": dict(
            sorted(subtree_counts.items(), key=lambda kv: -kv[1])),
        "moves": sorted(records, key=lambda r: r["new_path"]),
    }

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

    print(f"moves={len(records)} moved={len(moved)} "
          f"pilot={len(pilot_records)} "
          f"proposed_high_confidence={len(proposed)} "
          f"review_required={len(review)} "
          f"collisions=0 double_moves=0 cycles=0")
    print(f"root entries: before={len(root_files_base) + len(dirs_base)}")
    print(f"projected if moved-only: "
          f"{manifest['counts']['projected_root_if_moved_only']}")
    print(f"projected if high-confidence batches executed: "
          f"{manifest['counts']['projected_root_if_high_confidence_batches_executed']}")
    print(f"projected if all classified executed: "
          f"{manifest['counts']['projected_root_if_all_classified_executed']}")
    print(f"(every projection already leaves the {unclassified_count} "
          f"unclassified files at the root)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
