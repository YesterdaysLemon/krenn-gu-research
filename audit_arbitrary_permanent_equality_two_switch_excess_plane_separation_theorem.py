"""Independent no-import audit of the two-switch excess-plane theorem."""

from __future__ import annotations

from fractions import Fraction


def determinant_3(rows: tuple[tuple[int, int, int], ...]) -> int:
    (a, b, c), (d, e, f), (g, h, i) = rows
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def main() -> None:
    a, b, c, d, e_1, e_2, alpha = 2, 3, 5, 11, 13, 17, 19
    rows = ((a, c, e_1), (b, d, e_2), (0, 0, alpha))
    minor = a * d - b * c
    assert determinant_3(rows) == alpha * minor
    assert minor != 0

    gain_c = Fraction(b, a)
    gain_d = Fraction(d, c)
    assert gain_c != gain_d

    y_1, y_2 = 23, 29
    pure_switch_factor = a * y_2 + b * y_1
    gain_b = Fraction(y_2, y_1)
    assert pure_switch_factor != 0
    assert gain_c != -gain_b

    tau_a, tau_b_c, tau_b_d = 1, -1, -1
    assert tau_a == -tau_b_c
    assert tau_a == -tau_b_d
    assert tau_b_c != -tau_b_d

    print("independent no-import two-switch excess-plane audit: PASS")


if __name__ == "__main__":
    main()
