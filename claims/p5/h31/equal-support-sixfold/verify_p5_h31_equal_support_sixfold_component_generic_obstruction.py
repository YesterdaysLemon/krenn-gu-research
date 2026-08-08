#!/usr/bin/env python3
"""Verify the generic marked H31 obstruction on the eleventh (equal-support
sixfold) pure-compression component, together with the exact interior
survivor-divisor theorem and the ternary closures of all five survivor strata.

Self-contained (sympy + Singular on PATH).  All statements are exact: the
symbolic identities are over Z[c0,c1,c2,t,v0..v3,x2,x3,t0..t3], the Groebner
projections are over the function field C(c0,c1,c2,d) of the gauge-normalized
family, and the survivor-locus elimination is over Q with the parameters as
ring variables.  Fail-closed: any Singular timeout or mismatch raises.
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
THEOREM = HERE / "P5_H31_EQUAL_SUPPORT_SIXFOLD_COMPONENT_GENERIC_OBSTRUCTION.md"
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

c0, c1, c2, d = sp.symbols("c0 c1 c2 d")
tt, v0, v1, v2, v3, x2, x3 = sp.symbols("t v0 v1 v2 v3 x2 x3")
T = sp.symbols("t0:4")
Z = sp.symbols("x0:4") + sp.symbols("y0:4")
W = sp.Symbol("w")

SINGULAR_TIMEOUT = 550

# words 0001,0010,0011,0100,0101,0110,1010 in MIXED order
WITNESS_ROWS = (0, 1, 2, 3, 4, 5, 9)
WITNESS_COLS = {0: (0, 1, 2, 3, 4, 6, 7), 1: (0, 1, 2, 3, 4, 5, 7)}

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

# per-sheet rational markings and the mode-0 Fitting minor rows
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


def perm3(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(3)) for p in PERMS3))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(4)) for p in PERMS4))


def wc(cc):
    return (0, 0, 1, -cc)


def raw_planes():
    vrow = (v0, v1, v2, v3)
    xrow = (tt * v0, tt * v1, x2, x3)
    return (
        ((v0, -v1, 0, 0), wc(c0)),
        (wc(c1), vrow),
        (wc(c2), xrow),
        ((0, 0, 1, 0), (0, 0, 0, 1)),
    )


def raw_concentrated():
    alpha = ((v0, -v1, 0, 0), wc(c1), wc(c2), (0, 0, 1, c0))
    beta = (wc(c0), (v0, v1, v2, v3), (tt * v0, tt * v1, x2, x3), (0, 0, 0, 1))
    return alpha, beta


def normalized_basis():
    alpha = ((1, -1, 0, 0), (0, 0, 1, -c1), (0, 0, 1, -c2), (0, 0, 1, c0))
    beta = ((0, 0, 1, -c0), (1, 1, 0, 1), (1, 1, 0, d), (0, 0, 0, 1))
    return alpha, beta


def marked_beta(alpha, beta, tvals=T):
    return tuple(tuple(sp.expand(beta[i][j] + tvals[i] * alpha[i][j])
                       for j in range(4)) for i in range(4))


def h31_word_forms(q, alpha, betat):
    common = tuple(j for j in range(4) if j != q)
    ap = tuple(tuple(alpha[i][j] for j in common) + (Z[i],) for i in range(4))
    bp = tuple(tuple(betat[i][j] for j in common) + (Z[4 + i],) for i in range(4))
    forms = {w: sp.expand(perm4(tuple(bp[i] if w[i] else ap[i] for i in range(4))))
             for w in WORDS}
    return forms, ap, bp


def check_raw_support_and_concentration():
    planes = raw_planes()
    adapt = (planes[0], planes[1], planes[2], ((0, 0, 1, 1), (0, 0, 1, -1)))
    raw = {w: perm4(tuple(adapt[i][w[i]] for i in range(4))) for w in WORDS}
    assert sp.expand(raw[(1, 1, 1, 0)] + 2 * tt * v0 * v1 * (c0 - 1)) == 0
    assert sp.expand(raw[(1, 1, 1, 1)] + 2 * tt * v0 * v1 * (c0 + 1)) == 0
    assert all(sp.expand(v) == 0 for w, v in raw.items()
               if w not in ((1, 1, 1, 0), (1, 1, 1, 1)))

    alpha, beta = raw_concentrated()
    for i in range(4):
        stack = sp.Matrix([list(planes[i][0]), list(planes[i][1]),
                           list(alpha[i]), list(beta[i])])
        assert stack.rank() == 2, i
    tensor = {w: perm4(tuple(beta[i] if w[i] else alpha[i] for i in range(4)))
              for w in WORDS}
    assert sp.expand(tensor[(1, 1, 1, 1)] - 2 * tt * v0 * v1) == 0
    assert all(sp.expand(v) == 0 for w, v in tensor.items() if w != (1, 1, 1, 1))
    return "2*t*v0*v1"


def check_gauge():
    """g=diag(1/v0,1/v1,1/V3,1/V3), V3=v3+c1*v2, carries the raw planes to the
    normalized family with d=(x3+c2*x2)/(t*(v3+c1*v2))."""
    planes = raw_planes()
    V3 = v3 + c1 * v2
    X3 = x3 + c2 * x2
    dval = X3 / (tt * V3)
    g = (1 / v0, 1 / v1, 1 / V3, 1 / V3)
    alpha_n, beta_n = normalized_basis()
    norm_planes = (
        (alpha_n[0], beta_n[0]),
        (alpha_n[1], beta_n[1]),
        (alpha_n[2], beta_n[2]),
        ((0, 0, 1, 0), (0, 0, 0, 1)),
    )
    for i in range(4):
        moved = tuple(tuple(sp.cancel(planes[i][row][j] * g[j]) for j in range(4))
                      for row in (0, 1))
        target = tuple(tuple(sp.cancel(sp.sympify(x).subs(d, dval)) for x in row)
                       for row in norm_planes[i])
        stack = sp.Matrix([list(moved[0]), list(moved[1]),
                           list(target[0]), list(target[1])]).applyfunc(sp.cancel)
        assert stack.rank() == 2, i
    # eigenvector identity: permanent under diagonal column scaling
    lam = sp.symbols("lam0:4")
    generic = tuple(tuple(sp.Symbol(f"g{i}_{j}") for j in range(4)) for i in range(4))
    scaled = tuple(tuple(generic[i][j] * lam[j] for j in range(4)) for i in range(4))
    assert sp.expand(perm4(scaled) - sp.prod(lam) * perm4(generic)) == 0
    # ground the gauge at the component certificate sample (9)
    sample = {c0: 3, c1: -2, c2: 5, tt: 2, v0: 3, v1: -7, v2: 2, v3: 5,
              x2: -1, x3: 4}
    dnum = dval.subs(sample)
    assert dnum == sp.Rational(-1, 2), dnum
    return "d=(x3+c2*x2)/(t*(v3+c1*v2)); sample (9) -> (3,-2,5,-1/2)"


def check_normalized_and_forcing():
    alpha, beta = normalized_basis()
    tensor = {w: perm4(tuple(beta[i] if w[i] else alpha[i] for i in range(4)))
              for w in WORDS}
    assert tensor[(1, 1, 1, 1)] == 2
    assert all(sp.expand(v) == 0 for w, v in tensor.items() if w != (1, 1, 1, 1))

    betat = marked_beta(alpha, beta)
    shifted = {w: perm4(tuple(betat[i] if w[i] else alpha[i] for i in range(4)))
               for w in WORDS}
    assert all(sp.expand(shifted[w] - tensor[w]) == 0 for w in WORDS)

    kappa = sp.symbols("ka0:4")
    nu = sp.symbols("nu0:4")
    sigma = sp.symbols("si0:4")
    tau = sp.symbols("ta0:4")
    kernel_rows = tuple(tuple(sigma[i] * alpha[i][j] + kappa[i] * beta[i][j]
                              for j in range(4)) for i in range(4))
    colour_rows = tuple(tuple(tau[i] * alpha[i][j] + nu[i] * beta[i][j]
                              for j in range(4)) for i in range(4))
    for i in range(4):
        near = tuple(0 if j == i else 1 for j in range(4))
        value = perm4(tuple(colour_rows[j] if near[j] else kernel_rows[j]
                            for j in range(4)))
        expected = 2 * kappa[i] * sp.prod(nu[j] for j in range(4) if j != i)
        assert sp.expand(value - expected) == 0, i
    assert sp.expand(perm4(colour_rows) - 2 * sp.prod(nu)) == 0


def check_dead_frames():
    """A_q = 0 identically over Z[c0,c1,c2,t,v,x2,x3,t0..t3] for q=2,3."""
    alpha, beta = raw_concentrated()
    betat = marked_beta(alpha, beta)
    for q in (2, 3):
        forms, _, _ = h31_word_forms(q, alpha, betat)
        assert sp.expand(forms[(0, 0, 0, 0)]) == 0, q
    # mechanism: the three kernel rows alpha_1,alpha_2,alpha_3 lie in Pi
    for i in (1, 2, 3):
        assert alpha[i][0] == 0 and alpha[i][1] == 0, i


def check_live_frames():
    alpha, beta = normalized_basis()
    betat = marked_beta(alpha, beta)
    expected_a = {
        0: (0, c2 - c0, c1 - c0, c1 + c2, 0, 0, 0, 0),
        1: (0, c0 - c2, c0 - c1, -c1 - c2, 0, 0, 0, 0),
    }
    witness = {}
    for q in (0, 1):
        forms, ap, bp = h31_word_forms(q, alpha, betat)
        arow = tuple(sp.expand(sp.diff(forms[(0, 0, 0, 0)], z)) for z in Z)
        assert arow == tuple(sp.expand(x) for x in expected_a[q]), (q, arow)
        assert all(sp.diff(x, ti) == 0 for x in arow for ti in T)

        # reconstruction kernel: restore column q
        sub = {Z[i]: alpha[i][q] for i in range(4)}
        sub.update({Z[4 + i]: betat[i][q] for i in range(4)})
        for w in WORDS:
            value = sp.expand(forms[w].subs(sub))
            assert value == (2 if w == (1, 1, 1, 1) else 0), (q, w, value)

        # rank-7 witness at t=0
        zero = {ti: 0 for ti in T}
        matrix = sp.Matrix([[sp.diff(forms[w].subs(zero), z) for z in Z]
                            for w in MIXED])
        minor = sp.factor(matrix[list(WITNESS_ROWS), list(WITNESS_COLS[q])].det())
        expected = 4 * d**2 * (c0 - c1)
        assert sp.expand(minor - expected) == 0, (q, minor)
        witness[q] = str(minor)
    return witness


def check_swap_symmetries():
    alpha, beta = normalized_basis()
    betat = marked_beta(alpha, beta)

    def s01(row):
        return (row[1], row[0], row[2], row[3])

    salpha = tuple(s01(r_) for r_ in alpha)
    sbetat = tuple(s01(r_) for r_ in betat)
    forms_swap, _, _ = h31_word_forms(0, salpha, sbetat)
    forms_q1, _, _ = h31_word_forms(1, alpha, betat)
    assert all(sp.expand(forms_swap[w] - forms_q1[w]) == 0 for w in WORDS)

    # mode-(12) swap composed with torus diag(1,1,1/d,1/d):
    # (c0,c1,c2,d) -> (c0,c2,c1,1/d), kernel/colour lines preserved
    sub = {c1: c2, c2: c1, d: 1 / d}
    torus = (1, 1, 1 / d, 1 / d)
    perm = (0, 2, 1, 3)
    for i in range(4):
        ai = tuple(sp.cancel(alpha[perm[i]][j] * torus[j]) for j in range(4))
        bi = tuple(sp.cancel(beta[perm[i]][j] * torus[j]) for j in range(4))
        at = tuple(sp.cancel(sp.sympify(x).subs(sub, simultaneous=True))
                   for x in alpha[i])
        bt = tuple(sp.cancel(sp.sympify(x).subs(sub, simultaneous=True))
                   for x in beta[i])
        assert sp.Matrix([list(ai), list(at)]).applyfunc(sp.cancel).rank() == 1, i
        assert sp.Matrix([list(bi), list(bt)]).applyfunc(sp.cancel).rank() == 1, i


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


def run_projection(q, sub, parameters):
    alpha, beta = family_on_divisor(sub)
    betat = marked_beta(alpha, beta)
    forms, _, _ = h31_word_forms(q, alpha, betat)
    equations = [forms[w] for w in MIXED]
    equations.append(forms[(0, 0, 0, 0)] - 1)
    equations.append(W * forms[(1, 1, 1, 1)] - 1)
    eliminated = Z + (W,)
    variables = eliminated + T
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


def run_survivor_locus(q):
    """Eliminate (z,w,t) with the parameters a=c0,b=c1,c=c2,e=d as ring
    variables: the exact interior survivor locus."""
    a, b, c, e = sp.symbols("a b c e")
    alpha = ((1, -1, 0, 0), (0, 0, 1, -b), (0, 0, 1, -c), (0, 0, 1, a))
    beta = ((0, 0, 1, -a), (1, 1, 0, 1), (1, 1, 0, e), (0, 0, 0, 1))
    betat = marked_beta(alpha, beta)
    forms, _, _ = h31_word_forms(q, alpha, betat)
    equations = [forms[w] for w in MIXED]
    equations.append(W * forms[(0, 0, 0, 0)] * forms[(1, 1, 1, 1)] - 1)
    elimvars = [str(z) for z in Z] + ["w"] + [str(ti) for ti in T]
    program = "\n".join((
        "ring R=0,(" + ",".join(elimvars) + ",a,b,c,e),(dp(13),dp(4));",
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
    assert generators == SURVIVOR_LOCUS, (q, generators)
    # the five-piece decomposition is elementary: with u=a^2*b*c*e,
    # generators are u*(e+1) and u*(b-c)
    a2 = sp.sympify("a**2*b*c*e", locals={"a": a, "b": b, "c": c, "e": e})
    g1 = sp.sympify(SURVIVOR_LOCUS[0].replace("^", "**"),
                    locals={"a": a, "b": b, "c": c, "e": e})
    g2 = sp.sympify(SURVIVOR_LOCUS[1].replace("^", "**"),
                    locals={"a": a, "b": b, "c": c, "e": e})
    assert sp.expand(g1 - a2 * (e + 1)) == 0
    assert sp.expand(g2 - a2 * (b - c)) == 0
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


def divisor_fitting_certificate(q, divisor, tvals, minor_rows):
    sub, parameters = DIVISOR_DATA[divisor]
    alpha, beta = family_on_divisor(sub)
    betat = marked_rows_cleared(alpha, beta, tvals)
    forms, ap, bp = h31_word_forms(q, alpha, betat)
    marked = one_marked_map(MARKED_MODE, ap, bp)
    minor = sp.expand(marked[list(minor_rows), :].det())
    equations = [forms[w] for w in MIXED] + [minor]
    equations.append(forms[(0, 0, 0, 0)] - 1)
    equations.append(W * forms[(1, 1, 1, 1)] - 1)
    variables = list(map(str, Z)) + ["w"]
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
    assert lines == ["UNIT:1"], (q, divisor, lines, stdout[-800:])
    return elapsed


def main() -> None:
    t_start = time.time()
    pure_raw = check_raw_support_and_concentration()
    gauge = check_gauge()
    check_normalized_and_forcing()
    check_dead_frames()
    witness = check_live_frames()
    check_swap_symmetries()

    projections = {}
    timings = {}
    for q in (0, 1):
        generators, elapsed = run_projection(q, {}, "c0,c1,c2,d")
        assert generators == ("1",), (q, generators)
        projections[q] = list(generators)
        timings[f"projection q={q}"] = round(elapsed, 2)

    locus = {}
    for q in (0, 1):
        generators, elapsed = run_survivor_locus(q)
        locus[q] = list(generators)
        timings[f"survivor locus q={q}"] = round(elapsed, 2)

    sheet_results = {}
    for divisor in DIVISOR_SHEETS:
        sub, parameters = DIVISOR_DATA[divisor]
        for q in (0, 1):
            generators, elapsed = run_projection(q, sub, parameters)
            assert generators == DIVISOR_SHEETS[divisor], (divisor, q, generators)
            sheet_results[f"{divisor} q={q}"] = {
                "sheet_ideal": list(generators),
                "seconds": round(elapsed, 2),
            }

    fitting_results = {}
    for divisor, label, tvals, minor_rows in SHEET_CERTIFICATES:
        for q in (0, 1):
            elapsed = divisor_fitting_certificate(q, divisor, tvals, minor_rows)
            fitting_results[f"{divisor} {label} q={q}"] = {
                "mode": MARKED_MODE,
                "minor_rows": list(minor_rows),
                "unit": True,
                "seconds": round(elapsed, 2),
            }

    output = {
        "verified": True,
        "component": "eleventh (equal-support sixfold) P4 component",
        "field": (
            "C(c0,c1,c2,d): gauge (v0,v1,t,v2,x2,v3)=(1,1,1,0,0,1) via row "
            "operations, the source torus, and d=(x3+c2*x2)/(t*(v3+c1*v2))"
        ),
        "method": (
            "gauge normalization to a unit single-word tensor, two "
            "identity-dead frames (q=2,3), reconstruction kernels and unit "
            "marking projections for q=0,1, an exact interior survivor-locus "
            "elimination, and per-sheet mode-0 Fitting closures of all five "
            "survivor strata"
        ),
        "raw_pure_coefficient": pure_raw,
        "gauge": gauge,
        "normalized_pure_coefficient": "2 (a unit: no pure-coefficient divisor)",
        "marked_invariance": (
            "the marked tensor is identically the single word T_1111=2 for "
            "every marking t"
        ),
        "dead_frames": {
            "q": [2, 3],
            "statement": (
                "the 0000-diagonal row vanishes identically over "
                "Z[c0,c1,c2,t,v0..v3,x2,x3,t0..t3]: no genuine binary Delta_2 "
                "neighbour for any marking at any chart point"
            ),
            "mechanism": (
                "the three kernel rows alpha_1=w_c1, alpha_2=w_c2, "
                "alpha_3=(0,0,1,c0) all lie in Pi=span(X2,X3); deleting "
                "column 2 or 3 confines them to a single common column, and "
                "every 0000 coefficient is a 3x3 permanent containing at "
                "least two of them"
            ),
        },
        "live_frames": {
            "q": [0, 1],
            "A_row": {
                "0": "(0, c2-c0, c1-c0, c1+c2) on (x0,x1,x2,x3), t-free",
                "1": "(0, c0-c2, c0-c1, -(c1+c2)) = -(q=0 row)",
            },
            "reconstruction_kernel": (
                "z_rec = restore column q: M z_rec = 0, A z_rec = 0, "
                "B z_rec = 2, identically in t"
            ),
            "rank7_witness_words": ["0001", "0010", "0011", "0100", "0101",
                                     "0110", "1010"],
            "rank7_witness_cols": {
                "0": "x0..x3,y0,y2,y3", "1": "x0..x3,y0,y1,y3"},
            "rank7_witness_at_t0": witness,
        },
        "swap_symmetries": {
            "source_01": (
                "the source transposition (01) fixes the family and carries "
                "the q=0 frame to the q=1 frame verbatim (all 16 word forms "
                "equal, same marking)"
            ),
            "mode_12": (
                "mode-(12) swap composed with diag(1,1,1/d,1/d) maps "
                "(c0,c1,c2,d) -> (c0,c2,c1,1/d)"
            ),
        },
        "marking_projections": {str(q): v for q, v in projections.items()},
        "survivor_locus": {
            "statement": (
                "eliminating (z,w,t0..t3) from the fourteen mixed words plus "
                "w*A*B-1 with the parameters as ring variables gives exactly "
                "(a^2*b*c*e*(e+1), a^2*b*c*e*(b-c)), a=c0,b=c1,c=c2,e=d; "
                "hence every parameter point with a genuine binary survivor "
                "in a live frame lies on {c0=0} u {c1=0} u {c2=0} u {d=0} u "
                "{c1=c2, d=-1}"
            ),
            "ideal": {str(q): v for q, v in locus.items()},
        },
        "divisor_sheets": sheet_results,
        "fitting_certificates": fitting_results,
        "ternary_closures": (
            "on every sheet of all five survivor strata the mode-0 one-marked "
            "map has rank four (single-minor unit certificates): no ternary "
            "H31 lift exists over the generic point of any stratum"
        ),
        "binary_level_exclusion": True,
        "generic_marked_fibre_excluded": True,
        "complete_boundary_marked_fibre_excluded": False,
        "all_pure_components_classified": False,
        "H31_excluded": False,
        "H22_excluded": False,
        "global_conjecture_resolved": False,
        "runtimes_seconds": timings,
        "total_seconds": round(time.time() - t_start, 2),
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            COMPONENT_PRIMARY.name: sha256(COMPONENT_PRIMARY),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    out_path = HERE / "tmp" / "p5_h31_equal_support_sixfold_component_generic_verified.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
