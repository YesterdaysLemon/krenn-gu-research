"""Verify the quantitative nonroot tangent-companion endpoint obstruction."""

from __future__ import annotations

import json
from itertools import product
from math import ceil, gcd

import sympy as sp

Covector = tuple[int, int, int]


def canonical(row: Covector) -> Covector:
    divisor = 0
    for value in row:
        divisor = gcd(divisor, abs(value))
    answer = tuple(value // divisor for value in row)
    first = next(value for value in answer if value)
    if first < 0:
        answer = tuple(-value for value in answer)
    return answer  # type: ignore[return-value]


def kernel_basis(row: Covector) -> tuple[Covector, Covector]:
    pivot = next(index for index, value in enumerate(row) if value)
    free = [index for index in range(3) if index != pivot]
    basis = []
    for coordinate in free:
        vector = [0, 0, 0]
        vector[coordinate] = row[pivot]
        vector[pivot] = -row[coordinate]
        basis.append(tuple(vector))
    return basis[0], basis[1]  # type: ignore[return-value]


def coordinate_restriction_zero(row: Covector, coordinate: int) -> bool:
    return all(vector[coordinate] == 0 for vector in kernel_basis(row))


def coordinate_axis(row: Covector, coordinate: int) -> bool:
    return all(value == 0 for index, value in enumerate(row) if index != coordinate)


def symbolic_hyperplane_check() -> dict[str, object]:
    vectors = {
        canonical(row)
        for row in product(range(-2, 3), repeat=3)
        if row != (0, 0, 0) and sum(row) != 0
    }
    checks = 0
    for row in vectors:
        for coordinate in range(3):
            actual = coordinate_restriction_zero(row, coordinate)
            expected = coordinate_axis(row, coordinate)
            if actual != expected:
                raise AssertionError((row, coordinate, actual, expected))
            checks += 1

    x0, x1, x2 = sp.symbols("x0 x1 x2")
    tensor_factor = sp.kronecker_product(sp.Matrix([x0, x1]), sp.Matrix([x2, 1]))
    if tensor_factor == sp.zeros(4, 1):
        raise AssertionError("generic tensor product vanished")
    return {"projective_covectors": len(vectors), "restriction_checks": checks, "generic_tensor_shape": list(tensor_factor.shape)}


def count_ledger() -> dict[str, object]:
    tested = 0
    feasible = 0
    impossible = 0
    for roots in range(2, 31):
        for endpoints in range(roots):
            lower = roots - endpoints
            possible = 3 * lower <= roots
            bound = endpoints >= ceil(2 * roots / 3)
            if possible != bound:
                raise AssertionError((roots, endpoints, possible, bound))
            if possible:
                counts = (lower, lower, roots - 2 * lower)
                if min(counts) < lower or sum(counts) != roots:
                    raise AssertionError((roots, endpoints, counts))
                if any(roots - count > endpoints for count in counts):
                    raise AssertionError((roots, endpoints, counts))
                feasible += 1
            else:
                impossible += 1
            tested += 1
    return {"root_endpoint_pairs": tested, "feasible": feasible, "impossible": impossible, "maximum_roots": 30}


def main() -> None:
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "hyperplane_tensor_criterion": symbolic_hyperplane_check(),
                "axis_count_ledger": count_ledger(),
                "endpoint_lower_bound": "t >= ceiling(2r/3)",
                "axis_multiplicity_lower_bound": "n_c >= r-t",
                "nonaxis_upper_bound": "m <= 3t-2r",
                "root_root_channels_excluded": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
