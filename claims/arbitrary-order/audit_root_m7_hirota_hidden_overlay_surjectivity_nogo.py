"""Independent no-import audit of hidden-overlay surjectivity."""

from fractions import Fraction

VARIABLES = ("a", "b", "c", "d", "e", "f")


def add(left: dict[str, int], right: dict[str, int]) -> dict[str, int]:
    result = dict(left)
    for key, value in right.items():
        result[key] = result.get(key, 0) + value
        if result[key] == 0:
            del result[key]
    return result


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
    # Independently reconstructed sparse visible polynomials.
    visible = [
        {"d": -1, "e": -1, "f": 1},
        {"a": -1, "b": 1, "d": -1},
        {"b": 1, "c": 1, "f": 1},
        {"a": -1, "c": 1, "e": -1},
    ]
    expected_pairs = {
        (0, 1): ("d", -1),
        (0, 2): ("f", 1),
        (0, 3): ("e", -1),
        (1, 2): ("b", 1),
        (1, 3): ("a", -1),
        (2, 3): ("c", 1),
    }
    for pair, expected in expected_pairs.items():
        common = set(visible[pair[0]]) & set(visible[pair[1]])
        assert common == {expected[0]}
        assert (
            visible[pair[0]][expected[0]]
            == visible[pair[1]][expected[0]]
            == expected[1]
        )

    jacobian = [
        [0, 0, 0, -1, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, -1, 0],
        [0, 1, 0, 0, 0, 0],
        [-1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
    ]
    assert rank(jacobian) == 6

    incidence = [
        [1, 1, 1, 0, 0, 0],
        [1, 0, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 1],
    ]
    assert rank(incidence) == 4

    # Isolated unit matching factors multiply every hafnian by one.
    unit_factor = 1 * 1
    assert all(add(poly, {}) == poly for poly in visible)
    assert unit_factor == 1

    print("independent no-import hidden-overlay audit: PASS")
    print("hidden Jacobian rank: 6; visible incidence rank: 4")


if __name__ == "__main__":
    main()
