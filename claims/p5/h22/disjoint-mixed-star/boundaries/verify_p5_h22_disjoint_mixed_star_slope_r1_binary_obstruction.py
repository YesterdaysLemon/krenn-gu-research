#!/usr/bin/env python3
"""Exact characteristic-zero closure of the slope divisor r=1 for BOTH
weighted H22 pencils on the disjoint mixed-star (eighth) component.

Scope: the generic component point (function field K=C(a,b,f)[phi]/(Phi))
with the pencil slope specialized to r=1 -- exactly the slope divisor
left open by the generic theorem
P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md, whose
t-free elimination divides by single-1-word own-extension coefficients
carrying the factor (r-1) (three of the four denominators in each
pencil).

All statements are exact sympy polynomial identities modulo Phi.

D_23 pencil at r=1 (equal-weight slope of the 23 pencil):
  (S1) universal kernel: the y_3 column of all fourteen mixed rows
       vanishes identically, for every marking t.  On the universal
       direction z=e_{y3}: A=0 and B=4 -- a pure-reconstruction-type
       line, the analogue of the ubiquitous q=1 kernel of the
       six-dimensional component.
  (S2) A = A0 * x_0 with A0 a nowhere-vanishing unit (reduced value
       4b(af-1)(af+1)(bf+1) up to a unit): genuine needs x_0 != 0.
  (S3) two-row combination identity, valid for every marking:
           A0*M_0011 - (E3 + A0*t3)*M_0010  =  A0*V*x_0   (mod Phi)
       with E3 the t-free part of the 0001-row x_0 coefficient and V
       the t-free part of the 0011-row x_0 coefficient, V a unit
       (reduced value -4af up to a unit).  Hence x_0 = 0 and A(z)=0
       on EVERY kernel vector of EVERY marking: the D_23 pencil has
       no genuine binary survivor at r=1.

D_01 pencil at r=1 (equal-weight slope of the 01 pencil):
  (S4) universal TWO-dimensional kernel: the y_1 and y_2 columns of
       all fourteen mixed rows vanish identically; on each line A=0,
       B=4 (double pure reconstruction).
  (S5) A = A0' * x_3 with A0' a unit (reduced value
       4ab*phi*(bf+1)(a^2f^2+2bf+1) up to a unit).
  (S6) two-row combination identity, valid for every marking:
           (C1 + A0'*t1)*M_0010 - A0'*M_0110  =  C1*C2*x_3   (mod Phi)
       with C1, C2 the t-free parts of the 0100/0010-row x_3
       coefficients, both units (reduced values -4phi(bf+1), -4phi up
       to units).  Hence x_3=0 and A(z)=0 on every kernel vector: the
       D_01 pencil has no genuine binary survivor at r=1 either.

Consequently at slope 1 neither weighted pencil admits a genuine
binary Delta_2 extension for any marking, before any third target row
is considered.  Every (a,b)-support subfamily of H22 requires at least
one sharp pencil with a genuine binary survivor, so the r=1 slope
divisor of the generic weighted-H22 obstruction is CLOSED at binary
level for both pencils, over the generic component point.

This parallels P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md.

Remaining after this script: intersections of r=1 with the parameter
divisors dividing the displayed units (a, b, f, phi, af+-1, bf+1,
a^2f+b, and the resultant factors), and the projective boundary.
"""

from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

def _repo_root():
    for candidate in Path(__file__).resolve().parents:
        if (candidate / ".git").exists():
            return candidate
    return Path(__file__).resolve().parent


_REPO_ROOT = _repo_root()
sys.path.insert(0, str(_REPO_ROOT / "research_snapshots" / "2026-08-04-p5-h22-slope-divisor-closures" / "scripts"))

import sympy as sp

from slope_common import (
    MIXED,
    PHI,
    T,
    Z,
    a,
    b,
    build_system,
    f,
    phi,
    phi_normal_form,
    resultant_certificate,
)

OUT = _REPO_ROOT / "research_snapshots" / "2026-08-04-p5-h22-slope-divisor-closures"


def zero_column(rows, column):
    for bits in MIXED:
        assert phi_normal_form(rows[bits][column]) == 0, (bits, column)


def zero_slots(row, keep):
    for m in range(8):
        if m != keep:
            assert phi_normal_form(row[m]) == 0, m


def tfree_part(expr, tvars):
    return sp.expand(expr.subs({tv: 0 for tv in tvars}))


def combination_identity(u, row_u, v, row_v, target_slot, value):
    """Assert u*row_u + v*row_v = value * e_{target_slot} slotwise
    mod Phi."""
    for m in range(8):
        lhs = sp.expand(u * row_u[m] + v * row_v[m])
        rhs = value if m == target_slot else 0
        assert phi_normal_form(sp.expand(lhs - rhs)) == 0, m


def main() -> None:
    started = time.monotonic()
    certificates = {}

    # ------------------------------------------------------------------
    # D_23 pencil at slope 1
    # ------------------------------------------------------------------
    d23 = build_system("23", sp.Integer(1))
    rows = d23["rows"]

    # (S1) universal kernel line e_{y3}.
    zero_column(rows, 7)
    assert phi_normal_form(d23["A"][7]) == 0
    assert phi_normal_form(sp.expand(d23["B"][7] - 4)) == 0
    certificates["d23_universal_kernel"] = {
        "direction": "z = e_{y3}, independent of t",
        "A_on_it": "0",
        "B_on_it": "4",
    }

    # (S2) A concentrated on x_0, unit coefficient.
    A0 = d23["A"][0]
    assert not set(A0.free_symbols) & set(T)
    zero_slots(d23["A"], 0)
    A0_red = phi_normal_form(A0)
    certificates["d23_A_concentration"] = {
        "identity": "A = A0 * x0 (mod Phi)",
        "A0_reduced_factored": str(sp.factor(A0_red)),
        "A0_unit_certificate": resultant_certificate(A0),
    }

    # (S3) two-row combination identity.
    row_0010 = rows[(0, 0, 1, 0)]
    row_0011 = rows[(0, 0, 1, 1)]
    zero_slots(row_0010, 0)
    zero_slots(row_0011, 0)
    E3 = tfree_part(rows[(0, 0, 0, 1)][0], (T[3],))
    V = tfree_part(row_0011[0], (T[2], T[3]))
    # t-expansions of the two selected x_0 coefficients:
    assert phi_normal_form(
        sp.expand(row_0010[0] - A0 * T[2])
    ) == 0
    assert phi_normal_form(
        sp.expand(row_0011[0] - (V + E3 * T[2] + A0 * T[2] * T[3]))
    ) == 0
    combination_identity(
        A0, row_0011, -(E3 + A0 * T[3]), row_0010, 0,
        sp.expand(A0 * V),
    )
    certificates["d23_two_row_obstruction"] = {
        "identity": (
            "A0*M_0011 - (E3 + A0*t3)*M_0010 = A0*V*x0  (mod Phi)"
        ),
        "V_reduced_factored": str(sp.factor(phi_normal_form(V))),
        "V_unit_certificate": resultant_certificate(V),
        "deduction": (
            "on any kernel vector A0*V*x0=0 with A0,V units, so x0=0 "
            "and A(z)=A0*x0=0: no genuine survivor for any marking"
        ),
    }

    # ledger: all seven bits_0=0 mixed rows are x_0 multiples.
    for bits in MIXED:
        if bits[0] == 0:
            zero_slots(rows[bits], 0)
    certificates["d23_x0_multiple_rows"] = [
        "".join(map(str, bits)) for bits in MIXED if bits[0] == 0
    ]

    # ------------------------------------------------------------------
    # D_01 pencil at slope 1
    # ------------------------------------------------------------------
    d01 = build_system("01", sp.Integer(1))
    rows01 = d01["rows"]

    # (S4) universal 2-dimensional kernel e_{y1}, e_{y2}.
    zero_column(rows01, 5)
    zero_column(rows01, 6)
    assert phi_normal_form(d01["A"][5]) == 0
    assert phi_normal_form(d01["A"][6]) == 0
    assert phi_normal_form(sp.expand(d01["B"][5] - 4)) == 0
    assert phi_normal_form(sp.expand(d01["B"][6] - 4)) == 0
    certificates["d01_universal_kernel"] = {
        "directions": "z = e_{y1} and z = e_{y2}, independent of t",
        "A_on_them": "0",
        "B_on_them": "4",
    }

    # (S5) A concentrated on x_3, unit coefficient.
    A0p = d01["A"][3]
    assert not set(A0p.free_symbols) & set(T)
    zero_slots(d01["A"], 3)
    certificates["d01_A_concentration"] = {
        "identity": "A = A0' * x3 (mod Phi)",
        "A0p_reduced_factored": str(
            sp.factor(phi_normal_form(A0p))
        ),
        "A0p_unit_certificate": resultant_certificate(A0p),
    }

    # (S6) two-row combination identity.
    row_0100 = rows01[(0, 1, 0, 0)]
    row_0010b = rows01[(0, 0, 1, 0)]
    row_0110 = rows01[(0, 1, 1, 0)]
    for row in (row_0100, row_0010b, row_0110):
        zero_slots(row, 3)
    C1 = tfree_part(row_0100[3], (T[1],))
    C2 = tfree_part(row_0010b[3], (T[2],))
    assert phi_normal_form(
        sp.expand(row_0100[3] - (C1 + A0p * T[1]))
    ) == 0
    assert phi_normal_form(
        sp.expand(row_0010b[3] - (C2 + A0p * T[2]))
    ) == 0
    assert phi_normal_form(
        sp.expand(
            row_0110[3]
            - (C2 * T[1] + C1 * T[2] + A0p * T[1] * T[2])
        )
    ) == 0
    combination_identity(
        C1 + A0p * T[1], row_0010b, -A0p, row_0110, 3,
        sp.expand(C1 * C2),
    )
    certificates["d01_two_row_obstruction"] = {
        "identity": (
            "(C1 + A0'*t1)*M_0010 - A0'*M_0110 = C1*C2*x3  (mod Phi)"
        ),
        "C1_reduced_factored": str(sp.factor(phi_normal_form(C1))),
        "C2_reduced_factored": str(sp.factor(phi_normal_form(C2))),
        "C1_unit_certificate": resultant_certificate(C1),
        "C2_unit_certificate": resultant_certificate(C2),
        "deduction": (
            "on any kernel vector C1*C2*x3=0 with C1,C2 units, so "
            "x3=0 and A(z)=A0'*x3=0: no genuine survivor for any "
            "marking"
        ),
    }

    # ledger: every bits_3=0 mixed row is an x_3 multiple.
    for bits in MIXED:
        if bits[3] == 0:
            zero_slots(rows01[bits], 3)
    certificates["d01_x3_multiple_rows"] = [
        "".join(map(str, bits)) for bits in MIXED if bits[3] == 0
    ]

    # ------------------------------------------------------------------
    # Independent finite-field replay (corroboration only).
    # ------------------------------------------------------------------
    from explore_p5_h22_disjoint_mixed_star_slope_divisors_modular import (
        build_rows,
        component_basis,
        dot,
        pattern_table,
        rref_nullspace,
        weighted3 as w3mod,
    )

    replay = {}
    for p in (11, 13):
        _, alpha_p, beta_p = component_basis(p)
        for direction in ("23", "01"):
            wa = [w3mod(alpha_p[m], direction, 1, p) for m in range(4)]
            wb = [w3mod(beta_p[m], direction, 1, p) for m in range(4)]
            table = pattern_table(wa, wb, p)
            genuine = 0
            for t in itertools.product(range(p), repeat=4):
                mixed, dA, dB = build_rows(t, table, p)
                _, kernel = rref_nullspace(mixed, p)
                restA = [dot(dA, v, p) for v in kernel]
                restB = [dot(dB, v, p) for v in kernel]
                if any(restA) and any(restB):
                    genuine += 1
            assert genuine == 0, (p, direction)
            replay[f"p{p}_D{direction}"] = (
                "all p^4 markings: no kernel vector with both "
                "diagonals nonzero"
            )
    certificates["modular_replay"] = replay

    result = {
        "verified": True,
        "field": "C(a,b,f)[phi]/(Phi), slope fixed at r=1",
        "component": "disjoint mixed-star fivefold (eighth orbit)",
        "statement": (
            "at slope r=1 neither weighted H22 pencil has a genuine "
            "binary Delta_2 extension for any marking; the r=1 slope "
            "divisor of the generic weighted-H22 obstruction is "
            "closed at binary level for both pencils over the generic "
            "component point"
        ),
        "certificates": certificates,
        "remaining_open": [
            "intersections of r=1 with the component parameter "
            "divisors dividing the displayed units",
            "projective component boundary at r=1",
        ],
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    path = OUT / "r1_binary_obstruction_verified.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
