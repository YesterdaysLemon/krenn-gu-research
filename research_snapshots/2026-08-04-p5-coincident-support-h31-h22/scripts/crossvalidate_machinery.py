#!/usr/bin/env python3
"""Cross-validate my H31 frame machinery against the repo's seventh-component
verifier (known EXPECTED_PROJECTIONS), and check the concentrated tenth-
component basis spans the certified planes with the certified tensor.
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

T = sp.symbols("t0:4")
Z = sp.symbols("x0:4") + sp.symbols("y0:4")
W = sp.Symbol("w")


def perm3(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(3)) for p in PERMS3))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(4)) for p in PERMS4))


def word_coeffs(q, alpha, beta):
    betat = tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))
    common = tuple(j for j in range(4) if j != q)
    alph = tuple(tuple(alpha[i][j] for j in common) for i in range(4))
    bett = tuple(tuple(betat[i][j] for j in common) for i in range(4))
    out = {}
    for wd in WORDS:
        expr = 0
        for i in range(4):
            others = tuple((bett[j] if wd[j] else alph[j]) for j in range(4) if j != i)
            zv = Z[i + (4 if wd[i] else 0)]
            expr += perm3(others) * zv
        out[wd] = sp.expand(expr)
    return out


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


def projection(q, alpha, beta, params, timeout=600):
    coeffs = word_coeffs(q, alpha, beta)
    eqs = [coeffs[wd] for wd in MIXED]
    eqs.append(coeffs[(0, 0, 0, 0)] - 1)
    eqs.append(W * coeffs[(1, 1, 1, 1)] - 1)
    eliminated = Z + (W,)
    variables = eliminated + T
    program = "\n".join((
        "ring R=(0," + ",".join(params) + "),("
        + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
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
    lines = []
    if out is not None:
        lines = [ln.split("=", 1)[1].replace(" ", "") for ln in out.splitlines()
                 if ln.startswith("marking[")]
    return tuple(lines), dt, status


def seventh_component_check():
    s, d, u, v = sp.symbols("s d u v")
    h = s - d
    planes = (
        ((1, 0, 0, -1), (0, 0, 1, 1)),
        ((s, 1 - u, 0, d + u * h), (0, 1 - v, s, d + v * h)),
        ((1, 0, -1, 0), (0, 1, -s, -d)),
        ((1, 0, 0, 1), (0, 0, 1, -1)),
    )
    alpha = (
        planes[0][0],
        tuple(sp.expand(v * planes[1][0][j] - u * planes[1][1][j]) for j in range(4)),
        planes[2][0],
        planes[3][1],
    )
    beta = (planes[0][1], planes[1][0], planes[2][1], planes[3][0])
    expected = {
        0: ("t3", "(u-v)*t2+(-s*v)", "(u-v)*t1+(u-1)", "t0-1"),
        1: ("1",),
        2: ("t3-1", "(u-v)*t2+(-s*v)", "(u-v)*t1+(u-1)", "t0"),
        3: ("t3", "(u-v)*t2+(-s*v)", "(u-v)*t1+(u-1)", "t0"),
    }
    for q in range(4):
        got, dt, status = projection(q, alpha, beta, ("s", "d", "u", "v"))
        ok = status == "OK" and got == expected[q]
        print(f"seventh q={q}: {status} {dt:.0f}s -> {got}  MATCH={ok}")
        assert ok, (q, got, expected[q])
    print("SEVENTH-COMPONENT CROSS-VALIDATION PASSED")


def tenth_plane_check():
    b, e, k, m, c = sp.symbols("b e k m c")
    P = b * e * c + b + e
    Q = b * e * (m + 1)
    Zplanes = [
        [(1, -1, 0, 0), (0, 1, b, -b * k)],
        [(1, -1, 0, 0), (0, 1, e, -e * k)],
        [(1, 1, 0, 0), (0, 0, 1, k)],
        [(1, m, 0, 0), (0, c, 1, -k)],
    ]
    alpha = (
        (1, -1, 0, 0),
        (1, -1, 0, 0),
        (0, 0, 1, k),
        (P, P * m - Q * c, -Q, Q * k),
    )
    beta = (
        (0, 1, b, -b * k),
        (0, 1, e, -e * k),
        (1, 1, 0, 0),
        (0, c, 1, -k),
    )
    for i in range(4):
        stack = sp.Matrix([list(Zplanes[i][0]), list(Zplanes[i][1]),
                           list(alpha[i]), list(beta[i])])
        assert stack.rank() == 2, i
    print("tenth: concentrated (alpha,beta) span the certified planes (rank-2 stacks)")
    Tt = {wd: perm4(tuple(beta[i] if wd[i] else alpha[i] for i in range(4)))
          for wd in WORDS}
    assert sp.expand(Tt[(1, 1, 1, 1)] + 2 * k * P) == 0
    assert all(sp.expand(val) == 0 for wd, val in Tt.items() if wd != (1, 1, 1, 1))
    print("tenth: T = -2*k*(b*e*c+b+e) e_1111, all other 15 words vanish (k symbolic)")
    # certified raw support identity at the certificate point
    point = {b: 2, e: 3, k: 5, m: 7, c: 11}
    raw = {wd: perm4(tuple(Zplanes[i][wd[i]] for i in range(4))).subs(point)
           for wd in WORDS}
    assert raw[(1, 1, 0, 0)] == -2 * 2 * 3 * 5 * 8 and raw[(1, 1, 0, 1)] == -2 * 5 * (2 * 3 * 11 + 5)
    assert all(val == 0 for wd, val in raw.items() if wd not in ((1, 1, 0, 0), (1, 1, 0, 1)))
    print("tenth: raw two-word support at (2,3,5,7,11) matches the working note")


if __name__ == "__main__":
    tenth_plane_check()
    seventh_component_check()
