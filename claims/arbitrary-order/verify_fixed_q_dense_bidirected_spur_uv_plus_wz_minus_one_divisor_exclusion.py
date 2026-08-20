"""Primary replay for the GLD37 uv+wz-1 divisor exclusion."""

from __future__ import annotations

import sympy as sp

from verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion import U, V, W, Z, equation


def key(port_word: str, root_word: str):
    return tuple(map(int, port_word)), tuple(map(int, root_word))


def assert_certificate(words, multipliers, detector):
    combined, rhs = {}, 0
    substitutions = {V: (1 - W * Z) / U}
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
        (("0100", "1000"), ("1222", "1222")),
        (1, (W * Z - 1) / U),
        -(W * Z - 1) / U,
    )
    assert_certificate(
        (("0100", "0010"), ("2212", "2212")),
        (1, W * (W * Z - 1) / U),
        -W * (W * Z - 1) / U,
    )
    print("PASS: two exact two-row certificates close the full GLD37 uv+wz-1 divisor")


if __name__ == "__main__":
    main()
