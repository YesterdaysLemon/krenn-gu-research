"""Primary exact checks for the two-switch port-completion shore theorem."""

from __future__ import annotations

from collections import defaultdict

import sympy as sp

COLORS = {"c": 0, "d": 1, "e": 2}


def validate_matching(
    matching: set[tuple[str, str]], modes: set[str], sources: set[str]
) -> None:
    assert {mode for mode, _ in matching} == modes
    assert {source for _, source in matching} == sources
    assert len(matching) == len(modes)


def main() -> None:
    left_1, left_2, right_1, right_2 = sp.symbols(
        "left_1 left_2 right_1 right_2", nonzero=True
    )
    rectangle = left_1 * right_2 + left_2 * right_1
    gain_left = left_2 / left_1
    gain_right = right_2 / right_1
    assert sp.simplify(rectangle / (left_1 * right_1) - gain_left - gain_right) == 0

    cells: dict[str, dict[str, tuple[int, int, int]]] = {
        "a": {"p1": (1, 1, 0), "p2": (1, 2, 0), "q": (0, 0, 1)},
        "bc": {"p1": (1, 0, 0), "p2": (1, 0, 0), "s": (0, 1, 0), "r": (0, 0, 1)},
        "bd": {"p1": (0, 1, 0), "p2": (0, 1, 0), "r": (1, 0, 0), "s": (0, 0, 1)},
        "x": {"q": (1, 0, 0), "t": (0, 1, 0), "p1": (0, 0, 1)},
        "y": {"t": (1, 0, 0), "q": (0, 1, 0), "p2": (0, 0, 1)},
        "z": {"s": (1, 0, 0), "r": (0, 1, 0), "t": (0, 0, 1)},
    }
    assert sum(len(row) for row in cells.values()) == 20
    assert [len(cells[mode]) for mode in ("a", "bc", "bd", "x", "y", "z")] == [
        3,
        4,
        4,
        3,
        3,
        3,
    ]
    for row in cells.values():
        assert sp.Matrix(list(row.values())).rank() == 3

    modes = set(cells)
    sources = {"p1", "p2", "q", "t", "r", "s"}
    matchings = {
        "c": {
            ("a", "p1"),
            ("bc", "p2"),
            ("bd", "r"),
            ("x", "q"),
            ("y", "t"),
            ("z", "s"),
        },
        "d": {
            ("a", "p1"),
            ("bd", "p2"),
            ("bc", "s"),
            ("x", "t"),
            ("y", "q"),
            ("z", "r"),
        },
        "e": {
            ("a", "q"),
            ("bc", "r"),
            ("bd", "s"),
            ("x", "p1"),
            ("y", "p2"),
            ("z", "t"),
        },
    }
    for colour, matching in matchings.items():
        validate_matching(matching, modes, sources)
        index = COLORS[colour]
        assert all(cells[mode][source][index] != 0 for mode, source in matching)

    residual_modes = {"x", "y", "z"}
    residual_sources = {"t", "r", "s"}
    residual_neighbors: dict[str, set[str]] = defaultdict(set)
    for mode in residual_modes:
        for source in cells[mode]:
            if source in residual_sources:
                residual_neighbors[mode].add(source)
    assert residual_neighbors["x"] | residual_neighbors["y"] == {"t"}

    # The coordinate quota pattern is injective except for one exceptional
    # pair, whose missing mode is restored by the excess cell at a.
    coordinate_maps = {
        "c": {"p1": "bc", "p2": "bc", "q": "x", "t": "y", "r": "bd", "s": "z"},
        "d": {"p1": "bd", "p2": "bd", "q": "y", "t": "x", "r": "z", "s": "bc"},
        "e": {"p1": "x", "p2": "y", "q": "a", "t": "z", "r": "bc", "s": "bd"},
    }
    for colour in ("c", "d"):
        mapping = coordinate_maps[colour]
        collisions = [
            source for source, mode in mapping.items() if mode == mapping["p1"]
        ]
        assert set(collisions) == {"p1", "p2"}
        assert "a" not in mapping.values()
    excess_plane = sp.Matrix([cells["a"]["p1"], cells["a"]["p2"]])
    assert excess_plane.rank() == 2
    for target in (sp.Matrix([[1, 0, 0]]), sp.Matrix([[0, 1, 0]])):
        assert sp.Matrix.vstack(excess_plane, target).rank() == 2
    assert len(set(coordinate_maps["e"].values())) == 6

    print("arbitrary permanent equality two-switch port-completion shore: PASS")
    print(
        "fixed construction/shore algebra only; no matching or support search was performed"
    )


if __name__ == "__main__":
    main()
