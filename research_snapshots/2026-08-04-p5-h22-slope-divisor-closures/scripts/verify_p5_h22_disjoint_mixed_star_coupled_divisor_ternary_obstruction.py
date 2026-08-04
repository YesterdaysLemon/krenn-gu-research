#!/usr/bin/env python3
"""ALTERNATIVE DESIGN (full 8-slot z-system): superseded by the
reduced-system certificate in
verify_p5_h22_disjoint_mixed_star_special_slope_reduced_fitting.py
(case 'coupled'), which works on the y-eliminated 10x4 system in four
x-variables and is much smaller.  Kept for the record; not part of
the certified chain.

Attempted exact closure of the coupled slope divisor
af(r+1)-(r-1)=0 of the D_01 pencil on the disjoint mixed-star
component (weighted H22).

On this divisor (parametrized inside C(a,b,f) by the rational slope
r_c=(af+1)/(1-af)):
  * the generic theorem's global one-minor marking certificate
    degenerates (its unit factor list contains af(r+1)-(r-1));
  * the sheet-t2 branch marking escapes to t_1=infinity (the branch is
    empty since r_c+1=2/(1-af) != 0);
  * modular reconnaissance finds four genuine survivor markings, one
    of which (t_1=t_2=t_3=0, special t_0) has mode-ZERO one-marked
    rank THREE -- the generic mode-zero Fitting obstruction genuinely
    fails there;
  * but the mode-THREE one-marked contraction has rank four on every
    genuine survivor, with common nonzero minors
    (0,2,4,7),(0,2,6,7),(0,3,5,7),(0,4,5,7),(0,4,6,7).

Certificate attempted here (single chart-free Fitting run):

  ideal(14 mixed rows at r_c, Phi,
        det N_3[0,2,4,7], det N_3[0,4,5,7],
        w*A*B-1)  ==  (1)

over (0,a,b,f) in (phi,t0..t3,z,w).  Unit => every genuine binary
survivor on the divisor has a rank-four mode-three one-marked
contraction => no ternary H22 lift => the coupled divisor is closed
at ternary level over the generic component point.

Timeout policy: 550 s; a timeout is recorded as a NULL result
(fail-closed), not a claim.
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
    MIXED,
    PHI,
    T,
    Z,
    a,
    b,
    build_system,
    f,
    one_marked,
    phi_normal_form,
    resultant_certificate,
    sing,
)

OUT = Path(__file__).resolve().parent.parent
TIMEOUT = 550
MODE = 3
MINOR_ROWS = ((0, 2, 4, 7), (0, 4, 5, 7))
BITS3 = tuple((i >> 2 & 1, i >> 1 & 1, i & 1) for i in range(8))


def clear_denominators(expr, allowed=(a * f - 1,)):
    """Uniformly clear the denominator of a (linear-form) expression;
    assert the denominator is invertible on the component."""
    together = sp.together(sp.expand(expr))
    numerator, denominator = sp.fraction(together)
    if denominator != 1:
        content = sp.factor(denominator)
        # denominator must be an integer times powers of allowed units
        test = content
        for unit in allowed:
            for _ in range(16):
                q = sp.simplify(test / unit)
                num2, den2 = sp.fraction(sp.together(q))
                if den2 == 1:
                    test = sp.expand(num2)
                else:
                    break
        assert test.is_number, (denominator, test)
    return sp.expand(numerator)


def main() -> None:
    started = time.monotonic()
    slope = (a * f + 1) / (1 - a * f)
    # on-divisor sanity
    assert sp.simplify(a * f * (slope + 1) - (slope - 1)) == 0
    # (af-1) is a unit on the component
    unit_cert = resultant_certificate(a * f - 1)

    data = build_system("01", slope)
    lin = []
    for bits in MIXED:
        row_expr = sum(
            c * zv for c, zv in zip(data["rows"][bits], Z)
        )
        lin.append(clear_denominators(row_expr))
    A = clear_denominators(
        sum(c * zv for c, zv in zip(data["A"], Z))
    )
    B = clear_denominators(
        sum(c * zv for c, zv in zip(data["B"], Z))
    )
    minors = []
    cache = {}
    for selected in MINOR_ROWS:
        entries = []
        for index in selected:
            bits3 = BITS3[index]
            if bits3 not in cache:
                cache[bits3] = [
                    clear_denominators(e)
                    for e in one_marked(data, MODE, bits3)
                ]
            entries.append(cache[bits3])
        minors.append(sp.expand(sp.Matrix(entries).det()))

    variables = (
        "phi,"
        + ",".join(str(t) for t in T)
        + ","
        + ",".join(str(z) for z in Z)
        + ",w"
    )
    program = "\n".join(
        [
            f"ring R=(0,a,b,f),({variables}),dp;",
            "option(redSB);",
            "ideal I=" + ",".join(sing(e) for e in lin) + ";",
            f"I=I,{sing(PHI)};",
            f"I=I,{sing(minors[0])};",
            f"I=I,{sing(minors[1])};",
            f"I=I,w*({sing(A)})*({sing(B)})-1;",
            "I=std(I);",
            '"CODEX_RESULT:coupled:"+string(reduce(1,I)==0);',
            "quit;",
        ]
    )
    status = None
    try:
        completed = subprocess.run(
            ("Singular", "-q"),
            input=program,
            text=True,
            capture_output=True,
            timeout=TIMEOUT,
        )
        if completed.returncode != 0 or completed.stderr.strip():
            status = {
                "result": "error",
                "returncode": completed.returncode,
                "stderr": completed.stderr[-1000:],
            }
        elif "CODEX_RESULT:coupled:1" in completed.stdout:
            status = {"result": "unit"}
        else:
            status = {
                "result": "not-unit",
                "stdout": completed.stdout[-1000:],
            }
    except subprocess.TimeoutExpired:
        subprocess.run(("pkill", "-9", "Singular"), check=False)
        status = {"result": "timeout-null", "timeout_s": TIMEOUT}

    result = {
        "divisor": "af(r+1)-(r-1)=0 (D_01 pencil)",
        "slope_parametrization": "r_c=(af+1)/(1-af)",
        "component": "disjoint mixed-star fivefold (eighth orbit)",
        "unit_certificate_af_minus_1": unit_cert,
        "certificate": {
            "mode": MODE,
            "minor_rows": [list(r_) for r_ in MINOR_ROWS],
            "form": (
                "ideal(14 rows at r_c, Phi, two mode-3 minors, "
                "w*A*B-1) over all markings"
            ),
            "status": status,
        },
        "modular_context": (
            "four genuine survivor markings on the divisor at "
            "p=11,13; one has mode-zero marked rank 3 (generic "
            "mode-zero certificate fails); all have mode-three rank 4 "
            "with the selected minors nonzero"
        ),
        "verified": status is not None and status.get("result") == "unit",
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    path = OUT / "coupled_divisor_ternary_obstruction_result.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
