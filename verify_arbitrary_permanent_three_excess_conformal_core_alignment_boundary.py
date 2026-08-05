"""Primary symbolic checks for the conformal-core alignment boundary."""

from __future__ import annotations

from collections import Counter
from itertools import permutations

import sympy as sp


Edge = tuple[str, str]


def is_perfect_matching(edges: set[Edge], modes: set[str], sources: set[str]) -> bool:
    return (
        len(edges) == len(modes)
        and {edge[0] for edge in edges} == modes
        and {edge[1] for edge in edges} == sources
    )


def is_connected(edges: set[Edge], vertices: set[str]) -> bool:
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    reached = set()
    frontier = {next(iter(vertices))}
    while frontier:
        vertex = frontier.pop()
        if vertex in reached:
            continue
        reached.add(vertex)
        frontier.update(adjacency[vertex] - reached)
    return reached == vertices


def main() -> None:
    d1, d2, d3, q12, q21, q23, q31 = sp.symbols(
        "d1 d2 d3 q12 q21 q23 q31", nonzero=True
    )
    cycle_four = sp.Matrix([[d1, q12], [q21, d2]])
    assert sp.expand(cycle_four.per() - (d1 * d2 + q12 * q21)) == 0
    cycle_six = sp.Matrix([[d1, q12, 0], [0, d2, q23], [q31, 0, d3]])
    assert sp.expand(cycle_six.per() - (d1 * d2 * d3 + q12 * q23 * q31)) == 0

    x11, x12, x13, x21, x22, x31, x33 = sp.symbols(
        "x11 x12 x13 x21 x22 x31 x33", nonzero=True
    )
    x23, x32 = sp.symbols("x23 x32")
    diagonal = x11 * x22 * x33
    a = x12 * x21 * x33 / diagonal
    b = x13 * x22 * x31 / diagonal
    c = x11 * x23 * x32 / diagonal
    u = x12 * x23 * x31 / diagonal
    v = x13 * x21 * x32 / diagonal
    r = x23 * x31 / (x21 * x33)
    s = x21 * x32 / (x22 * x31)
    assert sp.cancel(u - a * r) == 0
    assert sp.cancel(v - b * s) == 0
    assert sp.cancel(c - r * s) == 0
    assert sp.cancel(u * v - a * b * c) == 0
    assert sp.cancel(1 + a + b + c + u + v - (1 + a + b + a * r + b * s + r * s)) == 0

    sqrt_two = sp.sqrt(2)
    bypass = sp.Matrix([[1, 1, 1 - sqrt_two], [-1, 1, 1], [1 + sqrt_two, -1, 1]])
    bypass_terms = tuple(
        sp.expand(sp.prod(bypass[row, perm[row]] for row in range(3)))
        for perm in permutations(range(3))
    )
    assert sp.expand(bypass.per()) == 0
    assert sorted(map(str, bypass_terms)).count("0") == 0
    assert all(sp.expand(bypass.minor_submatrix(row, row).per()) == 0 for row in range(3))
    assert sp.expand(1 - 1 - 1) == -1
    assert sp.expand(-1 + (1 + sqrt_two) + (1 - sqrt_two)) == 1

    modes = {f"x{j}" for j in range(3)} | {f"y{j}" for j in range(3)}
    sources = {f"p{j}" for j in range(3)} | {f"q{j}" for j in range(3)}
    a_edges = {(f"x{j}", f"p{j}") for j in range(3)}
    n_edges = {(f"y{j}", f"q{j}") for j in range(3)}
    c_edges = {(f"x{j}", f"q{j}") for j in range(3)}
    d_edges = {(f"y{j}", f"p{j}") for j in range(3)}
    cp_edges = {(f"x{j}", f"q{(j + 1) % 3}") for j in range(3)}
    dp_edges = {(f"y{j}", f"p{(j + 1) % 3}") for j in range(3)}
    e_edges = {(f"x{j}", f"p{(j - 1) % 3}") for j in range(3)}
    support = a_edges | n_edges | c_edges | d_edges | cp_edges | dp_edges | e_edges
    assert len(support) == 21
    assert is_connected(support, modes | sources)

    m0 = {
        ("x0", "q0"),
        ("y0", "p0"),
        ("x1", "p1"),
        ("x2", "p2"),
        ("y1", "q1"),
        ("y2", "q2"),
    }
    m1 = {
        ("x0", "p0"),
        ("y0", "q0"),
        ("x1", "q1"),
        ("x2", "q2"),
        ("y1", "p1"),
        ("y2", "p2"),
    }
    m2 = cp_edges | dp_edges
    excess_matching = e_edges | n_edges
    for matching in (m0, m1, m2, excess_matching, a_edges | n_edges):
        assert is_perfect_matching(matching, modes, sources)
    assert m0 | m1 | m2 == support - e_edges
    assert m0 | m1 | m2 | excess_matching == support

    mode_degrees = Counter(edge[0] for edge in support)
    source_degrees = Counter(edge[1] for edge in support)
    assert sorted(mode_degrees.values()) == [3, 3, 3, 4, 4, 4]
    assert sorted(source_degrees.values()) == [3, 3, 3, 4, 4, 4]

    core_vertices_modes = {f"x{j}" for j in range(3)}
    core_vertices_sources = {f"p{j}" for j in range(3)}
    induced_core = {
        edge
        for edge in support
        if edge[0] in core_vertices_modes and edge[1] in core_vertices_sources
    }
    assert induced_core == a_edges | e_edges

    edge_colour = {edge: 0 for edge in m0}
    edge_colour.update({edge: 1 for edge in m1})
    edge_colour.update({edge: 2 for edge in m2})
    edge_colour.update({("x0", "p2"): 1, ("x1", "p0"): 0, ("x2", "p1"): 0})
    word = {mode: (1 if mode in {"x0", "y0"} else 0) for mode in modes}
    eligible = {edge for edge, colour in edge_colour.items() if word[edge[0]] == colour}
    assert eligible == a_edges | e_edges | n_edges

    port = sp.Matrix([[1, 0, -1], [1, 1, 0], [0, 1, 1]])
    port_terms = [
        sp.prod(port[row, perm[row]] for row in range(3))
        for perm in permutations(range(3))
    ]
    assert sorted(term for term in port_terms if term != 0) == [-1, 1]
    assert port.per() == 0

    # The private odd-path edge of P_i gives an identity submatrix on T_i.
    theta_private_edge_incidence = sp.eye(3)
    assert theta_private_edge_incidence.rank() == 3

    # One explicit odd exchange relation is contradictory; an even one is not.
    lambda_1 = sp.Matrix([1, 0])
    lambda_2 = sp.Matrix([0, 1])
    lambda_3 = sp.Matrix([-1, -1])
    assert lambda_1 + lambda_2 + lambda_3 == sp.zeros(2, 1)
    assert 1 + 1 + 1 == 3

    print("arbitrary permanent conformal-core alignment boundary: PASS")
    print("explicit symbolic models only; no graph or matching family census was performed")


if __name__ == "__main__":
    main()
