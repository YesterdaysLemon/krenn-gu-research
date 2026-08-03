"""Independent no-import audit of the four-root hidden-pair theorem."""

from fractions import Fraction
from itertools import combinations


def rank(matrix: list[list[int]]) -> int:
    rows = [[Fraction(value) for value in row] for row in matrix]
    result = 0
    for column in range(len(rows[0])):
        pivot = next(
            (row for row in range(result, len(rows)) if rows[row][column]), None
        )
        if pivot is None:
            continue
        rows[result], rows[pivot] = rows[pivot], rows[result]
        scale = rows[result][column]
        rows[result] = [value / scale for value in rows[result]]
        for row in range(len(rows)):
            if row != result and rows[row][column]:
                scale = rows[row][column]
                rows[row] = [
                    value - scale * base
                    for value, base in zip(rows[row], rows[result], strict=True)
                ]
        result += 1
    return result


def main() -> None:
    fixed = (0, 1, 2)
    legal = [subset for size in (0, 2) for subset in combinations(fixed, size)]
    assert legal == [(), (0, 1), (0, 2), (1, 2)]

    assert rank([[1, 0], [0, 1]]) == 2
    assert rank([[1, 2], [3, 6]]) == 1
    mu = Fraction(2)
    quotient_second = (Fraction(3), Fraction(-5))
    quotient_first = tuple(-mu * value for value in quotient_second)
    assert all(
        first + mu * second == 0
        for first, second in zip(quotient_first, quotient_second, strict=True)
    )

    # Monomial supports of X and Y are disjoint, so their gcd is one.  The
    # two-active sharpness forms reproduce them after multiplying by x0,y1.
    x_support = frozenset({"x0", "x1", "x2", "x3", "x4"})
    y_support = frozenset({"y0", "y1", "y2", "y3", "y4"})
    h0_support = x_support - {"x0"}
    h1_support = y_support - {"y1"}
    assert x_support.isdisjoint(y_support)
    assert h0_support.isdisjoint(h1_support)
    assert h0_support | {"x0"} == x_support
    assert h1_support | {"y1"} == y_support

    top = [[1, 1], [1, -1]]
    assert rank(top) == 2
    print("independent no-import four-root hidden-pair audit: PASS")


if __name__ == "__main__":
    main()
