"""Audit exact Smith-form signed-lattice transport."""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from integer_constant_lattice import IntegerConstantLattice  # noqa: E402
from integer_signed_lattice import IntegerSignedLattice  # noqa: E402

from analyze_fourteen_vertex_partial_circuit_factor_cegar import (  # noqa: E402
    partial_relation_clauses,
)
from analyze_fourteen_vertex_portal_determinant_lattice import (  # noqa: E402
    contiguous_cycles,
)


def combine(
    coefficients: list[int], rows: list[list[int]]
) -> list[int]:
    return [
        sum(
            coefficient * row[position]
            for coefficient, row in zip(
                coefficients, rows, strict=True
            )
        )
        for position in range(len(rows[0]))
    ]


def check_constructed_points(
    rows: list[list[int]],
    *,
    seed: int,
    trials: int,
) -> tuple[int, int]:
    lattice = IntegerSignedLattice(rows)
    rng = random.Random(seed)
    points = 0
    parity_checks = 0
    for _ in range(trials):
        source = [
            rng.randrange(-4, 5) for _row in rows
        ]
        vector = combine(source, rows)
        recovered = lattice.coordinates(vector)
        if recovered is None:
            raise AssertionError("constructed lattice point was rejected")
        if combine(recovered, rows) != vector:
            raise AssertionError("recovered coordinates did not replay")
        points += 1
        if not lattice.has_odd_kernel:
            if (sum(source) - sum(recovered)) % 2:
                raise AssertionError("transported parity changed")
            expected = -1 if sum(source) % 2 else 1
            if lattice.transported_sign(vector) != expected:
                raise AssertionError("transported sign changed")
            parity_checks += 1
    return points, parity_checks


def main() -> None:
    started = time.perf_counter()
    curated = [
        {
            "rows": [[1, 0], [0, 1]],
            "rank": 2,
            "invariants": (1, 1),
            "odd_kernel": False,
        },
        {
            "rows": [[2, 0], [0, 2]],
            "rank": 2,
            "invariants": (2, 2),
            "odd_kernel": False,
        },
        {
            "rows": [[2], [1]],
            "rank": 1,
            "invariants": (1,),
            "odd_kernel": True,
        },
        {
            "rows": [[1, 1], [1, -1], [1, 1]],
            "rank": 2,
            "invariants": (1, 2),
            "odd_kernel": False,
        },
    ]
    curated_checked = 0
    constructed_points = 0
    parity_checks = 0
    for case_id, case in enumerate(curated):
        rows = case["rows"]
        lattice = IntegerSignedLattice(rows)
        if lattice.rank != case["rank"]:
            raise AssertionError("curated Smith rank changed")
        if lattice.invariant_factors != case["invariants"]:
            raise AssertionError("curated Smith invariants changed")
        if lattice.has_odd_kernel != case["odd_kernel"]:
            raise AssertionError("curated kernel parity changed")
        points, parities = check_constructed_points(
            rows, seed=7000 + case_id, trials=80
        )
        constructed_points += points
        parity_checks += parities
        curated_checked += 1

    nonsaturated = IntegerSignedLattice([[2, 0], [0, 2]])
    if nonsaturated.coordinates([1, 0]) is not None:
        raise AssertionError("nonsaturated nonmember was accepted")
    if nonsaturated.coordinates([2, 2]) is None:
        raise AssertionError("nonsaturated member was rejected")

    rng = random.Random(20260725)
    random_matrices = 0
    for matrix_id in range(80):
        generators = rng.randrange(1, 6)
        width = rng.randrange(1, 7)
        rows = [
            [rng.randrange(-2, 3) for _ in range(width)]
            for _ in range(generators)
        ]
        if not any(any(row) for row in rows):
            rows[0][0] = 1
        points, parities = check_constructed_points(
            rows, seed=9000 + matrix_id, trials=20
        )
        constructed_points += points
        parity_checks += parities
        random_matrices += 1

    source_path = Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit8_"
        "partial_minimal_circuit_lattice.json"
    )
    source = json.loads(source_path.read_text(encoding="utf-8"))
    cycles = contiguous_cycles(tuple(map(int, source["partition"])))
    factors = tuple(
        tuple(tuple(map(int, item)) for item in factor)
        for factor in source["singleton_factors"]
    )
    _clauses, symbolic_rows, _origins = partial_relation_clauses(
        factors, cycles
    )
    variables = sorted(
        {
            variable
            for row in symbolic_rows
            for variable, _coefficient in row
        }
    )
    positions = {
        variable: position
        for position, variable in enumerate(variables)
    }
    rows = []
    for symbolic in symbolic_rows:
        row = [0] * len(variables)
        for variable, coefficient in symbolic:
            row[positions[variable]] = int(coefficient)
        rows.append(row)
    hard_lattice = IntegerSignedLattice(rows)
    if (
        len(rows) != 22
        or len(variables) != 76
        or hard_lattice.rank != 22
        or hard_lattice.invariant_factors != (1,) * 22
        or hard_lattice.kernel_basis
        or hard_lattice.has_odd_kernel
    ):
        raise AssertionError("hard order-14 Smith data changed")
    points, parities = check_constructed_points(
        rows, seed=141422, trials=200
    )
    constructed_points += points
    parity_checks += parities

    rational_consistent = IntegerConstantLattice(
        [[2], [1]], [Fraction(4), Fraction(2)]
    )
    if rational_consistent.has_inconsistent_kernel:
        raise AssertionError("consistent rational constants rejected")
    if (
        rational_consistent.transported_constant([1]) != 2
        or rational_consistent.transported_constant([2]) != 4
        or rational_consistent.transported_constant([-1])
        != Fraction(1, 2)
    ):
        raise AssertionError("rational transport changed")
    rational_inconsistent = IntegerConstantLattice(
        [[2], [1]], [Fraction(3), Fraction(2)]
    )
    if not rational_inconsistent.has_inconsistent_kernel:
        raise AssertionError("inconsistent rational constants accepted")

    payload = {
        "verified": True,
        "status": "integer_signed_lattice_transport_verified",
        "scope": (
            "Smith identities, invariant factors, kernel parity, exact "
            "membership coordinates, transported signs, nonsaturated "
            "membership, rational constants, and the order-14 "
            "22-relation instance"
        ),
        "curated_matrices_checked": curated_checked,
        "random_matrices_checked": random_matrices,
        "constructed_lattice_points_checked": constructed_points,
        "transported_parities_checked": parity_checks,
        "order14_relations": len(rows),
        "order14_relation_variables": len(variables),
        "order14_rank": hard_lattice.rank,
        "order14_invariant_factors": list(
            hard_lattice.invariant_factors
        ),
        "order14_kernel_dimension": len(hard_lattice.kernel_basis),
        "rational_constant_cases_checked": 2,
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    output = Path("tmp/integer_signed_lattice_transport_verified.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
