#!/usr/bin/env python3
"""Verify the final monotone boundary of normalized q5_221."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_FINAL_MONOTONE_BOUNDARY_OBSTRUCTION.md"
CLOSED_MONOTONE = frozenset((0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11))
EXACT_ONLY = frozenset((8, 12, 13))
EXPECTED = (
    (0b0011, 0b0011, 0b0111),
    (0b0011, 0b0011, 0b1101),
    (0b0011, 0b0101, 0b0111),
    (0b0011, 0b0101, 0b1011),
    (0b0011, 0b0101, 0b1110),
    (0b0011, 0b0111, 0b0011),
    (0b0011, 0b0111, 0b0101),
    (0b0011, 0b0111, 0b1001),
    (0b0011, 0b0111, 0b1100),
    (0b0011, 0b1100, 0b0111),
    (0b0011, 0b1101, 0b0011),
    (0b0011, 0b1101, 0b0101),
    (0b0011, 0b1101, 0b0110),
    (0b0011, 0b1101, 0b1100),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permute_bits(bits: int, permutation) -> int:
    return sum(
        1 << permutation[index]
        for index in range(4)
        if bits & (1 << index)
    )


def canonical(pattern):
    images = []
    for permutation in itertools.permutations(range(4)):
        image = tuple(permute_bits(bits, permutation) for bits in pattern)
        images.append(image)
        images.append((image[1], image[0], image[2]))
    return min(images)


def subbits(bits: int, size: int):
    modes = tuple(index for index in range(4) if bits & (1 << index))
    return tuple(
        sum(1 << mode for mode in selection)
        for selection in itertools.combinations(modes, size)
    )


def contained_cover_indices(pattern):
    indices = set()
    for large_colour in range(3):
        choices = tuple(
            subbits(bits, 3 if colour == large_colour else 2)
            for colour, bits in enumerate(pattern)
        )
        for cover in itertools.product(*choices):
            representative = canonical(cover)
            indices.add(EXPECTED.index(representative))
    return frozenset(indices)


def permanent(matrix):
    order = len(matrix)
    return sp.factor(
        sum(
            sp.prod(matrix[row][permutation[row]] for row in range(order))
            for permutation in itertools.permutations(range(order))
        )
    )


def coefficient(factors, rows):
    return permanent(
        [
            [
                sum(
                    left * right
                    for left, right in zip(row, factor, strict=True)
                )
                for factor in factors
            ]
            for row in rows
        ]
    )


def main() -> None:
    allowed_majority = tuple(
        bits for bits in range(16) if bits.bit_count() >= 2
    )
    distinguished = tuple(
        bits for bits in range(16) if bits.bit_count() == 2
    )
    patterns = tuple(
        pattern
        for pattern in itertools.product(
            allowed_majority,
            allowed_majority,
            distinguished,
        )
        if sum(bits.bit_count() for bits in pattern) >= 8
    )

    exceptional_by_size = {}
    for pattern in patterns:
        covers = contained_cover_indices(pattern)
        assert covers
        if covers & CLOSED_MONOTONE:
            continue
        assert covers <= EXACT_ONLY
        size = sum(bits.bit_count() for bits in pattern)
        exceptional_by_size.setdefault(size, set()).add(
            canonical(pattern)
        )

    expected_exceptional = {
        (0b0111, 0b1011, 0b1100),
        (0b0011, 0b1111, 0b1100),
    }
    assert exceptional_by_size == {8: expected_exceptional}

    # The common-equality slice contains too few sign vertices for a
    # valid nonzero decomposable P3 triple.
    sign_rectangle = (
        (1, 1, 1),
        (1, -1, -1),
        (1, -1, 1),
        (1, 1, -1),
    )
    full_equality = tuple(
        normal for normal in sign_rectangle if normal[1] == normal[2]
    )
    support_two = ((0, 1, 1), (0, 1, -1))
    support_two_equality = tuple(
        normal for normal in support_two if normal[1] == normal[2]
    )
    assert len(full_equality) == 2
    assert len(support_two_equality) == 1

    e = tuple(
        tuple(1 if row == column else 0 for column in range(4))
        for row in range(4)
    )
    h0 = tuple(left - right for left, right in zip(e[0], e[1], strict=True))
    h1 = tuple(left - right for left, right in zip(e[2], e[3], strict=True))
    t2 = (e[0], e[1], e[2], e[3])
    contracted_t2 = sp.Matrix(
        [
            [
                coefficient(t2, (h0, h1, left, right))
                for right in e
            ]
            for left in e
        ]
    )
    expected_pair = sp.Matrix(
        [
            [
                coefficient((h0, h1), (left, right))
                for right in e
            ]
            for left in e
        ]
    )
    assert contracted_t2 == expected_pair
    assert contracted_t2.rank() == 2

    injection_pairing = sp.Matrix(
        [
            [
                sum(
                    left * right
                    for left, right in zip(row, vector, strict=True)
                )
                for vector in (h0, h1)
            ]
            for row in (h0, h1)
        ]
    )
    assert injection_pairing == sp.diag(2, 2)
    assert injection_pairing.rank() == 2

    target_pure_bilinear = sp.Matrix(((0, 0, 0), (0, 0, 0), (0, 0, 1)))
    assert target_pure_bilinear.rank() == 1

    # The two cross-pullback independence gates in the hard
    # orientation of S.
    p, q = sp.symbols("p q")
    d_pullbacks = sp.Matrix(((1, 0, 0), (p, 0, q)))
    c_pullbacks = sp.Matrix(((0, 1, 0), (0, p, q)))
    assert d_pullbacks[:, (0, 2)].det() == q
    assert c_pullbacks[:, (1, 2)].det() == q

    output = {
        "verified": True,
        "field": "C",
        "incidence_patterns_checked": len(patterns),
        "closed_monotone_cover_orbits": sorted(CLOSED_MONOTONE),
        "exact_only_cover_orbits": sorted(EXACT_ONLY),
        "exceptional_eight_incidence_orbits": [
            [format(bits, "04b") for bits in pattern]
            for pattern in sorted(expected_exceptional)
        ],
        "exceptional_orbits_at_nine_or_more_incidences": 0,
        "full_support_equal_coordinate_vertices": len(full_equality),
        "support_two_equal_coordinate_vertices": len(
            support_two_equality
        ),
        "double_contracted_T2_rank": contracted_t2.rank(),
        "AB_restriction_rank_on_h0_h1": injection_pairing.rank(),
        "required_target_bilinear_rank": target_pure_bilinear.rank(),
        "q5_221_excluded": True,
        "P5_to_Delta3_excluded": False,
        "remaining_branch_in_original_three_type_partition": "q4_211",
        "complete_high_coordinate_partition": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_final_monotone_boundary_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
