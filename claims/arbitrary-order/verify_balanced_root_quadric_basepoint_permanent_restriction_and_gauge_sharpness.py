"""Primary exact checks for the balanced root-quadric basepoint bridge."""

from __future__ import annotations

from functools import cache
from itertools import permutations
from math import factorial

import sympy as sp

Vertices = tuple[int, ...]
Matching = tuple[tuple[int, int], ...]


@cache
def perfect_matchings(vertices: Vertices) -> tuple[Matching, ...]:
    """Return every labelled perfect matching of ``vertices``."""
    if not vertices:
        return ((),)
    first = vertices[0]
    result: list[Matching] = []
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            result.append(((first, partner),) + tail)
    return tuple(result)


def permanent(matrix: list[list[sp.Expr]]) -> sp.Expr:
    """Compute one small unsigned permanent directly."""
    size = len(matrix)
    return sp.expand(
        sum(
            sp.prod(matrix[row][sigma[row]] for row in range(size))
            for sigma in permutations(range(size))
        )
    )


def labelled_edge_weight(
    left: int,
    right: int,
    roots: set[int],
    root_edges: dict[tuple[int, int], sp.Symbol],
    cross_edges: dict[tuple[int, int], sp.Symbol],
    nonroot_edges: dict[tuple[int, int], sp.Symbol],
) -> sp.Expr:
    """Return the symbolic label for one balanced complete-graph edge."""
    edge = (min(left, right), max(left, right))
    if edge in root_edges:
        return root_edges[edge]
    if edge in nonroot_edges:
        return nonroot_edges[edge]
    root, nonroot = (left, right) if left in roots else (right, left)
    return cross_edges[(root, nonroot)]


def assert_balanced_sector_residue() -> dict[int, tuple[int, int]]:
    """Replay the all-cross residue after killing every root edge."""
    ledger: dict[int, tuple[int, int]] = {}
    for m in range(2, 6):
        roots = tuple(range(m))
        root_set = set(roots)
        nonroots = tuple(range(m, 2 * m))
        root_edges = {
            edge: sp.Symbol(f"q_{edge[0]}_{edge[1]}")
            for edge in (
                (left, right)
                for left in roots
                for right in roots
                if left < right
            )
        }
        cross_edges = {
            (left, right): sp.Symbol(f"h_{left}_{right - m}")
            for left in roots
            for right in nonroots
        }
        nonroot_edges = {
            edge: sp.Symbol(f"d_{edge[0] - m}_{edge[1] - m}")
            for edge in (
                (left, right)
                for left in nonroots
                for right in nonroots
                if left < right
            )
        }

        full = sp.Add(
            *(
                sp.prod(
                    labelled_edge_weight(
                        left,
                        right,
                        root_set,
                        root_edges,
                        cross_edges,
                        nonroot_edges,
                    )
                    for left, right in matching
                )
                for matching in perfect_matchings(tuple(range(2 * m)))
            )
        )
        killed = sp.expand(full.subs({value: 0 for value in root_edges.values()}))
        all_cross = permanent(
            [[cross_edges[(root, nonroot)] for nonroot in nonroots] for root in roots]
        )
        assert sp.expand(killed - all_cross) == 0

        surviving = sum(
            1
            for matching in perfect_matchings(tuple(range(2 * m)))
            if all(
                not ({left, right} <= root_set)
                for left, right in matching
            )
        )
        assert surviving == factorial(m)
        ledger[m] = (len(perfect_matchings(tuple(range(2 * m)))), surviving)
    return ledger


def construction_matrices() -> tuple[sp.Matrix, ...]:
    """Return the exact normalized eight-vertex gauge fixture."""
    return (
        sp.eye(3),
        sp.Matrix([[-1, 0, 0], [0, 1, -1], [0, 0, -1]]),
        sp.Matrix([[0, 0, -1], [0, -1, 0], [1, 0, 0]]),
        sp.Matrix([[0, -1, 0], [0, 1, 1], [-1, 0, 1]]),
        sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, -1]]),
        sp.diag(1, 1, -1),
        sp.Matrix([[-1, 0, 0], [0, 0, 1], [0, 1, 0]]),
        sp.Matrix(
            [
                [0, 0, sp.Rational(1, 6)],
                [sp.Rational(1, 3), 0, 0],
                [0, sp.Rational(1, 3), 0],
            ]
        ),
    )


def tensor_coefficient(
    word: tuple[int, ...], edge_blocks: dict[tuple[int, int], sp.Matrix]
) -> sp.Expr:
    """Evaluate one coordinate coefficient by all perfect matchings."""
    return sp.simplify(
        sum(
            sp.prod(
                edge_blocks[(left, right)][word[left], word[right]]
                for left, right in matching
            )
            for matching in perfect_matchings(tuple(range(len(word))))
        )
    )


def assert_fixed_gauge_sharpness() -> dict[str, object]:
    """Check the normalized all-rank-drop fixture and its gauge caveat."""
    gauges = construction_matrices()
    blocks = {
        (left, right): gauges[left].T * gauges[right]
        for left in range(8)
        for right in range(left + 1, 8)
    }

    gauge_determinants = tuple(sp.det(matrix) for matrix in gauges)
    assert gauge_determinants == (
        1,
        1,
        -1,
        1,
        -1,
        -1,
        1,
        sp.Rational(1, 54),
    )
    block_determinants = {sp.det(matrix) for matrix in blocks.values()}
    assert block_determinants == {
        -1,
        1,
        -sp.Rational(1, 54),
        sp.Rational(1, 54),
    }

    pure = tuple(tensor_coefficient((colour,) * 8, blocks) for colour in range(3))
    mixed_word = (0, 0, 1, 1, 1, 1, 1, 1)
    mixed = tensor_coefficient(mixed_word, blocks)
    assert pure == (1, 1, 1)
    assert mixed == -1

    x0, x1, x2 = sp.symbols("x0 x1 x2")
    variables = (x0, x1, x2)
    vector = sp.Matrix(variables)
    monomials = (x0**2, x1**2, x2**2, x0 * x1, x0 * x2, x1 * x2)
    columns = []
    for left in range(4):
        for right in range(left + 1, 4):
            quadratic = sp.Poly(
                sp.expand((vector.T * blocks[(left, right)] * vector)[0]),
                *variables,
            )
            columns.append(
                sp.Matrix([quadratic.coeff_monomial(monomial) for monomial in monomials])
            )
    coefficient_matrix = sp.Matrix.hstack(*columns)
    assert coefficient_matrix == sp.Matrix(
        [
            [-1, 0, 0, 0, 0, -1],
            [1, -1, 1, -1, 1, -1],
            [-1, 0, 1, 0, -2, 0],
            [0, 0, -1, 0, 1, 0],
            [0, 0, -1, 0, 1, 1],
            [-1, 0, 1, 1, 0, 0],
        ]
    )
    assert coefficient_matrix.det() == -1

    identity = sp.eye(3)
    for (left, right), block in blocks.items():
        synchronized = gauges[left].inv().T * block * gauges[right].inv()
        assert synchronized == identity

    return {
        "gauge_determinants": gauge_determinants,
        "block_determinants": tuple(sorted(block_determinants)),
        "pure_coefficients": pure,
        "mixed_00111111": mixed,
        "root_quadric_determinant": coefficient_matrix.det(),
        "latent_common_form_edges": len(blocks),
    }


def assert_low_order_interfaces() -> dict[str, int]:
    """Check the elementary low-order tensors used by imported obstructions."""
    p2 = sp.Matrix([[0, 1], [1, 0]])
    delta3 = sp.eye(3)
    assert p2.rank() == 2
    assert delta3.rank() == 3

    p3: dict[tuple[int, int, int], sp.Rational] = {}
    for sigma in permutations(range(3)):
        p3[sigma] = sp.Rational(1)
    signs = (
        ((1, 1, 1), 1),
        ((1, 1, -1), -1),
        ((1, -1, 1), -1),
        ((-1, 1, 1), -1),
    )
    decomposition: dict[tuple[int, int, int], sp.Rational] = {}
    for vector, sign in signs:
        for index in (
            (first, second, third)
            for first in range(3)
            for second in range(3)
            for third in range(3)
        ):
            value = sp.Rational(sign, 4)
            value *= vector[index[0]] * vector[index[1]] * vector[index[2]]
            decomposition[index] = decomposition.get(index, sp.Rational(0)) + value
    assert all(
        decomposition.get(index, 0) == p3.get(index, 0)
        for index in set(decomposition) | set(p3)
    )
    return {"rank_p2": p2.rank(), "rank_delta3": delta3.rank(), "p3_terms": 4}


def main() -> None:
    sectors = assert_balanced_sector_residue()
    sharpness = assert_fixed_gauge_sharpness()
    low_order = assert_low_order_interfaces()
    print("balanced root-quadric basepoint bridge primary checks: PASS")
    print(f"  balanced matching sectors (all, all-cross): {sectors}")
    print(f"  fixed-gauge sharpness fixture: {sharpness}")
    print(f"  low-order interfaces: {low_order}")


if __name__ == "__main__":
    main()
