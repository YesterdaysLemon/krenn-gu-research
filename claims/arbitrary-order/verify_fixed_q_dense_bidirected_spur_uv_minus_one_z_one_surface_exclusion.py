"""Primary replay for the GLD34 z=1 surface inside the GLD32 divisor."""

from __future__ import annotations

import sympy as sp

from verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion import U, V, W, Z, equation


def key(port_word: str, root_word: str):
    return tuple(map(int, port_word)), tuple(map(int, root_word))


def assert_certificate(words, multipliers, detector):
    combined, rhs = {}, 0
    substitutions = {V: -1 / U, Z: 1}
    for pair, multiplier in zip(words, multipliers, strict=True):
        row, value = equation(*key(*pair))
        for index, coefficient in row.items():
            combined[index] = sp.factor(
                combined.get(index, 0) + multiplier * coefficient.subs(substitutions)
            )
        rhs = sp.factor(rhs + multiplier * value.subs(substitutions))
    assert not {index: value for index, value in combined.items() if value != 0}
    assert sp.factor(rhs - detector) == 0


def main():
    assert_certificate(
        (("1202", "0212"), ("2212", "2212")),
        (1, -W),
        W,
    )
    assert_certificate(
        (("0122", "1022"), ("1222", "1222")),
        (1, 1 / U),
        -1 / U,
    )
    print("PASS: two exact two-row certificates close the full GLD34 z=1 surface")


if __name__ == "__main__":
    main()
