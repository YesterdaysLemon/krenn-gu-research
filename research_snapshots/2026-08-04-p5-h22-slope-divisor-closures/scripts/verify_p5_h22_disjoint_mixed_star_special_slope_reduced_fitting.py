#!/usr/bin/env python3
"""Chart-free ternary Fitting certificates on the y-ELIMINATED reduced
system for the two special slopes of the disjoint mixed-star weighted
H22 theorem where genuine binary survivors exist:

  (A) D_23 at r=0   (torus boundary; = H31 q=2 frame): mode-0 minors
      rows (0,1,3,7),(0,1,5,7);
  (B) D_01 on the coupled divisor af(r+1)-(r-1)=0, parametrized by
      r_c=(af+1)/(1-af): mode-3 minors rows (0,2,4,7),(0,4,5,7)
      (the generic mode-0 certificate provably fails on one survivor
      there: its mode-0 one-marked rank drops to three).

Validity of the reduction at these slopes: the four single-1-word
own-extension denominators of the generic theorem are all NONZERO at
r=0 (their (r-1),(r+1) factors evaluate to -1,+1) and on the coupled
divisor (r_c-1=2af/(1-af), r_c+1=2/(1-af)); each substituted
denominator gets a fresh resultant certificate below.  Hence the
14 x 8 mixed kernel is isomorphic to the kernel of the reduced 10 x 4
system G(t)x=0, exactly as in the generic theorem.

Certificate shape (per case): over (0,a,b,f) in variables
(phi,t0,t1,t2,t3,x0..x3,w),

  ideal( G(t)x rows, Phi, det Dm[rows_1], det Dm[rows_2],
         w*A(x)*B(x)-1 ) == (1),

with Dm the mode-m one-marked 4x4 matrices on the kernel substitution
and A,B the two diagonals.  Unit ideal => every genuine binary
survivor AT EVERY MARKING has a rank-four mode-m one-marked
contraction => no ternary H22 lift => the slope locus is closed at
ternary level over the generic component point.

Timeout policy: 550 s per Singular run; timeouts recorded as NULL
results (fail-closed)."""

from __future__ import annotations

import itertools
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

import sympy as sp

import verify_p5_h22_disjoint_mixed_star_component_generic_obstruction as V

OUT = Path(__file__).resolve().parent.parent
TIMEOUT = 550
BITS3 = tuple(itertools.product((0, 1), repeat=3))

a, b, f, phi, r = V.a, V.b, V.f, V.phi, V.r
T, X = V.T, V.X
w = V.w
PHI = V.PHI


def clear_row(expr, unit=(a * f - 1)):
    """Uniformly clear the denominator of an expression; the
    denominator must be an integer times a power of `unit`."""
    together = sp.together(sp.expand(expr))
    numerator, denominator = sp.fraction(together)
    if denominator != 1:
        test = sp.factor(denominator)
        for _ in range(64):
            if test.is_number:
                break
            quotient = sp.cancel(test / unit)
            n2, d2 = sp.fraction(sp.together(quotient))
            assert d2 == 1, (denominator, test)
            test = sp.factor(n2)
        assert test.is_number, (denominator, test)
    return sp.expand(numerator)


def clear_family(entries, unit=(a * f - 1)):
    """Scale a family of expressions by ONE common factor (a power of
    `unit` times an integer) that clears all denominators.  Implemented
    by tagging: the tagged sum is cleared uniformly by construction."""
    tags = [sp.Symbol(f"__tag{i}") for i in range(len(entries))]
    tagged = sum(e * tag for e, tag in zip(entries, tags))
    cleared = sp.expand(clear_row(tagged, unit))
    out = []
    for tag in tags:
        component = sp.expand(sp.diff(cleared, tag))
        assert not (
            set(component.free_symbols) & set(tags)
        )
        out.append(component)
    return out


def marked_matrix_entries(alpha_rows, beta_rows, mode, selected):
    """The sixteen entries of the selected 4 rows of the mode-`mode`
    one-marked map, each matrix row denominator-cleared by one common
    factor (row scaling) and the sixteen entries phi-reduced with one
    uniform unit factor (matrix scaling), so the determinant changes
    only by a unit.  The determinant itself is computed by Singular."""
    others = tuple(m for m in range(4) if m != mode)
    entries = []
    for index in selected:
        bits = BITS3[index]
        chosen = tuple(
            beta_rows[m] if bit else alpha_rows[m]
            for m, bit in zip(others, bits)
        )
        row = []
        for col in range(4):
            basis = tuple(sp.Integer(int(i == col)) for i in range(4))
            row.append(V.perm4((basis,) + chosen))
        entries.extend(clear_family(row))
    return V.phi_reduce_uniform(entries)


def certify(direction, slope, mode, minor_rows, label):
    data = V.build_direction(direction)
    # denominators at the special slope are units
    denominator_certs = {}
    for m, den in sorted(data["denominators"].items()):
        value = sp.expand(den.subs({r: slope}))
        value = clear_row(value)
        reduced = V.phi_normal_form(value)
        assert reduced != 0
        if phi in reduced.free_symbols:
            res = sp.factor(sp.resultant(
                sp.Poly(reduced, phi), sp.Poly(PHI, phi)))
        else:
            res = sp.factor(reduced)
        assert res != 0
        denominator_certs[str(m)] = str(res)[:200]
    # substituted reduced system; each G row is denominator-cleared by
    # one common factor and phi-reduced with one uniform unit factor
    # per row (row scalings), then assembled.
    g_red = []
    for grow in data["g_matrix"]:
        entries = clear_family([
            sp.expand(entry.subs({r: slope})) for entry in grow
        ])
        entries = V.phi_reduce_uniform(entries)
        g_red.append(sp.expand(
            sum(entry * xv for entry, xv in zip(entries, X))
        ))
    alpha_rows = tuple(
        tuple(sp.expand(sp.sympify(e).subs({r: slope}))
              for e in row)
        for row in data["alpha_rows"]
    )
    beta_rows = tuple(
        tuple(sp.expand(sp.sympify(e).subs({r: slope}))
              for e in row)
        for row in data["beta_rows"]
    )
    minor_matrices = [
        marked_matrix_entries(alpha_rows, beta_rows, mode, selected)
        for selected in minor_rows
    ]
    diag_a = V.phi_normal_form(clear_row(
        V.perm4(tuple(alpha_rows[m] for m in range(4)))
    ))
    diag_b = V.phi_normal_form(clear_row(
        V.perm4(tuple(beta_rows[m] for m in range(4)))
    ))
    variables = (
        "phi,t0,t1,t2,t3,"
        + ",".join(str(x) for x in X)
        + ",w"
    )
    lines = [
        f"ring R=(0,a,b,f),({variables}),dp;",
        "option(redSB);",
        "ideal I=" + ",".join(V.sing(e) for e in g_red) + ";",
        f"I=I,{V.sing(PHI)};",
    ]
    for index, entries in enumerate(minor_matrices):
        flat = ",".join(V.sing(entry) for entry in entries)
        lines.append(f"matrix D{index}[4][4]={flat};")
        lines.append(f"I=I,det(D{index});")
    lines.extend(
        [
            f"poly AB=({V.sing(diag_a)})*({V.sing(diag_b)});",
            "I=I,w*AB-1;",
            "I=std(I);",
            f'"CODEX_RESULT:{label}:"+string(reduce(1,I)==0);',
            "quit;",
        ]
    )
    program = "\n".join(lines)
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
                "stderr": completed.stderr[-800:],
            }
        elif f"CODEX_RESULT:{label}:1" in completed.stdout:
            status = {"result": "unit"}
        else:
            status = {
                "result": "not-unit",
                "stdout": completed.stdout[-800:],
            }
    except subprocess.TimeoutExpired:
        subprocess.run(("pkill", "-9", "Singular"), check=False)
        status = {"result": "timeout-null", "timeout_s": TIMEOUT}
    return {
        "direction": direction,
        "slope": str(slope),
        "mode": mode,
        "minor_rows": [list(m_) for m_ in minor_rows],
        "denominator_unit_certificates": denominator_certs,
        "status": status,
    }


def main() -> None:
    started = time.monotonic()
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    results = {}
    if which in ("r0", "both"):
        results["d23_r0"] = certify(
            "23", sp.Integer(0), 0,
            ((0, 1, 3, 7), (0, 1, 5, 7)), "d23-r0",
        )
        print(json.dumps(results["d23_r0"]["status"]))
    if which in ("coupled", "both"):
        results["d01_coupled"] = certify(
            "01", (a * f + 1) / (1 - a * f), 3,
            ((0, 2, 4, 7), (0, 4, 5, 7)), "d01-coupled",
        )
        print(json.dumps(results["d01_coupled"]["status"]))
    results["elapsed_seconds"] = round(time.monotonic() - started, 3)
    path = OUT / "special_slope_reduced_fitting_results.json"
    merged = {}
    if path.exists():
        merged = json.loads(path.read_text())
    merged.update(results)
    path.write_text(json.dumps(merged, indent=2) + "\n")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
