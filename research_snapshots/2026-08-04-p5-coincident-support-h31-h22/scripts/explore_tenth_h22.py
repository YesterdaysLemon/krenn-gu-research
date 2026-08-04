#!/usr/bin/env python3
"""H22 weighted pencils for the tenth component.

D_01^r(u)=(r u0+u1, u2, u3, ext),  D_23^r(u)=(u0, u1, r u2+u3, ext).

Checks: (i) A-row identity for D_01 (symbolic k and slope), (ii) generic
structure of D_23 (ranks, kernels at a sample), (iii) exact char-0
function-field projections for both pencils over C(b,e,m,c,r) at k=1.
"""
from __future__ import annotations

import itertools
import subprocess
import time

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))
PERMS4 = tuple(itertools.permutations(range(4)))

b, e, k, m, c, r = sp.symbols("b e k m c r")
P = b * e * c + b + e
Q = b * e * (m + 1)
T = sp.symbols("t0:4")
Z = sp.symbols("x0:4") + sp.symbols("y0:4")
W = sp.Symbol("w")


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(4)) for p in PERMS4))


def concentrated_basis(kval=None):
    kk = k if kval is None else kval
    alpha = ((1, -1, 0, 0), (1, -1, 0, 0), (0, 0, 1, kk),
             (P, P * m - Q * c, -Q, Q * kk))
    beta = ((0, 1, b, -b * kk), (0, 1, e, -e * kk), (1, 1, 0, 0), (0, c, 1, -kk))
    return alpha, beta


def diag_row(row, ext, pencil, slope):
    if pencil == "01":
        return (slope * row[0] + row[1], row[2], row[3], ext)
    if pencil == "23":
        return (row[0], row[1], slope * row[2] + row[3], ext)
    raise ValueError(pencil)


def pencil_coeffs(pencil, kval=None, slope=r):
    alpha, beta = concentrated_basis(kval)
    betat = tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))
    alpha_d = tuple(diag_row(alpha[i], Z[i], pencil, slope) for i in range(4))
    beta_d = tuple(diag_row(betat[i], Z[4 + i], pencil, slope) for i in range(4))
    return {wd: perm4(tuple(beta_d[i] if wd[i] else alpha_d[i] for i in range(4)))
            for wd in WORDS}


def sing(expr):
    return str(sp.expand(expr)).replace("**", "^")


def run_singular(program, timeout):
    t0 = time.time()
    try:
        cp = subprocess.run(["Singular", "-q"], input=program, text=True,
                            capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, time.time() - t0, "TIMEOUT"
    if cp.returncode != 0 or cp.stderr.strip():
        return None, time.time() - t0, f"ERR rc={cp.returncode} stderr={cp.stderr[:400]}"
    return cp.stdout, time.time() - t0, "OK"


def a_row_identity_01():
    coeffs = pencil_coeffs("01", kval=None)  # k symbolic, slope symbolic
    a = coeffs[(0, 0, 0, 0)]
    assert sp.expand(a) == 0, a
    print("IDENTITY: D_01 pencil word-0000 coefficient vanishes identically"
          " (k, slope, marking, params all symbolic).")


def d23_structure():
    coeffs = pencil_coeffs("23", kval=1)
    Arow = sp.Matrix([[sp.diff(coeffs[(0, 0, 0, 0)], zz) for zz in Z]])
    print("D_23 A row (t-dependence?):",
          all(sp.expand(sp.diff(Arow[0, j], ti)) == 0 for j in range(8) for ti in T))
    print("  A =", [sp.factor(Arow[0, j]) for j in range(8)])
    sample = {b: 2, e: 3, m: 7, c: 11, r: sp.Rational(5, 3)}
    tsample = {T[i]: v for i, v in enumerate((5, -4, 9, sp.Rational(3, 7)))}
    M = sp.Matrix([[sp.diff(coeffs[wd], zz) for zz in Z] for wd in MIXED])
    Ms = M.subs(sample).subs(tsample)
    Bs = sp.Matrix([[sp.diff(coeffs[(1, 1, 1, 1)], zz) for zz in Z]]).subs(sample).subs(tsample)
    As = Arow.subs(sample)
    ns = Ms.nullspace()
    print(f"  D_23 sample rank={Ms.rank()}, kernel dim={len(ns)}")
    for i, v in enumerate(ns):
        print(f"    kernel[{i}]: A={sp.nsimplify((As*v)[0])}, B={sp.nsimplify((Bs*v)[0])}")


def projection(pencil, timeout=550):
    coeffs = pencil_coeffs(pencil, kval=1)
    eqs = [coeffs[wd] for wd in MIXED]
    eqs.append(coeffs[(0, 0, 0, 0)] - 1)
    eqs.append(W * coeffs[(1, 1, 1, 1)] - 1)
    eliminated = Z + (W,)
    variables = eliminated + T
    program = "\n".join((
        "ring R=(0,b,e,m,c,r),(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
        "option(redSB);",
        "ideal incidence=" + ",".join(sing(x) for x in eqs) + ";",
        "ideal basis=std(incidence);",
        "ideal marking=eliminate(basis," + "*".join(map(str, eliminated)) + ");",
        "marking=std(marking);",
        '"MARKING";',
        "marking;",
        "quit;",
    ))
    out, dt, status = run_singular(program, timeout)
    print(f"pencil {pencil}: {status} in {dt:.1f}s")
    if out is not None:
        for line in out.splitlines():
            if line.startswith("marking[") or line == "MARKING":
                print("   ", line.strip())
    return out


def main():
    a_row_identity_01()
    d23_structure()
    projection("23")


if __name__ == "__main__":
    main()
