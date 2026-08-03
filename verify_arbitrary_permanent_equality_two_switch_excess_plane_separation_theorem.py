"""Primary exact checks for the two-switch excess-plane theorem."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    a, b, c, d, alpha = sp.symbols("a b c d alpha", nonzero=True)
    e_1, e_2 = sp.symbols("e_1 e_2")
    rows = sp.Matrix([[a, c, e_1], [b, d, e_2], [0, 0, alpha]])
    minor = a * d - b * c
    assert sp.factor(rows.det()) == alpha * minor

    gain_c = b / a
    gain_d = d / c
    assert sp.factor(gain_d - gain_c) == minor / (a * c)

    y_1, y_2 = sp.symbols("y_1 y_2", nonzero=True)
    pure_switch_factor = a * y_2 + b * y_1
    gain_b = y_2 / y_1
    assert sp.simplify(pure_switch_factor / (a * y_1) - gain_c - gain_b) == 0

    # The displayed signs turn both known permanents into signed determinants.
    signs = {
        "a": (1, 1),
        "b_c": (1, -1),
        "b_d": (1, -1),
    }
    tau = {row: second / first for row, (first, second) in signs.items()}
    assert tau["a"] == -tau["b_c"]
    assert tau["a"] == -tau["b_d"]
    assert tau["b_c"] != -tau["b_d"]

    print("arbitrary permanent equality two-switch excess-plane separation: PASS")
    print(
        "fixed determinant/gain algebra only; no matching or support search was performed"
    )


if __name__ == "__main__":
    main()
