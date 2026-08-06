#!/usr/bin/env python3
"""Verify the generic weighted H22 obstruction on the tenth
(coincident-support) pure-compression component.

Self-contained (sympy + Singular on PATH).  Identities are exact over
Z[b,e,k,m,c,r,t]; the four Groebner projections are over C(b,e,m,c,r) and,
for the special slopes 1,-1,0, over C(b,e,m,c).  Fail-closed.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import time
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def find_root() -> Path:
    for candidate in (HERE, *HERE.parents):
        if (candidate / "P4_INOUT_PATH_STRATUM_WORKING_NOTE.md").exists():
            return candidate
    return HERE


ROOT = find_root()
THEOREM = HERE / "P5_H22_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md"
COMPANION = HERE / "P5_H31_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md"
COMPONENT = ROOT / "P4_INOUT_PATH_STRATUM_WORKING_NOTE.md"
COMPONENT_PRIMARY = ROOT / "branch_ambient_certificates.py"

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))
PERMS4 = tuple(itertools.permutations(range(4)))

b, e, k, m, c, r = sp.symbols("b e k m c r")
P = b * e * c + b + e
Q = b * e * (m + 1)
ASTAR = 2 * b * c * e - (b + e) * (m - 1)
T = sp.symbols("t0:4")
Z = sp.symbols("x0:4") + sp.symbols("y0:4")
W = sp.Symbol("w")

SINGULAR_TIMEOUT = 550
WITNESS_ROWS = (0, 1, 3, 4, 5, 7, 8)
WITNESS_COLS = (0, 1, 2, 3, 4, 5, 6)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(4)) for p in PERMS4))


def concentrated_basis(kk):
    alpha = ((1, -1, 0, 0), (1, -1, 0, 0), (0, 0, 1, kk),
             (P, P * m - Q * c, -Q, Q * kk))
    beta = ((0, 1, b, -b * kk), (0, 1, e, -e * kk), (1, 1, 0, 0), (0, c, 1, -kk))
    return alpha, beta


def marked_beta(alpha, beta):
    return tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                 for i in range(4))


def diag_row(row, ext, pencil, slope):
    if pencil == "01":
        return (slope * row[0] + row[1], row[2], row[3], ext)
    if pencil == "23":
        return (row[0], row[1], slope * row[2] + row[3], ext)
    raise ValueError(pencil)


def pencil_words(pencil, kk, slope):
    alpha, beta = concentrated_basis(kk)
    betat = marked_beta(alpha, beta)
    alpha_d = tuple(diag_row(alpha[i], Z[i], pencil, slope) for i in range(4))
    beta_d = tuple(diag_row(betat[i], Z[4 + i], pencil, slope) for i in range(4))
    words = {wd: perm4(tuple(beta_d[i] if wd[i] else alpha_d[i] for i in range(4)))
             for wd in WORDS}
    return alpha, betat, words


def check_pure_normal_form():
    alpha, beta = concentrated_basis(k)
    tensor = {wd: perm4(tuple(beta[i] if wd[i] else alpha[i] for i in range(4)))
              for wd in WORDS}
    assert sp.expand(tensor[(1, 1, 1, 1)] + 2 * k * P) == 0
    assert all(sp.expand(v) == 0 for wd, v in tensor.items() if wd != (1, 1, 1, 1))


def check_01_identity():
    _, _, words = pencil_words("01", k, r)
    assert sp.expand(words[(0, 0, 0, 0)]) == 0
    # mechanisms
    alpha, _ = concentrated_basis(k)
    assert alpha[0] == alpha[1] == (1, -1, 0, 0)
    assert sp.expand(alpha[2][2] * alpha[3][3] + alpha[2][3] * alpha[3][2]) == 0


def check_23_structure():
    alpha, betat, words = pencil_words("23", k, r)
    arow = tuple(sp.expand(sp.diff(words[(0, 0, 0, 0)], zz)) for zz in Z)
    expected = tuple(sp.expand(v) for v in (
        -(k + r) * ASTAR, -(k + r) * ASTAR, 2 * Q * (r - k), -2 * (k + r),
        0, 0, 0, 0))
    assert arow == expected, arow
    assert all(sp.diff(x, ti) == 0 for x in arow for ti in T)

    # doubled-column identity
    for wd in WORDS:
        rows = tuple(betat[i] if wd[i] else alpha[i] for i in range(4))
        d2 = perm4(tuple((row[0], row[1], row[2], row[2]) for row in rows))
        d3 = perm4(tuple((row[0], row[1], row[3], row[3]) for row in rows))
        value = sp.expand(d3 + k**2 * d2)
        if wd == (1, 1, 1, 1):
            assert sp.expand(value - 4 * k**2 * P) == 0
        else:
            assert value == 0, wd

    # universal kernel z*
    sub = {Z[i]: r * alpha[i][3] + k**2 * alpha[i][2] for i in range(4)}
    sub.update({Z[4 + i]: r * betat[i][3] + k**2 * betat[i][2] for i in range(4)})
    for wd in WORDS:
        value = sp.expand(words[wd].subs(sub))
        if wd == (1, 1, 1, 1):
            assert sp.expand(value + 2 * k * P * (r - k) ** 2) == 0
        else:
            assert value == 0, wd

    # rank-7 witness at t=0, k=1
    zero = {ti: 0 for ti in T}
    one = {k: 1}
    matrix = sp.Matrix([[sp.diff(words[wd].subs(zero).subs(one), zz) for zz in Z]
                        for wd in MIXED])
    minor = sp.factor(matrix[list(WITNESS_ROWS), list(WITNESS_COLS)].det())
    expected_minor = -4 * b * c**2 * e**3 * (m + 1)**2 * (r - 1)**3 * (r + 1)**4 * P
    assert sp.expand(minor - expected_minor) == 0, minor
    return str(sp.factor(expected_minor))


def singular_str(expr):
    return str(sp.expand(expr)).replace("**", "^")


def run_singular(program: str, timeout: float):
    start = time.time()
    completed = subprocess.run(
        ["Singular", "-q"],
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout + 10,
    )
    elapsed = time.time() - start
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            ("Singular failure", completed.returncode, completed.stdout[-2000:],
             completed.stderr[:2000])
        )
    return completed.stdout, elapsed


def run_projection(slope_value):
    generic = slope_value is None
    slope = r if generic else sp.Integer(slope_value)
    _, _, words = pencil_words("23", sp.Integer(1), slope)
    equations = [words[wd] for wd in MIXED]
    equations.append(words[(0, 0, 0, 0)] - 1)
    equations.append(W * words[(1, 1, 1, 1)] - 1)
    eliminated = Z + (W,)
    variables = eliminated + T
    parameters = "b,e,m,c,r" if generic else "b,e,m,c"
    program = "\n".join((
        f"ring R=(0,{parameters}),(" + ",".join(map(str, variables))
        + "),(dp(9),dp(4));",
        "option(redSB);",
        "ideal incidence=" + ",".join(singular_str(x) for x in equations) + ";",
        "ideal basis=std(incidence);",
        "ideal marking=eliminate(basis," + "*".join(map(str, eliminated)) + ");",
        "marking=std(marking);",
        '"MARKING";',
        "marking;",
        "quit;",
    ))
    stdout, elapsed = run_singular(program, SINGULAR_TIMEOUT)
    generators = tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in stdout.replace("\r\n", "\n").splitlines()
        if line.startswith("marking[")
    )
    return generators, elapsed


# --------------------------------------------------------------------------
# Interior parameter divisors {c=0} and {b+e=0}: D_23 sheet projections
# (slope-free sheets) and per-sheet ternary Fitting closures (mode-2
# one-marked minors, A=1 normalization).  The D_01 pencil needs no divisor
# work: its identity holds at every chart point.
# --------------------------------------------------------------------------

WORDS3 = tuple(itertools.product((0, 1), repeat=3))
DIVISOR_SHEETS = {
    "c=0": (
        "t3",
        "t2",
        "(e^2*m+e^2)*t0+(b^2*m+b^2)*t1+(-b^2+b*e*m-b*e-e^2)",
        "(b^2*m^2-b^2)*t1^2+(2*b^2+b*e*m^2-2*b*e*m+b*e-2*e^2*m)*t1"
        "+(-b^2+b*e*m-b*e+e^2*m)",
    ),
    "b+e=0": (
        "(2*b^2)*t3+1",
        "t2",
        "t0+t1-1",
        "t1^2-t1",
    ),
}
DIVISOR_PARAMS = {"c=0": "b,e,m,r", "b+e=0": "b,m,c,r"}
DIVISOR_SUBS = {"c=0": {c: 0}, "b+e=0": {e: -b}}
MINOR_ROWS = ((0, 1, 2, 7), (0, 1, 3, 7))
MARKED_MODE = 2


def d23_divisor_frame(divisor, tvals):
    sub = DIVISOR_SUBS[divisor]
    alpha, beta = concentrated_basis(sp.Integer(1))
    alpha = tuple(tuple(sp.expand(sp.sympify(x).subs(sub)) for x in row)
                  for row in alpha)
    beta = tuple(tuple(sp.expand(sp.sympify(x).subs(sub)) for x in row)
                 for row in beta)
    betat = []
    for i in range(4):
        row = tuple(sp.together(beta[i][j] + tvals[i] * alpha[i][j])
                    for j in range(4))
        lcm = sp.lcm([sp.fraction(sp.cancel(x))[1] for x in row])
        betat.append(tuple(sp.expand(sp.cancel(x * lcm)) for x in row))
    betat = tuple(betat)

    def drow(row, ext):
        return (row[0], row[1], sp.expand(r * row[2] + row[3]), ext)

    alpha_p = tuple(drow(alpha[i], Z[i]) for i in range(4))
    beta_p = tuple(drow(betat[i], Z[4 + i]) for i in range(4))
    forms = {wd: sp.expand(perm4(tuple(beta_p[i] if wd[i] else alpha_p[i]
                                       for i in range(4)))) for wd in WORDS}
    return forms, alpha_p, beta_p


def one_marked_map(mode, alpha_p, beta_p):
    rows = []
    for bits in WORDS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta_p[other] if bits[bit_index] else alpha_p[other])
                bit_index += 1
        row = []
        for coordinate in range(4):
            basis = tuple(int(idx == coordinate) for idx in range(4))
            row.append(perm4(tuple(basis if other == mode else selected[other]
                                   for other in range(4))))
        rows.append(row)
    return sp.Matrix(rows)


def d23_divisor_sheet_projection(divisor):
    forms, _, _ = d23_divisor_frame(divisor, T)
    equations = [forms[wd] for wd in MIXED]
    equations.append(forms[(0, 0, 0, 0)] - 1)
    equations.append(W * forms[(1, 1, 1, 1)] - 1)
    eliminated = Z + (W,)
    variables = eliminated + T
    program = "\n".join((
        f"ring R=(0,{DIVISOR_PARAMS[divisor]}),("
        + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
        "option(redSB);",
        "ideal I=" + ",".join(singular_str(x) for x in equations) + ";",
        "ideal J=std(I);",
        "ideal L=eliminate(J," + "*".join(map(str, eliminated)) + ");",
        "L=std(L);",
        '"SHEETS";',
        "L;",
        "quit;",
    ))
    stdout, elapsed = run_singular(program, SINGULAR_TIMEOUT)
    generators = tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in stdout.replace("\r\n", "\n").splitlines()
        if line.startswith("L[")
    )
    return generators, elapsed


def d23_divisor_fitting(divisor, tvals, extra_vars=(), extra_eqs=()):
    forms, alpha_p, beta_p = d23_divisor_frame(divisor, tvals)
    marked = one_marked_map(MARKED_MODE, alpha_p, beta_p)
    minors = [sp.expand(marked[list(rows_), :].det()) for rows_ in MINOR_ROWS]
    equations = [forms[wd] for wd in MIXED] + minors + list(extra_eqs)
    equations.append(forms[(0, 0, 0, 0)] - 1)
    equations.append(W * forms[(1, 1, 1, 1)] - 1)
    variables = list(map(str, Z + (W,))) + [str(v) for v in extra_vars]
    order = f"(dp(9),dp({len(extra_vars)}))" if extra_vars else "dp"
    program = "\n".join((
        f"ring R=(0,{DIVISOR_PARAMS[divisor]}),("
        + ",".join(variables) + f"),{order};",
        "ideal I=" + ",".join(singular_str(x) for x in equations) + ";",
        "I=std(I);",
        "int unit=(reduce(1,I)==0);",
        '"UNIT:"+string(unit);',
        "quit;",
    ))
    stdout, elapsed = run_singular(program, SINGULAR_TIMEOUT)
    lines = [ln.strip() for ln in stdout.splitlines() if ln.startswith("UNIT:")]
    assert lines == ["UNIT:1"], (divisor, lines, stdout[-800:])
    return elapsed


def run_d23_divisor_closures():
    results = {}
    s0, s1 = sp.symbols("s0 s1")
    lin = (e**2 * m + e**2) * s0 + (b**2 * m + b**2) * s1 \
        + (-b**2 + b * e * m - b * e - e**2)
    quad = (b**2 * m**2 - b**2) * s1**2 \
        + (2 * b**2 + b * e * m**2 - 2 * b * e * m + b * e - 2 * e**2 * m) * s1 \
        + (-b**2 + b * e * m - b * e + e**2 * m)
    for divisor in ("c=0", "b+e=0"):
        generators, elapsed = d23_divisor_sheet_projection(divisor)
        assert generators == DIVISOR_SHEETS[divisor], (divisor, generators)
        certificates = {}
        if divisor == "b+e=0":
            t3v = sp.Rational(-1, 2) / b**2
            for t1v, name in ((0, "t=(1,0,0,-1/(2b^2))"),
                              (1, "t=(0,1,0,-1/(2b^2))")):
                dt = d23_divisor_fitting(divisor, (1 - t1v, t1v, 0, t3v))
                certificates[name] = {"unit": True, "seconds": round(dt, 2)}
        else:
            dt = d23_divisor_fitting(divisor, (s0, s1, 0, 0),
                                     extra_vars=(s0, s1), extra_eqs=(lin, quad))
            certificates["t2=t3=0, (t0,t1) on lin+quad"] = {
                "unit": True, "seconds": round(dt, 2)}
        results[divisor] = {
            "sheet_ideal_slope_free": list(generators),
            "sheet_projection_seconds": round(elapsed, 2),
            "mode2_minors": [list(rows_) for rows_ in MINOR_ROWS],
            "fitting_certificates": certificates,
        }
    return results


def main() -> None:
    check_pure_normal_form()
    check_01_identity()
    witness = check_23_structure()

    labels = {None: "generic", 1: "r=1", -1: "r=-1", 0: "r=0"}
    projections = {}
    timings = {}
    for slope_value, label in labels.items():
        generators, elapsed = run_projection(slope_value)
        assert generators == ("1",), (label, generators)
        projections[label] = list(generators)
        timings[label] = round(elapsed, 2)

    divisor_closures = run_d23_divisor_closures()

    output = {
        "verified": True,
        "component": "tenth (coincident-support double-arrow) P4 component",
        "field": "C(b,e,m,c,r) at the k=1 torus gauge, slope transcendental",
        "parameter_renaming": "working-note parameter r renamed to c",
        "method": (
            "identity-dead 01 pencil, universal 23-pencil reconstruction "
            "kernel, and unit binary marking projections (generic + three "
            "special slopes)"
        ),
        "pure_coefficient": "-2*k*(b*e*c+b+e)",
        "pencils": {
            "01": "(r*u0+u1,u2,u3,ext)",
            "23": "(u0,u1,r*u2+u3,ext)",
        },
        "pencil_01_identity": (
            "word-0000 coefficient vanishes identically over "
            "Z[b,e,k,m,c,r,t,z]: no sharp Delta_2 extension ever"
        ),
        "pencil_23_A_row": (
            "(-(k+r)*A*, -(k+r)*A*, 2*Q*(r-k), -2*(k+r)) on (x0..x3), t-free; "
            "A*=2*b*c*e-(b+e)*(m-1), Q=b*e*(m+1)"
        ),
        "doubled_column_identity": (
            "D3_w + k^2*D2_w = 0 for w != 1111 and = 4*k^2*P at w=1111"
        ),
        "universal_kernel": (
            "ext_i = r*row_i[3] + k^2*row_i[2]: M z*=0, A z*=0, "
            "B z*=-2*k*P*(r-k)^2 identically"
        ),
        "rank7_witness_at_t0": witness,
        "marking_projections": projections,
        "projection_runtimes_seconds": timings,
        "slope_endpoints": {
            "r=0": "the H31 q=2 frame (also closed there)",
            "r=infinity": "the H31 q=3 frame (closed by the companion theorem)",
        },
        "interior_divisor_closures": {
            "statement": (
                "on {c=0} and {b+e=0} the D_23 binary marking sheets are "
                "slope-free and identical to the H31 sheets; on every sheet "
                "each genuine survivor has a rank-four mode-2 one-marked map "
                "(minors 0127/0137): no ternary H22 lift exists over the "
                "generic point of either divisor, for any slope; the D_01 "
                "pencil is identically non-sharp on the divisors as well"
            ),
            "results": divisor_closures,
        },
        "support_split": (
            "a != 0 needs sharp D_01 (impossible identically); b != 0 needs "
            "sharp D_23 (empty by the unit projections); (a,b) != (0,0)"
        ),
        "binary_level_exclusion": True,
        "fitting_stage_needed": False,
        "generic_H22_incidence_on_tenth_component_empty": True,
        "weighted_slope_and_parameter_boundaries_closed": False,
        "closed_special_slopes": ["0", "1", "-1", "infinity"],
        "all_pure_components_classified": False,
        "H22_excluded": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            COMPONENT_PRIMARY.name: sha256(COMPONENT_PRIMARY),
            COMPANION.name: sha256(COMPANION),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    out_path = HERE / "tmp" / "p5_h22_coincident_support_component_generic_verified.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
