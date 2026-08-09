"""Primary exact replay for the physical P7 leaf-annihilator reduction."""

from __future__ import annotations

import itertools
import math

import sympy as sp

LEAVES = tuple(range(1, 8))
EDGES = tuple(itertools.combinations(LEAVES, 2))
TRIPLES = tuple(itertools.combinations(LEAVES, 3))
FOUR_SETS = tuple(itertools.combinations(LEAVES, 4))
FIVE_SETS = tuple(itertools.combinations(LEAVES, 5))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
TRIPLE_INDEX = {subset: index for index, subset in enumerate(TRIPLES)}
FOUR_INDEX = {subset: index for index, subset in enumerate(FOUR_SETS)}
FIVE_INDEX = {subset: index for index, subset in enumerate(FIVE_SETS)}


def boolean_add(
    left: dict[frozenset[int], sp.Expr],
    right: dict[frozenset[int], sp.Expr],
) -> dict[frozenset[int], sp.Expr]:
    """Add sparse Boolean-algebra elements."""
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
        if sp.expand(scalar * coefficient) != 0
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


def forms_equal(
    left: dict[frozenset[int], sp.Expr],
    right: dict[frozenset[int], sp.Expr],
) -> bool:
    """Compare two symbolic Boolean forms after expansion."""
    keys = set(left) | set(right)
    return all(sp.expand(left.get(key, 0) - right.get(key, 0)) == 0 for key in keys)


def lefschetz_matrix(source_degree: int, power: int) -> sp.Matrix:
    """Multiplication by ell^power between leaf Boolean degrees."""
    source = tuple(itertools.combinations(LEAVES, source_degree))
    target = tuple(itertools.combinations(LEAVES, source_degree + power))
    return sp.Matrix(
        [
            [
                math.factorial(power) if set(column).issubset(row) else 0
                for column in source
            ]
            for row in target
        ]
    )


def multiplication_by_f_degree_two(f_symbols: dict[tuple[int, int], sp.Expr]) -> sp.Matrix:
    """Matrix mu_2(F):A_2->A_4."""
    return sp.Matrix(
        [
            [
                f_symbols[
                    tuple(vertex for vertex in four if vertex not in edge)
                ]
                if set(edge).issubset(four)
                else 0
                for edge in EDGES
            ]
            for four in FOUR_SETS
        ]
    )


def multiplication_by_f_degree_three(
    f_symbols: dict[tuple[int, int], sp.Expr],
) -> sp.Matrix:
    """Matrix mu_3(F):A_3->A_5."""
    return sp.Matrix(
        [
            [
                f_symbols[
                    tuple(vertex for vertex in five if vertex not in triple)
                ]
                if set(triple).issubset(five)
                else 0
                for triple in TRIPLES
            ]
            for five in FIVE_SETS
        ]
    )


def main() -> None:
    """Run the exact symbolic checks."""
    ell = {frozenset({vertex}): sp.Integer(1) for vertex in LEAVES}
    f_symbols = {edge: sp.Symbol(f"f_{edge[0]}{edge[1]}") for edge in EDGES}
    a_symbols = {vertex: sp.Symbol(f"a_{vertex}") for vertex in LEAVES}
    t = sp.Symbol("t", nonzero=True)
    f_form = {frozenset(edge): coefficient for edge, coefficient in f_symbols.items()}
    a_form = {
        frozenset({vertex}): coefficient for vertex, coefficient in a_symbols.items()
    }
    n_form = boolean_scale(sp.Rational(1, 2), boolean_mul(f_form, f_form))
    jn_form = {
        frozenset(triple): n_form[
            frozenset(vertex for vertex in LEAVES if vertex not in triple)
        ]
        for triple in TRIPLES
    }
    radial_residual = boolean_add(
        boolean_mul(a_form, f_form), boolean_scale(-t, jn_form)
    )
    k_form = boolean_add(
        boolean_scale(2, boolean_mul(ell, a_form)), boolean_scale(t, f_form)
    )
    primitive_defect = boolean_add(n_form, boolean_mul(ell, jn_form))
    master_left = boolean_mul(f_form, k_form)
    master_right = boolean_add(
        boolean_scale(2, boolean_mul(ell, radial_residual)),
        boolean_scale(2 * t, primitive_defect),
    )
    assert forms_equal(master_left, master_right)

    lefschetz_3_4 = lefschetz_matrix(3, 1)
    lefschetz_2_5 = lefschetz_matrix(2, 3)
    assert lefschetz_3_4.shape == (35, 35)
    assert lefschetz_3_4.rank() == 35
    assert lefschetz_2_5.shape == (21, 21)
    assert lefschetz_2_5.rank() == 21

    incidence = sp.Matrix(
        [[int(vertex in edge) for vertex in LEAVES] for edge in EDGES]
    )
    assert incidence.rank() == 7
    assert incidence.T * incidence == 5 * sp.eye(7) + sp.ones(7)
    assert 21 - incidence.rank() == 14

    mu_two = multiplication_by_f_degree_two(f_symbols)
    mu_three = multiplication_by_f_degree_three(f_symbols)
    reordered_mu_three = sp.zeros(21, 35)
    for edge_row, edge in enumerate(EDGES):
        five = tuple(vertex for vertex in LEAVES if vertex not in edge)
        for four_column, four in enumerate(FOUR_SETS):
            triple = tuple(vertex for vertex in LEAVES if vertex not in four)
            reordered_mu_three[edge_row, four_column] = mu_three[
                FIVE_INDEX[five], TRIPLE_INDEX[triple]
            ]
    assert reordered_mu_three == mu_two.T

    uniform = {edge: sp.Integer(1) for edge in EDGES}
    uniform_mu_two = multiplication_by_f_degree_two(uniform)
    inclusion_2_4 = sp.Matrix(
        [
            [int(set(edge).issubset(four)) for edge in EDGES]
            for four in FOUR_SETS
        ]
    )
    assert uniform_mu_two == inclusion_2_4
    assert uniform_mu_two.rank() == 21

    switching = {vertex: sp.Symbol(f"s_{vertex}", nonzero=True) for vertex in LEAVES}
    switched_f = {
        edge: switching[edge[0]] * switching[edge[1]] for edge in EDGES
    }
    switched_mu_two = multiplication_by_f_degree_two(switched_f)
    row_diagonal = sp.diag(
        *(sp.prod(switching[vertex] for vertex in four) for four in FOUR_SETS)
    )
    column_inverse = sp.diag(
        *(1 / (switching[edge[0]] * switching[edge[1]]) for edge in EDGES)
    )
    assert switched_mu_two == row_diagonal * inclusion_2_4 * column_inverse

    gamma = sp.symbols("g_0:20")
    g_coefficients = list(gamma) + [-sum(gamma)]
    g_form = {
        frozenset(edge): g_coefficients[index] for index, edge in enumerate(EDGES)
    }
    down_coefficients = {
        vertex: sum(
            g_coefficients[EDGE_INDEX[edge]] for edge in EDGES if vertex in edge
        )
        for vertex in LEAVES
    }
    down_form = {
        frozenset({vertex}): coefficient
        for vertex, coefficient in down_coefficients.items()
    }
    phi_form = boolean_add(
        boolean_mul(g_form, jn_form),
        boolean_scale(-1, boolean_mul(down_form, n_form)),
    )
    c_form = boolean_add(
        boolean_scale(2, boolean_mul(a_form, g_form)),
        boolean_scale(-t, boolean_mul(down_form, f_form)),
    )
    syzygy_left = boolean_mul(f_form, c_form)
    syzygy_right = boolean_add(
        boolean_scale(2 * t, phi_form),
        boolean_scale(2, boolean_mul(g_form, radial_residual)),
    )
    assert forms_equal(syzygy_left, syzygy_right)

    # Coefficient-matrix form of the factorization has a 20-dimensional source.
    c_matrix = sp.Matrix(
        [
            [sp.expand(c_form.get(frozenset(triple), 0)).coeff(variable) for variable in gamma]
            for triple in TRIPLES
        ]
    )
    phi_matrix = sp.Matrix(
        [
            [sp.expand(phi_form.get(frozenset(five), 0)).coeff(variable) for variable in gamma]
            for five in FIVE_SETS
        ]
    )
    assert c_matrix.shape == (35, 20)
    assert phi_matrix.shape == (21, 20)

    # Exact square-zero coordinate-boundary control.
    boundary_b = {
        vertex: sp.Symbol(f"q_{vertex}") for vertex in LEAVES if vertex != 1
    }
    boundary_f = {
        frozenset({1, vertex}): coefficient
        for vertex, coefficient in boundary_b.items()
    }
    boundary_a = {frozenset({1}): sp.Integer(1)}
    boundary_n = boolean_mul(boundary_f, boundary_f)
    boundary_radial = boolean_mul(boundary_a, boundary_f)
    boundary_k = boolean_add(
        boolean_scale(2, boolean_mul(ell, boundary_a)),
        boolean_scale(t, boundary_f),
    )
    assert boundary_n == {}
    assert boundary_radial == {}
    assert boolean_mul(boundary_f, boundary_k) == {}

    print("PASS: ell:A3->A4 and ell^3:A2->A5 are exact isomorphisms")
    print("PASS: FK master identity proves radial extension equivalence")
    print("PASS: leaf incidence quotient has dimensions 7+14")
    print("PASS: mu_3(F) is the complemented transpose of mu_2(F)")
    print("PASS: uniform switching family has mu_2 rank exactly 21")
    print("PASS: F*C_G=2t*Phi+2G*(AF-tJN) checked symbolically")
    print("PASS: structured cubic source has dimension 20")
    print("PASS: exact square-zero coordinate-boundary family")
    print("searches=0 finite_fields=0 graph_enumerations=0 groebner=0")
    print("SCOPE: physical rank-20 syzygy branch remains UNKNOWN")
    print("SCOPE: physical leaf-rank-at-most-19 branch remains UNKNOWN")
    print("SCOPE: P7 and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
