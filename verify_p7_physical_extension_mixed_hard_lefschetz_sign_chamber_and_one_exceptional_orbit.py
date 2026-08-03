"""Exact verifier for the P7 mixed-Lefschetz extension obstructions.

The same-sign chamber exclusion itself invokes the cited mixed Hard
Lefschetz theorem.  This script checks every problem-specific algebraic
translation and the complete characteristic-zero one-exceptional orbit.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp

LEAVES = tuple(range(7))
EDGES = tuple(combinations(LEAVES, 2))
FIVE_SETS = tuple(combinations(LEAVES, 5))
BooleanForm = dict[frozenset[int], sp.Expr]


def boolean_add(left: BooleanForm, right: BooleanForm) -> BooleanForm:
    """Add sparse elements of the square-free Boolean algebra."""
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = sp.expand(out.get(monomial, 0) + coefficient)
        if out[monomial] == 0:
            del out[monomial]
    return out


def boolean_scale(scalar: sp.Expr, form: BooleanForm) -> BooleanForm:
    """Scale a sparse Boolean form."""
    return {
        monomial: expanded
        for monomial, coefficient in form.items()
        if (expanded := sp.expand(scalar * coefficient)) != 0
    }


def boolean_mul(left: BooleanForm, right: BooleanForm) -> BooleanForm:
    """Multiply modulo z_i^2=0."""
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


def forms_equal(left: BooleanForm, right: BooleanForm) -> bool:
    """Compare two formal Boolean forms coefficientwise."""
    keys = set(left) | set(right)
    return all(sp.expand(left.get(key, 0) - right.get(key, 0)) == 0 for key in keys)


def mixed_lefschetz_matrix(a: tuple[sp.Expr, ...]) -> sp.Matrix:
    """Complemented matrix of multiplication by ell^2 A from A2 to A5."""
    return sp.Matrix(
        [
            [
                2 * sum(a[vertex] for vertex in LEAVES if vertex not in edge + row)
                if set(edge).isdisjoint(row)
                else 0
                for edge in EDGES
            ]
            for row in EDGES
        ]
    )


def direct_boolean_mixed_matrix(a: tuple[sp.Expr, ...]) -> sp.Matrix:
    """Build the same map by literal Boolean multiplication."""
    ell = {frozenset({vertex}): sp.Integer(1) for vertex in LEAVES}
    a_form = {
        frozenset({vertex}): coefficient
        for vertex, coefficient in enumerate(a)
    }
    cubic = boolean_mul(boolean_mul(ell, ell), a_form)
    rows = []
    for row_edge in EDGES:
        five_set = frozenset(vertex for vertex in LEAVES if vertex not in row_edge)
        row = []
        for edge in EDGES:
            edge_form = {frozenset(edge): sp.Integer(1)}
            row.append(boolean_mul(edge_form, cubic).get(five_set, 0))
        rows.append(row)
    return sp.Matrix(rows)


def main() -> None:
    ell = {frozenset({vertex}): sp.Integer(1) for vertex in LEAVES}
    f_symbols = {edge: sp.Symbol(f"f_{edge[0]}{edge[1]}") for edge in EDGES}
    a_symbols = tuple(sp.Symbol(f"a_{vertex}") for vertex in LEAVES)
    t = sp.Symbol("t", nonzero=True)
    f_form = {frozenset(edge): coefficient for edge, coefficient in f_symbols.items()}
    a_form = {
        frozenset({vertex}): coefficient
        for vertex, coefficient in enumerate(a_symbols)
    }
    k_form = boolean_add(
        boolean_scale(2, boolean_mul(ell, a_form)),
        boolean_scale(t, f_form),
    )

    # Universal source of the necessary mixed-Lefschetz kernel.
    identity_left = boolean_mul(ell, boolean_mul(f_form, k_form))
    identity_right = boolean_add(
        boolean_scale(
            2,
            boolean_mul(boolean_mul(ell, ell), boolean_mul(a_form, f_form)),
        ),
        boolean_scale(t, boolean_mul(ell, boolean_mul(f_form, f_form))),
    )
    assert forms_equal(identity_left, identity_right)

    generic_matrix = mixed_lefschetz_matrix(a_symbols)
    assert generic_matrix == direct_boolean_mixed_matrix(a_symbols)

    # Intrinsic weighted-Kneser anticommutator formula.
    kneser_7 = sp.Matrix(
        [
            [int(set(edge).isdisjoint(row)) for edge in EDGES]
            for row in EDGES
        ]
    )
    total = sum(a_symbols)
    edge_weights = sp.diag(*(sum(a_symbols[vertex] for vertex in edge) for edge in EDGES))
    assert generic_matrix == 2 * (
        total * kneser_7 - edge_weights * kneser_7 - kneser_7 * edge_weights
    )

    # The symmetric Kähler anchor has the claimed exact signature.
    symmetric_matrix = mixed_lefschetz_matrix((sp.Integer(1),) * 7)
    assert symmetric_matrix == 6 * kneser_7
    lambda_symbol = sp.Symbol("lambda")
    assert sp.factor(symmetric_matrix.charpoly(lambda_symbol).as_expr()) == (
        (lambda_symbol - 60)
        * (lambda_symbol + 24) ** 6
        * (lambda_symbol - 6) ** 14
    )

    # Complete S6 block calculation for A=(p,q,q,q,q,q,q).
    p, q = sp.symbols("p q", nonzero=True)
    special_matrix = mixed_lefschetz_matrix((p,) + (q,) * 6)
    star_edges = tuple(edge for edge in EDGES if 0 in edge)
    internal_edges = tuple(edge for edge in EDGES if 0 not in edge)
    reordered_edges = star_edges + internal_edges
    edge_index = {edge: index for index, edge in enumerate(EDGES)}
    order = [edge_index[edge] for edge in reordered_edges]
    reordered = special_matrix.extract(order, order)

    c_matrix = sp.Matrix(
        [
            [int(vertex not in edge) for edge in internal_edges]
            for vertex in range(1, 7)
        ]
    )
    d_matrix = sp.Matrix(
        [
            [int(set(edge).isdisjoint(row)) for edge in internal_edges]
            for row in internal_edges
        ]
    )
    expected_block = sp.zeros(21)
    expected_block[:6, 6:] = 6 * q * c_matrix
    expected_block[6:, :6] = 6 * q * c_matrix.T
    expected_block[6:, 6:] = 2 * (p + 2 * q) * d_matrix
    assert reordered == expected_block
    assert c_matrix * c_matrix.T == 4 * sp.eye(6) + 6 * sp.ones(6)
    assert sp.factor(d_matrix.charpoly(lambda_symbol).as_expr()) == (
        (lambda_symbol - 6)
        * (lambda_symbol + 3) ** 5
        * (lambda_symbol - 1) ** 9
    )

    determinant_formula = (
        (2 * (p + 2 * q)) ** 9
        * (-144 * q**2) ** 5
        * (-1440 * q**2)
    )
    assert sp.factor(special_matrix.det(method="domain-ge") - determinant_formula) == 0

    # On the only determinant wall, the entire kernel is internal and 9D.
    exceptional = special_matrix.subs({p: -2, q: 1})
    exceptional_reordered = exceptional.extract(order, order)
    assert exceptional.rank() == 12
    assert c_matrix.rank() == 6
    assert len(c_matrix.nullspace()) == 9
    for kernel_vector in exceptional_reordered.nullspace():
        assert kernel_vector[:6, :] == sp.zeros(6, 1)
        assert c_matrix * kernel_vector[6:, :] == sp.zeros(6, 1)

    print("PASS: physical equations force the exact mixed kernel (ell^2 A)F=0")
    print("PASS: M_A is the weighted KG(7,2) pencil 2(SC-WC-CW)")
    print("PASS: the symmetric anchor has signature (15,6)")
    print("PASS: the S6 block determinant is the exact degree-21 formula")
    print("PASS: its sole wall has a 9D kernel with every star coordinate zero")
    print("searches=0 finite_fields=0 graph_enumerations=0 groebner=0")
    print("SCOPE: mixed-sign general extensions, P7, and global Krenn-Gu remain unresolved")


if __name__ == "__main__":
    main()
