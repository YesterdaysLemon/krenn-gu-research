"""Verify five-mode incidence classification and exact P7 polar sharpness.

The normal forms are derived by the partition argument in the note.  This
script checks those forms and one fixed rational model; it performs no mode
assignment, support, word, graph, or parameter search.
"""

import sympy as sp

IncidenceType = tuple[frozenset[int], ...]

BLOCKERS = ("t", "u01", "v01", "u02", "v02", "u12", "v12")
DOUBLE_TYPES = {
    "u01": (0, 1),
    "v01": (0, 1),
    "u02": (0, 2),
    "v02": (0, 2),
    "u12": (1, 2),
    "v12": (1, 2),
}
MISSING_PAIRS = {
    0: ("u12", "v12"),
    1: ("u02", "v02"),
    2: ("u01", "v01"),
}


def neighbourhoods(pattern: IncidenceType) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(index for index, label in enumerate(pattern) if color in label)
        for color in range(3)
    )


def in_row_span(vector: sp.Matrix, rows: sp.Matrix) -> bool:
    return rows.col_join(vector.T).rank() == rows.rank()


def main() -> None:
    # Nineteen colour-orbit normal forms derived from Y=1,...,5.
    patterns: dict[str, IncidenceType] = {
        "A": ((frozenset((1, 2))), frozenset((0,)), frozenset((0,)), frozenset((1,)), frozenset((2,))),
        "B1": (frozenset((1, 2)), frozenset((1, 2)), frozenset((0,)), frozenset((0,)), frozenset((0,))),
        "B2": (frozenset((1, 2)), frozenset((1, 2)), frozenset((0,)), frozenset((0,)), frozenset((1,))),
        "B3": (frozenset((1, 2)), frozenset((0, 2)), frozenset((0,)), frozenset((1,)), frozenset((2,))),
        "B4": (frozenset((1, 2)), frozenset((0, 2)), frozenset((0,)), frozenset((0,)), frozenset((1,))),
        "C1": (frozenset((1, 2)), frozenset((1, 2)), frozenset((1, 2)), frozenset((0,)), frozenset((0,))),
        "C2": (frozenset((1, 2)), frozenset((1, 2)), frozenset((0, 2)), frozenset((0,)), frozenset((0,))),
        "C3": (frozenset((1, 2)), frozenset((1, 2)), frozenset((0, 2)), frozenset((0,)), frozenset((1,))),
        "C4": (frozenset((1, 2)), frozenset((1, 2)), frozenset((0, 2)), frozenset((0,)), frozenset((2,))),
        "C5": (frozenset((1, 2)), frozenset((0, 2)), frozenset((0, 1)), frozenset((0,)), frozenset((0,))),
        "C6": (frozenset((1, 2)), frozenset((0, 2)), frozenset((0, 1)), frozenset((0,)), frozenset((1,))),
        "D1": (frozenset((1, 2)), frozenset((1, 2)), frozenset((1, 2)), frozenset((0, 2)), frozenset((0,))),
        "D2": (frozenset((1, 2)), frozenset((1, 2)), frozenset((0, 2)), frozenset((0, 2)), frozenset((0,))),
        "D3": (frozenset((1, 2)), frozenset((1, 2)), frozenset((0, 2)), frozenset((0, 2)), frozenset((2,))),
        "D4": (frozenset((1, 2)), frozenset((1, 2)), frozenset((0, 2)), frozenset((0, 1)), frozenset((0,))),
        "D5": (frozenset((1, 2)), frozenset((1, 2)), frozenset((0, 2)), frozenset((0, 1)), frozenset((1,))),
        "E1": (frozenset((1, 2)), frozenset((1, 2)), frozenset((1, 2)), frozenset((0, 2)), frozenset((0, 2))),
        "E2": (frozenset((1, 2)), frozenset((1, 2)), frozenset((1, 2)), frozenset((0, 2)), frozenset((0, 1))),
        "E3": (frozenset((1, 2)), frozenset((1, 2)), frozenset((0, 2)), frozenset((0, 2)), frozenset((0, 1))),
    }
    expected_by_y = {1: 1, 2: 4, 3: 6, 4: 5, 5: 3}
    counts_by_y = {value: 0 for value in expected_by_y}
    polar_survivors: list[str] = []
    for name, pattern in patterns.items():
        double_count = sum(len(label) == 2 for label in pattern)
        counts_by_y[double_count] += 1
        ns = neighbourhoods(pattern)
        assert all(len(neighbourhood) >= 2 for neighbourhood in ns)
        size_two_classes = [
            sum(other == neighbourhood for other in ns)
            for neighbourhood in ns
            if len(neighbourhood) == 2
        ]
        if all(multiplicity == 2 for multiplicity in size_two_classes):
            polar_survivors.append(name)
    assert counts_by_y == expected_by_y
    assert polar_survivors == ["B1", "D4", "E3"]

    e = tuple(sp.eye(3).col(color) for color in range(3))
    root_zero = {
        "t": sp.Matrix((1, 1, -2)),
        "u01": sp.Matrix((1, 0, 0)),
        "v01": sp.Matrix((1, -1, 0)),
        "u02": sp.Matrix((0, 0, 1)),
        "v02": sp.Matrix((0, 0, 1)),
        "u12": sp.Matrix((0, 1, 0)),
        "v12": sp.Matrix((0, 0, 1)),
    }
    root_rows = [root_zero]
    for n_value in range(2, 6):
        n = sp.Integer(n_value)
        root_rows.append(
            {
                "t": sp.Matrix((1, n, n**2)),
                "u01": sp.Matrix((1, n, 0)),
                "v01": sp.Matrix((n, 1, 0)),
                "u02": sp.Matrix((1, 0, n)),
                "v02": sp.Matrix((n, 0, 1)),
                "u12": sp.Matrix((0, 1, n)),
                "v12": sp.Matrix((0, n, 1)),
            }
        )

    # Canonical blocker spans and root-wise local concision.
    for blocker in BLOCKERS:
        rows = sp.Matrix.vstack(*(root_rows[index][blocker].T for index in range(5)))
        if blocker == "t":
            assert rows.rank() == 3
        else:
            support = DOUBLE_TYPES[blocker]
            missing = ({0, 1, 2} - set(support)).pop()
            assert rows.rank() == 2
            assert all(in_row_span(e[color], rows) for color in support)
            assert not in_row_span(e[missing], rows)
    for index in range(5):
        rows = sp.Matrix.vstack(*(root_rows[index][blocker].T for blocker in BLOCKERS))
        assert rows.rank() == 3

    residual_rows = {
        "t": (e[0] - e[2], e[1] - e[2]),
        "u01": (e[0], e[1] - e[2]),
        "v01": (e[0] - e[2], e[1] - e[2]),
        "u02": (e[1], e[2]),
        "v02": (e[2], e[1]),
        "u12": (e[0], e[1]),
        "v12": (e[2], e[0]),
    }
    null_vectors = {
        "t": sp.Matrix((1, 1, 1)),
        "u01": sp.Matrix((0, 1, 1)),
        "v01": sp.Matrix((1, 1, 1)),
        "u02": sp.Matrix((1, 0, 0)),
        "v02": sp.Matrix((1, 0, 0)),
        "u12": sp.Matrix((0, 0, 1)),
        "v12": sp.Matrix((0, 1, 0)),
    }

    coordinate_incidence: dict[str, tuple[int, ...]] = {}
    j_form = sp.Matrix(((0, 1), (1, 0)))
    local_frames: dict[str, sp.Matrix] = {}
    for blocker in BLOCKERS:
        a_w, b_w = residual_rows[blocker]
        frame = sp.Matrix.vstack(a_w.T, b_w.T)
        local_frames[blocker] = frame
        assert frame.rank() == 2
        assert frame * null_vectors[blocker] == sp.zeros(2, 1)
        coordinate_incidence[blocker] = tuple(
            color for color in range(3) if in_row_span(e[color], frame)
        )
        root_frame = sp.Matrix.vstack(
            *(root_rows[index][blocker].T for index in range(5))
        )
        assert root_frame.col_join(frame).rank() == 3
    assert coordinate_incidence == {
        "t": (),
        "u01": (0,),
        "v01": (),
        "u02": (1, 2),
        "v02": (1, 2),
        "u12": (0, 1),
        "v12": (0, 2),
    }

    color_neighbourhoods = {
        color: {
            blocker
            for blocker in BLOCKERS
            if color in coordinate_incidence[blocker]
        }
        for color in range(3)
    }
    assert color_neighbourhoods == {
        0: {"u01", "u12", "v12"},
        1: {"u02", "v02", "u12"},
        2: {"u02", "v02", "v12"},
    }

    evaluated_shore = sp.Matrix(
        [
            [root_rows[index][blocker].dot(null_vectors[blocker]) for blocker in BLOCKERS]
            for index in range(5)
        ]
    )
    assert evaluated_shore.row(0) == sp.zeros(1, 7)

    polar_identity_count = 0
    port_ranks: set[int] = set()
    for left_index in range(7):
        for right_index in range(left_index + 1, 7):
            free_pair = {BLOCKERS[left_index], BLOCKERS[right_index]}
            complement = [
                index for index in range(7) if index not in (left_index, right_index)
            ]
            shore_scalar = sp.per(evaluated_shore[:, complement])
            assert shore_scalar == 0
            target_diagonal = tuple(
                sp.prod(
                    null_vectors[BLOCKERS[index]][color]
                    for index in complement
                )
                for color in range(3)
            )
            assert target_diagonal == (0, 0, 0)
            assert all(
                not neighbourhood.issubset(free_pair)
                for neighbourhood in color_neighbourhoods.values()
            )
            port = (
                local_frames[BLOCKERS[left_index]].T
                * j_form
                * local_frames[BLOCKERS[right_index]]
            )
            port_ranks.add(port.rank())
            polar_identity_count += 1
    assert polar_identity_count == 21
    assert port_ranks == {2}

    pure_permanents: dict[int, sp.Expr] = {}
    residual_values: dict[int, sp.Expr] = {}
    for color, pair in MISSING_PAIRS.items():
        complement = [blocker for blocker in BLOCKERS if blocker not in pair]
        pure_matrix = sp.Matrix(
            [
                [root_rows[index][blocker][color] for blocker in complement]
                for index in range(5)
            ]
        )
        pure_permanents[color] = sp.per(pure_matrix)
        left, right = pair
        port = local_frames[left].T * j_form * local_frames[right]
        residual_values[color] = port[color, color]
    assert pure_permanents == {0: 652, 1: 284, 2: 7200}
    assert residual_values == {0: 1, 1: 1, 2: 1}

    print("PASS: nineteen partition-derived five-mode incidence normal forms")
    print("PASS: exact rank-two polar survivors are B1, D4, E3")
    print("PASS: fixed D4 model satisfies all 21 polar matrix identities")
    print("PASS: canonical profile and pure coefficients 652, 284, 7200")
    print("SCOPE: sharp for polar-plus-pure data; mixed-word identity not claimed")


if __name__ == "__main__":
    main()
