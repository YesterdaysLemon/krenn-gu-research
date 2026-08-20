"""Primary exact replay for the GLD40 affine bidirected-spur chart completion."""

from __future__ import annotations

import sympy as sp

from verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion import U, V, W, Z, equation


def key(port_word: str, root_word: str):
    return tuple(map(int, port_word)), tuple(map(int, root_word))


def cleaned(row, substitutions):
    values = {
        index: sp.factor(sp.sympify(value).subs(substitutions))
        for index, value in row.items()
    }
    return {index: value for index, value in values.items() if value != 0}


def assert_relation(first_key, second_key, substitutions, multiplier, first_expected, second_expected):
    first_row, first_rhs = equation(*key(*first_key))
    second_row, second_rhs = equation(*key(*second_key))
    assert cleaned(first_row, substitutions) == first_expected
    assert cleaned(second_row, substitutions) == second_expected
    first_rhs = sp.factor(first_rhs.subs(substitutions))
    second_rhs = sp.factor(second_rhs.subs(substitutions))
    assert first_rhs == 0
    assert second_rhs == -1
    combined = {
        index: sp.factor(
            sp.sympify(first_row.get(index, 0)).subs(substitutions)
            - multiplier * sp.sympify(second_row.get(index, 0)).subs(substitutions)
        )
        for index in range(81)
    }
    assert not {index: value for index, value in combined.items() if value != 0}
    assert sp.factor(first_rhs - multiplier * second_rhs - multiplier) == 0


def main():
    assert_relation(
        ("1022", "0122"), ("2122", "2122"), {}, U,
        {4: -U, 16: U}, {4: -1, 16: 1},
    )
    assert_relation(
        ("1202", "0212"), ("2212", "2212"), {}, W,
        {7: -W, 19: W}, {7: -1, 19: 1},
    )
    boundary = {U: 0, W: 0}
    assert_relation(
        ("0100", "1000"), ("1222", "1222"), boundary, V,
        {1: -V, 13: V}, {1: -1, 13: 1},
    )
    assert_relation(
        ("0010", "1000"), ("1222", "1222"), boundary, Z,
        {1: -Z, 13: Z}, {1: -1, 13: 1},
    )
    print(
        "PASS: four exact two-row detectors plus the GLD23 identity boundary "
        "cover the full GLD40 affine chart"
    )


if __name__ == "__main__":
    main()
