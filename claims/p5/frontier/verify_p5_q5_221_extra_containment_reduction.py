#!/usr/bin/env python3
"""Verify the fourteen q5_221 seven-incidence cover orbits."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_EXTRA_CONTAINMENT_REDUCTION.md"


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


def mode_degrees(pattern):
    return tuple(
        sum(bool(bits & (1 << mode)) for bits in pattern)
        for mode in range(4)
    )


def main() -> None:
    allowed_rows = tuple(bits for bits in range(16) if bits.bit_count() >= 2)
    patterns = tuple(
        pattern
        for pattern in itertools.product(allowed_rows, repeat=3)
        if sum(bits.bit_count() for bits in pattern) == 7
    )
    orbits = tuple(sorted({canonical(pattern) for pattern in patterns}))
    assert orbits == EXPECTED
    assert all(
        sorted(bits.bit_count() for bits in pattern) == [2, 2, 3]
        for pattern in orbits
    )

    degree_histogram = {}
    for pattern in orbits:
        profile = tuple(sorted(mode_degrees(pattern), reverse=True))
        degree_histogram[profile] = degree_histogram.get(profile, 0) + 1
    assert degree_histogram == {
        (3, 3, 1, 0): 2,
        (3, 2, 2, 0): 2,
        (3, 2, 1, 1): 5,
        (2, 2, 2, 1): 5,
    }
    distinguished_triple_orbits = tuple(
        index
        for index, pattern in enumerate(orbits)
        if pattern[2].bit_count() == 3
    )
    assert distinguished_triple_orbits == (0, 1, 2, 3, 4, 9)

    # Every incidence pattern with row sizes at least two and total at
    # least seven contains a seven-incidence subpattern: choose two per
    # row, then one additional incidence.
    for pattern in itertools.product(allowed_rows, repeat=3):
        if sum(bits.bit_count() for bits in pattern) < 7:
            continue
        selected_two = tuple(
            sum(1 << mode for mode in tuple(
                index for index in range(4) if bits & (1 << index)
            )[:2])
            for bits in pattern
        )
        extra = next(
            (colour, mode)
            for colour, bits in enumerate(pattern)
            for mode in range(4)
            if bits & (1 << mode)
            and not selected_two[colour] & (1 << mode)
        )
        cover = list(selected_two)
        cover[extra[0]] |= 1 << extra[1]
        assert canonical(tuple(cover)) in EXPECTED

    output = {
        "verified": True,
        "seven_incidence_matrices_before_quotient": len(patterns),
        "marked_cover_orbits": len(orbits),
        "representatives": [
            [format(bits, "04b") for bits in pattern] for pattern in orbits
        ],
        "mode_degree_profile_histogram": {
            str(profile): count
            for profile, count in sorted(degree_histogram.items())
        },
        "all_extra_patterns_contain_a_cover": True,
        "distinguished_row_size_three_orbits": list(
            distinguished_triple_orbits
        ),
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q5_221_extra_containment_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
