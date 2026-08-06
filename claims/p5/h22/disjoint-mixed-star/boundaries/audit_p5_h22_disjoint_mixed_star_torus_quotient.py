#!/usr/bin/env python3
"""Independent modular audit of the component-eight torus quotient."""

from __future__ import annotations

import json
from pathlib import Path


import sys
HERE = Path(__file__).resolve().parent


def _repo_root() -> Path:
    for candidate in (HERE, *HERE.parents):
        if (candidate / ".git").exists():
            return candidate
    return HERE


REPO_ROOT = _repo_root()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))
SAMPLES = (
    (11, (1, 2, 7, 3)),
    (13, (1, 3, 5, 10)),
)


def matrix_multiply(left, right, modulus):
    return tuple(
        tuple(
            sum(
                left[row][index] * right[index][column]
                for index in range(len(right))
            )
            % modulus
            for column in range(len(right[0]))
        )
        for row in range(len(left))
    )


def family(parameters, modulus):
    a, b, f, phi = parameters
    p = modulus
    j = (f + b * phi * phi) % p
    kappa = phi * (b * f + 1) % p
    eta = -(b * f + 1) % p
    return (
        ((0, 0, 1, -1), (a + b, a - b, 0, 2)),
        (
            (-a * f + 1, -a * f - 1, f + phi, f - phi),
            (1, 1, 0, 0),
        ),
        (
            (
                -a * j + eta,
                -a * j - eta,
                j + kappa,
                j - kappa,
            ),
            (1, 1, 0, 0),
        ),
        ((1, -1, 0, 0), (0, 0, 1, 1)),
    )


def component_relation(parameters, modulus):
    a, b, f, phi = parameters
    return (
        a * a * b * f * phi * phi
        + a * a * f * f
        - b * b * f * f
        + b * b * phi * phi
        - b * f
        - 1
    ) % modulus


def weighted(row, extension, direction, slope, modulus):
    if direction == "01":
        return (
            (slope * row[0] + row[1]) % modulus,
            row[2] % modulus,
            row[3] % modulus,
            extension % modulus,
        )
    if direction == "23":
        return (
            row[0] % modulus,
            row[1] % modulus,
            (slope * row[2] + row[3]) % modulus,
            extension % modulus,
        )
    raise ValueError(direction)


def audit_sample(modulus: int, parameters) -> dict[str, object]:
    a, b, f, phi = parameters
    inverse_f = pow(f, -1, modulus)
    normalized_parameters = (
        a * f % modulus,
        b * f % modulus,
        1,
        phi * inverse_f % modulus,
    )
    source_diagonal = (
        (f, 0, 0, 0),
        (0, f, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )
    row_changes = (
        ((1, 0), (0, 1)),
        ((f, 0), (0, f)),
        ((f, 0), (0, f)),
        ((f, 0), (0, 1)),
    )
    original = family(parameters, modulus)
    normalized = family(normalized_parameters, modulus)
    for original_plane, normalized_plane, row_change in zip(
        original,
        normalized,
        row_changes,
        strict=True,
    ):
        assert matrix_multiply(
            original_plane,
            source_diagonal,
            modulus,
        ) == matrix_multiply(
            row_change,
            normalized_plane,
            modulus,
        )
    assert component_relation(parameters, modulus) == (
        component_relation(normalized_parameters, modulus)
    )

    rows = (
        (1, 2, 3, 4),
        (3, 5, 7, 9),
    )
    contraction_checks = 0
    for row in rows:
        transformed = (
            f * row[0] % modulus,
            f * row[1] % modulus,
            row[2] % modulus,
            row[3] % modulus,
        )
        for direction in ("01", "23"):
            for slope in (2, 3):
                for extension in (1, 4):
                    left = weighted(
                        transformed,
                        extension,
                        direction,
                        slope,
                        modulus,
                    )
                    right = weighted(
                        row,
                        extension,
                        direction,
                        slope,
                        modulus,
                    )
                    expected = (
                        (
                            f * right[0] % modulus,
                            right[1],
                            right[2],
                            right[3],
                        )
                        if direction == "01"
                        else (
                            f * right[0] % modulus,
                            f * right[1] % modulus,
                            right[2],
                            right[3],
                        )
                    )
                    assert left == expected
                    contraction_checks += 1
    return {
        "modulus": modulus,
        "original_parameters": list(parameters),
        "normalized_parameters": list(normalized_parameters),
        "plane_identities": 4,
        "contraction_checks": contraction_checks,
    }


def main() -> None:
    samples = [
        audit_sample(modulus, parameters)
        for modulus, parameters in SAMPLES
    ]
    result = {
        "scope": "finite-field corroboration only",
        "imports_primary_verifier": False,
        "samples": samples,
        "audited": True,
    }
    output = (
        REPO_ROOT / "tmp"
        / "p5_h22_disjoint_mixed_star_torus_quotient_audited.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
