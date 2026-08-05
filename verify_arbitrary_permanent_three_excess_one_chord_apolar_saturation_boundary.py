"""Primary exact checks for the one-chord apolar-saturation boundary."""

from __future__ import annotations

from collections import defaultdict, deque
from itertools import permutations

import sympy as sp

MODES = ("a0", "a1", "a2", "r0", "r1", "r2")
SOURCES = ("p0", "p1", "p2", "q0", "q1", "q2")

E0 = (1, 0, 0)
E1 = (0, 1, 0)
E2 = (0, 0, 1)


def main() -> None:
    cells: dict[tuple[str, str], tuple[int, int, int]] = {
        ("a0", "p0"): E0,
        ("a0", "p1"): (1, 1, 0),
        ("a0", "p2"): (-3, 0, 1),
        ("a1", "p0"): (0, 1, 1),
        ("a1", "p1"): E1,
        ("a1", "p2"): E1,
        ("a2", "p0"): E2,
        ("a2", "p2"): E2,
        ("a1", "q0"): E0,
        ("a2", "q1"): E0,
        ("a2", "q0"): E1,
        ("a2", "q2"): E2,
        ("r0", "p0"): E1,
        ("r0", "p1"): E2,
        ("r1", "p1"): E0,
        ("r2", "p2"): E0,
        ("r0", "q2"): E0,
        ("r1", "q1"): E1,
        ("r1", "q0"): E2,
        ("r2", "q2"): E1,
        ("r2", "q1"): E2,
    }
    excess = {("a0", "p1"), ("a0", "p2"), ("a1", "p0")}
    mandatory = set(cells) - excess
    assert len(cells) == 21 and len(mandatory) == 18 and len(excess) == 3

    # One mandatory coordinate cell for every source and colour.
    for source in SOURCES:
        colours = []
        for edge in mandatory:
            if edge[1] != source:
                continue
            vector = cells[edge]
            assert sum(value != 0 for value in vector) == 1
            colours.append(next(i for i, value in enumerate(vector) if value))
        assert sorted(colours) == [0, 1, 2]

    mode_degrees = tuple(sum(edge[0] == mode for edge in cells) for mode in MODES)
    source_degrees = tuple(
        sum(edge[1] == source for edge in cells) for source in SOURCES
    )
    assert mode_degrees == (3, 4, 5, 3, 3, 3)
    assert source_degrees == (4, 4, 4, 3, 3, 3)

    for mode in MODES:
        local = sp.Matrix.hstack(
            *(sp.Matrix(cells[edge]) for edge in cells if edge[0] == mode)
        )
        assert local.rank() == 3

    matchings = {
        0: {("a0", "p0"), ("a1", "q0"), ("a2", "q1"), ("r0", "q2"), ("r1", "p1"), ("r2", "p2")},
        1: {("a0", "p1"), ("a1", "p2"), ("a2", "q0"), ("r0", "p0"), ("r1", "q1"), ("r2", "q2")},
        2: {("a0", "p2"), ("a1", "p0"), ("a2", "q2"), ("r0", "p1"), ("r1", "q0"), ("r2", "q1")},
    }
    for colour, matching in matchings.items():
        assert {edge[0] for edge in matching} == set(MODES)
        assert {edge[1] for edge in matching} == set(SOURCES)
        assert all(cells[edge][colour] != 0 for edge in matching)

    # Strong connectivity of the M0-contracted alternating digraph.
    owner = {source: mode for mode, source in matchings[0]}
    arcs: dict[str, set[str]] = defaultdict(set)
    for mode, source in cells:
        arcs[mode].add(owner[source])

    def reachable(start: str) -> set[str]:
        seen = {start}
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for target in arcs[vertex]:
                if target not in seen:
                    seen.add(target)
                    queue.append(target)
        return seen

    assert all(reachable(mode) == set(MODES) for mode in MODES)

    exterior_matching = {("r0", "q2"), ("r1", "q0"), ("r2", "q1")}
    exterior_word = {"r0": 0, "r1": 2, "r2": 2}
    for mode, colour in exterior_word.items():
        eligible = [edge for edge in cells if edge[0] == mode and cells[edge][colour]]
        assert eligible == [next(edge for edge in exterior_matching if edge[0] == mode)]

    core_matrix = sp.Matrix([[1, 1, -3], [1, 1, 1], [1, 0, 1]])
    terms = tuple(
        sp.prod(core_matrix[i, sigma[i]] for i in range(3))
        for sigma in permutations(range(3))
        if sp.prod(core_matrix[i, sigma[i]] for i in range(3)) != 0
    )
    assert terms == (1, 1, 1, -3)
    assert sum(terms) == 0

    boundary_vectors = {
        "a0": (),
        "a1": (E0,),
        "a2": (E0, E1, E2),
    }
    boundary_ranks = []
    for mode in ("a0", "a1", "a2"):
        vectors = boundary_vectors[mode]
        rank = 0 if not vectors else sp.Matrix.hstack(*(sp.Matrix(v) for v in vectors)).rank()
        boundary_ranks.append(rank)
    assert tuple(boundary_ranks) == (0, 1, 3)
    assert tuple(3 - rank for rank in boundary_ranks) == (3, 2, 0)

    theta_matchings = (
        {("a0", "p0"), ("a1", "p1"), ("a2", "p2")},
        {("a0", "p1"), ("a1", "p0"), ("a2", "p2")},
        {("a0", "p2"), ("a1", "p1"), ("a2", "p0")},
    )
    backbone = set().union(*matchings.values())
    defects = tuple(len(theta - backbone) for theta in theta_matchings)
    assert defects == (2, 1, 2) and min(defects) == 1

    print("arbitrary permanent one-chord apolar saturation boundary: PASS")
    print("fixed symbolic witness only; no support-family or matching-tuple census")


if __name__ == "__main__":
    main()
