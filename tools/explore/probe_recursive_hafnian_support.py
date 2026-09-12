"""Bounded probe for the recursive hafnian zero-pattern relaxation.

This program reports SAT/UNSAT solver outcomes.  Without a separately checked
proof trace, an UNSAT result is computational evidence rather than a promoted
computer-assisted theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys as _bootstrap_sys
import time
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

from pysat.solvers import (  # noqa: E402
    Cadical153,
    Cadical195,
    Glucose4,
    Kissat404,
)

from krenn_gu.recursive_hafnian_support import (  # noqa: E402
    RecursiveHafnianSupportInstance,
    build_recursive_hafnian_support_cnf,
)

SOLVERS = {
    "cadical153": Cadical153,
    "cadical195": Cadical195,
    "glucose4": Glucose4,
    "kissat404": Kissat404,
}


def sha256_file(path: _BootstrapPath) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def decode_model(
    instance: RecursiveHafnianSupportInstance,
    model: list[int],
) -> dict[str, object]:
    positive = {literal for literal in model if literal > 0}
    return {
        "edge_supports": {
            str(colour): [
                list(edge)
                for (candidate_colour, edge), variable in sorted(
                    instance.edge_variables.items()
                )
                if candidate_colour == colour and variable in positive
            ]
            for colour in range(3)
        },
        "nonzero_hafnian_counts": {
            str(colour): sum(
                variable in positive
                for (candidate_colour, _subset), variable in
                instance.hafnian_variables.items()
                if candidate_colour == colour
            )
            for colour in range(3)
        },
        "nonzero_hafnian_sets": {
            str(colour): [
                sorted(subset)
                for (candidate_colour, subset), variable in sorted(
                    instance.hafnian_variables.items(),
                    key=lambda item: (item[0][0], len(item[0][1]), sorted(item[0][1])),
                )
                if candidate_colour == colour and variable in positive
            ]
            for colour in range(3)
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--solver", choices=sorted(SOLVERS), default="cadical195")
    parser.add_argument("--output", type=_BootstrapPath, required=True)
    parser.add_argument("--dimacs", type=_BootstrapPath)
    parser.add_argument("--build-only", action="store_true")
    parser.add_argument("--two-part-only", action="store_true")
    parser.add_argument("--no-singleton-cancellation", action="store_true")
    parser.add_argument(
        "--cycle-type",
        help="partition of n/2, e.g. 3+2; fixes one matching in colours 0 and 1",
    )
    parser.add_argument(
        "--third-cycle-type",
        help=(
            "partition of n/2 for a colour-2 matching; valid as an exhaustive "
            "subsplit only when --cycle-type is all shared edges"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cycle_type = (
        tuple(int(part) for part in args.cycle_type.split("+"))
        if args.cycle_type
        else None
    )
    third_cycle_type = (
        tuple(int(part) for part in args.third_cycle_type.split("+"))
        if args.third_cycle_type
        else None
    )
    started = time.perf_counter()
    instance = build_recursive_hafnian_support_cnf(
        args.n,
        two_part_only=args.two_part_only,
        no_singleton_cancellation=args.no_singleton_cancellation,
        matching_cycle_type=cycle_type,
        third_matching_cycle_type=third_cycle_type,
    )
    built_seconds = time.perf_counter() - started

    dimacs = args.dimacs
    if dimacs is None:
        dimacs = args.output.with_suffix(".cnf")
    dimacs.parent.mkdir(parents=True, exist_ok=True)
    instance.cnf.to_file(str(dimacs))

    result = "NOT_SOLVED"
    decoded = None
    solve_seconds = 0.0
    if not args.build_only:
        solver_started = time.perf_counter()
        solver_type = SOLVERS[args.solver]
        with solver_type(bootstrap_with=instance.cnf.clauses) as solver:
            satisfiable = solver.solve()
            result = "SAT" if satisfiable else "UNSAT"
            if satisfiable:
                decoded = decode_model(instance, solver.get_model())
        solve_seconds = time.perf_counter() - solver_started

    payload = {
        "model": "recursive_hafnian_zero_pattern",
        "scope": "necessary_condition_for_all_diagonal_complex_witnesses",
        "n": args.n,
        "flags": {
            "two_part_only": args.two_part_only,
            "no_singleton_cancellation": args.no_singleton_cancellation,
            "matching_cycle_type": list(cycle_type) if cycle_type else None,
            "third_matching_cycle_type": (
                list(third_cycle_type) if third_cycle_type else None
            ),
        },
        "solver": args.solver,
        "result": result,
        "evidence": (
            "solver_status_without_independently_checked_proof_trace"
            if result == "UNSAT"
            else "explicit_boolean_model" if result == "SAT" else "instance_only"
        ),
        "variables": instance.pool.top,
        "clauses": len(instance.cnf.clauses),
        "clause_families": {
            "product_definition": instance.product_definition_clauses,
            "nonzero_accessibility": instance.nonzero_accessibility_clauses,
            "singleton_cancellation": instance.singleton_cancellation_clauses,
            "rainbow": instance.rainbow_clauses,
            "constant_words": 3,
            "matching_symmetry": instance.symmetry_clauses,
        },
        "build_seconds": round(built_seconds, 6),
        "solve_seconds": round(solve_seconds, 6),
        "dimacs": str(dimacs.resolve()),
        "dimacs_sha256": sha256_file(dimacs),
        "decoded_model": decoded,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
