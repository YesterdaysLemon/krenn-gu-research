#!/usr/bin/env python3
"""Independent combinatorial audit of the all-full P5 orbit coverage."""

from __future__ import annotations

import itertools
import json
from collections import Counter


SUPPORTS = {
    "c10_orbit_126": (
        (7, 7, 4, 2, 1),
        (1, 7, 7, 4, 2),
        (2, 1, 7, 7, 4),
        (4, 2, 1, 7, 7),
        (7, 4, 2, 1, 7),
    ),
    "c10_orbit_122": (
        (7, 7, 4, 2, 1),
        (4, 7, 7, 1, 2),
        (2, 1, 7, 7, 4),
        (1, 4, 2, 7, 7),
        (7, 2, 1, 4, 7),
    ),
    "c4c6_orbit_56": (
        (7, 7, 4, 2, 1),
        (7, 7, 2, 1, 4),
        (4, 1, 7, 7, 2),
        (2, 4, 1, 7, 7),
        (1, 2, 7, 4, 7),
    ),
}

VERTEX_PERMUTATIONS = tuple(itertools.permutations(range(5)))
COLOUR_PERMUTATIONS = tuple(itertools.permutations(range(3)))


def full_graph(
    supports: tuple[tuple[int, ...], ...],
) -> frozenset[tuple[int, int]]:
    return frozenset(
        (mode, source)
        for mode in range(5)
        for source in range(5)
        if supports[mode][source] == 7
    )


def component_sizes(
    edges: frozenset[tuple[int, int]],
) -> tuple[int, ...]:
    adjacency = {
        ("m", mode): set() for mode in range(5)
    } | {
        ("s", source): set() for source in range(5)
    }
    for mode, source in edges:
        adjacency[("m", mode)].add(("s", source))
        adjacency[("s", source)].add(("m", mode))
    unseen = set(adjacency)
    sizes = []
    while unseen:
        root = min(unseen)
        stack = [root]
        component = set()
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend(adjacency[vertex] - component)
        unseen.difference_update(component)
        sizes.append(len(component))
    return tuple(sorted(sizes))


def skeleton(
    supports: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    output = []
    for row in supports:
        for mask in row:
            if mask == 7:
                output.append(-1)
            elif mask in (1, 2, 4):
                output.append(mask.bit_length() - 1)
            else:
                raise AssertionError(f"unexpected support mask {mask}")
    return tuple(output)


def automorphisms(
    edges: frozenset[tuple[int, int]],
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    output = []
    for mode_permutation in VERTEX_PERMUTATIONS:
        for source_permutation in VERTEX_PERMUTATIONS:
            image = frozenset(
                (
                    mode_permutation[mode],
                    source_permutation[source],
                )
                for mode, source in edges
            )
            if image == edges:
                output.append((mode_permutation, source_permutation))
    return tuple(output)


def transform(
    pattern: tuple[int, ...],
    mode_permutation: tuple[int, ...],
    source_permutation: tuple[int, ...],
    colour_permutation: tuple[int, ...],
) -> tuple[int, ...]:
    image = [-1] * 25
    for mode in range(5):
        for source in range(5):
            value = pattern[5 * mode + source]
            image[
                5 * mode_permutation[mode]
                + source_permutation[source]
            ] = -1 if value < 0 else colour_permutation[value]
    return tuple(image)


def enumerate_colourings(
    edges: frozenset[tuple[int, int]],
) -> tuple[tuple[int, ...], ...]:
    patterns = []
    for row_colours in itertools.product(
        itertools.permutations(range(3)), repeat=5
    ):
        pattern = [-1] * 25
        for mode in range(5):
            singleton_sources = [
                source
                for source in range(5)
                if (mode, source) not in edges
            ]
            if len(singleton_sources) != 3:
                raise AssertionError("full graph is not two-regular")
            for source, colour in zip(
                singleton_sources, row_colours[mode]
            ):
                pattern[5 * mode + source] = colour
        if all(
            sorted(
                pattern[5 * mode + source]
                for mode in range(5)
                if (mode, source) not in edges
            )
            == [0, 1, 2]
            for source in range(5)
        ):
            patterns.append(tuple(pattern))
    return tuple(patterns)


def orbit_partition(
    patterns: tuple[tuple[int, ...], ...],
    group: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
) -> tuple[tuple[tuple[int, ...], ...], ...]:
    universe = set(patterns)
    unseen = set(patterns)
    orbits = []
    while unseen:
        representative = min(unseen)
        orbit = {
            transform(
                representative,
                mode_permutation,
                source_permutation,
                colour_permutation,
            )
            for mode_permutation, source_permutation in group
            for colour_permutation in COLOUR_PERMUTATIONS
        } & universe
        unseen.difference_update(orbit)
        orbits.append(tuple(sorted(orbit)))
    return tuple(sorted(orbits, key=lambda orbit: orbit[0]))


def main() -> None:
    c10_edges = full_graph(SUPPORTS["c10_orbit_126"])
    if c10_edges != full_graph(SUPPORTS["c10_orbit_122"]):
        raise AssertionError("C10 representatives use different full graphs")
    c4c6_edges = full_graph(SUPPORTS["c4c6_orbit_56"])
    if component_sizes(c10_edges) != (10,):
        raise AssertionError("first full graph is not C10")
    if component_sizes(c4c6_edges) != (4, 6):
        raise AssertionError("second full graph is not C4+C6")

    results = {}
    for shape, edges, expected in (
        ("C10", c10_edges, (10, 36, (6, 30))),
        ("C4+C6", c4c6_edges, (24, 24, (24,))),
    ):
        group = automorphisms(edges)
        patterns = enumerate_colourings(edges)
        orbits = orbit_partition(patterns, group)
        observed = (
            len(group),
            len(patterns),
            tuple(sorted(len(orbit) for orbit in orbits)),
        )
        if observed != expected:
            raise AssertionError(
                f"{shape} census differs: {observed} != {expected}"
            )
        names = (
            ("c10_orbit_126", "c10_orbit_122")
            if shape == "C10"
            else ("c4c6_orbit_56",)
        )
        canonical = {
            min(
                transform(
                    skeleton(SUPPORTS[name]),
                    mode_permutation,
                    source_permutation,
                    colour_permutation,
                )
                for mode_permutation, source_permutation in group
                for colour_permutation in COLOUR_PERMUTATIONS
            )
            for name in names
        }
        if canonical != {orbit[0] for orbit in orbits}:
            raise AssertionError(f"{shape} representatives miss an orbit")
        results[shape] = {
            "full_graph_automorphisms": len(group),
            "labelled_proper_colourings": len(patterns),
            "orbits": len(orbits),
            "orbit_sizes": sorted(len(orbit) for orbit in orbits),
        }

    multiplicities = Counter(
        tuple(sorted(colouring.count(colour) for colour in range(3)))
        for colouring in itertools.product(range(3), repeat=5)
        if len(set(colouring)) == 3
    )
    if multiplicities != Counter({(1, 2, 2): 90, (1, 1, 3): 60}):
        raise AssertionError("tricolour coefficient census differs")

    print(
        json.dumps(
            {
                "verified": True,
                "scope": (
                    "proper-colour all-full exact-three-coordinate support "
                    "orbit census"
                ),
                "shapes": results,
                "tricolour_coefficients": {
                    "total": 150,
                    "multiplicity_3_1_1": 60,
                    "multiplicity_2_2_1": 90,
                },
                "coefficient_solver_replayed_here": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
