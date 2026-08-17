"""Independent no-import audit of common-contraction synchronization."""

from fractions import Fraction


def rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    if not work:
        return 0
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def family_matrix(index: int, x: Fraction, y: Fraction) -> list[list[Fraction]]:
    return [
        [Fraction(1), Fraction(0)],
        [Fraction(0), x + index],
        [Fraction(0), y + index + 1],
    ]


def append_desired(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    desired = (Fraction(0), Fraction(1), Fraction(0))
    return [row + [desired[i]] for i, row in enumerate(matrix)]


def audit_common_points() -> None:
    x = Fraction(2)
    y = Fraction(3)
    for size in (7, 31):
        for index in range(1, size + 1):
            nuisance = family_matrix(index, x, y)
            assert rank(nuisance) == 2
            assert rank(append_desired(nuisance)) == 3
            assert x + 2 * index + 1


def audit_disjoint_exceptional_points() -> None:
    def survives(target: int, value: int) -> bool:
        nuisance = [[Fraction(value - target)]]
        augmented = [[Fraction(value - target), Fraction(1)]]
        return rank(augmented) == rank(nuisance) + 1

    assert survives(1, 1)
    assert not survives(2, 1)
    assert survives(2, 2)
    assert not survives(1, 2)
    for target in (1, 2):
        assert rank([[Fraction(3 - target)]]) == 1


def main() -> None:
    audit_common_points()
    audit_disjoint_exceptional_points()
    print("maximal-nuisance-rank synchronization independent audit: PASS")


if __name__ == "__main__":
    main()
