#!/usr/bin/env python3
"""Incidence Jacobian rank and family tangent at the second, more generic
W-sample (x = t*(v0,v1) with t=2)."""
import itertools, sympy as sp

e = sp.Symbol("e")
v = sp.symbols("v0:4")
x = sp.symbols("x0:4")
z = sp.symbols("z0:4")
t0, t1, t2 = sp.symbols("t0:3")
U1_A = (0, 0, 1, -1)
Y3 = (0, 0, 1, 1)
COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
COMPLEMENT = {ab: tuple(sorted(set(range(4)) - set(ab))) for ab in COORD_PAIRS}
PERMS4 = tuple(itertools.permutations(range(4)))

def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}

def pairing(P, Q):
    return sp.expand(sum(P[ab]*Q[COMPLEMENT[ab]] for ab in COORD_PAIRS))

def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))

def analyse_sample(sample, name):
    vv = tuple(sample[k] for k in v); xx = tuple(sample[k] for k in x); ee = sample[e]
    rows = []
    for c in (rmul([0, 0, 1, -ee], Y3), rmul(list(xx), Y3)):
        form = pairing(rmul(list(z), list(vv)), c)
        rows.append([sp.nsimplify(sp.diff(form, zi)) for zi in z])
    M = sp.Matrix(rows)
    assert M.rank() == 2
    ker = M.nullspace(); assert len(ker) == 2
    planes = (
        sp.Matrix([[sp.nsimplify(c) for c in k] for k in ker]),
        sp.Matrix([list(U1_A), list(vv)]),
        sp.Matrix([[0, 0, 1, -ee], list(xx)]),
        sp.Matrix([list(Y3), [0, 0, 1, ee]]),
    )
    pivots = ((0, 2), (0, 2), (0, 2), (2, 3))
    reduced = []
    coordinate_point = []
    for plane, piv in zip(planes, pivots):
        chart = plane[:, piv].inv() * plane
        reduced.append(chart)
        nonpiv = tuple(i for i in range(4) if i not in piv)
        coordinate_point.extend(sp.nsimplify(chart[r_, c_]) for r_ in range(2) for c_ in nonpiv)
    T_point = {}
    for bits in itertools.product((0, 1), repeat=4):
        T_point[bits] = sp.nsimplify(perm4(tuple(tuple(reduced[m][bits[m], j] for j in range(4)) for m in range(4))))
    anchor = next(b for b in itertools.product((0, 1), repeat=4) if T_point[b] != 0)
    zvars = sp.symbols("Z0:16"); rvars = sp.symbols("R0:4")
    universal = []
    for mode, piv in enumerate(pivots):
        nonpiv = tuple(i for i in range(4) if i not in piv)
        plane = sp.zeros(2, 4)
        plane[0, piv[0]] = 1; plane[1, piv[1]] = 1
        entries = zvars[4*mode: 4*mode+4]
        for r_ in range(2):
            for o_, c_ in enumerate(nonpiv):
                plane[r_, c_] = entries[2*r_ + o_]
        universal.append(plane)
    T_universal = {}
    for bits in itertools.product((0, 1), repeat=4):
        T_universal[bits] = perm4(tuple(tuple(universal[m][bits[m], j] for j in range(4)) for m in range(4)))
    ratios = tuple(T_point[tuple((1-anchor[m_] if m_ == mode else anchor[m_]) for m_ in range(4))]/T_point[anchor]
                   for mode in range(4))
    equations = []
    for word in itertools.product((0, 1), repeat=4):
        if word == anchor:
            continue
        monomial = sp.prod(rvars[m] for m in range(4) if word[m] != anchor[m])
        equations.append(sp.expand(T_universal[word] - T_universal[anchor]*monomial))
    substitution = dict(zip(tuple(zvars)+tuple(rvars), tuple(coordinate_point)+ratios))
    assert all(sp.simplify(eq.subs(substitution)) == 0 for eq in equations)
    inc = sp.Matrix(equations).jacobian(tuple(zvars)+tuple(rvars)).subs(substitution)
    r = inc.rank()
    print(f"[{name}] anchor {anchor}; incidence Jacobian rank {r}; tangent dim {20-r}")
    return r

# sample 2: t=2 scaling, generic-ish
s2 = {e: -2, v[0]: 3, v[1]: -7, v[2]: 2, v[3]: 5, x[0]: 6, x[1]: -14, x[2]: -1, x[3]: 8}
analyse_sample(s2, "W sample 2")
# sample 3: another generic one, t=-3
s3 = {e: 5, v[0]: 1, v[1]: 2, v[2]: -3, v[3]: 7, x[0]: -3, x[1]: -6, x[2]: 4, x[3]: 9}
analyse_sample(s3, "W sample 3")
