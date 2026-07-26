"""Materialize the exact SAT replay CNF for a global CEGAR manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from candidate_killer_cover_sat import candidate_cover_cnf
from global_candidate_laurent_cegar import (
    add_entry_support_symmetry_breaking,
    candidate_variable_map,
    symmetry_blocking_clauses,
    symmetry_transforms,
)
from search_witness import EquationSystem


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifests", type=Path, nargs="*")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--symmetry-floor",
        choices=("none", "generators", "full"),
        default="none",
        help="promote every manifest to at least this symmetry mode",
    )
    parser.add_argument(
        "--pattern-manifest",
        type=Path,
        action="append",
        default=[],
        help="certified whole-pattern manifest to block under full symmetry",
    )
    parser.add_argument(
        "--entry-symmetry-breaking",
        choices=("none", "generators"),
        default="none",
        help="lex-minimize the entry support under safe group comparisons",
    )
    parser.add_argument(
        "--exclude-pattern-orbit",
        type=int,
        action="append",
        default=[],
        help="omit a pattern row by its manifest orbit index",
    )
    args = parser.parse_args()

    system = EquationSystem(6, 3)
    candidates = candidate_variable_map()
    cnf = candidate_cover_cnf(10)
    base_clauses = len(cnf.clauses)
    mode_rank = {"none": 0, "generators": 1, "full": 2}
    manifest_summaries = []
    for manifest_path in args.manifests:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_mode = str(manifest.get("symmetry_images", "none"))
        symmetry_mode = max(
            (manifest_mode, args.symmetry_floor),
            key=mode_rank.__getitem__,
        )
        transforms = symmetry_transforms(symmetry_mode)
        before = len(cnf.clauses)
        for row in manifest["rows"]:
            clauses = symmetry_blocking_clauses(
                system,
                candidates,
                {
                    tuple(int(value) for value in arc)
                    for arc in row["candidate_arcs"]
                },
                {int(index) for index in row["positive_entries"]},
                {int(index) for index in row["negative_entries"]},
                transforms,
            )
            cnf.clauses.extend(clauses)
        manifest_summaries.append(
            {
                "manifest": str(manifest_path),
                "rows": len(manifest["rows"]),
                "symmetry_images": symmetry_mode,
                "clauses_added": len(cnf.clauses) - before,
            }
        )
    pattern_summaries = []
    full_transforms = symmetry_transforms("full")
    certified_pattern_statuses = {
        "certified",
        "certified_with_exact_fallback",
        "unconditional_laurent_contradiction",
    }
    for pattern_manifest_path in args.pattern_manifest:
        pattern_manifest = json.loads(
            pattern_manifest_path.read_text(encoding="utf-8")
        )
        before = len(cnf.clauses)
        certified_rows = [
            row
            for row in pattern_manifest["rows"]
            if row["status"] in certified_pattern_statuses
            and int(row["orbit"]) not in args.exclude_pattern_orbit
        ]
        for row in certified_rows:
            candidate_arcs = {
                (vertex, colour, int(neighbour))
                for vertex, pattern_row in enumerate(row["pattern"])
                for colour, neighbour in enumerate(pattern_row)
            }
            cnf.clauses.extend(
                symmetry_blocking_clauses(
                    system,
                    candidates,
                    candidate_arcs,
                    set(),
                    set(),
                    full_transforms,
                )
            )
        pattern_summaries.append(
            {
                "manifest": str(pattern_manifest_path),
                "certified_patterns": len(certified_rows),
                "clauses_added": len(cnf.clauses) - before,
            }
        )
    symmetry_breaking_clauses = add_entry_support_symmetry_breaking(
        cnf,
        system,
        symmetry_transforms(args.entry_symmetry_breaking),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    cnf.write_dimacs(args.output)
    print(
        json.dumps(
            {
                "manifests": manifest_summaries,
                "pattern_manifests": pattern_summaries,
                "output": str(args.output),
                "variables": cnf.variable_count,
                "base_clauses": base_clauses,
                "learned_clauses": len(cnf.clauses) - base_clauses,
                "entry_symmetry_breaking": args.entry_symmetry_breaking,
                "symmetry_breaking_clauses": symmetry_breaking_clauses,
                "clauses": len(cnf.clauses),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
