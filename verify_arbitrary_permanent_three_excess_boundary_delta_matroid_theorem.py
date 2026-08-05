"""Exact proof guards for boundary delta-matroid response identities."""

from __future__ import annotations

from itertools import permutations

import sympy as sp


def permanent(matrix: sp.Matrix) -> sp.Expr:
    assert matrix.rows == matrix.cols
    if matrix.rows == 0:
        return sp.Integer(1)
    return sp.expand(
        sum(
            sp.prod(matrix[row, permutation[row]] for row in range(matrix.rows))
            for permutation in permutations(range(matrix.rows))
        )
    )


def delete_row_column(matrix: sp.Matrix, row: int, column: int) -> sp.Matrix:
    return matrix.minor_submatrix(row, column)


def main() -> None:
    # Fixed 2+2 block identity.  This is a 24-term symbolic proof guard, not
    # a support-family or coefficient-word census.
    x = sp.Matrix(2, 2, sp.symbols("x00 x01 x10 x11"))
    y = sp.Matrix(2, 2, sp.symbols("y00 y01 y10 y11"))
    z = sp.Matrix(2, 2, sp.symbols("z00 z01 z10 z11"))
    w = sp.Matrix(2, 2, sp.symbols("w00 w01 w10 w11"))

    c_per = sp.Matrix(
        2,
        2,
        lambda q, r: permanent(delete_row_column(w, r, q)),
    )
    elementary_response = y * c_per * z

    direct_response = sp.Matrix(
        2,
        2,
        lambda i, j: sp.expand(
            sum(
                y[i, q]
                * z[r, j]
                * permanent(delete_row_column(w, r, q))
                for q in range(2)
                for r in range(2)
            )
        ),
    )
    assert elementary_response.applyfunc(sp.expand) == direct_response

    full = x.row_join(y).col_join(z.row_join(w))
    empty_sector = permanent(x) * permanent(w)
    elementary_sector = sp.expand(
        sum(
            elementary_response[i, j]
            * permanent(delete_row_column(x, i, j))
            for i in range(2)
            for j in range(2)
        )
    )
    all_cross_sector = permanent(y) * permanent(z)
    assert sp.expand(
        permanent(full) - empty_sector - elementary_sector - all_cross_sector
    ) == 0

    # One alternating-path toggle: the size-four terminal sector descends to
    # the elementary sector {a1,p1} without a sector census.
    empty_matching = {("r0", "q0"), ("r1", "q1")}
    large_matching = {
        ("a0", "q0"),
        ("a1", "q1"),
        ("r0", "p0"),
        ("r1", "p1"),
    }
    path = {("a0", "q0"), ("r0", "q0"), ("r0", "p0")}
    toggled = large_matching.symmetric_difference(path)
    expected = {("r0", "q0"), ("a1", "q1"), ("r1", "p1")}
    assert toggled == expected
    assert path <= empty_matching.union(large_matching)

    # Boolean B D* C reachability for the same contracted exterior matching.
    # a0 reaches p0 through v0; a1 reaches p1 through v1.  Adding v0->v1
    # also makes (a0,p1) linkable, while (a1,p0) remains cut off.
    directed_arcs = {
        ("a0", "v0"),
        ("a1", "v1"),
        ("v0", "v1"),
        ("v0", "p0"),
        ("v1", "p1"),
    }

    def reachable(start: str, target: str) -> bool:
        seen = {start}
        frontier = [start]
        while frontier:
            vertex = frontier.pop()
            for left, right in directed_arcs:
                if left == vertex and right not in seen:
                    seen.add(right)
                    frontier.append(right)
        return target in seen

    assert reachable("a0", "p0")
    assert reachable("a0", "p1")
    assert reachable("a1", "p1")
    assert not reachable("a1", "p0")

    print("boundary delta-matroid and permanental response theorem: PASS")
    print("fixed symbolic identities only; no support-family enumeration")


if __name__ == "__main__":
    main()
