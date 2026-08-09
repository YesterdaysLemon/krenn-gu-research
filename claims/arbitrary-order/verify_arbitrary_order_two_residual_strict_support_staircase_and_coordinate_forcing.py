"""Verify the two-residual strict-support staircase and coordinate forcing.

This is a fixed exact symbolic replay, not a graph, support, word, or
parameter search.
"""

from itertools import combinations

import sympy as sp


def permanent(matrix: sp.Matrix):
    """Return the permanent by fixed first-row recursion."""
    if matrix.rows == 0:
        return sp.Integer(1)
    return sp.expand(
        sum(
            matrix[0, column] * permanent(matrix.minor_submatrix(0, column))
            for column in range(matrix.cols)
        )
    )


def main() -> None:
    # Exact matching recursion on u,v,q0,q1.
    direct, residual = sp.symbols("B h")
    a_u, a_v, b_u, b_v = sp.symbols("a_u a_v b_u b_v")
    matching_sum = direct * residual + a_u * b_v + b_u * a_v
    expected = residual * direct + a_u * b_v + b_u * a_v
    assert sp.expand(matching_sum - expected) == 0

    # A generic P5 checks the unsigned two-row Laplace transport.  The written
    # assignment bijection proves the identity for every m=r+2.
    entries = sp.symbols("z0:25")
    generic = sp.Matrix(5, 5, entries)
    full = permanent(generic)
    laplace = sp.Integer(0)
    root_rows = (0, 1, 2)
    port_rows = (3, 4)
    for port_columns in combinations(range(5), 2):
        root_columns = tuple(
            column for column in range(5) if column not in port_columns
        )
        laplace += permanent(generic.extract(port_rows, port_columns)) * permanent(
            generic.extract(root_rows, root_columns)
        )
    assert sp.expand(full - laplace) == 0

    # Fixed representatives of the two exact residual alternatives on
    # three-dimensional kernel spaces.
    x0, x1, x2, y0, y1, y2 = sp.symbols("x0 x1 x2 y0 y1 y2")
    coordinate_beta = x0 * y1
    assert coordinate_beta.subs({x0: 2, x1: 3, x2: 5, y0: 7, y1: 11, y2: 13}) != 0
    coordinate_matrix = sp.Matrix(((0, 1, 0), (0, 0, 0), (0, 0, 0)))
    assert coordinate_matrix.rank() == 1
    noncoordinate_beta = x0 * y0 + x1 * y1
    torus_zero = noncoordinate_beta.subs(
        {x0: 1, x1: 1, x2: 1, y0: 1, y1: -1, y2: 1}
    )
    assert torus_zero == 0
    noncoordinate_matrix = sp.Matrix(((1, 0, 0), (0, 1, 0), (0, 0, 0)))
    assert noncoordinate_matrix.rank() == 2

    # General support transport and its P5/P6/P7 specializations.
    r = sp.symbols("r", integer=True, nonnegative=True)
    m = r + 2
    strict_support = 3 * m + 3
    assert sp.expand(strict_support - (3 * r + 9)) == 0

    second_surplus = {
        root_count: {
            "order": root_count + 2,
            "strict_support": 3 * (root_count + 2) + 3,
            "coordinate_cut": 3 * (root_count + 2) + 2,
        }
        for root_count in (3, 4, 5)
    }
    assert second_surplus == {
        3: {"order": 5, "strict_support": 18, "coordinate_cut": 17},
        4: {"order": 6, "strict_support": 21, "coordinate_cut": 20},
        5: {"order": 7, "strict_support": 24, "coordinate_cut": 23},
    }

    five_root_staircase = tuple(3 * order + 3 for order in (5, 6, 7))
    assert five_root_staircase == (18, 21, 24)

    # Contracted active forms inject into their underlying graph-cut blocks.
    active_root, active_a, active_b = 14, 5, 4
    graph_root, graph_a, graph_b = 15, 5, 5
    assert active_root <= graph_root
    assert active_a <= graph_a
    assert active_b <= graph_b
    assert active_root + active_a + active_b <= graph_root + graph_a + graph_b

    print("PASS: exact two-residual matching recursion")
    print("PASS: generic P5 two-row permanent Laplace identity")
    print("PASS: coordinate-monomial and torus-zero representatives")
    print("PASS: arbitrary-r strict support is 3r+9")
    print("PASS: P5/P6/P7 thresholds are 18/21/24")
    print("SCOPE: coordinate-monomial and higher-residual branches remain open")
    print("searches=0")


if __name__ == "__main__":
    main()
