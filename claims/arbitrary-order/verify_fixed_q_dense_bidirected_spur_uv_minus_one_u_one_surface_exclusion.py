"""Primary replay for the GLD33 u=1 surface inside the GLD32 divisor."""

from __future__ import annotations

import sympy as sp

from verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion import U, V, W, Z, equation


def key(port_word: str, root_word: str):
    return tuple(map(int, port_word)), tuple(map(int, root_word))


def table(words, multipliers):
    return tuple(key(*pair) for pair in words), tuple(map(sp.sympify, multipliers))


DETECTOR_A_KEYS, DETECTOR_A_MULTIPLIERS = table(
    (("0011", "0011"), ("0010", "0010"), ("0011", "0000"),
     ("0002", "0002"), ("1000", "1000"), ("0100", "1000"),
     ("0100", "0100"), ("1000", "0100"), ("1100", "0000"),
     ("0110", "0000"), ("0101", "0000"), ("1010", "0000"),
     ("0102", "0102")),
    (2 * (W * Z - 2) * (W**2 * Z**2 + W * Z**2 + 2 * W * Z - Z**2 + 2 * Z + 1),
     Z**2 * (W + 1) * (W * Z - 2) * (W * Z + 3),
     4 * Z * (W + 1) * (W * Z - 2),
     -2 * (Z + 1) * (W * Z - 2) * (W * Z + 1),
     -2 * Z * (W + 1) * (W * Z - 2) * (W * Z + 1),
     -2 * Z * (W + 1) * (W * Z - 2) * (W * Z + 1),
     2 * Z * (W + 1) * (W * Z - 2),
     -2 * Z * (W * Z - 2) * (W * Z + 1) ** 2,
     -2 * Z * (W * Z + 1) * (3 * W * Z + 3 * W + 3 * Z + 2),
     (W * Z + 1) * (W**2 * Z**2 + 2 * W**2 * Z - W * Z**2 + 4 * W * Z + 2 * W + 8 * Z + 4),
     2 * Z * (W + 1) * (Z - 1) * (W * Z - 2),
     (W * Z + 1) * (W**2 * Z**2 + 2 * W**2 * Z + W * Z**2 + 4 * W * Z + 2 * W + 4 * Z + 4),
     2 * W * Z * (Z - 1) * (W * Z - 2)),
)

DETECTOR_B_KEYS, DETECTOR_B_MULTIPLIERS = table(
    (("0011", "0011"), ("0010", "0010"), ("0011", "0000"),
     ("0002", "0002"), ("1000", "1000"), ("0100", "1000"),
     ("0100", "0100"), ("1000", "0100"), ("0100", "0010"),
     ("1100", "0000"), ("0110", "0000"), ("1010", "0000"),
     ("1010", "1010"), ("0100", "1110")),
    (-(Z + 1) * (W * Z - 2) * (W * Z + 2),
     -Z * (W * Z - 2) * (W * Z + Z + 2),
     -2 * (Z + 1) * (W * Z - 2), 2 * (Z + 1) * (W * Z - 2),
     2 * Z * (W + 1) * (W * Z - 2), 2 * Z * (W * Z - 2) * (W * Z + 1),
     -2 * Z * (W * Z - 2), 2 * Z * (W * Z - 2) * (W * Z + 1),
     2 * Z * (Z - 1) * (W * Z - 2), 2 * Z * (4 * W * Z + 2 * W + 3 * Z + 2),
     -2 * W**2 * Z**2 - W**2 * Z + W * Z**2 - 4 * W * Z - 2 * W - 8 * Z - 4,
     -2 * W**2 * Z**2 - W**2 * Z - W * Z**2 - 4 * W * Z - 2 * W - 4 * Z - 4,
     2 * W * Z * (Z - 1) * (W * Z - 2), 2 * W * Z * (Z - 1) * (W * Z - 2)),
)

CURVE_KEYS, CURVE_MULTIPLIERS = table(
    (("0011", "0011"), ("0010", "0010"), ("0011", "0000"),
     ("0002", "0002"), ("1000", "1000"), ("0100", "1000"),
     ("0100", "0100"), ("1000", "0100"), ("1100", "0000"),
     ("0110", "0000"), ("0101", "0000"), ("0102", "0102"),
     ("1110", "0010")),
    (-2 * (Z**2 - 4 * Z - 9), 5 * Z * (Z + 2), 4 * (Z + 2),
     -6 * (Z + 1), -6 * (Z + 2), -6 * (Z + 2), 2 * (Z + 2),
     -18 * Z, -6 * (Z**2 + 3 * Z + 1), -6 * Z,
     2 * (Z - 1) * (Z + 2), 4 * (Z - 1), 3 * (3 * Z**2 + 8 * Z + 6)),
)

POINT_KEYS, POINT_MULTIPLIERS = table(
    (("0011", "0011"), ("0010", "0010"), ("0011", "0000"),
     ("0002", "0002"), ("1000", "1000"), ("0100", "1000"),
     ("0100", "0100"), ("1000", "0100"), ("1100", "0000"),
     ("0110", "0000"), ("1010", "0000"), ("0120", "0120")),
    (-3, 6, -6, 6, -6, -6, 3, -6, 5, 2, 5, 6),
)


def assert_certificate(keys, multipliers, substitutions, detector):
    combined, rhs = {}, 0
    for row_key, multiplier in zip(keys, multipliers, strict=True):
        row, value = equation(*row_key)
        for index, coefficient in row.items():
            combined[index] = sp.factor(combined.get(index, 0) + multiplier * coefficient.subs(substitutions))
        rhs = sp.factor(rhs + multiplier * value.subs(substitutions))
    assert not {index: value for index, value in combined.items() if value != 0}
    assert sp.factor(rhs - detector) == 0


def main():
    surface = {U: 1, V: -1}
    assert_certificate(DETECTOR_A_KEYS, DETECTOR_A_MULTIPLIERS, surface, 4 * W * Z * (W * Z - 2) * (W * Z + 1))
    assert_certificate(DETECTOR_B_KEYS, DETECTOR_B_MULTIPLIERS, surface, -2 * W * Z * (Z + 1) * (W * Z - 2))
    assert_certificate(CURVE_KEYS, CURVE_MULTIPLIERS, {**surface, W: 2 / Z}, 24)
    assert_certificate(POINT_KEYS, POINT_MULTIPLIERS, {**surface, W: 1, Z: -1}, 6)
    print("PASS: exact certificates close the full GLD33 u=1 bidirected-spur surface")


if __name__ == "__main__":
    main()
