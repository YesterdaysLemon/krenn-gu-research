"""Verify the exact common-terminal-block scalar realizations.

Three explicit seven-core graphs use one terminal block over Q(sqrt(21)) and
realize the 186 prescribed coordinates of the formal 2+2+1 ledger.  This is a
fixed certificate check, with no support search or parameter sweep.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp

P = ("1", "2", "3", "4", "5", "a", "b")
Q = frozenset(("a", "b"))
RHO = sp.sqrt(21)
KAPPA = 1 + 22 / RHO
SIGMA = {"1": "4", "4": "1", "2": "3", "3": "2", "5": "5", "a": "b", "b": "a"}


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
        ledger[colour][frozenset(deletion)] = sp.sympify(value)

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

    for deletion, colour in {
        "123a": 2,
        "124b": 2,
        "134a": 2,
        "234b": 2,
        "125a": 1,
        "345b": 0,
    }.items():
        assign(deletion, colour)

    assign("1234", 2, sp.Rational(1, 7))
    assign("1234ab", 2, sp.Rational(1, 7))
    return ledger, len(prescribed)


def common_terminal_block() -> dict[frozenset[str], sp.Expr]:
    weights = {
        "12": -KAPPA,
        "14": -KAPPA,
        "23": -KAPPA,
        "34": -KAPPA,
        "13": 7,
        "24": 7,
        "1a": 7,
        "3a": 7,
        "2b": 7,
        "4b": 7,
        "1b": -RHO,
        "2a": -RHO,
        "3b": -RHO,
        "4a": -RHO,
        "ab": 1 - RHO,
    }
    return {frozenset(pair): sp.sympify(weight) for pair, weight in weights.items()}


def graph_with_common_terminal_block() -> dict[frozenset[str], sp.Expr]:
    return dict(common_terminal_block())


def build_colour_zero():
    graph = graph_with_common_terminal_block()
    core = ("f1", "f2", "ell", "h3", "h4", "h5", "ha")

    add_edge(graph, "f1", "1", 1)
    add_edge(graph, "f2", "2", 1)
    for terminal in ("3", "5", "a"):
        add_edge(graph, "ell", terminal, 1)
    for terminal in ("3", "4", "5", "a"):
        add_edge(graph, "h" + terminal, terminal, 1)

    add_edge(graph, "h3", "h5", RHO)
    add_edge(graph, "h4", "h5", -6 - 1 / RHO)
    add_edge(graph, "h4", "ha", 1 / RHO)
    add_edge(graph, "h5", "ha", KAPPA)

    b_column = {
        "h3": -RHO,
        "h4": -5 - 2 * RHO / 21,
        "h5": 230 + 104 * RHO / 7,
        "ha": 1 + 16 * RHO / 21,
    }
    for core_vertex, weight in b_column.items():
        add_edge(graph, core_vertex, "b", weight)
    return graph, core


def relabel_terminals(
    graph: dict[frozenset[str], sp.Expr],
    permutation: dict[str, str],
) -> dict[frozenset[str], sp.Expr]:
    result: dict[frozenset[str], sp.Expr] = {}
    for edge, weight in graph.items():
        left, right = tuple(edge)
        add_edge(result, permutation.get(left, left), permutation.get(right, right), weight)
    return result


def build_colour_one():
    graph, core = build_colour_zero()
    return relabel_terminals(graph, SIGMA), core


def build_colour_two():
    graph = graph_with_common_terminal_block()
    core = ("z_*", "z_1", "z_2", "z_3", "z_4", "z_5", "z_6")
    add_edge(graph, "5", "z_*", sp.Rational(1, 7))
    add_edge(graph, "z_1", "z_2", 1)
    add_edge(graph, "z_3", "z_4", 1 / RHO)
    add_edge(graph, "z_5", "z_6", RHO)

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
    return graph, core


def terminal_block(graph: dict[frozenset[str], sp.Expr]):
    return {
        frozenset(pair): graph.get(frozenset(pair), sp.Integer(0))
        for pair in combinations(P, 2)
    }


def cofactor(deletion: frozenset[str], core: tuple[str, ...], hafnian) -> sp.Expr:
    surviving = tuple(terminal for terminal in P if terminal not in deletion)
    return hafnian(core + surviving)


def check_wick_anchor_derivation() -> None:
    """Check the determinant-one four-core construction behind colour 0."""

    anchors = ("3", "4", "5", "a")
    b_values = {
        "34": KAPPA,
        "35": 1 / RHO,
        "3a": -6 - 1 / RHO,
        "45": 0,
        "4a": RHO,
        "5a": 0,
    }
    b_matrix = sp.zeros(4)
    for pair, value in b_values.items():
        left, right = (anchors.index(pair[0]), anchors.index(pair[1]))
        b_matrix[left, right] = b_matrix[right, left] = value
    assert sp.simplify(b_matrix.det() - 1) == 0

    v = sp.Matrix(
        (-RHO, -5 - 2 * RHO / 21, 230 + 104 * RHO / 7, 1 + 16 * RHO / 21)
    )
    desired_b_pairs = sp.Matrix((1 + RHO, -6, -1, -1 + RHO))
    assert all(sp.simplify(value) == 0 for value in b_matrix * v - desired_b_pairs)

    e2 = dict(b_values)
    e2.update({"3b": 1 + RHO, "4b": -6, "5b": -1, "ab": -1 + RHO})
    linear = {"3": 1, "4": 0, "5": 1, "a": 1, "b": 0}
    expected_cubic = {
        "345": KAPPA,
        "34a": 1 + 43 / RHO,
        "34b": -6,
        "35a": -6,
        "35b": RHO,
        "3ab": 2 * RHO,
        "45a": RHO,
        "45b": -6,
        "4ab": -6,
        "5ab": -2 + RHO,
    }
    for triple, expected in expected_cubic.items():
        actual = sum(
            linear[terminal]
            * e2["".join(symbol for symbol in triple if symbol != terminal)]
            for terminal in triple
            if linear[terminal] != 0
        )
        assert sp.simplify(actual - expected) == 0

    deconvolved_top = sp.simplify(v[0] + v[2] + v[3])
    assert deconvolved_top == 231 + 307 * RHO / 21
    free_empty = 155 + 110 * RHO / 7
    assert sp.simplify(free_empty + 76 - 23 / RHO - deconvolved_top) == 0


def main() -> None:
    assert sp.simplify(RHO**2 - 21) == 0
    ledger, prescribed_per_colour = formal_ledger()
    assert prescribed_per_colour == 62
    common = {
        edge: sp.simplify(weight) for edge, weight in terminal_block(common_terminal_block()).items()
    }

    # Sigma is an involutive automorphism of both M and the c0/c1 ledgers.
    assert all(SIGMA[SIGMA[terminal]] == terminal for terminal in P)
    for pair in combinations(P, 2):
        image = frozenset(SIGMA[terminal] for terminal in pair)
        assert sp.simplify(common[frozenset(pair)] - common[image]) == 0
    for deletion, value in ledger[0].items():
        image = frozenset(SIGMA[terminal] for terminal in deletion)
        assert value == ledger[1][image]

    check_wick_anchor_derivation()

    builders = (build_colour_zero, build_colour_one, build_colour_two)
    free_values = (
        (sp.Integer(0), 155 + 110 * RHO / 7),
        (sp.Integer(0), 155 + 110 * RHO / 7),
        (sp.Rational(103, 147), sp.Rational(103, 147) + 36 * RHO),
    )
    checked = 0
    for colour, (builder, (free_q, free_empty)) in enumerate(zip(builders, free_values, strict=True)):
        graph, core = builder()
        assert all(
            sp.simplify(value - common[edge]) == 0
            for edge, value in terminal_block(graph).items()
        )
        hafnian = hafnian_evaluator(graph)
        for deletion, expected in ledger[colour].items():
            assert sp.simplify(cofactor(deletion, core, hafnian) - expected) == 0
            checked += 1
        assert sp.simplify(cofactor(Q, core, hafnian) - free_q) == 0
        assert sp.simplify(cofactor(frozenset(), core, hafnian) - free_empty) == 0

    assert checked == 186
    print("common terminal block M2 across scalar charts: VERIFIED")
    print("field=Q(rho), rho^2=21")
    print("prescribed_values_checked=186")
    print("c0: C_Q=0, C_empty=155+110*rho/7")
    print("c1: C_Q=0, C_empty=155+110*rho/7")
    print("c2: C_Q=103/147, C_empty=103/147+36*rho")
    print("sigma=(1 4)(2 3)(a b): M2 invariant and c0 ledger -> c1 ledger")
    print("support_search=0 parameter_sweep=0 graph_family_enumeration=0")
    print("tensor_valued_common_graph=UNRESOLVED mixed_word_cancellation=UNRESOLVED")


if __name__ == "__main__":
    main()
