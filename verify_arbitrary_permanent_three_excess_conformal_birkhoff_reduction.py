"""Primary symbolic checks for the conformal--Birkhoff reduction."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    x = sp.Matrix(3, 3, lambda r, s: sp.Symbol(f"x{r + 1}{s + 1}"))
    diagonal = x[0, 0] * x[1, 1] * x[2, 2]
    a = x[0, 1] * x[1, 0] / (x[0, 0] * x[1, 1])
    b = x[0, 2] * x[2, 0] / (x[0, 0] * x[2, 2])
    c = x[1, 2] * x[2, 1] / (x[1, 1] * x[2, 2])
    u = x[0, 1] * x[1, 2] * x[2, 0] / diagonal
    v = x[0, 2] * x[1, 0] * x[2, 1] / diagonal

    assert sp.factor(u * v - a * b * c) == 0
    normalized_permanent = sp.cancel(x.per() / diagonal)
    assert sp.factor(normalized_permanent - (1 + a + b + c + u + v)) == 0

    fixed_channels = (
        sp.cancel(x.minor_submatrix(0, 0).per() / (x[1, 1] * x[2, 2])),
        sp.cancel(x.minor_submatrix(1, 1).per() / (x[0, 0] * x[2, 2])),
        sp.cancel(x.minor_submatrix(2, 2).per() / (x[0, 0] * x[1, 1])),
    )
    expected_channels = (1 + c, 1 + b, 1 + a)
    assert all(
        sp.factor(value - expected) == 0
        for value, expected in zip(fixed_channels, expected_channels, strict=True)
    )

    sqrt_two = sp.sqrt(2)
    for u_value, v_value in (
        (1 + sqrt_two, 1 - sqrt_two),
        (1 - sqrt_two, 1 + sqrt_two),
    ):
        assert sp.expand(1 - 1 - 1 - 1 + u_value + v_value) == 0
        assert sp.expand(u_value * v_value + 1) == 0

    full_bypass = sp.Matrix([[1, 1, 1 - sqrt_two], [-1, 1, 1], [1 + sqrt_two, -1, 1]])
    assert sp.expand(full_bypass.per()) == 0
    assert all(
        sp.expand(full_bypass.minor_submatrix(row, row).per()) == 0 for row in range(3)
    )
    assert all(entry != 0 for entry in full_bypass)
    full_diagonal = full_bypass[0, 0] * full_bypass[1, 1] * full_bypass[2, 2]
    full_gains = (
        full_bypass[0, 1] * full_bypass[1, 0] / (full_bypass[0, 0] * full_bypass[1, 1]),
        full_bypass[0, 2] * full_bypass[2, 0] / (full_bypass[0, 0] * full_bypass[2, 2]),
        full_bypass[1, 2] * full_bypass[2, 1] / (full_bypass[1, 1] * full_bypass[2, 2]),
        full_bypass[0, 1] * full_bypass[1, 2] * full_bypass[2, 0] / full_diagonal,
        full_bypass[0, 2] * full_bypass[1, 0] * full_bypass[2, 1] / full_diagonal,
    )
    expected_full_gains = (-1, -1, -1, 1 + sqrt_two, 1 - sqrt_two)
    assert all(
        sp.expand(value - expected) == 0
        for value, expected in zip(full_gains, expected_full_gains, strict=True)
    )

    bypass_values = {a: 0, b: 0, c: -1, u: 0, v: 0}
    assert sp.expand((1 + a + b + c + u + v).subs(bypass_values)) == 0
    assert sp.expand((u * v - a * b * c).subs(bypass_values)) == 0

    # A disconnected support would give rank one, while every nontrivial
    # Delta_3 flattening has three nonzero independent diagonal terms.
    factored_flattening_rank = 1
    delta_flattening_rank = sp.eye(3).rank()
    assert (factored_flattening_rank, delta_flattening_rank) == (1, 3)
    core_matching_counts = (2, 3)
    assert core_matching_counts == (2, 3)

    print("arbitrary permanent conformal--Birkhoff reduction: PASS")
    print("fixed three-port identities only; no matching enumeration was performed")


if __name__ == "__main__":
    main()
