"""Verify the pairwise rank-one mixed-second-jet resonance cliques exactly."""

from __future__ import annotations

import json
from itertools import combinations_with_replacement, product
from math import gcd

import sympy as sp

Covector = tuple[int, int, int]


def canonical(vector: Covector) -> Covector:
    divisor = 0
    for entry in vector:
        divisor = gcd(divisor, abs(entry))
    reduced = tuple(entry // divisor for entry in vector)
    first = next(entry for entry in reduced if entry)
    if first < 0:
        reduced = tuple(-entry for entry in reduced)
    return reduced  # type: ignore[return-value]


def resonant(left: Covector, right: Covector) -> bool:
    for missing in range(3):
        if left[missing] or right[missing]:
            continue
        remaining = [index for index in range(3) if index != missing]
        if left[remaining[0]] * right[remaining[0]] == left[remaining[1]] * right[remaining[1]]:
            return True
    return False


def support(vector: Covector) -> tuple[int, ...]:
    return tuple(index for index, entry in enumerate(vector) if entry)


def balanced_pair(vector: Covector) -> bool:
    occupied = support(vector)
    return len(occupied) == 2 and vector[occupied[0]] == vector[occupied[1]]


def axis_triple(triple: tuple[Covector, Covector, Covector]) -> bool:
    return {support(vector) for vector in triple} == {(0,), (1,), (2,)}


def symbolic_support_two() -> dict[str, str]:
    x, y, z, w = sp.symbols("x y z w", nonzero=True)
    coefficient_matrix = sp.Matrix([[x, -y], [y, -x]])
    determinant = sp.factor(coefficient_matrix.det())
    expected = -(x - y) * (x + y)
    if sp.expand(determinant - expected) != 0:
        raise AssertionError((determinant, expected))
    if sp.factor((x * z - y * w).subs({z: y, w: x})) != 0:
        raise AssertionError("reciprocal partner parametrization failed")
    return {
        "third_partner_matrix": str(coefficient_matrix.tolist()),
        "determinant": str(determinant),
        "nonzero_sum_branch": "x=y",
    }


def exact_box() -> dict[str, int]:
    vectors = sorted(
        {
            canonical(vector)
            for vector in product(range(-2, 3), repeat=3)
            if vector != (0, 0, 0) and sum(vector) != 0
        }
    )
    compatible_triples = 0
    balanced_triples = 0
    axis_triples = 0
    for triple in combinations_with_replacement(vectors, 3):
        if not all(resonant(triple[i], triple[j]) for i in range(3) for j in range(i + 1, 3)):
            continue
        compatible_triples += 1
        if triple[0] == triple[1] == triple[2] and balanced_pair(triple[0]):
            balanced_triples += 1
        elif axis_triple(triple):
            axis_triples += 1
        else:
            raise AssertionError(("unclassified triple", triple))

    axes = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    fourth_axis_partners = sum(all(resonant(axis, vector) for axis in axes) for vector in vectors)
    if fourth_axis_partners:
        raise AssertionError(fourth_axis_partners)
    return {
        "projective_covectors": len(vectors),
        "compatible_triples": compatible_triples,
        "balanced_triples": balanced_triples,
        "axis_triples": axis_triples,
        "fourth_axis_partners": fourth_axis_partners,
    }


def main() -> None:
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "symbolic_support_two": symbolic_support_two(),
                "exact_projective_box_audit": exact_box(),
                "r_at_least_four_pattern": "one repeated balanced coordinate-pair covector",
                "r_equals_three_extra_pattern": "the three coordinate covectors",
                "cofactor_realizability_proved": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
