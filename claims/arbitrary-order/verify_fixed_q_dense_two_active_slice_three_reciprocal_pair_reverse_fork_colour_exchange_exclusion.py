"""All-row recursive-permanent replay of the GLD56 reverse-fork transfer."""

from __future__ import annotations

from itertools import product

import sympy as sp

from verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_star_colour_exchange_exclusion import (
    PARAMETER_EXCHANGE,
    U,
    V,
    W,
    coordinate_sign,
    equation,
    mapped_index,
    swap_word,
)


FORK_PATH = ((0, 1), (0, 2), (1, 3))
REVERSE_FORK = ((1, 0), (2, 0), (3, 1))
O12 = {(0, 1), (1, 2), (3, 2)}
POSITION_PERMUTATION = {0: 2, 1: 1, 2: 3, 3: 0}


def main():
    assert {
        (POSITION_PERMUTATION[left], POSITION_PERMUTATION[right])
        for left, right in REVERSE_FORK
    } == O12
    for value in (U, V, W):
        exchanged = value / (value - 1)
        assert sp.cancel(exchanged / (exchanged - 1) - value) == 0

    words = tuple(product(range(3), repeat=4))
    for port_word, root_word in product(words, repeat=2):
        fork_row, fork_rhs = equation(port_word, root_word, FORK_PATH)
        reverse_row, reverse_rhs = equation(
            swap_word(port_word), swap_word(root_word), REVERSE_FORK
        )
        reverse_row = {
            index: sp.cancel(value.xreplace(PARAMETER_EXCHANGE))
            for index, value in reverse_row.items()
        }
        reverse_rhs = sp.cancel(reverse_rhs.xreplace(PARAMETER_EXCHANGE))
        assert sp.cancel(reverse_rhs - fork_rhs) == 0, (port_word, root_word, "rhs")
        for index in range(81):
            actual = reverse_row.get(mapped_index(index), 0)
            expected = coordinate_sign(index) * fork_row.get(index, 0)
            assert sp.cancel(actual - expected) == 0, (port_word, root_word, index)
    print("PASS: all 6561 complete rows transfer GLD53 fork path to GLD56 O12")


if __name__ == "__main__":
    main()
