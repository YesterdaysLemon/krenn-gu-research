"""Enumerate the residual-symmetry cases for a second singleton edge.

At a normalized degree-three vertex, edges 01, 02, and 03 are the
monochromatic singleton star of colours 0, 1, and 2.  For an exact
19-block n=8 support, the reciprocal-killer count forces at least five
reciprocal edges.  The star supplies three, so at least one additional
reciprocal singleton lies among vertices 1..7.

The stabilizer of the normalized star is S3 acting diagonally on
vertices 1,2,3 and colours 0,1,2, times S4 on vertices 4,5,6,7.  This
script enumerates the orbits of one additional reciprocal edge,
including its selected killer colour at each endpoint.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from augment_reciprocal_cardinality import candidate_map


Descriptor = tuple[int, int, int, int]


def transform(
    descriptor: Descriptor,
    colour_permutation: tuple[int, ...],
    free_permutation: tuple[int, ...],
) -> Descriptor:
    first, second, first_colour, second_colour = descriptor
    vertex_map = {
        1: colour_permutation[0] + 1,
        2: colour_permutation[1] + 1,
        3: colour_permutation[2] + 1,
        4: free_permutation[0],
        5: free_permutation[1],
        6: free_permutation[2],
        7: free_permutation[3],
    }
    mapped_first = vertex_map[first]
    mapped_second = vertex_map[second]
    mapped_first_colour = colour_permutation[first_colour]
    mapped_second_colour = colour_permutation[second_colour]
    if mapped_first < mapped_second:
        return (
            mapped_first,
            mapped_second,
            mapped_first_colour,
            mapped_second_colour,
        )
    return (
        mapped_second,
        mapped_first,
        mapped_second_colour,
        mapped_first_colour,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/degree3_e19_second_reciprocal_orbits.json"
        ),
    )
    args = parser.parse_args()

    descriptors = {
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
    candidates = candidate_map(center_degree=3, candidate_base=750)
    unseen = set(descriptors)
    rows: list[dict[str, object]] = []
    while unseen:
        representative = min(unseen)
        orbit = {
            transform(representative, colours, free_vertices)
            for colours, free_vertices in group
        }
        if not orbit <= descriptors:
            raise AssertionError("residual action left the descriptor set")
        unseen -= orbit
        first, second, first_colour, second_colour = representative
        rows.append(
            {
                "orbit_index": len(rows),
                "representative": list(representative),
                "orbit_size": len(orbit),
                "forward_candidate": candidates[
                    first, first_colour, second
                ],
                "reverse_candidate": candidates[
                    second, second_colour, first
                ],
            }
        )

    payload = {
        "scope": (
            "one additional reciprocal singleton after the normalized "
            "n=8 degree-three singleton star"
        ),
        "target_edges": 19,
        "forced_reciprocals": 5,
        "star_reciprocals": 3,
        "additional_reciprocals": 2,
        "descriptor_count": len(descriptors),
        "group_order": len(group),
        "orbit_count": len(rows),
        "candidate_base": 750,
        "orbits": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({**payload, "output_sha256": sha256(args.output)}, indent=2))


if __name__ == "__main__":
    main()
