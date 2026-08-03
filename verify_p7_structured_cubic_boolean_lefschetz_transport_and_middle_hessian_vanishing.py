"""Exact verifier for the P7 structured-cubic Lefschetz transport theorem.

All calculations are formal over characteristic zero.  There is no graph,
support, parameter, numerical, finite-field, or Groebner search.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp

LEAVES = tuple(range(1, 8))
EDGES = tuple(combinations(LEAVES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
FULL_SET = frozenset(LEAVES)
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
        monomial: sp.expand(coefficient)
        for monomial, coefficient in out.items()
        if sp.expand(coefficient) != 0
    }


def boolean_down(form: BooleanForm) -> BooleanForm:
    """Apply partial=sum_i partial_i to a square-free form."""
    out: BooleanForm = {}
    for monomial, coefficient in form.items():
        for vertex in monomial:
            target = frozenset(set(monomial) - {vertex})
            out[target] = sp.expand(out.get(target, 0) + coefficient)
    return {
        monomial: coefficient
        for monomial, coefficient in out.items()
        if coefficient != 0
    }


def forms_equal(left: BooleanForm, right: BooleanForm) -> bool:
    """Compare formal Boolean forms coefficientwise."""
    keys = set(left) | set(right)
    return all(sp.expand(left.get(key, 0) - right.get(key, 0)) == 0 for key in keys)


def quadratic_sum(form: BooleanForm) -> sp.Expr:
    """Sum all degree-two coefficients."""
    assert all(len(monomial) == 2 for monomial in form)
    return sp.expand(sum(form.values()))


def edge_form(coefficients: list[sp.Expr]) -> BooleanForm:
    """Build a quadratic in the fixed edge order."""
    return {
        frozenset(edge): coefficients[index]
        for index, edge in enumerate(EDGES)
        if coefficients[index] != 0
    }


def main() -> None:
    ell = {frozenset({vertex}): sp.Integer(1) for vertex in LEAVES}
    omega = boolean_scale(sp.Rational(1, 2), boolean_mul(ell, ell))
    assert all(omega[frozenset(edge)] == 1 for edge in EDGES)
    assert quadratic_sum(omega) == 21

    # The Boolean sl_2 transport on the total-zero edge hyperplane.
    down_matrix = sp.Matrix(
        [[int(vertex in edge) for edge in EDGES] for vertex in LEAVES]
    )
    up_matrix = down_matrix.T
    ud_matrix = up_matrix * down_matrix
    transport = sp.eye(21) + ud_matrix
    g0_basis = sp.Matrix.hstack(
        *(
            sp.eye(21)[:, index] - sp.eye(21)[:, 20]
            for index in range(20)
        )
    )
    transported_basis = transport * g0_basis
    assert all(sum(transported_basis[:, column]) == 0 for column in range(20))
    transport_g0 = transported_basis[:20, :]
    identity_g0 = sp.eye(20)
    assert (transport_g0 - identity_g0) * (transport_g0 - 6 * identity_g0) == sp.zeros(20)
    assert (transport_g0 - identity_g0).rank() == 6
    assert (transport_g0 - 6 * identity_g0).rank() == 14
    assert transport_g0.det() == 6**6
    inverse_g0 = (
        (sp.eye(21) - sp.Rational(1, 6) * ud_matrix) * g0_basis
    )[:20, :]
    assert transport_g0 * inverse_g0 == identity_g0

    f_symbols = {edge: sp.Symbol(f"f_{edge[0]}{edge[1]}") for edge in EDGES}
    a_symbols = {vertex: sp.Symbol(f"a_{vertex}") for vertex in LEAVES}
    t = sp.Symbol("t", nonzero=True)
    f_form = {frozenset(edge): coefficient for edge, coefficient in f_symbols.items()}
    a_form = {
        frozenset({vertex}): coefficient for vertex, coefficient in a_symbols.items()
    }
    k_form = boolean_add(
        boolean_scale(2, boolean_mul(ell, a_form)),
        boolean_scale(t, f_form),
    )

    # The physical cubic annihilator AOmega is forced by FK and ell F^2.
    identity_16_left = boolean_mul(ell, boolean_mul(f_form, k_form))
    identity_16_right = boolean_add(
        boolean_scale(4, boolean_mul(f_form, boolean_mul(a_form, omega))),
        boolean_scale(t, boolean_mul(ell, boolean_mul(f_form, f_form))),
    )
    assert forms_equal(identity_16_left, identity_16_right)

    # Universal structured-cubic transport identity for a generic G in G_0.
    gamma = list(sp.symbols("g_0:20"))
    g_coefficients = gamma + [-sum(gamma)]
    generic_g = edge_form(g_coefficients)
    generic_d = boolean_down(generic_g)
    generic_tg = boolean_add(generic_g, boolean_mul(ell, generic_d))
    generic_c = boolean_add(
        boolean_scale(2, boolean_mul(a_form, generic_g)),
        boolean_scale(-t, boolean_mul(generic_d, f_form)),
    )
    transported_c = boolean_add(
        boolean_scale(2, boolean_mul(a_form, generic_tg)),
        boolean_scale(-1, boolean_mul(generic_d, k_form)),
    )
    assert forms_equal(generic_c, transported_c)

    # Canonical covariant H and its explicit transported preimage G.
    s = quadratic_sum(k_form)
    h_form = boolean_add(
        boolean_scale(s, omega),
        boolean_scale(-21, k_form),
    )
    assert sp.expand(quadratic_sum(h_form)) == 0
    h_down = boolean_down(h_form)
    canonical_g = boolean_add(
        h_form,
        boolean_scale(-sp.Rational(1, 6), boolean_mul(ell, h_down)),
    )
    assert sp.expand(quadratic_sum(canonical_g)) == 0
    canonical_d = boolean_down(canonical_g)
    assert forms_equal(
        boolean_add(canonical_g, boolean_mul(ell, canonical_d)),
        h_form,
    )

    canonical_c = boolean_add(
        boolean_scale(2, boolean_mul(a_form, canonical_g)),
        boolean_scale(-t, boolean_mul(canonical_d, f_form)),
    )
    c_via_h = boolean_add(
        boolean_scale(2, boolean_mul(a_form, h_form)),
        boolean_scale(-1, boolean_mul(canonical_d, k_form)),
    )
    assert forms_equal(canonical_c, c_via_h)

    linear_factor = boolean_add(
        boolean_add(
            boolean_scale(sp.Rational(1, 2) * s, ell),
            boolean_scale(-42, a_form),
        ),
        boolean_scale(-1, canonical_d),
    )
    covariant_right = boolean_add(
        boolean_scale(
            -sp.Rational(1, 2) * t * s,
            boolean_mul(ell, f_form),
        ),
        boolean_mul(linear_factor, k_form),
    )
    assert forms_equal(canonical_c, covariant_right)

    # Under FK=ell F^2=0, this exact reduction forces FC_G=0.
    forced_syzygy_right = boolean_add(
        boolean_scale(
            -sp.Rational(1, 2) * t * s,
            boolean_mul(ell, boolean_mul(f_form, f_form)),
        ),
        boolean_mul(linear_factor, boolean_mul(f_form, k_form)),
    )
    assert forms_equal(boolean_mul(f_form, canonical_c), forced_syzygy_right)

    # Explicit inverse-system Hessian pairing for Psi_F.
    hessian = sp.zeros(21, 21)
    pairing = sp.zeros(21, 21)
    for row, first_edge in enumerate(EDGES):
        first_form = {frozenset(first_edge): sp.Integer(1)}
        for column, second_edge in enumerate(EDGES):
            if set(first_edge) & set(second_edge):
                hessian[row, column] = 0
            else:
                union = set(first_edge) | set(second_edge)
                hessian[row, column] = sum(
                    a_symbols[vertex]
                    * f_symbols[tuple(sorted(set(LEAVES) - union - {vertex}))]
                    for vertex in set(LEAVES) - union
                )
            second_form = {frozenset(second_edge): sp.Integer(1)}
            top_product = boolean_mul(
                boolean_mul(boolean_mul(first_form, second_form), a_form),
                f_form,
            )
            pairing[row, column] = top_product.get(FULL_SET, 0)
    assert hessian == pairing

    omega_vector = sp.ones(21, 1)
    hessian_kernel_numerator = 4 * hessian * omega_vector
    physical_numerator = boolean_add(
        boolean_mul(ell, boolean_mul(f_form, k_form)),
        boolean_scale(-t, boolean_mul(ell, boolean_mul(f_form, f_form))),
    )
    paired_physical_numerator = sp.zeros(21, 1)
    for row, edge in enumerate(EDGES):
        edge_monomial = {frozenset(edge): sp.Integer(1)}
        paired_physical_numerator[row, 0] = boolean_mul(
            edge_monomial,
            physical_numerator,
        ).get(FULL_SET, 0)
    assert hessian_kernel_numerator == paired_physical_numerator

    print("PASS: T|G_0 has spectrum 1^14,6^6, determinant 6^6, and the stated inverse")
    print("PASS: ell*F*K=4*F*A*Omega+t*ell*F^2 as an exact Boolean identity")
    print("PASS: C_G=2*A*T(G)-(partial G)*K for every total-zero G")
    print("PASS: the canonical nonzero covariant reduces C_G to sigma(K)[ell F]")
    print("PASS: the apolar second-Hessian pairing and forced Omega kernel agree")
    print("searches=0 finite_fields=0 graph_enumerations=0 groebner=0")
    print("SCOPE: physical extension existence, P7, and global Krenn-Gu remain unresolved")


if __name__ == "__main__":
    main()
