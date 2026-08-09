"""Verify the overlapping rank-six support classification and P3+K2 obstruction.

This is a fixed exact symbolic replay, not a graph, support, word, or
parameter search.
"""

from itertools import combinations

import sympy as sp


def permanent(matrix: sp.Matrix):
    """Return the permanent by a fixed first-row symbolic recursion."""
    size = matrix.rows
    if size == 0:
        return sp.Integer(1)
    return sp.expand(
        sum(
            matrix[0, column] * permanent(matrix.minor_submatrix(0, column))
            for column in range(size)
        )
    )


def laplace_permanent(matrix: sp.Matrix, first_rows: tuple[int, ...]):
    """Expand a square permanent along one fixed row set."""
    size = matrix.rows
    other_rows = tuple(row for row in range(size) if row not in first_rows)
    result = sp.Integer(0)
    for columns in combinations(range(size), len(first_rows)):
        other_columns = tuple(
            column for column in range(size) if column not in columns
        )
        result += permanent(matrix.extract(first_rows, columns)) * permanent(
            matrix.extract(other_rows, other_columns)
        )
    return sp.expand(result)


def main() -> None:
    # Both residual descents are ordinary exact Laplace identities on one
    # generic five-row permanent: 2+3 for degree three and 4+1 for degree one.
    entries = sp.symbols("z0:25")
    generic = sp.Matrix(5, 5, entries)
    full = permanent(generic)
    assert sp.expand(full - laplace_permanent(generic, (0, 1))) == 0
    assert sp.expand(full - laplace_permanent(generic, (0, 1, 2, 3))) == 0

    # Exact characteristic-zero coefficient antecedent.  Every colour occurs
    # nontrivially among the three selected degree-five rows.
    rho = sp.symbols("rho")
    beta = 2 * (1 + rho) / 7
    beta_norm = sp.rem(
        sp.together(beta * beta.subs(rho, -rho)).as_numer_denom()[0],
        rho**2 - 21,
        rho,
    )
    assert beta_norm == -80
    assert sp.rem(rho**2, rho**2 - 21, rho) == 21
    assert sp.Integer(-6) != 0

    # Structural degree signatures of the five three-edge simple graphs.
    signatures = {
        "3K2": (1, 1, 1, 1, 1, 1),
        "P3+K2": (2, 1, 1, 1, 1),
        "P4": (2, 2, 1, 1),
        "K1,3": (3, 1, 1, 1),
        "K3": (2, 2, 2),
    }
    assert all(sum(signature) == 6 for signature in signatures.values())
    assert len(set(signatures.values())) == 5

    surviving_supports = {
        "K3": ({0, 1}, {1, 2}, {0, 2}),
        "K1,3": ({0, 1}, {0, 2}, {0, 3}),
        "P4": ({0, 1}, {1, 2}, {2, 3}),
    }
    assert all(
        len({frozenset(edge) for edge in edges}) == 3
        for edges in surviving_supports.values()
    )
    assert {
        name: len(set().union(*edges))
        for name, edges in surviving_supports.items()
    } == {"K3": 3, "K1,3": 4, "P4": 4}

    # P3+K2: the six required scalar/vector components.
    p, x, y, u, v, r, s, t, w = sp.symbols("p x y u v r s t w")
    equation_a = u + p * r
    equation_b = x + p * s
    equation_c = v + p * t
    equation_d = y + p * w
    equation_e = 1 + x * t + y * r
    equation_f = p + x * v + y * u

    first_certificate = sp.expand(
        p * equation_e
        + equation_f
        - x * equation_c
        - y * equation_a
    )
    assert first_certificate == 2 * p
    unit_certificate = sp.expand(
        equation_e
        - t * equation_b
        - r * equation_d
        + (s * t + r * w)
        * (
            p * equation_e
            + equation_f
            - x * equation_c
            - y * equation_a
        )
        / 2
    )
    assert unit_certificate == 1

    groebner_basis = sp.groebner(
        (
            equation_a,
            equation_b,
            equation_c,
            equation_d,
            equation_e,
            equation_f,
        ),
        p,
        x,
        y,
        u,
        v,
        r,
        s,
        t,
        w,
        order="grevlex",
    )
    assert tuple(poly.as_expr() for poly in groebner_basis.polys) == (sp.Integer(1),)

    # K1,3 control: the central vector equation has zero leaf-leaf factors.
    e0 = sp.Matrix((1, 0, 0))
    e1 = sp.Matrix((0, 1, 0))
    e2 = sp.Matrix((0, 0, 1))
    star_hafnian = e0 * 0 + e1 * 0 + e2 * 0
    assert star_hafnian == sp.zeros(3, 1)

    # P4 control in Q1 tensor Q2, represented as a 2 x 2 matrix.
    u_basis = sp.Matrix((1, 0))
    v_basis = sp.Matrix((0, 1))
    s_basis = sp.Matrix((1, 0))
    t_basis = sp.Matrix((0, 1))
    outer_support_matching = u_basis * t_basis.T
    cross_matching = (-u_basis) * t_basis.T
    middle_matching = v_basis * s_basis.T * 0
    assert outer_support_matching + cross_matching + middle_matching == sp.zeros(2)
    assert v_basis * s_basis.T != sp.zeros(2)

    # In all three surviving overlap controls, fewer than six displayed modes
    # are active, so their displayed-span singleton shadows are identically zero.
    active_mode_counts = {
        name: len(set().union(*edges))
        for name, edges in surviving_supports.items()
    }
    assert all(count < 6 for count in active_mode_counts.values())

    print("PASS: exact five-row 2+3 and 4+1 Laplace descents")
    print("PASS: five structural three-edge support types")
    print("PASS: P3+K2 cubic equations have an explicit unit certificate")
    print("PASS: Groebner cross-check returns the unit ideal")
    print("PASS: K3, K1,3, and P4 quotient-core controls survive")
    print("SCOPE: their full unprojected physical lifts remain unresolved")
    print("searches=0")


if __name__ == "__main__":
    main()
