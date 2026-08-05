"""Primary checks for the bosonic Plucker defect and six-token boundary."""

from __future__ import annotations

from collections import Counter
from itertools import permutations

import sympy as sp


Edge = tuple[str, str]


def permanent(matrix: sp.Matrix) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(matrix[row, permutation[row]] for row in range(matrix.rows))
            for permutation in permutations(range(matrix.cols))
        )
    )


def perfect(edges: set[Edge], modes: set[str], sources: set[str]) -> bool:
    return (
        len(edges) == len(modes)
        and {left for left, _ in edges} == modes
        and {right for _, right in edges} == sources
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


def support_model() -> tuple[set[Edge], set[str], set[str]]:
    modes = {f"a{i}" for i in range(3)} | {f"b{i}" for i in range(3)}
    sources = {f"p{i}" for i in range(3)} | {f"q{i}" for i in range(3)}
    ap = {(f"a{i}", f"p{j}") for i in range(3) for j in range(3)}
    spokes = {(f"a{i}", f"q{i}") for i in range(3)}
    spokes |= {(f"b{i}", f"p{i}") for i in range(3)}
    outer = {(f"b{i}", f"q{i}") for i in range(3)}
    outer |= {(f"b{i}", f"q{(i + 1) % 3}") for i in range(3)}
    return ap | spokes | outer, modes, sources


def matching_containing_ap(i: int, j: int) -> set[Edge]:
    remaining_modes = [index for index in range(3) if index != i]
    remaining_sources = [index for index in range(3) if index != j]
    ap_matching = {(f"a{i}", f"p{j}")}
    ap_matching |= {
        (f"a{left}", f"p{right}")
        for left, right in zip(remaining_modes, remaining_sources, strict=True)
    }
    return ap_matching | {(f"b{k}", f"q{k}") for k in range(3)}


def main() -> None:
    symbols = sp.symbols("x11:14 x21:24 x31:34")
    generic = sp.Matrix(3, 3, symbols)
    minors = {
        (i, j): permanent(generic.minor_submatrix(i, j))
        for i in range(3)
        for j in range(3)
    }
    identity = (
        permanent(generic) * generic[2, 2]
        - minors[0, 0] * minors[1, 1]
        - minors[0, 1] * minors[1, 0]
        + 2 * generic[0, 2] * generic[1, 2] * generic[2, 0] * generic[2, 1]
    )
    assert sp.expand(identity) == 0

    root_two = sp.sqrt(2)
    bypass = sp.Matrix(
        [
            [1, 1, 1 - root_two],
            [-1, 1, 1],
            [1 + root_two, -1, 1],
        ]
    )
    bypass_minors = {
        (i, j): sp.simplify(permanent(bypass.minor_submatrix(i, j)))
        for i in range(3)
        for j in range(3)
    }
    assert permanent(bypass) == 0
    assert [bypass_minors[i, i] for i in range(3)] == [0, 0, 0]
    assert bypass_minors[0, 1] == bypass_minors[1, 0] == root_two
    defect = sp.expand(
        2 * bypass[0, 2] * bypass[1, 2] * bypass[2, 0] * bypass[2, 1]
    )
    assert defect == 2

    support, modes, sources = support_model()
    assert len(support) == 21 == 3 * len(modes) + 3
    assert connected(support)
    mode_degrees = Counter(left for left, _ in support)
    source_degrees = Counter(right for _, right in support)
    assert {mode_degrees[f"a{i}"] for i in range(3)} == {4}
    assert {mode_degrees[f"b{i}"] for i in range(3)} == {3}
    assert {source_degrees[f"p{i}"] for i in range(3)} == {4}
    assert {source_degrees[f"q{i}"] for i in range(3)} == {3}

    witnesses: dict[Edge, set[Edge]] = {}
    for i in range(3):
        for j in range(3):
            edge = (f"a{i}", f"p{j}")
            witnesses[edge] = matching_containing_ap(i, j)
    diagonal_outer = {(f"b{i}", f"q{i}") for i in range(3)}
    shifted_outer = {(f"b{i}", f"q{(i + 1) % 3}") for i in range(3)}
    diagonal_ap = {(f"a{i}", f"p{i}") for i in range(3)}
    for edge in diagonal_outer:
        witnesses[edge] = diagonal_outer | diagonal_ap
    for edge in shifted_outer:
        witnesses[edge] = shifted_outer | diagonal_ap
    for i in range(3):
        mixed_witness = {(f"a{i}", f"q{i}"), (f"b{i}", f"p{i}")}
        mixed_witness |= {
            edge
            for j in range(3)
            if j != i
            for edge in ((f"a{j}", f"p{j}"), (f"b{j}", f"q{j}"))
        }
        witnesses[(f"a{i}", f"q{i}")] = mixed_witness
        witnesses[(f"b{i}", f"p{i}")] = mixed_witness
    assert set(witnesses) == support
    assert all(edge in witness and perfect(witness, modes, sources) for edge, witness in witnesses.items())

    theta = {
        ("a0", "p0"),
        ("a0", "p1"),
        ("a1", "p1"),
        ("a1", "p0"),
        ("a0", "p2"),
        ("a2", "p2"),
        ("a2", "p0"),
    }
    chords = {("a1", "p2"), ("a2", "p1")}
    assert theta | chords == {(f"a{i}", f"p{j}") for i in range(3) for j in range(3)}
    theta_vertices = {endpoint for edge in theta for endpoint in edge}
    outside_modes = modes - theta_vertices
    outside_sources = sources - theta_vertices
    assert perfect(diagonal_outer, outside_modes, outside_sources)

    excess = {(f"a{i}", f"p{i}") for i in range(3)}
    colours: dict[Edge, set[int]] = {edge: {0, 1, 2} for edge in excess}
    for i in range(3):
        for j in range(3):
            if i != j:
                colours[(f"a{i}", f"p{j}")] = {i}
        colours[(f"a{i}", f"q{i}")] = {(i + 1) % 3}
        colours[(f"b{i}", f"p{i}")] = {i}
        colours[(f"b{i}", f"q{i}")] = {(i + 2) % 3}
        colours[(f"b{i}", f"q{(i + 1) % 3}")] = {(i + 1) % 3}
    assert set(colours) == support
    mandatory = support - excess
    for source in sources:
        source_colours = [next(iter(colours[edge])) for edge in mandatory if edge[1] == source]
        assert Counter(source_colours) == Counter({0: 1, 1: 1, 2: 1})

    for i in range(3):
        a_vectors = []
        for edge in support:
            if edge[0] == f"a{i}":
                a_vectors.append([int(colour in colours[edge]) for colour in range(3)])
        assert sp.Matrix(a_vectors).rank() == 3
        b_vectors = []
        for edge in support:
            if edge[0] == f"b{i}":
                b_vectors.append([int(colour in colours[edge]) for colour in range(3)])
        assert sp.Matrix(b_vectors).rank() == 3

    for c in range(3):
        pure = {
            (f"a{(c - 1) % 3}", f"q{(c - 1) % 3}"),
            (f"b{(c - 2) % 3}", f"q{(c - 2) % 3}"),
            (f"b{(c - 1) % 3}", f"q{c}"),
            (f"b{c}", f"p{c}"),
            (f"a{c}", f"p{(c - 1) % 3}"),
            (f"a{(c + 1) % 3}", f"p{(c + 1) % 3}"),
        }
        assert perfect(pure, modes, sources)
        assert all(c in colours[edge] for edge in pure)

    word = {f"a{i}": i for i in range(3)} | {f"b{i}": (i + 2) % 3 for i in range(3)}
    eligible = {edge for edge in support if word[edge[0]] in colours[edge]}
    expected = {(f"a{i}", f"p{j}") for i in range(3) for j in range(3)} | diagonal_outer
    assert eligible == expected

    print("arbitrary permanent bosonic Plucker defect theorem: PASS")
    print("symbolic and constructive witness checks only; no support-family census was performed")


if __name__ == "__main__":
    main()
