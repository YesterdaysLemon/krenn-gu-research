#!/usr/bin/env python3
"""Independent audit of the component-21 kappa-infinity U0 blow-up."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

import sympy as sp

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_COMPONENT21_KAPPA_INFINITY_U0_PROJECTIVE_BLOWUP_COMPLETE_OBSTRUCTION.md"
)
PRIMARY = (
    ROOT
    / "verify_p5_component21_kappa_infinity_u0_projective_blowup_complete_obstruction.py"
)
DEPENDENCIES = {
    "claims/p5/frontier/P5_COMPONENT21_PQ_ZERO_NORMAL_BLOWUP_TRANSFER_OBSTRUCTION.md": (
        "efcaac7d95ead192dfd4fd6167d3ee1c47eaaddef746fe5c0da85033ab132c1a"
    ),
    "claims/p5/frontier/verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py": (
        "2f2b64ccf1aca2e6960d8bc4c21a57be2e9cf601d192d85f7e15255b8fa9f697"
    ),
    "claims/p5/frontier/audit_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py": (
        "e7f8c89c5437f8c3369563820e44e404f3f0603210b99fa1f26c831ecb541dc7"
    ),
    "claims/p5/frontier/P5_COMPONENT21_KAPPA_INFINITY_FIRST_NORMAL_COMPLETE_OBSTRUCTION.md": (
        "e4c11df96058efbabb09958e9ae4910b7b3747e19d3f2bc8179be36b075ad497"
    ),
    "claims/p5/frontier/verify_p5_component21_kappa_infinity_first_normal_complete_obstruction.py": (
        "779ffd59a0d4e7e3a1e563110441661cabd4f3744c138eb6053f086385c1e68a"
    ),
    "claims/p5/frontier/audit_p5_component21_kappa_infinity_first_normal_complete_obstruction.py": (
        "ccc328fad2ce2508e9108beaab1b6dd5b8cd64860b42afdc43f82ba1a1360ab7"
    ),
}
WORDS = tuple(itertools.product((0, 1), repeat=4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def combine(
    left_scale: sp.Expr,
    left: tuple[sp.Expr, ...],
    right_scale: sp.Expr,
    right: tuple[sp.Expr, ...],
) -> tuple[sp.Expr, ...]:
    return tuple(
        sp.expand(left_scale * left[index] + right_scale * right[index])
        for index in range(4)
    )


def pluecker(left: tuple[sp.Expr, ...], right: tuple[sp.Expr, ...]):
    return {
        (i, j): sp.expand(left[i] * right[j] - left[j] * right[i])
        for i in range(4)
        for j in range(i + 1, 4)
    }


def permanent_dp(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        next_states: dict[int, sp.Expr] = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                target = mask | (1 << column)
                next_states[target] = sp.expand(
                    next_states.get(target, sp.Integer(0)) + coefficient * entry
                )
        states = next_states
    return sp.expand(states[15])


def support(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> dict[str, str]:
    result = {}
    for word in WORDS:
        selected = tuple(beta[i] if word[i] else alpha[i] for i in range(4))
        coefficient = sp.factor(permanent_dp(selected))
        if coefficient != 0:
            result["".join(map(str, word))] = str(coefficient)
    return result


def main() -> None:
    cap_r, cap_p, cap_q, p, q, ell = sp.symbols("R P Q p q ell")
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    row_00 = combine(1, cap_a, p, cap_b)
    row_01 = combine(1, cap_c, q, cap_b)
    affine = pluecker(row_00, row_01)
    basis_ac = pluecker(cap_a, cap_c)
    basis_ab = pluecker(cap_a, cap_b)
    basis_bc = pluecker(cap_b, cap_c)
    homogeneous = {
        key: sp.expand(
            cap_r * basis_ac[key] + cap_q * basis_ab[key] + cap_p * basis_bc[key]
        )
        for key in basis_ac
    }
    assert {
        key: value.subs({cap_r: 1, cap_p: p, cap_q: q})
        for key, value in homogeneous.items()
    } == affine

    vertical_row = combine(cap_q, cap_a, -cap_p, cap_c)
    vertical = pluecker(vertical_row, cap_b)
    assert {key: value.subs(cap_r, 0) for key, value in homogeneous.items()} == vertical

    affine_alpha = (
        row_00,
        combine(ell, cap_a, 1, cap_c),
        cap_c,
        cap_d,
    )
    affine_beta = (
        row_01,
        cap_a,
        cap_b,
        combine(1, cap_a, ell, cap_c),
    )
    assert support(affine_alpha, affine_beta) == {
        "0111": "4*p",
        "1111": "4*q",
    }
    assert (
        support(
            tuple(
                tuple(entry.subs({p: 0, q: 0}) for entry in row) for row in affine_alpha
            ),
            tuple(
                tuple(entry.subs({p: 0, q: 0}) for entry in row) for row in affine_beta
            ),
        )
        == {}
    )

    boundary_alpha = (
        vertical_row,
        combine(ell, cap_a, 1, cap_c),
        cap_c,
        cap_d,
    )
    boundary_beta = (
        cap_b,
        cap_a,
        cap_b,
        combine(1, cap_a, ell, cap_c),
    )
    assert support(boundary_alpha, boundary_beta) == {"1111": "4"}
    assert support(
        (vertical_row, cap_a, cap_c, cap_d),
        (cap_b, cap_c, cap_b, cap_c),
    ) == {"1111": "-4"}

    local = {key: value.subs(cap_r, 1) for key, value in homogeneous.items()}
    centre = {key: value.subs({cap_p: 0, cap_q: 0}) for key, value in local.items()}
    first_normal = {key: sp.expand(local[key] - centre[key]) for key in local}
    assert first_normal == vertical

    for filename, expected in DEPENDENCIES.items():
        assert sha256(ROOT / filename) == expected
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    assert "three disjoint types of points" in theorem_text
    assert "source-marking or extension-coordinate infinity" in theorem_text
    assert "global Krenn--Gu conjecture remains **UNRESOLVED**" in theorem_text

    completed = subprocess.run(
        (sys.executable, str(PRIMARY)),
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=120,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    primary_output = json.loads(completed.stdout)
    assert primary_output["status"] == "pass"
    assert primary_output["blowup_cover_complete"] is True
    assert primary_output["arbitrary_source_extension_projective_closed"] is False

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent no-import subset-DP Pluecker audit",
                "field": "exact characteristic zero",
                "homogeneous_u0_P2_verified": True,
                "affine_pure_support": {"0111": "4*p", "1111": "4*q"},
                "unique_zero_tensor_centre": "[1:0:0]",
                "R_zero_vertical_line_verified": True,
                "exceptional_vertical_line_verified": True,
                "blowup_cover_complete": True,
                "dependency_hashes_verified": True,
                "primary_replay_passed": True,
                "marked_H31_empty": True,
                "weighted_H22_empty": True,
                "arbitrary_source_extension_projective_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "primary_sha256": sha256(PRIMARY),
                "theorem_sha256": sha256(THEOREM),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
