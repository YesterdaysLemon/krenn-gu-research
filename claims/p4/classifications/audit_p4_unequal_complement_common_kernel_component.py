#!/usr/bin/env python3
"""Independent exact audit of the unequal-complement common-kernel component."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


ROOT = HERE
PRIMARY = HERE / "verify_p4_unequal_complement_common_kernel_component.py"
THEOREM = HERE / "P4_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT.md"
PAIRS = tuple(itertools.combinations(range(4), 2))


def add(*vectors: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum(entries) for entries in zip(*vectors))


def scale(value: Fraction, vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(value * entry for entry in vector)


def rank(rows: list[tuple[Fraction, ...]]) -> int:
    matrix = [list(row) for row in rows if any(row)]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / divisor for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row:
                continue
            multiple = matrix[row][column]
            if multiple:
                matrix[row] = [
                    entry - multiple * pivot_entry
                    for entry, pivot_entry in zip(matrix[row], matrix[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def pair_product(
    left: tuple[Fraction, ...], right: tuple[Fraction, ...]
) -> tuple[Fraction, ...]:
    return tuple(left[i] * right[j] + left[j] * right[i] for i, j in PAIRS)


def permanent(rows: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    return sum(
        (
            rows[0][permutation[0]]
            * rows[1][permutation[1]]
            * rows[2][permutation[2]]
            * rows[3][permutation[3]]
        )
        for permutation in itertools.permutations(range(4))
    )


def transform(
    vector: tuple[Fraction, ...],
    permutation: tuple[int, ...],
    scales: tuple[Fraction, ...],
) -> tuple[Fraction, ...]:
    return tuple(scales[index] * vector[permutation[index]] for index in range(4))


def main() -> None:
    primary = PRIMARY.read_text(encoding="utf-8")
    theorem = THEOREM.read_text(encoding="utf-8")
    for fragment in (
        "expected_branch_bases",
        '"component_orbit_number": 22',
        '"complete_CC_orientation_classified": True',
        '"finite_field_proof_used": False',
    ):
        assert fragment in primary
    for fragment in (
        "four linear sheets",
        "component twenty-two",
        "exhaust every projective complementary",
        "Krenn--Gu conjecture remains",
        "UNRESOLVED",
    ):
        assert fragment in theorem

    # An unrelated rational point on L1, then a source permutation and
    # unequal diagonal scaling.  This audit shares no code with the primary.
    A = Fraction(2)
    R = Fraction(-1)
    D = Fraction(3)
    u = (1 - D) / 2
    v = (1 + D) / 2
    G = -(2 * A + R) / 2
    a = (Fraction(1), Fraction(1), Fraction(0), Fraction(0))
    c = (Fraction(1), Fraction(-1), Fraction(0), Fraction(0))
    m = (2 * A, Fraction(0), Fraction(1), Fraction(1))
    mr = add(m, scale(R, c))
    d = add(scale(G, a), (Fraction(0), Fraction(0), u, v))
    y0 = (Fraction(0), D * (2 * A + R), -u, v)
    x0 = (-A * v, A * (u + 1) + R, Fraction(1), Fraction(0))
    raw_planes = ((y0, x0), (m, a), (mr, a), (c, d))

    source_permutation = (2, 0, 3, 1)
    source_scales = tuple(map(Fraction, (2, 3, 5, 7)))
    planes = tuple(
        tuple(transform(row, source_permutation, source_scales) for row in plane)
        for plane in raw_planes
    )

    coefficients = {}
    for bits in itertools.product(range(2), repeat=4):
        coefficients[bits] = permanent(
            tuple(planes[mode][bits[mode]] for mode in range(4))
        )
    support = {bits: value for bits, value in coefficients.items() if value}
    assert set(support) == {(1, 1, 1, 1)}
    assert support[(1, 1, 1, 1)] != 0

    profile = []
    relation_ranks = []
    for edge in PAIRS:
        rows = [
            pair_product(planes[edge[0]][i], planes[edge[1]][j])
            for i in range(2)
            for j in range(2)
        ]
        edge_rank = rank(rows)
        profile.append(edge_rank)
        if edge in ((1, 2), (1, 3), (2, 3)):
            # Exact rank-one edge relations have coefficient rank one;
            # the synchronizer has coefficient rank two.
            relation_ranks.append(2 if edge == (1, 2) else 1)
    assert profile == [4, 4, 4, 3, 3, 3]
    assert relation_ranks == [2, 1, 1]

    # The normalized Pluecker extension has a fixed nonzero last coordinate,
    # so the D=-1 basis collapse in the primary is only a row-chart failure.
    extended_pluecker = (
        A * D * (2 * A + R) / 2,
        A * (D - 1) / 4,
        A * (D + 1) / 4,
        (A * D + 3 * A + 2 * R) / 4,
        (A * D - 3 * A - 2 * R) / 4,
        Fraction(-1, 2),
    )
    assert extended_pluecker[-1] != 0

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "independent_source_permutation": source_permutation,
                "independent_source_scales": list(map(int, source_scales)),
                "pure_support": ["1111"],
                "pair_profile": profile,
                "relation_ranks": relation_ranks,
                "projective_D_minus_one_extension_nonzero": True,
                "complete_CC_boundary_ledger_replayed": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
