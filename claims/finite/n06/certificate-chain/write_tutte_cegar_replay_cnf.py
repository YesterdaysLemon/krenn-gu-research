"""Materialize one Tutte case strengthened by verified CEGAR clauses."""

from __future__ import annotations

import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])

import argparse
import json
from pathlib import Path

from candidate_matching_obstruction_sat import matching_obstruction_cnf
from global_candidate_laurent_cegar import (
    add_entry_support_symmetry_breaking,
    candidate_variable_map,
    symmetry_blocking_clauses,
    symmetry_transforms,
)
from krenn_gu.search_witness import EquationSystem


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-matching", type=int, required=True)
    parser.add_argument("--separator-size", type=int, required=True)
    parser.add_argument("--group-sizes")
    parser.add_argument("manifests", type=Path, nargs="*")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--symmetry-floor",
        choices=("none", "generators", "full"),
        default="none",
    )
    parser.add_argument(
        "--pattern-manifest",
        type=Path,
        action="append",
        default=[],
    )
    parser.add_argument(
        "--entry-symmetry-breaking",
        choices=("none", "generators"),
        default="none",
    )
    args = parser.parse_args()

    group_sizes = (
        tuple(int(token) for token in args.group_sizes.split(","))
        if args.group_sizes
        else None
    )
    cnf, obstruction = matching_obstruction_cnf(
        args.separator_size,
        group_sizes,
        maximum_matching=args.maximum_matching,
    )
    base_clauses = len(cnf.clauses)
    system = EquationSystem(6, 3)
    candidates = candidate_variable_map()
    mode_rank = {"none": 0, "generators": 1, "full": 2}
    summaries = []
    for manifest_path in args.manifests:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        mode = max(
            (
                str(manifest.get("symmetry_images", "none")),
                args.symmetry_floor,
            ),
            key=mode_rank.__getitem__,
        )
        transforms = symmetry_transforms(mode)
        before = len(cnf.clauses)
        for row in manifest["rows"]:
            cnf.clauses.extend(
                symmetry_blocking_clauses(
                    system,
                    candidates,
                    {
                        tuple(int(value) for value in arc)
                        for arc in row["candidate_arcs"]
                    },
                    {
                        int(index)
                        for index in row["positive_entries"]
                    },
                    {
                        int(index)
                        for index in row["negative_entries"]
                    },
                    transforms,
                )
            )
        summaries.append(
            {
                "manifest": str(manifest_path),
                "rows": len(manifest["rows"]),
                "symmetry_images": mode,
                "clauses_added": len(cnf.clauses) - before,
            }
        )
    certified_pattern_statuses = {
        "certified",
        "certified_with_exact_fallback",
        "unconditional_laurent_contradiction",
    }
    full_transforms = symmetry_transforms("full")
    pattern_summaries = []
    for pattern_manifest_path in args.pattern_manifest:
        pattern_manifest = json.loads(
            pattern_manifest_path.read_text(encoding="utf-8")
        )
        before = len(cnf.clauses)
        certified_rows = [
            row
            for row in pattern_manifest["rows"]
            if row["status"] in certified_pattern_statuses
        ]
        for row in certified_rows:
            cnf.clauses.extend(
                symmetry_blocking_clauses(
                    system,
                    candidates,
                    {
                        (vertex, colour, int(neighbour))
                        for vertex, pattern_row in enumerate(row["pattern"])
                        for colour, neighbour in enumerate(pattern_row)
                    },
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
                "maximum_matching": args.maximum_matching,
                "separator_size": args.separator_size,
                "odd_groups": obstruction["odd_groups"],
                "group_sizes": (
                    list(group_sizes) if group_sizes is not None else None
                ),
                "manifests": summaries,
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
