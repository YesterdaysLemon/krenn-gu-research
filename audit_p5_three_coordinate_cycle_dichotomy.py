"""Independent matching-decomposition audit of the P5 cycle dichotomy."""

from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict


VERTICES = tuple(range(5))
PERMUTATIONS = tuple(itertools.permutations(VERTICES))


def main() -> None:
    decompositions = defaultdict(int)
    ordered_disjoint_pairs = 0
    for first in PERMUTATIONS:
        for second in PERMUTATIONS:
            if any(first[mode] == second[mode] for mode in VERTICES):
                continue
            ordered_disjoint_pairs += 1
            edge_set = frozenset(
                (mode, source)
                for mode in VERTICES
                for source in (first[mode], second[mode])
            )
            assert len(edge_set) == 10
            decompositions[edge_set] += 1

    assert ordered_disjoint_pairs == 5280
    assert len(decompositions) == 2040
    multiplicities = Counter(decompositions.values())
    assert multiplicities == Counter({2: 1440, 4: 600})
    assert 1440 * 2 + 600 * 4 == ordered_disjoint_pairs

    # A connected even cycle has two ordered alternating
    # decompositions.  Thus multiplicity two means one component
    # (C10), while multiplicity four means two components (C4 + C6).
    print(
        json.dumps(
            {
                "verified": True,
                "ordered_disjoint_matching_pairs": (
                    ordered_disjoint_pairs
                ),
                "distinct_labelled_unions": len(decompositions),
                "decomposition_multiplicities": {
                    str(key): value
                    for key, value in sorted(multiplicities.items())
                },
                "shape_counts": {
                    "C10": multiplicities[2],
                    "C4_disjoint_C6": multiplicities[4],
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
