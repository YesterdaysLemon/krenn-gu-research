"""Primary finite check of the P5 three-coordinate cycle dichotomy."""

from __future__ import annotations

import itertools
import json
from collections import Counter


MODES = tuple(range(5))
SOURCES = tuple(range(5))


def component_sizes(
    choices: tuple[tuple[int, int], ...],
) -> tuple[int, ...]:
    adjacency = {
        **{("mode", mode): [] for mode in MODES},
        **{("source", source): [] for source in SOURCES},
    }
    for mode, pair in enumerate(choices):
        for source in pair:
            adjacency[("mode", mode)].append(("source", source))
            adjacency[("source", source)].append(("mode", mode))

    unseen = set(adjacency)
    sizes = []
    while unseen:
        root = unseen.pop()
        stack = [root]
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbour in adjacency[vertex]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    stack.append(neighbour)
        sizes.append(size)
    return tuple(sorted(sizes))


def main() -> None:
    # Fifteen distinct source-colour requirements and at most three
    # coordinate cells per mode force equality in every count.
    required_source_colour_pairs = len(SOURCES) * 3
    maximum_coordinate_cells = len(MODES) * 3
    assert required_source_colour_pairs == maximum_coordinate_cells == 15

    shapes = Counter()
    examples = {}
    source_pairs = tuple(itertools.combinations(SOURCES, 2))
    for choices in itertools.product(source_pairs, repeat=len(MODES)):
        source_degrees = [0] * len(SOURCES)
        for pair in choices:
            for source in pair:
                source_degrees[source] += 1
        if source_degrees != [2] * len(SOURCES):
            continue

        shape = component_sizes(choices)
        assert shape in ((10,), (4, 6))
        shapes[shape] += 1
        examples.setdefault(shape, choices)

    assert sum(shapes.values()) == 2040
    assert shapes == Counter({(10,): 1440, (4, 6): 600})
    print(
        json.dumps(
            {
                "verified": True,
                "required_coordinate_cells": 15,
                "labelled_noncoordinate_graphs": sum(shapes.values()),
                "shape_counts": {
                    "C10": shapes[(10,)],
                    "C4_disjoint_C6": shapes[(4, 6)],
                },
                "examples": {
                    "C10": examples[(10,)],
                    "C4_disjoint_C6": examples[(4, 6)],
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
