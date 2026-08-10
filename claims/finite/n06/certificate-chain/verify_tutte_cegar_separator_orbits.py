"""Solve fixed task-separator orbits strengthened by global CEGAR clauses."""

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
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from candidate_matching_obstruction_sat import (
    fixed_separator_cnf,
    separator_orbit_representatives,
)
from global_candidate_laurent_cegar import (
    candidate_variable_map,
    symmetry_blocking_clauses,
    symmetry_transforms,
)
from krenn_gu.search_witness import EquationSystem


LEARNED_CLAUSES: list[tuple[int, ...]] = []


def initialize_worker(learned_clauses: list[tuple[int, ...]]) -> None:
    global LEARNED_CLAUSES
    LEARNED_CLAUSES = learned_clauses


def solve_orbit(
    item: tuple[int, tuple[int, ...], str],
) -> dict[str, object]:
    from pysat.solvers import Solver

    index, row_masks, solver_name = item
    cnf, metadata = fixed_separator_cnf(row_masks)
    cnf.clauses.extend(LEARNED_CLAUSES)
    started = time.perf_counter()
    with Solver(
        name=solver_name,
        bootstrap_with=cnf.clauses,
    ) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None
        try:
            statistics = solver.accum_stats()
        except NotImplementedError:
            statistics = None
    return {
        "orbit": index,
        **metadata,
        "status": "SAT" if sat else "UNSAT",
        "solver": solver_name,
        "variables": cnf.variable_count,
        "clauses": len(cnf.clauses),
        "learned_clauses": len(LEARNED_CLAUSES),
        "elapsed_seconds": time.perf_counter() - started,
        "statistics": statistics,
        "model": model,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--separator-size", type=int, required=True)
    parser.add_argument("manifests", type=Path, nargs="+")
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
        "--solver",
        choices=(
            "cadical195",
            "glucose42",
            "maplechrono",
            "mergesat3",
            "minisat22",
        ),
        default="cadical195",
    )
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    system = EquationSystem(6, 3)
    candidates = candidate_variable_map()
    mode_rank = {"none": 0, "generators": 1, "full": 2}
    learned_clauses: set[tuple[int, ...]] = set()
    manifest_summaries = []
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
        before = len(learned_clauses)
        for row in manifest["rows"]:
            learned_clauses.update(
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
        manifest_summaries.append(
            {
                "manifest": str(manifest_path),
                "rows": len(manifest["rows"]),
                "symmetry_images": mode,
                "new_clauses": len(learned_clauses) - before,
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
        before = len(learned_clauses)
        certified_rows = [
            row
            for row in pattern_manifest["rows"]
            if row["status"] in certified_pattern_statuses
        ]
        for row in certified_rows:
            learned_clauses.update(
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
                "new_clauses": len(learned_clauses) - before,
            }
        )
    learned_list = sorted(learned_clauses)
    representatives = separator_orbit_representatives(
        args.separator_size
    )
    items = [
        (index, row_masks, args.solver)
        for index, row_masks in enumerate(representatives)
    ]
    if args.jobs > 1:
        with ProcessPoolExecutor(
            max_workers=args.jobs,
            initializer=initialize_worker,
            initargs=(learned_list,),
        ) as executor:
            rows = list(executor.map(solve_orbit, items))
    else:
        initialize_worker(learned_list)
        rows = [solve_orbit(item) for item in items]
    counts = Counter(str(row["status"]) for row in rows)
    result = {
        "separator_size": args.separator_size,
        "orbits": len(rows),
        "manifests": manifest_summaries,
        "pattern_manifests": pattern_summaries,
        "learned_clauses": len(learned_list),
        "status_counts": dict(counts),
        "certified": counts == Counter({"UNSAT": len(rows)}),
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"wrote {args.output}: orbits={len(rows)} "
        f"counts={dict(counts)}"
    )
    if not result["certified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
