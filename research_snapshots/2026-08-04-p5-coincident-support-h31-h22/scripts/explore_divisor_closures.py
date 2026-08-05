#!/usr/bin/env python3
"""Relative marking projections over the two confirmed codim-1 survivor
divisors {c=0} and {b+e=0} (H31 q=2,3 and H22 D_23), and Fitting-stage
closure attempts on the resulting sheets.
"""
from __future__ import annotations

import itertools
import subprocess
import time

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
PERMS3 = tuple(itertools.permutations(range(3)))
PERMS4 = tuple(itertools.permutations(range(4)))

b, e, m, c, r = sp.symbols("b e m c r")
P = b * e * c + b + e
Q = b * e * (m + 1)
T = sp.symbols("t0:4")
Z = sp.symbols("x0:4") + sp.symbols("y0:4")
W = sp.Symbol("w")


def perm3(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(3)) for p in PERMS3))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(4)) for p in PERMS4))


def concentrated_basis():
    alpha = ((1, -1, 0, 0), (1, -1, 0, 0), (0, 0, 1, 1), (P, P * m - Q * c, -Q, Q))
    beta = ((0, 1, b, -b), (0, 1, e, -e), (1, 1, 0, 0), (0, c, 1, -1))
    return alpha, beta


def frames(q, sub):
    """H31 frame word forms and extended rows, with substitution sub applied."""
    alpha, beta = concentrated_basis()
    alpha = tuple(tuple(sp.expand(sp.sympify(x).subs(sub)) for x in row) for row in alpha)
    beta = tuple(tuple(sp.expand(sp.sympify(x).subs(sub)) for x in row) for row in beta)
    betat = tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))
    common = tuple(j for j in range(4) if j != q)
    alph = tuple(tuple(alpha[i][j] for j in common) for i in range(4))
    bett = tuple(tuple(betat[i][j] for j in common) for i in range(4))
    forms = {}
    for wd in WORDS:
        expr = 0
        for i in range(4):
            others = tuple((bett[j] if wd[j] else alph[j]) for j in range(4) if j != i)
            expr += perm3(others) * Z[i + (4 if wd[i] else 0)]
        forms[wd] = sp.expand(expr)
    # extended 4-column rows (3 common + extension) for one-marked maps
    alpha_p = tuple(alph[i] + (Z[i],) for i in range(4))
    beta_p = tuple(bett[i] + (Z[4 + i],) for i in range(4))
    return forms, alpha_p, beta_p


def d23_frames(sub):
    alpha, beta = concentrated_basis()
    alpha = tuple(tuple(sp.expand(sp.sympify(x).subs(sub)) for x in row) for row in alpha)
    beta = tuple(tuple(sp.expand(sp.sympify(x).subs(sub)) for x in row) for row in beta)
    betat = tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))

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


def sing(expr):
    return str(sp.expand(expr)).replace("**", "^")


def run(program, timeout=550):
    t0 = time.time()
    try:
        cp = subprocess.run(["Singular", "-q"], input=program, text=True,
                            capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, time.time() - t0
    return cp.stdout, time.time() - t0


def projection(forms, params, label):
    eqs = [forms[wd] for wd in MIXED]
    eqs.append(forms[(0, 0, 0, 0)] - 1)
    eqs.append(W * forms[(1, 1, 1, 1)] - 1)
    eliminated = Z + (W,)
    variables = eliminated + T
    program = "\n".join((
        f"ring R=(0,{params}),(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
        "option(redSB);",
        "ideal I=" + ",".join(sing(x) for x in eqs) + ";",
        "ideal J=std(I);",
        "ideal L=eliminate(J," + "*".join(map(str, eliminated)) + ");",
        "L=std(L);",
        '"SHEETS";', "L;", "quit;",
    ))
    out, dt = run(program)
    lines = None
    if out is not None:
        lines = [ln.split("=", 1)[1].replace(" ", "") for ln in out.splitlines()
                 if ln.startswith("L[")]
    print(f"{label}: {'TIMEOUT' if lines is None else lines} ({dt:.1f}s)")
    return lines


def fitting(forms, alpha_p, beta_p, params, sheet_subs, minors, label):
    """Unit certificate: (mixed rows on sheet, selected minors, w*A*B-1)=(1)."""
    eqs = [forms[wd].subs(sheet_subs) for wd in MIXED]
    saturator = W * (forms[(0, 0, 0, 0)] * forms[(1, 1, 1, 1)]).subs(sheet_subs) - 1
    minor_polys = []
    for mode, rowset in minors:
        marked = one_marked_map(mode, tuple(
            tuple(sp.sympify(x).subs(sheet_subs) for x in row) for row in alpha_p
        ), tuple(
            tuple(sp.sympify(x).subs(sheet_subs) for x in row) for row in beta_p
        ))
        minor_polys.append(sp.expand(marked[list(rowset), :].det()))
    variables = Z + (W,)
    remaining_t = sorted({str(s) for eq in eqs for s in eq.free_symbols
                          if str(s).startswith("t")})
    allvars = list(map(str, variables)) + remaining_t
    program = "\n".join((
        f"ring R=(0,{params}),(" + ",".join(allvars) + "),dp;",
        "ideal I=" + ",".join(sing(x) for x in eqs + minor_polys + [saturator]) + ";",
        "I=std(I);",
        "int unit=(reduce(1,I)==0);",
        '"UNIT:"+string(unit);', "quit;",
    ))
    out, dt = run(program)
    status = "TIMEOUT" if out is None else \
        [ln for ln in out.splitlines() if ln.startswith("UNIT:")]
    print(f"  Fitting {label} minors={minors}: {status} ({dt:.1f}s)")
    return status


def main():
    # ---- divisor c=0 ----
    for q in (2, 3):
        forms, ap, bp = frames(q, {c: 0})
        sheets = projection(forms, "b,e,m", f"H31 q={q} on c=0")
    # ---- divisor e=-b ----
    for q in (2, 3):
        forms, ap, bp = frames(q, {e: -b})
        sheets = projection(forms, "b,m,c", f"H31 q={q} on b+e=0")
    # ---- H22 D_23 shadows ----
    forms, ap, bp = d23_frames({c: 0})
    projection(forms, "b,e,m,r", "H22 D_23 on c=0")
    forms, ap, bp = d23_frames({e: -b})
    projection(forms, "b,m,c,r", "H22 D_23 on b+e=0")


if __name__ == "__main__":
    main()
