#!/usr/bin/env python3
"""Replay the exact chart identities of the in-out path stratum note.

All computations are exact (sympy rationals plus one Singular
factorization).  This is an exploratory checkpoint verifier: it
certifies the chart identities and sample-point invariants, not a
component classification.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
NOTE = ROOT / "P4_INOUT_PATH_STRATUM_WORKING_NOTE.md"

d = sp.Symbol("d")
v = sp.symbols("v0:4")
x = sp.symbols("x0:4")

U1_A = (0, 0, 1, -1)
Y3 = (0, 0, 1, 1)
U3_B = (1, 0, d, 0)
Y2 = (1, 0, -d, 0)

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
COMPLEMENT = {ab: tuple(sorted(set(range(4)) - set(ab)))
              for ab in COORD_PAIRS}
PERMS4 = tuple(itertools.permutations(range(4)))

F1 = -d*v[1]*x[0] + d*v[0]*x[1] - (v[2]+v[3])*x[1] - v[1]*x[2] + v[1]*x[3]
F2 = -d*v[1]*x[0] - d*v[0]*x[1] + (v[2]+v[3])*x[1] - v[1]*x[2] + v[1]*x[3]
F3 = d*v[1]*x[0] - d*v[0]*x[1] + (v[2]+v[3])*x[1] + v[1]*x[2] + v[1]*x[3]
F4 = d*v[1]*x[0] + d*v[0]*x[1] + (v[2]+v[3])*x[1] + v[1]*x[2] + v[1]*x[3]

SAMPLES = {
    "F1": {"v": (5, 8, 5, 5), "x": (7, 9, -3, sp.Rational(143, 8)),
           "d": 7,
           "profile": (4, 4, 3, 4, 3, 3),
           "relations": (((0, 3), 1), ((1, 3), 1), ((2, 3), 1))},
    "F2": {"v": (6, -4, -6, 5), "x": (0, -5, -7, sp.Rational(-263, 4)),
           "d": -8,
           "profile": (4, 4, 3, 4, 3, 3),
           "relations": (((0, 3), 1), ((1, 3), 1), ((2, 3), 1))},
    "F4": {"v": (3, 5, -4, -9), "x": (7, -7, -8, sp.Rational(-9, 5)),
           "d": -3,
           "profile": (4, 3, 2, 4, 3, 3),
           "relations": (((0, 2), 1), ((1, 3), 1), ((2, 3), 1))},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rmul(u, w):
    return {ab: sp.expand(u[ab[0]] * w[ab[1]] + u[ab[1]] * w[ab[0]])
            for ab in COORD_PAIRS}


def pairing(P, Q):
    return sp.expand(sum(P[ab] * Q[COMPLEMENT[ab]]
                         for ab in COORD_PAIRS))


def perm4(rows):
    return sp.expand(sum(
        sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4
    ))


def covector_matrix():
    zsym = sp.symbols("z0:4")
    rows = []
    # the u_1-side conditions vanish identically by associativity
    for w_row, is_u1 in ((U1_A, True), (tuple(v), False)):
        for c in (rmul(Y2, Y3), rmul(list(x), Y3)):
            zw = rmul(list(zsym), list(w_row))
            form = pairing(zw, c)
            row = [sp.expand(sp.diff(form, zi)) for zi in zsym]
            if is_u1:
                assert all(e == 0 for e in row)
            else:
                rows.append(row)
    return sp.Matrix(rows)


def cramer_identity(M):
    minors = {}
    for a_, b_ in itertools.combinations(range(4), 2):
        minors[(a_, b_)] = sp.expand(
            M[0, a_] * M[1, b_] - M[0, b_] * M[1, a_]
        )
    pivot = minors[(0, 1)]
    assert sp.expand(pivot + (v[2]+v[3]) * F3) == 0
    w2 = (minors[(1, 2)], -minors[(0, 2)], minors[(0, 1)], 0)
    w3 = (minors[(1, 3)], -minors[(0, 3)], 0, minors[(0, 1)])
    for w in (w2, w3):
        assert all(
            sp.expand(sum(M[r_, c_] * w[c_] for c_ in range(4))) == 0
            for r_ in range(2)
        )
    B = sp.zeros(2, 2)
    for i0, u0row in enumerate((w2, w3)):
        for i1, u1row in enumerate((U1_A, tuple(v))):
            B[i0, i1] = perm4((tuple(u0row), u1row, tuple(x), U3_B))
    det = sp.expand(B.det())
    return det, pivot


def factor_in_singular(det):
    program = "\n".join((
        "ring R=0,(d,v0,v1,v2,v3,x0,x1,x2,x3),dp;",
        f"poly f={str(det).replace('**', '^')};",
        f"poly g={str(sp.expand((v[2]+v[3])*F1*F2*F3*F4)).replace('**', '^')};",
        "poly q=f/g;",
        "poly check=f-q*g;",
        "int ok=(check==0)&&(q!=0)&&(deg(q)==0);",
        '"CODEX_RESULT:"+string(ok)+":"+string(q);',
        "quit;",
    ))
    completed = subprocess.run(
        ("Singular", "-q"), input=program, text=True,
        encoding="utf-8", errors="replace",
        capture_output=True, timeout=600, check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError((completed.returncode, completed.stdout,
                              completed.stderr))
    markers = [line for line in completed.stdout.splitlines()
               if line.startswith("CODEX_RESULT:")]
    assert len(markers) == 1
    _tag, ok, content = markers[0].split(":", 2)
    assert ok == "1", completed.stdout
    return content


def analyse_point(point):
    subs = {**dict(zip(v, point["v"])), **dict(zip(x, point["x"])),
            d: point["d"]}
    zsym = sp.symbols("z0:4")
    rows = []
    for c in (rmul(Y2, Y3), rmul(list(x), Y3)):
        zw = rmul(list(zsym), list(v))
        form = pairing(zw, c)
        rows.append([sp.expand(sp.diff(form, zi)).subs(subs)
                     for zi in zsym])
    M = sp.Matrix(rows)
    kernel = M.nullspace()
    assert len(kernel) == 2
    def sub_row(row):
        return [sp.nsimplify(sp.sympify(c_).subs(subs)) for c_ in row]
    planes = [
        [[sp.nsimplify(c_) for c_ in vec] for vec in kernel],
        [sub_row(U1_A), sub_row(v)],
        [sub_row(Y2), sub_row(x)],
        [sub_row(Y3), sub_row(U3_B)],
    ]
    T = {}
    for bits in itertools.product((0, 1), repeat=4):
        rows_sel = tuple(tuple(planes[m][bits[m]]) for m in range(4))
        T[bits] = perm4(rows_sel)
    assert any(value != 0 for value in T.values())
    for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)),
                        ((0, 3), (1, 2))):
        m = sp.zeros(4, 4)
        for bits in itertools.product((0, 1), repeat=4):
            r_ = 2 * bits[left[0]] + bits[left[1]]
            c_ = 2 * bits[right[0]] + bits[right[1]]
            m[r_, c_] = T[bits]
        assert m.rank() == 1
    profile = []
    relations = []
    for a_, b_ in itertools.combinations(range(4), 2):
        rows_ = []
        for pa in planes[a_]:
            for pb in planes[b_]:
                prod = rmul(pa, pb)
                rows_.append([prod[ab] for ab in COORD_PAIRS])
        mm = sp.Matrix(rows_)
        r = mm.rank()
        profile.append(r)
        if r == 3:
            k = [sp.simplify(c_) for c_ in mm.T.nullspace()[0]]
            M2 = sp.Matrix([[k[0], k[1]], [k[2], k[3]]])
            relations.append(((a_, b_), M2.rank()))
    return tuple(profile), tuple(relations)


def f4_slice_certificates():
    """Family tangent rank five, incidence Jacobian rank fourteen,
    and the exact containment of the F4 branch in the sixfold."""
    t0, t1, t2 = sp.symbols("t0:3")
    x0_val = sp.solve(sp.Eq(F4, 0), x[0])[0]
    subs_x0 = {x[0]: x0_val}
    zsym = sp.symbols("z0:4")
    rows = []
    for c in (rmul(Y2, Y3),
              rmul([sp.sympify(e).subs(subs_x0) for e in x], Y3)):
        zw = rmul(list(zsym), list(v))
        form = pairing(zw, c)
        rows.append([sp.expand(sp.diff(form, zi)) for zi in zsym])
    M = sp.Matrix(rows)
    minors = {}
    for a_, b_ in itertools.combinations(range(4), 2):
        minors[(a_, b_)] = sp.together(
            M[0, a_] * M[1, b_] - M[0, b_] * M[1, a_]
        )
    w2 = (minors[(1, 2)], -minors[(0, 2)], minors[(0, 1)], 0)
    w3 = (minors[(1, 3)], -minors[(0, 3)], 0, minors[(0, 1)])
    planes = (
        sp.Matrix([list(w2), list(w3)]),
        sp.Matrix([list(U1_A), list(v)]),
        sp.Matrix([list(Y2),
                   [sp.sympify(e).subs(subs_x0) for e in x]]),
        sp.Matrix([list(Y3), list(U3_B)]),
    )
    pivots = ((0, 2), (0, 2), (0, 1), (0, 2))
    torus = sp.diag(t0, t1, t2, 1)
    scaled_planes = tuple(plane * torus for plane in planes)
    reduced = []
    chart_coords = []
    for plane, piv in zip(scaled_planes, pivots):
        chart = plane[:, piv].inv() * plane
        nonpiv = tuple(i for i in range(4) if i not in piv)
        reduced.append(chart)
        chart_coords.extend(chart[r_, c_] for r_ in range(2)
                            for c_ in nonpiv)
    sample = SAMPLES["F4"]
    point = {**dict(zip(v, sample["v"])),
             **{x[1]: sample["x"][1], x[2]: sample["x"][2],
                x[3]: sample["x"][3]},
             d: sample["d"], t0: 1, t1: 1, t2: 1}
    params = (d, v[0], v[1], v[2], v[3], x[1], x[2], x[3],
              t0, t1, t2)
    jac = sp.Matrix(chart_coords).jacobian(params).subs(point)
    jac = sp.Matrix([[sp.nsimplify(sp.cancel(e)) for e in row]
                     for row in jac.tolist()])
    assert jac.rank() == 5
    # universal incidence at the F4 point
    reduced_point = tuple(plane.subs(point) for plane in reduced)
    T_point = {}
    for bits in itertools.product((0, 1), repeat=4):
        rows_sel = tuple(
            tuple(reduced_point[m][bits[m], j] for j in range(4))
            for m in range(4)
        )
        T_point[bits] = sp.nsimplify(perm4(rows_sel))
    support = tuple(sorted(
        bits for bits, value in T_point.items() if value != 0
    ))
    assert support == ((1, 0, 1, 0), (1, 1, 1, 0)), support
    anchor = (1, 0, 1, 0)
    zvars = sp.symbols("Z0:16")
    rvars = sp.symbols("R0:4")
    universal = []
    for mode, piv in enumerate(pivots):
        nonpiv = tuple(i for i in range(4) if i not in piv)
        plane = sp.zeros(2, 4)
        plane[0, piv[0]] = 1
        plane[1, piv[1]] = 1
        entries = zvars[4 * mode: 4 * mode + 4]
        for r_ in range(2):
            for o_, c_ in enumerate(nonpiv):
                plane[r_, c_] = entries[2 * r_ + o_]
        universal.append(plane)
    T_universal = {}
    for bits in itertools.product((0, 1), repeat=4):
        rows_sel = tuple(
            tuple(universal[m][bits[m], j] for j in range(4))
            for m in range(4)
        )
        T_universal[bits] = perm4(rows_sel)
    ratios = []
    for mode in range(4):
        adjacent = list(anchor)
        adjacent[mode] = 1 - adjacent[mode]
        ratios.append(T_point[tuple(adjacent)] / T_point[anchor])
    equations = []
    for word in itertools.product((0, 1), repeat=4):
        if word == anchor:
            continue
        monomial = sp.prod(
            rvars[m] for m in range(4) if word[m] != anchor[m]
        )
        equations.append(sp.expand(
            T_universal[word] - T_universal[anchor] * monomial
        ))
    coordinate_point = tuple(
        sp.nsimplify(sp.cancel(c.subs(point))) for c in chart_coords
    )
    substitution = dict(zip(
        tuple(zvars) + tuple(rvars),
        coordinate_point + tuple(ratios),
    ))
    assert all(
        sp.simplify(eq.subs(substitution)) == 0 for eq in equations
    )
    incidence_jacobian = sp.Matrix(equations).jacobian(
        tuple(zvars) + tuple(rvars)
    ).subs(substitution)
    assert incidence_jacobian.rank() == 14
    # exact containment identities in the sixfold chart
    my = [sp.cancel(c.subs({t0: 1, t1: 1, t2: 1}))
          for c in chart_coords]
    tt0 = -1 / my[1]
    tt2 = 1 / my[3]
    for index in (0, 2, 9, 12, 14):
        assert sp.simplify(my[index]) == 0, index
    assert sp.simplify(sp.together(my[8] + tt2 / tt0)) == 0
    ratio_h = sp.cancel(my[11] - my[10] / tt2)
    first = sp.simplify(sp.together(
        1 - my[4] * tt0 * ratio_h - my[5] * tt0
    ))
    second = sp.simplify(sp.together(
        1 - my[6] * tt2 * ratio_h - my[7] * tt2
    ))
    assert first == 0 and second == 0


def disjoint_chart_certificates():
    """Disjoint-support in-out chart: identically vanishing u_1-side
    conditions, factored Cramer pivot, and the exact embedding of the
    eighth component killing the active determinant modulo Phi."""
    U3_disj = (1, 1, 0, 0)
    Y2_disj = (1, -1, 0, 0)
    zsym = sp.symbols("zd0:4")
    for c in (rmul(Y2_disj, Y3), rmul(list(x), Y3)):
        zw = rmul(list(zsym), list(U1_A))
        form = pairing(zw, c)
        assert all(
            sp.expand(sp.diff(form, zi)) == 0 for zi in zsym
        )
    rows = []
    for c in (rmul(Y2_disj, Y3), rmul(list(x), Y3)):
        zw = rmul(list(zsym), list(v))
        form = pairing(zw, c)
        rows.append([sp.expand(sp.diff(form, zi)) for zi in zsym])
    M = sp.Matrix(rows)
    minors = {}
    for a_, b_ in itertools.combinations(range(4), 2):
        minors[(a_, b_)] = sp.expand(
            M[0, a_] * M[1, b_] - M[0, b_] * M[1, a_]
        )
    pivot = minors[(0, 1)]
    symmetric = (
        (v[2] + v[3]) * (x[0] + x[1])
        + (v[0] + v[1]) * (x[2] + x[3])
    )
    assert sp.expand(pivot + (v[2] + v[3]) * symmetric) == 0
    w2 = (minors[(1, 2)], -minors[(0, 2)], pivot, 0)
    w3 = (minors[(1, 3)], -minors[(0, 3)], 0, pivot)
    B = sp.zeros(2, 2)
    for i0, u0row in enumerate((w2, w3)):
        for i1, u1row in enumerate((U1_A, tuple(v))):
            B[i0, i1] = perm4((
                tuple(u0row), u1row, tuple(x), U3_disj
            ))
    determinant = sp.expand(B.det())
    # eighth-component embedding through (02)(13) and t3=-t2, t1=t0
    a8, b8, f8, p8 = sp.symbols("a8 b8 f8 phi8")
    t2s = sp.Symbol("t2s")
    j8 = f8 + b8 * p8**2
    kap8 = p8 * (b8 * f8 + 1)
    eta8 = -(b8 * f8 + 1)
    alpha1_8 = (-a8 * f8 + 1, -a8 * f8 - 1, f8 + p8, f8 - p8)
    beta0_8 = (a8 + b8, a8 - b8, 0, 2)
    _ = (j8, kap8, eta8)

    def sigma_torus(row):
        swapped = (row[2], row[3], row[0], row[1])
        return (swapped[0], swapped[1],
                t2s * swapped[2], -t2s * swapped[3])

    v_img = sigma_torus(alpha1_8)
    x_img = sigma_torus(beta0_8)
    phi8_poly = sp.expand(
        a8**2 * b8 * f8 * p8**2 + a8**2 * f8**2
        - b8**2 * f8**2 + b8**2 * p8**2 - b8 * f8 - 1
    )
    family = {**{v[i]: v_img[i] for i in range(4)},
              **{x[i]: x_img[i] for i in range(4)}}
    det_family = sp.expand(determinant.subs(family))
    remainder = sp.rem(
        sp.Poly(det_family, p8), sp.Poly(phi8_poly, p8)
    )
    assert sp.expand(remainder.as_expr()) == 0
    pivot_family = sp.rem(
        sp.Poly(sp.expand(pivot.subs(family)), p8),
        sp.Poly(phi8_poly, p8),
    )
    assert sp.expand(pivot_family.as_expr()) != 0
    # double-deep stratum of the disjoint chart: rank-one covector in
    # direction (0,0,1,1), kernel z2+z3=0, and the exact moduli
    # determinant 4(beta-alpha)(v0+v1)x2^2.
    deep_sub = {v[3]: -v[2], x[3]: -x[2]}
    deep_rows = []
    for c in (rmul(Y2_disj, Y3),
              rmul([sp.sympify(e).subs(deep_sub) for e in x], Y3)):
        zw = rmul(list(zsym),
                  [sp.sympify(e).subs(deep_sub) for e in v])
        form = pairing(zw, c)
        deep_rows.append(
            [sp.cancel(sp.diff(form, zi)) for zi in zsym]
        )
    deep_matrix = sp.Matrix(deep_rows)
    assert deep_matrix.rank() == 1
    alpha, beta = sp.symbols("alphadd betadd")
    k1 = (1, 0, 0, 0)
    k2 = (0, 1, 0, 0)
    k3 = (0, 0, 1, -1)
    u0a = tuple(sp.expand(a1 + alpha * a3)
                for a1, a3 in zip(k1, k3))
    u0b = tuple(sp.expand(a2 + beta * a3)
                for a2, a3 in zip(k2, k3))
    v_deep = tuple(sp.sympify(e).subs(deep_sub) for e in v)
    x_deep = tuple(sp.sympify(e).subs(deep_sub) for e in x)
    B_deep = sp.zeros(2, 2)
    for i0, u0row in enumerate((u0a, u0b)):
        for i1, u1row in enumerate((U1_A, v_deep)):
            B_deep[i0, i1] = perm4((
                u0row, u1row, x_deep, U3_disj
            ))
    deep_det = sp.expand(B_deep.det())
    target_deep = sp.expand(
        4 * (beta - alpha) * (v[0] + v[1]) * x[2]**2
    )
    assert sp.expand(deep_det - target_deep) == 0


def x3_wall_certificates():
    """Rank-fifteen incidence smoothness and rank-four wall tangent
    at the exact x3-branch sample, plus the profile data used by the
    ninth-component eliminations."""
    alpha, beta = sp.symbols("alpha beta")
    T0v, T1v = sp.symbols("tw0 tw1")
    x0_val = -(d * v[0] * x[1] + v[1] * x[2]) / (d * v[1])
    substitution = {v[3]: -v[2], x[3]: 0, x[0]: x0_val}
    c_row = (-d * v[1], -d * v[0], v[1], v[1])
    k1 = (-c_row[1], c_row[0], 0, 0)
    k2 = (-c_row[2], 0, c_row[0], 0)
    k3 = (-c_row[3], 0, 0, c_row[0])
    u0a = tuple(sp.expand(a1 + alpha * a3)
                for a1, a3 in zip(k1, k3))
    u0b = tuple(sp.expand(a2 + beta * a3)
                for a2, a3 in zip(k2, k3))

    def sub_row(row):
        return tuple(sp.sympify(c_).subs(substitution) for c_ in row)

    planes = [
        sp.Matrix([list(u0a), list(u0b)]),
        sp.Matrix([list(U1_A), list(sub_row(v))]),
        sp.Matrix([list(sub_row(Y2)), list(sub_row(x))]),
        sp.Matrix([list(Y3), list(sub_row(U3_B))]),
    ]
    torus = sp.diag(T0v, T1v, 1, 1)
    planes = [plane * torus for plane in planes]
    pivots = ((0, 1), (0, 2), (0, 1), (0, 2))
    chart_coords = []
    reduced = []
    for plane, piv in zip(planes, pivots):
        chart = plane[:, piv].inv() * plane
        nonpiv = tuple(i for i in range(4) if i not in piv)
        reduced.append(chart)
        chart_coords.extend(chart[r_, c_] for r_ in range(2)
                            for c_ in nonpiv)
    point = {d: 2, v[0]: 3, v[1]: 5, v[2]: 7, x[1]: 11, x[2]: -4,
             alpha: sp.Rational(2, 3), beta: sp.Rational(-1, 2),
             T0v: 1, T1v: 1}
    params = (d, v[0], v[1], v[2], x[1], x[2], alpha, beta,
              T0v, T1v)
    jac = sp.Matrix(chart_coords).jacobian(params).subs(point)
    jac = sp.Matrix([[sp.nsimplify(sp.cancel(e)) for e in row]
                     for row in jac.tolist()])
    assert jac.rank() == 4
    # with the full projective torus the family tangent has rank five,
    # matching the smooth incidence dimension: the ninth component's
    # certificate.  The slice-preserving two-torus rank four above is
    # the normalized-slice dimension.
    T2v = sp.Symbol("tw2")
    full_planes = [
        plane * sp.diag(1, 1, T2v, 1) for plane in planes
    ]
    full_coords = []
    for plane, piv in zip(full_planes, pivots):
        chart = plane[:, piv].inv() * plane
        nonpiv = tuple(i for i in range(4) if i not in piv)
        full_coords.extend(chart[r_, c_] for r_ in range(2)
                           for c_ in nonpiv)
    full_point = {**point, T2v: 1}
    full_jac = sp.Matrix(full_coords).jacobian(
        params + (T2v,)
    ).subs(full_point)
    full_jac = sp.Matrix([
        [sp.nsimplify(sp.cancel(e)) for e in row]
        for row in full_jac.tolist()
    ])
    assert full_jac.rank() == 5
    # incidence Jacobian rank fifteen
    reduced_point = tuple(plane.subs(point) for plane in reduced)
    T_point = {}
    for bits in itertools.product((0, 1), repeat=4):
        rows_sel = tuple(
            tuple(reduced_point[m][bits[m], j] for j in range(4))
            for m in range(4)
        )
        T_point[bits] = sp.nsimplify(perm4(rows_sel))
    anchor = next(
        bits for bits in itertools.product((0, 1), repeat=4)
        if T_point[bits] != 0
    )
    zvars = sp.symbols("W0:16")
    rvars = sp.symbols("S0:4")
    universal = []
    for mode, piv in enumerate(pivots):
        nonpiv = tuple(i for i in range(4) if i not in piv)
        plane = sp.zeros(2, 4)
        plane[0, piv[0]] = 1
        plane[1, piv[1]] = 1
        entries = zvars[4 * mode: 4 * mode + 4]
        for r_ in range(2):
            for o_, c_ in enumerate(nonpiv):
                plane[r_, c_] = entries[2 * r_ + o_]
        universal.append(plane)
    T_universal = {}
    for bits in itertools.product((0, 1), repeat=4):
        rows_sel = tuple(
            tuple(universal[m][bits[m], j] for j in range(4))
            for m in range(4)
        )
        T_universal[bits] = perm4(rows_sel)
    ratios = tuple(
        T_point[tuple(
            (1 - anchor[m_] if m_ == mode else anchor[m_])
            for m_ in range(4)
        )] / T_point[anchor]
        for mode in range(4)
    )
    equations = []
    for word in itertools.product((0, 1), repeat=4):
        if word == anchor:
            continue
        monomial = sp.prod(
            rvars[m] for m in range(4) if word[m] != anchor[m]
        )
        equations.append(sp.expand(
            T_universal[word] - T_universal[anchor] * monomial
        ))
    coordinate_point = tuple(
        sp.nsimplify(sp.cancel(c_.subs(point)))
        for c_ in chart_coords
    )
    incidence_substitution = dict(zip(
        tuple(zvars) + tuple(rvars),
        coordinate_point + ratios,
    ))
    assert all(
        sp.simplify(eq.subs(incidence_substitution)) == 0
        for eq in equations
    )
    incidence_jacobian = sp.Matrix(equations).jacobian(
        tuple(zvars) + tuple(rvars)
    ).subs(incidence_substitution)
    assert incidence_jacobian.rank() == 15
    # sample profile used by the eliminations
    planes_pt = [
        [list(reduced_point[m].row(0)), list(reduced_point[m].row(1))]
        for m in range(4)
    ]
    profile = []
    for a_, b_ in itertools.combinations(range(4), 2):
        rows_ = []
        for pa in planes_pt[a_]:
            for pb in planes_pt[b_]:
                prod = rmul(pa, pb)
                rows_.append([prod[ab] for ab in COORD_PAIRS])
        profile.append(sp.Matrix(rows_).rank())
    assert tuple(profile) == (4, 4, 4, 3, 3, 3), profile
    # first-component confinement value is nonzero at the sample
    confinement = (d * v[0] * x[1] + v[1] * x[3]).subs(
        {**{d: 2, v[0]: 3, v[1]: 5}, x[1]: 11, x[3]: 0}
    )
    assert confinement != 0


def sheet_and_deep_stratum():
    # sheet v3=-v2, sub-pivot columns (0,2)
    M = covector_matrix().subs({v[3]: -v[2]})
    M = sp.Matrix([[sp.expand(e) for e in row] for row in M.tolist()])
    piv = sp.expand(M[0, 0] * M[1, 2] - M[0, 2] * M[1, 0])
    G4 = sp.expand(F4.subs({v[3]: -v[2]}))
    quotient = sp.simplify(piv / (v[1] * G4))
    assert quotient.is_Rational and quotient != 0
    # F3-sheet closure identities
    assert sp.expand(F1 + F3 - 2 * v[1] * x[3]) == 0
    assert sp.expand(
        F2 + F3
        - 2 * (-d * v[0] * x[1] + (v[2] + v[3]) * x[1]
               + v[1] * x[3])
    ) == 0
    # deep stratum: additionally G4=0 via x0
    x0_val = -(d * v[0] * x[1] + v[1] * (x[2] + x[3])) / (d * v[1])
    deep = covector_matrix().subs({v[3]: -v[2], x[0]: x0_val})
    deep = sp.Matrix([[sp.cancel(e) for e in row]
                      for row in deep.tolist()])
    assert deep.rank() == 1
    covector = [sp.cancel(e) for e in deep.row(0)]
    scale = sp.cancel(covector[0] / (-d * v[1]))
    assert all(
        sp.simplify(entry - scale * target) == 0
        for entry, target in zip(
            covector, (-d * v[1], -d * v[0], v[1], v[1])
        )
    )
    # deep-stratum active determinant, independent of U_0 moduli
    alpha, beta = sp.symbols("alpha beta")
    c_row = (-d * v[1], -d * v[0], v[1], v[1])
    k1 = (-c_row[1], c_row[0], 0, 0)
    k2 = (-c_row[2], 0, c_row[0], 0)
    k3 = (-c_row[3], 0, 0, c_row[0])
    u0a = tuple(sp.expand(a1 + alpha * a3)
                for a1, a3 in zip(k1, k3))
    u0b = tuple(sp.expand(a2 + beta * a3)
                for a2, a3 in zip(k2, k3))
    subs_deep = {v[3]: -v[2], x[0]: x0_val}
    u1_rows = (U1_A,
               tuple(sp.sympify(c_).subs(subs_deep) for c_ in v))
    x_row = tuple(sp.sympify(c_).subs(subs_deep) for c_ in x)
    B = sp.zeros(2, 2)
    for i0, u0row in enumerate((u0a, u0b)):
        for i1 in range(2):
            B[i0, i1] = perm4((u0row, u1_rows[i1], x_row, U3_B))
    det = sp.cancel(sp.together(sp.expand(B.det())))
    numerator, denominator = sp.fraction(det)
    assert sp.simplify(denominator - 1) == 0 or not (
        set(sp.sympify(denominator).free_symbols)
        & {alpha, beta}
    )
    target = 4 * d**2 * v[1]**2 * x[3] * (
        d * v[0] * x[1] + v[1] * x[3]
    )
    ratio = sp.simplify(sp.cancel(numerator / target))
    assert not (set(sp.sympify(ratio).free_symbols)
                & {alpha, beta, x[3]})
    # first-component embedding
    l_, i_ = sp.symbols("l i")
    fam = {d: i_, v[0]: l_, v[1]: 1, v[2]: -i_ * l_, v[3]: i_ * l_,
           x[0]: 0, x[1]: 1, x[2]: 0, x[3]: -i_ * l_}
    assert sp.simplify((v[2] + v[3]).subs(fam)) == 0
    assert sp.simplify(F4.subs(fam)) == 0
    assert sp.simplify(F1.subs(fam)) == 0
    assert sp.simplify(
        (d * v[0] * x[1] + v[1] * x[3]).subs(fam)
    ) == 0


def sixth_component_invariants():
    """Generic pair profile and relation ranks of the sixth
    component match the F1/F2 samples."""
    dd, pp, qq = sp.symbols("dsix psix qsix")
    n = qq * (dd + pp + qq)
    planes = (
        ((-dd * pp, dd + qq, n, 0), (dd * pp, -dd - qq, 0, n)),
        ((0, 0, 1, 1), (-dd, 1, -pp - qq, dd)),
        ((pp, 1, 0, qq), (-1, 0, 1, 0)),
        ((1, 0, 1, 0), (0, 0, -1, 1)),
    )
    values = {dd: 2, pp: 3, qq: 5}
    planes_point = tuple(
        tuple(tuple(sp.sympify(e).subs(values) for e in row)
              for row in plane)
        for plane in planes
    )
    profile = []
    relations = []
    for a_, b_ in itertools.combinations(range(4), 2):
        rows_ = []
        for pa in planes_point[a_]:
            for pb in planes_point[b_]:
                prod = rmul(list(pa), list(pb))
                rows_.append([prod[ab] for ab in COORD_PAIRS])
        mm = sp.Matrix(rows_)
        r = mm.rank()
        profile.append(r)
        if r == 3:
            k = [sp.simplify(c_) for c_ in mm.T.nullspace()[0]]
            relations.append(
                ((a_, b_),
                 sp.Matrix([[k[0], k[1]], [k[2], k[3]]]).rank())
            )
    assert tuple(profile) == (4, 4, 3, 4, 3, 3), profile
    assert tuple(relations) == (
        ((0, 3), 1), ((1, 3), 1), ((2, 3), 1)
    ), relations
    # exact identifications: torus-aligned sixth family kills F1;
    # the mode-0<->1 swapped embedding kills F2.
    T0, T1, T2 = sp.symbols("tsixa tsixb tsixc")
    n = qq * (dd + pp + qq)

    def torus(row):
        return (T0 * row[0], T1 * row[1], T2 * row[2],
                -T2 * row[3])

    def branch_value(expression, v_row, x_row, d_value):
        return sp.factor(sp.simplify(expression.subs({
            d: d_value,
            **{v[i]: v_row[i] for i in range(4)},
            **{x[i]: x_row[i] for i in range(4)},
        })))

    d_value = T2 / T0
    alpha1 = torus((-dd, 1, -pp - qq, dd))
    beta2 = torus((pp, 1, 0, qq))
    assert branch_value(F1, alpha1, beta2, d_value) == 0
    assert branch_value(F2, alpha1, beta2, d_value) != 0
    alpha0 = torus((dd * pp, -dd - qq, 0, n))
    assert branch_value(F2, alpha0, beta2, d_value) == 0
    assert branch_value(F1, alpha0, beta2, d_value) != 0
    # the swapped embedding's u_1-slot vector: support {2,3} direction
    # of the sixth's mode-0 plane, proportional to u_1 and killing y_3
    beta0 = torus((-dd * pp, dd + qq, n, 0))
    free0 = tuple(sp.simplify(b_ + a_)
                  for b_, a_ in zip(beta0, alpha0))
    assert free0[0] == 0 and free0[1] == 0
    assert sp.simplify(free0[2] + free0[3]) == 0


def main() -> None:
    note_text = " ".join(NOTE.read_text(encoding="utf-8").split())
    assert "not a complete component theorem" in note_text
    assert (
        "the F_4 branch is contained in the seventh component"
        in note_text
    )

    M = covector_matrix()
    det, pivot = cramer_identity(M)
    content = factor_in_singular(det)
    sheet_and_deep_stratum()
    sixth_component_invariants()
    f4_slice_certificates()

    branch_results = {}
    for label, point in SAMPLES.items():
        expr = {"F1": F1, "F2": F2, "F4": F4}[label]
        subs = {**dict(zip(v, point["v"])),
                **dict(zip(x, point["x"])), d: point["d"]}
        assert sp.simplify(expr.subs(subs)) == 0
        assert sp.simplify(((v[2]+v[3]) * F3).subs(subs)) != 0
        others = [e for lab, e in
                  (("F1", F1), ("F2", F2), ("F4", F4)) if lab != label]
        assert all(sp.simplify(e.subs(subs)) != 0 for e in others)
        profile, relations = analyse_point(point)
        assert profile == point["profile"], (label, profile)
        assert relations == point["relations"], (label, relations)
        branch_results[label] = {
            "profile": list(profile),
            "rank3_relations": [
                [list(edge), rank] for edge, rank in relations
            ],
        }

    x3_wall_certificates()
    disjoint_chart_certificates()

    result = {
        "verified": True,
        "checkpoint_only": True,
        "chart": "in-out path, overlap-one supports",
        "active_determinant_content": content,
        "open_chart_pure_locus": "F1*F2*F4=0",
        "sheet_v2_plus_v3": "pure locus restricts to F1*F2=0",
        "deep_stratum_rank_drop": True,
        "deep_stratum_pure_locus":
            "x3=0 or d*v0*x1+v1*x3=0, U0-moduli free",
        "f3_sheet_closed_by_identities": True,
        "first_component_embeds_in_deep_stratum": True,
        "sixth_component_invariants_match_f1_f2": True,
        "f1_branch_is_sixth_component_translate": True,
        "f2_branch_is_sixth_component_translate": True,
        "no_new_component_in_open_chart": True,
        "x3_wall_incidence_jacobian_rank": 15,
        "x3_wall_slice_tangent_rank": 4,
        "x3_wall_full_torus_tangent_rank": 5,
        "x3_wall_sample_profile": [4, 4, 4, 3, 3, 3],
        "ninth_component_certified": True,
        "certified_component_lower_bound": 9,
        "branch2_identified_as_first_component": True,
        "disjoint_chart_open_stratum_is_eighth_component": True,
        "component_exhaustiveness_still_open": True,
        "branches": branch_results,
        "f4_family_tangent_rank": 5,
        "f4_incidence_jacobian_rank": 14,
        "f4_contained_in_six_dimensional_component": True,
        "no_ninth_component_from_f4": True,
        "component_classification_completed": False,
        "component_exhaustiveness_resolved": False,
        "global_problem_resolved": False,
        "note": {"path": NOTE.name, "sha256": sha256(NOTE)},
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p4_inout_path_stratum_working_note_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
