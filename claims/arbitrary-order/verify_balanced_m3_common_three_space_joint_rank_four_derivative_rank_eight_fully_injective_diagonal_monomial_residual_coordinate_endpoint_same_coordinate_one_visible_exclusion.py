#!/usr/bin/env python3
"""Exact symbolic replay for the same-coordinate one-visible exclusion.

The written theorem owns the coordinate-free S2CG zero-pair classification.
This replay checks its algebraic interfaces, the two S2CF corrected cubes,
the complete-face indices, and the recovered-source/unsliced quotient sign.
"""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp


def unit(size: int, index: int) -> sp.Matrix:
    value = sp.zeros(size, 1)
    value[index] = 1
    return value


def row(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    return x.col_join(y).col_join(z)


def blocks(value: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return value[:3, :], value[3:6, :], value[6:9, :]


def tensor3(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    value = sp.zeros(27, 1)
    for i, j, k in product(range(3), repeat=3):
        value[9 * i + 3 * j + k] = x[i] * y[j] * z[k]
    return value


def polarized(u: sp.Matrix, v: sp.Matrix, q: sp.Matrix) -> sp.Matrix:
    rows = (blocks(u), blocks(v), blocks(q))
    value = sp.zeros(27, 1)
    for sigma in permutations(range(3)):
        value += tensor3(
            rows[sigma[0]][0], rows[sigma[1]][1], rows[sigma[2]][2]
        )
    return sp.simplify(value)


def permutation_sign(sigma: tuple[int, ...]) -> int:
    inversions = sum(
        sigma[i] > sigma[j]
        for i in range(3)
        for j in range(i + 1, 3)
    )
    return -1 if inversions % 2 else 1


def alternating(rows: tuple[sp.Matrix, ...]) -> sp.Matrix:
    split = tuple(blocks(value) for value in rows)
    value = sp.zeros(27, 1)
    for sigma in permutations(range(3)):
        value += permutation_sign(sigma) * tensor3(
            split[sigma[0]][0],
            split[sigma[1]][1],
            split[sigma[2]][2],
        )
    return sp.simplify(value)


def quotient_indices(base_colour: int) -> tuple[int, ...]:
    return tuple(
        9 * i + 3 * j + k
        for i, j, k in product(range(3), repeat=3)
        if i != base_colour and j != base_colour and k != base_colour
    )


def quotient(value: sp.Matrix, base_colour: int) -> sp.Matrix:
    return sp.Matrix([value[index] for index in quotient_indices(base_colour)])


def check_corrected_cubes() -> None:
    # (shared coordinate, visible coordinate, the two perpendicular rows)
    for shared, visible, perpendicular in (
        (1, 0, (0, 2)),
        (0, 1, (1, 2)),
    ):
        assert shared != visible
        first, exceptional = perpendicular
        # Visible corner.
        visible_coefficients = tuple(
            (
                int(first == k) * int(first == k),
                int(first == 2) * int(first == 2),
            )
            for k in range(3)
        )
        assert visible_coefficients[visible] == (1, 0)
        assert all(
            coefficients == (0, 0)
            for k, coefficients in enumerate(visible_coefficients)
            if k != visible
        )
        # The two cross cells vanish on every q_k.
        for alpha, beta in ((first, exceptional), (exceptional, first)):
            for k in range(3):
                target = int(alpha == k) * int(beta == k)
                correction = int(alpha == 2) * int(beta == 2)
                assert (target, correction) == (0, 0)


def check_zero_pair_incidence_interfaces() -> None:
    e0, e1, _ = (unit(3, index) for index in range(3))
    zero = sp.zeros(3, 1)
    x = row(e0, zero, zero)
    x_prime = row(e1, zero, zero)
    y = row(zero, e0, zero)
    z = row(zero, zero, e0)
    generic = row(
        sp.Matrix(sp.symbols("qx0:3")),
        sp.Matrix(sp.symbols("qy0:3")),
        sp.Matrix(sp.symbols("qz0:3")),
    )

    # S2CG's conjugate and dependent square-zero interfaces.
    assert polarized(x + y, x - y, generic) == sp.zeros(27, 1)
    assert polarized(x, x, generic) == sp.zeros(27, 1)

    # Two distinct independent zero-pair planes span the three pure lines.
    a, d = x + y, x - y
    c, b = x + z, x - z
    assert polarized(a, d, generic) == sp.zeros(27, 1)
    assert polarized(c, b, generic) == sp.zeros(27, 1)
    assert sp.Matrix.hstack(a, c).rank() == 2
    assert sp.Matrix.hstack(b, d).rank() == 2
    assert sp.Matrix.hstack(a, d, c, b).rank() == 3
    assert polarized(a, b, x) != sp.zeros(27, 1)

    # Equal independent planes give R=P=span(x,y).
    c_equal, b_equal = x + 2 * y, x - 2 * y
    assert polarized(c_equal, b_equal, generic) == sp.zeros(27, 1)
    assert sp.Matrix.hstack(a, c_equal).rank() == 2
    assert sp.Matrix.hstack(b_equal, d).rank() == 2
    assert sp.Matrix.hstack(a, c_equal, b_equal, d).rank() == 2
    assert polarized(a, b_equal, z) != sp.zeros(27, 1)

    # One dependent pair supplies the omitted source; two dependent pairs
    # give the same split plane.  The remaining used-source fork has Alt=0.
    assert polarized(z, z, generic) == sp.zeros(27, 1)
    assert sp.Matrix.hstack(a, z, z, d).rank() == 3
    assert polarized(x, x, generic) == sp.zeros(27, 1)
    assert polarized(y, y, generic) == sp.zeros(27, 1)
    assert sp.Matrix.hstack(x, y, y, x).rank() == 2
    assert polarized(x, y, z) != sp.zeros(27, 1)
    assert alternating((x, y, x_prime)) == sp.zeros(27, 1)
    assert alternating((x, y, z)) == tensor3(e0, e0, e0)


def retained_face_value(i: int, j: int, k: int) -> int:
    assert k in (1, 2) and (i, j) != (2, 2)
    return int(i == j == k)


def check_complementary_recovered_face() -> None:
    # Exactly the eight cross-face entries used in the x=y=e1 proof vanish.
    used = tuple(
        (i, j, k)
        for k in (1, 2)
        for i, j in product(range(3), repeat=2)
        if (i == 1 and j in (0, 2)) or (j == 1 and i in (0, 2))
    )
    assert len(used) == 8
    assert all(retained_face_value(i, j, k) == 0 for i, j, k in used)
    assert retained_face_value(1, 1, 1) == 1

    # In split Q, q1 contains one base factor in every summand, so the triple
    # quotient kills M(r1,p1,q1), while it retains the transverse T1.
    symbols = sp.symbols("r0:9") + sp.symbols("p0:9")
    r = sp.Matrix(symbols[:9])
    p = sp.Matrix(symbols[9:])
    a, b, c = sp.symbols("a b c")
    e0, e1, _ = (unit(3, index) for index in range(3))
    zero = sp.zeros(3, 1)
    q = a * row(e0, zero, zero) + b * row(zero, e0, zero) + c * row(
        zero, zero, e0
    )
    assert quotient(polarized(r, p, q), 0) == sp.zeros(8, 1)
    t1 = tensor3(e1, e1, e1)
    assert quotient(t1, 0) != sp.zeros(8, 1)

    # In the equal split plane, choosing its two pure generators reads the
    # omitted-source component of the outside row without cancellation.
    rz = sp.Matrix(sp.symbols("rz0:3"))
    outside = row(sp.zeros(3, 1), sp.zeros(3, 1), rz)
    extracted = polarized(
        outside, row(e0, zero, zero), row(zero, e0, zero)
    )
    assert extracted == tensor3(e0, e0, rz)


def check_aligned_unsliced_quotient() -> None:
    lam = sp.symbols("lambda", nonzero=True)
    h0, h1, h2 = sp.symbols("h0 h1 h2")
    u0, u1, u2 = sp.symbols("u0 u1 u2")
    e0, e1, e2 = (unit(3, index) for index in range(3))
    t0 = tensor3(e0, e0, e0)
    t1 = tensor3(e1, e1, e1)
    t2 = tensor3(e2, e2, e2)

    # The (2,2) entries recover all three sources when x=y=e0.
    s0 = u0 * t1 / lam
    s1 = u1 * t1 / lam
    s2 = (u2 * t1 - t2) / lam
    assert quotient(s0, 1) == sp.zeros(8, 1)
    assert quotient(s1, 1) == sp.zeros(8, 1)
    assert quotient(s2, 1) == -quotient(t2, 1) / lam

    # Any q0 in the split-Q/equal-H base span makes P000 vanish in the
    # triple quotient.  Use arbitrary outside rows to check this symbolically.
    r_symbols = sp.symbols("ar0:9")
    p_symbols = sp.symbols("ap0:9")
    q_coefficients = sp.symbols("qa qb qc")
    r0 = sp.Matrix(r_symbols)
    p0 = sp.Matrix(p_symbols)
    q0 = (
        q_coefficients[0] * row(e1, sp.zeros(3, 1), sp.zeros(3, 1))
        + q_coefficients[1] * row(sp.zeros(3, 1), e1, sp.zeros(3, 1))
        + q_coefficients[2] * row(sp.zeros(3, 1), sp.zeros(3, 1), e1)
    )
    p000 = polarized(r0, p0, q0)
    assert quotient(p000, 1) == sp.zeros(8, 1)

    # Exact first-slice sign: (P000-T0)-sum Hc_00 Sc must vanish.  Its
    # quotient is -bar(T0)+(h2/lambda)bar(T2), which can never be zero.
    residual = p000 - t0 - h0 * s0 - h1 * s1 - h2 * s2
    projected = sp.simplify(quotient(residual, 1))
    expected = -quotient(t0, 1) + h2 * quotient(t2, 1) / lam
    assert sp.simplify(projected - expected) == sp.zeros(8, 1)
    targets = sp.Matrix.hstack(quotient(t0, 1), quotient(t2, 1))
    assert targets.rank() == 2
    assert any(
        sp.simplify(entry).coeff(h2, 0) != 0 for entry in projected
    )


def main() -> None:
    check_corrected_cubes()
    check_zero_pair_incidence_interfaces()
    check_complementary_recovered_face()
    check_aligned_unsliced_quotient()
    print(
        "PASS: both same-coordinate cubes, exhaustive zero-pair incidence "
        "interfaces, recovered-face contradiction, and aligned unsliced "
        "quotient contradiction"
    )


if __name__ == "__main__":
    main()
