"""Independent exact audit of diagonal gluing and its mixed-word witness.

This audit imports neither SymPy nor either primary verifier.  It reconstructs
the three scalar charts in Q[rho]/(rho^2-21), glues their diagonal block
evaluations, and checks the pure and selected mixed coefficients directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from itertools import combinations


@dataclass(frozen=True)
class Q21:
    rational: Fraction = Fraction(0)
    radical: Fraction = Fraction(0)

    def __init__(self, rational=0, radical=0):
        object.__setattr__(self, "rational", Fraction(rational))
        object.__setattr__(self, "radical", Fraction(radical))

    @staticmethod
    def coerce(value) -> Q21:
        return value if isinstance(value, Q21) else Q21(value)

    def __add__(self, other) -> Q21:
        other = self.coerce(other)
        return Q21(self.rational + other.rational, self.radical + other.radical)

    __radd__ = __add__

    def __neg__(self) -> Q21:
        return Q21(-self.rational, -self.radical)

    def __sub__(self, other) -> Q21:
        return self + (-self.coerce(other))

    def __rsub__(self, other) -> Q21:
        return self.coerce(other) - self

    def __mul__(self, other) -> Q21:
        other = self.coerce(other)
        return Q21(
            self.rational * other.rational + 21 * self.radical * other.radical,
            self.rational * other.radical + self.radical * other.rational,
        )

    __rmul__ = __mul__


ZERO = Q21()
ONE = Q21(1)
RHO = Q21(0, 1)
INV_RHO = Q21(0, Fraction(1, 21))
KAPPA = Q21(1, Fraction(22, 21))
P = ("1", "2", "3", "4", "5", "a", "b")
Q = frozenset(("a", "b"))
Z = tuple(f"z{index}" for index in range(7))
VERTICES = Z + P
SIGMA = {"1": "4", "4": "1", "2": "3", "3": "2", "5": "5", "a": "b", "b": "a"}


def add_edge(
    graph: dict[frozenset[str], Q21],
    left: str,
    right: str,
    weight,
) -> None:
    key = frozenset((left, right))
    assert len(key) == 2 and key not in graph
    graph[key] = Q21.coerce(weight)


def weight(graph: dict[frozenset[str], Q21], left: str, right: str) -> Q21:
    return graph.get(frozenset((left, right)), ZERO)


def hafnian_evaluator(graph: dict[frozenset[str], Q21]):
    @cache
    def hafnian(vertices: tuple[str, ...]) -> Q21:
        if not vertices:
            return ONE
        if len(vertices) % 2:
            return ZERO
        first = vertices[0]
        total = ZERO
        for position in range(1, len(vertices)):
            edge = weight(graph, first, vertices[position])
            if edge != ZERO:
                rest = vertices[1:position] + vertices[position + 1 :]
                total += edge * hafnian(rest)
        return total

    return lambda vertices: hafnian(tuple(sorted(vertices)))


def formal_ledger() -> dict[int, dict[frozenset[str], Q21]]:
    deletions = [
        frozenset(deletion)
        for size in (2, 4, 6)
        for deletion in combinations(P, size)
        if not (size == 2 and frozenset(deletion) == Q)
    ]
    assert len(deletions) == 62
    ledger = {colour: {deletion: ZERO for deletion in deletions} for colour in range(3)}

    def assign(deletion: str, colour: int, value=1) -> None:
        ledger[colour][frozenset(deletion)] = Q21.coerce(value)

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
    assign("1234", 2, Fraction(1, 7))
    assign("1234ab", 2, Fraction(1, 7))
    return ledger


def common_terminal_block() -> dict[frozenset[str], Q21]:
    graph: dict[frozenset[str], Q21] = {}
    for pair, edge_weight in {
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
    }.items():
        add_edge(graph, pair[0], pair[1], edge_weight)
    return graph


def build_colour_zero():
    graph = dict(common_terminal_block())
    core = ("f1", "f2", "ell", "h3", "h4", "h5", "ha")
    for left, right, edge_weight in (
        ("f1", "1", 1),
        ("f2", "2", 1),
        ("ell", "3", 1),
        ("ell", "5", 1),
        ("ell", "a", 1),
        ("h3", "3", 1),
        ("h4", "4", 1),
        ("h5", "5", 1),
        ("ha", "a", 1),
        ("h3", "h5", RHO),
        ("h4", "h5", -6 - INV_RHO),
        ("h4", "ha", INV_RHO),
        ("h5", "ha", KAPPA),
        ("h3", "b", -RHO),
        ("h4", "b", Q21(-5, Fraction(-2, 21))),
        ("h5", "b", Q21(230, Fraction(104, 7))),
        ("ha", "b", Q21(1, Fraction(16, 21))),
    ):
        add_edge(graph, left, right, edge_weight)
    return graph, core


def relabel_terminals(graph: dict[frozenset[str], Q21]):
    result: dict[frozenset[str], Q21] = {}
    for edge, edge_weight in graph.items():
        left, right = tuple(edge)
        add_edge(result, SIGMA.get(left, left), SIGMA.get(right, right), edge_weight)
    return result


def build_colour_one():
    graph, core = build_colour_zero()
    return relabel_terminals(graph), core


def build_colour_two():
    graph = dict(common_terminal_block())
    core = ("z_*", "z_1", "z_2", "z_3", "z_4", "z_5", "z_6")
    for left, right, edge_weight in (
        ("5", "z_*", Fraction(1, 7)),
        ("z_1", "z_2", 1),
        ("z_3", "z_4", INV_RHO),
        ("z_5", "z_6", RHO),
    ):
        add_edge(graph, left, right, edge_weight)
    rows = {
        "z_1": ("1", "3"),
        "z_2": ("2", "4"),
        "z_3": ("a", "1", "3"),
        "z_4": ("b", "2", "4"),
        "z_5": ("1", "3"),
        "z_6": ("2", "4"),
    }
    for core_vertex, terminals in rows.items():
        for terminal in terminals:
            add_edge(graph, core_vertex, terminal, 1)
    return graph, core


def canonical_graph(builder):
    graph, old_core = builder()
    rename = dict(zip(old_core, Z, strict=True))
    result: dict[frozenset[str], Q21] = {}
    for edge, edge_weight in graph.items():
        left, right = tuple(edge)
        add_edge(result, rename.get(left, left), rename.get(right, right), edge_weight)
    return result


def induced_diagonal_graph(
    charts: tuple[dict[frozenset[str], Q21], ...],
    core_colours: dict[str, int],
) -> dict[frozenset[str], Q21]:
    result: dict[frozenset[str], Q21] = {}
    for left, right in combinations(VERTICES, 2):
        if left in Z and right in Z:
            if core_colours[left] == core_colours[right]:
                edge_weight = weight(charts[core_colours[left]], left, right)
            else:
                edge_weight = ZERO
        elif left in Z:
            assert right in P
            edge_weight = weight(charts[core_colours[left]], left, right)
        else:
            assert left in P and right in P
            all_weights = tuple(weight(chart, left, right) for chart in charts)
            assert all(edge_weight == all_weights[0] for edge_weight in all_weights)
            edge_weight = all_weights[0]
        if edge_weight != ZERO:
            add_edge(result, left, right, edge_weight)
    return result


def cofactor(graph: dict[frozenset[str], Q21], deletion: frozenset[str]) -> Q21:
    survivors = tuple(terminal for terminal in P if terminal not in deletion)
    return hafnian_evaluator(graph)(Z + survivors)


def main() -> None:
    assert RHO * RHO == Q21(21)
    assert INV_RHO * RHO == ONE
    ledger = formal_ledger()
    charts = tuple(
        canonical_graph(builder) for builder in (build_colour_zero, build_colour_one, build_colour_two)
    )

    free_values = (
        (ZERO, Q21(155, Fraction(110, 7))),
        (ZERO, Q21(155, Fraction(110, 7))),
        (Q21(Fraction(103, 147)), Q21(Fraction(103, 147), 36)),
    )
    checked = 0
    for colour in range(3):
        pure = induced_diagonal_graph(charts, {vertex: colour for vertex in Z})
        for pair in combinations(VERTICES, 2):
            assert weight(pure, *pair) == weight(charts[colour], *pair)
        for deletion, expected in ledger[colour].items():
            assert cofactor(pure, deletion) == expected
            checked += 1
        assert cofactor(pure, Q) == free_values[colour][0]
        assert cofactor(pure, frozenset()) == free_values[colour][1]
    assert checked == 186

    mixed_colours = {Z[index]: (2 if index < 3 else 0) for index in range(7)}
    mixed = induced_diagonal_graph(charts, mixed_colours)
    assert cofactor(mixed, frozenset("1234ab")) == Q21(Fraction(1, 7))

    print("independent exact diagonal-gluing audit: PASS")
    print("prescribed_pure_values_checked=186")
    print("mixed_witness=1/7")
    print("candidate_searches=0")


if __name__ == "__main__":
    main()
