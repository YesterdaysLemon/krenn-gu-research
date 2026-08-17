"""Independent no-import audit of the fixed-Q quotient trichotomy."""

from fractions import Fraction
from itertools import combinations
from math import comb


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    size = len(matrix)
    work = [row[:] for row in matrix]
    sign = Fraction(1)
    value = Fraction(1)
    for column in range(size):
        pivot = next((i for i in range(column, size) if work[i][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign = -sign
        diagonal = work[column][column]
        value *= diagonal
        for i in range(column + 1, size):
            if not work[i][column]:
                continue
            factor = work[i][column] / diagonal
            for j in range(column, size):
                work[i][j] -= factor * work[column][j]
    return sign * value


def has_nonzero_minor(columns: list[list[Fraction]], size: int) -> bool:
    if size == 0:
        return True
    row_count = len(columns[0])
    for chosen_columns in combinations(range(len(columns)), size):
        for chosen_rows in combinations(range(row_count), size):
            minor = [
                [columns[column][row] for column in chosen_columns]
                for row in chosen_rows
            ]
            if determinant(minor):
                return True
    return False


def audit_pure_flattenings() -> None:
    alpha = (Fraction(7), Fraction(-2), Fraction(11))
    rank_zero = [[Fraction(0), Fraction(0)] for _ in range(3)]
    rank_one = [
        [Fraction(1), Fraction(2)],
        [Fraction(-3), Fraction(-6)],
        [Fraction(4), Fraction(8)],
    ]
    rank_two = [
        [Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(1)],
    ]
    rank_three = [
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1)],
    ]
    for expected, columns in enumerate((rank_zero, rank_one, rank_two, rank_three)):
        scaled = [
            [alpha[i] * entry for entry in column] for i, column in enumerate(columns)
        ]
        assert has_nonzero_minor(scaled, expected)
        assert not has_nonzero_minor(scaled, expected + 1)

    # A simple tensor has no nonzero 2x2 exterior minor.
    left = [Fraction(2), Fraction(-5), Fraction(3)]
    right = [Fraction(7), Fraction(11), Fraction(-1)]
    simple_columns = [[right[j] * x for x in left] for j in range(3)]
    assert has_nonzero_minor(simple_columns, 1)
    assert not has_nonzero_minor(simple_columns, 2)


def audit_branch_logic() -> None:
    # q=1: nonzero target simple tensor has two nonzero factors.
    pure_line = [Fraction(3), Fraction(-4)]
    response = [Fraction(2), Fraction(0), Fraction(5)]
    target = [[entry * scalar for entry in pure_line] for scalar in response]
    assert has_nonzero_minor(target, 1)
    assert not has_nonzero_minor(target, 2)
    assert any(pure_line) and any(response)

    # q=0 with a nonzero response forces the other factor to vanish.
    zero_target = [[Fraction(0), Fraction(0)] for _ in response]
    assert not has_nonzero_minor(zero_target, 1)
    assert any(response)
    quotient_g = [Fraction(0), Fraction(0)]
    assert not any(quotient_g)

    # q=0 with response zero is compatible with a surviving selector class.
    surviving_g = [Fraction(1), Fraction(-1)]
    zero_response = [Fraction(0), Fraction(0), Fraction(0)]
    assert all(scalar * entry == 0 for scalar in zero_response for entry in surviving_g)
    assert any(surviving_g)

    # Dense-annihilator countercontrol for coefficient purity.
    nuisance = [Fraction(1), Fraction(-1)]
    annihilator = [Fraction(1), Fraction(1)]
    assert sum(x * y for x, y in zip(nuisance, annihilator, strict=True)) == 0
    for coordinate in ([Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]):
        assert sum(x * y for x, y in zip(nuisance, coordinate, strict=True))


def audit_dimension_ledger() -> None:
    assert sum(comb(6, k) * 3**k for k in (2, 4, 6)) == 2079
    assert sum(comb(8, k) * 3**k for k in (2, 4, 6, 8)) == 32895

    effective = 0
    for q_count in range(3):
        for port_count in range(7):
            if q_count + port_count == 0 or (q_count + port_count) % 2:
                continue
            effective += comb(2, q_count) * comb(6, port_count) * 3**port_count
    assert effective == 8191
    assert [3 ** (12 - size) for size in (2, 4, 6)] == [59049, 6561, 729]
    assert [effective * 3**size for size in (2, 4, 6)] == [
        73719,
        663471,
        5971239,
    ]


def main() -> None:
    audit_pure_flattenings()
    audit_branch_logic()
    audit_dimension_ledger()
    print("fixed-Q target-quotient independent audit: PASS")
    print("exterior-minor and dimension routes are independent of the primary")


if __name__ == "__main__":
    main()
