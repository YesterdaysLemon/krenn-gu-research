"""Independent no-import audit of the canonical-profile incidence boundary."""


BLOCKERS = ("t", "u01", "v01", "u02", "v02", "u12", "v12")
PURE_BLOCKERS = {
    0: ("t", "u01", "v01", "u02", "v02"),
    1: ("t", "u01", "v01", "u12", "v12"),
    2: ("t", "u02", "v02", "u12", "v12"),
}
MISSING_PAIRS = {0: ("u12", "v12"), 1: ("u02", "v02"), 2: ("u01", "v01")}


def rank(matrix):
    work = [list(map(int, row)) for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        for row in range(pivot_row + 1, rows):
            entry = work[row][column]
            if entry:
                work[row] = [
                    pivot_value * work[row][j] - entry * work[pivot_row][j]
                    for j in range(columns)
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def permanent(matrix):
    size = len(matrix)
    states = {0: 1}
    for row in matrix:
        updated = {}
        for mask, coefficient in states.items():
            for column in range(size):
                if not mask & (1 << column):
                    new_mask = mask | (1 << column)
                    updated[new_mask] = updated.get(new_mask, 0) + coefficient * row[column]
        states = updated
    return states[(1 << size) - 1]


def cross(left, right):
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def dot(left, right):
    return sum(x * y for x, y in zip(left, right, strict=True))


def main() -> None:
    root_rows = []
    for i in range(5):
        n = i + 1
        root_rows.append(
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

    expected_ranks = {"t": 3, **{blocker: 2 for blocker in BLOCKERS[1:]}}
    actual_ranks = {
        blocker: rank([root_rows[i][blocker] for i in range(5)])
        for blocker in BLOCKERS
    }
    assert actual_ranks == expected_ranks
    assert all(rank([root_rows[i][blocker] for blocker in BLOCKERS]) == 3 for i in range(5))

    pure = {}
    for color, blockers in PURE_BLOCKERS.items():
        matrix = [[root_rows[i][blocker][color] for blocker in blockers] for i in range(5)]
        assert all(entry > 0 for row in matrix for entry in row)
        pure[color] = permanent(matrix)
    assert pure == {0: 1020, 1: 2700, 2: 9116}

    e0 = (1, 0, 0)
    g = (1, 1, 1)
    h = (1, 2, 3)
    residual = {
        "t": (e0, g),
        "u01": (e0, g),
        "v01": (g, e0),
        "u02": (g, h),
        "v02": (g, h),
        "u12": (g, h),
        "v12": (g, h),
    }

    boundary = {"t", "u01", "v01"}
    for blocker in BLOCKERS:
        a_w, b_w = residual[blocker]
        normal = cross(a_w, b_w)
        assert normal != (0, 0, 0)
        assert dot(a_w, normal) == dot(b_w, normal) == 0
        zero_coordinates = tuple(color for color in range(3) if normal[color] == 0)
        if blocker in boundary:
            assert zero_coordinates == (0,)
        else:
            assert zero_coordinates == ()
        assert rank([*([root_rows[i][blocker] for i in range(5)]), a_w, b_w]) == 3

    pair_values = {}
    for color, (u, v) in MISSING_PAIRS.items():
        a_u, b_u = residual[u]
        a_v, b_v = residual[v]
        pair_values[color] = a_u[color] * b_v[color] + b_u[color] * a_v[color]
    assert pair_values == {0: 2, 1: 4, 2: 1}
    assert {color: pure[color] * pair_values[color] for color in range(3)} == {
        0: 2040,
        1: 10800,
        2: 9116,
    }

    # A polar normal with one prescribed zero and two nonzero coordinates
    # yields exactly that incidence; an all-nonzero normal yields none.
    for color in range(3):
        normal = tuple(0 if coordinate == color else coordinate + 1 for coordinate in range(3))
        assert tuple(i for i, value in enumerate(normal) if value == 0) == (color,)
    assert all((1, 2, 3)[color] != 0 for color in range(3))

    print("PASS: independent exact canonical-profile incidence audit")
    print("PASS: three clustered non-torus blockers and all pure factors")
    print("SCOPE: mixed-word P7 identity is not claimed")


if __name__ == "__main__":
    main()
