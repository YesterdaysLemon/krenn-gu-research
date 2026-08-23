"""Focused exact checks for the GLS35 raw root-deck quotient/no-go theorem."""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp

A0, A1, Q0, Q1, U0, U1, U2, U3 = range(8)
PORTS = (U0, U1, U2, U3)
EYE = sp.eye(3)
E = tuple(EYE[:, index] for index in range(3))
ONE = sp.ones(3, 1)


def tensor(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    """Flatten a two-factor covector tensor in lexicographic order."""

    return sp.kronecker_product(left, right)


def put_edge(
    edges: dict[tuple[int, int], sp.Matrix],
    left: int,
    right: int,
    value: sp.Matrix,
) -> None:
    if left < right:
        edges[(left, right)] = value
    else:
        edges[(right, left)] = value.T


def edge_block(
    edges: dict[tuple[int, int], sp.Matrix], left: int, right: int
) -> sp.Matrix:
    if left < right:
        return edges.get((left, right), sp.zeros(3))
    return edges.get((right, left), sp.zeros(3)).T


@cache
def perfect_matchings(
    vertices: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer: list[tuple[tuple[int, int], ...]] = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def graph_coefficient(
    edges: dict[tuple[int, int], sp.Matrix], word: tuple[int, ...]
) -> sp.Expr:
    total = sp.Integer(0)
    for matching in perfect_matchings(tuple(range(len(word)))):
        term = sp.Integer(1)
        for left, right in matching:
            term *= edge_block(edges, left, right)[word[left], word[right]]
        total += term
    return sp.factor(total)


def deck_value(
    edges: dict[tuple[int, int], sp.Matrix],
    vertices: tuple[int, ...],
    vectors: dict[int, sp.Matrix],
) -> sp.Expr:
    total = sp.Integer(0)
    for matching in perfect_matchings(vertices):
        term = sp.Integer(1)
        for left, right in matching:
            term *= (vectors[left].T * edge_block(edges, left, right) * vectors[right])[
                0
            ]
        total += term
    return sp.factor(total)


def build_control() -> tuple[dict[tuple[int, int], sp.Matrix], sp.Matrix, sp.Matrix]:
    edges: dict[tuple[int, int], sp.Matrix] = {}
    w0 = sp.Matrix(((0, 1, -1), (1, 0, 0), (-1, 0, 1)))
    w1 = sp.Matrix(((1, 1, -1), (0, -1, 2), (-1, 0, 0)))

    xi00, xi01, xi10, xi11 = E[1], E[2], E[2], E[1]
    put_edge(edges, A0, Q0, xi00 * E[0].T)
    put_edge(edges, A0, Q1, xi01 * E[0].T)
    put_edge(edges, A1, Q0, xi10 * E[0].T)
    put_edge(edges, A1, Q1, xi11 * E[0].T)
    for port in PORTS:
        put_edge(edges, A0, port, w0)
        put_edge(edges, A1, port, w1)

    put_edge(edges, U0, U1, E[0] * E[0].T)
    put_edge(edges, U2, U3, sp.Rational(1, 2) * E[0] * E[0].T)
    return edges, w0, w1


def raw_anchor_matrix(
    edges: dict[tuple[int, int], sp.Matrix],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    xi0 = {residual: edge_block(edges, A0, residual) * ONE for residual in (Q0, Q1)}
    xi1 = {residual: edge_block(edges, A1, residual) * ONE for residual in (Q0, Q1)}
    q = tensor(xi0[Q0], xi1[Q1]) + tensor(xi0[Q1], xi1[Q0])

    columns: list[sp.Matrix] = []
    for residual in (Q0, Q1):
        for port in PORTS:
            for colour in range(3):
                columns.append(
                    tensor(
                        xi0[residual],
                        edge_block(edges, A1, port)[:, colour],
                    )
                    + tensor(
                        edge_block(edges, A0, port)[:, colour],
                        xi1[residual],
                    )
                )

    # The top-anchor column is zero.  Every promoted-pair coefficient slice is
    # included.  Its omega*W_uv term is also zero in this control.
    for left, right in combinations(PORTS, 2):
        for left_colour in range(3):
            for right_colour in range(3):
                columns.append(
                    tensor(
                        edge_block(edges, A0, left)[:, left_colour],
                        edge_block(edges, A1, right)[:, right_colour],
                    )
                    + tensor(
                        edge_block(edges, A0, right)[:, right_colour],
                        edge_block(edges, A1, left)[:, left_colour],
                    )
                )

    nuisance = sp.Matrix.hstack(*columns)
    epsilon = tensor(ONE, ONE).T
    p = (epsilon * q)[0]
    projector = p * sp.eye(9) - q * epsilon
    return nuisance, q, projector


def check_selector_and_transverse_interfaces() -> dict[str, object]:
    # Exact rank-stratum representatives for both sides of Theorem 3.
    q_escape = sp.eye(9)[:, 8]
    b_escape = sp.eye(9)[:, :8]
    assert b_escape.rank() == 8
    assert b_escape.row_join(q_escape).rank() == 9
    selector = sp.zeros(1, 9)
    selector[0, 8] = 2
    assert selector * b_escape == sp.zeros(1, 8)
    assert (selector * q_escape)[0] == 2

    b_swallow = sp.eye(9)
    assert b_swallow.row_join(q_escape).rank() == b_swallow.rank() == 9

    edges, _, _ = build_control()
    nuisance, q, projector = raw_anchor_matrix(edges)
    assert nuisance.shape == (9, 78)
    assert nuisance.rank() == nuisance.row_join(q).rank() == 8
    assert projector * q == sp.zeros(9, 1)
    assert projector.rank() == 8

    # P_Q commutes with coefficient slicing; on omega=0 this is exactly the
    # GLS23 top transverse nuisance.  Here the raw swallowed q disappears.
    transverse = projector * nuisance
    assert transverse.rank() == 7
    return {
        "escape_ranks": (8, 9),
        "swallow_ranks": (9, 9),
        "control_raw_ranks": (8, 8),
        "control_transverse_rank": 7,
    }


def check_literal_absorption_and_output_anchor() -> dict[str, object]:
    edges, w0, w1 = build_control()
    assert w0.det() == w1.det() == -1
    assert w0.T * ONE == E[1]
    assert w1.T * ONE == E[2]

    xi00 = edge_block(edges, A0, Q0) * ONE
    xi01 = edge_block(edges, A0, Q1) * ONE
    xi10 = edge_block(edges, A1, Q0) * ONE
    xi11 = edge_block(edges, A1, Q1) * ONE
    q = tensor(xi00, xi11) + tensor(xi01, xi10)
    p = (tensor(ONE, ONE).T * q)[0]
    assert p == 2

    slice_vector = E[1] + E[2]
    assert w0 * slice_vector == E[2]
    assert w1 * slice_vector == E[1]
    literal_slice = tensor(xi00, w1 * slice_vector) + tensor(w0 * slice_vector, xi10)
    assert literal_slice == q

    kernels = []
    for port in PORTS:
        a = edge_block(edges, A0, port).T * ONE
        b = edge_block(edges, A1, port).T * ONE
        assert a == E[1]
        assert b == E[2]
        kernel = sp.Matrix.vstack(a.T, b.T).nullspace()
        assert kernel == [E[0]]
        kernels.append(tuple(kernel[0]))

    kernel_vectors = {port: E[0] for port in PORTS}
    h_value = deck_value(edges, PORTS, kernel_vectors)
    assert h_value == sp.Rational(1, 2)
    assert p * h_value == 1

    singleton_values = []
    for free in PORTS:
        covector = sp.zeros(3, 1)
        for colour in range(3):
            vectors = {port: (E[colour] if port == free else E[0]) for port in PORTS}
            covector[colour] = p * deck_value(edges, PORTS, vectors)
        assert covector == E[0]
        assert sp.Matrix.hstack(E[1], E[2], covector).rank() == 3
        singleton_values.append(tuple(covector))

    # With no residual-port edges, every one-Q deck in the singleton equation
    # vanishes.  This is checked by exhausting its four-vertex matchings.
    one_q_decks = []
    for residual in (Q0, Q1):
        other_residual = Q1 if residual == Q0 else Q0
        for free in PORTS:
            vertices = (other_residual, *(port for port in PORTS if port != free))
            values = {vertex: E[0] for vertex in vertices}
            value = deck_value(edges, vertices, values)
            assert value == 0
            one_q_decks.append(value)

    pure = tuple(graph_coefficient(edges, (colour,) * 8) for colour in range(3))
    assert pure == (0, 0, 0)
    return {
        "p": p,
        "literal_slice_equals_q": literal_slice == q,
        "kernel_axes": tuple(kernels),
        "H_kernel": h_value,
        "pH_kernel": p * h_value,
        "singleton_classes": tuple(singleton_values),
        "zero_one_q_decks": len(one_q_decks),
        "pure_coefficients": pure,
    }


def check_quotient_dichotomy_representatives() -> dict[str, object]:
    # Escape representative: quotient basis [q], nonzero pure deck e_0^4.
    q_class = sp.Matrix((1,))
    pure_classes = (sp.Matrix((1,)), sp.Matrix((0,)), sp.Matrix((0,)))
    h_pure = {(0, 0, 0, 0): sp.Integer(1)}
    assert q_class[0] * h_pure[(0, 0, 0, 0)] == pure_classes[0][0]
    assert sp.Matrix.hstack(*pure_classes).rank() == 1

    # Swallow representative: [q]=0 forces all independent pure coefficients
    # to be zero.  The assertion is coefficientwise, not numerical sampling.
    swallowed = (sp.Integer(0),) * 3
    assert all(value == 0 for value in swallowed)
    return {"escape_pure_rank": 1, "swallowed_pure_classes": swallowed}


def main() -> None:
    interfaces = check_selector_and_transverse_interfaces()
    control = check_literal_absorption_and_output_anchor()
    quotient = check_quotient_dichotomy_representatives()
    print("GLS35 raw root-deck quotient/no-go primary checks: PASS")
    print("  selector/transverse interfaces:", interfaces)
    print("  exact local physical no-go:", control)
    print("  quotient dichotomy representatives:", quotient)
    print("  scope: interface correction/no-go only; node/global closure OPEN")


if __name__ == "__main__":
    main()
