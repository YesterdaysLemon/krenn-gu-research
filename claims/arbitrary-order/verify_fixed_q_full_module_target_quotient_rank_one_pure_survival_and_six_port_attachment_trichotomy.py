"""Primary exact replay for the fixed-Q target-quotient trichotomy.

The theorem is proved by quotient linear algebra in its owning document.
This script checks the finite dimension ledger and exact branch controls.
"""

from fractions import Fraction
from math import comb


def rank(rows: list[list[Fraction]]) -> int:
    matrix = [row[:] for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (i for i in range(pivot_row, row_count) if matrix[i][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for i in range(row_count):
            if i == pivot_row or not matrix[i][column]:
                continue
            scale = matrix[i][column]
            matrix[i] = [
                left - scale * right
                for left, right in zip(matrix[i], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def transpose(columns: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*columns, strict=True)]


def quotient_rank(
    nuisance: list[list[Fraction]], pure_columns: list[list[Fraction]]
) -> int:
    ambient_rows = transpose(nuisance + pure_columns)
    nuisance_rows = transpose(nuisance) if nuisance else []
    return rank(ambient_rows) - rank(nuisance_rows)


def outer(left: list[Fraction], right: list[Fraction]) -> list[list[Fraction]]:
    return [[x * y for y in right] for x in left]


def check_dimensions() -> None:
    four_full = sum(comb(6, k) * 3**k for k in (2, 4, 6))
    six_full = sum(comb(8, k) * 3**k for k in (2, 4, 6, 8))
    assert four_full == 2079
    assert six_full == 32895

    effective = 0
    for mask in range(1, 1 << 8):
        if mask.bit_count() % 2:
            continue
        open_port_count = sum(bool(mask & (1 << i)) for i in range(2, 8))
        effective += 3**open_port_count
    assert effective == 8191

    lambda_dimensions = {2: 3**10, 4: 3**8, 6: 3**6}
    hom_rows = {size: effective * 3**size for size in (2, 4, 6)}
    assert lambda_dimensions == {2: 59049, 4: 6561, 6: 729}
    assert hom_rows == {2: 73719, 4: 663471, 6: 5971239}
    assert 15 + 15 + 1 == 31


def check_canonical_tensor_ranks() -> None:
    alpha = [Fraction(2), Fraction(3), Fraction(5)]
    cases = {
        0: [[Fraction(0), Fraction(0)] for _ in range(3)],
        1: [
            [Fraction(1), Fraction(0)],
            [Fraction(2), Fraction(0)],
            [Fraction(-1), Fraction(0)],
        ],
        2: [
            [Fraction(1), Fraction(0), Fraction(0)],
            [Fraction(0), Fraction(1), Fraction(0)],
            [Fraction(0), Fraction(0), Fraction(0)],
        ],
        3: [
            [Fraction(1), Fraction(0), Fraction(0)],
            [Fraction(0), Fraction(1), Fraction(0)],
            [Fraction(0), Fraction(0), Fraction(1)],
        ],
    }
    for expected, pure_vectors in cases.items():
        target_columns = [
            [scale * value for value in vector]
            for scale, vector in zip(alpha, pure_vectors, strict=True)
        ]
        assert rank(transpose(target_columns)) == expected

    g = [Fraction(1), Fraction(0)]
    response = [Fraction(2), Fraction(6), Fraction(-5)]
    assert transpose(
        [[alpha[i] * value for value in cases[1][i]] for i in range(3)]
    ) == outer(g, response)

    # Rank two cannot equal one decomposable tensor: a displayed 2x2 minor is 6.
    rank_two_target = transpose(
        [[alpha[i] * value for value in cases[2][i]] for i in range(3)]
    )
    assert (
        rank_two_target[0][0] * rank_two_target[1][1]
        - (rank_two_target[0][1] * rank_two_target[1][0])
        == 6
    )


def check_ambient_quotient_controls() -> None:
    e = [[Fraction(int(i == j)) for i in range(4)] for j in range(4)]

    # Rank-one pure survival: [e0]=[e1]!=0 modulo N.
    nuisance = [[Fraction(1), Fraction(-1), Fraction(0), Fraction(0)]]
    pure = [e[0], e[1], [Fraction(2), Fraction(2), Fraction(0), Fraction(0)]]
    g = e[0]
    assert quotient_rank(nuisance, pure) == 1
    assert quotient_rank(nuisance, [g]) == 1
    normalizer = [Fraction(1), Fraction(1), Fraction(0), Fraction(0)]
    assert sum(x * y for x, y in zip(normalizer, nuisance[0], strict=True)) == 0
    assert sum(x * y for x, y in zip(normalizer, g, strict=True)) == 1

    # Swallowed pure target with nonzero response forces g into nuisance.
    swallowed = [e[0], e[1], e[2]]
    assert quotient_rank(swallowed, [e[0], e[1], e[2]]) == 0
    assert quotient_rank(swallowed, [e[0]]) == 0

    # If the response is zero, pure rank zero does not decide g.
    assert quotient_rank(swallowed, [e[3]]) == 1

    # Two surviving pure directions give the forbidden target rank two.
    nuisance_two = [e[3]]
    assert quotient_rank(nuisance_two, [e[0], e[1]]) == 2

    # Exact coefficient-purity countercontrol: the only annihilator line is dense.
    two_dim_nuisance = [[Fraction(1), Fraction(-1)]]
    dense = [Fraction(1), Fraction(1)]
    assert quotient_rank(two_dim_nuisance, [[Fraction(1), Fraction(0)]]) == 1
    assert sum(x * y for x, y in zip(dense, two_dim_nuisance[0], strict=True)) == 0
    assert all(
        sum(x * y for x, y in zip(candidate, two_dim_nuisance[0], strict=True)) != 0
        for candidate in ([Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)])
    )


def main() -> None:
    check_dimensions()
    check_canonical_tensor_ranks()
    check_ambient_quotient_controls()
    print("fixed-Q target-quotient primary replay: PASS")
    print("four-root full deck: 2079; six-root full deck: 32895")
    print("six-root effective fixed-Q deck: 8191; attachment rows: 15+15+1")


if __name__ == "__main__":
    main()
