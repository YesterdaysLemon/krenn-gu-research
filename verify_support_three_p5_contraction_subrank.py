#!/usr/bin/env python3
"""Primary verifier for the support-three P_5 contraction obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "SUPPORT_THREE_P5_CONTRACTION_SUBRANK.md"
COLOURS = frozenset(range(3))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def kernel_types() -> tuple[tuple[str, frozenset[int]], ...]:
    lines = tuple(
        ("line", frozenset(support))
        for size in (1, 2)
        for support in itertools.combinations(range(3), size)
    )
    planes = tuple(
        ("plane", frozenset({missing})) for missing in range(3)
    )
    return lines + planes


def diagonal_product_basis(
    left: tuple[str, frozenset[int]],
    right: tuple[str, frozenset[int]],
) -> tuple[frozenset[int], ...]:
    """Supports of a basis for coordinatewise products of two kernels."""
    left_kind, left_data = left
    right_kind, right_data = right
    if left_kind == "line" and right_kind == "line":
        intersection = left_data & right_data
        return (intersection,) if intersection else ()
    if left_kind == "plane" and right_kind == "line":
        return tuple(
            frozenset({colour}) for colour in sorted(right_data - left_data)
        )
    if left_kind == "line" and right_kind == "plane":
        return diagonal_product_basis(right, left)

    left_missing = next(iter(left_data))
    right_missing = next(iter(right_data))
    if left_missing == right_missing:
        return tuple(
            frozenset({colour})
            for colour in range(3)
            if colour != left_missing
        )
    remaining = COLOURS - {left_missing, right_missing}
    return (frozenset(remaining),)


def complementary_form_can_match(
    left: tuple[str, frozenset[int]],
    right: tuple[str, frozenset[int]],
    diagonal_support: frozenset[int],
) -> bool:
    """Necessary rank and row/column-space test for F_ij."""
    left_kind, left_data = left
    right_kind, right_data = right
    if left_kind == "line" and right_kind == "line":
        # F has rank two and full row/column spaces K_i^perp,K_j^perp.
        required_kernel = COLOURS - diagonal_support
        return (
            len(diagonal_support) == 2
            and left_data == required_kernel
            and right_data == required_kernel
        )
    if left_kind == "plane" and right_kind == "line":
        if len(diagonal_support) != 1:
            return False
        colour = next(iter(diagonal_support))
        missing = next(iter(left_data))
        # The plane side has covector space <e_missing>; the line side
        # can supply e_colour only when that coordinate kills the line.
        return missing == colour and colour not in right_data
    if left_kind == "line" and right_kind == "plane":
        return complementary_form_can_match(
            right, left, diagonal_support
        )

    if len(diagonal_support) != 1:
        return False
    colour = next(iter(diagonal_support))
    return next(iter(left_data)) == next(iter(right_data)) == colour


def main() -> None:
    # The support-three contraction has a nondegenerate quadratic factor.
    z0, z1, z2 = sp.symbols("z0 z1 z2", nonzero=True)
    quadratic_matrix = sp.Matrix(
        [[0, z2, z1], [z2, 0, z0], [z1, z0, 0]]
    )
    quadratic_determinant = sp.factor(quadratic_matrix.det())
    assert quadratic_determinant == 2 * z0 * z1 * z2

    # Reconstruct rank(P_3)=4.  Its three-dimensional slice space has no
    # nonzero rank-one matrix because its principal minors are squares.
    x, y, z = sp.symbols("x y z")
    p3_slice = sp.Matrix([[0, z, y], [z, 0, x], [y, x, 0]])
    principal_minors = (
        sp.factor(p3_slice.extract((0, 1), (0, 1)).det()),
        sp.factor(p3_slice.extract((0, 2), (0, 2)).det()),
        sp.factor(p3_slice.extract((1, 2), (1, 2)).det()),
    )
    assert principal_minors == (-z**2, -y**2, -x**2)
    assert sp.Matrix(
        [
            [sp.diff(p3_slice[row, column], variable) for variable in (x, y, z)]
            for row in range(3)
            for column in range(3)
        ]
    ).rank() == 3
    polarization = sp.expand(
        (x + y + z) ** 3
        - (x + y - z) ** 3
        - (x - y + z) ** 3
        - (-x + y + z) ** 3
    )
    assert polarization == 24 * x * y * z

    # Exhaust the nine abstract kernel types at four modes.  For every
    # complementary pair, the coordinatewise-product image must have
    # dimension at most one and its sole diagonal form must be compatible
    # with the rank and row/column spaces of F_ij.
    types = kernel_types()
    rejection_counts: Counter[str] = Counter()
    survivors = []
    quadruples_checked = 0
    pair_checks = 0
    for kernels in itertools.product(types, repeat=4):
        quadruples_checked += 1
        rejected = False
        for first, second in itertools.combinations(range(4), 2):
            pair_checks += 1
            diagonal_basis = diagonal_product_basis(
                kernels[first], kernels[second]
            )
            if len(diagonal_basis) > 1:
                rejection_counts["product_image_dimension_at_least_two"] += 1
                rejected = True
                break
            if not diagonal_basis:
                continue
            complement = tuple(
                mode for mode in range(4) if mode not in (first, second)
            )
            if not complementary_form_can_match(
                kernels[complement[0]],
                kernels[complement[1]],
                diagonal_basis[0],
            ):
                rejection_counts["rank_or_row_space_mismatch"] += 1
                rejected = True
                break
        if not rejected:
            survivors.append(kernels)
    assert quadruples_checked == 9**4
    assert not survivors

    # Explicit induced two-edge box for every full-support contraction.
    first_edge = (0, 1, 3, 4)
    second_edge = (1, 3, 4, 0)
    box = tuple(
        tuple(
            second_edge[mode] if (choice >> mode) & 1 else first_edge[mode]
            for mode in range(4)
        )
        for choice in range(16)
    )

    def active(entry: tuple[int, ...]) -> bool:
        return (
            len(set(entry)) == 4
            and next(index for index in range(5) if index not in entry) < 3
        )

    active_box = {entry for entry in box if active(entry)}
    assert active_box == {first_edge, second_edge}
    assert all(
        next(index for index in range(5) if index not in entry) == 2
        for entry in active_box
    )

    output = {
        "verified": True,
        "field": "C",
        "quadratic_determinant": str(quadratic_determinant),
        "p3_principal_minors": [str(item) for item in principal_minors],
        "p3_tensor_rank": 4,
        "kernel_types": len(types),
        "kernel_quadruples_checked": quadruples_checked,
        "kernel_pair_checks": pair_checks,
        "kernel_rejection_counts": dict(rejection_counts),
        "kernel_survivors": len(survivors),
        "explicit_diagonal_two_box_entries": [first_edge, second_edge],
        "support_three_contraction_subrank": 2,
        "support_at_most_three_contraction_subrank_upper_bound": 2,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "support_three_p5_contraction_subrank_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
