"""Coarsen exact-three P5 survivor supports into structural motifs."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path


MODES = tuple(range(5))
SOURCES = tuple(range(5))
COLOURS = tuple(range(3))
SINGLETONS = (1, 2, 4)
PARTIALS = (3, 5, 6)
SHAPES = {
    "c10": ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4)),
    "c4c6": ((0, 1), (0, 1), (2, 3), (3, 4), (2, 4)),
}


def edges(shape: str) -> tuple[tuple[int, int], ...]:
    return tuple(
        (mode, source)
        for mode, sources in enumerate(SHAPES[shape])
        for source in sources
    )


def shape_automorphisms(
    shape: str,
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    required = set(edges(shape))
    output = []
    for mode_permutation in itertools.permutations(MODES):
        for source_permutation in itertools.permutations(SOURCES):
            image = {
                (
                    mode_permutation[mode],
                    source_permutation[source],
                )
                for mode, source in required
            }
            if image == required:
                output.append((mode_permutation, source_permutation))
    expected = {"c10": 10, "c4c6": 24}[shape]
    if len(output) != expected:
        raise AssertionError("shape automorphism count changed")
    return tuple(output)


def mask_colour(mask: int) -> int:
    if mask not in SINGLETONS:
        raise ValueError("mask is not a singleton")
    return mask.bit_length() - 1


def missing_colour(mask: int) -> int:
    if mask not in PARTIALS:
        raise ValueError("mask is not partial")
    return next(
        colour for colour in COLOURS if not mask & (1 << colour)
    )


def cycle_components(
    shape: str,
) -> tuple[tuple[tuple[int, int], ...], ...]:
    remaining = set(edges(shape))
    components = []
    while remaining:
        start = min(remaining)
        ordered = [start]
        current_edge = start
        current_node = ("s", start[1])
        while True:
            incident = [
                edge
                for edge in edges(shape)
                if (
                    current_node == ("m", edge[0])
                    or current_node == ("s", edge[1])
                )
            ]
            if len(incident) != 2:
                raise AssertionError("noncoordinate graph is not 2-regular")
            next_edge = next(
                edge for edge in incident if edge != current_edge
            )
            if next_edge == start:
                break
            ordered.append(next_edge)
            if current_node == ("m", next_edge[0]):
                current_node = ("s", next_edge[1])
            else:
                current_node = ("m", next_edge[0])
            current_edge = next_edge
        remaining.difference_update(ordered)
        components.append(tuple(ordered))
    result = tuple(sorted(components, key=lambda component: len(component)))
    expected = {"c10": (10,), "c4c6": (4, 6)}[shape]
    if tuple(map(len, result)) != expected:
        raise AssertionError("cycle component lengths changed")
    return result


def dihedral_canonical(sequence: tuple[int, ...]) -> tuple[int, ...]:
    rotations = []
    for oriented in (sequence, tuple(reversed(sequence))):
        rotations.extend(
            oriented[offset:] + oriented[:offset]
            for offset in range(len(oriented))
        )
    return min(rotations)


def partial_geometry(
    supports: tuple[tuple[int, ...], ...],
    components: tuple[tuple[tuple[int, int], ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        dihedral_canonical(
            tuple(
                int(supports[mode][source] in PARTIALS)
                for mode, source in component
            )
        )
        for component in components
    )


def coloured_partial_geometry(
    supports: tuple[tuple[int, ...], ...],
    components: tuple[tuple[tuple[int, int], ...], ...],
) -> tuple[tuple[int, ...], ...]:
    candidates = []
    for permutation in itertools.permutations(COLOURS):
        component_sequences = []
        for component in components:
            sequence = []
            for mode, source in component:
                mask = supports[mode][source]
                sequence.append(
                    permutation[missing_colour(mask)]
                    if mask in PARTIALS
                    else 3
                )
            component_sequences.append(
                dihedral_canonical(tuple(sequence))
            )
        candidates.append(tuple(component_sequences))
    return min(candidates)


def colour_mask(mask: int, permutation: tuple[int, ...]) -> int:
    return sum(
        ((mask >> colour) & 1) << permutation[colour]
        for colour in COLOURS
    )


def coordinate_backbone(
    shape: str,
    supports: tuple[tuple[int, ...], ...],
    automorphisms: tuple[
        tuple[tuple[int, ...], tuple[int, ...]], ...
    ],
) -> tuple[int, ...]:
    candidates = []
    for mode_permutation, source_permutation in automorphisms:
        for colour_permutation in itertools.permutations(COLOURS):
            image = [7] * 25
            for mode in MODES:
                for source in SOURCES:
                    mask = supports[mode][source]
                    if mask not in SINGLETONS:
                        continue
                    new_position = (
                        5 * mode_permutation[mode]
                        + source_permutation[source]
                    )
                    image[new_position] = colour_mask(
                        mask, colour_permutation
                    )
            candidates.append(tuple(image))
    return min(candidates)


def validate_support(
    shape: str,
    supports: tuple[tuple[int, ...], ...],
) -> None:
    observed_noncoordinate = {
        (mode, source)
        for mode in MODES
        for source in SOURCES
        if supports[mode][source] not in SINGLETONS
    }
    if observed_noncoordinate != set(edges(shape)):
        raise AssertionError("support has the wrong noncoordinate shape")
    if sum(
        mask in PARTIALS for row in supports for mask in row
    ) != 3:
        raise AssertionError("support is not exact-three-partial")
    for source in SOURCES:
        singletons = [
            supports[mode][source]
            for mode in MODES
            if supports[mode][source] in SINGLETONS
        ]
        if sorted(singletons) != list(SINGLETONS):
            raise AssertionError("source coordinate colours changed")


def encode_key(value: tuple) -> str:
    return json.dumps(value, separators=(",", ":"))


def analyze(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    shape = payload["shape"]
    components = cycle_components(shape)
    automorphisms = shape_automorphisms(shape)
    geometry_histogram = Counter()
    coloured_geometry_histogram = Counter()
    backbone_histogram = Counter()
    joint_histogram = Counter()
    for case in payload["cases"]:
        supports = tuple(tuple(row) for row in case["supports"])
        validate_support(shape, supports)
        geometry = partial_geometry(supports, components)
        coloured_geometry = coloured_partial_geometry(
            supports, components
        )
        backbone = coordinate_backbone(
            shape, supports, automorphisms
        )
        geometry_histogram[geometry] += 1
        coloured_geometry_histogram[coloured_geometry] += 1
        backbone_histogram[backbone] += 1
        joint_histogram[(backbone, coloured_geometry)] += 1

    backbone_ids = {
        backbone: index
        for index, backbone in enumerate(sorted(backbone_histogram))
    }
    return {
        "shape": shape,
        "support_orbits": len(payload["cases"]),
        "cycle_lengths": [len(component) for component in components],
        "partial_geometry_classes": len(geometry_histogram),
        "partial_geometry_histogram": {
            encode_key(key): count
            for key, count in sorted(geometry_histogram.items())
        },
        "colour_quotiented_partial_geometry_classes": len(
            coloured_geometry_histogram
        ),
        "colour_quotiented_partial_geometry_histogram": {
            encode_key(key): count
            for key, count in sorted(
                coloured_geometry_histogram.items()
            )
        },
        "coordinate_backbone_classes": len(backbone_histogram),
        "coordinate_backbone_histogram": {
            str(backbone_ids[key]): count
            for key, count in sorted(
                backbone_histogram.items(),
                key=lambda item: backbone_ids[item[0]],
            )
        },
        "backbone_x_coloured_geometry_classes": len(joint_histogram),
        "largest_joint_classes": [
            {
                "backbone": backbone_ids[key[0]],
                "coloured_geometry": encode_key(key[1]),
                "support_orbits": count,
            }
            for key, count in joint_histogram.most_common(20)
        ],
        "status": "EXPLORATORY_STRUCTURAL_COARSENING",
        "global_conjecture_resolved": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("catalogues", type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    catalogues = [analyze(path) for path in args.catalogues]
    result = {
        "catalogues": catalogues,
        "totals": {
            "support_orbits": sum(
                item["support_orbits"] for item in catalogues
            ),
            "partial_geometry_classes": sum(
                item["partial_geometry_classes"]
                for item in catalogues
            ),
            "colour_quotiented_partial_geometry_classes": sum(
                item["colour_quotiented_partial_geometry_classes"]
                for item in catalogues
            ),
            "coordinate_backbone_classes": sum(
                item["coordinate_backbone_classes"]
                for item in catalogues
            ),
            "backbone_x_coloured_geometry_classes": sum(
                item["backbone_x_coloured_geometry_classes"]
                for item in catalogues
            ),
        },
        "status": "EXPLORATORY_STRUCTURAL_COARSENING",
        "global_conjecture_resolved": False,
    }
    if args.output is not None:
        args.output.write_text(
            json.dumps(result, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
