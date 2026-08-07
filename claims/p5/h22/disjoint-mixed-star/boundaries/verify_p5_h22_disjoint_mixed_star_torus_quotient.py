#!/usr/bin/env python3
"""Verify the source-torus quotient of component eight."""

from __future__ import annotations

import hashlib
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
# The disjoint-mixed-star P4 component package moved in Stage 3;
# expose it through the shared helper (Stage 4 consolidation of the
# Stage 3 per-importer shims) so the bare-name import below
# resolves.
expose_claim_package(REPO_ROOT, "claims/p4/components/disjoint-mixed-star")

import sympy as sp

from verify_p4_disjoint_mixed_star_pure_component import (  # noqa: E402
    family, relation)
from verify_p5_h22_disjoint_mixed_star_component_generic_obstruction import (
    weighted_row,
)


THEOREM = HERE / "P5_H22_DISJOINT_MIXED_STAR_TORUS_QUOTIENT.md"
COMPONENT = (
    REPO_ROOT / "claims" / "p4" / "components" / "disjoint-mixed-star"
    / "P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix_zero(matrix: sp.Matrix) -> bool:
    return all(sp.factor(entry) == 0 for entry in matrix)


def main() -> None:
    theorem_text = THEOREM.read_text(encoding="utf-8")
    assert "exact source-torus quotient lemma" in theorem_text
    assert "does not close" in theorem_text

    a, b, f, phi, r, extension = sp.symbols(
        "a b f phi r extension"
    )
    normalized_parameters = (a * f, b * f, 1, phi / f)
    original = family(a, b, f, phi)
    normalized = family(*normalized_parameters)
    source_diagonal = sp.diag(f, f, 1, 1)
    row_changes = (
        sp.eye(2),
        f * sp.eye(2),
        f * sp.eye(2),
        sp.diag(f, 1),
    )
    plane_identities = []
    for mode, (original_plane, normalized_plane, row_change) in enumerate(
        zip(
            original,
            normalized,
            row_changes,
            strict=True,
        )
    ):
        difference = sp.simplify(
            original_plane * source_diagonal
            - row_change * normalized_plane
        )
        assert matrix_zero(difference)
        assert sp.factor(row_change.det()) != 0
        plane_identities.append(
            {
                "mode": mode,
                "row_change": str(row_change),
                "identity": True,
            }
        )

    original_relation = relation(a, b, f, phi)
    normalized_relation = sp.factor(
        relation(*normalized_parameters)
    )
    assert sp.factor(original_relation - normalized_relation) == 0

    row = tuple(sp.symbols("u0:4"))
    transformed_row = tuple(
        (sp.Matrix([row]) * source_diagonal).row(0)
    )
    output_changes = {
        "01": sp.diag(f, 1, 1, 1),
        "23": sp.diag(f, f, 1, 1),
    }
    contraction_identities = []
    for direction, output_change in output_changes.items():
        left = sp.Matrix(
            [
                weighted_row(
                    transformed_row,
                    extension,
                    direction,
                    r,
                )
            ]
        )
        right = (
            sp.Matrix(
                [
                    weighted_row(
                        row,
                        extension,
                        direction,
                        r,
                    )
                ]
            )
            * output_change
        )
        assert matrix_zero(sp.simplify(left - right))
        assert sp.factor(output_change.det()) != 0
        contraction_identities.append(
            {
                "direction": direction,
                "output_change": str(output_change),
                "slope_unchanged": True,
                "identity": True,
            }
        )

    result = {
        "statement": (
            "On f!=0, component eight and both weighted H22 "
            "incidences descend to the slice f=1."
        ),
        "scope": "dense source-torus chart over characteristic zero",
        "parameter_quotient": {
            "a_normalized": "a*f",
            "b_normalized": "b*f",
            "f_normalized": "1",
            "phi_normalized": "phi/f",
        },
        "source_diagonal": str(source_diagonal),
        "plane_identities": plane_identities,
        "component_relation_invariant": True,
        "contraction_identities": contraction_identities,
        "marking_coordinate_change": {
            "t0": "t0",
            "t1": "t1",
            "t2": "t2",
            "t3": "f*t3",
        },
        "proof_boundary": {
            "f_zero_boundary": "handled separately by existing theorem",
            "remaining_linear_slope_divisor": "open",
            "remaining_quadratic_slope_divisor": "open",
            "component_exhaustiveness": "open",
            "global_prize_conjecture": "unresolved",
        },
        "sha256": {
            "theorem": sha256(THEOREM),
            "component": sha256(COMPONENT),
        },
        "verified": True,
    }
    output = (
        REPO_ROOT / "tmp"
        / "p5_h22_disjoint_mixed_star_torus_quotient_verified.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
