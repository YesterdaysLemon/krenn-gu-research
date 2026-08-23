"""Focused exact checks for the GLS32 first-polarized sharpness theorem."""

from __future__ import annotations

from itertools import combinations, product
from pathlib import Path
import runpy

import sympy as sp


GLS31 = runpy.run_path(
    str(
        Path(__file__).with_name(
            "verify_maximal_root_surplus_two_zero_anchor_simultaneous_absorption_and_tangent_pencil_sharpness.py"
        )
    )
)

A0, A1, Q0, Q1, K, U1, U2, U3 = range(8)
VERTICES = tuple(range(8))
ROOTS = (A0, A1, K)
Q = (Q0, Q1)
PORTS = (K, U1, U2, U3)
PAIRS = tuple(combinations(PORTS, 2))
ONE = sp.ones(3, 1)
EYE = sp.eye(3)
E = tuple(EYE[:, index] for index in range(3))

put_edge = GLS31["put_edge"]
edge_block = GLS31["edge_block"]
outer = GLS31["outer"]
perfect_matchings = GLS31["perfect_matchings"]
graph_coefficient = GLS31["graph_coefficient"]
response_matrix = GLS31["response_matrix"]
tensor4_from_pair_terms = GLS31["tensor4_from_pair_terms"]
check_transverse_modules = GLS31["check_transverse_modules"]
check_tangent_pencil = GLS31["check_tangent_pencil"]


T_VALUES = (sp.Integer(1), sp.Integer(1), sp.Integer(1), sp.Rational(1, 12))
LAMBDA_VALUES = (
    sp.Integer(1),
    sp.Integer(1),
    sp.Rational(-3, 2),
    sp.Integer(1),
    sp.Integer(1),
    sp.Integer(-2),
)


def build_control() -> dict[tuple[int, int], sp.Matrix]:
    edges: dict[tuple[int, int], sp.Matrix] = {}
    e00 = outer(E[0], E[0])
    e11 = outer(E[1], E[1])
    e22 = outer(E[2], E[2])
    w = E[1] + E[2]
    j = outer(w, w)

    put_edge(edges, A0, Q0, e11)
    put_edge(edges, A0, Q1, e22)
    put_edge(edges, A1, Q0, e22)
    put_edge(edges, A1, Q1, e11)
    put_edge(edges, Q0, Q1, e00)
    put_edge(edges, A0, K, outer(E[0] - E[2], E[0]))
    put_edge(edges, A1, K, outer(E[0] + E[1] - 2 * E[2], E[0]))
    for root in (A0, A1):
        for port in (U1, U2, U3):
            put_edge(edges, root, port, e00)

    for port, value in zip(PORTS, T_VALUES, strict=True):
        put_edge(edges, Q0, port, value * outer(E[0], w))
        put_edge(edges, Q1, port, -value * outer(E[0], w))
    for pair, response in zip(PAIRS, LAMBDA_VALUES, strict=True):
        left_index = PORTS.index(pair[0])
        right_index = PORTS.index(pair[1])
        put_edge(
            edges,
            *pair,
            response * e00 + 2 * T_VALUES[left_index] * T_VALUES[right_index] * j,
        )
    return edges


def check_maximum_root_and_incidence(edges) -> dict[str, object]:
    assert edge_block(edges, A0, A1) == sp.zeros(3)
    for root in (A0, A1):
        assert (ONE.T * edge_block(edges, root, K) * ONE)[0] == 0

    # If a residual port and two promoted ports were in a torus root, each
    # promoted w-value would vanish and their nonzero lambda edge could not.
    w = E[1] + E[2]
    for residual in Q:
        for port, value in zip(PORTS, T_VALUES, strict=True):
            expected_sign = 1 if residual == Q0 else -1
            assert edge_block(edges, residual, port) == (
                expected_sign * value * outer(E[0], w)
            )
    assert all(value != 0 for value in LAMBDA_VALUES)

    # Four promoted torus vectors would force all three complementary products
    # lambda_01 lambda_23, lambda_02 lambda_13, lambda_03 lambda_12 equal.
    cross_products = (
        LAMBDA_VALUES[0] * LAMBDA_VALUES[5],
        LAMBDA_VALUES[1] * LAMBDA_VALUES[4],
        LAMBDA_VALUES[2] * LAMBDA_VALUES[3],
    )
    assert len(set(cross_products)) == 3

    outside = (Q0, Q1, U1, U2, U3)
    incidence = {
        vertex: sp.Matrix.vstack(
            *(ONE.T * edge_block(edges, root, vertex) for root in ROOTS)
        )
        for vertex in outside
    }
    ranks = tuple(incidence[vertex].rank() for vertex in outside)
    assert ranks == (3, 3, 2, 2, 2)
    assert sum(3 - rank for rank in ranks) == 3
    return {
        "maximum_root_order": 3,
        "promoted_cross_products": cross_products,
        "incidence_ranks": ranks,
        "incidence_defect": 3,
    }


def one_q_deck(edges, removed_residual: int, removed_port: int) -> sp.Matrix:
    other_residual = Q1 if removed_residual == Q0 else Q0
    kept_ports = tuple(port for port in PORTS if port != removed_port)
    vertices = (other_residual, *kept_ports)
    matchings = tuple(perfect_matchings(vertices))
    answer = sp.zeros(1, 27)
    for kept_word in product(range(3), repeat=3):
        total = 0
        for residual_colour in range(3):
            colours = {
                other_residual: residual_colour,
                **dict(zip(kept_ports, kept_word, strict=True)),
            }
            for matching in matchings:
                term = 1
                for left, right in matching:
                    term *= edge_block(edges, left, right)[
                        colours[left], colours[right]
                    ]
                total += term
        column = 9 * kept_word[0] + 3 * kept_word[1] + kept_word[2]
        answer[column] = sp.factor(total)
    return answer


def contraction_profile(
    edges,
    left_colours,
    right_colours,
    pure_support: tuple[int, ...],
) -> tuple[tuple[tuple[int, ...], sp.Expr], ...]:
    failures = []
    for word in product(range(3), repeat=4):
        value = sum(
            graph_coefficient(edges, (a0, a1, q0, q1, *word))
            for a0 in left_colours
            for a1 in right_colours
            for q0 in range(3)
            for q1 in range(3)
        )
        target = 1 if len(set(word)) == 1 and word[0] in pure_support else 0
        difference = sp.factor(value - target)
        if difference != 0:
            failures.append((word, difference))
    return tuple(failures)


def check_first_polarized_and_normal_equations(edges) -> dict[str, object]:
    e00 = outer(E[0], E[0])
    normal = E[0]
    responses = {pair: response_matrix(edges, pair) for pair in PAIRS}
    assert tuple(response[0, 0] for response in responses.values()) == LAMBDA_VALUES
    assert all(
        response == value * e00
        for response, value in zip(responses.values(), LAMBDA_VALUES, strict=True)
    )

    a = {port: (ONE.T * edge_block(edges, A0, port)).T for port in PORTS}
    b = {port: (ONE.T * edge_block(edges, A1, port)).T for port in PORTS}
    x = {port: (normal.T * edge_block(edges, A0, port)).T for port in PORTS}
    y = {port: (normal.T * edge_block(edges, A1, port)).T for port in PORTS}
    assert a[K] == b[K] == sp.zeros(3, 1)
    assert all(a[port] == b[port] == E[0] for port in (U1, U2, U3))
    assert all(x[port] == y[port] == E[0] for port in PORTS)

    k10 = {
        pair: outer(x[pair[0]], b[pair[1]]) + outer(b[pair[0]], x[pair[1]])
        for pair in PAIRS
    }
    k01 = {
        pair: outer(a[pair[0]], y[pair[1]]) + outer(y[pair[0]], a[pair[1]])
        for pair in PAIRS
    }
    k11 = {
        pair: outer(x[pair[0]], y[pair[1]]) + outer(y[pair[0]], x[pair[1]])
        for pair in PAIRS
    }
    expected = {
        word: (sp.Integer(1) if word == (0, 0, 0, 0) else sp.Integer(0))
        for word in product(range(3), repeat=4)
    }
    assert tensor4_from_pair_terms(k10, responses) == expected
    assert tensor4_from_pair_terms(k01, responses) == expected
    assert tensor4_from_pair_terms(k11, responses) == expected

    one_q_cancellations = 0
    for port in PORTS:
        assert one_q_deck(edges, Q0, port) + one_q_deck(edges, Q1, port) == sp.zeros(
            1, 27
        )
        one_q_cancellations += 1

    assert not contraction_profile(edges, (0,), range(3), (0,))
    assert not contraction_profile(edges, range(3), (0,), (0,))
    assert not contraction_profile(edges, (0,), (0,), (0,))
    actual_root_failures = contraction_profile(edges, range(3), range(3), (0, 1, 2))
    assert len(actual_root_failures) == 41
    return {
        "response_scalars": LAMBDA_VALUES,
        "one_q_pairwise_label_cancellations": one_q_cancellations,
        "first_left_failures": 0,
        "first_right_failures": 0,
        "normal_failures": 0,
        "actual_root_contraction_failures": len(actual_root_failures),
    }


def check_pure_and_mixed(edges) -> dict[str, object]:
    pure = tuple(graph_coefficient(edges, (colour,) * 8) for colour in range(3))
    assert pure == (1, 1, 1)
    failures = []
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        value = graph_coefficient(edges, word)
        if value != 0:
            failures.append((word, value))
    assert len(failures) == 316
    hamming_one = ((1, 1, 1, 1, 1, 1, 1, 2), sp.Integer(1))
    assert hamming_one in failures
    return {
        "pure_coefficients": pure,
        "mixed_failures": len(failures),
        "hamming_one_failure": hamming_one,
    }


def main() -> None:
    edges = build_control()
    root = check_maximum_root_and_incidence(edges)
    equations = check_first_polarized_and_normal_equations(edges)
    modules = check_transverse_modules(edges)
    tangent = check_tangent_pencil(edges)
    coefficients = check_pure_and_mixed(edges)
    print("GLS32 first-polarized simultaneous-absorption primary checks: PASS")
    print("  maximum-root/incidence:", root)
    print("  complete first-polarized/normal equations:", equations)
    print("  complete GLS23/GLS26 modules:", modules)
    print("  quotient and L=H replay:", tangent)
    print("  pure/mixed coefficients:", coefficients)
    print("  scope: stronger sharpness only; divisor/node/global closure OPEN")


if __name__ == "__main__":
    main()
