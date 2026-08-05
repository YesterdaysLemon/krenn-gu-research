#!/usr/bin/env python3
"""The updated census table: THIRTEEN component orbits, with the exact
invariant package of each certified component's sample and the pairwise
separating invariants.

Columns: dimension, pair profile (generic, at the documented sample),
rank sum, has-rank-2-pair-edge, coordinate-plane count, some-triple-span
<= 3 (with which triple), kernel-kernel rank-one relation present.

The thirteen orbits:
  1  first     dim 5  (4,4,4,3,3,3)  sum 21   triangle, one rank-2 relation
  2  dq        dim 5  (4,4,3,4,3,3)  sum 21
  3  L1        dim 5  (4,4,3,4,3,3)  sum 21
  4  L2        dim 5  (4,4,3,4,3,3)  sum 21
  5  L3        dim 5  (4,4,3,4,3,3)  sum 21
  6  sixth     dim 5  (4,4,3,4,3,3)  sum 21
  7  seventh   dim 6  (4,3,2,4,4,3)  sum 20   rank-2 pair edge
  8  eighth    dim 5  (4,4,3,4,3,3)  sum 21
  9  ninth     dim 5  (4,4,4,3,3,3)  sum 21   all-rank-one triangle
 10  tenth     dim 6  (3,3,4,3,4,4)  sum 21   triple-span-3
 11  eleventh  dim 6  (4,4,3,4,3,3)  sum 21   coordinate plane (U3 = Pi)
 12  twelfth   dim 5  (3,3,3,4,3,3)  sum 19   NEW (this sweep)
 13  thirteenth dim 5 (3,3,4,3,3,3)  sum 19   NEW (this sweep)
"""
import itertools, sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))


def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


def is_coordinate_plane(rows, pair):
    comp = tuple(i for i in range(4) if i not in pair)
    off = sp.Matrix([[rows[r][c] for c in comp] for r in range(2)])
    on = sp.Matrix([[rows[r][c] for c in pair] for r in range(2)])
    return off.is_zero_matrix and on.det() != 0


samples = {}
samples["first"] = [[(1, 0, -1, -2), (0, 1, 1, 0)], [(1, 1, 0, 0), (0, 0, 1, 1)],
                    [(0, 1, 0, 1), (-1, 0, 1, 0)], [(1, 0, 1, 0), (0, 0, -1, 1)]]
samples["dq"] = [[(2, -1, -1, -2), (1, -1, 1, 1)], [(1, 0, 0, -1), (1, 1, -1, 1)],
                 [(3, 1, 1, -1), (0, 1, -1, 0)], [(1, 0, 0, 1), (0, 1, 1, 0)]]
samples["L1"] = [[(2, 4, 0, 0), (0, 0, 1, 1)], [(0, 1, -1, 0), (1, 0, 1, 3)],
                 [(1, 0, 4, 2), (0, 1, 0, -1)], [(0, 1, 1, 0), (0, 1, 0, 1)]]
samples["L2"] = [[(2, 0, 4, 0), (0, 0, 1, 1)], [(0, 1, -1, 0), (1, 0, 1, 3)],
                 [(1, 0, 4, 6), (0, 1, 0, -1)], [(0, 1, 1, 0), (0, 1, 0, 1)]]
samples["L3"] = [[(2, 10, -8, 0), (0, 0, 1, 1)], [(0, 1, -1, 0), (1, 0, 1, 2)],
                 [(1, 0, 3, -6), (0, 1, 0, -1)], [(0, 1, 1, 0), (0, 1, 0, 1)]]
dd, pp, qq = 2, 3, 5
n6 = qq*(dd + pp + qq)
samples["sixth"] = [[(-dd*pp, dd + qq, n6, 0), (dd*pp, -dd - qq, 0, n6)],
                    [(0, 0, 1, 1), (-dd, 1, -pp - qq, dd)],
                    [(pp, 1, 0, qq), (-1, 0, 1, 0)], [(1, 0, 1, 0), (0, 0, -1, 1)]]
a7, c7, d7, b7, e7 = 1, 2, 4, 1, 2
h7 = a7 + c7 - d7
samples["seventh"] = [[(1, 0, 0, -1), (0, 0, 1, 1)],
                      [(1, b7, 0, 1 - b7*h7), (0, e7, 1, 1 - e7*h7)],
                      [(1, 0, -1, 0), (0, 1, -a7 - c7, -d7)],
                      [(1, 0, 0, 1), (0, 0, 1, -1)]]
a8, b8, f8, ph8 = sp.Integer(-12), sp.Integer(-10), sp.Rational(3, 4), sp.Rational(-5, 28)
j8 = f8 + b8*ph8**2
kap8 = ph8*(b8*f8 + 1)
eta8 = -(b8*f8 + 1)
samples["eighth"] = [[(0, 0, 1, -1), (a8 + b8, a8 - b8, 0, 2)],
                     [(-a8*f8 + 1, -a8*f8 - 1, f8 + ph8, f8 - ph8), (1, 1, 0, 0)],
                     [(-a8*j8 + eta8, -a8*j8 - eta8, j8 + kap8, j8 - kap8), (1, 1, 0, 0)],
                     [(1, -1, 0, 0), (0, 0, 1, 1)]]
d9, v90, v91, v92, x91, x92 = 2, 3, 5, 7, 11, -4
x90 = sp.Rational(-(d9*v90*x91 + v91*x92), d9*v91)
c9 = (-d9*v91, -d9*v90, v91, v91)
k19, k29, k39 = (-c9[1], c9[0], 0, 0), (-c9[2], 0, c9[0], 0), (-c9[3], 0, 0, c9[0])
al9, be9 = sp.Rational(2, 3), sp.Rational(-1, 2)
samples["ninth"] = [[tuple(k19[j] + al9*k39[j] for j in range(4)),
                     tuple(k29[j] + be9*k39[j] for j in range(4))],
                    [(0, 0, 1, -1), (v90, v91, v92, -v92)],
                    [(1, 0, -d9, 0), (x90, x91, x92, 0)],
                    [(0, 0, 1, 1), (1, 0, d9, 0)]]
samples["tenth"] = [[(1, -1, 0, 0), (0, 1, 2, -10)],
                    [(1, -1, 0, 0), (0, 1, 3, -15)],
                    [(1, 1, 0, 0), (0, 0, 1, 5)],
                    [(1, 7, 0, 0), (0, 11, 1, -5)]]
samples["eleventh"] = [[(3, 7, 0, 0), (0, 0, 1, -3)],
                       [(0, 0, 1, 2), (3, -7, 2, 5)],
                       [(0, 0, 1, -5), (6, -14, -1, 4)],
                       [(0, 0, 1, 1), (0, 0, 1, -1)]]
# the two NEW components (this sweep): F12 (Zb1) and F13 (Za2) samples
samples["twelfth"] = [[(1, 1, 0, 0), (0, 0, -1, 2)],
                      [(1, -1, 0, 0), (0, 1, 3, -1)],
                      [(1, -1, 0, 0), (0, 1, 5, -15)],
                      [(1, 1, 0, 0), (0, 0, 1, 2)]]
samples["thirteenth"] = [[(1, 1, 0, 0), (1, 0, -1, 7)],
                         [(1, -1, 0, 0), (0, 1, 2, -10)],
                         [(1, -1, 0, 0), (0, 1, 3, -15)],
                         [(1, 1, 0, 0), (0, sp.Rational(1, 6), 1, 7)]]
DIMS = {"first": 5, "dq": 5, "L1": 5, "L2": 5, "L3": 5, "sixth": 5,
        "seventh": 6, "eighth": 5, "ninth": 5, "tenth": 6, "eleventh": 6,
        "twelfth": 5, "thirteenth": 5}
EXPECTED = {
    "first": (4, 4, 4, 3, 3, 3), "dq": (4, 4, 3, 4, 3, 3),
    "L1": (4, 4, 3, 4, 3, 3), "L2": (4, 4, 3, 4, 3, 3), "L3": (4, 4, 3, 4, 3, 3),
    "sixth": (4, 4, 3, 4, 3, 3), "seventh": (4, 3, 2, 4, 4, 3),
    "eighth": (4, 4, 3, 4, 3, 3), "ninth": (4, 4, 4, 3, 3, 3),
    "tenth": (3, 3, 4, 3, 4, 4), "eleventh": (4, 4, 3, 4, 3, 3),
    "twelfth": (3, 3, 3, 4, 3, 3), "thirteenth": (3, 3, 4, 3, 3, 3),
}
print(f"{'component':11s} dim profile          sum r2edge #coordpl tri<=3")
rows_out = {}
for name, planes in samples.items():
    planes = [[tuple(sp.nsimplify(c) for c in row) for row in pl] for pl in planes]
    T = {bits: perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4)))
         for bits in itertools.product((0, 1), repeat=4)}
    assert any(val != 0 for val in T.values()), name
    for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
        m = sp.zeros(4, 4)
        for bits in itertools.product((0, 1), repeat=4):
            m[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = T[bits]
        assert m.rank() == 1, (name, left, right)
    prof = []
    for a_, b_ in COORD_PAIRS:
        rows_ = []
        for pa in planes[a_]:
            for pb in planes[b_]:
                prod = rmul(pa, pb)
                rows_.append([prod[ab] for ab in COORD_PAIRS])
        prof.append(sp.Matrix(rows_).rank())
    prof = tuple(prof)
    assert prof == EXPECTED[name], (name, prof)
    cpl = sum(1 for pl in planes
              if any(is_coordinate_plane(pl, pair) for pair in COORD_PAIRS))
    tri3 = [tri for tri in itertools.combinations(range(4), 3)
            if sp.Matrix([list(planes[m][r]) for m in tri for r in range(2)]).rank() <= 3]
    rows_out[name] = (prof, cpl, tri3)
    print(f"{name:11s}  {DIMS[name]}  {str(prof):17s} {sum(prof):2d}   "
          f"{'Y' if 2 in prof else 'n'}      {cpl}      {tri3 if tri3 else '-'}")
print()
print("Separating headlines:")
print(" * twelfth/thirteenth vs all certified fivefolds: rank sum 19 < 21")
print("   everywhere on their closures (s06/s08 minor identities);")
print(" * twelfth vs thirteenth: profile patterns (3,3,3,4,3,3) vs")
print("   (3,3,4,3,3,3) agree as multisets, separated by the two-")
print("   complementary-coordinate-plane incidence invariant (s08);")
print(" * vs the sixfolds: dimension; the tenth also by triple-span,")
print("   the eleventh also by the coordinate-plane invariant (s07).")
print("ALL CHECKS PASSED")
