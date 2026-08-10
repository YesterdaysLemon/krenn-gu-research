"""Incrementally solve fixed compatibility-vertex-cover separator orbits.

For a fixed set S of task vertices, saying S covers the compatibility graph
only adds the binary clauses forbidding compatibility edges wholly outside
S.  Activation literals let one SAT instance share the expensive global
support formula and certified whole-pattern blockers across all S6 x S3
separator representatives.
"""

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
from pathlib import Path

from candidate_killer_cover_sat import candidate_support_problem
from candidate_matching_obstruction_sat import separator_orbit_representatives
from global_candidate_laurent_cegar import (
    candidate_variable_map,
    symmetry_blocking_clauses,
    symmetry_transforms,
)
from krenn_gu.search_witness import EquationSystem


def separator_tasks(row_masks: tuple[int, ...]) -> set[tuple[int, int]]:
    return {
        (vertex, colour)
        for vertex, mask in enumerate(row_masks)
        for colour in range(3)
        if mask & (1 << colour)
    }


def write_checkpoint(
    output: Path,
    separator_size: int,
    solver_name: str,
    rows: list[dict[str, object]],
    orbit_count: int,
    clauses: int,
    variables: int,
) -> None:
    counts = Counter(str(row["status"]) for row in rows)
    payload = {
        "separator_size": separator_size,
        "solver": solver_name,
        "orbits": orbit_count,
        "completed_orbits": len(rows),
        "status_counts": dict(counts),
        "certified": (
            len(rows) == orbit_count
            and counts == Counter({"UNSAT": orbit_count})
        ),
        "variables": variables,
        "clauses": clauses,
        "rows": rows,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--separator-size", type=int, required=True)
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
    parser.add_argument("--first-orbit", type=int, default=0)
    parser.add_argument("--last-orbit", type=int)
    parser.add_argument("--reverse", action="store_true")
    parser.add_argument("--stop-on-sat", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    from pysat.solvers import Solver

    system = EquationSystem(6, 3)
    cnf, candidates = candidate_support_problem()
    if candidates != candidate_variable_map():
        raise AssertionError("candidate variable numbering changed")

    full_transforms = symmetry_transforms("full")
    certified_statuses = {
        "certified",
        "certified_with_exact_fallback",
        "unconditional_laurent_contradiction",
    }
    for manifest_path in args.pattern_manifest:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for row in manifest["rows"]:
            if row["status"] not in certified_statuses:
                continue
            arcs = {
                (vertex, colour, int(neighbour))
                for vertex, pattern_row in enumerate(row["pattern"])
                for colour, neighbour in enumerate(pattern_row)
            }
            cnf.clauses.extend(
                symmetry_blocking_clauses(
                    system,
                    candidates,
                    arcs,
                    set(),
                    set(),
                    full_transforms,
                )
            )

    representatives = separator_orbit_representatives(args.separator_size)
    last = (
        len(representatives)
        if args.last_orbit is None
        else min(args.last_orbit, len(representatives))
    )
    indices = list(range(args.first_orbit, last))
    if args.reverse:
        indices.reverse()

    selectors: dict[int, int] = {}
    for orbit in indices:
        selector = cnf.variable()
        selectors[orbit] = selector
        separator = separator_tasks(representatives[orbit])
        tasks = tuple(
            (vertex, colour)
            for vertex in range(6)
            for colour in range(3)
        )
        for first_index, (first_vertex, first_colour) in enumerate(tasks):
            if (first_vertex, first_colour) in separator:
                continue
            for second_vertex, second_colour in tasks[first_index + 1 :]:
                if (
                    first_vertex == second_vertex
                    or (second_vertex, second_colour) in separator
                ):
                    continue
                cnf.add(
                    -selector,
                    -candidates[
                        (first_vertex, first_colour, second_vertex)
                    ],
                    -candidates[
                        (second_vertex, second_colour, first_vertex)
                    ],
                )

    rows: list[dict[str, object]] = []
    with Solver(name=args.solver, bootstrap_with=cnf.clauses) as solver:
        for orbit in indices:
            started = time.perf_counter()
            sat = solver.solve(assumptions=[selectors[orbit]])
            elapsed = time.perf_counter() - started
            model = solver.get_model() if sat else None
            try:
                statistics = solver.accum_stats()
            except NotImplementedError:
                statistics = None
            row = {
                "orbit": orbit,
                "row_masks": list(representatives[orbit]),
                "separator_tasks": [
                    list(task)
                    for task in sorted(
                        separator_tasks(representatives[orbit])
                    )
                ],
                "status": "SAT" if sat else "UNSAT",
                "elapsed_seconds": elapsed,
                "statistics": statistics,
                "model": model,
            }
            rows.append(row)
            write_checkpoint(
                args.output,
                args.separator_size,
                args.solver,
                rows,
                len(indices),
                len(cnf.clauses),
                cnf.variable_count,
            )
            print(
                f"orbit={orbit} status={row['status']} "
                f"elapsed={elapsed:.3f}s",
                flush=True,
            )
            if sat and args.stop_on_sat:
                break

    if len(rows) != len(indices) or any(
        row["status"] != "UNSAT" for row in rows
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
