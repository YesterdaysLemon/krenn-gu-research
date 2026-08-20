"""Primary exact replay for the GLD39 nonzero bidirected-spur chart completion."""

from __future__ import annotations

import sympy as sp

from verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion import W, equation


def key(port_word: str, root_word: str):
    return tuple(map(int, port_word)), tuple(map(int, root_word))


def cleaned(row):
    return {index: sp.factor(value) for index, value in row.items() if value != 0}


def main():
    first_row, first_rhs = equation(*key("1202", "0212"))
    second_row, second_rhs = equation(*key("2212", "2212"))

    assert cleaned(first_row) == {7: -W, 19: W}
    assert cleaned(second_row) == {7: -1, 19: 1}
    assert first_rhs == 0
    assert second_rhs == -1

    combined = {
        index: sp.factor(first_row.get(index, 0) - W * second_row.get(index, 0))
        for index in range(81)
    }
    assert not {index: value for index, value in combined.items() if value != 0}
    assert sp.factor(first_rhs - W * second_rhs - W) == 0
    print("PASS: exact two-row identity 0=w closes the full GLD39 nonzero bidirected-spur chart")


if __name__ == "__main__":
    main()
