#!/usr/bin/env python3
"""Independent marked-multigraph audit of q5_221 incidence types."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_HYPERPLANE_INCIDENCE_REDUCTION.md"
VERTEX_PERMUTATIONS = tuple(itertools.permutations(range(4)))
EDGES = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_marked_multigraph(
    majority_edges: tuple[tuple[int, int], tuple[int, int]],
    singleton_edge: tuple[int, int],
) -> tuple[tuple[tuple[int, int], ...], tuple[int, int]]:
    images = []
    for permutation in VERTEX_PERMUTATIONS:
        majority_image = tuple(
            sorted(
                tuple(sorted((permutation[first], permutation[second])))
                for first, second in majority_edges
            )
        )
        singleton_image = tuple(
            sorted(
                (
                    permutation[singleton_edge[0]],
                    permutation[singleton_edge[1]],
                )
            )
        )
        images.append(
            (majority_image, singleton_image)
        )
    return min(images)


def main() -> None:
    orbit_counts = Counter()
    for majority_indices in itertools.combinations_with_replacement(
        range(len(EDGES)),
        2,
    ):
        majority_edges = tuple(
            EDGES[index] for index in majority_indices
        )
        for singleton_edge in EDGES:
            orbit_counts[
                canonical_marked_multigraph(
                    majority_edges,
                    singleton_edge,
                )
            ] += 1
    assert sum(orbit_counts.values()) == 126
    assert len(orbit_counts) == 9

    degree_profiles = []
    multiplicity_profiles = []
    marked_multiplicities = []
    marked_endpoint_degree_profiles = []
    underlying_orbits = set()
    for majority_edges, singleton_edge in orbit_counts:
        representative = majority_edges + (singleton_edge,)
        underlying_orbits.add(
            min(
                tuple(
                    sorted(
                        tuple(
                            sorted(
                                (
                                    permutation[first],
                                    permutation[second],
                                )
                            )
                        )
                        for first, second in representative
                    )
                )
                for permutation in VERTEX_PERMUTATIONS
            )
        )
        degrees = [0] * 4
        for first, second in representative:
            degrees[first] += 1
            degrees[second] += 1
        degree_profiles.append(tuple(sorted(degrees, reverse=True)))
        multiplicity_profiles.append(
            tuple(
                sorted(
                    Counter(representative).values(),
                    reverse=True,
                )
            )
        )
        marked_multiplicities.append(
            Counter(representative)[singleton_edge]
        )
        marked_endpoint_degree_profiles.append(
            tuple(
                sorted(
                    (
                        degrees[singleton_edge[0]],
                        degrees[singleton_edge[1]],
                    ),
                    reverse=True,
                )
            )
        )
    profile_pairs = Counter(
        zip(
            degree_profiles,
            multiplicity_profiles,
            marked_multiplicities,
            marked_endpoint_degree_profiles,
            strict=True,
        )
    )
    assert len(underlying_orbits) == 6
    assert len(profile_pairs) == 9

    output = {
        "audited": True,
        "marked_edge_multisets_checked": sum(orbit_counts.values()),
        "marked_incidence_orbits": len(orbit_counts),
        "underlying_uncoloured_incidence_orbits": len(
            underlying_orbits
        ),
        "canonical_marked_multigraphs": [
            {
                "majority_edges": [
                    list(edge) for edge in majority_edges
                ],
                "singleton_edge": list(singleton_edge),
            }
            for majority_edges, singleton_edge in sorted(orbit_counts)
        ],
        "decorated_profiles": [
            {
                "degree_profile": list(degrees),
                "edge_multiplicity_profile": list(multiplicities),
                "singleton_edge_multiplicity": marked_multiplicity,
                "singleton_endpoint_degrees": list(
                    marked_endpoint_degrees
                ),
                "orbits": count,
            }
            for (
                degrees,
                multiplicities,
                marked_multiplicity,
                marked_endpoint_degrees,
            ), count in sorted(
                profile_pairs.items()
            )
        ],
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "independent incidence audit",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_hyperplane_incidence_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
