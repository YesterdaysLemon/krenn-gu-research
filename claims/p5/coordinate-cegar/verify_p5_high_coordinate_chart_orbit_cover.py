#!/usr/bin/env python3
"""Independently reconstruct a high-coordinate P5 chart-orbit cover."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pysat.solvers import Solver

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])

from krenn_gu import p5_high_coordinate as HIGH
from krenn_gu import p5_pair_support_semantics as SEMANTICS
import verify_p5_high_coordinate_chart_ledgers as LEDGER


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def transformed_mask(mask: int, colours: tuple[int, ...]) -> int:
    return sum(
        1 << colours[colour]
        for colour in SEMANTICS.COLOURS
        if mask & (1 << colour)
    )


def transformed_supports(
    supports: tuple[tuple[int, ...], ...],
    modes: tuple[int, ...],
    sources: tuple[int, ...],
    colours: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    result = [
        [0 for _source in SEMANTICS.SOURCES]
        for _mode in SEMANTICS.MODES
    ]
    for mode in SEMANTICS.MODES:
        for source in SEMANTICS.SOURCES:
            result[modes[mode]][sources[source]] = transformed_mask(
                supports[mode][source],
                colours,
            )
    return tuple(tuple(row) for row in result)


def independent_chart_orbit(
    pool,
    branch: str,
    closure: tuple[tuple[int, ...], ...],
    tree: tuple[tuple[int, int, int], ...],
) -> tuple[tuple[int, ...], ...]:
    clauses = set()
    for permutation in itertools.permutations((1, 2, 3, 4)):
        modes = (0,) + permutation
        for sources, colours in HIGH.source_colour_stabilizer(branch):
            moved_closure = transformed_supports(
                closure,
                modes,
                sources,
                colours,
            )
            moved_tree = tuple(
                (
                    modes[mode],
                    sources[source],
                    colours[colour],
                )
                for mode, source, colour in tree
            )
            clauses.add(
                HIGH.chart_clause(
                    pool,
                    moved_closure,
                    moved_tree,
                    branch,
                )
            )
    return tuple(sorted(clauses))


def checked_source(
    metadata: dict,
    label: str,
) -> tuple[Path, dict]:
    path = Path(metadata["path"])
    if not path.is_file():
        raise FileNotFoundError(f"{label} source is missing: {path}")
    observed = file_sha256(path)
    if observed != metadata["sha256"]:
        raise AssertionError(
            f"{label} source hash changed: {path}"
        )
    state = json.loads(path.read_text(encoding="utf-8"))
    if state.get("status") != metadata.get("status"):
        raise AssertionError(
            f"{label} source status changed: {path}"
        )
    return path, state


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--require-unsat", action="store_true")
    parser.add_argument(
        "--skip-record-validation",
        action="store_true",
        help="reconstruct clauses without regenerating algebra sources",
    )
    parser.add_argument("--rerun-singular", action="store_true")
    parser.add_argument("--fresh-limit", type=int)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument(
        "--singular-timeout",
        type=float,
        default=240,
    )
    args = parser.parse_args()
    if (
        args.jobs <= 0
        or args.singular_timeout <= 0
        or (args.fresh_limit is not None and args.fresh_limit <= 0)
    ):
        raise ValueError("invalid orbit-cover verifier arguments")

    primary_raw = args.state.read_bytes()
    primary = json.loads(primary_raw)
    branch = primary.get("branch")
    if branch not in HIGH.BRANCH_BACKBONES:
        raise ValueError("primary state has an unsupported branch")
    metadata = primary["metadata"]

    allowed = SEMANTICS.finite_field_local_signatures()
    cnf, pool = SEMANTICS.build_pair_support_cnf(allowed)
    branch_metadata = HIGH.add_branch_restriction(
        cnf,
        pool,
        allowed,
        branch,
    )
    lex_leaders = HIGH.add_stabilizer_lex_leaders(
        cnf,
        pool,
        branch,
    )
    base_clauses = len(cnf.clauses)

    clauses: set[tuple[int, ...]] = set()
    tasks = []
    representative_counts: Counter[str] = Counter()
    raw_clause_counts: Counter[str] = Counter()

    def consume(
        records: list[dict],
        label: str,
        transport: bool,
        require_zero_forest: bool = False,
    ) -> None:
        representative_counts[label] += len(records)
        for index, record in enumerate(records):
            if require_zero_forest and record.get(
                "gauge_tree"
            ) not in ([], ()):
                raise AssertionError(
                    f"{label} record {index} is not zero-forest"
                )
            if args.skip_record_validation:
                closure = LEDGER.normalized_supports(
                    record["closure_supports"]
                )
                tree = LEDGER.normalized_tree(
                    record["gauge_tree"]
                )
                clause = HIGH.chart_clause(
                    pool,
                    closure,
                    tree,
                    branch,
                )
            else:
                clause, task = LEDGER.validate_record(
                    branch,
                    pool,
                    record,
                )
                tasks.append(task)
                closure = LEDGER.normalized_supports(
                    record["closure_supports"]
                )
                tree = LEDGER.normalized_tree(
                    record["gauge_tree"]
                )
            moved = (
                independent_chart_orbit(
                    pool,
                    branch,
                    closure,
                    tree,
                )
                if transport
                else (clause,)
            )
            if transport and clause not in moved:
                raise AssertionError(
                    f"{label} orbit lost representative {index}"
                )
            raw_clause_counts[label] += len(moved)
            clauses.update(moved)

    for source_metadata in metadata.get(
        "transformed_seed_sources", []
    ):
        _path, state = checked_source(
            source_metadata,
            "transformed",
        )
        consume(
            state.get("records", []),
            "transformed",
            False,
        )

    for source_metadata in metadata.get(
        "zero_forest_orbit_sources", []
    ):
        _path, state = checked_source(
            source_metadata,
            "zero_forest_orbit",
        )
        consume(
            state.get("records", []),
            "zero_forest_orbit",
            True,
            require_zero_forest=True,
        )

    for source_metadata in metadata.get(
        "chart_orbit_sources", []
    ):
        _path, state = checked_source(
            source_metadata,
            "chart_orbit",
        )
        consume(
            state.get("records", []),
            "chart_orbit",
            True,
        )

    consume(
        primary.get("records", []),
        "primary",
        bool(metadata.get("learn_chart_orbits")),
    )

    cnf.extend([list(clause) for clause in sorted(clauses)])
    solver_results = {}
    for solver_name in ("cadical195", "glucose4"):
        with Solver(
            name=solver_name,
            bootstrap_with=cnf.clauses,
        ) as solver:
            solver_results[solver_name] = (
                "UNSAT" if not solver.solve() else "SAT"
            )
    if args.require_unsat and any(
        result != "UNSAT" for result in solver_results.values()
    ):
        raise AssertionError("required chart-orbit cover remains SAT")

    fresh_results = []
    if args.rerun_singular:
        if args.skip_record_validation:
            raise ValueError(
                "fresh replay requires record validation"
            )
        selected = (
            tasks
            if args.fresh_limit is None
            else tasks[: args.fresh_limit]
        )
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            fresh_results = list(
                executor.map(
                    lambda task: LEDGER.rerun(
                        task,
                        args.singular_timeout,
                    ),
                    selected,
                )
            )
        if not all(result["verified"] for result in fresh_results):
            raise AssertionError("fresh Singular orbit replay failed")

    print(
        json.dumps(
            {
                "verified": True,
                "branch": branch,
                "primary_state": args.state.as_posix(),
                "primary_state_sha256": hashlib.sha256(
                    primary_raw
                ).hexdigest(),
                "primary_status": primary.get("status"),
                "catalogue_signatures": len(allowed),
                "branch_restriction": branch_metadata,
                "lex_leaders": lex_leaders,
                "representative_records": dict(
                    representative_counts
                ),
                "raw_transported_clauses": dict(raw_clause_counts),
                "unique_cover_clauses": len(clauses),
                "variables": pool.top,
                "base_clauses": base_clauses,
                "total_clauses": len(cnf.clauses),
                "record_sources_regenerated": (
                    0
                    if args.skip_record_validation
                    else len(tasks)
                ),
                "solver_results": solver_results,
                "fresh_singular_replays": len(fresh_results),
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
