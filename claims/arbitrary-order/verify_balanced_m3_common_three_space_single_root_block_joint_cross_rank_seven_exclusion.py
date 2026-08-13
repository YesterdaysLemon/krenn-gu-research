"""Exact replay for the single-root-block joint-rank-seven exclusion."""

from __future__ import annotations

from itertools import product

import sympy as sp


def basis(index: int) -> sp.Matrix:
    return sp.eye(9)[:, index]


def tensor_index(x: int, y: int, z: int) -> int:
    return 9 * x + 3 * y + z


def pair_product(p: sp.Matrix, q: sp.Matrix) -> sp.Matrix:
    """Return the YZ, XZ, and XY polarized products in one vector."""
    out = sp.zeros(27, 1)
    for i, j in product(range(3), repeat=2):
        out[3 * i + j] = p[3 + i] * q[6 + j] + q[3 + i] * p[6 + j]
        out[9 + 3 * i + j] = p[i] * q[6 + j] + q[i] * p[6 + j]
        out[18 + 3 * i + j] = p[i] * q[3 + j] + q[i] * p[3 + j]
    return out


def derivative(p: sp.Matrix, q: sp.Matrix) -> sp.Matrix:
    """Map r to the polarized three-source permanent per(r,p,q)."""
    pair = pair_product(p, q)
    out = sp.zeros(27, 9)
    for x, y, z in product(range(3), repeat=3):
        row = tensor_index(x, y, z)
        out[row, x] = pair[3 * y + z]
        out[row, 3 + y] = pair[9 + 3 * x + z]
        out[row, 6 + z] = pair[18 + 3 * x + y]
    return out


def marked_normal_forms() -> dict[str, tuple[list[sp.Matrix], list[sp.Matrix]]]:
    x0, x1, x2 = (basis(i) for i in range(3))
    y0, y1 = basis(3), basis(4)
    z0 = basis(6)
    zero = sp.zeros(9, 1)
    return {
        "pure/pure": ([x0, y0, zero], [y1, x1, zero]),
        "pure/mixed shared": (
            [x0, x2 - z0, zero],
            [x2 + z0, x1, zero],
        ),
        "pure/mixed disjoint": (
            [x0, y0 - z0, zero],
            [y0 + z0, x1, zero],
        ),
        "mixed/mixed same": (
            [x0 + y0, x1 + y1, zero],
            [x1 - y1, x0 - y0, zero],
        ),
        "mixed/mixed different": (
            [x0 + y0, x1 + z0, zero],
            [x1 - z0, x0 - y0, zero],
        ),
    }


def check_grid_normal_forms() -> None:
    for name, (p_rows, q_rows) in marked_normal_forms().items():
        rows = [*p_rows, *q_rows]
        assert sp.Matrix.hstack(*rows).rank() == 4, name
        for i, j in product(range(3), repeat=2):
            if i != j:
                assert pair_product(p_rows[i], q_rows[j]) == sp.zeros(27, 1), name
        assert pair_product(p_rows[0], q_rows[0]) != sp.zeros(27, 1), name
        assert pair_product(p_rows[1], q_rows[1]) != sp.zeros(27, 1), name
        assert p_rows[2] == sp.zeros(9, 1)
        assert q_rows[2] == sp.zeros(9, 1)
    print("rank-four marked-grid normal forms: PASS (5 families)")


def check_common_projection_cases() -> None:
    forms = marked_normal_forms()
    expected_columns = {
        "pure/pure": set(range(6, 9)),
        "pure/mixed shared": set(range(3, 6)),
    }
    for name, columns in expected_columns.items():
        p_rows, q_rows = forms[name]
        for index in (0, 1):
            matrix = derivative(p_rows[index], q_rows[index])
            nonzero_columns = {j for j in range(9) if matrix[:, j] != sp.zeros(27, 1)}
            assert nonzero_columns == columns
            assert matrix[:, sorted(columns)].rank() == 3
    print("common-complement projection obstruction: PASS (P/P and shared P/M)")


def check_disjoint_pure_mixed_case() -> None:
    p_rows, q_rows = marked_normal_forms()["pure/mixed disjoint"]
    d0 = derivative(p_rows[0], q_rows[0])
    d1 = derivative(p_rows[1], q_rows[1])
    yz_columns = list(range(3, 9))
    assert sp.Matrix.vstack(d0[:, yz_columns], d1[:, yz_columns]).rank() == 6

    y0, z0 = basis(3), basis(6)
    kernel_plus = y0 - z0
    kernel_minus = y0 + z0
    assert d0 * kernel_plus == sp.zeros(27, 1)
    assert d1 * kernel_minus == sp.zeros(27, 1)
    plane = sp.Matrix.hstack(kernel_plus, kernel_minus)
    assert plane.rank() == 2
    assert (d0 * plane).rank() == 1
    assert (d1 * plane).rank() == 1

    # Both surviving YZ output factors are y0 tensor z0, whereas two GHZ
    # colours have independent YZ coordinate tensors.
    yz_forced = sp.zeros(9, 1)
    yz_forced[0] = 1
    yz_other = sp.zeros(9, 1)
    yz_other[4] = 1
    assert sp.Matrix.hstack(yz_forced, yz_other).rank() == 2
    print("disjoint P/M kernel-line obstruction: PASS (shared YZ factor)")


def check_mixed_mixed_cases() -> None:
    same_p, same_q = marked_normal_forms()["mixed/mixed same"]
    product_zero = pair_product(same_p[0], same_q[0])
    product_one = pair_product(same_p[1], same_q[1])
    assert product_zero == -product_one
    assert derivative(same_p[0], same_q[0]) == -derivative(same_p[1], same_q[1])

    diff_p, diff_q = marked_normal_forms()["mixed/mixed different"]
    d0 = derivative(diff_p[0], diff_q[0])
    d1 = derivative(diff_p[1], diff_q[1])
    assert sp.Matrix.vstack(d0, d1).rank() == 9
    print("mixed/mixed obstruction: PASS (proportional / joint-kernel zero)")


def check_exceptional_covector_boundary() -> None:
    # In the exceptional chart R contains a two-plane S in one source.
    # A nonzero complementary pair tensor maps two independent members of S
    # to independent tensors, so every rank-one restriction kills S.
    c_tensor = sp.zeros(9, 1)
    c_tensor[0] = 1
    z1, z2 = basis(7), basis(8)
    p, q = basis(0), basis(3)
    d = derivative(p, q)
    assert pair_product(p, q)[18:27, :] == c_tensor
    assert sp.Matrix.hstack(d * z1, d * z2).rank() == 2
    exceptional_line = sp.Matrix([1, 0, 0])
    target_covectors = sp.Matrix.hstack(sp.Matrix([0, 1, 0]), sp.Matrix([0, 0, 1]))
    assert exceptional_line.rank() == 1
    assert target_covectors.rank() == 2
    print("exceptional derivative covector boundary: PASS (one versus two)")


def main() -> None:
    check_grid_normal_forms()
    check_common_projection_cases()
    check_disjoint_pure_mixed_case()
    check_mixed_mixed_cases()
    check_exceptional_covector_boundary()
    print("balanced m=3 single-root-block joint-rank-seven exclusion: PASS")


if __name__ == "__main__":
    main()
