#!/usr/bin/env python3
"""Independent polarization audit for the repeated-pair cover theorem."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_REPEATED_MAJORITY_PAIR_COVER_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pairing(first, second):
    return sum(
        left * right
        for left, right in zip(first, second, strict=True)
    )


def polarization_coefficient(source_factors, target_rows):
    variables = sp.symbols("t_P t_Q t_R t_S")
    polynomial = sp.prod(
        sum(
            variables[mode] * pairing(target_rows[mode], source_factor)
            for mode in range(4)
        )
        for source_factor in source_factors
    )
    return sp.factor(
        sp.Poly(polynomial, *variables).coeff_monomial(
            sp.prod(variables)
        )
    )


def main() -> None:
    e0 = (1, 0, 0, 0, 0)
    e1 = (0, 1, 0, 0, 0)
    e2 = (0, 0, 1, 0, 0)
    e3 = (0, 0, 0, 1, 0)
    h2 = (0, 0, 0, 0, 1)
    u0 = (1, 1, 0, 0, 0)
    h0 = (1, -1, 0, 0, 0)
    u1 = (0, 0, 1, 1, 0)
    h1 = (0, 0, 1, -1, 0)

    p0, p2, q0, q2, b, f, cap_c = sp.symbols(
        "p0 p2 q0 q2 b f C"
    )
    alpha = sp.symbols("alpha")

    # Only the rows involved in the three decisive coefficients are
    # needed.  They are read independently from the geometric chart.
    p_row0 = tuple(left + p0 * right for left, right in zip(h1, u1))
    p_row2 = tuple(p2 * value for value in u1)
    q_row0 = tuple(left + q0 * right for left, right in zip(h1, u1))
    q_row2 = tuple(q2 * value for value in u1)
    r_row0 = tuple(b * value for value in u0)
    r_row2 = tuple(f * value for value in u0)
    s_row0 = tuple(
        left + right
        for left, right in zip(
            h2,
            tuple(
                value
                for value in u0
            ),
        )
    )
    s_row2 = tuple(
        cap_c * (left + alpha * right)
        for left, right in zip(u0, h1)
    )

    t0 = (u0, e2, e3, h2)
    t2 = (e0, e1, e2, e3)
    required_t0 = polarization_coefficient(
        t0,
        (p_row0, q_row0, r_row0, s_row0),
    )
    forbidden_t0 = polarization_coefficient(
        t0,
        (p_row0, q_row0, r_row2, s_row0),
    )
    required_t2 = polarization_coefficient(
        t2,
        (p_row2, q_row2, r_row2, s_row2),
    )
    assert required_t0 == 4 * b * (p0 * q0 - 1)
    assert forbidden_t0 == 4 * f * (p0 * q0 - 1)
    assert required_t2 == 4 * cap_c * f * p2 * q2

    # Audit the kernel and incidence content without importing the
    # primary verifier's row-space helpers.
    gram = lambda rows: sp.Matrix(rows) * sp.Matrix(rows).T
    assert gram((h0, h1, u1)).det() != 0
    assert gram((h1, h2, u0)).det() != 0
    assert pairing(h0, u0) == pairing(h1, u1) == 0
    assert pairing(h0, h1) == pairing(h0, h2) == 0
    assert pairing(h1, h2) == 0

    # In the S chart, restriction to J12 has kernel h0 and the pinned
    # rows send h2 and u1 to distinct target coordinate lines.
    s_basis0 = tuple(left + alpha * right for left, right in zip(u0, h1))
    beta = sp.symbols("beta")
    s_basis1 = tuple(left + beta * right for left, right in zip(u1, h1))
    assert pairing(s_basis0, h0) == pairing(s_basis1, h0) == 0
    assert pairing(h2, h0) == 0
    assert pairing(s_basis0, u1) == 0
    assert pairing(s_basis1, u1) == 2

    output = {
        "audited": True,
        "field": "C",
        "method": "independent mixed-polynomial coefficient extraction",
        "ambient_row_spaces_enumerated": 0,
        "required_T0_0000": str(required_t0),
        "forbidden_T0_0020": str(forbidden_t0),
        "required_T2_2222": str(required_t2),
        "normal_form_incidence_checked": True,
        "exact_cover_excluded": True,
        "monotone_cover_excluded": False,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "symbolic identity and normal-form audit",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_q5_221_repeated_majority_pair_cover_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
