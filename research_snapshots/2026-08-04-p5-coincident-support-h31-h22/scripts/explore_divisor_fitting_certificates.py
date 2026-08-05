#!/usr/bin/env python3
"""Chart-free char-0 Fitting closures of the divisors {c=0} and {b+e=0}:

  ideal( 14 mixed rows, det P_mode2[0,1,2,7], det P_mode2[0,1,3,7],
         w*A*B - 1 )  over the divisor function field, all markings t free
  = (1)?

Frames: H31 q=2,3 and the weighted D_23 pencil (slope r in the field).
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
MARKED_MODE = 2


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


def h31_frame(q, sub):
    alpha, beta = concentrated_basis(sub)
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
    alpha_p = tuple(alph[i] + (Z[i],) for i in range(4))
    beta_p = tuple(bett[i] + (Z[4 + i],) for i in range(4))
    return forms, alpha_p, beta_p


def d23_frame(sub):
    alpha, beta = concentrated_basis(sub)
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


def certificate(label, forms, alpha_p, beta_p, params):
    marked = one_marked_map(MARKED_MODE, alpha_p, beta_p)
    minors = [sp.expand(marked[list(rows_), :].det()) for rows_ in MINOR_ROWS]
    eqs = [forms[wd] for wd in MIXED]
    eqs += minors
    eqs.append(W * forms[(0, 0, 0, 0)] * forms[(1, 1, 1, 1)] - 1)
    variables = list(map(str, Z + (W,) + T))
    program = "\n".join((
        f"ring R=(0,{params}),(" + ",".join(variables) + "),(dp(9),dp(4));",
        "ideal I=" + ",".join(sing(x) for x in eqs) + ";",
        "I=std(I);",
        "int unit=(reduce(1,I)==0);",
        '"UNIT:"+string(unit);', "quit;",
    ))
    out, dt = run(program)
    status = "TIMEOUT" if out is None else \
        ",".join(ln for ln in out.splitlines() if ln.startswith("UNIT:"))
    print(f"{label}: {status} ({dt:.1f}s)")
    return status


def main():
    for q in (2, 3):
        forms, ap, bp = h31_frame(q, {c: 0})
        certificate(f"H31 q={q} on c=0 (mode-2 minors 0127+0137)", forms, ap, bp,
                    "b,e,m")
    for q in (2, 3):
        forms, ap, bp = h31_frame(q, {e: -b})
        certificate(f"H31 q={q} on b+e=0 (mode-2 minors 0127+0137)", forms, ap, bp,
                    "b,m,c")
    forms, ap, bp = d23_frame({c: 0})
    certificate("H22 D_23 on c=0 (mode-2 minors 0127+0137)", forms, ap, bp,
                "b,e,m,r")
    forms, ap, bp = d23_frame({e: -b})
    certificate("H22 D_23 on b+e=0 (mode-2 minors 0127+0137)", forms, ap, bp,
                "b,m,c,r")


if __name__ == "__main__":
    main()
