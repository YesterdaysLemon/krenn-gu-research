"""Primary symbolic replay for the P7 deletion-cube observability boundary."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def permanent_dp(matrix: sp.Matrix) -> sp.Expr:
    """Permanent by square-free subset recursion, not permutation search."""
    rows, cols = matrix.shape
    assert rows == cols
    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for i in range(rows):
        nxt: dict[int, sp.Expr] = {}
        for mask, value in states.items():
            for j in range(cols):
                if mask & (1 << j) == 0:
                    new_mask = mask | (1 << j)
                    nxt[new_mask] = nxt.get(new_mask, 0) + value * matrix[i, j]
        states = nxt
    return sp.expand(states[(1 << cols) - 1])


def minor(matrix: sp.Matrix, rows: tuple[int, ...], cols: tuple[int, ...]) -> sp.Matrix:
    return sp.Matrix([[matrix[i, j] for j in cols] for i in rows])


def check_marked_laplace_identity() -> None:
    symbols = sp.symbols("h0:25")
    matrix = sp.Matrix(5, 5, symbols)
    full = permanent_dp(matrix)
    total = sp.Integer(0)
    all_rows = tuple(range(5))
    all_cols = tuple(range(5))
    marked = 0
    for rows in combinations(all_rows, 3):
        row_complement = tuple(i for i in all_rows if i not in rows)
        for cols in combinations(all_cols, 3):
            if marked not in cols:
                continue
            col_complement = tuple(j for j in all_cols if j not in cols)
            total += permanent_dp(minor(matrix, rows, cols)) * permanent_dp(
                minor(matrix, row_complement, col_complement)
            )
    assert sp.Poly(sp.expand(total - 6 * full), *symbols).is_zero


def check_observation_kernels() -> None:
    mu = sp.symbols("mu", nonzero=True)
    one_channel = sp.Matrix([[1, mu]])
    invisible = sp.Matrix([mu, -1])
    assert one_channel * invisible == sp.zeros(1, 1)
    assert one_channel.rank() == 1

    two_channels = sp.eye(2)
    assert two_channels.rank() == 2
    assert two_channels.inv() == sp.eye(2)

    overlay = sp.Matrix(
        [
            [1, 1, 1, 0, 0, 0],
            [1, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 1],
        ]
    )
    s, t = sp.symbols("s t")
    hidden = sp.Matrix([-s - t, s, t, t, s, -s - t])
    assert overlay.rank() == 4
    assert overlay * hidden == sp.zeros(4, 1)


def multiply_square_zero(
    left: dict[frozenset[int], sp.Expr],
    right: dict[frozenset[int], sp.Expr],
) -> dict[frozenset[int], sp.Expr]:
    out: dict[frozenset[int], sp.Expr] = {}
    for support_left, coeff_left in left.items():
        for support_right, coeff_right in right.items():
            if support_left & support_right:
                continue
            support = support_left | support_right
            out[support] = sp.expand(
                out.get(support, 0) + coeff_left * coeff_right
            )
    return {support: coeff for support, coeff in out.items() if coeff != 0}


def check_top_face_fibre() -> None:
    a = sp.symbols("a", nonzero=True)
    empty = frozenset()
    ports_12 = frozenset({1, 2})
    ports_34 = frozenset({3, 4})
    ports_1234 = frozenset({1, 2, 3, 4})
    moment = {empty: sp.Integer(1), ports_34: a}
    relative = {ports_12: 1 / a}
    response = multiply_square_zero(moment, relative)
    assert response == {ports_12: 1 / a, ports_1234: sp.Integer(1)}
    assert moment.get(ports_1234, 0) == 0
    assert response[ports_1234] == 1
    assert sp.diff(moment[ports_34], a) == 1
    assert sp.diff(response[ports_12], a) == -1 / a**2


def check_deletion_label_gap() -> None:
    roots = {f"r{i}" for i in range(5)}
    blockers = {f"b{i}" for i in range(7)}
    residuals = {"q0", "q1"}

    four_ports = {"b0", "b1", "b2", "b3"}
    six_ports = blockers - {"b6"}
    label_four = roots | (blockers - four_ports)
    label_six = roots | (blockers - six_ports)
    assert len(label_four & blockers) == 3
    assert len(label_six & blockers) == 1

    root_pair = {"r0", "r1"}
    known_labels = [root_pair, root_pair | residuals]
    assert all(not (label & blockers) for label in known_labels)
    assert label_four not in known_labels
    assert label_six not in known_labels


def check_double_blocker_kernels() -> None:
    # Any three root rows contained in a two-dimensional blocker row span
    # have a nonzero common kernel.  This representative symbolic matrix has
    # arbitrary rows in span(e0*,e1*) and kernel e2.
    alpha = sp.symbols("a0:3")
    beta = sp.symbols("b0:3")
    rows = sp.Matrix([[alpha[i], beta[i], 0] for i in range(3)])
    kernel_vector = sp.Matrix([0, 0, 1])
    assert rows * kernel_vector == sp.zeros(3, 1)
    assert rows.rank() <= 2


def main() -> None:
    check_marked_laplace_identity()
    check_observation_kernels()
    check_top_face_fibre()
    check_deletion_label_gap()
    check_double_blocker_kernels()
    print("PASS: generic marked 5x5 permanental Laplace identity")
    print("PASS: selector ranks and invisible cofactor deformations")
    print("PASS: exact one-parameter top-face response fibre")
    print("PASS: blocker-deletion label gap and double-blocker kernels")
    print("SCOPE: P7 cell and global Krenn-Gu conjecture remain UNRESOLVED")


if __name__ == "__main__":
    main()
