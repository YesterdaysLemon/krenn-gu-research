#!/usr/bin/env python3
"""Triangle stratum: build Lambda, impose det=0, find rational samples,
compute invariants."""
import itertools, json, pathlib, sympy as sp

kappa, n2, n3, r = sp.symbols("kappa n2 n3 r")
tw = {eval(k): sp.sympify(v) for k, v in json.loads(pathlib.Path("triangle_data.json").read_text()).items()}
p = sp.symbols("p0:4")
q = sp.symbols("q0:4")

# t[(0,w)] linear in p; t[(1,w)] the same forms in q. verify and extract Lambda.
Lam = sp.zeros(4, 4)
for w in range(4):
    expr_p = tw[(0, w)]
    expr_q = tw[(1, w)]
    for j in range(4):
        Lam[w, j] = sp.expand(sp.diff(expr_p, p[j]))
        assert sp.simplify(sp.diff(expr_q, q[j]) - Lam[w, j]) == 0
    assert sp.simplify(expr_p - sum(Lam[w, j]*p[j] for j in range(4))) == 0
print("Lambda extracted; entries are polynomials in (kappa,n2,n3)")
detL = sp.factor(Lam.det())
print("det Lambda =", detL)
