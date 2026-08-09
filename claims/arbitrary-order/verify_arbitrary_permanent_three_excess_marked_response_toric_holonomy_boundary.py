"""Exact verifier for the marked-response alternating-separator boundary."""

from __future__ import annotations

from collections import Counter, defaultdict

import sympy as sp


Vector = tuple[int, int, int]
Edge = tuple[str, str]


def permanental_cofactor_transpose(matrix: sp.Matrix) -> sp.Matrix:
    rows, columns = matrix.shape
    assert rows == columns
    return sp.Matrix(
        columns,
        rows,
        lambda q, r: matrix.minor_submatrix(r, q).per(),
    )


def dot(vector: Vector, mark: Vector) -> int:
    return sum(x * y for x, y in zip(vector, mark, strict=True))


def is_perfect_matching(
    edges: set[Edge], modes: tuple[str, ...], sources: tuple[str, ...]
) -> bool:
    return (
        len(edges) == len(modes)
        and {mode for mode, _ in edges} == set(modes)
        and {source for _, source in edges} == set(sources)
    )


def reachable(adjacency: dict[str, set[str]], start: str) -> set[str]:
    seen = {start}
    frontier = [start]
    while frontier:
        vertex = frontier.pop()
        for neighbor in adjacency[vertex] - seen:
            seen.add(neighbor)
            frontier.append(neighbor)
    return seen


def check_abstract_response() -> None:
    s, t = sp.symbols("s t", nonzero=True)
    w = sp.eye(2)
    y = sp.eye(2)
    z = sp.Matrix(((1, s), (t, 1)))
    c_per = permanental_cofactor_transpose(w)
    assert c_per == sp.eye(2)

    omega = y * c_per * z
    assert omega == z
    assert sp.factor(omega.det()) == 1 - s * t

    degree_two_response = y.per() * z.per()
    assert sp.factor(degree_two_response) == 1 + s * t
    assert sp.expand(2 * degree_two_response - 2 * (1 + s * t)) == 0

    # Every elementary coefficient and the top balanced coefficient are
    # symbolically nonzero away from s*t in {0,-1}; no feasible-set census
    # is used here.
    assert all(entry != 0 for entry in omega)


def check_tight_physical_countermodel() -> None:
    modes = ("a0", "a1", "a2", "r1", "r2")
    sources = ("p0", "p1", "p2", "q1", "q2")
    e0, e1, e2 = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    l0, l1, l2 = (1, 1, 1), (1, 2, 1), (1, 1, -2)

    cells: dict[Edge, Vector] = {
        ("a0", "p0"): l0,
        ("a0", "p1"): l1,
        ("a0", "p2"): l2,
        ("a1", "p0"): e0,
        ("a1", "p1"): e0,
        ("a2", "p0"): e1,
        ("a2", "p2"): e1,
        ("a1", "q1"): e1,
        ("a1", "q2"): e2,
        ("a2", "q1"): e2,
        ("a2", "q2"): (2, 0, 0),
        ("r1", "q1"): e0,
        ("r2", "q2"): e1,
        ("r1", "p0"): e2,
        ("r1", "p1"): e1,
        ("r1", "p2"): e2,
        ("r2", "p1"): e2,
        ("r2", "p2"): e0,
    }
    assert len(cells) == 18 == 3 * len(modes) + 3

    mode_degrees = Counter(mode for mode, _ in cells)
    source_degrees = Counter(source for _, source in cells)
    assert tuple(mode_degrees[mode] for mode in modes) == (3, 4, 4, 4, 3)
    assert tuple(source_degrees[source] for source in sources) == (4, 4, 4, 3, 3)

    def coordinate(vector: Vector) -> int | None:
        support = [index for index, value in enumerate(vector) if value]
        return support[0] if len(support) == 1 else None

    for source in sources:
        colors = Counter(
            coordinate(vector)
            for (mode, endpoint), vector in cells.items()
            if endpoint == source and coordinate(vector) is not None
        )
        assert colors == Counter({0: 1, 1: 1, 2: 1})

    excess = {edge for edge, vector in cells.items() if coordinate(vector) is None}
    assert excess == {("a0", "p0"), ("a0", "p1"), ("a0", "p2")}

    for mode in modes:
        local_vectors = [vector for (row, _), vector in cells.items() if row == mode]
        assert sp.Matrix.hstack(*(sp.Matrix(vector) for vector in local_vectors)).rank() == 3
    assert sp.Matrix.hstack(sp.Matrix(l0), sp.Matrix(l1), sp.Matrix(l2)).det() == -3

    pure = {
        0: {
            ("r1", "q1"),
            ("a2", "q2"),
            ("a0", "p0"),
            ("a1", "p1"),
            ("r2", "p2"),
        },
        1: {
            ("a1", "q1"),
            ("r2", "q2"),
            ("a0", "p0"),
            ("a2", "p2"),
            ("r1", "p1"),
        },
        2: {
            ("a2", "q1"),
            ("a1", "q2"),
            ("a0", "p0"),
            ("r1", "p2"),
            ("r2", "p1"),
        },
    }
    for color, matching in pure.items():
        assert is_perfect_matching(matching, modes, sources)
        assert all(cells[edge][color] != 0 for edge in matching)

    # Forced decompositions of the three pure coefficients.
    pure0 = 2 * (l0[0] + l1[0])
    pure1 = l0[1] + l2[1]
    pure2 = l0[2] + l2[2]
    assert (pure0, pure1, pure2) == (4, 2, -1)

    f_matching = {
        ("a0", "p0"),
        ("a1", "p1"),
        ("a2", "p2"),
        ("r1", "q1"),
        ("r2", "q2"),
    }
    assert is_perfect_matching(f_matching, modes, sources)
    assert f_matching <= set().union(*pure.values())

    word = {"a0": 2, "a1": 0, "a2": 1, "r1": 0, "r2": 1}
    eligible = {edge for edge, vector in cells.items() if vector[word[edge[0]]] != 0}
    theta = {
        ("a0", "p0"),
        ("a0", "p1"),
        ("a0", "p2"),
        ("a1", "p0"),
        ("a1", "p1"),
        ("a2", "p0"),
        ("a2", "p2"),
    }
    empty_exterior = {("r1", "q1"), ("r2", "q2")}
    assert eligible == theta | empty_exterior
    aligned_coefficient = l0[2] + l1[2] + l2[2]
    assert aligned_coefficient == 1 + 1 - 2 == 0

    # Conformality and matching-coveredness follow from one matching and its
    # contracted alternating digraph; no perfect-matching family is listed.
    assert is_perfect_matching(empty_exterior, ("r1", "r2"), ("q1", "q2"))
    matched_source_to_mode = {source: mode for mode, source in f_matching}
    adjacency: dict[str, set[str]] = defaultdict(set)
    for mode in modes:
        adjacency[mode]
    for edge in cells:
        if edge not in f_matching:
            mode, source = edge
            adjacency[mode].add(matched_source_to_mode[source])
    expected_adjacency = {
        "a0": {"a1", "a2"},
        "a1": {"a0", "r1", "r2"},
        "a2": {"a0", "r1", "r2"},
        "r1": {"a0", "a1", "a2"},
        "r2": {"a1", "a2"},
    }
    assert dict(adjacency) == expected_adjacency
    assert all(reachable(adjacency, mode) == set(modes) for mode in modes)

    outgoing_colors = Counter(
        coordinate(cells[edge])
        for edge in cells
        if edge[0] in {"a0", "a1", "a2"} and edge[1] in {"q1", "q2"}
    )
    incoming_colors = Counter(
        coordinate(cells[edge])
        for edge in cells
        if edge[0] in {"r1", "r2"} and edge[1] in {"p0", "p1", "p2"}
    )
    assert outgoing_colors == Counter({0: 1, 1: 1, 2: 2})
    assert incoming_colors == Counter({0: 1, 1: 1, 2: 3})
    assert incoming_colors - outgoing_colors == Counter({2: 1})

    # Transverse pair-deletion jet for the anchor-a0p1 cofactor block:
    # entrance rows (a1,a2), exit columns (p0,p2).
    entrance_marks = {"a1": (0, 1, 1), "a2": (1, 0, 1)}
    exterior_marks = {"r1": (1, 0, 1), "r2": (1, 1, 0)}
    y = sp.Matrix(
        2,
        2,
        lambda i, j: dot(
            cells[(("a1", "a2")[i], ("q1", "q2")[j])],
            entrance_marks[("a1", "a2")[i]],
        ),
    )
    w = sp.diag(
        dot(cells[("r1", "q1")], exterior_marks["r1"]),
        dot(cells[("r2", "q2")], exterior_marks["r2"]),
    )
    z = sp.Matrix(
        2,
        2,
        lambda i, j: dot(
            cells.get((("r1", "r2")[i], ("p0", "p2")[j]), (0, 0, 0)),
            exterior_marks[("r1", "r2")[i]],
        ),
    )
    assert y == sp.Matrix(((1, 1), (1, 2)))
    assert w == sp.eye(2)
    assert z == sp.Matrix(((1, 1), (0, 1)))
    omega = y * permanental_cofactor_transpose(w) * z
    assert omega == sp.Matrix(((1, 2), (1, 3)))
    assert y.det() == z.det() == omega.det() == 1

    # The exact projected residue certifies failure of P_5 -> Delta_3.
    residue = sp.Matrix(l0) + sp.Matrix(l1) + sp.Matrix(l2)
    assert residue == sp.Matrix((3, 4, 0))
    assert residue != sp.zeros(3, 1)


def check_one_channel_exception() -> None:
    y0, y1, z0, z1 = sp.symbols("y0 y1 z0 z1")
    omega_one = sp.Matrix((y0, y1)) * sp.Matrix(((z0, z1),))
    assert sp.factor(omega_one.det()) == 0


def main() -> None:
    check_abstract_response()
    check_tight_physical_countermodel()
    check_one_channel_exception()
    print("marked-response alternating-separator boundary: PASS")
    print("tight physical countermodel, full-rank jet, and one-channel exception")


if __name__ == "__main__":
    main()
