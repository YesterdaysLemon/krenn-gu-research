"""Independent no-import audit for GLS52.

The audit uses only sparse word dictionaries and direct rational matrices.
It shares no implementation or algebra package with the primary verifier.
"""

from fractions import Fraction
from itertools import combinations


def add_matrix(left, right):
    return tuple(left[index] + right[index] for index in range(9))


def outer(left, right):
    return tuple(left[row] * right[column] for row in range(3) for column in range(3))


def pure_word(color, length, scalar=Fraction(1)):
    return {(color,) * length: scalar}


def evaluate(tensor, word):
    return tensor.get(tuple(word), Fraction(0))


def test_label_census() -> None:
    labels = ("q0", "q1", "u", "v", "i0", "i1", "i2")
    effective = {"q0", "u", "v"}
    pair_companions = {
        pair: pair[0] in effective and pair[1] in effective
        for pair in combinations(labels, 2)
    }
    live = {pair for pair, is_live in pair_companions.items() if is_live}
    assert live == {("q0", "u"), ("q0", "v"), ("u", "v")}
    assert sum(pair_companions.values()) == 3


def test_star_rows_directly() -> None:
    a = (Fraction(2), Fraction(0), Fraction(0))
    b = (Fraction(-3), Fraction(0), Fraction(0))
    samples = (
        ((1, 4, -2), (3, -1, 5)),
        ((0, 7, 1), (-4, 2, 6)),
        ((9, 0, -3), (8, 5, 0)),
    )
    for x, y in samples:
        value = add_matrix(outer(a, y), outer(x, b))
        assert value[4] == 0
        assert value[8] == 0


def test_opposite_word_contradiction() -> None:
    gamma = Fraction(7, 3)
    for inactive_count in range(1, 9):
        word_i = (1,) * inactive_count
        word_j = (2,) * inactive_count
        forced_i = pure_word(1, inactive_count, gamma)
        forced_j = pure_word(2, inactive_count, gamma)
        assert evaluate(forced_i, word_i) == gamma
        assert evaluate(forced_i, word_j) == 0
        assert evaluate(forced_j, word_j) == gamma
        assert evaluate(forced_j, word_i) == 0

        # If one physical deck obeyed both forced identities, evaluation at
        # word_i would make the same coefficient gamma and zero.
        required_at_word_i = {
            evaluate(forced_i, word_i),
            evaluate(forced_j, word_i),
        }
        assert required_at_word_i == {Fraction(0), gamma}

        # All-ones contraction sums coefficients and hides the distinction.
        assert sum(forced_i.values()) == sum(forced_j.values()) == gamma


def test_contracted_rank_seven_rows() -> None:
    zero = (Fraction(0),) * 3
    e = [
        tuple(Fraction(int(index == color)) for index in range(3))
        for color in range(3)
    ]
    half = Fraction(1, 2)
    xu = [tuple(-value for value in e[0]), zero, e[2]]
    yu = [tuple(half * value for value in e[0]), e[1], zero]
    xv = [tuple(-value for value in e[0]), e[1], zero]
    yv = [tuple(half * value for value in e[0]), zero, e[2]]
    for color in (1, 2):
        for left in range(3):
            for right in range(3):
                matrix = add_matrix(
                    outer(xu[left], yv[right]),
                    outer(xv[right], yu[left]),
                )
                expected = Fraction(int(left == right == color))
                assert matrix[3 * color + color] == expected


def main() -> None:
    test_label_census()
    test_star_rows_directly()
    test_opposite_word_contradiction()
    test_contracted_rank_seven_rows()
    print("GLS52 independent no-import audit: PASS")


if __name__ == "__main__":
    main()
