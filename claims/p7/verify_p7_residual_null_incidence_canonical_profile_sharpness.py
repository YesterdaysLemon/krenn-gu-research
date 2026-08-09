"""Verify sharp residual-null incidence on the canonical P7 profile.

This is one fixed exact SymPy calculation.  It performs no support search,
parameter search, or graph-family enumeration.
"""

import sympy as sp

BLOCKERS = ("t", "u01", "v01", "u02", "v02", "u12", "v12")
DOUBLE_TYPES = {
    "u01": (0, 1),
    "v01": (0, 1),
    "u02": (0, 2),
    "v02": (0, 2),
    "u12": (1, 2),
    "v12": (1, 2),
}
PURE_BLOCKERS = {
    0: ("t", "u01", "v01", "u02", "v02"),
    1: ("t", "u01", "v01", "u12", "v12"),
    2: ("t", "u02", "v02", "u12", "v12"),
}
MISSING_PAIRS = {
    0: ("u12", "v12"),
    1: ("u02", "v02"),
    2: ("u01", "v01"),
}


def in_row_span(vector: sp.Matrix, rows: sp.Matrix) -> bool:
    """Return whether a column vector belongs to the span of row covectors."""

    augmented = rows.col_join(vector.T)
    return augmented.rank() == rows.rank()


def main() -> None:
    e = tuple(sp.eye(3).col(c) for c in range(3))

    # Fixed root rows from equation (12) of the note.
    root_rows: list[dict[str, sp.Matrix]] = []
    for i in range(5):
        n = sp.Integer(i + 1)
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

    # Exact canonical blocker types.
    blocker_ranks: dict[str, int] = {}
    for blocker in BLOCKERS:
        rows = sp.Matrix.vstack(*(root_rows[i][blocker].T for i in range(5)))
        blocker_ranks[blocker] = rows.rank()
        if blocker == "t":
            assert rows.rank() == 3
            assert all(in_row_span(e[c], rows) for c in range(3))
        else:
            support = DOUBLE_TYPES[blocker]
            missing = ({0, 1, 2} - set(support)).pop()
            assert rows.rank() == 2
            assert all(in_row_span(e[c], rows) for c in support)
            assert not in_row_span(e[missing], rows)

    # Every fixed root sees a concise three-dimensional row family.
    for i in range(5):
        rows = sp.Matrix.vstack(*(root_rows[i][blocker].T for blocker in BLOCKERS))
        assert rows.rank() == 3

    # The three fixed pure P5 matrices and their exact permanents.
    pure_permanents: dict[int, sp.Expr] = {}
    for color, blockers in PURE_BLOCKERS.items():
        matrix = sp.Matrix(
            [
                [root_rows[i][blocker][color] for blocker in blockers]
                for i in range(5)
            ]
        )
        assert all(entry > 0 for entry in matrix)
        pure_permanents[color] = sp.expand(matrix.per())
    assert pure_permanents == {0: 1020, 1: 2700, 2: 9116}

    g = sp.Matrix((1, 1, 1))
    h = sp.Matrix((1, 2, 3))
    residual_rows: dict[str, tuple[sp.Matrix, sp.Matrix]] = {
        "t": (e[0], g),
        "u01": (e[0], g),
        "v01": (g, e[0]),
        "u02": (g, h),
        "v02": (g, h),
        "u12": (g, h),
        "v12": (g, h),
    }

    # Polar axes and common-null lines.
    coordinate_incidence: dict[str, tuple[int, ...]] = {}
    null_lines: dict[str, sp.Matrix] = {}
    for blocker in BLOCKERS:
        a_w, b_w = residual_rows[blocker]
        polar_rows = sp.Matrix.vstack(a_w.T, b_w.T)
        assert polar_rows.rank() == 2
        coordinate_incidence[blocker] = tuple(
            c for c in range(3) if in_row_span(e[c], polar_rows)
        )
        null_line = a_w.cross(b_w)
        assert null_line != sp.zeros(3, 1)
        assert a_w.dot(null_line) == 0
        assert b_w.dot(null_line) == 0
        null_lines[blocker] = null_line

        # Residual rows restore local rank three at every double blocker.
        root_blocker_rows = sp.Matrix.vstack(
            *(root_rows[i][blocker].T for i in range(5))
        )
        total_rows = root_blocker_rows.col_join(polar_rows)
        assert total_rows.rank() == 3

    boundary = ("t", "u01", "v01")
    assert all(coordinate_incidence[w] == (0,) for w in boundary)
    assert all(coordinate_incidence[w] == () for w in BLOCKERS if w not in boundary)
    assert all(sp.prod(null_lines[w]) == 0 for w in boundary)
    assert all(sp.prod(null_lines[w]) != 0 for w in BLOCKERS if w not in boundary)

    # The three pure residual two-row factors.
    pure_pair_values: dict[int, sp.Expr] = {}
    for color, (u, v) in MISSING_PAIRS.items():
        a_u, b_u = residual_rows[u]
        a_v, b_v = residual_rows[v]
        pure_pair_values[color] = sp.expand(
            a_u[color] * b_v[color] + b_u[color] * a_v[color]
        )
    assert pure_pair_values == {0: 2, 1: 4, 2: 1}

    full_pure_values = {
        color: pure_permanents[color] * pure_pair_values[color]
        for color in range(3)
    }
    assert all(value != 0 for value in full_pure_values.values())

    # Fixed representatives of the arbitrary normal construction: a normal
    # with one zero yields exactly the corresponding coordinate incidence;
    # an all-nonzero normal yields none.
    representative_normals = {
        0: sp.Matrix((0, 1, 1)),
        1: sp.Matrix((1, 0, 1)),
        2: sp.Matrix((1, 1, 0)),
        "torus": sp.Matrix((1, 1, 1)),
    }
    for label, normal in representative_normals.items():
        contained_axes = tuple(c for c in range(3) if normal[c] == 0)
        if label == "torus":
            assert contained_axes == ()
            assert sp.prod(normal) != 0
        else:
            assert contained_axes == (label,)
            assert sp.prod(normal) == 0

    print(
        {
            "verified": True,
            "blocker_ranks": blocker_ranks,
            "pure_p5_permanents": pure_permanents,
            "coordinate_incidence": coordinate_incidence,
            "pure_residual_pair_values": pure_pair_values,
            "full_pure_values": full_pure_values,
            "non_torus_blockers": len(boundary),
            "support_searches": 0,
            "mixed_word_identity_claimed": False,
        }
    )


if __name__ == "__main__":
    main()
