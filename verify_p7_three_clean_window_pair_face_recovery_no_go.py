"""Verify the three-clean-window pair-face recovery no-go theorem."""

from itertools import combinations, permutations
from math import prod

import sympy as sp

PORTS = tuple(range(6))
TARGET_WINDOW = frozenset(range(4))
EDGES = tuple(combinations(PORTS, 2))
TARGET_COLUMNS = tuple(
    index for index, edge in enumerate(EDGES) if set(edge) <= TARGET_WINDOW
)
NUISANCE_COLUMNS = tuple(
    index for index in range(len(EDGES)) if index not in TARGET_COLUMNS
)

REPRESENTATIVES = (
    ("1256", "3456"),
    ("1256", "1456"),
    ("3456", "3456"),
    ("1345", "2356"),
    ("1245", "2456"),
    ("1236", "2345"),
    ("1235", "1345"),
    ("1245", "1246"),
    ("2346", "2346"),
)

EXPECTED_RANKS = (
    (11, 7),
    (11, 6),
    (8, 4),
    (11, 7),
    (10, 6),
    (10, 6),
    (9, 4),
    (10, 6),
    (7, 3),
)

KERNEL_WITNESSES = (
    (0, 1, -1, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    (1, -2, 1, 0, -1, 1, -2, -1, 0, 1, 0, 0, -1, 0, 1),
    (0, 1, -1, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    (-1, 1, 0, -1, 0, 0, 1, 0, 0, -1, 0, 0, 1, 0, 0),
    (-1, 0, 1, 0, 0, 1, 0, 1, -1, -1, 0, 0, -1, 1, 0),
    (1, -1, 0, 0, 0, 0, -1, 1, -1, 1, -1, 1, 0, 0, 0),
    (-1, 2, -1, -1, 0, -1, 2, 2, 0, -1, -1, 0, 2, 0, 0),
    (0, -1, 1, -1, -1, 1, -1, 1, 1, 0, 0, 0, 0, 0, 0),
    (-1, 1, 0, 0, 0, 0, 1, 0, -1, -1, 0, 1, 0, 0, 0),
)


def window(label: str) -> frozenset[int]:
    return frozenset(int(value) - 1 for value in label)


def observation_matrix(windows: tuple[frozenset[int], ...]) -> sp.Matrix:
    return sp.Matrix(
        [
            [int(vertex in edge and set(edge) <= current) for edge in EDGES]
            for current in windows
            for vertex in sorted(current)
        ]
    )


def canonical_pair(pair):
    return tuple(sorted(pair, key=lambda value: tuple(sorted(value))))


def orbit(pair):
    result = set()
    for inside in permutations(range(4)):
        for outside in ((4, 5), (5, 4)):
            relabelling = dict(zip(PORTS, inside + outside, strict=True))
            image = tuple(
                frozenset(relabelling[value] for value in current)
                for current in pair
            )
            result.add(canonical_pair(image))
            result.add(canonical_pair((image[1], image[0])))
    return result


def main() -> None:
    representative_pairs = tuple(
        canonical_pair((window(left), window(right)))
        for left, right in REPRESENTATIVES
    )

    covered = set()
    for pair in representative_pairs:
        covered.update(orbit(pair))
    non_target_windows = tuple(
        frozenset(values)
        for values in combinations(PORTS, 4)
        if frozenset(values) != TARGET_WINDOW
    )
    all_pairs = {
        canonical_pair((left, right))
        for left in non_target_windows
        for right in non_target_windows
    }
    assert covered == all_pairs
    assert len(representative_pairs) == 9

    for pair, expected, witness_values in zip(
        representative_pairs,
        EXPECTED_RANKS,
        KERNEL_WITNESSES,
        strict=True,
    ):
        matrix = observation_matrix((TARGET_WINDOW,) + pair)
        witness = sp.Matrix(witness_values)
        assert matrix * witness == sp.zeros(matrix.rows, 1)
        assert any(witness[index] != 0 for index in TARGET_COLUMNS)
        total_rank = matrix.rank()
        nuisance_rank = matrix[:, NUISANCE_COLUMNS].rank()
        assert (total_rank, nuisance_rank) == expected
        assert total_rank - nuisance_rank <= 5

    # Repeated copies of the target add nothing; one other window alone also
    # contributes no target defect direction.
    all_windows = tuple(frozenset(values) for values in combinations(PORTS, 4))
    for other in all_windows:
        matrix = observation_matrix((TARGET_WINDOW, TARGET_WINDOW, other))
        assert matrix.rank() - matrix[:, NUISANCE_COLUMNS].rank() == 4

    sharp_matrix = observation_matrix(
        (TARGET_WINDOW, window("1256"), window("1456"))
    )
    total_rows = tuple(range(11))
    total_columns = tuple(range(10)) + (12,)
    nuisance_rows = (4, 5, 6, 7, 9, 10)
    nuisance_local_columns = (0, 1, 2, 3, 6, 8)
    assert sharp_matrix.extract(total_rows, total_columns).det() == 4
    assert (
        sharp_matrix[:, NUISANCE_COLUMNS]
        .extract(nuisance_rows, nuisance_local_columns)
        .det()
        == -2
    )
    assert prod((4, -2)) != 0

    print("nine selector-matroid isomorphism types: COMPLETE")
    print("each type has an explicit target-visible kernel weighting")
    print("three-window target recovery <=5: VERIFIED")
    print("sharp type has ranks 11 and 6, determinants 4 and -2")
    print("graph_search=0 support_search=0 colour_word_search=0")


if __name__ == "__main__":
    main()
