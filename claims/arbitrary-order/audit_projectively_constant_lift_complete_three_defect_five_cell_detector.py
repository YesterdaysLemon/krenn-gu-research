"""Independent no-import audit for the complete three-defect detector."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product

COORDS = (0, 1, 2)
MODES = tuple(range(5))
WORDS4 = tuple(product(COORDS, repeat=4))
ZERO = (0, 0, 0)
E0 = (1, 0, 0)
E1 = (0, 1, 0)
RATIO_VALUES = (-2, -1, 1, 2)


def recursive_permanent(rows: tuple[tuple[int, ...], ...]) -> int:
    cache: dict[tuple[int, int], int] = {}

    def visit(mode: int, used: int) -> int:
        key = (mode, used)
        if key in cache:
            return cache[key]
        if mode == len(rows):
            return 1
        total = 0
        for source, value in enumerate(rows[mode]):
            if used & (1 << source):
                continue
            if value:
                total += value * visit(mode + 1, used | (1 << source))
        cache[key] = total
        return total

    return visit(0, 0)


def collision_matrix(
    types: tuple[str, ...],
    deleted: int,
    ratios: tuple[int, ...],
) -> list[list[int]]:
    """Build collision columns via a recursive four-row permanent."""
    a_rows: list[tuple[int, int, int]] = []
    b_rows: list[tuple[int, int, int]] = []
    for mode, mode_type in enumerate(types):
        if mode_type == "R":
            a_rows.append((ratios[mode], 0, 0))
            b_rows.append(E0)
        elif mode_type == "B":
            a_rows.append(ZERO)
            b_rows.append(E0)
        elif mode_type == "T":
            a_rows.append(E0)
            b_rows.append(E1)
        else:
            raise ValueError(mode_type)

    retained = tuple(mode for mode in MODES if mode != deleted)
    matrix = [[0 for _ in range(15)] for _ in range(81)]
    for h_mode in retained:
        for h_coord in COORDS:
            column = 3 * h_mode + h_coord
            for word_index, word in enumerate(WORDS4):
                rows = []
                for local_index, mode in enumerate(retained):
                    h_value = int(mode == h_mode and word[local_index] == h_coord)
                    a_value = a_rows[mode][word[local_index]]
                    b_value = b_rows[mode][word[local_index]]
                    rows.append((h_value, a_value, a_value, b_value))
                matrix[word_index][column] = recursive_permanent(tuple(rows))
    return matrix


def stack(*matrices: list[list[int]]) -> list[list[int]]:
    return [row[:] for matrix in matrices for row in matrix]


def rational_rref(
    integer_matrix: list[list[int]],
) -> tuple[list[list[Fraction]], tuple[int, ...]]:
    rows = [list(map(Fraction, row)) for row in integer_matrix if any(row)]
    if not rows:
        return [], ()
    row_count = len(rows)
    column_count = len(rows[0])
    pivot_row = 0
    pivots: list[int] = []
    for column in range(column_count):
        selected = next(
            (row for row in range(pivot_row, row_count) if rows[row][column]),
            None,
        )
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        pivot = rows[pivot_row][column]
        rows[pivot_row] = [entry / pivot for entry in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                left - scale * right
                for left, right in zip(rows[row], rows[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return rows[:pivot_row], tuple(pivots)


def nullspace(integer_matrix: list[list[int]]) -> list[list[Fraction]]:
    rref, pivots = rational_rref(integer_matrix)
    column_count = len(integer_matrix[0])
    free = [column for column in range(column_count) if column not in pivots]
    vectors = []
    for free_column in free:
        vector = [Fraction(0) for _ in range(column_count)]
        vector[free_column] = Fraction(1)
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -rref[row][free_column]
        vectors.append(vector)
    return vectors


def assert_coordinates_zero(
    vectors: list[list[Fraction]],
    coordinates: tuple[tuple[int, int], ...],
) -> None:
    assert all(
        vector[3 * mode + coord] == 0
        for vector in vectors
        for mode, coord in coordinates
    )


def audit_zero_b_profiles() -> int:
    profiles = 0
    for axes in product(COORDS, repeat=4):
        counts = Counter(axes)
        if len(counts) != 3:
            continue
        profiles += 1
        singleton_sources = [
            axes.index(colour) for colour, multiplicity in counts.items() if multiplicity == 1
        ]
        assert sorted(counts.values()) == [1, 1, 2]
        assert len(singleton_sources) == 2
        assert singleton_sources[0] != singleton_sources[1]
    assert profiles == 36
    return profiles


def audit_rrr() -> tuple[int, int, int]:
    types = ("R", "R", "R", "T", "T")
    ratio_charts = 0
    pair_checks = 0
    triple_checks = 0
    for first, second, third in product(RATIO_VALUES, repeat=3):
        ratios = (first, second, third, 1, 1)
        matrices = [collision_matrix(types, deleted, ratios) for deleted in range(3)]
        ratio_charts += 1

        for deleted_left, deleted_right in ((0, 1), (0, 2), (1, 2)):
            vectors = nullspace(stack(matrices[deleted_left], matrices[deleted_right]))
            expected = int(ratios[deleted_left] == ratios[deleted_right]) * 2
            assert len(vectors) == expected
            if vectors:
                assert_coordinates_zero(
                    vectors,
                    (
                        (0, 1),
                        (0, 2),
                        (1, 1),
                        (1, 2),
                        (2, 1),
                        (2, 2),
                        (3, 2),
                        (4, 2),
                    ),
                )
            pair_checks += 1

        triple = nullspace(stack(*matrices))
        expected_triple = int(first == second == third)
        assert len(triple) == expected_triple
        if triple:
            assert_coordinates_zero(
                triple,
                tuple((mode, coord) for mode in range(3) for coord in COORDS),
            )
        triple_checks += 1
    assert ratio_charts == 64
    assert pair_checks == 192
    assert triple_checks == 64
    return ratio_charts, pair_checks, triple_checks


def audit_rrb() -> tuple[int, int]:
    types = ("R", "R", "B", "T", "T")
    charts = 0
    intersections = 0
    for first, second in product(RATIO_VALUES, repeat=2):
        ratios = (first, second, 1, 1, 1)
        matrices = [collision_matrix(types, deleted, ratios) for deleted in range(3)]
        rr = nullspace(stack(matrices[0], matrices[1]))
        assert len(rr) == 3
        assert_coordinates_zero(rr, ((3, 2), (4, 2)))
        for regular in (0, 1):
            assert not nullspace(stack(matrices[regular], matrices[2]))
            intersections += 1
        charts += 1
    assert charts == 16
    assert intersections == 32
    return charts, intersections


def audit_rbb() -> int:
    types = ("R", "B", "B", "T", "T")
    charts = 0
    for ratio in RATIO_VALUES:
        matrices = [
            collision_matrix(types, deleted, (ratio, 1, 1, 1, 1))
            for deleted in range(3)
        ]
        triple = nullspace(stack(*matrices))
        assert len(triple) == 2
        assert_coordinates_zero(
            triple,
            tuple((mode, coord) for mode in (1, 2) for coord in COORDS),
        )
        charts += 1
    assert charts == 4
    return charts


def audit_bbb() -> tuple[int, int]:
    types = ("B", "B", "B", "T", "T")
    matrices = [
        collision_matrix(types, deleted, (1, 1, 1, 1, 1)) for deleted in range(3)
    ]
    pair = nullspace(stack(matrices[0], matrices[1]))
    triple = nullspace(stack(*matrices))
    assert len(pair) == 7
    assert len(triple) == 6
    assert_coordinates_zero(
        pair,
        tuple((mode, coord) for mode in range(3) for coord in (1, 2)),
    )
    assert_coordinates_zero(
        triple,
        tuple((mode, coord) for mode in range(3) for coord in COORDS),
    )
    return len(pair), len(triple)


def bit_count(mask: int) -> int:
    return mask.bit_count()


def audit_inactive_sets() -> dict[str, int]:
    full = 0b1111
    subsets = [mask for mask in range(16) if bit_count(mask) >= 2]
    pairs = [mask for mask in range(16) if bit_count(mask) == 2]

    rrb = [
        (left, right, b_set)
        for left, right, b_set in product(subsets, repeat=3)
        if not left & b_set and not right & b_set
    ]
    assert len(rrb) == 6
    assert all(left == right == (full ^ b_set) for left, right, b_set in rrb)

    two_equal = [
        sets
        for sets in product(pairs, repeat=3)
        if not sets[0] & sets[2] and not sets[1] & sets[2]
    ]
    assert len(two_equal) == 6

    degrees: Counter[tuple[int, int, int, int]] = Counter()
    for sets in product(pairs, repeat=3):
        if sets[0] & sets[1] & sets[2]:
            continue
        degree = tuple(
            sorted(
                (sum(bool(mask & (1 << root)) for mask in sets) for root in range(4)),
                reverse=True,
            )
        )
        degrees[degree] += 1
    assert degrees == Counter({(2, 2, 1, 1): 90, (2, 2, 2, 0): 24})

    rbb = []
    for regular, b_left, b_right in product(subsets, pairs, pairs):
        if b_left | b_right == full:
            continue
        if b_left != b_right:
            continue
        if regular & ~b_left:
            continue
        rbb.append((regular, b_left, b_right))
    assert len(rbb) == 6
    assert all(regular == left == right for regular, left, right in rbb)
    return {"RRB": len(rrb), "two-equal": len(two_equal), "equal": sum(degrees.values()), "RBB": len(rbb)}


def audit_four_b_boundary() -> int:
    checked = 0
    for b_count in (4, 5):
        b_modes = set(range(b_count))
        for h_left, h_right, b_mode in product(MODES, repeat=3):
            if len({h_left, h_right, b_mode}) < 3:
                continue
            assert not b_modes.issubset({h_left, h_right, b_mode})
        checked += 1
    return checked


def main() -> None:
    profiles = audit_zero_b_profiles()
    rrr = audit_rrr()
    rrb = audit_rrb()
    rbb = audit_rbb()
    bbb = audit_bbb()
    inactive = audit_inactive_sets()
    boundary = audit_four_b_boundary()
    print(f"AUDIT PASS: {profiles} zero-b rank-three coordinate profiles")
    print(f"AUDIT PASS: RRR ratio/pair/triple checks are {rrr}")
    print(f"AUDIT PASS: RRB ratio/intersection checks are {rrb}")
    print(f"AUDIT PASS: {rbb} RBB ratio charts; BBB nullities are {bbb}")
    print(f"AUDIT PASS: independent inactive-set ledgers are {inactive}")
    print(f"AUDIT PASS: {boundary} structural four/five-B boundaries")
    print("AUDIT SCOPE: exactly-three-defect R/B five-cells detected")
    print("AUDIT SCOPE: four/five R/B defects and global conjecture remain open")
    print("searches=0")


if __name__ == "__main__":
    main()
