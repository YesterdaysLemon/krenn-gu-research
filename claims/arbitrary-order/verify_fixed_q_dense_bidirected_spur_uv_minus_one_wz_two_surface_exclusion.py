"""Primary replay for the GLD36 wz=2 surface inside the GLD32 divisor."""

from __future__ import annotations

import sympy as sp

from verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion import U, V, W, Z, equation


def key(port_word: str, root_word: str):
    return tuple(map(int, port_word)), tuple(map(int, root_word))


def main():
    substitutions = {V: -1 / U, W: 2 / Z}
    words = (("0100", "1000"), ("1222", "1222"))
    multipliers = (1, 1 / U)
    combined, rhs = {}, 0
    for pair, multiplier in zip(words, multipliers, strict=True):
        row, value = equation(*key(*pair))
        for index, coefficient in row.items():
            combined[index] = sp.factor(
                combined.get(index, 0) + multiplier * coefficient.subs(substitutions)
            )
        rhs = sp.factor(rhs + multiplier * value.subs(substitutions))
    assert not {index: value for index, value in combined.items() if value != 0}
    assert sp.factor(rhs + 1 / U) == 0
    print("PASS: an exact two-row certificate closes GLD36 and completes the uv=-1 divisor")


if __name__ == "__main__":
    main()
