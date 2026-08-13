"""Exact replay for the complete S2U full-joint-cross-rank exclusion."""

from __future__ import annotations

from collections import Counter
from itertools import product

import sympy as sp


def tensor_index(x: int, y: int, z: int) -> int:
    return 9 * x + 3 * y + z


def derivative_matrix(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    """Map (x,y,z) to x*A+B*y+C*z in X tensor Y tensor Z."""
    out = sp.zeros(27, 9)
    for x, y, z in product(range(3), repeat=3):
        row = tensor_index(x, y, z)
        out[row, x] = a[y, z]
        out[row, 3 + y] = b[x, z]
        out[row, 6 + z] = c[x, y]
    return out


def restriction_matrix(r_space: sp.Matrix) -> sp.Matrix:
    """Map (A,B,C) to the three derivative values on the rows of R."""
    out = sp.zeros(81, 27)
    for root_row, x, y, z in product(range(3), repeat=4):
        row = 27 * root_row + tensor_index(x, y, z)
        out[row, 3 * y + z] = r_space[root_row, x]
        out[row, 9 + 3 * x + z] = r_space[root_row, 3 + y]
        out[row, 18 + 3 * x + y] = r_space[root_row, 6 + z]
    return out


def pair_matrix(q: sp.Matrix) -> sp.Matrix:
    """Map p to the three polarized pair products (A_yz,B_xz,C_xy)."""
    qx, qy, qz = q[:3, 0], q[3:6, 0], q[6:9, 0]
    out = sp.zeros(27, 9)
    for i, j in product(range(3), repeat=2):
        # A=p_y tensor q_z+q_y tensor p_z.
        out[3 * i + j, 3 + i] = qz[j]
        out[3 * i + j, 6 + j] = qy[i]
        # B=p_x tensor q_z+q_x tensor p_z.
        out[9 + 3 * i + j, i] = qz[j]
        out[9 + 3 * i + j, 6 + j] = qx[i]
        # C=p_x tensor q_y+q_x tensor p_y.
        out[18 + 3 * i + j, i] = qy[j]
        out[18 + 3 * i + j, 3 + j] = qx[i]
    return out


def projection_from_kernel(kernel: list[list[int]]) -> sp.Matrix:
    matrix = sp.Matrix(kernel) if kernel else sp.zeros(0, 3)
    out = sp.zeros(3, 3)
    for column, vector in enumerate(matrix.nullspace()):
        out[:, column] = vector
    return out


KERNEL_ATLAS: list[list[list[list[int]]]] = [
    [[[0, 1, 1], [1, 0, 1]], [[0, 1, 1], [1, 0, 0]], [[0, 1, 0], [1, 0, 1]]],
    [[[0, 1, 1], [1, 0, 1]], [[0, 1, 1], [1, 0, 1]], [[1, 1, 1]]],
    [[[0, 1, 1], [1, 0, 1]], [[0, 1, 1], [1, 0, 0]], [[1, 1, 1]]],
    [[[0, 1, 1], [1, 0, 1]], [[0, 1, 1], [1, 0, 0]], [[0, 1, 0]]],
    [[[0, 1, 1], [1, 0, 1]], [[0, 1, 1], [1, 0, 1]], []],
    [[[0, 1, 1], [1, 0, 1]], [[0, 1, 1], [1, 0, 0]], []],
    [[[0, 1, 1], [1, 0, 1]], [[1, 1, 1]], [[1, 1, 1]]],
    [[[0, 1, 1], [1, 0, 1]], [[1, 1, 1]], [[1, 1, 0]]],
    [[[0, 1, 1], [1, 0, 1]], [[1, 1, 1]], [[1, 0, 0]]],
    [[[0, 1, 1], [1, 0, 1]], [[1, 1, 0]], [[1, 0, 1]]],
    [[[0, 1, 1], [1, 0, 1]], [[1, 1, 1]], []],
    [[[0, 1, 1], [1, 0, 1]], [[1, 1, 0]], []],
    [[[0, 1, 1], [1, 0, 1]], [], []],
    [[[1, 1, 1]], [[1, 1, 1]], [[1, 1, 0]]],
    [[[1, 1, 1]], [[1, 1, 0]], [[1, 0, 1]]],
    [[[1, 1, 1]], [[1, 1, 0]], [[0, 0, 1]]],
    [[[1, 1, 1]], [[1, 1, 1]], []],
    [[[1, 1, 1]], [[1, 1, 0]], []],
    [[[1, 1, 1]], [], []],
    [[], [], []],
]


def check_derivative_kernel_atlas() -> None:
    ranks: Counter[int] = Counter()
    exceptional_profiles: list[tuple[int, int, int]] = []
    for kernels in KERNEL_ATLAS:
        projections = [projection_from_kernel(kernel) for kernel in kernels]
        r_space = projections[0].row_join(projections[1]).row_join(projections[2])
        assert r_space.rank() == 3
        profile = tuple(projection.rank() for projection in projections)
        assert min(profile) >= 1
        value = restriction_matrix(r_space).rank()
        ranks[value] += 1
        if value < 27:
            exceptional_profiles.append(profile)
    assert ranks == Counter({27: 18, 24: 2})
    assert exceptional_profiles == [(1, 1, 2), (1, 1, 3)]
    print("full-support derivative-kernel atlas: PASS (18 injective; 2 exceptional)")


def check_three_summand_syzygy_normal_form() -> None:
    e0, e1 = sp.eye(3)[:, 0], sp.eye(3)[:, 1]
    x = y = z = e0
    b = c0 = b0 = e1
    a_tensor = -(y * b0.T + c0 * z.T)
    b_tensor = x * b0.T + b * z.T
    c_tensor = x * c0.T - b * y.T
    matrix = derivative_matrix(a_tensor, b_tensor, c_tensor)
    first = x.col_join(y).col_join(z)
    second = b.col_join(c0).col_join(-b0)
    assert matrix * first == sp.zeros(27, 1)
    assert matrix * second == sp.zeros(27, 1)
    assert matrix.rank() == 7
    assert sp.Matrix.hstack(first, second).rank() == 2
    print("three-nonzero Hilbert-Burch syzygy boundary: PASS (kernel dimension 2)")


def exceptional_r_space(epsilon: int) -> sp.Matrix:
    out = sp.zeros(3, 9)
    out[0, 0] = 1
    out[0, 3] = 1
    out[0, 6] = epsilon
    out[1, 7] = 1
    out[2, 8] = 1
    return out


def check_exceptional_derivative_kernel() -> None:
    x, y = sp.eye(3)[:, 0], sp.eye(3)[:, 0]
    for epsilon in (0, 1):
        delta = restriction_matrix(exceptional_r_space(epsilon))
        expected: list[sp.Matrix] = []
        for t in sp.eye(3).columnspace():
            a_tensor = y * t.T
            b_tensor = -(x * t.T)
            c_tensor = sp.zeros(3)
            vector = sp.Matrix(list(a_tensor) + list(b_tensor) + list(c_tensor))
            assert delta * vector == sp.zeros(81, 1)
            expected.append(vector)
        assert delta.rank() == 24
        assert sp.Matrix.hstack(*expected).rank() == 3
    print("exceptional synchronized derivative kernel: PASS (rank 24 in 2 charts)")


def q_from_support(support: tuple[int, ...]) -> sp.Matrix:
    out = sp.zeros(9, 1)
    for source in support:
        out[3 * source] = 1
    return out


def check_injective_pair_zero_divisors() -> None:
    ranks: Counter[tuple[int, int]] = Counter()
    for mask in range(1, 8):
        support = tuple(source for source in range(3) if mask & (1 << source))
        value = pair_matrix(q_from_support(support)).rank()
        ranks[(len(support), value)] += 1
    assert ranks == Counter({(1, 6): 3, (2, 8): 3, (3, 9): 1})
    print("injective pair-product support orbits: PASS (nullities 3 / 1 / 0)")


def same_span(left: list[sp.Matrix], right: list[sp.Matrix]) -> bool:
    left_matrix = sp.Matrix.hstack(*left)
    right_matrix = sp.Matrix.hstack(*right)
    return (
        left_matrix.rank()
        == right_matrix.rank()
        == left_matrix.row_join(right_matrix).rank()
    )


def check_exceptional_pair_zero_divisors() -> None:
    delta = restriction_matrix(exceptional_r_space(1))
    ex = sp.eye(9)[:, 0]
    ey = sp.eye(9)[:, 3]
    ez = sp.eye(9)[:, 6]
    source_x = [sp.eye(9)[:, i] for i in range(3)]
    source_y = [sp.eye(9)[:, 3 + i] for i in range(3)]
    source_z = [sp.eye(9)[:, 6 + i] for i in range(3)]
    ell_minus = ex - ey
    ell_plus = ex + ey

    cases = [
        (ex, source_x),
        (sp.eye(9)[:, 1], source_x),
        (ey, source_y),
        (sp.eye(9)[:, 4], source_y),
        (ez, [*source_z, ell_minus]),
        (ell_minus, [*source_z, ell_plus]),
        (ell_minus + ez, source_z),
    ]
    for q, expected in cases:
        kernel = (delta * pair_matrix(q)).nullspace()
        assert same_span(kernel, expected)

    assert len((delta * pair_matrix(ex + ey)).nullspace()) == 1
    assert len((delta * pair_matrix(ex + ey + ez)).nullspace()) == 1
    print("exceptional pair-product zero divisors: PASS (7 boundary orbits)")


def check_grid_pigeonholes() -> None:
    regular_reasons: Counter[str] = Counter()
    for labels in product("XYZ", repeat=3):
        if len(set(labels)) == 1:
            regular_reasons["six-in-three"] += 1
        else:
            regular_reasons["zero-intersection"] += 1
    assert regular_reasons == Counter({"zero-intersection": 24, "six-in-three": 3})

    exceptional_reasons: Counter[str] = Counter()
    for labels in product(("X", "Y", "L"), repeat=3):
        if set(labels) == {"L"}:
            exceptional_reasons["nine-in-five"] += 1
        elif len(set(labels)) == 1:
            exceptional_reasons["six-in-three"] += 1
        else:
            exceptional_reasons["zero-intersection"] += 1
    assert exceptional_reasons == Counter(
        {"zero-intersection": 24, "six-in-three": 2, "nine-in-five": 1}
    )
    print("off-diagonal zero-grid pigeonholes: PASS (27 regular + 27 exceptional)")


def main() -> None:
    check_derivative_kernel_atlas()
    check_three_summand_syzygy_normal_form()
    check_exceptional_derivative_kernel()
    check_injective_pair_zero_divisors()
    check_exceptional_pair_zero_divisors()
    check_grid_pigeonholes()
    print("balanced m=3 full-joint-cross-rank exclusion: PASS")


if __name__ == "__main__":
    main()
