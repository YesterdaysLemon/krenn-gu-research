#!/usr/bin/env python3
"""Verify a ten-equation affine contradiction in one exact-three C10 support."""

from __future__ import annotations

import json
import re
from pathlib import Path

import sympy as sp

import generate_p5_exact_three_partial_support_system as GENERATOR


ROOT = Path(__file__).resolve().parent
CATALOGUE = (
    ROOT
    / "research_snapshots"
    / "2026-07-27-p5-coordinate-cegar"
    / "three_partial_c10_audit"
    / "sat_catalogue_c10.json"
)
SUPPORTS = (
    (6, 6, 1, 4, 1),
    (2, 7, 5, 1, 4),
    (4, 4, 7, 7, 2),
    (1, 2, 2, 7, 7),
    (7, 1, 4, 2, 7),
)
SIGNATURE_INDICES = (4784, 2458, 3717, 326, 5012)
CORE = {
    3: "1+u7*u16",
    8: "1+u10+u8*u16",
    21: "u7*u22+u7*u18+u1*u13+u1*u7*u15+u1*u7*u11",
    48: "u21+u16*u19+u9*u16+u6+u4*u5+u2*u5",
    49: "u22+u18+u9*u16+u6+u4*u5+u2*u5",
    66: "u21+u16*u19+u10+u8*u16+u3*u16",
    67: "u22+u10+u10*u18+u8*u16+u8*u16*u18+u3*u16",
    77: "1+u1",
    126: (
        "u15+u13*u22+u7*u22+u7*u15*u18+u7*u11*u22"
        "+u3*u22+u0*u7*u15+u0*u3*u15"
    ),
    138: (
        "u22+u16+u10*u18+u8*u16*u18+u0*u10"
        "+u0*u8*u16+u0*u3*u16"
    ),
}
REPRESENTATIVE_WORDS = {
    3: "00020",
    8: "00120",
    21: "01012",
    48: "02221",
    49: "02222",
    66: "10121",
    67: "10122",
    77: "11000",
    126: "20012",
    138: "20122",
}
IDEAL = re.compile(
    r"^ideal I=(?P<equations>.*?);$\n^ideal G=",
    re.MULTILINE | re.DOTALL,
)


def require_zero(expression: sp.Expr, label: str) -> None:
    if sp.expand(expression) != 0:
        raise AssertionError(f"symbolic identity failed: {label}")


def main() -> None:
    catalogue = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    catalogue_case = catalogue["cases"][384]
    if (
        catalogue_case.get("orbit_index") != 384
        or tuple(
            tuple(row) for row in catalogue_case.get("supports", ())
        )
        != SUPPORTS
        or tuple(
            catalogue_case.get("witness_signature_indices", ())
        )
        != SIGNATURE_INDICES
    ):
        raise AssertionError("catalogue orbit 384 changed")

    program, metadata = GENERATOR.generate(
        SUPPORTS, SIGNATURE_INDICES
    )
    ideal = IDEAL.search(program)
    if ideal is None:
        raise AssertionError("regenerated source has no recognizable ideal")
    equations = ideal.group("equations").split(",\n")
    mixed = equations[:-1]
    if metadata != {
        "nonzero_entries": 42,
        "gauge_free_variables": 23,
        "laurent_parameters": 23,
        "mixed_equations": 193,
        "pure_coefficients": 3,
    }:
        raise AssertionError(f"system metadata changed: {metadata}")
    for index, expected in CORE.items():
        if mixed[index] != expected:
            raise AssertionError(f"mixed equation {index} changed")

    u = sp.symbols("u0:23")
    local = {f"u{index}": symbol for index, symbol in enumerate(u)}
    f = {
        index: sp.sympify(text, locals=local)
        for index, text in CORE.items()
    }
    used_variables = sorted(
        set().union(*(polynomial.free_symbols for polynomial in f.values())),
        key=lambda symbol: int(symbol.name[1:]),
    )
    core_basis = sp.groebner(
        list(f.values()), *used_variables, order="grevlex"
    )
    if not (
        len(core_basis.polys) == 1
        and core_basis.polys[0].as_expr() == 1
    ):
        raise AssertionError("the ten-equation affine ideal is not unit")

    a = u[7]
    b = u[16]
    h = u[18]
    q = u[0] - 1
    r = u[1]
    s = u[3]
    t = u[22]
    ell = u[13] + a * u[15] + a * u[11]
    common = u[9] * b + u[6] + u[4] * u[5] + u[2] * u[5]
    root = u[21] + b * u[19]
    middle = u[10] + u[8] * b

    require_zero(f[3] - (1 + a * b), "F3 normal form")
    require_zero(f[8] - (1 + middle), "F8 normal form")
    require_zero(
        f[21] - (a * (t + h) + r * ell),
        "F21 normal form",
    )
    require_zero(f[48] - (root + common), "F48 normal form")
    require_zero(f[49] - (t + h + common), "F49 normal form")
    require_zero(
        f[66] - (root + middle + s * b),
        "F66 normal form",
    )
    require_zero(
        f[67] - (t + (1 + h) * middle + s * b),
        "F67 normal form",
    )
    require_zero(f[77] - (1 + r), "F77 normal form")
    require_zero(
        f[126]
        - (
            t * (u[13] + a + a * u[11] + s)
            + u[15] * (1 + a * h + u[0] * (a + s))
        ),
        "F126 normal form",
    )
    require_zero(
        f[138] - (t + b + h * middle + u[0] * (middle + s * b)),
        "F138 normal form",
    )

    residual = f[67] - (1 + h) * f[8]
    require_zero(residual - (t + s * b - 1 - h), "residual")
    require_zero(
        (f[66] - f[8])
        - (f[48] - f[49])
        - residual
        - 2 * h,
        "the first seven equations force 2h=0",
    )

    residual_h0 = sp.expand(residual.subs(h, 0))
    require_zero(
        f[138].subs(h, 0)
        - (b - q * t)
        - u[0] * (f[8] + residual_h0),
        "F138 forces b=q*t after h=0",
    )
    require_zero(
        f[21].subs({h: 0, r: -1}) - (a * t - ell),
        "F21 forces ell=a*t after h=0 and r=-1",
    )
    require_zero(
        f[126].subs(h, 0)
        - (
            t * (ell - a * u[15] + a + s)
            + u[15] * (1 + u[0] * (a + s))
        ),
        "F126 reduced form",
    )

    print(
        json.dumps(
            {
                "verified": True,
                "scope": (
                    "one exact-three-partial C10 P5 support orbit"
                ),
                "catalogue_orbit_index": 384,
                "full_mixed_equations": len(mixed),
                "core_mixed_equations": len(CORE),
                "core_representative_colour_words": list(
                    REPRESENTATIVE_WORDS.values()
                ),
                "uses_saturation_equation": False,
                "uses_pure_nonzero_assumptions": False,
                "sympy_core_groebner_basis": ["1"],
                "contradiction": (
                    "F126 reduces to 2*t*(a+s), while the other "
                    "nine equations force t and a+s nonzero"
                ),
                "excluded_characteristic": 2,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
