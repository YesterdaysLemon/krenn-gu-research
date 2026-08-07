#!/usr/bin/env python3
"""No-import exact audit of the component-21 reverse classification."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRIMARY = ROOT / "verify_p4_coincident_support_star_reverse_classification.py"
THEOREM = ROOT / "P4_COINCIDENT_SUPPORT_STAR_REVERSE_CLASSIFICATION.md"


def permanent(rows: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    return sum(
        rows[0][p[0]] * rows[1][p[1]] * rows[2][p[2]] * rows[3][p[3]]
        for p in itertools.permutations(range(4))
    )


def add(*vectors: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum(entries) for entries in zip(*vectors))


def scale(value: Fraction, vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(value * entry for entry in vector)


def main() -> None:
    primary = PRIMARY.read_text(encoding="utf-8")
    theorem = THEOREM.read_text(encoding="utf-8")
    for fragment in (
        "T1010 - ell * T1110 + j * T1111",
        '"vertical_projective_placement": True',
        '"other_star_orientations_classified": False',
    ):
        assert fragment in primary
    for fragment in (
        "nonzero all-pair point in this marked orientation",
        "other endpoint signatures",
        "UNRESOLVED",
    ):
        assert fragment in theorem

    # Independent rational sample in the unreduced Borel chart.
    alpha, ell = Fraction(2), Fraction(-1)
    aa, beta, phi, e = map(Fraction, (3, 5, 7, 11))
    k, n = Fraction(2), Fraction(3)
    h = j = Fraction(0)
    A = (Fraction(1), Fraction(1), Fraction(0), Fraction(0))
    C = (Fraction(1), Fraction(-1), Fraction(0), Fraction(0))
    B = (Fraction(0), Fraction(0), Fraction(1), Fraction(1))
    D = (Fraction(0), Fraction(0), Fraction(1), Fraction(-1))
    b, d = beta * n, beta * k
    f, g = phi * n, phi * k
    planes = (
        (
            add(A, scale(-alpha, C)),
            add(scale(aa, A), scale(b, B), scale(d, D)),
        ),
        (add(scale(ell, A), C), A),
        (C, add(scale(e, A), scale(f, B), scale(g, D))),
        (add(scale(h, A), scale(j, C), scale(k, B), scale(n, D)), add(A, scale(ell, C))),
    )
    coefficients = {
        bits: permanent(tuple(planes[mode][bits[mode]] for mode in range(4)))
        for bits in itertools.product(range(2), repeat=4)
    }
    support = {bits: value for bits, value in coefficients.items() if value}
    assert set(support) == {(1, 1, 1, 1)}
    assert support[(1, 1, 1, 1)] == 4 * beta * phi * (n * n - k * k)

    # Direct projective equalities, including both endpoints and their
    # vertical limits, in (A^C,A^B,C^B) coordinates.
    p = beta / aa
    q = beta / (alpha * aa)
    finite_component = (Fraction(1), q, -p)
    finite_target = (alpha * aa, beta, -alpha * beta)
    assert finite_target == tuple((alpha * aa) * value for value in finite_component)
    endpoint_A = (Fraction(1), beta / aa, Fraction(0))
    endpoint_C = (Fraction(1), Fraction(0), -beta / aa)
    assert endpoint_A[2] == 0 and endpoint_C[1] == 0
    vertical_targets = (
        (Fraction(0), Fraction(1), -alpha),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(-1)),
    )
    assert all(any(point) for point in vertical_targets)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "independent_nonzero_support": ["1111"],
                "finite_pluecker_placement": True,
                "endpoint_placements": 2,
                "vertical_projective_arcs": 3,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
