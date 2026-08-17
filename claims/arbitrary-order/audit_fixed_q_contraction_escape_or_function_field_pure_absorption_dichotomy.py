"""Independent no-import audit of contraction escape/generic absorption."""

from fractions import Fraction


Polynomial = tuple[int, ...]


def trim(polynomial: Polynomial) -> Polynomial:
    values = list(polynomial)
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer = [0] * (len(left) + len(right) - 1)
    for i, first in enumerate(left):
        for j, second in enumerate(right):
            answer[i + j] += first * second
    return trim(tuple(answer))


def evaluate(polynomial: Polynomial, value: Fraction) -> Fraction:
    answer = Fraction(0)
    for coefficient in reversed(polynomial):
        answer = answer * value + coefficient
    return answer


def rank(rows: list[list[Fraction]]) -> int:
    matrix = [row[:] for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (index for index in range(pivot_row, len(matrix)) if matrix[index][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for index, row in enumerate(matrix):
            if index == pivot_row or not row[column]:
                continue
            factor = row[column]
            matrix[index] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(row, matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def check_escapable_controls() -> None:
    determinants = ((1, -1), (-1, 2, -1))
    for target_count in (7, 31):
        product_value: Polynomial = (1,)
        for index in range(target_count):
            product_value = multiply(product_value, determinants[index % 2])
        assert product_value != (0,)
        assert evaluate(product_value, Fraction(2)) != 0

    for power in (1, 2):
        at_one = Fraction(1 - 1) ** power
        at_two = Fraction(2 - 1) ** power
        nuisance_one = [[Fraction(1)], [at_one]]
        augmented_one = [[Fraction(1), Fraction(1)], [at_one, Fraction(0)]]
        nuisance_two = [[Fraction(1)], [at_two]]
        augmented_two = [[Fraction(1), Fraction(1)], [at_two, Fraction(0)]]
        assert rank(nuisance_one) == rank(augmented_one) == 1
        assert rank(nuisance_two) == 1
        assert rank(augmented_two) == 2


def check_persistent_and_zero_controls() -> None:
    for value in (Fraction(0), Fraction(2), Fraction(5, 3)):
        nuisance = value - 1
        assert nuisance * 1 == (value - 1) * 1
        if value == 1:
            raise AssertionError("unexpected test value")
    assert rank([[Fraction(0)]]) == 0
    assert rank([[Fraction(0), Fraction(1)]]) == 1

    nuisance = [[Fraction(1)], [Fraction(0)]]
    with_pure = [[Fraction(1), Fraction(1)], [Fraction(0), Fraction(0)]]
    with_desired = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
    assert rank(nuisance) == rank(with_pure) == 1
    assert rank(with_desired) == 2


def main() -> None:
    check_escapable_controls()
    check_persistent_and_zero_controls()
    print("fixed-Q contraction escape/generic absorption independent audit: PASS")


if __name__ == "__main__":
    main()
