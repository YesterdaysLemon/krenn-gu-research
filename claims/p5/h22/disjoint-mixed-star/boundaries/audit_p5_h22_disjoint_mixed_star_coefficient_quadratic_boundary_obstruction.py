#!/usr/bin/env python3
"""Independent modular audit of the coefficient-quadratic boundary.

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


SLOPE = 2
MINORS = ((0, 1, 3, 7), (0, 1, 5, 7))
SAMPLES = (
    (7, (1, 4, 2, 3)),
    (13, (1, 11, 6, 3)),
)
EXPECTED_COUNTS = {
    (7, "01"): 0,
    (7, "23"): 6,
    (13, "01"): 2,
    (13, "23"): 12,
}


def component_basis(parameters, modulus):
    a, b, f, phi = parameters
    p = modulus
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
    coefficient_divisor = (
        a * a * f * f + 2 * b * f + 1
    ) % p
    quadratic = (
        (a * a * f * f + 1) * phi * phi
        + f * f * (a * a * f * f - 3)
    ) % p
    assert relation == coefficient_divisor == quadratic == 0
    assert a * f % p not in (1, p - 1)
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


def determinant_minor(matrix, rows, modulus):
    return A.determinant_mod(
        [
            [matrix[row][column] for column in range(4)]
            for row in rows
        ],
        modulus,
    )


def audit_case(
    modulus: int,
    parameters,
    direction: str,
) -> dict[str, object]:
    alpha, canonical_beta = component_basis(
        parameters, modulus
    )
    genuine_markings = 0
    genuine_directions = 0
    rank_four_directions = 0
    first_minor_nonzero = 0
    second_minor_nonzero = 0
    for shifts in itertools.product(range(modulus), repeat=4):
        beta = tuple(
            tuple(
                (
                    canonical_beta[mode][coordinate]
                    + shifts[mode] * alpha[mode][coordinate]
                )
                % modulus
                for coordinate in range(4)
            )
            for mode in range(4)
        )
        mixed, first, second = E.matrices(
            alpha,
            beta,
            direction,
            SLOPE,
            modulus,
        )
        _rank, kernel = A.rref_nullspace(mixed, modulus)
        local_genuine = 0
        for projective in A.projective_directions(
            len(kernel), modulus
        ):
            extension = A.combine(projective, kernel, modulus)
            if not (
                A.dot(first, extension, modulus)
                and A.dot(second, extension, modulus)
            ):
                continue
            local_genuine += 1
            genuine_directions += 1
            _values, alpha_d, beta_d = E.coefficients(
                alpha,
                beta,
                direction,
                SLOPE,
                extension,
                modulus,
            )
            marked = A.one_marked_map(
                0,
                alpha_d,
                beta_d,
                modulus,
            )
            minors = tuple(
                determinant_minor(marked, rows, modulus)
                for rows in MINORS
            )
            first_minor_nonzero += bool(minors[0])
            second_minor_nonzero += bool(minors[1])
            assert any(minors), (
                modulus,
                direction,
                shifts,
                extension,
                minors,
            )
            assert A.rref_nullspace(marked, modulus)[0] == 4
            rank_four_directions += 1
        if local_genuine:
            genuine_markings += 1
    expected = EXPECTED_COUNTS[(modulus, direction)]
    assert genuine_directions == expected
    assert rank_four_directions == genuine_directions
    if modulus == 13 and direction == "01":
        assert genuine_directions == 2
        assert first_minor_nonzero == second_minor_nonzero == 1
    return {
        "modulus": modulus,
        "component_point": list(parameters),
        "direction": direction,
        "slope": SLOPE,
        "markings": modulus**4,
        "genuine_markings": genuine_markings,
        "genuine_projective_directions": genuine_directions,
        "rank_four_projective_directions": rank_four_directions,
        "first_minor_nonzero": first_minor_nonzero,
        "second_minor_nonzero": second_minor_nonzero,
    }


def main() -> None:
    cases = [
        audit_case(modulus, parameters, direction)
        for modulus, parameters in SAMPLES
        for direction in ("01", "23")
    ]
    result = {
        "scope": "finite-field corroboration only",
        "imports_primary_verifier": False,
        "cases": cases,
        "audited": True,
    }
    output = (
        REPO_ROOT / "tmp"
        / "p5_h22_disjoint_mixed_star_coefficient_quadratic_audited.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
