"""Exact symbolic replay of the P7 zeon harmonic-square Riccati theorem."""

from __future__ import annotations

from itertools import combinations

import sympy as sp

VERTICES = tuple(range(8))
EDGES = tuple(combinations(VERTICES, 2))
TRIPLES = tuple(combinations(VERTICES, 3))
FOUR_SETS = tuple(combinations(VERTICES, 4))
FIVE_SETS = tuple(combinations(VERTICES, 5))
BooleanForm = dict[frozenset[int], sp.Expr]


def boolean_add(left: BooleanForm, right: BooleanForm) -> BooleanForm:
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = sp.expand(out.get(monomial, 0) + coefficient)
        if out[monomial] == 0:
            del out[monomial]
    return out


def boolean_scale(scalar: sp.Expr, form: BooleanForm) -> BooleanForm:
    return {
        monomial: expanded
        for monomial, coefficient in form.items()
        if (expanded := sp.expand(scalar * coefficient)) != 0
    }


def boolean_mul(left: BooleanForm, right: BooleanForm) -> BooleanForm:
    out: BooleanForm = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            if left_monomial & right_monomial:
                continue
            monomial = left_monomial | right_monomial
            out[monomial] = sp.expand(
                out.get(monomial, 0) + left_coefficient * right_coefficient
            )
    return {
        monomial: coefficient
        for monomial, coefficient in out.items()
        if coefficient != 0
    }


def partial(vertex: int, form: BooleanForm) -> BooleanForm:
    return {
        monomial - {vertex}: coefficient
        for monomial, coefficient in form.items()
        if vertex in monomial
    }


def lowering(form: BooleanForm) -> BooleanForm:
    out: BooleanForm = {}
    for vertex in VERTICES:
        out = boolean_add(out, partial(vertex, form))
    return out


def forms_equal(left: BooleanForm, right: BooleanForm) -> bool:
    keys = set(left) | set(right)
    return all(
        sp.expand(left.get(key, 0) - right.get(key, 0)) == 0
        for key in keys
    )


def verify_corrected_leibniz() -> None:
    vertices = tuple(range(4))
    subsets = tuple(
        frozenset(subset)
        for size in range(5)
        for subset in combinations(vertices, size)
    )
    left_form = {
        subset: sp.Symbol(f"f_{''.join(map(str, sorted(subset))) or 'e'}")
        for subset in subsets
    }
    right_form = {
        subset: sp.Symbol(f"g_{''.join(map(str, sorted(subset))) or 'e'}")
        for subset in subsets
    }
    for vertex in vertices:
        product = boolean_mul(left_form, right_form)
        expected = boolean_add(
            boolean_mul(partial(vertex, left_form), right_form),
            boolean_mul(left_form, partial(vertex, right_form)),
        )
        correction = boolean_scale(
            -2,
            boolean_mul(
                {frozenset({vertex}): sp.Integer(1)},
                boolean_mul(
                    partial(vertex, left_form),
                    partial(vertex, right_form),
                ),
            ),
        )
        expected = boolean_add(expected, correction)
        assert forms_equal(partial(vertex, product), expected)


def verify_middle_harmonic_equivalence() -> None:
    raising = sp.Matrix(
        [
            [int(set(column) < set(row)) for column in FOUR_SETS]
            for row in FIVE_SETS
        ]
    )
    lowering_matrix = sp.Matrix(
        [
            [int(set(row) < set(column)) for column in FOUR_SETS]
            for row in TRIPLES
        ]
    )
    assert raising.shape == lowering_matrix.shape == (56, 70)
    assert raising.rank() == lowering_matrix.rank() == 56
    assert raising.col_join(lowering_matrix).rank() == 56


def verify_harmonic_square_and_contractions() -> None:
    edge_symbol = {
        edge: sp.Symbol(f"b_{edge[0]}{edge[1]}") for edge in EDGES
    }

    def b(left: int, right: int) -> sp.Expr:
        return edge_symbol[tuple(sorted((left, right)))]

    q_form = {
        frozenset(edge): coefficient for edge, coefficient in edge_symbol.items()
    }
    h_form = boolean_scale(sp.Rational(1, 2), boolean_mul(q_form, q_form))
    d_h = lowering(h_form)
    d_q = lowering(q_form)
    harmonic_right: BooleanForm = {}
    for vertex in VERTICES:
        local_square = boolean_mul(
            partial(vertex, q_form), partial(vertex, q_form)
        )
        harmonic_right = boolean_add(
            harmonic_right,
            boolean_mul(
                {frozenset({vertex}): sp.Integer(1)}, local_square
            ),
        )
    harmonic_left = boolean_mul(q_form, d_q)
    assert forms_equal(
        d_h, boolean_add(harmonic_left, boolean_scale(-1, harmonic_right))
    )

    row_sum = {
        vertex: sum(b(vertex, other) for other in VERTICES if other != vertex)
        for vertex in VERTICES
    }
    total = sum(row_sum.values())
    triangle = {}
    for triple in TRIPLES:
        i, j, k = triple
        expression = sp.expand(
            b(i, j) * row_sum[k]
            + b(i, k) * row_sum[j]
            + b(j, k) * row_sum[i]
            - 2
            * (
                b(i, j) * b(i, k)
                + b(i, j) * b(j, k)
                + b(i, k) * b(j, k)
            )
        )
        triangle[triple] = expression
        assert sp.expand(d_h[frozenset(triple)] - expression) == 0

    riccati = {}
    for i, j in EDGES:
        matrix_square = sum(
            b(i, k) * b(k, j)
            for k in VERTICES
            if k not in (i, j)
        )
        residual = sp.expand(
            matrix_square
            - (total / 2 - 2 * row_sum[i] - 2 * row_sum[j]) * b(i, j)
            - row_sum[i] * row_sum[j]
            - 2 * b(i, j) ** 2
        )
        riccati[(i, j)] = residual
        contracted_triangles = sum(
            triangle[tuple(sorted((i, j, k)))]
            for k in VERTICES
            if k not in (i, j)
        )
        assert sp.expand(contracted_triangles + 2 * residual) == 0

    vertex_residual = {}
    for i in VERTICES:
        br_i = sum(b(i, j) * row_sum[j] for j in VERTICES if j != i)
        edge_square_sum = sum(
            b(i, j) ** 2 for j in VERTICES if j != i
        )
        residual = sp.expand(
            br_i
            - edge_square_sum
            - row_sum[i] * (total / 2 - row_sum[i])
        )
        vertex_residual[i] = residual
        assert sp.expand(
            sum(
                riccati[tuple(sorted((i, j)))]
                for j in VERTICES
                if j != i
            )
            - 3 * residual
        ) == 0

    casimir = sp.expand(
        total**2
        - 4
        * (
            sum(value**2 for value in row_sum.values())
            - sum(value**2 for value in edge_symbol.values())
        )
    )
    assert sp.expand(2 * sum(vertex_residual.values()) + casimir) == 0


def main() -> None:
    verify_corrected_leibniz()
    verify_middle_harmonic_equivalence()
    verify_harmonic_square_and_contractions()
    print("PASS: corrected zeon Leibniz rule on a universal Boolean algebra")
    print("PASS: middle raising/lowering kernels agree and have dimension 14")
    print("PASS: primitive squares are exact zeon harmonic squares")
    print("PASS: matrix Riccati, vertex, and quadratic Casimir contractions")
    print("searches=0 finite_fields=0 graph_enumerations=0")
    print("SCOPE: complex primitive-square torus and global Krenn-Gu remain unresolved")


if __name__ == "__main__":
    main()
