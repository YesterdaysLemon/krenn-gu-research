"""Primary exact replay for primitive P7 additive-gauge rigidity."""

from __future__ import annotations

import itertools
import math

import sympy as sp

N = 8
VERTICES = tuple(range(N))
EDGES = tuple(itertools.combinations(VERTICES, 2))
TRIPLES = tuple(itertools.combinations(VERTICES, 3))


def boolean_add(
    left: dict[frozenset[int], sp.Expr],
    right: dict[frozenset[int], sp.Expr],
) -> dict[frozenset[int], sp.Expr]:
    """Add sparse elements of the square-free Boolean algebra."""
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = sp.expand(out.get(monomial, 0) + coefficient)
        if out[monomial] == 0:
            del out[monomial]
    return out


def boolean_scale(
    scalar: sp.Expr,
    value: dict[frozenset[int], sp.Expr],
) -> dict[frozenset[int], sp.Expr]:
    """Scale a sparse Boolean-algebra element."""
    return {
        monomial: sp.expand(scalar * coefficient)
        for monomial, coefficient in value.items()
        if coefficient != 0
    }


def boolean_mul(
    left: dict[frozenset[int], sp.Expr],
    right: dict[frozenset[int], sp.Expr],
) -> dict[frozenset[int], sp.Expr]:
    """Multiply modulo z_i^2=0."""
    out: dict[frozenset[int], sp.Expr] = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            if left_monomial & right_monomial:
                continue
            monomial = left_monomial | right_monomial
            out[monomial] = sp.expand(
                out.get(monomial, 0) + left_coefficient * right_coefficient
            )
    return {
        monomial: sp.expand(coefficient)
        for monomial, coefficient in out.items()
        if sp.expand(coefficient) != 0
    }


def boolean_power(
    value: dict[frozenset[int], sp.Expr], power: int
) -> dict[frozenset[int], sp.Expr]:
    """Take a nonnegative Boolean-algebra power."""
    out: dict[frozenset[int], sp.Expr] = {frozenset(): sp.Integer(1)}
    for _ in range(power):
        out = boolean_mul(out, value)
    return out


def lefschetz_matrix(source_degree: int, power: int) -> sp.Matrix:
    """Matrix of multiplication by ell^power in the Boolean algebra."""
    source = tuple(itertools.combinations(VERTICES, source_degree))
    target = tuple(itertools.combinations(VERTICES, source_degree + power))
    return sp.Matrix(
        [
            [
                math.factorial(power) if set(column).issubset(row) else 0
                for column in source
            ]
            for row in target
        ]
    )


def support_multiplication_matrix(support_size: int) -> sp.Matrix:
    """Matrix A_2 -> A_3 for U=sum_{i<support_size} z_i."""
    support = set(range(support_size))
    return sp.Matrix(
        [
            [
                1
                if set(edge).issubset(triple)
                and next(iter(set(triple) - set(edge))) in support
                else 0
                for edge in EDGES
            ]
            for triple in TRIPLES
        ]
    )


def inclusion_matrix(size: int, source_degree: int) -> sp.Matrix:
    """Unsigned one-step inclusion W_(r,r+1)(size)."""
    source = tuple(itertools.combinations(range(size), source_degree))
    target = tuple(itertools.combinations(range(size), source_degree + 1))
    return sp.Matrix(
        [
            [int(set(column).issubset(row)) for column in source]
            for row in target
        ]
    )


def complemented_lefschetz_matrix() -> sp.Matrix:
    """Return ell^2:A_3->A_5 after complementing the target basis."""
    return sp.Matrix(
        [
            [2 * int(not (set(row) & set(column))) for column in TRIPLES]
            for row in TRIPLES
        ]
    )


def main() -> None:
    """Run the exact symbolic checks."""
    b = {edge: sp.Symbol(f"b_{edge[0]}{edge[1]}") for edge in EDGES}
    u = tuple(sp.Symbol(f"u_{vertex}") for vertex in VERTICES)

    ell = {frozenset({vertex}): sp.Integer(1) for vertex in VERTICES}
    linear_u = {frozenset({vertex}): u[vertex] for vertex in VERTICES}
    quad_b = {frozenset(edge): b[edge] for edge in EDGES}
    direct_gauged = {
        frozenset(edge): b[edge] + u[edge[0]] + u[edge[1]] for edge in EDGES
    }
    derived_gauged = boolean_add(quad_b, boolean_mul(ell, linear_u))
    assert direct_gauged == derived_gauged

    primitive_difference = boolean_mul(
        ell,
        boolean_add(
            boolean_power(direct_gauged, 2),
            boolean_scale(-1, boolean_power(quad_b, 2)),
        ),
    )
    gauge_obstruction = boolean_mul(
        linear_u,
        boolean_add(boolean_scale(2, quad_b), boolean_mul(ell, linear_u)),
    )
    factored_difference = boolean_mul(boolean_power(ell, 2), gauge_obstruction)
    assert primitive_difference == factored_difference
    gauged_defect = boolean_mul(ell, boolean_power(direct_gauged, 2))
    base_defect = boolean_mul(ell, boolean_power(quad_b, 2))
    assert gauged_defect == boolean_add(base_defect, factored_difference)

    for triple in TRIPLES:
        i, j, k = triple
        expected = 2 * (
            u[i] * b[(j, k)]
            + u[j] * b[(i, k)]
            + u[k] * b[(i, j)]
            + u[i] * u[j]
            + u[i] * u[k]
            + u[j] * u[k]
        )
        actual = gauge_obstruction[frozenset(triple)]
        assert sp.expand(actual - expected) == 0

    lefschetz_3_5 = lefschetz_matrix(3, 2)
    lefschetz_2_5 = lefschetz_matrix(2, 3)
    assert lefschetz_3_5.shape == (56, 56)
    assert lefschetz_3_5.rank() == 56
    assert lefschetz_2_5.shape == (56, 28)
    assert lefschetz_2_5.rank() == 28

    target_five_sets = tuple(itertools.combinations(VERTICES, 5))
    target_index = {target: index for index, target in enumerate(target_five_sets)}
    complemented_rows = []
    for triple in TRIPLES:
        complement = tuple(vertex for vertex in VERTICES if vertex not in triple)
        complemented_rows.append(list(lefschetz_3_5.row(target_index[complement])))
    complemented = sp.Matrix(complemented_rows)
    kneser = complemented_lefschetz_matrix()
    assert complemented == kneser

    kneser_squared = kneser * kneser
    kneser_cubed = kneser_squared * kneser
    kneser_fourth = kneser_cubed * kneser
    identity_56 = sp.eye(56)
    assert (
        kneser_fourth
        - 12 * kneser_cubed
        - 220 * kneser_squared
        + 1056 * kneser
        + 2880 * identity_56
    ) == sp.zeros(56)
    assert (sp.trace(kneser), sp.trace(kneser_squared), sp.trace(kneser_cubed)) == (
        0,
        2240,
        0,
    )
    spectrum = {20: 1, -12: 7, 6: 20, -2: 28}
    assert sum(spectrum.values()) == 56
    for power, expected_trace in ((1, 0), (2, 2240), (3, 0)):
        assert sum(
            multiplicity * eigenvalue**power
            for eigenvalue, multiplicity in spectrum.items()
        ) == expected_trace
    determinant = math.prod(
        eigenvalue**multiplicity
        for eigenvalue, multiplicity in spectrum.items()
    )
    assert determinant == -(2**64) * 3**27 * 5
    inverse_numerator = (
        -kneser_cubed
        + 12 * kneser_squared
        + 220 * kneser
        - 1056 * identity_56
    )
    assert inverse_numerator * kneser == 2880 * identity_56

    support_ranks = {
        support_size: support_multiplication_matrix(support_size).rank()
        for support_size in range(1, N + 1)
    }
    assert all(support_ranks[support_size] == 28 for support_size in range(5, 9))
    assert all(support_ranks[support_size] < 28 for support_size in range(1, 5))

    for support_size in range(5, 9):
        for source_degree in (0, 1, 2):
            block = inclusion_matrix(support_size, source_degree)
            assert block.rank() == block.cols

    for support_size in range(1, 5):
        support = set(range(support_size))
        outside = set(VERTICES) - support
        substitutions = {u[vertex]: 0 for vertex in outside}
        for inside_vertex in support:
            for outside_edge in itertools.combinations(sorted(outside), 2):
                triple = frozenset({inside_vertex, *outside_edge})
                actual = sp.expand(gauge_obstruction[triple].subs(substitutions))
                expected = 2 * u[inside_vertex] * b[outside_edge]
                assert sp.expand(actual - expected) == 0

    star_coefficients = tuple(sp.Symbol(f"a_{vertex}") for vertex in range(1, N))
    lam = sp.Symbol("lambda")
    star = {
        frozenset({0, vertex}): star_coefficients[vertex - 1]
        for vertex in range(1, N)
    }
    star_u = {frozenset({0}): lam}
    gauged_star = boolean_add(star, boolean_mul(ell, star_u))
    assert boolean_power(star, 2) == {}
    assert boolean_power(gauged_star, 2) == {}
    for vertex in range(1, N):
        assert gauged_star[frozenset({0, vertex})] == (
            star_coefficients[vertex - 1] + lam
        )
    assert all(
        frozenset(edge) not in gauged_star
        for edge in itertools.combinations(range(1, N), 2)
    )

    incidence = sp.Matrix(
        [[int(vertex in edge) for vertex in VERTICES] for edge in EDGES]
    )
    assert incidence.rank() == 8
    assert incidence.T * incidence == 6 * sp.eye(8) + sp.ones(8)

    print("PASS: primitive additive-gauge rigidity and coordinate boundary")
    print(f"  rank(ell^2:A3->A5) = {lefschetz_3_5.rank()}")
    print(f"  rank(ell^3:A2->A5) = {lefschetz_2_5.rank()}")
    print("  spectrum(2 KG(8,3)) = 20^1, (-12)^7, 6^20, (-2)^28")
    print(f"  complemented determinant = {determinant}")
    print("  fixed cubic inverse for the quadratic Theta gauge system checked")
    print(f"  support ranks A2->A3 = {support_ranks}")
    print("  all 56 quadratic gauge equations checked symbolically")
    print("  nonzero gauge forces an independent complement of size at least four")
    print("  the exact star boundary family confirms the boundary is essential")
    print("  no search, floating point, or finite-field evidence used")


if __name__ == "__main__":
    main()
