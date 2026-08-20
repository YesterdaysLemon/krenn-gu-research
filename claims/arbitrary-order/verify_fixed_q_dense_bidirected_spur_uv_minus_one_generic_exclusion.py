"""Primary exact replay for the GLD32 generic uv=-1 bidirected-spur divisor."""

from __future__ import annotations

import sympy as sp

from verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion import (
    U,
    V,
    W,
    Z,
    equation,
)


def key(port_word: str, root_word: str):
    return tuple(map(int, port_word)), tuple(map(int, root_word))


KEYS = tuple(
    key(*words)
    for words in (
        ("0011", "0011"), ("0010", "0010"), ("0011", "0000"),
        ("0002", "0002"), ("1000", "1000"), ("0100", "1000"),
        ("0100", "0100"), ("1000", "0100"), ("1100", "0000"),
        ("0110", "0000"), ("0101", "0000"), ("1010", "0000"),
        ("1100", "1100"), ("0000", "1100"),
    )
)

A = U**2 * W * Z**2 - U**2 * W * Z + 2 * U**2 * Z - 2 * U**2 - U * W * Z**2 + U * W * Z - 2 * U * Z**2 - 4 * U * Z + 2 * U + 4 * Z
B = -U**2 * Z - U**2 + U * W * Z**2 - U * W * Z - 2 * U * Z**2 + 2 * U * Z - W * Z**2 + W * Z + Z + 1
C = U * W * Z + 2 * U - W * Z - 2 * Z - 2
D = -U**2 * Z**2 + U * W * Z**3 - 2 * U * W * Z**2 + U * W * Z - 2 * U * Z**3 - 2 * U * Z - 2 * U - W * Z**3 + 2 * W * Z**2 - W * Z + Z**2 + 4 * Z + 2
E = -U**2 + U * W * Z - 3 * U * W - 2 * U * Z - 2 * W * Z + 4 * W + 3
F = U**2 * W * Z - 3 * U**2 - U * W * Z - 3 * U * W - 2 * U * Z + 4 * U - W * Z + 4 * W + 1
G = -U**3 * Z - U**3 + U**2 * W * Z**2 - 2 * U**2 * W * Z - 2 * U**2 * Z**2 + 2 * U**2 * Z - U**2 - U * W * Z**2 + 3 * U * W * Z + U * Z + 3 * U - W * Z - 1

MULTIPLIERS = (
    -U**2 * Z * (U - 1) * (Z - 1) * (Z + 1) * (W * Z - 2) * (W * Z + 2),
    U * Z * (Z + 1) * (W * Z - 2) * A,
    U * (U - 1) * (Z - 1) * (Z + 1) * (W * Z - 2) * C,
    2 * U * Z * (U - 1) * (Z - 1) * (Z + 1) * (W * Z - 2),
    -2 * U * Z * (Z + 1) * (W * Z - 2) * B,
    -2 * U * Z * (U - 1) ** 2 * (Z + 1) * (W * Z - 2) * (W * Z + 1),
    2 * Z * (U - 1) ** 2 * (Z + 1) * (W * Z - 2),
    -2 * Z * (Z + 1) * (W * Z - 2) * B,
    -2 * U * Z * (Z + 1) * D,
    2 * U * Z**2 * (Z + 1) * E,
    2 * U * Z * (U - 1) ** 2 * (Z - 1) * (Z + 1) * (W * Z - 2),
    2 * Z**2 * (Z + 1) * F,
    2 * Z * (Z + 1) * (W * Z - 2) * G,
    2 * Z * (W * Z - 2) * G,
)


def combine(substitutions):
    combined, rhs = {}, 0
    for row_key, multiplier in zip(KEYS, MULTIPLIERS, strict=True):
        row, value = equation(*row_key)
        for index, coefficient in row.items():
            combined[index] = sp.factor(
                combined.get(index, 0) + multiplier * coefficient.subs(substitutions)
            )
        rhs = sp.factor(rhs + multiplier * value.subs(substitutions))
    return {index: value for index, value in combined.items() if value != 0}, rhs


def main():
    row, rhs = combine({V: -1 / U})
    detector = -2 * U * W * Z**2 * (U - 1) * (Z - 1) * (Z + 1) * (W * Z - 2)
    assert not row
    assert sp.factor(rhs - detector) == 0
    print("PASS: exact 14-row certificate gives the GLD32 generic uv=-1 divisor detector")


if __name__ == "__main__":
    main()
