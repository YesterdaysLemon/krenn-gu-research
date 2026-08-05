"""Verify the four-face mixed circuit for the fixed 2+2+1 pure charts.

Only four specified degree-five no-terminal-edge responses are evaluated.
The twelve cross-colour core edges remain symbolic; no support or parameter
search is performed.
"""

from __future__ import annotations

from functools import cache

import sympy as sp

import verify_p7_221_common_terminal_block_scalar_hafnian_realizability as scalar

Z = tuple(f"z{index}" for index in range(7))
P = scalar.P
MIXED_COLOURS = (2, 2, 2, 0, 0, 0, 0)
CROSS_PAIRS = tuple((left, right) for left in range(3) for right in range(3, 7))
SURVIVOR_FACES = ("125ab", "145ab", "235ab", "345ab")


def canonical_graph(builder):
    graph, old_core = builder()
    rename = dict(zip(old_core, Z, strict=True))
    result: dict[frozenset[str], sp.Expr] = {}
    for edge, weight in graph.items():
        left, right = tuple(edge)
        scalar.add_edge(result, rename.get(left, left), rename.get(right, right), weight)
    return result


def edge_weight(graph, left: str, right: str) -> sp.Expr:
    return graph.get(frozenset((left, right)), sp.Integer(0))


def mixed_incidence_and_core():
    colour_zero = canonical_graph(scalar.build_colour_zero)
    colour_two = canonical_graph(scalar.build_colour_two)
    charts = {0: colour_zero, 2: colour_two}

    incidence = sp.zeros(7)
    for row, core_vertex in enumerate(Z):
        chart = charts[MIXED_COLOURS[row]]
        for column, terminal in enumerate(P):
            incidence[row, column] = edge_weight(chart, core_vertex, terminal)

    variables = {(left, right): sp.Symbol(f"x{left}{right}") for left, right in CROSS_PAIRS}
    core_edges: dict[tuple[int, int], sp.Expr] = {}
    for left in range(7):
        for right in range(left + 1, 7):
            if MIXED_COLOURS[left] == MIXED_COLOURS[right]:
                chart = charts[MIXED_COLOURS[left]]
                core_edges[left, right] = edge_weight(chart, Z[left], Z[right])
            else:
                core_edges[left, right] = variables[left, right]
    return incidence, core_edges, variables


def permanent_evaluator(matrix: sp.Matrix):
    @cache
    def permanent(rows: tuple[int, ...], columns: tuple[int, ...]) -> sp.Expr:
        if not rows:
            return sp.Integer(1)
        first = rows[0]
        return sp.expand(
            sum(
                matrix[first, column]
                * permanent(rows[1:], columns[:position] + columns[position + 1 :])
                for position, column in enumerate(columns)
            )
        )

    return permanent


def degree_five_response(
    survivor_face: str,
    incidence: sp.Matrix,
    core_edges: dict[tuple[int, int], sp.Expr],
    permanent,
) -> sp.Expr:
    columns = tuple(P.index(terminal) for terminal in survivor_face)
    total = sp.Integer(0)
    for left in range(7):
        for right in range(left + 1, 7):
            remaining_rows = tuple(index for index in range(7) if index not in (left, right))
            total += core_edges[left, right] * permanent(remaining_rows, columns)
    return sp.expand(total)


def main() -> None:
    incidence, core_edges, variables = mixed_incidence_and_core()
    permanent = permanent_evaluator(incidence)
    responses = {
        face: degree_five_response(face, incidence, core_edges, permanent)
        for face in SURVIVOR_FACES
    }

    rho = scalar.RHO
    x = variables
    common_part = (-5 - 2 * rho / 21) * x[0, 3] - rho * x[0, 4]
    expected = {
        "125ab": common_part - sp.Rational(1, 7) + rho / 7,
        "145ab": common_part
        + (sp.Rational(230, 7) + 104 * rho / 49) * x[2, 3]
        - rho * x[2, 5] / 7
        - sp.Rational(1, 7)
        + rho / 7,
        "235ab": common_part
        + (sp.Rational(230, 7) + 104 * rho / 49) * x[1, 4]
        + (-sp.Rational(5, 7) - 2 * rho / 147) * x[1, 5]
        - sp.Rational(1, 7)
        + rho / 7,
        "345ab": common_part
        + (sp.Rational(230, 7) + 104 * rho / 49) * (x[1, 4] + x[2, 3])
        + (-sp.Rational(5, 7) - 2 * rho / 147) * x[1, 5]
        - rho * x[2, 5] / 7
        + sp.Rational(229, 7)
        + 111 * rho / 49,
    }
    for face in SURVIVOR_FACES:
        assert sp.simplify(responses[face] - expected[face]) == 0

    circuit = sp.expand(
        responses["125ab"]
        - responses["145ab"]
        - responses["235ab"]
        + responses["345ab"]
    )
    for variable in variables.values():
        assert sp.diff(circuit, variable) == 0
    target = 2 * (805 + 52 * rho) / 49
    assert sp.simplify(circuit - target) == 0
    norm = 805**2 - 21 * 52**2
    assert norm == 591241
    assert norm > 0

    deletion_faces = {
        face: "".join(terminal for terminal in P if terminal not in face)
        for face in SURVIVOR_FACES
    }
    assert deletion_faces == {
        "125ab": "34",
        "145ab": "23",
        "235ab": "14",
        "345ab": "12",
    }

    print("fixed-chart degree-five mixed circuit: VERIFIED")
    print("mixed_core_word=(2,2,2,0,0,0,0)")
    print("faces=125ab-145ab-235ab+345ab")
    print("cross_colour_core_variables=12 all_cancel")
    print("circuit=2*(805+52*sqrt(21))/49 != 0")
    print("support_search=0 parameter_sweep=0 subset_family_enumeration=0")
    print("scope=these_fixed_pure_scalar_certificates_only")


if __name__ == "__main__":
    main()
