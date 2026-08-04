#!/usr/bin/env python3
"""Global char-0 unit certificates: is (M z, A z - 1, w*Bz - 1) the unit ideal
in Q[b,e,m,c][t,z,w] (params as ring variables)?  If yes, the q-frame
exclusion holds at EVERY chart point, not only generically.
Tries std and slimgb with 550 s budgets; fail-open reporting (nulls recorded).
Also q=3, and the H22 D_23 pencil with r as a ring variable.
"""
from __future__ import annotations

import itertools
import subprocess
import time

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))
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


def h31_forms(q):
    alpha, beta = concentrated_basis()
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
    return forms


def d23_forms():
    alpha, beta = concentrated_basis()
    betat = tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))

    def drow(row, ext):
        return (row[0], row[1], r * row[2] + row[3], ext)

    alpha_d = tuple(drow(alpha[i], Z[i]) for i in range(4))
    beta_d = tuple(drow(betat[i], Z[4 + i]) for i in range(4))
    return {wd: perm4(tuple(beta_d[i] if wd[i] else alpha_d[i] for i in range(4)))
            for wd in WORDS}


def sing(expr):
    return str(sp.expand(expr)).replace("**", "^")


def attempt(label, forms, extra_ring_vars, engine, timeout=550):
    eqs = [forms[wd] for wd in MIXED]
    eqs.append(forms[(0, 0, 0, 0)] - 1)
    eqs.append(W * forms[(1, 1, 1, 1)] - 1)
    variables = list(map(str, Z + (W,) + T)) + extra_ring_vars
    blocks = f"(dp(9),dp(4),dp({len(extra_ring_vars)}))"
    program = "\n".join((
        "ring R=0,(" + ",".join(variables) + f"),{blocks};",
        "ideal I=" + ",".join(sing(x) for x in eqs) + ";",
        (f"ideal J={engine}(I);"),
        "int unit=(reduce(1,J)==0);",
        '"UNIT:"+string(unit);',
        "quit;",
    ))
    t0 = time.time()
    try:
        cp = subprocess.run(["Singular", "-q"], input=program, text=True,
                            capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"{label} [{engine}]: TIMEOUT ({time.time()-t0:.0f}s) -> null")
        return None
    dt = time.time() - t0
    unit_lines = [ln for ln in cp.stdout.splitlines() if ln.startswith("UNIT:")]
    print(f"{label} [{engine}]: {unit_lines} ({dt:.1f}s)")
    return unit_lines


def main():
    for q in (2, 3):
        forms = h31_forms(q)
        got = attempt(f"H31 q={q} global", forms, ["b", "e", "m", "c"], "slimgb")
        if got is None:
            attempt(f"H31 q={q} global", forms, ["b", "e", "m", "c"], "std")
    forms = d23_forms()
    got = attempt("H22 D_23 global", forms, ["b", "e", "m", "c", "r"], "slimgb")
    if got is None:
        attempt("H22 D_23 global", forms, ["b", "e", "m", "c", "r"], "std")


if __name__ == "__main__":
    main()
