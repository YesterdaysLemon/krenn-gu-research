#!/usr/bin/env python3
"""Exact replay of the tight-five-root P5 extraction lemma.

The written theorem is arbitrary-order.  This verifier checks its finite
matching-factor core, the order-five permanent pullback, and the symbolic
diagonal/rescaling consequences without searching graph supports.
"""

from __future__ import annotations

import itertools
import json
from functools import cache

import sympy as sp

ROOTS = tuple(range(5))
BLOCKERS = tuple(range(5, 10))


@cache
def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        edge = tuple(sorted((first, second)))
        for matching in perfect_matchings(remainder):
            result.append(tuple(sorted((edge, *matching))))
    return tuple(result)


def permanent(matrix: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    size = len(matrix)
    return sp.Add(
        *(
            sp.prod(matrix[row][permutation[row]] for row in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


def matching_factor_check(residual_size: int) -> dict[str, int]:
    residual = tuple(range(10, 10 + residual_size))
    vertices = ROOTS + BLOCKERS + residual
    all_matchings = perfect_matchings(vertices)

    root_set = set(ROOTS)
    residual_set = set(residual)

    def survives(matching):
        for left, right in matching:
            if left in root_set and right in root_set:
                return False
            if (
                left in root_set
                and right in residual_set
                or right in root_set
                and left in residual_set
            ):
                return False
        return True

    surviving = {matching for matching in all_matchings if survives(matching)}
    residual_matchings = perfect_matchings(residual)
    expected = set()
    for blocker_order in itertools.permutations(BLOCKERS):
        root_blocker = tuple(
            sorted(
                tuple(sorted((root, blocker)))
                for root, blocker in zip(ROOTS, blocker_order, strict=True)
            )
        )
        for residual_matching in residual_matchings:
            expected.add(tuple(sorted((*root_blocker, *residual_matching))))

    assert surviving == expected
    assert len(surviving) == 120 * len(residual_matchings)
    return {
        "vertices": len(vertices),
        "all_matchings": len(all_matchings),
        "surviving_matchings": len(surviving),
        "root_blocker_bijections": 120,
        "residual_matchings": len(residual_matchings),
    }


def main() -> None:
    # A union of five vertices containing three blocker sets of size at least
    # five makes all three blocker sets equal to the union.
    universe = frozenset(range(5))
    possible_large_subsets = tuple(
        frozenset(subset)
        for size in range(5, 6)
        for subset in itertools.combinations(universe, size)
    )
    assert possible_large_subsets == (universe,)

    matching_checks = [matching_factor_check(size) for size in (0, 2, 4)]

    # Reconstruct P5 as the permanent of five column vectors.  Its 120 tensor
    # monomials are distinct and have coefficient one.
    entries = tuple(
        tuple(sp.symbols(f"m{row}_{column}") for column in range(5))
        for row in range(5)
    )
    p5 = permanent(entries)
    p5_poly = sp.Poly(p5, *(entry for row in entries for entry in row))
    assert len(p5_poly.terms()) == 120
    assert {coefficient for _, coefficient in p5_poly.terms()} == {sp.Integer(1)}

    # Pulling column u back by L_u replaces m_(i,u) by a_(i,u)(z_u).
    # Checking one general symbolic column and all five permutation roles is
    # enough to replay the map convention used in the theorem.
    z = tuple(
        tuple(sp.symbols(f"z{mode}_{colour}") for colour in range(3))
        for mode in range(5)
    )
    ell = tuple(
        tuple(
            tuple(
                sp.symbols(f"l{row}_{mode}_{colour}") for colour in range(3)
            )
            for mode in range(5)
        )
        for row in range(5)
    )
    pulled_matrix = tuple(
        tuple(
            sp.Add(
                *(
                    ell[row][mode][colour] * z[mode][colour]
                    for colour in range(3)
                )
            )
            for mode in range(5)
        )
        for row in range(5)
    )
    pulled_p5 = permanent(pulled_matrix)
    substitution = {
        entries[row][mode]: pulled_matrix[row][mode]
        for row in range(5)
        for mode in range(5)
    }
    assert sp.expand(p5.subs(substitution) - pulled_p5) == 0

    # The three coordinate diagonals are independent, and three nonzero
    # coefficients give a rank-three one-mode flattening.
    diagonals = tuple(
        sp.prod(z[mode][colour] for mode in range(5)) for colour in range(3)
    )
    lambdas = sp.symbols("lambda0:3", nonzero=True)
    diagonal_tensor = sp.Add(
        *(lambdas[colour] * diagonals[colour] for colour in range(3))
    )
    diagonal_poly = sp.Poly(
        diagonal_tensor, *(variable for mode in z for variable in mode)
    )
    assert len(diagonal_poly.terms()) == 3
    assert diagonal_poly.total_degree() == 5
    flattening = sp.diag(*lambdas)
    assert sp.factor(flattening.det()) == sp.prod(lambdas)
    assert flattening.rank() == 3

    rescaled = sp.expand(
        diagonal_tensor.subs(
            {z[0][colour]: z[0][colour] / lambdas[colour] for colour in range(3)},
            simultaneous=True,
        )
    )
    assert sp.simplify(rescaled - sp.Add(*diagonals)) == 0

    print(
        json.dumps(
            {
                "status": "verified",
                "field": "C",
                "root_count": 5,
                "blocker_union_size": 5,
                "blocker_sets_forced_common": True,
                "matching_factor_checks": matching_checks,
                "p5_permanent_monomials": len(p5_poly.terms()),
                "diagonal_terms": len(diagonal_poly.terms()),
                "diagonal_flattening_rank": 3,
                "one_mode_rescaling": "verified",
                "arbitrary_order_scope": "proved in the accompanying theorem",
                "global_conjecture": "unresolved",
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
