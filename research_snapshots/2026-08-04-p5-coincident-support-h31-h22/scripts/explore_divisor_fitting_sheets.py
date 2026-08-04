#!/usr/bin/env python3
"""Per-sheet char-0 Fitting closures of the divisor survivor sheets.

{b+e=0}: sheets t=(1,0,0,-1/(2b^2)) and t=(0,1,0,-1/(2b^2))  (fully rational);
{c=0}:   sheet t2=t3=0 with (t0,t1) on the linear+quadratic locus (adjoined).

Certificate per sheet: ideal(mixed rows, det P_2[0,1,2,7], det P_2[0,1,3,7],
w*A*B-1) = (1) over the divisor function field.
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

MINOR_ROWS = ((0, 1, 2, 7), (0, 1, 3, 7))
MODE = 2


def perm3(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(3)) for p in PERMS3))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(4)) for p in PERMS4))


def concentrated_basis(sub):
    alpha = ((1, -1, 0, 0), (1, -1, 0, 0), (0, 0, 1, 1), (P, P * m - Q * c, -Q, Q))
    beta = ((0, 1, b, -b), (0, 1, e, -e), (1, 1, 0, 0), (0, c, 1, -1))
    alpha = tuple(tuple(sp.expand(sp.sympify(x).subs(sub)) for x in row) for row in alpha)
    beta = tuple(tuple(sp.expand(sp.sympify(x).subs(sub)) for x in row) for row in beta)
    return alpha, beta


def build(q_or_pencil, sub, tsubs):
    """q in {2,3} for H31 deletion frames; 'd23' for the weighted pencil."""
    alpha, beta = concentrated_basis(sub)
    betat = tuple(tuple(sp.expand(sp.together(beta[i][j] + tsubs[i] * alpha[i][j]))
                        for j in range(4)) for i in range(4))
    # clear denominators rowwise (denominators are powers of 2b^2 etc.)
    cleaned = []
    for i in range(4):
        row = betat[i]
        dens = [sp.fraction(sp.cancel(x))[1] for x in row]
        lcm = sp.lcm(dens)
        cleaned.append(tuple(sp.expand(sp.cancel(x * lcm)) for x in row))
    betat = tuple(cleaned)
    if q_or_pencil == "d23":
        def drow(row, ext):
            return (row[0], row[1], sp.expand(r * row[2] + row[3]), ext)
        alpha_p = tuple(drow(alpha[i], Z[i]) for i in range(4))
        beta_p = tuple(drow(betat[i], Z[4 + i]) for i in range(4))
    else:
        q = q_or_pencil
        common = tuple(j for j in range(4) if j != q)
        alpha_p = tuple(tuple(alpha[i][j] for j in common) + (Z[i],) for i in range(4))
        beta_p = tuple(tuple(betat[i][j] for j in common) + (Z[4 + i],)
                       for i in range(4))
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


def certificate(label, forms, alpha_p, beta_p, params, extra_vars=(), extra_eqs=()):
    marked = one_marked_map(MODE, alpha_p, beta_p)
    minors = [sp.expand(marked[list(rows_), :].det()) for rows_ in MINOR_ROWS]
    eqs = [forms[wd] for wd in MIXED] + minors + list(extra_eqs)
    eqs.append(forms[(0, 0, 0, 0)] - 1)
    eqs.append(W * forms[(1, 1, 1, 1)] - 1)
    variables = list(map(str, Z + (W,))) + list(map(str, extra_vars))
    order = f"(dp(9),dp({len(extra_vars)}))" if extra_vars else "dp"
    program = "\n".join((
        f"ring R=(0,{params}),(" + ",".join(variables) + f"),{order};",
        "ideal I=" + ",".join(sing(x) for x in eqs) + ";",
        "I=std(I);",
        "int unit=(reduce(1,I)==0);",
        '"UNIT:"+string(unit);', "quit;",
    ))
    out, dt = run(program)
    status = "TIMEOUT-null" if out is None else \
        ",".join(ln for ln in out.splitlines() if ln.startswith("UNIT:"))
    print(f"{label}: {status} ({dt:.1f}s)", flush=True)
    return status


def main():
    t3v = sp.Rational(-1, 2) / b**2
    for q in (2, 3):
        for t1v, name in ((0, "sheetA t=(1,0,0,-1/2b^2)"),
                          (1, "sheetB t=(0,1,0,-1/2b^2)")):
            forms, ap, bp = build(q, {e: -b}, (1 - t1v, t1v, 0, t3v))
            certificate(f"H31 q={q} b+e=0 {name}", forms, ap, bp, "b,m,c")
    for name, frame in (("q=2", 2), ("q=3", 3)):
        t0s, t1s = sp.symbols("s0 s1")
        forms, ap, bp = build(frame, {c: 0}, (t0s, t1s, 0, 0))
        lin = (e**2 * m + e**2) * t0s + (b**2 * m + b**2) * t1s \
            + (-b**2 + b * e * m - b * e - e**2)
        quad = (b**2 * m**2 - b**2) * t1s**2 \
            + (2 * b**2 + b * e * m**2 - 2 * b * e * m + b * e - 2 * e**2 * m) * t1s \
            + (-b**2 + b * e * m - b * e + e**2 * m)
        certificate(f"H31 {name} c=0 sheet (adjoined)", forms, ap, bp, "b,e,m",
                    extra_vars=(t0s, t1s), extra_eqs=(lin, quad))
    # weighted pencil on the divisors
    for t1v, name in ((0, "sheetA"), (1, "sheetB")):
        forms, ap, bp = build("d23", {e: -b}, (1 - t1v, t1v, 0, t3v))
        certificate(f"H22 D_23 b+e=0 {name}", forms, ap, bp, "b,m,c,r")
    t0s, t1s = sp.symbols("s0 s1")
    forms, ap, bp = build("d23", {c: 0}, (t0s, t1s, 0, 0))
    lin = (e**2 * m + e**2) * t0s + (b**2 * m + b**2) * t1s \
        + (-b**2 + b * e * m - b * e - e**2)
    quad = (b**2 * m**2 - b**2) * t1s**2 \
        + (2 * b**2 + b * e * m**2 - 2 * b * e * m + b * e - 2 * e**2 * m) * t1s \
        + (-b**2 + b * e * m - b * e + e**2 * m)
    certificate("H22 D_23 c=0 sheet (adjoined)", forms, ap, bp, "b,e,m,r",
                extra_vars=(t0s, t1s), extra_eqs=(lin, quad))


if __name__ == "__main__":
    main()
