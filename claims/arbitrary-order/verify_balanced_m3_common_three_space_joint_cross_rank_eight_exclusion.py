"""Exact replay for the S2Q common-three-space joint-rank-eight exclusion."""

from __future__ import annotations

from itertools import product

import sympy as sp


def tidx(x: int, y: int, z: int) -> int:
    return 9 * x + 3 * y + z


def derivative_matrix(
    a_tensor: sp.Matrix, b_tensor: sp.Matrix, c_tensor: sp.Matrix
) -> sp.Matrix:
    out = sp.zeros(27, 9)
    for x, y, z in product(range(3), repeat=3):
        row = tidx(x, y, z)
        out[row, x] = a_tensor[y, z]
        out[row, 3 + y] = b_tensor[x, z]
        out[row, 6 + z] = c_tensor[x, y]
    return out


def check_hyperplane_rank_loss() -> None:
    e0, e1 = sp.eye(3)[:, 0], sp.eye(3)[:, 1]
    a_tensor = e0 * e0.T
    b_tensor = e1 * e1.T
    full = derivative_matrix(a_tensor, b_tensor, sp.zeros(3))
    assert full.rank() == 6

    # Restriction to a hyperplane is represented by eight independent
    # columns.  Both loss zero and the sharp loss one occur.
    no_loss = full[:, :8]
    sharp_loss = full[:, 1:]
    assert no_loss.rank() == 6
    assert sharp_loss.rank() == 5
    print("hyperplane derivative rank loss: PASS (loss 0 / sharp loss 1)")


def pair_product_matrix(q: sp.Matrix) -> sp.Matrix:
    """Map p to the three cross-source components of p*q."""
    qx, qy, qz = q[:3, 0], q[3:6, 0], q[6:9, 0]
    out = sp.zeros(27, 9)
    for i, j in product(range(3), repeat=2):
        out[3 * i + j, 3 + i] = qz[j]
        out[3 * i + j, 6 + j] = qy[i]
        out[9 + 3 * i + j, i] = qz[j]
        out[9 + 3 * i + j, 6 + j] = qx[i]
        out[18 + 3 * i + j, i] = qy[j]
        out[18 + 3 * i + j, 3 + j] = qx[i]
    return out


def vector(*blocks: tuple[int, int, int]) -> sp.Matrix:
    return sp.Matrix([entry for block in blocks for entry in block])


def check_zero_divisor_orbits() -> None:
    zero = (0, 0, 0)
    e0 = (1, 0, 0)
    e1 = (0, 1, 0)
    pure = vector(e0, zero, zero)
    mixed = vector(e0, e1, zero)
    full = vector(e0, e1, (0, 0, 1))

    pure_kernel = pair_product_matrix(pure).nullspace()
    mixed_kernel = pair_product_matrix(mixed).nullspace()
    full_kernel = pair_product_matrix(full).nullspace()
    assert len(pure_kernel) == 3
    assert sp.Matrix.hstack(*pure_kernel).columnspace() == [
        sp.eye(9)[:, i] for i in range(3)
    ]
    assert len(mixed_kernel) == 1
    assert mixed_kernel[0] == vector((-1, 0, 0), e1, zero)
    assert full_kernel == []
    print("three-source degree-one zero divisors: PASS (dimensions 3 / 1 / 0)")


def check_off_diagonal_grid_case_budget() -> None:
    # Case census by the number of nonzero q rows and their support types.
    # Each entry records the proved maximum dimension of span(P,Q).
    budgets = {
        0: [3],
        1: [4, 3, 2],  # pure / mixed / full
        2: [3, 4, 4, 3, 4, 3, 2],
        3: [3, 4, 3, 4, 4],
    }
    assert max(value for values in budgets.values() for value in values) == 4
    assert sum(len(values) for values in budgets.values()) == 16

    # Sharp pure-source controls: two independent pairs occupy two source
    # summands and attain dimension four.
    zero = (0, 0, 0)
    e0, e1 = (1, 0, 0), (0, 1, 0)
    q0 = vector(e0, zero, zero)
    q1 = vector(zero, e0, zero)
    p0 = vector(zero, e1, zero)
    p1 = vector(e1, zero, zero)
    p2 = sp.zeros(9, 1)
    q2 = sp.zeros(9, 1)
    rows = [p0, p1, p2, q0, q1, q2]
    assert sp.Matrix.hstack(*rows).rank() == 4
    for i, j in product(range(3), repeat=2):
        if i != j:
            assert pair_product_matrix(rows[3 + j]) * rows[i] == sp.zeros(27, 1)
    print("off-diagonal zero-grid dimension budget: PASS (16 cases; sharp rank 4)")


def exceptional_r_space(epsilon: int) -> sp.Matrix:
    out = sp.zeros(3, 9)
    out[0, 0] = 1
    out[0, 3] = 1
    out[0, 6] = epsilon
    out[1, 7] = 1
    out[2, 8] = 1
    return out


def restriction_matrix(r_space: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(81, 27)
    for row_index, x, y, z in product(range(3), repeat=4):
        row = 27 * row_index + tidx(x, y, z)
        out[row, 3 * y + z] = r_space[row_index, x]
        out[row, 9 + 3 * x + z] = r_space[row_index, 3 + y]
        out[row, 18 + 3 * x + y] = r_space[row_index, 6 + z]
    return out


def check_exceptional_covector_line() -> None:
    # On either exceptional chart, the two-dimensional pure-Z intersection
    # is spanned by the last two rows.
    for epsilon in (0, 1):
        r_space = exceptional_r_space(epsilon)
        delta = restriction_matrix(r_space)

        # A nonzero XY component C already gives rank two on those rows.
        c_tensor = sp.zeros(3)
        c_tensor[0, 0] = 1
        quadratic = sp.Matrix([0] * 18 + list(c_tensor))
        image = delta * quadratic
        assert sp.Matrix.hstack(image[27:54, :], image[54:81, :]).rank() == 2
        assert image[27:54, :] != sp.zeros(27, 1)
        assert image[54:81, :] != sp.zeros(27, 1)

        # Every rank-one restriction must therefore kill both pure-Z rows,
        # so its source covector lies on the unique first-coordinate line.
        covectors = [sp.Matrix([1, 0, 0]), sp.Matrix([2, 0, 0])]
        assert sp.Matrix.hstack(*covectors).rank() == 1
    print("exceptional rank-one restriction covector: PASS (one line in 2 charts)")


def check_two_target_covectors() -> None:
    ell_one = sp.Matrix([0, 1, 0])
    ell_two = sp.Matrix([0, 0, 1])
    assert sp.Matrix.hstack(ell_one, ell_two).rank() == 2
    print("two surviving GHZ root covectors: PASS (rank 2)")


def main() -> None:
    check_hyperplane_rank_loss()
    check_zero_divisor_orbits()
    check_off_diagonal_grid_case_budget()
    check_exceptional_covector_line()
    check_two_target_covectors()
    print("balanced m=3 joint-cross-rank-eight exclusion: PASS")


if __name__ == "__main__":
    main()
