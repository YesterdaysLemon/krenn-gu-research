"""Focused exact checks for same-graph defect vanishing and target attachment."""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp


def hafnian(
    vertices: tuple[int, ...], edges: dict[tuple[int, int], sp.Expr]
) -> sp.Expr:
    @cache
    def recurse(active: tuple[int, ...]) -> sp.Expr:
        if not active:
            return sp.Integer(1)
        if len(active) % 2:
            return sp.Integer(0)
        first = active[0]
        total = sp.Integer(0)
        for partner in active[1:]:
            edge = edges.get(tuple(sorted((first, partner))), sp.Integer(0))
            remaining = tuple(vertex for vertex in active[1:] if vertex != partner)
            total += edge * recurse(remaining)
        return sp.expand(total)

    return recurse(tuple(sorted(vertices)))


def even_subsets(vertices: range) -> list[tuple[int, ...]]:
    return [
        subset
        for size in range(0, len(vertices) + 1, 2)
        for subset in combinations(vertices, size)
    ]


def check_physical_insertion_identity() -> None:
    port_count = 6
    q0, q1 = port_count, port_count + 1
    port_edges = {
        (i, j): sp.Integer((i + 1) * (j + 2) - 3)
        for i, j in combinations(range(port_count), 2)
    }
    a = [sp.Integer(i + 2) for i in range(port_count)]
    b = [sp.Integer(2 * i - 1) for i in range(port_count)]
    h = sp.Integer(3)

    full_edges = dict(port_edges)
    full_edges[(q0, q1)] = h
    for port in range(port_count):
        full_edges[tuple(sorted((port, q0)))] = a[port]
        full_edges[tuple(sorted((port, q1)))] = b[port]

    moments: dict[tuple[int, ...], sp.Expr] = {}
    responses: dict[tuple[int, ...], sp.Expr] = {}
    for subset in even_subsets(range(port_count)):
        moments[subset] = hafnian(subset, port_edges)
        responses[subset] = hafnian((*subset, q0, q1), full_edges)

    assert responses[()] == h
    for subset in even_subsets(range(port_count)):
        half_size = len(subset) // 2
        insertion = sum(
            responses[edge]
            * moments[tuple(vertex for vertex in subset if vertex not in edge)]
            for edge in combinations(subset, 2)
        )
        defect = sp.expand(
            responses[subset] - insertion + (half_size - 1) * h * moments[subset]
        )
        assert defect == 0, (subset, defect)


def check_top_cancellation_control() -> None:
    identity = sp.eye(3)
    e01 = sp.zeros(3)
    e01[0, 1] = 1
    direct = identity + e01
    a_u = sp.Matrix([1, 0, 0])
    b_v = sp.Matrix([0, -1, 0])
    zero = sp.zeros(3, 1)
    corrected = a_u * b_v.T + zero * zero.T
    top = direct + corrected
    assert corrected == -e01
    assert top == identity
    assert corrected[0, 1] == -1


def check_selector_identity() -> None:
    omega, h, u, t, nuisance = sp.symbols("omega h u t nuisance", nonzero=True)
    top = h * u + t
    selected = omega * u + nuisance
    identity = sp.expand(omega * top - h * selected + h * nuisance - omega * t)
    assert identity == 0
    assert sp.solve(sp.Eq(omega * t, -h * selected), selected) == [-omega * t / h]


def augmented_edges(
    r: int, base_word: bool
) -> tuple[tuple[int, ...], dict[tuple[int, int], sp.Expr]]:
    q0, q1 = r, r + 1
    edges: dict[tuple[int, int], sp.Expr] = {}
    for i, j in combinations(range(r), 2):
        edges[(i, j)] = sp.Integer(0) if base_word else sp.Symbol(f"l{i}{j}")
    for root in range(r):
        edges[(root, q0)] = sp.Symbol(f"a{root}")
        edges[(root, q1)] = sp.Symbol(f"b{root}")
    return tuple(range(r + 2)), edges


def check_root_legality() -> None:
    for r in range(1, 7):
        vertices, base_edges = augmented_edges(r, base_word=True)
        value = hafnian(vertices, base_edges)
        if r == 2:
            assert value != 0
        else:
            assert value == 0

        vertices, general_edges = augmented_edges(r, base_word=False)
        general = hafnian(vertices, general_edges)
        if r % 2:
            assert general == 0

    vertices, edges = augmented_edges(4, base_word=False)
    actual = hafnian(vertices, edges)
    expected = sp.Integer(0)
    for i, j in combinations(range(4), 2):
        remaining = [root for root in range(4) if root not in (i, j)]
        p, q = remaining
        fan = edges[(p, 4)] * edges[(q, 5)] + edges[(p, 5)] * edges[(q, 4)]
        expected += edges[(i, j)] * fan
    assert sp.expand(actual - expected) == 0


def check_coboundary_holonomy() -> None:
    gauges = [
        sp.eye(2),
        sp.diag(sp.Rational(2), sp.Rational(1, 2)),
        sp.Matrix([[0, 1], [1, 0]]),
    ]
    transitions = [gauges[(i + 1) % 3].inv() * gauges[i] for i in range(3)]
    holonomy = transitions[2] * transitions[1] * transitions[0]
    assert holonomy == sp.eye(2)


def main() -> None:
    check_physical_insertion_identity()
    check_top_cancellation_control()
    check_selector_identity()
    check_root_legality()
    check_coboundary_holonomy()
    print("same-graph response-defect and target-selector checks: PASS")


if __name__ == "__main__":
    main()
