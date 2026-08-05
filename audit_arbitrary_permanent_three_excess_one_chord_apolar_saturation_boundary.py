"""Independent no-import audit of the apolar-saturation witness."""

from __future__ import annotations

from collections import defaultdict, deque
from itertools import combinations, permutations


def determinant3(columns: tuple[tuple[int, int, int], ...]) -> int:
    a, b, c = columns
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - b[0] * (a[1] * c[2] - a[2] * c[1])
        + c[0] * (a[1] * b[2] - a[2] * b[1])
    )


def rank3(vectors: tuple[tuple[int, int, int], ...]) -> int:
    if not vectors:
        return 0
    if any(determinant3(columns) != 0 for columns in combinations(vectors, 3)):
        return 3
    if any(
        a[i] * b[j] - a[j] * b[i] != 0
        for a, b in combinations(vectors, 2)
        for i, j in ((0, 1), (0, 2), (1, 2))
    ):
        return 2
    return 1


def main() -> None:
    modes = ("a0", "a1", "a2", "r0", "r1", "r2")
    sources = ("p0", "p1", "p2", "q0", "q1", "q2")
    e0, e1, e2 = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    cells = {
        ("a0", "p0"): e0,
        ("a0", "p1"): (1, 1, 0),
        ("a0", "p2"): (-3, 0, 1),
        ("a1", "p0"): (0, 1, 1),
        ("a1", "p1"): e1,
        ("a1", "p2"): e1,
        ("a2", "p0"): e2,
        ("a2", "p2"): e2,
        ("a1", "q0"): e0,
        ("a2", "q1"): e0,
        ("a2", "q0"): e1,
        ("a2", "q2"): e2,
        ("r0", "p0"): e1,
        ("r0", "p1"): e2,
        ("r1", "p1"): e0,
        ("r2", "p2"): e0,
        ("r0", "q2"): e0,
        ("r1", "q1"): e1,
        ("r1", "q0"): e2,
        ("r2", "q2"): e1,
        ("r2", "q1"): e2,
    }
    excess = {("a0", "p1"), ("a0", "p2"), ("a1", "p0")}
    mandatory = set(cells) - excess
    assert len(cells) == 21 and len(mandatory) == 18
    assert tuple(sum(edge[0] == mode for edge in cells) for mode in modes) == (3, 4, 5, 3, 3, 3)
    assert tuple(sum(edge[1] == source for edge in cells) for source in sources) == (4, 4, 4, 3, 3, 3)

    for source in sources:
        source_vectors = [cells[edge] for edge in mandatory if edge[1] == source]
        assert sorted(source_vectors) == sorted((e0, e1, e2))
    for mode in modes:
        local_vectors = tuple(cells[edge] for edge in cells if edge[0] == mode)
        assert rank3(local_vectors) == 3

    matchings = (
        {("a0", "p0"), ("a1", "q0"), ("a2", "q1"), ("r0", "q2"), ("r1", "p1"), ("r2", "p2")},
        {("a0", "p1"), ("a1", "p2"), ("a2", "q0"), ("r0", "p0"), ("r1", "q1"), ("r2", "q2")},
        {("a0", "p2"), ("a1", "p0"), ("a2", "q2"), ("r0", "p1"), ("r1", "q0"), ("r2", "q1")},
    )
    for matching in matchings:
        assert {edge[0] for edge in matching} == set(modes)
        assert {edge[1] for edge in matching} == set(sources)
    for colour, matching in enumerate(matchings):
        assert all(cells[edge][colour] != 0 for edge in matching)

    owner = {source: mode for mode, source in matchings[0]}
    arcs: dict[str, set[str]] = defaultdict(set)
    for mode, source in cells:
        arcs[mode].add(owner[source])

    for start in modes:
        seen = {start}
        queue = deque([start])
        while queue:
            for target in arcs[queue.popleft()]:
                if target not in seen:
                    seen.add(target)
                    queue.append(target)
        assert seen == set(modes)

    exterior_matching = {("r0", "q2"), ("r1", "q0"), ("r2", "q1")}
    exterior_word = {"r0": 0, "r1": 2, "r2": 2}
    for mode, colour in exterior_word.items():
        eligible = [edge for edge in cells if edge[0] == mode and cells[edge][colour]]
        assert eligible == [next(edge for edge in exterior_matching if edge[0] == mode)]

    core_modes = ("a0", "a1", "a2")
    core_sources = ("p0", "p1", "p2")
    core_word = (0, 1, 2)
    port_terms = []
    for sigma in permutations(range(3)):
        term = 1
        for i in range(3):
            edge = (core_modes[i], core_sources[sigma[i]])
            if edge not in cells:
                term = 0
                break
            term *= cells[edge][core_word[i]]
        if term:
            port_terms.append(term)
    assert tuple(port_terms) == (1, 1, 1, -3)
    assert sum(port_terms) == 0

    boundary_vectors = (
        (),
        (cells[("a1", "q0")],),
        (cells[("a2", "q0")], cells[("a2", "q1")], cells[("a2", "q2")]),
    )
    boundary_ranks = tuple(rank3(vectors) for vectors in boundary_vectors)
    assert boundary_ranks == (0, 1, 3)
    assert tuple(3 - rank for rank in boundary_ranks) == (3, 2, 0)

    theta_matchings = (
        {("a0", "p0"), ("a1", "p1"), ("a2", "p2")},
        {("a0", "p1"), ("a1", "p0"), ("a2", "p2")},
        {("a0", "p2"), ("a1", "p1"), ("a2", "p0")},
    )
    backbone = set().union(*matchings)
    defects = tuple(len(theta - backbone) for theta in theta_matchings)
    assert defects == (2, 1, 2)

    print("independent no-import one-chord apolar saturation audit: PASS")


if __name__ == "__main__":
    main()
