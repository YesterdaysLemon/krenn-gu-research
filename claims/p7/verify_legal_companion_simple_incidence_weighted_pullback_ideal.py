"""Primary exact replay for the legal-companion weighted pullback ideal."""

import sympy as sp

PIVOT_ROWS = {
    0: (
        (1, 2, 3, 4, 5),
        (1, 2, 3, 4, 6),
        (1, 2, 3, 4, 7),
        (1, 2, 3, 4, 8),
        (1, 2, 3, 5, 6),
        (1, 2, 4, 5, 6),
        (1, 3, 4, 5, 6),
        (2, 3, 4, 5, 6),
    ),
    1: (
        (0, 2, 3, 4, 5),
        (0, 2, 3, 4, 6),
        (0, 2, 3, 4, 7),
        (0, 2, 3, 4, 8),
        (0, 2, 3, 5, 6),
        (0, 2, 4, 5, 6),
        (0, 3, 4, 5, 6),
        (2, 3, 4, 5, 6),
    ),
}

LOCAL_EDGES = (
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 4),
)


def pentad(values):
    k12, k13, k14, k15, k23, k24, k25, k34, k35, k45 = (
        values[edge] for edge in LOCAL_EDGES
    )
    return (
        k12 * k13 * k24 * k35 * k45
        - k12 * k13 * k25 * k34 * k45
        - k12 * k14 * k23 * k35 * k45
        + k12 * k14 * k25 * k34 * k35
        + k12 * k15 * k23 * k34 * k45
        - k12 * k15 * k24 * k34 * k35
        + k13 * k14 * k23 * k25 * k45
        - k13 * k14 * k24 * k25 * k35
        - k13 * k15 * k23 * k24 * k45
        + k13 * k15 * k24 * k25 * k34
        - k14 * k15 * k23 * k25 * k34
        + k14 * k15 * k23 * k24 * k35
    )


def deck_value(vertices, zero_residual_edge):
    order = len(vertices)
    all_one = {4: 3, 6: 15, 8: 105}[order]
    if not zero_residual_edge or not {0, 1}.issubset(vertices):
        return sp.Integer(all_one)
    using_residual_edge = {4: 1, 6: 3, 8: 15}[order]
    return sp.Integer(all_one - using_residual_edge)


def pinned_data(pin, zero_residual_edge):
    partners = tuple(vertex for vertex in range(9) if vertex != pin)
    rows = PIVOT_ROWS[pin]
    matrix = sp.Matrix(
        [
            [
                deck_value(tuple(v for v in row if v != partner), zero_residual_edge)
                if partner in row
                else 0
                for partner in partners
            ]
            for row in rows
        ]
    )
    rhs = sp.Matrix(
        [deck_value(tuple(sorted((pin, *row))), zero_residual_edge) for row in rows]
    )
    determinant = sp.expand(matrix.det())
    cramer = matrix.adjugate() * rhs
    assert matrix * cramer == determinant * rhs
    return determinant, dict(zip(partners, cramer, strict=True))


def verify_maximal_minor_kernel():
    a, b, c, d, e, f, g, h, i = sp.symbols("a b c d e f g h i")
    selected = sp.Matrix([[a, b, c], [d, e, f]])
    q = sp.Matrix(
        [
            selected[:, [1, 2]].det(),
            -selected[:, [0, 2]].det(),
            selected[:, [0, 1]].det(),
        ]
    )
    assert (selected * q).applyfunc(sp.expand) == sp.zeros(2, 1)
    extra = sp.Matrix([[g, h, i]])
    assert sp.expand((extra * q)[0] - selected.col_join(extra).det()) == 0

    quotient = sp.Matrix([[-2, 1, 0], [-3, 0, 1], [-5, 1, 1]])
    q_first = sp.Matrix([1, 2, 3])
    assert quotient.rank() == 2
    assert quotient * q_first == sp.zeros(3, 1)
    gamma = sp.Matrix([[1, 0, 0]]).col_join(quotient)
    assert gamma.rank() == 3
    assert gamma * q_first == sp.Matrix([1, 0, 0, 0])


def verify_weights_and_pair_ideal():
    q_symbols = sp.symbols("q0:10")
    q = dict(zip(LOCAL_EDGES, q_symbols, strict=True))
    u0 = sp.symbols("a0:5")
    u1 = sp.symbols("b0:5")
    khat = {(i, j): u0[i] * u1[j] + u0[j] * u1[i] for i, j in LOCAL_EDGES}
    assert sp.expand(pentad(khat)) == 0

    s, tau = sp.symbols("s tau", nonzero=True)
    scaled_q = {edge: s * value for edge, value in q.items()}
    scaled_khat = {
        (i, j): (s**8 * u0[i]) * (s**8 * u1[j])
        + (s**8 * u0[j]) * (s**8 * u1[i])
        for i, j in LOCAL_EDGES
    }
    assert sp.expand(pentad(scaled_q) - s**5 * pentad(q)) == 0
    for edge in LOCAL_EDGES:
        assert sp.expand(scaled_khat[edge] - s**16 * khat[edge]) == 0
        assert sp.expand(
            s**15 * tau * scaled_q[edge] - scaled_khat[edge]
            - s**16 * (tau * q[edge] - khat[edge])
        ) == 0

    edge_a, edge_b = LOCAL_EDGES[:2]
    alpha = q[edge_a] * khat[edge_b] - q[edge_b] * khat[edge_a]
    scaled_alpha = (
        scaled_q[edge_a] * scaled_khat[edge_b]
        - scaled_q[edge_b] * scaled_khat[edge_a]
    )
    assert sp.expand(scaled_alpha - s**17 * alpha) == 0
    assert sp.expand(
        q[edge_a] * (tau * q[edge_b] - khat[edge_b])
        - q[edge_b] * (tau * q[edge_a] - khat[edge_a])
        + alpha
    ) == 0

    tau_q = {edge: tau * value for edge, value in q.items()}
    assert sp.expand(pentad(tau_q) - tau**5 * pentad(q)) == 0


def verify_exact_nonforcing_decks():
    d0_one, u0_one = pinned_data(0, zero_residual_edge=False)
    d1_one, _ = pinned_data(1, zero_residual_edge=False)
    assert d0_one == d1_one == 32805
    assert u0_one[1] == 32805

    d0, u0 = pinned_data(0, zero_residual_edge=True)
    d1, u1 = pinned_data(1, zero_residual_edge=True)
    assert d0 == d1 == 32805
    assert u0[1] == 0
    for blocker in range(2, 9):
        assert u0[blocker] == d0
        assert u1[blocker] == d1

    modified_pairs = dict(zip(LOCAL_EDGES, range(1, 11), strict=True))
    assert pentad(modified_pairs) == -6
    common_khat = 2 * 32805**2
    alignment = (
        modified_pairs[LOCAL_EDGES[0]] * common_khat
        - modified_pairs[LOCAL_EDGES[1]] * common_khat
    )
    assert alignment == -2152336050


def main():
    verify_maximal_minor_kernel()
    verify_weights_and_pair_ideal()
    verify_exact_nonforcing_decks()
    print("PASS: legal-companion simple-incidence weighted pullback ideal")
    print("relative_weights=pentad:5,h_gate:8,tau:15,alignment:17")
    print("h0_pinned_d0=d1=32805")
    print("ambient_h0_bad_pentad=-6 bad_alignment=-2152336050")
    print("graph_or_parameter_search_used=False")


if __name__ == "__main__":
    main()
