"""Independently verify the degree-three second-singleton orbit split."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


Descriptor = tuple[int, int, int, int]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def allowed_edges() -> tuple[tuple[int, int], ...]:
    return tuple(
        edge
        for edge in itertools.combinations(range(8), 2)
        if edge[0] != 0 or edge[1] <= 3
    )


def candidates() -> dict[tuple[int, int, int], int]:
    neighbours = {vertex: [] for vertex in range(8)}
    for first, second in allowed_edges():
        neighbours[first].append(second)
        neighbours[second].append(first)
    result: dict[tuple[int, int, int], int] = {}
    next_variable = 750
    for vertex in range(8):
        for colour in range(3):
            for neighbour in neighbours[vertex]:
                result[vertex, colour, neighbour] = next_variable
                next_variable += 3
    return result


def image(
    descriptor: Descriptor,
    colours: tuple[int, ...],
    free_vertices: tuple[int, ...],
) -> Descriptor:
    first, second, first_colour, second_colour = descriptor
    vertex_image = (
        0,
        colours[0] + 1,
        colours[1] + 1,
        colours[2] + 1,
        *free_vertices,
    )
    mapped = (
        vertex_image[first],
        vertex_image[second],
        colours[first_colour],
        colours[second_colour],
    )
    if mapped[0] < mapped[1]:
        return mapped
    return (mapped[1], mapped[0], mapped[3], mapped[2])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(
            "tmp/degree3_e19_second_reciprocal_orbits.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/degree3_e19_second_reciprocal_orbits_audit.json"
        ),
    )
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))

    universe = {
        (first, second, first_colour, second_colour)
        for first, second in itertools.combinations(range(1, 8), 2)
        for first_colour in range(3)
        for second_colour in range(3)
    }
    group = tuple(
        itertools.product(
            itertools.permutations(range(3)),
            itertools.permutations(range(4, 8)),
        )
    )
    candidate_variables = candidates()
    covered: set[Descriptor] = set()
    expected_rows: list[dict[str, object]] = []
    for orbit_index, row in enumerate(manifest["orbits"]):
        representative = tuple(map(int, row["representative"]))
        if len(representative) != 4:
            raise AssertionError("malformed representative")
        orbit = {
            image(representative, colours, free_vertices)
            for colours, free_vertices in group
        }
        if covered & orbit:
            raise AssertionError("reported orbits overlap")
        covered.update(orbit)
        first, second, first_colour, second_colour = representative
        expected = {
            "orbit_index": orbit_index,
            "representative": list(representative),
            "orbit_size": len(orbit),
            "forward_candidate": candidate_variables[
                first, first_colour, second
            ],
            "reverse_candidate": candidate_variables[
                second, second_colour, first
            ],
        }
        if row != expected:
            raise AssertionError(
                f"orbit row {orbit_index} changed: {row} != {expected}"
            )
        expected_rows.append(expected)

    if covered != universe:
        raise AssertionError("orbit split is not exhaustive")
    if len(expected_rows) != 13:
        raise AssertionError("expected exactly 13 residual orbits")
    if sum(row["orbit_size"] for row in expected_rows) != 189:
        raise AssertionError("orbit sizes do not cover 21*9 descriptors")
    if (
        manifest["forced_reciprocals"],
        manifest["star_reciprocals"],
        manifest["additional_reciprocals"],
    ) != (5, 3, 2):
        raise AssertionError("reciprocal count metadata changed")

    payload = {
        "verified": True,
        "manifest": str(args.manifest),
        "manifest_sha256": sha256(args.manifest),
        "descriptor_count": len(universe),
        "group_order": len(group),
        "orbit_count": len(expected_rows),
        "orbit_sizes_sum": sum(
            row["orbit_size"] for row in expected_rows
        ),
        "counting_reason": (
            "24 directed killer incidences on 19 selected blocks force "
            "at least 5 reciprocal edges; the normalized singleton star "
            "uses 3, so at least 2 more lie among vertices 1..7"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
