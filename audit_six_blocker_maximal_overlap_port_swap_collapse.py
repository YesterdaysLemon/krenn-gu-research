#!/usr/bin/env python3
"""Independent no-import audit of the maximal-overlap port swap."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction

import sympy as sp


def subset_permanent(matrix: tuple[tuple[int, ...], ...]) -> int:
    states = {0: 1}
    for column in range(6):
        next_states = {}
        for mask, value in states.items():
            for row in range(6):
                if mask & (1 << row):
                    continue
                new_mask = mask | (1 << row)
                next_states[new_mask] = (
                    next_states.get(new_mask, 0) + value * matrix[row][column]
                )
        states = next_states
    return states.get(63, 0)


def covector_rows():
    e0, e1, e2 = (1, 0, 0), (0, 1, 0), (0, 0, 1)

    def add(left, right, scale=1):
        return tuple(left[index] + scale * right[index] for index in range(3))

    exceptional0 = (e1, e2, add(e1, e2), add(e1, e2, 2), add(e1, e2, -1), e0)
    exceptional1 = (e0, e2, add(e0, e2), add(e0, e2, 2), add(e0, e2, -1), e1)
    exceptional2 = (e0, e1, add(e0, e1), add(e0, e1, 2), add(e0, e1, -1), e2)
    full = (
        e0,
        e1,
        e2,
        (1, 1, 1),
        (1, 2, 3),
        (3, 2, 1),
    )
    return (exceptional0, exceptional1, exceptional2, full, full, full)


def span_profile(rows) -> int:
    matrix = sp.Matrix(rows)
    rank = matrix.rank()
    mask = 0
    for colour in range(3):
        coordinate = [0, 0, 0]
        coordinate[colour] = 1
        if matrix.col_join(sp.Matrix([coordinate])).rank() == rank:
            mask |= 1 << colour
    return mask


def contraction_digest(rows) -> str:
    swap = (0, 1, 2, 3, 5, 4)
    base_values = []
    swapped_values = []
    for word in itertools.product(range(3), repeat=6):
        base = tuple(
            tuple(rows[mode][row][word[mode]] for mode in range(6)) for row in range(6)
        )
        moved = tuple(base[swap[row]] for row in range(6))
        base_value = subset_permanent(base)
        moved_value = subset_permanent(moved)
        assert base_value == moved_value
        base_values.append(base_value)
        swapped_values.append(moved_value)
    assert base_values == swapped_values
    encoded = ",".join(map(str, base_values)).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    rows = covector_rows()
    left = tuple(span_profile(mode[:5]) for mode in rows)
    right = tuple(span_profile((*mode[:4], mode[5])) for mode in rows)
    assert left == (6, 5, 3, 7, 7, 7)
    assert right == (7, 7, 7, 7, 7, 7)
    assert tuple(sp.Matrix(mode).rank() for mode in rows) == (3, 3, 3, 3, 3, 3)

    digest = contraction_digest(rows)

    # A different rational section realizes all incident covectors.
    root = sp.Matrix([1, 1, 1])
    section = sp.Matrix([1, 0, 0])
    for mode in rows:
        for covector_tuple in mode:
            covector = sp.Matrix([covector_tuple])
            block = section * covector
            assert root.T * block == covector
            assert block != sp.zeros(3)

    # A different nonzero root-root block gives the same torus nonblocker.
    root_block = sp.diag(2, -3, 1)
    assert (root.T * root_block * root)[0] == 0
    root_covector = root.T * root_block
    assert root_covector == sp.Matrix([[2, -3, 1]])
    assert span_profile([tuple(root_covector)]) == 0
    assert (root_covector * root)[0] == 0

    # Independently compare the two GHZ coefficient products using unequal
    # full-support integer root vectors.
    root_vectors = tuple(
        (Fraction(index + 1), Fraction(index + 2), Fraction(index + 4))
        for index in range(6)
    )
    ghz_coefficients = []
    for colour in range(3):
        left_coefficient = root_vectors[5][colour]
        for root_index in (0, 1, 2, 3, 4):
            left_coefficient *= root_vectors[root_index][colour]
        right_coefficient = root_vectors[4][colour]
        for root_index in (0, 1, 2, 3, 5):
            right_coefficient *= root_vectors[root_index][colour]
        assert left_coefficient == right_coefficient
        assert left_coefficient != 0
        ghz_coefficients.append(left_coefficient)

    # Direct support audit: a simultaneous transposition of values 4 and 5
    # permutes the 720 permanent monomials.
    support = tuple(itertools.permutations(range(6)))
    transposed = {
        tuple(5 if value == 4 else 4 if value == 5 else value for value in word)
        for word in support
    }
    assert transposed == set(support)

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent subset permanent and alternate block sections",
                "left_profiles": left,
                "right_profiles": right,
                "target_words_checked": 3**6,
                "permanent_monomials_checked": len(support),
                "contraction_sha256": digest,
                "ghz_coefficients": [str(value) for value in ghz_coefficients],
                "local_incident_blocks_realized": True,
                "global_matching_identity_realized": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
