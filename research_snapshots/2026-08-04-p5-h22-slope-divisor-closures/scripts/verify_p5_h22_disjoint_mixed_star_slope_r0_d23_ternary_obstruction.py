#!/usr/bin/env python3
"""SUPERSEDED / NULL RESULT: this first design (chart certificates +
sheet Fitting on the full 14x8 system) exceeded the 550 s Singular
budget on its first chart and was abandoned (fail-closed null).  The
working certificate is the reduced-system chart-free run in
verify_p5_h22_disjoint_mixed_star_special_slope_reduced_fitting.py
(case r0).  Kept for the record.

Original description: exact closure of the torus-boundary slope r=0
of the D_23 pencil on the disjoint mixed-star component (weighted
H22).

At r=0 the weighted deletion D_23^0(u)=(u_0,u_1,u_3,ext) IS the H31
q=2 coordinate frame (delete source coordinate 2, adjoin the fifth
coordinate).  Unlike r=+-1, genuine binary survivors EXIST at r=0
(the H31 theorem's q=2 marking), so the closure is ternary:

  (C1) three chart certificates: for each i in {1,2,3}, the ideal
       (14 mixed rows at r=0, Phi, w*A*B-1, s*t_i-1) is unit, so every
       genuine binary marking satisfies t_1=t_2=t_3=0 (t_0 free);
  (C2) one Fitting certificate on that sheet: adding the mode-zero
       one-marked minors in rows (0,1,3,7) and (0,1,5,7) (the same
       rows as the generic theorem) plus the Rabinowitsch inversion
       of A*B yields the unit ideal.

Hence every genuine binary survivor of the D_23 pencil at r=0 has a
rank-four mode-zero one-marked contraction and admits no ternary lift:
the r=0 boundary slope of the D_23 pencil is closed at ternary level
over the generic component point.  This is the weighted-H22 shadow of
the H31 generic theorem's q=2 obstruction (whose selected minor rows
(0,1,3,7) and identity det = R*A*B^2 live in the same frame).
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sympy as sp

from slope_common import (
    ALPHA,
    BETA,
    MIXED,
    PHI,
    T,
    Z,
    build_system,
    one_marked_mode_zero,
    phi_normal_form,
    sing,
)

OUT = Path(__file__).resolve().parent.parent
TIMEOUT = 550
FITTING_ROWS = ((0, 1, 3, 7), (0, 1, 5, 7))
BITS3 = tuple(
    (i >> 2 & 1, i >> 1 & 1, i & 1) for i in range(8)
)


def run_singular(program, label):
    completed = subprocess.run(
        ("Singular", "-q"),
        input=program,
        text=True,
        capture_output=True,
        timeout=TIMEOUT,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (label, completed.returncode, completed.stdout[-2000:],
             completed.stderr[-2000:])
        )
    return completed.stdout


def main() -> None:
    started = time.monotonic()
    data = build_system("23", sp.Integer(0))

    # Frame identification: D_23^0 deletes source coordinate 2.
    for m in range(4):
        assert data["walpha"][m] == (
            ALPHA[m][0], ALPHA[m][1], sp.expand(ALPHA[m][3])
        )
    certificates = {
        "frame": "D_23^0 = H31 q=2 coordinate frame (u0,u1,u3,ext)"
    }

    lin = []
    for bits in MIXED:
        lin.append(sum(c * zv for c, zv in zip(data["rows"][bits], Z)))
    A = sum(c * zv for c, zv in zip(data["A"], Z))
    B = sum(c * zv for c, zv in zip(data["B"], Z))

    variables = (
        "phi,"
        + ",".join(str(t) for t in T)
        + ","
        + ",".join(str(z) for z in Z)
        + ",w,s"
    )

    # (C1) chart certificates.
    for i in (1, 2, 3):
        program = "\n".join(
            [
                f"ring R=(0,a,b,f),({variables}),dp;",
                "option(redSB);",
                "ideal I=" + ",".join(sing(e) for e in lin) + ";",
                f"I=I,{sing(PHI)};",
                f"I=I,w*({sing(A)})*({sing(B)})-1;",
                f"I=I,s*t{i}-1;",
                "I=std(I);",
                f'"CODEX_RESULT:t{i}:"+string(reduce(1,I)==0);',
                "quit;",
            ]
        )
        output = run_singular(program, f"chart t{i}")
        assert f"CODEX_RESULT:t{i}:1" in output, output
        certificates[f"chart_t{i}"] = "unit ideal"

    # (C2) Fitting certificate on t1=t2=t3=0.
    sheet = {T[1]: 0, T[2]: 0, T[3]: 0}
    lin_sheet = [sp.expand(e.subs(sheet)) for e in lin]
    A_sheet = sp.expand(A.subs(sheet))
    B_sheet = sp.expand(B.subs(sheet))
    minors = []
    marked_cache = {}
    for selected in FITTING_ROWS:
        entries = []
        for index in selected:
            bits3 = BITS3[index]
            if bits3 not in marked_cache:
                row = one_marked_mode_zero(data, bits3)
                marked_cache[bits3] = [
                    sp.expand(entry.subs(sheet)) for entry in row
                ]
            entries.append(marked_cache[bits3])
        matrix = sp.Matrix(entries)
        minors.append(sp.expand(matrix.det()))
    variables2 = (
        "phi,t0,"
        + ",".join(str(z) for z in Z)
        + ",w"
    )
    program = "\n".join(
        [
            f"ring R=(0,a,b,f),({variables2}),dp;",
            "option(redSB);",
            "ideal I=" + ",".join(sing(e) for e in lin_sheet) + ";",
            f"I=I,{sing(PHI)};",
            f"I=I,{sing(minors[0])};",
            f"I=I,{sing(minors[1])};",
            f"I=I,w*({sing(A_sheet)})*({sing(B_sheet)})-1;",
            "I=std(I);",
            '"CODEX_RESULT:fitting:"+string(reduce(1,I)==0);',
            "quit;",
        ]
    )
    output = run_singular(program, "fitting sheet")
    assert "CODEX_RESULT:fitting:1" in output, output
    certificates["fitting_t1t2t3_zero"] = (
        "unit ideal with mode-zero minors (0,1,3,7),(0,1,5,7)"
    )

    result = {
        "verified": True,
        "field": "C(a,b,f)[phi]/(Phi), slope fixed at r=0 (torus "
                 "boundary of the D_23 pencil)",
        "component": "disjoint mixed-star fivefold (eighth orbit)",
        "statement": (
            "every genuine binary survivor of the D_23 pencil at r=0 "
            "lies on t1=t2=t3=0 and has a rank-four mode-zero "
            "one-marked contraction: no ternary lift; the r=0 "
            "boundary slope is closed over the generic component "
            "point"
        ),
        "h31_shadow": (
            "the frame equals the H31 q=2 slice; the H31 generic "
            "theorem's marking (t1=t2=t3=0, L_2=0) and minor rows "
            "(0,1,3,7) reappear here"
        ),
        "certificates": certificates,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    path = OUT / "r0_d23_ternary_obstruction_verified.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
