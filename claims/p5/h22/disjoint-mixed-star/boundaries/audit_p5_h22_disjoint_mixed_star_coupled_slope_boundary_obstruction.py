#!/usr/bin/env python3
"""Independent modular audit of the coupled H22 slope boundary.

This finite-field census is corroboration only, not a proof over C.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import (  # noqa: E402
    bootstrap,
    expose_claim_package,
)

REPO_ROOT, HERE = bootstrap(__file__, also=[".."])

# Stage 9 moved the H31 disjoint-mixed-star generic package into
# claims/p5/h31/disjoint-mixed-star/; expose it through the shared
# helper so the bare-name import below resolves.
expose_claim_package(REPO_ROOT, "claims/p5/h31/disjoint-mixed-star")

import audit_p5_h31_disjoint_mixed_star_component_generic_obstruction as A
import explore_p5_h22_disjoint_mixed_star_modular as E
from audit_p5_h31_marked_basis_open_branch import rank_mod


MODULUS = 11
PARAMETERS = (1, 2, 7, 3)
CERTIFICATES = {
    "01": (1, (0, 4, 5, 7)),
    "23": (0, (0, 1, 3, 7)),
}


def determinant_minor(matrix, rows):
    return A.determinant_mod(
        [
            [matrix[row][column] for column in range(4)]
            for row in rows
        ],
        MODULUS,
    )


def main() -> None:
    A.SAMPLES[MODULUS] = PARAMETERS
    (a, b, f, _phi), alpha, canonical_beta = A.component_basis(
        MODULUS
    )
    numerator = (a * a * f - a * b * f - a + b) % MODULUS
    denominator = (
        a * a * f + a * b * f + a + b
    ) % MODULUS
    assert denominator
    slope = numerator * pow(denominator, -1, MODULUS) % MODULUS
    cases = []
    for direction, (mode, rows) in CERTIFICATES.items():
        genuine_directions = 0
        rank_four_directions = 0
        for shifts in itertools.product(range(MODULUS), repeat=4):
            beta = tuple(
                tuple(
                    (
                        canonical_beta[index][coordinate]
                        + shifts[index] * alpha[index][coordinate]
                    )
                    % MODULUS
                    for coordinate in range(4)
                )
                for index in range(4)
            )
            mixed, first, second = E.matrices(
                alpha,
                beta,
                direction,
                slope,
                MODULUS,
            )
            _rank, kernel = A.rref_nullspace(mixed, MODULUS)
            for projective in A.projective_directions(
                len(kernel),
                MODULUS,
            ):
                extension = A.combine(
                    projective,
                    kernel,
                    MODULUS,
                )
                if not (
                    A.dot(first, extension, MODULUS)
                    and A.dot(second, extension, MODULUS)
                ):
                    continue
                genuine_directions += 1
                _values, alpha_d, beta_d = E.coefficients(
                    alpha,
                    beta,
                    direction,
                    slope,
                    extension,
                    MODULUS,
                )
                marked = A.one_marked_map(
                    mode,
                    alpha_d,
                    beta_d,
                    MODULUS,
                )
                assert determinant_minor(marked, rows)
                assert rank_mod(marked, MODULUS) == 4
                rank_four_directions += 1
        assert genuine_directions > 0
        assert rank_four_directions == genuine_directions
        cases.append(
            {
                "direction": direction,
                "marked_mode": mode,
                "minor_rows": list(rows),
                "markings": MODULUS**4,
                "genuine_projective_directions": genuine_directions,
                "rank_four_projective_directions": rank_four_directions,
            }
        )
    result = {
        "scope": "finite-field corroboration only",
        "imports_primary_verifier": False,
        "modulus": MODULUS,
        "component_point": list(PARAMETERS),
        "coupled_slope": slope,
        "cases": cases,
        "audited": True,
    }
    output = (
        REPO_ROOT / "tmp"
        / "p5_h22_disjoint_mixed_star_coupled_slope_audited.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
