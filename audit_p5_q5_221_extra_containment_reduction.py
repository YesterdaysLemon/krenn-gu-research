#!/usr/bin/env python3
"""Independent cover-generation audit for the q5_221 extra frontier."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_EXTRA_CONTAINMENT_REDUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relabel_edge(edge, permutation):
    return frozenset(permutation[vertex] for vertex in edge)


def encode(edges):
    return tuple(sum(1 << vertex for vertex in edge) for edge in edges)


def canonical_marked_edges(edges):
    images = []
    for ordering in itertools.permutations(range(4)):
        permutation = dict(enumerate(ordering))
        image = tuple(relabel_edge(edge, permutation) for edge in edges)
        images.append(encode(image))
        images.append(encode((image[1], image[0], image[2])))
    return min(images)


def main() -> None:
    two_sets = tuple(
        frozenset(pair) for pair in itertools.combinations(range(4), 2)
    )
    minimal_orbits = {
        canonical_marked_edges(edges)
        for edges in itertools.product(two_sets, repeat=3)
    }
    assert len(minimal_orbits) == 9

    covers = set()
    raw_extensions = 0
    for encoded in minimal_orbits:
        edges = tuple(
            frozenset(
                vertex for vertex in range(4) if bits & (1 << vertex)
            )
            for bits in encoded
        )
        for colour in range(3):
            for vertex in set(range(4)) - edges[colour]:
                extension = list(edges)
                extension[colour] = extension[colour] | {vertex}
                covers.add(canonical_marked_edges(tuple(extension)))
                raw_extensions += 1

    assert len(covers) == 14
    assert all(
        sorted(bits.bit_count() for bits in cover) == [2, 2, 3]
        for cover in covers
    )
    degree_profiles = {}
    for cover in covers:
        profile = tuple(
            sorted(
                (
                    sum(bool(bits & (1 << mode)) for bits in cover)
                    for mode in range(4)
                ),
                reverse=True,
            )
        )
        degree_profiles[profile] = degree_profiles.get(profile, 0) + 1
    assert degree_profiles == {
        (3, 3, 1, 0): 2,
        (3, 2, 2, 0): 2,
        (3, 2, 1, 1): 5,
        (2, 2, 2, 1): 5,
    }
    distinguished_triple_covers = tuple(
        cover for cover in sorted(covers) if cover[2].bit_count() == 3
    )
    assert len(distinguished_triple_covers) == 6

    output = {
        "audited": True,
        "method": "independent extension of nine marked minimal edge orbits",
        "minimal_marked_orbits": len(minimal_orbits),
        "raw_orbit_representative_extensions": raw_extensions,
        "distinct_marked_cover_orbits": len(covers),
        "mode_degree_profile_histogram": {
            str(profile): count
            for profile, count in sorted(degree_profiles.items())
        },
        "ambient_row_spaces_enumerated": 0,
        "distinguished_row_size_three_cover_count": len(
            distinguished_triple_covers
        ),
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q5_221_extra_containment_audited.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
