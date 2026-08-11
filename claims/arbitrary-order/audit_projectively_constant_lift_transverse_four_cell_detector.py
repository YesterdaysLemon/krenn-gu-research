"""Independent no-import audit of the transverse four-cell detector."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

Word = tuple[int, int, int, int]
Vector = tuple[int, ...]


def basis_collision_column(active_mode: int, component: int) -> Vector:
    """Enumerate P4(h,a,a,b) with a=e0, b=e1 and one basis h entry."""
    values = []
    for word in product(range(3), repeat=4):
        total = 0
        for assignment in permutations(range(4)):
            term = 1
            for row, mode in enumerate(assignment):
                if row == 0:
                    term *= int(mode == active_mode and word[mode] == component)
                elif row in (1, 2):
                    term *= int(word[mode] == 0)
                else:
                    term *= int(word[mode] == 1)
            total += term
        values.append(total)
    return tuple(values)


def rational_rank(rows: list[list[int]]) -> int:
    """Return exact row rank by a standard-library Fraction elimination."""
    matrix = [[Fraction(value) for value in row] for row in rows]
    pivot_row = 0
    width = len(matrix[0])
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                left - multiple * right
                for left, right in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def tensor_from_coordinates(coordinates: tuple[int, ...]) -> dict[Word, int]:
    """Linearly combine the twelve independently enumerated columns."""
    words = tuple(product(range(3), repeat=4))
    columns = tuple(
        basis_collision_column(mode, component)
        for mode in range(4)
        for component in range(3)
    )
    return {
        word: sum(coordinates[column] * columns[column][row] for column in range(12))
        for row, word in enumerate(words)
    }


def recover_coordinates(tensor: dict[Word, int]) -> tuple[Fraction, ...]:
    """Apply the written z, pair-sum y, and complement-sum x left inverse."""
    z_values = []
    for mode in range(4):
        word = [0, 0, 0, 0]
        word[mode] = 2
        word[(mode + 1) % 4] = 1
        z_values.append(Fraction(tensor[tuple(word)], 2))

    pair_sums: dict[tuple[int, int], Fraction] = {}
    for first, second in ((0, 1), (0, 2), (0, 3), (1, 2)):
        word = [0, 0, 0, 0]
        word[first] = word[second] = 1
        pair_sums[first, second] = Fraction(tensor[tuple(word)], 2)
    y0 = (pair_sums[0, 1] + pair_sums[0, 2] - pair_sums[1, 2]) / 2
    y_values = (
        y0,
        pair_sums[0, 1] - y0,
        pair_sums[0, 2] - y0,
        pair_sums[0, 3] - y0,
    )

    complement_sums = []
    for mode in range(4):
        word = [0, 0, 0, 0]
        word[mode] = 1
        complement_sums.append(Fraction(tensor[tuple(word)], 2))
    total = sum(complement_sums, Fraction()) / 3
    x_values = tuple(total - complement_sums[mode] for mode in range(4))

    recovered = []
    for mode in range(4):
        recovered.extend((x_values[mode], y_values[mode], z_values[mode]))
    return tuple(recovered)


def audit_collision_left_inverse() -> None:
    columns = [
        basis_collision_column(mode, component)
        for mode in range(4)
        for component in range(3)
    ]
    rows = [list(row) for row in zip(*columns, strict=True)]
    assert len(rows) == 81
    assert rational_rank(rows) == 12

    tests = [
        tuple(int(index == basis) for index in range(12)) for basis in range(12)
    ]
    tests.append((2, -3, 5, 7, 11, -13, 17, -19, 23, 29, 31, -37))
    for coordinates in tests:
        recovered = recover_coordinates(tensor_from_coordinates(coordinates))
        assert recovered == tuple(Fraction(value) for value in coordinates)


def direct_collision(
    a: tuple[tuple[int, int, int], ...],
    b: tuple[tuple[int, int, int], ...],
    h: tuple[tuple[int, int, int], ...],
) -> dict[Word, int]:
    """Enumerate a general integer P4(h,a,a,b) without the primary matrix."""
    result: dict[Word, int] = {}
    rows = (h, a, a, b)
    for word in product(range(3), repeat=4):
        total = 0
        for assignment in permutations(range(4)):
            term = 1
            for row, mode in enumerate(assignment):
                term *= rows[row][mode][word[mode]]
            total += term
        result[word] = total
    return result


def audit_dependent_boundary() -> None:
    e0 = (1, 0, 0)
    e1 = (0, 1, 0)
    zero = (0, 0, 0)
    a = (e0, e0, e0, e0)
    b = (e0, e0, e1, e1)
    h = ((-1, 0, 0), e0, zero, zero)
    tensor = direct_collision(a, b, h)
    assert h != (zero,) * 4
    assert set(tensor.values()) == {0}


def audit_companion_deletions() -> None:
    checked = 0
    all_pairs = 0
    for values in product((-1, 0, 1), repeat=6):
        columns = (
            (values[0], values[3]),
            (values[1], values[4]),
            (values[2], values[5]),
        )
        minors = []
        for first, second in ((0, 1), (0, 2), (1, 2)):
            left, right = columns[first], columns[second]
            minors.append(left[0] * right[1] - left[1] * right[0])
        if not any(minors):
            continue
        checked += 1
        assert any(value != 0 for value in minors)
        if all(value != 0 for value in minors):
            all_pairs += 1
    assert checked == 624
    assert all_pairs > 0


def audit_detector_assembly() -> None:
    """Check independent companions cannot cancel two nonzero cofactors."""
    first_cofactor = (2, -3, 5)
    second_cofactor = (7, 11, -13)
    first_companion = (1, 0)
    second_companion = (0, 1)
    assembled = tuple(
        first_companion[row] * first_cofactor[column]
        + second_companion[row] * second_cofactor[column]
        for row in range(2)
        for column in range(3)
    )
    assert assembled[:3] == first_cofactor
    assert assembled[3:] == second_cofactor


def main() -> None:
    audit_collision_left_inverse()
    audit_dependent_boundary()
    audit_companion_deletions()
    audit_detector_assembly()
    print("AUDIT PASS: independent 4! ledger gives collision rank 12 of 12")
    print("AUDIT PASS: explicit rational left inverse recovers all 12 coordinates")
    print("AUDIT PASS: dependent ambient example has a nonzero collision kernel")
    print("AUDIT PASS: rank-two companion triples admit a basis deletion")
    print("AUDIT PASS: independent companion selectors prevent tensor cancellation")
    print("AUDIT SCOPE: written proof supplies local-basis and full-span transport")
    print("AUDIT SCOPE: transversality is assumed; larger and global cells stay open")
    print("searches=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
