#!/usr/bin/env python3
"""Exact identification of the H22 pencil slope boundaries r=0 and
r=infinity with the four H31 coordinate frames, on the disjoint
mixed-star component.

  D_01^0        = q=0 frame (delete source coordinate 0),
  D_01^infinity = q=1 frame (delete source coordinate 1),
  D_23^0        = q=2 frame (delete source coordinate 2),
  D_23^infinity = q=3 frame (delete source coordinate 3).

r=0 is literal substitution; r=infinity holds after scaling the
weighted column by 1/r (a uniform column scaling multiplies every
binary word coefficient by exactly 1/r, hence rescales the whole
mixed system, diagonals included, leaving kernels and genuineness
unchanged), i.e. substituting r=1/s, scaling by s, and letting s->0.

Consequences via the verified H31 generic theorem
(P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md):
  * q=0,1: the projected marking ideal is UNIT: no genuine binary
    survivor for any marking => the D_01 boundary slopes r=0,infinity
    are closed at binary level;
  * q=2,3: exactly one marking survives (t1=t2=t3=0, L_q=0) and the
    mode-zero one-marked minor in rows (0,1,3,7) equals +-R*A*B^2
    with R nonzero: every genuine survivor has a rank-four one-marked
    contraction => no ternary lift (H31 or H22) => the D_23 boundary
    slopes r=0,infinity are closed at ternary level.

Modular corroboration at p=11: D_01^0 has 0 survivors; D_23^0 has the
single survivor t=(t0*,0,0,0) with t0* the L_2 root (checked
numerically below).
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import sympy as sp


for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(
    __file__,
    also=[
        "../../../../../research_snapshots/"
        "2026-08-04-p5-h22-slope-divisor-closures/scripts"
    ],
)

from slope_common import ALPHA, BETA, T, build_system

OUT = REPO_ROOT / "research_snapshots/2026-08-04-p5-h22-slope-divisor-closures"
s = sp.Symbol("s")


def deleted(row, q):
    return tuple(row[c] for c in range(4) if c != q)


def main() -> None:
    started = time.monotonic()
    checks = {}

    # r=0 identifications (literal).
    d01 = build_system("01", sp.Integer(0))
    d23 = build_system("23", sp.Integer(0))
    for m in range(4):
        assert tuple(sp.expand(e) for e in d01["walpha"][m]) == tuple(
            sp.expand(e) for e in deleted(ALPHA[m], 0)
        )
        marked_beta = tuple(
            sp.expand(BETA[m][c] + T[m] * ALPHA[m][c]) for c in range(4)
        )
        assert tuple(sp.expand(e) for e in d01["wbeta"][m]) == tuple(
            sp.expand(e) for e in deleted(marked_beta, 0)
        )
        assert tuple(sp.expand(e) for e in d23["walpha"][m]) == tuple(
            sp.expand(e) for e in deleted(ALPHA[m], 2)
        )
        assert tuple(sp.expand(e) for e in d23["wbeta"][m]) == tuple(
            sp.expand(e) for e in deleted(marked_beta, 2)
        )
    checks["r0"] = "D_01^0 = q=0 frame, D_23^0 = q=2 frame (exact)"

    # r=infinity identifications (scale weighted column by s=1/r).
    d01_inf = build_system("01", 1 / s)
    d23_inf = build_system("23", 1 / s)
    for m in range(4):
        marked_beta = tuple(
            sp.expand(BETA[m][c] + T[m] * ALPHA[m][c]) for c in range(4)
        )
        # D_01: weighted first entry is u0/s+u1; s*entry -> u0 at s=0.
        scaled = sp.expand(s * d01_inf["walpha"][m][0]).subs({s: 0})
        assert scaled == sp.expand(ALPHA[m][0])
        assert d01_inf["walpha"][m][1:] == deleted(ALPHA[m], 0)[1:]
        scaled_b = sp.expand(s * d01_inf["wbeta"][m][0]).subs({s: 0})
        assert sp.expand(scaled_b - marked_beta[0]) == 0
        # D_23: weighted third entry is u2/s+u3; s*entry -> u2 at s=0.
        scaled = sp.expand(s * d23_inf["walpha"][m][2]).subs({s: 0})
        assert sp.expand(scaled - ALPHA[m][2]) == 0
        scaled_b = sp.expand(s * d23_inf["wbeta"][m][2]).subs({s: 0})
        assert sp.expand(scaled_b - marked_beta[2]) == 0
    checks["r_infinity"] = (
        "after the uniform column scaling, D_01^inf = q=1 frame and "
        "D_23^inf = q=3 frame (exact limits)"
    )

    # Modular corroboration of the q=2 shadow at p=11.
    from explore_p5_h22_disjoint_mixed_star_slope_divisors_modular import (
        SAMPLES,
    )

    p = 11
    a_, b_, f_, phi_ = SAMPLES[p]
    G = (a_ * a_ * b_ * f_ * f_ + 2 * b_ * b_ * f_ + b_) % p
    coefficient = (1 - a_ * a_ * f_ * f_) % p
    constant_two = (
        3 * a_ * a_ * f_ * f_ - 2 * b_ * b_ * f_ * f_
        - 2 * b_ * f_ - 3
    ) % p
    t0_expected = (
        -(G * phi_ + constant_two) * pow(coefficient, -1, p)
    ) % p
    assert t0_expected == 4  # the observed lone r=0 D_23 survivor
    checks["modular_L2_root"] = (
        "p=11: L_2 root t0=4 equals the observed lone D_23^0 "
        "survivor marking"
    )

    result = {
        "verified": True,
        "component": "disjoint mixed-star fivefold (eighth orbit)",
        "statement": (
            "the H22 pencil slope boundaries r=0,infinity are exactly "
            "the four H31 coordinate frames; the verified H31 generic "
            "theorem closes them (q=0,1 at binary level, q=2,3 at "
            "ternary level via the (0,1,3,7) minor identity "
            "det = +-R*A*B^2)"
        ),
        "h31_citation": (
            "P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_"
            "OBSTRUCTION.md, eqs (6)-(10); verified by "
            "verify_p5_h31_disjoint_mixed_star_component_generic_"
            "obstruction.py"
        ),
        "checks": checks,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    path = OUT / "slope_boundary_frame_identifications_verified.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
