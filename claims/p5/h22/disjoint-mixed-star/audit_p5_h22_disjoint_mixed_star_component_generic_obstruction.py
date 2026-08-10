#!/usr/bin/env python3
"""Independent modular audit for the generic eighth-component H22 theorem.

The finite-field censuses here corroborate the characteristic-zero primary
verifier.  They are not themselves a proof over C.
"""

from __future__ import annotations

import itertools
import json
from concurrent.futures import ThreadPoolExecutor
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

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/marked-basis-open-branch")

# Stage 9 moved the H31 disjoint-mixed-star generic package into
# claims/p5/h31/disjoint-mixed-star/; expose it through the shared
# helper so the bare-name import below resolves.
expose_claim_package(REPO_ROOT, "claims/p5/h31/disjoint-mixed-star")
import audit_p5_h31_disjoint_mixed_star_component_generic_obstruction as A
import explore_p5_h22_disjoint_mixed_star_modular as E
from audit_p5_h31_marked_basis_open_branch import rank_mod


MINOR_0137 = (0, 1, 3, 7)
MINOR_0157 = (0, 1, 5, 7)
SAMPLES = {
    11: (1, 2, 7, 3),
    13: (1, 3, 5, 10),
}
EXPECTED_D01 = {
    11: [
        (4, 2, 0, 0),
        (4, 4, 0, 10),
        (7, 0, 4, 0),
        (7, 0, 7, 7),
        (8, 0, 0, 0),
    ],
    13: [
        (8, 0, 2, 11),
        (8, 0, 5, 0),
        (9, 3, 0, 9),
        (9, 12, 0, 0),
        (10, 0, 0, 0),
    ],
}
EXPECTED_D23 = {
    11: [(value, 0, 0, 0) for value in range(1, 11)],
    13: [
        (value, 0, 0, 0)
        for value in range(13)
        if value != 10
    ],
}


def determinant_minor(matrix, rows, modulus):
    return A.determinant_mod(
        [
            [matrix[row][column] for column in range(4)]
            for row in rows
        ],
        modulus,
    )


def audit_field(modulus: int) -> dict[str, object]:
    A.SAMPLES[modulus] = SAMPLES[modulus]
    _parameters, alpha, canonical_beta = A.component_basis(modulus)
    result = {}
    for direction in ("01", "23"):
        survivors = []
        genuine_directions = 0
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
                2,
                modulus,
            )
            rank, kernel = A.rref_nullspace(mixed, modulus)
            if rank == 8:
                continue
            assert rank == 7
            genuine = []
            for projective in A.projective_directions(
                len(kernel),
                modulus,
            ):
                extension = A.combine(projective, kernel, modulus)
                if (
                    A.dot(first, extension, modulus)
                    and A.dot(second, extension, modulus)
                ):
                    genuine.append(extension)
            if not genuine:
                continue
            assert len(genuine) == 1
            survivors.append(shifts)
            for extension in genuine:
                _values, alpha_d, beta_d = E.coefficients(
                    alpha,
                    beta,
                    direction,
                    2,
                    extension,
                    modulus,
                )
                marked = A.one_marked_map(
                    0,
                    alpha_d,
                    beta_d,
                    modulus,
                )
                assert rank_mod(marked, modulus) == 4
                first_minor = determinant_minor(
                    marked,
                    MINOR_0137,
                    modulus,
                )
                second_minor = determinant_minor(
                    marked,
                    MINOR_0157,
                    modulus,
                )
                if direction == "01":
                    assert first_minor or second_minor
                else:
                    assert first_minor and second_minor
                genuine_directions += 1
        expected = (
            EXPECTED_D01[modulus]
            if direction == "01"
            else EXPECTED_D23[modulus]
        )
        assert survivors == expected
        if direction == "01":
            assert all(
                shifts[1] * shifts[2] % modulus == 0
                for shifts in survivors
            )
        else:
            assert all(
                shifts[1] == shifts[2] == shifts[3] == 0
                for shifts in survivors
            )
        result[direction] = {
            "survivors": [list(shifts) for shifts in survivors],
            "survivor_count": len(survivors),
            "genuine_projective_directions": genuine_directions,
            "mixed_rank": 7,
            "mode_zero_marked_rank": 4,
        }
    return {
        "modulus": modulus,
        "component_point": list(SAMPLES[modulus]),
        "slope": 2,
        "directions": result,
    }


def main() -> None:
    with ThreadPoolExecutor(max_workers=2) as executor:
        fields = list(executor.map(audit_field, (11, 13)))
    result = {
        "scope": "finite-field corroboration only",
        "imports_primary_verifier": False,
        "fields": fields,
        "audited": True,
    }
    output = (
        REPO_ROOT / "tmp"
        / "p5_h22_disjoint_mixed_star_component_generic_audited.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
