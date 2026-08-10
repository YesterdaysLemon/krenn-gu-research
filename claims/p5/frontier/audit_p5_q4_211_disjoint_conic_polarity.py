#!/usr/bin/env python3
"""Independent finite-field audit of the disjoint conic polarity."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_DISJOINT_CONIC_POLARITY_REDUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derivative(polynomial, variables, direction):
    return sp.expand(
        sum(
            coefficient * sp.diff(polynomial, variable)
            for coefficient, variable in zip(
                direction,
                variables,
                strict=True,
            )
        )
    )


def projective_line(prime):
    values = [(1, value) for value in range(prime)]
    values.append((0, 1))
    return values


def audit_prime(prime):
    lines = projective_line(prime)
    valid = []
    for kernels in itertools.product(lines, repeat=4):
        # Ordered as A,B,C,D.  The restricted inverse-polarity form is
        # a nonzero scalar times delta_i*delta_j.
        delta = [kernel[1] for kernel in kernels]
        if any(
            delta[left] * delta[right] % prime
            for left in (0, 1)
            for right in (2, 3)
        ):
            continue
        assert (
            delta[0] == delta[1] == 0
            or delta[2] == delta[3] == 0
        )
        valid.append(kernels)

    expected = (
        2 * (prime + 1) ** 2 - 1
    )
    # AB fixed to s gives (p+1)^2 choices on CD; CD fixed to s gives
    # the same count, with the all-s pattern counted twice.
    assert len(valid) == expected
    return {
        "prime": prime,
        "projective_kernel_lines": len(lines),
        "ordered_K22_patterns_checked": len(lines) ** 4,
        "polar_patterns": len(valid),
        "expected_polar_patterns": expected,
        "all_force_one_side_common_s_kernel": True,
    }


def main() -> None:
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    a, b, c = sp.symbols("a b c")
    variables = (x0, x1, x2, x3, x4)
    permanent = sp.prod(variables)
    u0 = (a, 1, 1, 0, 0)
    h1 = (b, 0, 0, -1, 0)
    h2 = (c, 0, 0, 0, -1)
    residual = permanent
    for direction in (u0, h1, h2):
        residual = derivative(residual, variables, direction)
    expected = (
        a * x1 * x2
        + (x1 + x2) * (x0 - b * x3 - c * x4)
    )
    assert sp.expand(residual - expected) == 0

    finite_field_audits = [audit_prime(prime) for prime in (3, 5)]
    output = {
        "audited": True,
        "method": "independent apolar derivative and projective K22 polarity census",
        "source_residual": str(sp.factor(residual)),
        "finite_field_audits": finite_field_audits,
        "ambient_row_spaces_enumerated": 0,
        "ambient_local_maps_enumerated": 0,
        "forced_common_s_kernel_pair": True,
        "disjoint_incidence_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "generic exact disjoint incidence only",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_disjoint_conic_polarity_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
