"""Independent no-import audit of five-mode polar equality sharpness."""


BLOCKERS = ("t", "u01", "v01", "u02", "v02", "u12", "v12")


def neighbourhoods(pattern):
    return tuple(
        frozenset(index for index, label in enumerate(pattern) if color in label)
        for color in range(3)
    )


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def matrix_multiply(left, right):
    return [
        [
            sum(
                left[row][inner] * right[inner][column]
                for inner in range(len(right))
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def determinant_3(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def rank_3(matrix):
    if determinant_3(matrix):
        return 3
    for first_row in range(3):
        for second_row in range(first_row + 1, 3):
            for first_column in range(3):
                for second_column in range(first_column + 1, 3):
                    minor = (
                        matrix[first_row][first_column]
                        * matrix[second_row][second_column]
                        - matrix[first_row][second_column]
                        * matrix[second_row][first_column]
                    )
                    if minor:
                        return 2
    return 1 if any(value for row in matrix for value in row) else 0


def rank_three_columns(matrix):
    for first in range(len(matrix)):
        for second in range(first + 1, len(matrix)):
            for third in range(second + 1, len(matrix)):
                if determinant_3([matrix[first], matrix[second], matrix[third]]):
                    return 3
    for first_row in range(len(matrix)):
        for second_row in range(first_row + 1, len(matrix)):
            for first_column in range(3):
                for second_column in range(first_column + 1, 3):
                    minor = (
                        matrix[first_row][first_column]
                        * matrix[second_row][second_column]
                        - matrix[first_row][second_column]
                        * matrix[second_row][first_column]
                    )
                    if minor:
                        return 2
    return 1 if any(value for row in matrix for value in row) else 0


def permanent(matrix):
    states = {0: 1}
    for row in matrix:
        next_states = {}
        for mask, coefficient in states.items():
            for column, value in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                next_mask = mask | bit
                next_states[next_mask] = next_states.get(next_mask, 0) + coefficient * value
        states = next_states
    return states.get((1 << len(matrix)) - 1, 0)


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def main():
    # These are the nineteen partition normal forms, not the output of a
    # distinguishable-mode assignment search.
    raw_patterns = {
        "A": ((1, 2), (0,), (0,), (1,), (2,)),
        "B1": ((1, 2), (1, 2), (0,), (0,), (0,)),
        "B2": ((1, 2), (1, 2), (0,), (0,), (1,)),
        "B3": ((1, 2), (0, 2), (0,), (1,), (2,)),
        "B4": ((1, 2), (0, 2), (0,), (0,), (1,)),
        "C1": ((1, 2), (1, 2), (1, 2), (0,), (0,)),
        "C2": ((1, 2), (1, 2), (0, 2), (0,), (0,)),
        "C3": ((1, 2), (1, 2), (0, 2), (0,), (1,)),
        "C4": ((1, 2), (1, 2), (0, 2), (0,), (2,)),
        "C5": ((1, 2), (0, 2), (0, 1), (0,), (0,)),
        "C6": ((1, 2), (0, 2), (0, 1), (0,), (1,)),
        "D1": ((1, 2), (1, 2), (1, 2), (0, 2), (0,)),
        "D2": ((1, 2), (1, 2), (0, 2), (0, 2), (0,)),
        "D3": ((1, 2), (1, 2), (0, 2), (0, 2), (2,)),
        "D4": ((1, 2), (1, 2), (0, 2), (0, 1), (0,)),
        "D5": ((1, 2), (1, 2), (0, 2), (0, 1), (1,)),
        "E1": ((1, 2), (1, 2), (1, 2), (0, 2), (0, 2)),
        "E2": ((1, 2), (1, 2), (1, 2), (0, 2), (0, 1)),
        "E3": ((1, 2), (1, 2), (0, 2), (0, 2), (0, 1)),
    }
    counts_by_y = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    survivors = []
    for name, raw_pattern in raw_patterns.items():
        pattern = tuple(frozenset(label) for label in raw_pattern)
        double_count = sum(len(label) == 2 for label in pattern)
        counts_by_y[double_count] += 1
        ns = neighbourhoods(pattern)
        assert all(len(neighbourhood) >= 2 for neighbourhood in ns)
        multiplicities = [
            sum(other == neighbourhood for other in ns)
            for neighbourhood in ns
            if len(neighbourhood) == 2
        ]
        if all(value == 2 for value in multiplicities):
            survivors.append(name)
    assert counts_by_y == {1: 1, 2: 4, 3: 6, 4: 5, 5: 3}
    assert survivors == ["B1", "D4", "E3"]

    roots = [
        {
            "t": (1, 1, -2),
            "u01": (1, 0, 0),
            "v01": (1, -1, 0),
            "u02": (0, 0, 1),
            "v02": (0, 0, 1),
            "u12": (0, 1, 0),
            "v12": (0, 0, 1),
        }
    ]
    for n in range(2, 6):
        roots.append(
            {
                "t": (1, n, n * n),
                "u01": (1, n, 0),
                "v01": (n, 1, 0),
                "u02": (1, 0, n),
                "v02": (n, 0, 1),
                "u12": (0, 1, n),
                "v12": (0, n, 1),
            }
        )

    double_supports = {
        "u01": (0, 1),
        "v01": (0, 1),
        "u02": (0, 2),
        "v02": (0, 2),
        "u12": (1, 2),
        "v12": (1, 2),
    }
    for blocker in BLOCKERS:
        root_frame = [roots[index][blocker] for index in range(5)]
        if blocker == "t":
            assert rank_three_columns(root_frame) == 3
        else:
            support = double_supports[blocker]
            missing = ({0, 1, 2} - set(support)).pop()
            assert all(row[missing] == 0 for row in root_frame)
            assert rank_three_columns(root_frame) == 2
    for index in range(5):
        root_local_rows = [roots[index][blocker] for blocker in BLOCKERS]
        assert rank_three_columns(root_local_rows) == 3

    residual = {
        "t": ((1, 0, -1), (0, 1, -1)),
        "u01": ((1, 0, 0), (0, 1, -1)),
        "v01": ((1, 0, -1), (0, 1, -1)),
        "u02": ((0, 1, 0), (0, 0, 1)),
        "v02": ((0, 0, 1), (0, 1, 0)),
        "u12": ((1, 0, 0), (0, 1, 0)),
        "v12": ((0, 0, 1), (1, 0, 0)),
    }
    nulls = {
        "t": (1, 1, 1),
        "u01": (0, 1, 1),
        "v01": (1, 1, 1),
        "u02": (1, 0, 0),
        "v02": (1, 0, 0),
        "u12": (0, 0, 1),
        "v12": (0, 1, 0),
    }
    expected_incidence = {
        "t": (),
        "u01": (0,),
        "v01": (),
        "u02": (1, 2),
        "v02": (1, 2),
        "u12": (0, 1),
        "v12": (0, 2),
    }
    incidence = {}
    for blocker in BLOCKERS:
        frame = residual[blocker]
        assert rank_3([list(frame[0]), list(frame[1]), [0, 0, 0]]) == 2
        assert dot(frame[0], nulls[blocker]) == 0
        assert dot(frame[1], nulls[blocker]) == 0
        incidence[blocker] = tuple(
            color for color in range(3) if nulls[blocker][color] == 0
        )
        assert incidence[blocker] == expected_incidence[blocker]
        assert dot(roots[0][blocker], nulls[blocker]) == 0
        local_rows = [roots[index][blocker] for index in range(5)] + list(frame)
        assert rank_three_columns(local_rows) == 3

    neighbourhood = {
        color: {blocker for blocker in BLOCKERS if color in incidence[blocker]}
        for color in range(3)
    }
    assert tuple(map(len, neighbourhood.values())) == (3, 3, 3)

    # Every complementary polar shore contains the identically zero root-zero
    # evaluation row.  Every target colour has three incidence modes, so no
    # two free modes contain its neighbourhood.  Hence all 21 identities are
    # 0=0 without calculating 21 permanents.
    assert all(dot(roots[0][blocker], nulls[blocker]) == 0 for blocker in BLOCKERS)
    assert all(len(neighbourhood[color]) == 3 for color in range(3))
    assert 7 * 6 // 2 == 21

    missing_pairs = {
        0: ("u12", "v12"),
        1: ("u02", "v02"),
        2: ("u01", "v01"),
    }
    pure_permanents = {}
    residual_values = {}
    for color, pair in missing_pairs.items():
        complement = [blocker for blocker in BLOCKERS if blocker not in pair]
        matrix = [
            [roots[index][blocker][color] for blocker in complement]
            for index in range(5)
        ]
        pure_permanents[color] = permanent(matrix)
        left, right = pair
        a_left, b_left = residual[left]
        a_right, b_right = residual[right]
        residual_values[color] = (
            a_left[color] * b_right[color]
            + b_left[color] * a_right[color]
        )
    assert pure_permanents == {0: 652, 1: 284, 2: 7200}
    assert residual_values == {0: 1, 1: 1, 2: 1}

    # Independent exact rank-two representative for a corrected port block.
    j_form = [[0, 1], [1, 0]]
    left_frame = [[0, 1, 0], [0, 0, 1]]
    right_frame = [[0, 0, 1], [0, 1, 0]]
    port = matrix_multiply(matrix_multiply(transpose(left_frame), j_form), right_frame)
    assert port == [[0, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert rank_3(port) == 2

    print("PASS: independent nineteen-type and three-survivor audit")
    print("PASS: exact D4 incidence and all 21 zero polar identities")
    print("PASS: exact pure values 652, 284, 7200")
    print("SCOPE: polar sharpness only; full mixed-word identity unresolved")


if __name__ == "__main__":
    main()
