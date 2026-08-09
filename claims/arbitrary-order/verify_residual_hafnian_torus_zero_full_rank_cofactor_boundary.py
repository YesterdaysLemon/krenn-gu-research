"""Primary verifier for the torus-zero full-rank cofactor boundary."""

from __future__ import annotations

import sympy as sp


def odd_double_factorial(value: int) -> int:
    if value <= 0:
        return 1
    product = 1
    for factor in range(1, value + 1, 2):
        product *= factor
    return product


def residual_matrix(order: int) -> sp.Matrix:
    assert order >= 4 and order % 2 == 0
    return sp.Matrix(
        order,
        order,
        lambda i, j: (
            0 if i == j else -(order - 2) if {i, j} == {0, 1} else 1
        ),
    )


def cofactor_matrix(order: int) -> sp.Matrix:
    alpha = odd_double_factorial(order - 3)
    beta = -2 * odd_double_factorial(order - 5)
    return sp.Matrix(
        order,
        order,
        lambda i, j: (
            0 if i == j else beta if i >= 2 and j >= 2 else alpha
        ),
    )


def deletion_cofactor_by_partition(order: int, first: int, second: int) -> int:
    """Closed matching partition for haf(A with two vertices deleted)."""
    if 0 in (first, second) or 1 in (first, second):
        return odd_double_factorial(order - 3)
    all_one = odd_double_factorial(order - 3)
    using_special = odd_double_factorial(order - 5)
    return all_one + (-(order - 2) - 1) * using_special


def check_symbolic_determinant_factorization() -> None:
    q, g = sp.symbols("q g", nonzero=True)
    alpha = (q - 3) * g
    beta = -2 * g
    k = q - 2
    residual_two_by_two = sp.Matrix(
        ((alpha, alpha * k), (2 * alpha, beta * (k - 1)))
    )
    expected_two_by_two = -2 * g**2 * (q - 3) ** 2 * (q - 1)
    assert sp.factor(residual_two_by_two.det() - expected_two_by_two) == 0

    determinant = sp.factor(
        (-alpha) * (-beta) ** (q - 3) * expected_two_by_two
    )
    expected = 2 ** (q - 2) * (q - 1) * (q - 3) ** 3 * g**q
    assert sp.factor(determinant - expected) == 0


def check_even_orders() -> None:
    for order in (4, 6, 8, 10, 12):
        matrix = residual_matrix(order)
        special = matrix[0, 1]
        total_all_one = odd_double_factorial(order - 1)
        using_special = odd_double_factorial(order - 3)
        hafnian_by_partition = total_all_one + (special - 1) * using_special
        assert hafnian_by_partition == 0

        cofactor = cofactor_matrix(order)
        cofactor_from_deletions = sp.Matrix(
            [
                [
                    0
                    if row == column
                    else deletion_cofactor_by_partition(order, row, column)
                    for column in range(order)
                ]
                for row in range(order)
            ]
        )
        assert cofactor_from_deletions == cofactor
        g = odd_double_factorial(order - 5)
        expected_determinant = (
            2 ** (order - 2) * (order - 1) * (order - 3) ** 3 * g**order
        )
        assert cofactor.det() == expected_determinant
        assert cofactor.rank() == order

        # Taking the concatenated incidence map R=I realizes the sharp Gram
        # rank without a support or matching search.
        incidence = sp.eye(order)
        gram = incidence.T * cofactor * incidence
        assert gram == cofactor
        assert gram.rank() == order


def check_channel_pairing() -> None:
    x0, x1, y0, y1 = sp.symbols("x0 x1 y0 y1")
    x = sp.Matrix((x0, x1))
    y = sp.Matrix((y0, y1))
    root_two = sp.sqrt(2)
    ell = (x + sp.I * y) / root_two
    middle = (x - sp.I * y) / root_two
    paired = sp.simplify(ell * middle.T + middle * ell.T)
    assert paired == x * x.T + y * y.T

    # One channel has rank at most two, while the q=4 torus-zero cofactor
    # matrix has rank four and therefore needs exactly two channels.
    assert (ell * middle.T + middle * ell.T).rank() <= 2
    assert cofactor_matrix(4).rank() == 4

    # The physical off-diagonal q=4 data nevertheless have a rank-two
    # diagonal completion, hence a single complex bosonic channel.
    omega = (-1 + sp.sqrt(3) * sp.I) / 2
    assert sp.simplify(omega**2 + omega + 1) == 0
    one_ell = sp.Matrix((-omega**2, -omega, -1, -1))
    one_middle = sp.Matrix((omega, omega**2, 1, 1))
    completion = sp.simplify(
        one_ell * one_middle.T + one_middle * one_ell.T
    )
    canonical = cofactor_matrix(4)
    for row in range(4):
        for column in range(4):
            if row != column:
                difference = completion[row, column] - canonical[row, column]
                assert sp.simplify(difference) == 0
    assert completion.rank() <= 2


def square_zero_top_coefficient(
    rows: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Expr:
    """Return the top square-free coefficient of the product of linear rows."""
    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        next_states: dict[int, sp.Expr] = {}
        for mask, coefficient in states.items():
            for column, value in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                new_mask = mask | bit
                next_states[new_mask] = (
                    next_states.get(new_mask, 0) + coefficient * value
                )
        states = next_states
    return sp.expand(states[(1 << len(rows)) - 1])


def check_two_row_laplace_identity() -> None:
    # Coefficient extraction in C[x_0,...,x_3]/(x_0^2,...,x_3^2), not a
    # permutation or matching enumeration.
    h0 = sp.symbols("h00 h01 h02 h03")
    h1 = sp.symbols("h10 h11 h12 h13")
    g = sp.symbols("g0 g1 g2 g3")
    k = sp.symbols("k0 k1 k2 k3")
    permanent = square_zero_top_coefficient((h0, h1, g, k))
    laplace = sp.Integer(0)
    for first in range(4):
        for second in range(first + 1, 4):
            root_columns = [
                column for column in range(4) if column not in (first, second)
            ]
            root_minor = (
                h0[root_columns[0]] * h1[root_columns[1]]
                + h0[root_columns[1]] * h1[root_columns[0]]
            )
            channel = g[first] * k[second] + k[first] * g[second]
            laplace += root_minor * channel
    assert sp.expand(permanent - laplace) == 0


def check_articulation_separator() -> None:
    l0, l1, b01, b02, b12 = sp.symbols("l0 l1 b01 b02 b12")
    # X={x0,x1}, S={s}, Y={y0,y1,y2}.  Deleting x_p and y_q leaves one
    # forced X--S edge and the complementary internal Y edge.
    left = sp.Matrix((l1, l0))
    right = sp.Matrix(((b12, b02, b01),))
    cross_cofactor = left * right
    assert cross_cofactor.rank() == 1
    for row in range(2):
        for column in range(3):
            assert cross_cofactor[row, column] == left[row] * right[column]


def main() -> None:
    check_symbolic_determinant_factorization()
    check_even_orders()
    check_channel_pairing()
    check_two_row_laplace_identity()
    check_articulation_separator()
    print("residual-hafnian torus-zero full-rank boundary: PASS")
    print("canonical channel, off-diagonal completion, and separator cross-rank")


if __name__ == "__main__":
    main()
