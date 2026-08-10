"""Verify the exact 24-model orbit-44 support boundary.

This verifier starts from the independently established predecessor CNF,
enumerates every factor assignment under selector 44, and checks that the
result is exactly the 24-clause subset mined from the later UNSAT formula.
It also binds every clause verbatim to one of the two independently
verified algebraic support-symmetry clause sets.

This proves completeness for the stated Boolean rule relaxation.  The
separate DRAT replay proves that the materialized conditioned CNF is UNSAT.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time

from pysat.formula import CNF
from pysat.solvers import Solver


EXPECTED_BASE_SHA256 = (
    "e9482392e9c6568190ba6a1a4cd6c23025e7c8fd5a17fc5ff0c582cf864adb35"
)
SELECTOR = 276
EDGE_VARIABLES = 231
ROLE_EDGE_VARIABLES = 77


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cycle_partition(
    first: tuple[tuple[int, int], ...],
    second: tuple[tuple[int, int], ...],
) -> tuple[int, ...]:
    adjacency = [[] for _ in range(14)]
    for left, right in (*first, *second):
        adjacency[left].append(right)
        adjacency[right].append(left)
    if any(len(neighbours) != 2 for neighbours in adjacency):
        raise AssertionError("factor union is not a 2-factor")
    seen = set()
    sizes = []
    for start in range(14):
        if start in seen:
            continue
        previous = -1
        current = start
        size = 0
        while current not in seen:
            seen.add(current)
            size += 1
            first_next, second_next = adjacency[current]
            following = (
                second_next if first_next == previous else first_next
            )
            previous, current = current, following
        sizes.append(size)
    return tuple(sorted(sizes))


def decode_clause(
    clause: tuple[int, ...],
    eligible_edges: tuple[tuple[int, int], ...],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if (
        len(clause) != 21
        or any(literal >= 0 for literal in clause)
        or any(abs(literal) > EDGE_VARIABLES for literal in clause)
    ):
        raise AssertionError("unexpected support no-good shape")
    roles = []
    for role in range(3):
        lower = role * ROLE_EDGE_VARIABLES
        variables = sorted(
            abs(literal)
            for literal in clause
            if lower < abs(literal) <= lower + ROLE_EDGE_VARIABLES
        )
        if len(variables) != 7:
            raise AssertionError("support no-good is not three factors")
        roles.append(
            tuple(
                eligible_edges[variable - lower - 1]
                for variable in variables
            )
        )
    return tuple(roles)


def verified_clause_source(
    clause_path: Path,
    verifier_path: Path,
) -> set[tuple[int, ...]]:
    clause_set = json.loads(clause_path.read_text(encoding="utf-8"))
    verifier = json.loads(verifier_path.read_text(encoding="utf-8"))
    if (
        clause_set.get("status")
        != "verified_binomial_support_no_goods_clause_set"
        or verifier.get("verified") is not True
        or verifier.get("status")
        != "binomial_support_no_good_clause_set_verified"
        or Path(verifier["augmentation"]) != clause_path
        or verifier["augmentation_sha256"] != sha256(clause_path)
    ):
        raise AssertionError("source certificate binding changed")
    clauses = {
        tuple(map(int, item))
        for item in clause_set["support_no_goods"]
    }
    if (
        len(clauses)
        != int(clause_set["candidate_support_no_goods"])
        or len(clauses) != int(verifier["support_no_goods"])
    ):
        raise AssertionError("source clause cardinality changed")
    return clauses


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit16_"
            "symbinomial300_orbit49support1.cnf"
        ),
    )
    parser.add_argument(
        "--core",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            "probe_extension_clause_core.json"
        ),
    )
    parser.add_argument(
        "--support1",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_probe_"
            "symmetry_support1_clause_set.json"
        ),
    )
    parser.add_argument(
        "--support1-verifier",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_probe_"
            "symmetry_support1_clause_set_verified.json"
        ),
    )
    parser.add_argument(
        "--support2",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_probe_"
            "symmetry_support2_clause_set.json"
        ),
    )
    parser.add_argument(
        "--support2-verifier",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_probe_"
            "symmetry_support2_clause_set_verified.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_"
            "core24_models_verified.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    started = time.perf_counter()
    if sha256(args.base_cnf) != EXPECTED_BASE_SHA256:
        raise AssertionError("predecessor CNF hash changed")

    core = json.loads(args.core.read_text(encoding="utf-8"))
    core_clauses = {
        tuple(map(int, clause)) for clause in core["clauses"]
    }
    if (
        core.get("status")
        != "UNSAT_deletion_irredundant_extension_clause_core"
        or int(core.get("assumption", -1)) != SELECTOR
        or len(core_clauses) != 24
        or int(core.get("irredundant_core_clauses", -1)) != 24
    ):
        raise AssertionError("core subset summary changed")

    source_sets = [
        verified_clause_source(args.support1, args.support1_verifier),
        verified_clause_source(args.support2, args.support2_verifier),
    ]
    memberships = [
        sum(clause in source for clause in core_clauses)
        for source in source_sets
    ]
    if memberships != [8, 16]:
        raise AssertionError("support-source memberships changed")
    if any(
        not any(clause in source for source in source_sets)
        for clause in core_clauses
    ):
        raise AssertionError("core clause lacks verified source")

    formula = CNF(from_file=str(args.base_cnf))
    if formula.nv != 324 or len(formula.clauses) != 4_716_109:
        raise AssertionError("predecessor DIMACS dimensions changed")
    enumerated = set()
    with Solver(
        name="cadical195", bootstrap_with=formula.clauses
    ) as solver:
        while solver.solve(assumptions=[SELECTOR]):
            positive = {
                literal
                for literal in solver.get_model()
                if 1 <= literal <= EDGE_VARIABLES
            }
            if len(positive) != 21:
                raise AssertionError("model does not select three factors")
            no_good = tuple(
                -variable for variable in sorted(positive, reverse=True)
            )
            if no_good in enumerated:
                raise AssertionError("model blocking failed")
            enumerated.add(no_good)
            solver.add_clause(list(no_good))
        if solver.solve(assumptions=[SELECTOR]):
            raise AssertionError("enumeration did not terminate UNSAT")
    if enumerated != core_clauses:
        raise AssertionError("exact orbit-44 model set changed")

    cycles = (
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (8, 9, 10, 11, 12, 13),
    )
    full_edges = {
        tuple(sorted((cycle[index], cycle[(index + 1) % len(cycle)])))
        for cycle in cycles
        for index in range(len(cycle))
    }
    eligible_edges = tuple(
        edge
        for edge in itertools.combinations(range(14), 2)
        if edge not in full_edges
    )
    if len(eligible_edges) != ROLE_EDGE_VARIABLES:
        raise AssertionError("eligible-edge enumeration changed")
    decoded = [
        decode_clause(clause, eligible_edges)
        for clause in sorted(core_clauses)
    ]
    unique_factors = [
        len({row[role] for row in decoded}) for role in range(3)
    ]
    pair_partitions = {
        f"{first}{second}": {
            "+".join(map(str, partition)): count
            for partition, count in sorted(
                Counter(
                    cycle_partition(row[first], row[second])
                    for row in decoded
                ).items()
            )
        }
        for first, second in ((0, 1), (0, 2), (1, 2))
    }
    if (
        unique_factors != [1, 16, 16]
        or pair_partitions
        != {
            "01": {"6+8": 24},
            "02": {"6+8": 24},
            "12": {"4+4+6": 24},
        }
    ):
        raise AssertionError("24-model factor classification changed")

    payload = {
        "verified": True,
        "status": "c4_c4_c6_orbit44_core24_models_verified",
        "scope": (
            "fresh exhaustive factor-assignment enumeration under "
            "selector 44 and verbatim binding of all 24 models to two "
            "independently verified algebraic support clause sets"
        ),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "base_cnf_variables": formula.nv,
        "base_cnf_clauses": len(formula.clauses),
        "selector": SELECTOR,
        "orbit": 44,
        "enumerated_factor_models": len(enumerated),
        "core": str(args.core),
        "core_sha256": sha256(args.core),
        "core_clauses": len(core_clauses),
        "support_source_memberships": memberships,
        "unique_factors_by_role": unique_factors,
        "pair_cycle_partitions": pair_partitions,
        "exact_model_clause_set_match": True,
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
