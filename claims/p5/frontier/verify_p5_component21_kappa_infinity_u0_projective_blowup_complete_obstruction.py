#!/usr/bin/env python3
"""Verify the U0-projective blow-up over component 21 kappa infinity."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])

from verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction import (
    add,
    pure_support,
    scale,
    wedge,
)

ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_COMPONENT21_KAPPA_INFINITY_U0_PROJECTIVE_BLOWUP_COMPLETE_OBSTRUCTION.md"
)
PINNED = {
    ROOT / "P5_COMPONENT21_PQ_ZERO_NORMAL_BLOWUP_TRANSFER_OBSTRUCTION.md": (
        "efcaac7d95ead192dfd4fd6167d3ee1c47eaaddef746fe5c0da85033ab132c1a"
    ),
    ROOT / "verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py": (
        "2f2b64ccf1aca2e6960d8bc4c21a57be2e9cf601d192d85f7e15255b8fa9f697"
    ),
    ROOT / "audit_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py": (
        "e7f8c89c5437f8c3369563820e44e404f3f0603210b99fa1f26c831ecb541dc7"
    ),
    ROOT / "P5_COMPONENT21_KAPPA_INFINITY_FIRST_NORMAL_COMPLETE_OBSTRUCTION.md": (
        "e4c11df96058efbabb09958e9ae4910b7b3747e19d3f2bc8179be36b075ad497"
    ),
    ROOT
    / "verify_p5_component21_kappa_infinity_first_normal_complete_obstruction.py": (
        "779ffd59a0d4e7e3a1e563110441661cabd4f3744c138eb6053f086385c1e68a"
    ),
    ROOT / "audit_p5_component21_kappa_infinity_first_normal_complete_obstruction.py": (
        "ccc328fad2ce2508e9108beaab1b6dd5b8cd64860b42afdc43f82ba1a1360ab7"
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    cap_r, cap_p, cap_q, p, q, ell = sp.symbols("R P Q p q ell")
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))

    row_00 = add(cap_a, scale(p, cap_b))
    row_01 = add(cap_c, scale(q, cap_b))
    affine_pluecker = wedge(row_00, row_01)
    homogeneous_pluecker = (
        cap_r * wedge(cap_a, cap_c)
        + cap_q * wedge(cap_a, cap_b)
        + cap_p * wedge(cap_b, cap_c)
    )
    assert sp.simplify(
        homogeneous_pluecker.subs({cap_r: 1, cap_p: p, cap_q: q}) - affine_pluecker
    ) == sp.zeros(6, 1)

    vertical_row = add(scale(cap_q, cap_a), scale(-cap_p, cap_c))
    assert homogeneous_pluecker.subs(cap_r, 0) == wedge(vertical_row, cap_b)

    affine_alpha = (
        row_00,
        add(scale(ell, cap_a), cap_c),
        cap_c,
        cap_d,
    )
    affine_beta = (
        row_01,
        cap_a,
        cap_b,
        add(cap_a, scale(ell, cap_c)),
    )
    assert pure_support(affine_alpha, affine_beta) == {
        "0111": "4*p",
        "1111": "4*q",
    }

    boundary_alpha = (
        vertical_row,
        add(scale(ell, cap_a), cap_c),
        cap_c,
        cap_d,
    )
    boundary_beta = (
        cap_b,
        cap_a,
        cap_b,
        add(cap_a, scale(ell, cap_c)),
    )
    assert pure_support(boundary_alpha, boundary_beta) == {"1111": "4"}
    infinity_alpha = (vertical_row, cap_a, cap_c, cap_d)
    infinity_beta = (cap_b, cap_c, cap_b, cap_c)
    assert pure_support(infinity_alpha, infinity_beta) == {"1111": "-4"}

    local_pluecker = homogeneous_pluecker.subs(cap_r, 1)
    base_pluecker = local_pluecker.subs({cap_p: 0, cap_q: 0})
    first_normal = sp.expand(local_pluecker - base_pluecker)
    assert first_normal == wedge(vertical_row, cap_b)
    assert (
        pure_support(
            tuple(
                tuple(entry.subs({p: 0, q: 0}) for entry in row) for row in affine_alpha
            ),
            tuple(
                tuple(entry.subs({p: 0, q: 0}) for entry in row) for row in affine_beta
            ),
        )
        == {}
    )

    dependency_hashes = {path.name: sha256(path) for path in PINNED}
    assert all(sha256(path) == expected for path, expected in PINNED.items())
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for required in (
        "There are no omitted mode-zero Grassmann points",
        "does not classify source-marking or extension-coordinate infinity",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
    ):
        assert required in theorem_text

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "component": 21,
                "u0_projective_surface": "P2 with coordinates [R:P:Q]",
                "homogeneous_pluecker_identity": True,
                "boundary_R_zero": "<Q*A-P*C,B>",
                "affine_pure_support": {"0111": "4*p", "1111": "4*q"},
                "unique_affine_zero_tensor": "[R:P:Q]=[1:0:0]",
                "exceptional_line": "<Q*A-P*C,B>",
                "boundary_and_exceptional_vertical_kappa_zero": True,
                "blowup_cover_complete": True,
                "marked_H31_empty": True,
                "weighted_H22_empty": True,
                "arbitrary_source_extension_projective_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "dependency_hashes": dependency_hashes,
                "theorem_sha256": sha256(THEOREM),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
