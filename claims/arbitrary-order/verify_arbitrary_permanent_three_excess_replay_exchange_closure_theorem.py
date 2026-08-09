"""Primary symbolic checks for replay/exchange closure and counterfamilies."""

from __future__ import annotations

from collections import Counter
from itertools import combinations

import sympy as sp


Edge = tuple[str, str]


def perfect(edges: set[Edge], modes: set[str], sources: set[str]) -> bool:
    return (
        len(edges) == len(modes)
        and {edge[0] for edge in edges} == modes
        and {edge[1] for edge in edges} == sources
    )


def connected(edges: set[Edge]) -> bool:
    vertices = {endpoint for edge in edges for endpoint in edge}
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    reached: set[str] = set()
    frontier = {next(iter(vertices))}
    while frontier:
        vertex = frontier.pop()
        if vertex not in reached:
            reached.add(vertex)
            frontier.update(adjacency[vertex] - reached)
    return reached == vertices


def base_model() -> dict[str, set[Edge]]:
    modes = {f"x{j}" for j in range(3)} | {f"y{j}" for j in range(3)}
    sources = {f"p{j}" for j in range(3)} | {f"q{j}" for j in range(3)}
    named = {
        "B0": {("x0", "p2")},
        "A1": {("x1", "p1")},
        "A2": {("x2", "p2")},
        "N": {(f"y{j}", f"q{j}") for j in range(3)},
        "C": {(f"x{j}", f"q{j}") for j in range(3)},
        "D": {(f"y{j}", f"p{j}") for j in range(3)},
        "CP": {(f"x{j}", f"q{(j + 1) % 3}") for j in range(3)},
        "DP": {("y0", "p1"), ("y2", "p0")},
        "J": {("y1", "p0")},
        "E": {("x0", "p0"), ("x1", "p0"), ("x2", "p1")},
        "modes": set(),
        "sources": set(),
    }
    named["modes"] = {(mode, mode) for mode in modes}
    named["sources"] = {(source, source) for source in sources}
    return named


def extend_model(n: int) -> tuple[set[Edge], set[str], set[str], tuple[set[Edge], ...], set[Edge]]:
    named = base_model()
    modes = {edge[0] for edge in named["modes"]} | {f"u{j}" for j in range(n)}
    sources = {edge[0] for edge in named["sources"]} | {f"v{j}" for j in range(n)}

    b0 = next(iter(named["B0"]))
    a1 = next(iter(named["A1"]))
    a2 = next(iter(named["A2"]))
    n_edges = named["N"]
    c_edges = named["C"]
    d_edges = named["D"]
    cp_edges = named["CP"]
    dp_edges = named["DP"]
    j_edge = next(iter(named["J"]))
    excess = named["E"]

    m0 = {b0, a1, ("x2", "q2"), ("y0", "q0"), ("y1", "q1"), ("y2", "p0")}
    m1 = {("x0", "q0"), a2, ("y2", "q2"), ("x1", "q1"), ("y0", "p0"), ("y1", "p1")}
    m2 = {("x2", "q0"), ("y2", "p2"), ("x1", "q2"), ("x0", "q1"), j_edge, ("y0", "p1")}
    mandatory = {b0, a1, a2} | n_edges | c_edges | d_edges | cp_edges | dp_edges | {j_edge}
    assert m0 | m1 | m2 == mandatory

    l0 = {(f"u{j}", f"v{j}") for j in range(n)}
    l1 = {(f"u{j}", f"v{(j + 1) % n}") for j in range(n)}
    l2 = {(f"u{j}", f"v{(j + 2) % n}") for j in range(n)}
    removed_base = ("y0", "q0")
    removed_extension = ("u0", "v0")
    cross = {("y0", "v0"), ("u0", "q0")}

    support = (mandatory | excess | l0 | l1 | l2) - {removed_base, removed_extension}
    support |= cross
    pure0 = (m0 | l0) - {removed_base, removed_extension}
    pure0 |= cross
    pure1 = m1 | l1
    pure2 = m2 | l2
    complement = (n_edges | l0) - {removed_base, removed_extension}
    complement |= cross
    return support, modes, sources, (pure0, pure1, pure2), complement


def main() -> None:
    vectors = sp.Matrix.hstack(
        sp.Matrix([1, 1, 0, 0, 0, 0]),
        sp.Matrix([0, 0, 1, 1, 0, 0]),
        sp.Matrix([0, 0, 0, 0, 1, 1]),
        sp.Matrix([1, 0, 0, 1, 1, 0]),
        sp.Matrix([0, 1, 1, 0, 0, 1]),
    )
    relation = sp.Matrix([-1, -1, -1, 1, 1])
    assert vectors.rank() == 4
    assert vectors * relation == sp.zeros(6, 1)
    assert all(vectors[:, subset].rank() == 4 for subset in combinations(range(5), 4))
    nullspace = vectors.nullspace()
    assert len(nullspace) == 1 and nullspace[0] == relation
    assert sum(relation) == -1

    named = base_model()
    base_modes = {edge[0] for edge in named["modes"]}
    base_sources = {edge[0] for edge in named["sources"]}
    b0 = next(iter(named["B0"]))
    a1 = next(iter(named["A1"]))
    a2 = next(iter(named["A2"]))
    j_edge = next(iter(named["J"]))
    base_m0 = {b0, a1, ("x2", "q2"), ("y0", "q0"), ("y1", "q1"), ("y2", "p0")}
    base_m1 = {
        ("x0", "q0"),
        a2,
        ("y2", "q2"),
        ("x1", "q1"),
        ("y0", "p0"),
        ("y1", "p1"),
    }
    base_m2 = {
        ("x2", "q0"),
        ("y2", "p2"),
        ("x1", "q2"),
        ("x0", "q1"),
        j_edge,
        ("y0", "p1"),
    }
    base_pure = (base_m0, base_m1, base_m2)
    base_support = base_m0 | base_m1 | base_m2 | named["E"]
    assert len(base_support) == 21
    assert connected(base_support)
    assert all(perfect(matching, base_modes, base_sources) for matching in base_pure)

    core_a = {("x0", "p0"), ("x1", "p1"), ("x2", "p2")}
    core_b = {("x0", "p2"), ("x1", "p0"), ("x2", "p1")}
    outer_n = {(f"y{j}", f"q{j}") for j in range(3)}
    assert perfect(core_a | outer_n, base_modes, base_sources)
    assert perfect(core_b | outer_n, base_modes, base_sources)
    assert (core_a | core_b) == {
        edge
        for edge in base_support
        if edge[0].startswith("x") and edge[1].startswith("p")
    }

    degree_modes = Counter(edge[0] for edge in base_support)
    degree_sources = Counter(edge[1] for edge in base_support)
    assert {mode: degree_modes[mode] - 3 for mode in base_modes if degree_modes[mode] > 3} == {
        "x0": 1,
        "x1": 1,
        "x2": 1,
    }
    assert {source: degree_sources[source] - 3 for source in base_sources if degree_sources[source] > 3} == {
        "p0": 2,
        "p1": 1,
    }

    colour_two = base_pure[2] | named["E"]
    deleted_a = {"x0", "p0"}
    residual_a = {edge for edge in colour_two if not deleted_a.intersection(edge)}
    assert not any("y1" in edge for edge in residual_a)
    deleted_b = {"x1", "p0", "x2", "p1"}
    residual_b = {edge for edge in colour_two if not deleted_b.intersection(edge)}
    assert not any("y0" in edge for edge in residual_b)
    assert not any("y1" in edge for edge in residual_b)

    for n in (3, 4, 7):
        support_n, modes_n, sources_n, pure_n, complement_n = extend_model(n)
        assert len(modes_n) == len(sources_n) == 6 + n
        assert len(support_n) == 21 + 3 * n == 3 * (6 + n) + 3
        assert connected(support_n)
        assert all(perfect(matching, modes_n, sources_n) for matching in pure_n)
        outside_modes = modes_n - {"x0", "x1", "x2"}
        outside_sources = sources_n - {"p0", "p1", "p2"}
        assert perfect(complement_n, outside_modes, outside_sources)
        assert all(degree >= 3 for degree in Counter(edge[0] for edge in support_n).values())
        assert all(degree >= 3 for degree in Counter(edge[1] for edge in support_n).values())

    print("arbitrary permanent replay/exchange closure theorem: PASS")
    print("symbolic construction checks only; no graph or matching family census was performed")


if __name__ == "__main__":
    main()
