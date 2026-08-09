"""Verify exact scalar hafnian realizations of the formal 2+2+1 ledger.

This is a fixed exact calculation on three explicitly displayed sparse graphs.
It performs no support search, parameter sweep, or graph-family enumeration.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp

P = ("1", "2", "3", "4", "5", "a", "b")
Q = frozenset(("a", "b"))


def add_edge(
    graph: dict[frozenset[str], sp.Expr],
    left: str,
    right: str,
    weight: sp.Expr | int,
) -> None:
    assert left != right
    key = frozenset((left, right))
    assert key not in graph
    graph[key] = sp.sympify(weight)


def hafnian_evaluator(graph: dict[frozenset[str], sp.Expr]):
    """Return a memoized exact hafnian evaluator for one fixed graph."""

    @cache
    def hafnian(vertices: tuple[str, ...]) -> sp.Expr:
        if not vertices:
            return sp.Integer(1)
        if len(vertices) % 2:
            return sp.Integer(0)

        first = vertices[0]
        total = sp.Integer(0)
        for position in range(1, len(vertices)):
            second = vertices[position]
            edge = graph.get(frozenset((first, second)), sp.Integer(0))
            if edge != 0:
                rest = vertices[1:position] + vertices[position + 1 :]
                total += edge * hafnian(rest)
        return sp.simplify(total)

    return lambda vertices: hafnian(tuple(sorted(vertices)))


def formal_ledger() -> tuple[dict[int, dict[frozenset[str], sp.Expr]], int]:
    """Return the 62 prescribed scalar coordinates in each colour chart."""

    ledger: dict[int, dict[frozenset[str], sp.Expr]] = {c: {} for c in range(3)}
    prescribed = [
        frozenset(deletion)
        for size in (2, 4, 6)
        for deletion in combinations(P, size)
        if not (size == 2 and frozenset(deletion) == Q)
    ]
    assert len(prescribed) == 62
    for colour in range(3):
        ledger[colour] = {deletion: sp.Integer(0) for deletion in prescribed}

    def assign(deletion: str, colour: int, value: sp.Expr | int = 1) -> None:
        key = frozenset(deletion)
        assert key in ledger[colour]
        ledger[colour][key] = sp.sympify(value)

    # Singleton endpoint tags, equation (14) of the common-jet model.
    for deletion, colour in {
        "1a": 1,
        "1b": 2,
        "2a": 2,
        "2b": 1,
        "3a": 0,
        "3b": 2,
        "4a": 2,
        "4b": 0,
        "5a": 0,
        "5b": 1,
    }.items():
        assign(deletion, colour)

    # Root-pair cofactors, with and without deletion of Q={a,b}.
    assign("12", 1, -1)
    assign("12", 2)
    assign("12ab", 1)
    assign("34", 0, -1)
    assign("34", 2)
    assign("34ab", 0)
    for pair, colour, with_q in (
        ("13", 2, True),
        ("14", 2, False),
        ("23", 2, False),
        ("24", 2, True),
        ("15", 1, True),
        ("25", 1, False),
        ("35", 0, False),
        ("45", 0, True),
    ):
        assign(pair, colour)
        if with_q:
            assign(pair + "ab", colour)

    # The six nonzero two-axis triple tags.
    for deletion, colour in {
        "123a": 2,
        "124b": 2,
        "134a": 2,
        "234b": 2,
        "125a": 1,
        "345b": 0,
    }.items():
        assign(deletion, colour)

    # The only nonzero quartet, in both legal parity classes.
    assign("1234", 2, sp.Rational(1, 7))
    assign("1234ab", 2, sp.Rational(1, 7))
    return ledger, len(prescribed)


def coordinate_copy_graph(colour: int):
    """Build the c=0 or c=1 seven-terminal coordinate-copy graph."""

    assert colour in (0, 1)
    graph: dict[frozenset[str], sp.Expr] = {}
    core = tuple(f"z_{terminal}" for terminal in P)
    for terminal, core_vertex in zip(P, core, strict=True):
        add_edge(graph, terminal, core_vertex, 1)

    nonzero_core_edges = {
        0: {
            "3a": 1,
            "4b": 1,
            "5a": 1,
            "35": 1,
            "45": 1,
            "34": -1,
        },
        1: {
            "1a": 1,
            "2b": 1,
            "5b": 1,
            "15": 1,
            "25": 1,
            "12": -1,
        },
    }
    for pair, weight in nonzero_core_edges[colour].items():
        add_edge(graph, f"z_{pair[0]}", f"z_{pair[1]}", weight)
    return graph, core


def colour_two_graph():
    """Build the exact colour-2 chart over Q(sqrt(21))."""

    rho = sp.sqrt(21)
    graph: dict[frozenset[str], sp.Expr] = {}
    core = ("z_*", "z_1", "z_2", "z_3", "z_4", "z_5", "z_6")

    # The private forced pair supplies the global factor 1/7 and kills every
    # deletion containing terminal 5.
    add_edge(graph, "5", "z_*", sp.Rational(1, 7))

    add_edge(graph, "z_1", "z_2", 1)
    add_edge(graph, "z_3", "z_4", 1 / rho)
    add_edge(graph, "z_5", "z_6", rho)

    cross_rows = {
        "z_1": ("1", "3"),
        "z_2": ("2", "4"),
        "z_3": ("a", "1", "3"),
        "z_4": ("b", "2", "4"),
        "z_5": ("1", "3"),
        "z_6": ("2", "4"),
    }
    for core_vertex, terminals in cross_rows.items():
        for terminal in terminals:
            add_edge(graph, core_vertex, terminal, 1)

    kappa = 1 + 22 / rho
    direct_edges = {
        "12": -kappa,
        "14": -kappa,
        "23": -kappa,
        "34": -kappa,
        "13": 7,
        "24": 7,
        "1a": 7,
        "3a": 7,
        "2b": 7,
        "4b": 7,
        "1b": -rho,
        "2a": -rho,
        "3b": -rho,
        "4a": -rho,
        "ab": 1 - rho,
    }
    for pair, weight in direct_edges.items():
        add_edge(graph, pair[0], pair[1], weight)
    return graph, core, direct_edges, rho


def cofactor(
    deletion: frozenset[str],
    core: tuple[str, ...],
    hafnian,
) -> sp.Expr:
    surviving_terminals = tuple(terminal for terminal in P if terminal not in deletion)
    return hafnian(core + surviving_terminals)


def check_coordinate_copy_charts(
    ledger: dict[int, dict[frozenset[str], sp.Expr]],
) -> None:
    for colour in (0, 1):
        graph, core = coordinate_copy_graph(colour)
        hafnian = hafnian_evaluator(graph)
        for deletion, expected in ledger[colour].items():
            assert sp.simplify(cofactor(deletion, core, hafnian) - expected) == 0

        # These two coordinates were not both prescribed by the lower ledger.
        assert cofactor(Q, core, hafnian) == 0
        assert cofactor(frozenset(), core, hafnian) == 1

        # The construction uses no terminal--terminal edge at all.
        assert all(
            frozenset(pair) not in graph for pair in combinations(P, 2)
        )


def check_colour_two_chart(
    ledger: dict[int, dict[frozenset[str], sp.Expr]],
) -> tuple[sp.Expr, sp.Expr]:
    graph, core, direct_edges, rho = colour_two_graph()
    hafnian = hafnian_evaluator(graph)
    for deletion, expected in ledger[2].items():
        assert sp.simplify(cofactor(deletion, core, hafnian) - expected) == 0

    free_q = sp.Rational(103, 147)
    free_empty = sp.Rational(103, 147) + 36 * rho
    assert sp.simplify(cofactor(Q, core, hafnian) - free_q) == 0
    assert sp.simplify(cofactor(frozenset(), core, hafnian) - free_empty) == 0

    # Check the six-port response quoted in the certificate before the forced
    # terminal-5/z_* factor is restored.
    six_core = tuple(vertex for vertex in core if vertex != "z_*")
    u = ("1", "2", "3", "4", "a", "b")
    assert hafnian(six_core) == 1

    pair_response = {frozenset(pair): sp.Integer(0) for pair in combinations(u, 2)}
    for pair in ("13", "24", "1a", "3a", "2b", "4b"):
        pair_response[frozenset(pair)] = sp.Integer(7)
    pair_response[frozenset("ab")] = sp.Integer(1)
    for terminals, expected in pair_response.items():
        assert sp.simplify(hafnian(six_core + tuple(terminals)) - expected) == 0

    zero_quartets = {
        frozenset(terminals) for terminals in ("123a", "124b", "134a", "234b")
    }
    for terminals in combinations(u, 4):
        terminal_set = frozenset(terminals)
        if terminal_set == frozenset("1234"):
            expected = sp.Rational(103, 21)
        elif terminal_set in zero_quartets:
            expected = sp.Integer(0)
        else:
            expected = sp.Integer(7)
        assert sp.simplify(hafnian(six_core + terminals) - expected) == 0
    assert sp.simplify(hafnian(six_core + u) - (sp.Rational(103, 21) + 252 * rho)) == 0

    # This proves only that the displayed chart differs from the displayed
    # c=0,1 charts on the common terminal--terminal block.  It is not a
    # universal no-go theorem for every possible common-block realization.
    assert direct_edges
    assert any(sp.simplify(weight) != 0 for weight in direct_edges.values())
    return free_q, free_empty


def main() -> None:
    ledger, prescribed_per_colour = formal_ledger()
    assert all(len(chart) == prescribed_per_colour for chart in ledger.values())
    check_coordinate_copy_charts(ledger)
    free_q, free_empty = check_colour_two_chart(ledger)

    print("formal 2+2+1 scalar hafnian charts: VERIFIED")
    print(f"prescribed_values_checked={3 * prescribed_per_colour}")
    print("c0: C_Q=0, C_empty=1")
    print("c1: C_Q=0, C_empty=1")
    print(f"c2: C_Q={free_q}, C_empty={free_empty}")
    print("support_search=0 parameter_sweep=0 graph_family_enumeration=0")
    print("common_physical_graph=UNRESOLVED mixed_word_cancellation=UNRESOLVED")


if __name__ == "__main__":
    main()
