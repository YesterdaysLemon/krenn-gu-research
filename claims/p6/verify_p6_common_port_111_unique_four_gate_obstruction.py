#!/usr/bin/env python3
"""Exact certificate excluding the unique four-gate rank-five branch."""

from __future__ import annotations

import itertools
import json

import sympy as sp

from verify_p6_common_port_111_rank_five_catalecticant import (
    BAD_NAMES,
    K_BASIS_INDICES,
    PAIRS,
    SPLIT_MINORS,
    VECTORS,
    canonical_factor,
    minimal_hitting_sets,
    product_two,
)

CYCLE_EDGES = ((1, 2), (2, 3), (3, 4), (4, 1))
UNIQUE_GATES = (0, 3, 5, 9)


def gate_matrix(edge: tuple[int, int]) -> sp.Matrix:
    result = sp.zeros(5, 5)
    left, right = edge
    result[left, right] = 1
    result[right, left] = 1
    return result


def coordinate_plane(indices: tuple[int, int, int]) -> sp.Matrix:
    return sp.eye(5)[:, indices]


def catalecticant_basis() -> list[list[int]]:
    bad = [product_two(VECTORS[left], VECTORS[right]) for left, right in BAD_NAMES]
    return [bad[index] for index in K_BASIS_INDICES]


def catalecticant_value(
    k_basis: list[list[int]], left: sp.Matrix, right: sp.Matrix
) -> sp.Matrix:
    result = sp.zeros(5, 5)
    for row, quadratic in enumerate(k_basis):
        for source_coordinate in range(5):
            value = 0
            for left_index, right_index in itertools.product(range(5), repeat=2):
                if len({source_coordinate, left_index, right_index}) < 3:
                    continue
                complement = tuple(
                    index
                    for index in range(5)
                    if index not in {source_coordinate, left_index, right_index}
                )
                value += (
                    left[left_index]
                    * right[right_index]
                    * quadratic[PAIRS.index(complement)]
                )
            result[row, source_coordinate] = sp.expand(value)
    return result


def symbolic_catalecticant(
    k_basis: list[list[int]],
) -> tuple[sp.Matrix, tuple[sp.Symbol, ...], tuple[sp.Symbol, ...]]:
    b = sp.symbols("b0:5")
    c = sp.symbols("c0:5")
    return catalecticant_value(k_basis, sp.Matrix(b), sp.Matrix(c)), b, c


def main() -> None:
    gates = {edge: gate_matrix(edge) for edge in CYCLE_EDGES}
    identity = sp.eye(5)

    # Each gate is a rank-two hyperbolic form with the displayed coordinate
    # radical.  A zero projection therefore identifies a whole radical plane.
    for edge, matrix in gates.items():
        complement = tuple(index for index in range(5) if index not in edge)
        radical = coordinate_plane(complement)
        assert matrix.rank() == 2
        assert matrix * radical == sp.zeros(5, 3)
        assert radical.rank() == 3

    # If one plane is the radical of an edge, the opposite gate forces the
    # other plane to the opposite radical; the following adjacent gate is then
    # visibly nonzero.  Symmetry covers a zero projection on either side.
    radical_contradictions = []
    for edge_index, edge in enumerate(CYCLE_EDGES):
        opposite = CYCLE_EDGES[(edge_index + 2) % 4]
        adjacent = CYCLE_EDGES[(edge_index + 1) % 4]
        left_radical = coordinate_plane(
            tuple(index for index in range(5) if index not in edge)
        )
        right_radical = coordinate_plane(
            tuple(index for index in range(5) if index not in opposite)
        )
        restriction = left_radical.T * gates[adjacent] * right_radical
        assert restriction != sp.zeros(3, 3)
        radical_contradictions.append(int(max(abs(value) for value in restriction)))

    # The only independent two-sets of the four-cycle are the two parity
    # classes.  Smaller zero sets leave all nonzero coordinate restrictions
    # on one line and cannot span a three-dimensional dual together with x0.
    cycle_vertices = (1, 2, 3, 4)
    independent_sets = []
    for size in range(5):
        for subset in itertools.combinations(cycle_vertices, size):
            if all(not ({left, right} <= set(subset)) for left, right in CYCLE_EDGES):
                independent_sets.append(subset)
    maximum_independent_sets = [
        subset for subset in independent_sets if len(subset) == 2
    ]
    assert maximum_independent_sets == [(1, 3), (2, 4)]

    even = coordinate_plane((0, 2, 4))
    odd = coordinate_plane((0, 1, 3))
    for plane in (even, odd):
        assert all(
            plane.T * matrix * plane == sp.zeros(3, 3) for matrix in gates.values()
        )
    assert any(even.T * matrix * odd != sp.zeros(3, 3) for matrix in gates.values())
    assert any(odd.T * matrix * even != sp.zeros(3, 3) for matrix in gates.values())

    # Rebuild the split-minor hypergraph and its unique four-cover.
    k_basis = catalecticant_basis()
    symbolic, b_variables, c_variables = symbolic_catalecticant(k_basis)
    variables = b_variables + c_variables
    factors: list[sp.Poly] = []
    hyperedges = []
    for rows, columns in SPLIT_MINORS:
        determinant = sp.expand(symbolic.extract(rows, columns).det())
        _constant, raw_factors = sp.factor_list(determinant, *variables)
        factor_ids = []
        for factor, exponent in raw_factors:
            assert exponent == 1
            normalized = canonical_factor(factor, variables)
            if normalized not in factors:
                factors.append(normalized)
            factor_ids.append(factors.index(normalized))
        hyperedges.append(tuple(sorted(factor_ids)))
    covers = minimal_hitting_sets(sorted(set(hyperedges)), len(factors))
    four_covers = [
        tuple(index for index in range(len(factors)) if mask & (1 << index))
        for mask in covers
        if mask.bit_count() == 4
    ]
    assert four_covers == [UNIQUE_GATES]

    expected_gates = (
        b_variables[3] * c_variables[4] + b_variables[4] * c_variables[3],
        b_variables[1] * c_variables[4] + b_variables[4] * c_variables[1],
        b_variables[1] * c_variables[2] + b_variables[2] * c_variables[1],
        b_variables[2] * c_variables[3] + b_variables[3] * c_variables[2],
    )
    assert tuple(factors[index] for index in UNIQUE_GATES) == tuple(
        canonical_factor(expression, variables) for expression in expected_gates
    )

    # One value in each alternating plane violates the full rank-two condition.
    even_value = catalecticant_value(k_basis, identity[:, 0], identity[:, 2])
    odd_value = catalecticant_value(k_basis, identity[:, 0], identity[:, 1])
    assert even_value == sp.Matrix(
        (
            (0, 2, 0, 0, 0),
            (0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0),
            (0, 0, 0, -2, 0),
            (0, 0, 0, -1, 1),
        )
    )
    assert odd_value == sp.Matrix(
        (
            (0, 0, 2, 0, 0),
            (0, 0, 0, 0, 0),
            (0, 0, 0, 0, 2),
            (0, 0, 0, 0, 0),
            (0, 0, 0, -1, 1),
        )
    )
    even_minor = even_value.extract((0, 3, 4), (1, 3, 4)).det()
    odd_minor = odd_value.extract((0, 2, 4), (2, 3, 4)).det()
    assert even_minor == -4
    assert odd_minor == 4
    assert even_value.rank() == odd_value.rank() == 3

    print(
        json.dumps(
            {
                "status": "verified",
                "field": "Q (hence characteristic zero)",
                "unique_four_gate_cover": list(UNIQUE_GATES),
                "forced_plane_pairs": ["even/even", "odd/odd"],
                "radical_case_contradictions": radical_contradictions,
                "even_catalecticant_minor": int(even_minor),
                "odd_catalecticant_minor": int(odd_minor),
                "remaining_minimal_covers": len(covers) - 1,
                "p6_to_delta3_decided": False,
                "global_conjecture_resolved": False,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
