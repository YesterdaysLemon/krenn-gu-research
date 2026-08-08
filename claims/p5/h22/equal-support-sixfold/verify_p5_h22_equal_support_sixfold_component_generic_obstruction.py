#!/usr/bin/env python3
"""Verify the generic weighted H22 obstruction on the eleventh (equal-support
sixfold) pure-compression component.

Self-contained (sympy + Singular on PATH).  Identities are exact over
Z[c0,c1,c2,t,v0..v3,x2,x3,r,t0..t3]; the all-slope marking projections
eliminate the slope as a ring variable over C(c0,c1,c2,d) (and over the
divisor fields), so no slope divisor is left open at the points they cover;
the pencil survivor-locus eliminations run over C(r) and at fixed rational
slopes.  Fail-closed: any Singular timeout or mismatch raises.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
import time
from pathlib import Path

import sympy as sp

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

ROOT = REPO_ROOT
THEOREM = HERE / "P5_H22_EQUAL_SUPPORT_SIXFOLD_COMPONENT_GENERIC_OBSTRUCTION.md"
COMPANION = (
    ROOT / "claims/p5/h31/equal-support-sixfold"
    / "P5_H31_EQUAL_SUPPORT_SIXFOLD_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = (
    ROOT / "claims/p4/components/equal-support-sixfold"
    / "P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md"
)
COMPONENT_PRIMARY = (
    ROOT / "claims/p4/components/equal-support-sixfold"
    / "verify_p4_equal_support_sixfold_pure_component.py"
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
PERMS3 = tuple(itertools.permutations(range(3)))
PERMS4 = tuple(itertools.permutations(range(4)))

c0, c1, c2, d, r = sp.symbols("c0 c1 c2 d r")
tt, v0, v1, v2, v3, x2, x3 = sp.symbols("t v0 v1 v2 v3 x2 x3")
T = sp.symbols("t0:4")
Z = sp.symbols("x0:4") + sp.symbols("y0:4")
W = sp.Symbol("w")

SINGULAR_TIMEOUT = 550
WITNESS_ROWS = (0, 1, 2, 3, 4, 5, 9)
WITNESS_COLS = (0, 1, 2, 3, 4, 5, 7)

SURVIVOR_LOCUS = (
    "a^2*b*c*e^2+a^2*b*c*e",
    "a^2*b^2*c*e-a^2*b*c^2*e",
)

DIVISOR_SHEETS = {
    "c0=0": (
        "(c1^2*d)*t1+(c2^2)*t2+(c1*c2*d)*t3+(-c1*d-c2*d)",
        "t0",
        "(c1^2*c2*d)*t3^2+(-c1*c2+c2^2)*t2+(-c1^2*d)*t3+(c1*d-c2*d)",
        "(c1*c2)*t2*t3+(-c2)*t2+(-c1*d)*t3+(d)",
        "(c2)*t2^2+(-d)*t2",
    ),
    "c1=0": ("(c0)*t3+1", "t2", "(c0)*t1+1", "t0"),
    "c2=0": ("(c0)*t3+1", "(c0)*t2+(d)", "t1", "t0"),
    "d=0": ("(c0^2-c1*c2)*t3+(c0)", "t2", "(c0-c1)*t1+1", "t0"),
    "c1=c2,d=-1": ("(c0-c1)*t3+1", "(c1)*t1+(-c1)*t2-1", "t0", "(c1)*t2^2+t2"),
}

DIVISOR_DATA = {
    "c0=0": ({c0: 0}, "c1,c2,d"),
    "c1=0": ({c1: 0}, "c0,c2,d"),
    "c2=0": ({c2: 0}, "c0,c1,d"),
    "d=0": ({d: 0}, "c0,c1,c2"),
    "c1=c2,d=-1": ({c2: c1, d: -1}, "c0,c1"),
}

SHEET_CERTIFICATES = (
    ("c1=0", "t=(0,-1/c0,0,-1/c0)",
     (0, -1 / c0, 0, -1 / c0), (0, 2, 4, 7)),
    ("c2=0", "t=(0,0,-d/c0,-1/c0)",
     (0, 0, -d / c0, -1 / c0), (0, 2, 4, 7)),
    ("d=0", "t=(0,-1/(c0-c1),0,-c0/(c0^2-c1*c2))",
     (0, -1 / (c0 - c1), 0, -c0 / (c0**2 - c1 * c2)), (0, 2, 4, 7)),
    ("c0=0", "m1: t=(0,1/c1,0,1/c1)",
     (0, 1 / c1, 0, 1 / c1), (0, 2, 4, 7)),
    ("c0=0", "m2: t=(0,1/c1,d/c2,0)",
     (0, 1 / c1, d / c2, 0), (0, 2, 5, 7)),
    ("c0=0", "m3: t=(0,0,d/c2,1/c2)",
     (0, 0, d / c2, 1 / c2), (0, 2, 3, 7)),
    ("c1=c2,d=-1", "mA: t=(0,1/c1,0,-1/(c0-c1))",
     (0, 1 / c1, 0, -1 / (c0 - c1)), (0, 2, 6, 7)),
    ("c1=c2,d=-1", "mB: t=(0,0,-1/c1,-1/(c0-c1))",
     (0, 0, -1 / c1, -1 / (c0 - c1)), (0, 2, 6, 7)),
)

MARKED_MODE = 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(4)) for p in PERMS4))


def normalized_basis():
    alpha = ((1, -1, 0, 0), (0, 0, 1, -c1), (0, 0, 1, -c2), (0, 0, 1, c0))
    beta = ((0, 0, 1, -c0), (1, 1, 0, 1), (1, 1, 0, d), (0, 0, 0, 1))
    return alpha, beta


def raw_concentrated():
    alpha = ((v0, -v1, 0, 0), (0, 0, 1, -c1), (0, 0, 1, -c2), (0, 0, 1, c0))
    beta = ((0, 0, 1, -c0), (v0, v1, v2, v3), (tt * v0, tt * v1, x2, x3),
            (0, 0, 0, 1))
    return alpha, beta


def marked_beta(alpha, beta, tvals=T):
    return tuple(tuple(sp.expand(beta[i][j] + tvals[i] * alpha[i][j])
                       for j in range(4)) for i in range(4))


def pencil_word_forms(pencil, slope, alpha, betat):
    def drow(row, ext):
        if pencil == "01":
            return (sp.expand(slope * row[0] + row[1]), row[2], row[3], ext)
        return (row[0], row[1], sp.expand(slope * row[2] + row[3]), ext)
    ap = tuple(drow(alpha[i], Z[i]) for i in range(4))
    bp = tuple(drow(betat[i], Z[4 + i]) for i in range(4))
    forms = {w: sp.expand(perm4(tuple(bp[i] if w[i] else ap[i] for i in range(4))))
             for w in WORDS}
    return forms, ap, bp


def h31_word_forms(q, alpha, betat):
    common = tuple(j for j in range(4) if j != q)
    ap = tuple(tuple(alpha[i][j] for j in common) + (Z[i],) for i in range(4))
    bp = tuple(tuple(betat[i][j] for j in common) + (Z[4 + i],) for i in range(4))
    return {w: sp.expand(perm4(tuple(bp[i] if w[i] else ap[i] for i in range(4))))
            for w in WORDS}


def check_pure_normal_form():
    alpha, beta = normalized_basis()
    tensor = {w: perm4(tuple(beta[i] if w[i] else alpha[i] for i in range(4)))
              for w in WORDS}
    assert tensor[(1, 1, 1, 1)] == 2
    assert all(sp.expand(v) == 0 for w, v in tensor.items() if w != (1, 1, 1, 1))
    betat = marked_beta(alpha, beta)
    shifted = {w: perm4(tuple(betat[i] if w[i] else alpha[i] for i in range(4)))
               for w in WORDS}
    assert all(sp.expand(shifted[w] - tensor[w]) == 0 for w in WORDS)


def check_23_identity():
    """The D_23 pencil's 0000 word vanishes identically -- raw parameters,
    slope and marking symbolic: the pencil is dead at every chart point."""
    alpha, beta = raw_concentrated()
    betat = marked_beta(alpha, beta)
    forms, _, _ = pencil_word_forms("23", r, alpha, betat)
    assert sp.expand(forms[(0, 0, 0, 0)]) == 0
    # mechanism: the three kernel rows lie in Pi, and D_23 merges columns 2,3
    for i in (1, 2, 3):
        assert alpha[i][0] == 0 and alpha[i][1] == 0, i


def check_01_structure():
    alpha, beta = normalized_basis()
    betat = marked_beta(alpha, beta)
    forms, ap, bp = pencil_word_forms("01", r, alpha, betat)

    # A row = (r-1) * (0, c0-c2, c0-c1, -(c1+c2)) on the x-slots
    arow = tuple(sp.expand(sp.diff(forms[(0, 0, 0, 0)], z)) for z in Z)
    expected = tuple(sp.expand(v) for v in (
        0, (r - 1) * (c0 - c2), (r - 1) * (c0 - c1), -(r - 1) * (c1 + c2),
        0, 0, 0, 0))
    assert arow == expected, arow
    assert all(sp.diff(x, ti) == 0 for x in arow for ti in T)

    # interpolation identity: every pencil word = r*(q=1 word) + (q=0 word)
    forms_q0 = h31_word_forms(0, alpha, betat)
    forms_q1 = h31_word_forms(1, alpha, betat)
    for w in WORDS:
        assert sp.expand(forms[w] - (r * forms_q1[w] + forms_q0[w])) == 0, w

    # doubled-column identity: D0_w + D1_w = 0 (w != 1111), = 4 (w = 1111)
    for w in WORDS:
        rows = tuple(betat[i] if w[i] else alpha[i] for i in range(4))
        d0 = perm4(tuple((row[0], row[0], row[2], row[3]) for row in rows))
        d1 = perm4(tuple((row[1], row[1], row[2], row[3]) for row in rows))
        value = sp.expand(d0 + d1)
        assert value == (4 if w == (1, 1, 1, 1) else 0), (w, value)

    # universal kernel z*: ext_i = row_i[0] + r*row_i[1]
    sub = {Z[i]: alpha[i][0] + r * alpha[i][1] for i in range(4)}
    sub.update({Z[4 + i]: betat[i][0] + r * betat[i][1] for i in range(4)})
    for w in WORDS:
        value = sp.expand(forms[w].subs(sub))
        if w == (1, 1, 1, 1):
            assert sp.expand(value - 2 * (r + 1)**2) == 0, value
        else:
            assert value == 0, (w, value)

    # rank-7 witness at t=0
    zero = {ti: 0 for ti in T}
    matrix = sp.Matrix([[sp.diff(forms[w].subs(zero), z) for z in Z]
                        for w in MIXED])
    minor = sp.factor(matrix[list(WITNESS_ROWS), list(WITNESS_COLS)].det())
    expected_minor = 4 * d**2 * (c0 - c1) * (r - 1)**5 * (r + 1)**2
    assert sp.expand(minor - expected_minor) == 0, minor

    # endpoint identifications: r=0 is the H31 q=0 frame; the leading
    # r-coefficient (projective r=infinity) is the H31 q=1 frame
    for w in WORDS:
        assert sp.expand(forms[w].subs(r, 0) - forms_q0[w]) == 0, w
        assert sp.expand(sp.diff(forms[w], r) - forms_q1[w]) == 0, w

    # swap covariance: source transposition (01) sends D_01^r to r*D_01^(1/r)
    def s01(row):
        return (row[1], row[0], row[2], row[3])
    salpha = tuple(s01(x) for x in alpha)
    sbetat = tuple(s01(x) for x in betat)
    forms_swap, _, _ = pencil_word_forms("01", r, salpha, sbetat)
    forms_inv, _, _ = pencil_word_forms("01", 1 / r, alpha, betat)
    for w in WORDS:
        assert sp.simplify(forms_swap[w] - r * forms_inv[w]) == 0, w

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


def family_on_divisor(sub):
    alpha, beta = normalized_basis()
    alpha = tuple(tuple(sp.sympify(x).subs(sub) for x in row) for row in alpha)
    beta = tuple(tuple(sp.sympify(x).subs(sub) for x in row) for row in beta)
    return alpha, beta


def run_allslope_projection(sub, parameters):
    """Marking projection with the slope r eliminated as a ring variable:
    covers every slope, including parameter-coupled values."""
    alpha, beta = family_on_divisor(sub)
    betat = marked_beta(alpha, beta)
    forms, _, _ = pencil_word_forms("01", r, alpha, betat)
    equations = [forms[w] for w in MIXED]
    equations.append(forms[(0, 0, 0, 0)] - 1)
    equations.append(W * forms[(1, 1, 1, 1)] - 1)
    eliminated = Z + (W, r)
    variables = eliminated + T
    program = "\n".join((
        f"ring R=(0,{parameters}),(" + ",".join(map(str, variables))
        + "),(dp(10),dp(4));",
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


def run_fixed_slope_projection(slope_value):
    alpha, beta = normalized_basis()
    betat = marked_beta(alpha, beta)
    forms, _, _ = pencil_word_forms("01", sp.Integer(slope_value), alpha, betat)
    equations = [forms[w] for w in MIXED]
    equations.append(forms[(0, 0, 0, 0)] - 1)
    equations.append(W * forms[(1, 1, 1, 1)] - 1)
    eliminated = Z + (W,)
    variables = eliminated + T
    program = "\n".join((
        "ring R=(0,c0,c1,c2,d),(" + ",".join(map(str, variables))
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


def run_pencil_locus(slope, param_r):
    """Survivor-locus elimination for the pencil: parameters as ring
    variables, slope either the transcendental parameter r or a fixed
    rational value."""
    a, b, c, e = sp.symbols("a b c e")
    alpha = ((1, -1, 0, 0), (0, 0, 1, -b), (0, 0, 1, -c), (0, 0, 1, a))
    beta = ((0, 0, 1, -a), (1, 1, 0, 1), (1, 1, 0, e), (0, 0, 0, 1))
    betat = marked_beta(alpha, beta)
    slope_expr = r if param_r else sp.Rational(slope)
    forms, _, _ = pencil_word_forms("01", slope_expr, alpha, betat)
    equations = [forms[w] for w in MIXED]
    equations.append(W * forms[(0, 0, 0, 0)] * forms[(1, 1, 1, 1)] - 1)
    elimvars = [str(z) for z in Z] + ["w"] + [str(ti) for ti in T]
    ringdef = ("ring R=(0,r),(" if param_r else "ring R=0,(") \
        + ",".join(elimvars) + ",a,b,c,e),(dp(13),dp(4));"
    program = "\n".join((
        ringdef,
        "ideal I=" + ",".join(singular_str(x) for x in equations) + ";",
        "ideal J=slimgb(I);",
        "ideal L=eliminate(J," + "*".join(elimvars) + ");",
        "L=std(L);",
        '"LOCUS";',
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


def one_marked_map(mode, ap, bp):
    rows = []
    for bits in WORDS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(bp[other] if bits[bit_index] else ap[other])
                bit_index += 1
        row = []
        for coordinate in range(4):
            basis = tuple(int(idx == coordinate) for idx in range(4))
            row.append(perm4(tuple(basis if other == mode else selected[other]
                                   for other in range(4))))
        rows.append(row)
    return sp.Matrix(rows)


def marked_rows_cleared(alpha, beta, tvals):
    out = []
    for i in range(4):
        row = tuple(sp.together(beta[i][j] + tvals[i] * alpha[i][j])
                    for j in range(4))
        lcm = sp.lcm([sp.fraction(sp.cancel(x))[1] for x in row])
        out.append(tuple(sp.expand(sp.cancel(x * lcm)) for x in row))
    return tuple(out)


def divisor_fitting_certificate(divisor, tvals, minor_rows):
    """Pencil Fitting certificate with the slope r kept a ring variable:
    every slope is covered."""
    sub, parameters = DIVISOR_DATA[divisor]
    alpha, beta = family_on_divisor(sub)
    betat = marked_rows_cleared(alpha, beta, tvals)
    forms, ap, bp = pencil_word_forms("01", r, alpha, betat)
    marked = one_marked_map(MARKED_MODE, ap, bp)
    minor = sp.expand(marked[list(minor_rows), :].det())
    equations = [forms[w] for w in MIXED] + [minor]
    equations.append(forms[(0, 0, 0, 0)] - 1)
    equations.append(W * forms[(1, 1, 1, 1)] - 1)
    variables = list(map(str, Z)) + ["w", "r"]
    program = "\n".join((
        f"ring R=(0,{parameters}),(" + ",".join(variables) + "),dp;",
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


def main() -> None:
    t_start = time.time()
    check_pure_normal_form()
    check_23_identity()
    witness = check_01_structure()

    timings = {}

    # generic all-slope projection and the r=-1, r=0 fixed-slope projections
    generators, elapsed = run_allslope_projection({}, "c0,c1,c2,d")
    assert generators == ("1",), generators
    timings["all-slope projection (generic)"] = round(elapsed, 2)
    projections = {"generic (r eliminated)": list(generators)}
    for slope in (-1, 0):
        generators, elapsed = run_fixed_slope_projection(slope)
        assert generators == ("1",), (slope, generators)
        projections[f"r={slope}"] = list(generators)
        timings[f"projection r={slope}"] = round(elapsed, 2)

    # pencil survivor locus: transcendental slope and fixed slopes
    locus = {}
    generators, elapsed = run_pencil_locus(None, True)
    assert generators == SURVIVOR_LOCUS, generators
    locus["C(r) transcendental"] = list(generators)
    timings["pencil locus over C(r)"] = round(elapsed, 2)
    for slope, expected in ((-1, ("1",)), (2, SURVIVOR_LOCUS),
                            (sp.Rational(1, 2), SURVIVOR_LOCUS)):
        generators, elapsed = run_pencil_locus(slope, False)
        assert generators == expected, (slope, generators)
        locus[f"r={slope}"] = list(generators)
        timings[f"pencil locus r={slope}"] = round(elapsed, 2)

    # all-slope divisor sheet projections
    sheet_results = {}
    for divisor in DIVISOR_SHEETS:
        sub, parameters = DIVISOR_DATA[divisor]
        generators, elapsed = run_allslope_projection(sub, parameters)
        assert generators == DIVISOR_SHEETS[divisor], (divisor, generators)
        sheet_results[divisor] = {
            "sheet_ideal_all_slopes": list(generators),
            "seconds": round(elapsed, 2),
        }

    # per-sheet Fitting certificates with r a ring variable
    fitting_results = {}
    for divisor, label, tvals, minor_rows in SHEET_CERTIFICATES:
        elapsed = divisor_fitting_certificate(divisor, tvals, minor_rows)
        fitting_results[f"{divisor} {label}"] = {
            "mode": MARKED_MODE,
            "minor_rows": list(minor_rows),
            "slope": "ring variable (all slopes)",
            "unit": True,
            "seconds": round(elapsed, 2),
        }

    output = {
        "verified": True,
        "component": "eleventh (equal-support sixfold) P4 component",
        "field": (
            "C(c0,c1,c2,d) in the gauge of the H31 companion theorem; the "
            "slope is eliminated as a ring variable wherever possible"
        ),
        "method": (
            "identity-dead D_23 pencil, D_01 interpolation between the two "
            "live H31 frames, doubled-column universal kernel, all-slope "
            "unit marking projections, exact pencil survivor-locus "
            "eliminations, and all-slope per-sheet Fitting closures"
        ),
        "pure_coefficient": "2 (unit)",
        "pencils": {
            "01": "(r*u0+u1,u2,u3,ext)",
            "23": "(u0,u1,r*u2+u3,ext)",
        },
        "pencil_23_identity": (
            "word-0000 coefficient vanishes identically over "
            "Z[c0,c1,c2,t,v,x2,x3,r,t,z]: no sharp Delta_2 extension at any "
            "slope, marking, or chart point"
        ),
        "pencil_01_A_row": (
            "(r-1)*(0, c0-c2, c0-c1, -(c1+c2)) on (x0..x3), t-free; dead at "
            "the equal-weight slope r=1"
        ),
        "interpolation_identity": (
            "D_01^r word = r*(H31 q=1 word) + (H31 q=0 word), all sixteen "
            "words identically; r=0 and r=infinity are exactly the live H31 "
            "frames"
        ),
        "doubled_column_identity": (
            "D0_w + D1_w = 0 for w != 1111 and = 4 at w = 1111"
        ),
        "universal_kernel": (
            "ext_i = row_i[0] + r*row_i[1]: M z*=0, A z*=0, B z* = 2*(r+1)^2 "
            "identically; degenerate exactly at r=-1"
        ),
        "swap_covariance": (
            "source transposition (01) maps D_01^r to r*D_01^(1/r)"
        ),
        "rank7_witness_at_t0": witness,
        "marking_projections": projections,
        "pencil_survivor_locus": {
            "statement": (
                "with parameters as ring variables the (z,w,t)-elimination "
                "of the genuine pencil incidence over C(r), and at the fixed "
                "slopes 2 and 1/2, equals the H31 survivor locus "
                "(a^2*b*c*e*(e+1), a^2*b*c*e*(b-c)); at r=-1 it is the unit "
                "ideal (empty); at r=1 the pencil is identity-dead; at "
                "r=0/infinity it is the H31 loci by the interpolation "
                "identity"
            ),
            "ideals": locus,
        },
        "divisor_sheets": sheet_results,
        "fitting_certificates": fitting_results,
        "support_split": (
            "b != 0 needs sharp D_23 (impossible identically); a != 0 needs "
            "sharp D_01 (empty by the all-slope unit projection); "
            "(a,b) != (0,0)"
        ),
        "binary_level_exclusion": True,
        "generic_H22_incidence_on_eleventh_component_empty": True,
        "no_open_slope_divisors_at_generic_point": True,
        "closed_special_slopes": ["all slopes (r eliminated)", "1 (dead)",
                                   "-1", "0", "infinity (= H31 q=1)"],
        "all_pure_components_classified": False,
        "H22_excluded": False,
        "global_conjecture_resolved": False,
        "runtimes_seconds": timings,
        "total_seconds": round(time.time() - t_start, 2),
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
    out_path = HERE / "tmp" / "p5_h22_equal_support_sixfold_component_generic_verified.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
