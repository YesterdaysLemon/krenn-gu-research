#!/usr/bin/env python3
"""Independent modular audit of the af/aphi H22 boundary.

The finite-field census is corroboration only, not a proof over C.
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


MODULUS = 7
SLOPE = 2
MINORS = ((0, 1, 3, 7), (0, 1, 5, 7))
BRANCH_SAMPLES = (
    ("af_plus1__aphi_plus1", (1, 2, 1, 1)),
    ("af_plus1__aphi_minus1", (1, 2, 1, 6)),
    ("af_minus1__aphi_plus1", (1, 2, 6, 1)),
    ("af_minus1__aphi_minus1", (1, 2, 6, 6)),
)


def component_basis(parameters):
    a, b, f, phi = parameters
    p = MODULUS
    j = (f + b * phi * phi) % p
    kappa = phi * (b * f + 1) % p
    eta = -(b * f + 1) % p
    alpha = (
        (0, 0, 1, -1),
        (-a * f + 1, -a * f - 1, f + phi, f - phi),
        (
            -a * j + eta,
            -a * j - eta,
            j + kappa,
            j - kappa,
        ),
        (1, -1, 0, 0),
    )
    beta = (
        (a + b, a - b, 0, 2),
        (1, 1, 0, 0),
        (1, 1, 0, 0),
        (0, 0, 1, 1),
    )
    alpha = tuple(
        tuple(value % p for value in row) for row in alpha
    )
    beta = tuple(tuple(value % p for value in row) for row in beta)
    relation = (
        a * a * b * f * phi * phi
        + a * a * f * f
        - b * b * f * f
        + b * b * phi * phi
        - b * f
        - 1
    ) % p
    assert relation == 0
    assert all(
        A.rref_nullspace(plane, p)[0] == 2
        for plane in (
            alpha[0:1] + beta[0:1],
            alpha[1:2] + beta[1:2],
            alpha[2:3] + beta[2:3],
            alpha[3:4] + beta[3:4],
        )
    )
    return alpha, beta


def determinant_minor(matrix, rows):
    return A.determinant_mod(
        [
            [matrix[row][column] for column in range(4)]
            for row in rows
        ],
        MODULUS,
    )


def audit_branch(branch: str, parameters) -> dict[str, object]:
    a, b, f, phi = parameters
    assert a * f % MODULUS in (1, MODULUS - 1)
    assert a * phi % MODULUS in (1, MODULUS - 1)
    assert b % MODULUS
    assert (a * a - b * b) % MODULUS
    assert (b * f + 1) % MODULUS
    assert (b * phi - 1) % MODULUS
    assert (b * phi + 1) % MODULUS

    alpha, canonical_beta = component_basis(parameters)
    cases = []
    for direction in ("01", "23"):
        genuine_directions = 0
        rank_four_directions = 0
        for shifts in itertools.product(
            range(MODULUS), repeat=4
        ):
            beta = tuple(
                tuple(
                    (
                        canonical_beta[mode][coordinate]
                        + shifts[mode] * alpha[mode][coordinate]
                    )
                    % MODULUS
                    for coordinate in range(4)
                )
                for mode in range(4)
            )
            mixed, first, second = E.matrices(
                alpha,
                beta,
                direction,
                SLOPE,
                MODULUS,
            )
            _rank, kernel = A.rref_nullspace(mixed, MODULUS)
            for projective in A.projective_directions(
                len(kernel), MODULUS
            ):
                extension = A.combine(
                    projective, kernel, MODULUS
                )
                if not (
                    A.dot(first, extension, MODULUS)
                    and A.dot(second, extension, MODULUS)
                ):
                    continue
                genuine_directions += 1
                if direction == "23":
                    raise AssertionError(
                        (
                            "D23 binary obstruction failed",
                            branch,
                            shifts,
                            extension,
                        )
                    )
                _values, alpha_d, beta_d = E.coefficients(
                    alpha,
                    beta,
                    direction,
                    SLOPE,
                    extension,
                    MODULUS,
                )
                marked = A.one_marked_map(
                    0,
                    alpha_d,
                    beta_d,
                    MODULUS,
                )
                minors = tuple(
                    determinant_minor(marked, rows)
                    for rows in MINORS
                )
                assert any(minors), (
                    branch,
                    shifts,
                    extension,
                    minors,
                )
                assert (
                    A.rref_nullspace(marked, MODULUS)[0] == 4
                )
                rank_four_directions += 1
        if direction == "23":
            assert genuine_directions == 0
        else:
            assert genuine_directions > 0
            assert rank_four_directions == genuine_directions
        cases.append(
            {
                "direction": direction,
                "slope": SLOPE,
                "markings": MODULUS**4,
                "genuine_projective_directions": genuine_directions,
                "rank_four_projective_directions": (
                    rank_four_directions
                ),
            }
        )
    return {
        "branch": branch,
        "modulus": MODULUS,
        "generic_component_point": list(parameters),
        "cases": cases,
    }


def main() -> None:
    branches = [
        audit_branch(branch, parameters)
        for branch, parameters in BRANCH_SAMPLES
    ]
    assert sum(
        case["genuine_projective_directions"]
        for branch in branches
        for case in branch["cases"]
        if case["direction"] == "01"
    ) > 0
    result = {
        "scope": "finite-field corroboration only",
        "imports_primary_verifier": False,
        "branches": branches,
        "audited": True,
    }
    output = (
        REPO_ROOT / "tmp"
        / "p5_h22_disjoint_mixed_star_af_aphi_audited.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
