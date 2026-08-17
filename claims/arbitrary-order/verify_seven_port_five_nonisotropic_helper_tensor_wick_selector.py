"""Primary exact replay for the seven-port five-helper tensor selector."""

from itertools import combinations, product

import sympy as sp


PAIRS = tuple(combinations(range(7), 2))
FOURS = tuple(combinations(range(7), 4))


def wick_matrix(vectors: tuple[tuple[int, int], ...]) -> sp.Matrix:
    def pairing(left: int, right: int):
        a_i, b_i = vectors[left]
        a_j, b_j = vectors[right]
        return a_i * b_j + b_i * a_j

    rows = []
    for four in FOURS:
        four_set = set(four)
        row = []
        for pair in PAIRS:
            if set(pair) <= four_set:
                left, right = tuple(four_set - set(pair))
                row.append(pairing(left, right))
            else:
                row.append(0)
        rows.append(row)
    return sp.Matrix(rows)


def coordinate_is_selected(matrix: sp.Matrix, pair: tuple[int, int]) -> bool:
    coordinate = sp.zeros(1, len(PAIRS))
    coordinate[0, PAIRS.index(tuple(sorted(pair)))] = 1
    return matrix.col_join(coordinate).rank() == matrix.rank()


def check_three_branches() -> None:
    helpers = ((2, 13), (3, 17), (5, 19), (7, 23), (11, 29))

    both_nonzero = ((1, 0), (0, 1)) + helpers
    full = wick_matrix(both_nonzero)
    assert full.rank() == 21
    assert coordinate_is_selected(full, (0, 1))

    one_zero = ((0, 0), (1, 0)) + helpers
    one_matrix = wick_matrix(one_zero)
    star_columns = [PAIRS.index((0, i)) for i in range(1, 7)]
    star_rows = [index for index, four in enumerate(FOURS) if 0 in four]
    star = one_matrix.extract(star_rows, star_columns)
    assert star.shape == (20, 6)
    assert star.rank() == 6

    both_zero = ((0, 0), (0, 0)) + helpers
    zero_matrix = wick_matrix(both_zero)
    pair_column = PAIRS.index((0, 1))
    witness_rows = [
        index
        for index, four in enumerate(FOURS)
        if set((0, 1)) <= set(four) and zero_matrix[index, pair_column] != 0
    ]
    assert witness_rows
    row = zero_matrix.row(witness_rows[0])
    assert [index for index, value in enumerate(row) if value] == [pair_column]


def check_all_tensor_coordinates() -> None:
    # Colour zero is a nonisotropic helper at every port.  The other endpoint
    # colours exercise zero, isotropic, and nonisotropic cases.
    port_colours = tuple(
        (
            (index + 2, index + 11),
            (0, 0),
            (index + 3, 0) if index % 2 == 0 else (0, index + 5),
        )
        for index in range(7)
    )
    checked = 0
    branch_counts = {"both_nonzero": 0, "one_zero": 0, "both_zero": 0}
    for u, v in PAIRS:
        for colour_u, colour_v in product(range(3), repeat=2):
            word = []
            for port in range(7):
                if port == u:
                    colour = colour_u
                elif port == v:
                    colour = colour_v
                else:
                    colour = 0
                word.append(port_colours[port][colour])
            for helper in set(range(7)) - {u, v}:
                a_i, b_i = word[helper]
                assert a_i * b_i != 0
            zero_u = word[u] == (0, 0)
            zero_v = word[v] == (0, 0)
            if not zero_u and not zero_v:
                support_a = {i for i, (a_i, _) in enumerate(word) if a_i}
                support_b = {i for i, (_, b_i) in enumerate(word) if b_i}
                assert len(support_a) >= 5 and len(support_b) >= 5
                assert support_a | support_b == set(range(7))
                branch_counts["both_nonzero"] += 1
            elif zero_u != zero_v:
                zero = u if zero_u else v
                support_a = {i for i, (a_i, _) in enumerate(word) if i != zero and a_i}
                support_b = {i for i, (_, b_i) in enumerate(word) if i != zero and b_i}
                assert len(support_a) >= 5 and len(support_b) >= 5
                branch_counts["one_zero"] += 1
            else:
                helpers = set(range(7)) - {u, v}
                assert any(
                    word[i][0] * word[j][1] + word[i][1] * word[j][0]
                    for i, j in combinations(sorted(helpers), 2)
                )
                branch_counts["both_zero"] += 1
            checked += 1
    assert checked == 21 * 9
    assert branch_counts == {"both_nonzero": 84, "one_zero": 84, "both_zero": 21}


def check_sharp_support_boundaries() -> None:
    # Six-port 3+3 two-shore control, embedded with a zero seventh port.
    vectors = ((1, 1),) * 3 + ((1, -1),) * 3 + ((0, 0),)
    matrix = wick_matrix(vectors)
    six_rows = [i for i, four in enumerate(FOURS) if 6 not in four]
    six_columns = [i for i, pair in enumerate(PAIRS) if 6 not in pair]
    six = matrix.extract(six_rows, six_columns)
    assert six.rank() == 10
    rectangle = sp.zeros(len(six_columns), 1)
    six_pairs = [PAIRS[i] for i in six_columns]
    for pair, value in {
        (0, 3): 1,
        (0, 4): -1,
        (1, 3): -1,
        (1, 4): 1,
    }.items():
        rectangle[six_pairs.index(pair)] = value
    assert six * rectangle == sp.zeros(len(six_rows), 1)

    # Seven-port union-five target-diagonal control.
    union_five = ((1, 1),) * 5 + ((0, 0),) * 2
    five_matrix = wick_matrix(union_five)
    assert five_matrix.rank() == 16
    kernel = sp.zeros(len(PAIRS), 1)
    for pair, value in {
        (0, 1): 1,
        (2, 3): 1,
        (0, 2): -1,
        (1, 3): -1,
    }.items():
        kernel[PAIRS.index(pair)] = value
    assert five_matrix * kernel == sp.zeros(len(FOURS), 1)


def main() -> None:
    check_three_branches()
    check_all_tensor_coordinates()
    check_sharp_support_boundaries()
    print("seven-port five-helper tensor Wick primary replay: PASS")


if __name__ == "__main__":
    main()
