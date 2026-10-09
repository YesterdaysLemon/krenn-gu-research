#!/usr/bin/env python3
"""Replay PERMANENT_PLANE_RESTRICTION_HYPERDETERMINANT_THEOREM.md (exact).

Primary verifier of the displayed identities and of the finite exact
linear-algebra facts quoted in the theorem document.  The proofs are the hand
arguments in the document; this script checks their algebraic content.  It is
not an independent audit.

Notation: Y_t in Z[y]^{3x2} (t = 0, 1, 2), A_ijk = perm(Y_0[:,i], Y_1[:,j],
Y_2[:,k]) the 2x2x2 cube tensor, l_t = Y_t[:,0] x Y_t[:,1] the Pluecker
(normal) vector of the column plane of Y_t, P_s = l_0[s0] l_1[s1] l_2[s2].

Checks:
  [1] Theorem 1: Cayley's hyperdeterminant Det(A) = F(l_0, l_1, l_2) with the
      explicit 21-term F; F = det(L)^2 - 8(e2(P_even) + e2(P_odd)); F = 4 x the
      bordered discriminant; absolute irreducibility ingredients; special values.
  [2] Slice covariant: det(Y_1^T B_v Y_2) = l_1^T adj(B_v) l_2 and
      adj(B_v) = v v^T - 2 diag(v)^2; the slice determinant of the cube
      contracted with x in direction 0 equals q_0(Y_0 x).
  [3] Theorem 2(a): the polarization identity, for all 27 row triples r,
      sum_{ijk} (-1)^{i+j+k} Y_0[r0,1-i] Y_1[r1,1-j] Y_2[r2,1-k] A_ijk
          = -perm(l_0 x e_r0, l_1 x e_r1, l_2 x e_r2).
  [4] Theorem 2(b): the 27 forms span a space J_3 of rank 22 over Q and over
      F_p (p = 3, 5, 7), rank 16 over F_2; its annihilator is
      S = span{e_a^{x3}, eps_+, eps_-}; Smith invariants of the 27 x 27 matrix.
  [5] Theorem 2(c): J_3 is the whole trilinear-Pluecker part of the cube ideal
      in multidegree (1,...,1) (exact integer ranks 208 and 213).
  [6] Corollary 3: rank-one tensors in S over F_3 and F_5 (brute force over
      projective points) are exactly the common-axis ones.
  [7] Corollary 4: P_s not in I; P_s^2 = P_s (P_s - P_t) + P_s P_t with
      P_s P_t divisible by a two-equal monomial; the all-equal monomial is
      nonzero at an isotropic point; F == sum_s P_s^2 mod the two-equal
      monomials.

Run:
    python claims/arbitrary-order/verify_permanent_plane_restriction_hyperdeterminant_theorem.py
"""

from __future__ import annotations

import itertools
import random
import sys
from collections import defaultdict

import flint
import sympy as sp

FAIL: list[str] = []


def check(cond, msg):
    print(("  PASS  " if cond else "  FAIL  ") + msg)
    if not cond:
        FAIL.append(msg)


PERMS = list(itertools.permutations(range(3)))
SIGN = {p: (1 if sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3)) % 2 == 0 else -1)
        for p in PERMS}

Y = [sp.Matrix(3, 2, lambda a, i, t=t: sp.Symbol(f"y{t}_{a}{i}")) for t in range(3)]
YSYMS = [s for t in range(3) for s in Y[t]]
LS = [[sp.Symbol(f"l{t}{a + 1}") for a in range(3)] for t in range(3)]


def perm3(x, y, z):
    return sp.Add(*[x[p[0]] * y[p[1]] * z[p[2]] for p in PERMS])


def cross(u, v):
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]


def e(a):
    return [1 if b == a else 0 for b in range(3)]


A = {(i, j, k): sp.expand(perm3(Y[0][:, i], Y[1][:, j], Y[2][:, k]))
     for i, j, k in itertools.product(range(2), repeat=3)}
LY = [cross(list(Y[t][:, 0]), list(Y[t][:, 1])) for t in range(3)]
LSUB = {LS[t][a]: LY[t][a] for t in range(3) for a in range(3)}


def cayley(a):
    a000, a001, a010, a011 = a[0, 0, 0], a[0, 0, 1], a[0, 1, 0], a[0, 1, 1]
    a100, a101, a110, a111 = a[1, 0, 0], a[1, 0, 1], a[1, 1, 0], a[1, 1, 1]
    return (a000**2 * a111**2 + a001**2 * a110**2 + a010**2 * a101**2 + a100**2 * a011**2
            - 2 * (a000 * a001 * a110 * a111 + a000 * a010 * a101 * a111
                   + a000 * a100 * a011 * a111 + a001 * a010 * a101 * a110
                   + a001 * a100 * a011 * a110 + a010 * a100 * a011 * a101)
            + 4 * (a000 * a011 * a101 * a110 + a001 * a010 * a100 * a111))


F_TEXT = ("l01**2*l12**2*l23**2 - 2*l01**2*l12*l13*l22*l23 + l01**2*l13**2*l22**2"
          " - 2*l01*l02*l11*l12*l23**2 - 6*l01*l02*l11*l13*l22*l23 - 6*l01*l02*l12*l13*l21*l23"
          " - 2*l01*l02*l13**2*l21*l22 - 6*l01*l03*l11*l12*l22*l23 - 2*l01*l03*l11*l13*l22**2"
          " - 2*l01*l03*l12**2*l21*l23 - 6*l01*l03*l12*l13*l21*l22 + l02**2*l11**2*l23**2"
          " - 2*l02**2*l11*l13*l21*l23 + l02**2*l13**2*l21**2 - 2*l02*l03*l11**2*l22*l23"
          " - 6*l02*l03*l11*l12*l21*l23 - 6*l02*l03*l11*l13*l21*l22 - 2*l02*l03*l12*l13*l21**2"
          " + l03**2*l11**2*l22**2 - 2*l03**2*l11*l12*l21*l22 + l03**2*l12**2*l21**2")
F = sp.sympify(F_TEXT, locals={str(s): s for row in LS for s in row})
P = {p: LS[0][p[0]] * LS[1][p[1]] * LS[2][p[2]] for p in PERMS}


# --------------------------------------------------------------------- [1]
def check_hyperdeterminant():
    print("[1] Theorem 1: Det(A) = F(l_0, l_1, l_2)")
    check(len(sp.Add.make_args(F)) == 21, "F has 21 terms")
    det_A = sp.expand(cayley(A))
    check(sp.expand(det_A - F.subs(LSUB)) == 0, "Det(A(Y)) == F(l(Y)) identically in the 18 entries")
    ev = [p for p in PERMS if SIGN[p] == 1]
    od = [p for p in PERMS if SIGN[p] == -1]
    e2 = lambda xs: sum(P[a] * P[b] for a, b in itertools.combinations(xs, 2))
    L = sp.Matrix(3, 3, lambda t, a: LS[t][a])
    check(sp.expand(F - (L.det() ** 2 - 8 * (e2(ev) + e2(od)))) == 0,
          "F = det(L)^2 - 8 (e2(P_even) + e2(P_odd)), L = rows l_0, l_1, l_2")
    l0, l1, l2 = (sp.Matrix(LS[t]) for t in range(3))
    Q12 = (l1 * l2.T + l2 * l1.T) / 2 - 2 * sp.diag(*[LS[1][a] * LS[2][a] for a in range(3)])
    bord = sp.Matrix(sp.BlockMatrix([[Q12, l0], [l0.T, sp.zeros(1)]]))
    check(sp.expand(F - 4 * bord.det()) == 0, "F = 4 det [[Q_12, l_0], [l_0^T, 0]] (bordered discriminant)")
    # symmetry in the three planes
    sw = {LS[0][a]: LS[1][a] for a in range(3)} | {LS[1][a]: LS[0][a] for a in range(3)}
    sw2 = {LS[1][a]: LS[2][a] for a in range(3)} | {LS[2][a]: LS[1][a] for a in range(3)}
    check(sp.expand(F.subs(sw, simultaneous=True) - F) == 0
          and sp.expand(F.subs(sw2, simultaneous=True) - F) == 0, "F is symmetric in l_0, l_1, l_2")
    # absolute irreducibility ingredients
    H = sp.hessian(F, LS[0])
    sub = {LS[1][0]: 2, LS[1][1]: -3, LS[1][2]: 5, LS[2][0]: 7, LS[2][1]: 1, LS[2][2]: -4}
    check(H.subs(sub).rank() == 3, "Hessian of F in l_0 has rank 3 at (l_1, l_2) = ((2,-3,5), (7,1,-4))")
    g = 0
    for entry in H:
        g = sp.gcd(g, sp.expand(entry))
    check(g.free_symbols == set() and g != 0, f"gcd of the l_0-Hessian entries is a constant ({g})")
    lsub = {LS[1][a]: LS[0][a] for a in range(3)}
    F_lll = sp.factor(F.subs(lsub).subs({LS[2][a]: LS[0][a] for a in range(3)}))
    check(sp.expand(F_lll + 48 * (LS[0][0] * LS[0][1] * LS[0][2]) ** 2) == 0, "F(l,l,l) = -48 (l1 l2 l3)^2")
    m = LS[2]
    F_llm = sp.expand(F.subs(lsub))
    check(sp.expand(F_llm + 8 * LS[0][0] * LS[0][1] * LS[0][2] * perm3(LS[0], m, m)) == 0,
          "F(l,l,m) = -8 (l1 l2 l3) perm(l, m, m)")
    pt = {LS[t][a]: (1 if a == t else 0) for t in range(3) for a in range(3)}
    check(F.subs(pt) == 1, "F(e_1, e_2, e_3) = 1 (distinct coordinate planes: nondegenerate)")
    pt = {LS[t][a]: (1 if a == 0 else 0) for t in range(3) for a in range(3)}
    check(F.subs(pt) == 0, "F(e_1, e_1, e_1) = 0")


# --------------------------------------------------------------------- [2]
def check_slice_covariant():
    print("[2] slice covariant q_0(v) = l_1^T adj(B_v) l_2 = (l_1.v)(l_2.v) - 2 sum_u l_1u l_2u v_u^2")
    v = sp.symbols("v1:4")
    Bv = sp.Matrix([[0, v[2], v[1]], [v[2], 0, v[0]], [v[1], v[0], 0]])
    target = sp.Matrix(v) * sp.Matrix(v).T - 2 * sp.diag(*[x ** 2 for x in v])
    check(sp.expand(Bv.adjugate() - target) == sp.zeros(3), "adj(B_v) = v v^T - 2 diag(v)^2")
    lhs = (Y[1].T * Bv * Y[2]).det()
    rhs = (sp.Matrix(LY[1]).T * Bv.adjugate() * sp.Matrix(LY[2]))[0]
    check(sp.expand(lhs - rhs) == 0, "det(Y_1^T B_v Y_2) = l_1^T adj(B_v) l_2 (Cauchy-Binet)")
    x0, x1 = sp.symbols("x0 x1")
    slice_mat = sp.Matrix(2, 2, lambda j, k: x0 * A[0, j, k] + x1 * A[1, j, k])
    vv = list(Y[0] * sp.Matrix([x0, x1]))
    q0 = (sp.Matrix(LY[1]).T * (sp.Matrix(vv) * sp.Matrix(vv).T - 2 * sp.diag(*[c ** 2 for c in vv]))
          * sp.Matrix(LY[2]))[0]
    check(sp.expand(slice_mat.det() - q0) == 0, "det(x0 A_0.. + x1 A_1..) = q_0(Y_0 x)")


# --------------------------------------------------------------------- [3]
def plucker_form(r):
    """perm(l_0 x e_r0, l_1 x e_r1, l_2 x e_r2) in the symbols LS."""
    return sp.expand(perm3(*[cross(LS[t], e(r[t])) for t in range(3)]))


def check_polarization():
    print("[3] Theorem 2(a): polarization identity for all 27 row triples")
    ok = True
    for r in itertools.product(range(3), repeat=3):
        lhs = sp.Add(*[(-1) ** (i + j + k) * Y[0][r[0], 1 - i] * Y[1][r[1], 1 - j] * Y[2][r[2], 1 - k] * A[i, j, k]
                       for i, j, k in itertools.product(range(2), repeat=3)])
        if sp.expand(lhs + plucker_form(r).subs(LSUB)) != 0:
            ok = False
    check(ok, "sum (-1)^{i+j+k} Y_0[r0,1-i] Y_1[r1,1-j] Y_2[r2,1-k] A_ijk = -perm(l_0 x e_r0, ...) for all r")
    zero = [r for r in itertools.product(range(3), repeat=3) if plucker_form(r) == 0]
    check(sorted(zero) == [(0, 0, 0), (1, 1, 1), (2, 2, 2)], "the form vanishes exactly for r = (a,a,a)")
    f = plucker_form((0, 1, 2))
    check(sp.expand(f - (P[(2, 0, 1)] - P[(1, 2, 0)])) == 0,
          "r = (1,2,3): form = P_(3,1,2) - P_(2,3,1) (difference of two even permutation monomials)")
    f = plucker_form((0, 0, 1))
    check(sp.expand(f - (LS[0][1] * LS[1][2] * LS[2][2] + LS[0][2] * LS[1][1] * LS[2][2])) == 0,
          "r = (1,1,2): form = l_0[2] l_1[3] l_2[3] + l_0[3] l_1[2] l_2[3]")


# --------------------------------------------------------------------- [4]
MONO27 = list(itertools.product(range(3), repeat=3))


def coeff_vector(f):
    poly = sp.Poly(f, *[s for row in LS for s in row])
    out = []
    for (a, b, c) in MONO27:
        expo = [0] * 9
        expo[a] += 1
        expo[3 + b] += 1
        expo[6 + c] += 1
        out.append(int(poly.coeff_monomial(tuple(expo))))
    return out


def form_matrix():
    return [coeff_vector(plucker_form(r)) for r in MONO27]


def s_basis():
    vecs = []
    for a in range(3):
        vecs.append([1 if m == (a, a, a) else 0 for m in MONO27])
    vecs.append([1 if (m in SIGN and SIGN[m] == 1) else 0 for m in MONO27])
    vecs.append([1 if (m in SIGN and SIGN[m] == -1) else 0 for m in MONO27])
    return vecs


def check_span():
    print("[4] Theorem 2(b): span J_3 of the 27 forms and its annihilator S")
    M = form_matrix()
    MZ = flint.fmpz_mat(M)
    check(MZ.rank() == 22, "rank over Q = 22")
    for p, want in [(2, 16), (3, 22), (5, 22), (7, 22)]:
        Mp = flint.nmod_mat(27, 27, [x % p for row in M for x in row], p)
        check(Mp.rank() == want, f"rank over F_{p} = {want}")
    S = s_basis()
    ann = all(sum(M[i][k] * s[k] for k in range(27)) == 0 for i in range(27) for s in S)
    check(ann, "every form annihilates e_a^{x3} (a = 1,2,3), eps_+ and eps_- (S is in the kernel)")
    check(flint.fmpz_mat(S).rank() == 5, "the five tensors spanning S are independent (so ker = S over Q)")
    from sympy.matrices.normalforms import smith_normal_form
    snf = smith_normal_form(sp.Matrix(M), domain=sp.ZZ)
    diag = sorted(abs(int(snf[i, i])) for i in range(27))
    check(diag == [0] * 5 + [1] * 16 + [2] * 6, "Smith invariants: 16 ones, 6 twos, 5 zeros")


# --------------------------------------------------------------------- [5]
VARS = [(t, a, i) for t in range(3) for a in range(3) for i in range(2)]
VID = {v: k for k, v in enumerate(VARS)}


def _mono(*vs):
    out = [0] * 18
    for v in vs:
        out[VID[v]] += 1
    return tuple(out)


def _pmul(p, q):
    r = defaultdict(int)
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            r[tuple(x + y for x, y in zip(m1, m2))] += c1 * c2
    return {m: c for m, c in r.items() if c}


def check_completeness():
    print("[5] Theorem 2(c): J_3 is the whole trilinear-Pluecker part of I in degree (1,...,1)")
    Ad = {}
    for i, j, k in itertools.product(range(2), repeat=3):
        p = defaultdict(int)
        for pi in PERMS:
            p[_mono((0, pi[0], i), (1, pi[1], j), (2, pi[2], k))] += 1
        Ad[i, j, k] = dict(p)
    rows = []
    for (i, j, k), p in Ad.items():
        for a, b, c in itertools.product(range(3), repeat=3):
            rows.append(_pmul(p, {_mono((0, a, 1 - i), (1, b, 1 - j), (2, c, 1 - k)): 1}))
    Lp = []
    for t in range(3):
        row = []
        for a in range(3):
            b, c = (a + 1) % 3, (a + 2) % 3
            row.append({_mono((t, b, 0), (t, c, 1)): 1, _mono((t, c, 0), (t, b, 1)): -1})
        Lp.append(row)
    plu = [_pmul(_pmul(Lp[0][a], Lp[1][b]), Lp[2][c]) for a, b, c in MONO27]
    monos = sorted({m for p in rows + plu for m in p})
    col = {m: k for k, m in enumerate(monos)}

    def mat(polys):
        M = flint.fmpz_mat(len(polys), len(monos))
        for r, p in enumerate(polys):
            for m, c in p.items():
                M[r, col[m]] = c
        return M
    rI = mat(rows).rank()
    rIP = mat(rows + plu).rank()
    check(len(rows) == 216 and rI == 208, f"216 products (trilinear multipliers x A_ijk) have rank {rI} = 208")
    check(rIP == 213, f"rank with the 27 Pluecker monomials adjoined = {rIP} = 213")
    check(rI + 27 - rIP == 22, "dim (I_(1^6) intersect Pluecker trilinear forms) = 22 = dim J_3")

    def rank_mod(polys, p):
        Mp = flint.nmod_mat(len(polys), len(monos), p)
        for r, q in enumerate(polys):
            for m, c in q.items():
                Mp[r, col[m]] = c % p
        return Mp.rank()
    for p, want in [(2, 17), (3, 22)]:
        d = rank_mod(rows, p) + 27 - rank_mod(rows + plu, p)
        check(d == want, f"over F_{p} the trilinear-Pluecker part of I_(1^6) has dimension {d} = {want}")


# --------------------------------------------------------------------- [6]
def check_rank_one_in_S():
    print("[6] Corollary 3: rank-one tensors l_0 x l_1 x l_2 annihilated by J_3 (finite fields)")
    M = form_matrix()
    for p in (3, 5):
        pts = []
        for v in itertools.product(range(p), repeat=3):
            if any(v):
                first = next(x for x in v if x)
                if first == 1:
                    pts.append(v)
        bad = []
        for l0 in pts:
            for l1 in pts:
                for l2 in pts:
                    X = [l0[a] * l1[b] * l2[c] % p for a, b, c in MONO27]
                    if all(sum(row[k] * X[k] for k in range(27)) % p == 0 for row in M):
                        common = [a for a in range(3) if all(lt == tuple(1 if b == a else 0 for b in range(3))
                                                               for lt in (l0, l1, l2))]
                        if not common:
                            bad.append((l0, l1, l2))
        check(not bad, f"over F_{p}: every annihilated triple of nonzero l_t is a common coordinate axis")


# --------------------------------------------------------------------- [7]
def two_equal(expo):
    """Does a monomial (exponent dict over LS) contain l_s[a] l_t[a] l_r[b], a != b?"""
    sup = [[a for a in range(3) if expo.get(LS[t][a], 0) > 0] for t in range(3)]
    for s, t in itertools.combinations(range(3), 2):
        r = 3 - s - t
        for a in set(sup[s]) & set(sup[t]):
            if any(b != a for b in sup[r]):
                return True
    return False


def check_degree_facts():
    print("[7] Corollary 4: Nullstellensatz facts for one-coordinate-per-plane monomials")
    M = form_matrix()
    MZ = flint.fmpz_mat(M)
    for target in [(0, 1, 2), (0, 0, 0)]:
        vec = [1 if m == target else 0 for m in MONO27]
        aug = flint.fmpz_mat(M + [vec])
        check(aug.rank() == 23, f"monomial l_0[{target[0]+1}] l_1[{target[1]+1}] l_2[{target[2]+1}] is not in J_3")
    vec = [1 if m == (0, 0, 1) else 0 for m in MONO27]
    check(flint.fmpz_mat(M + [vec]).rank() == 22, "two-equal monomial l_0[1] l_1[1] l_2[2] is in J_3 (Proposition 4)")
    # P_s^2 = P_s (P_s - P_t) + P_s P_t, P_s P_t divisible by a two-equal monomial
    ok = True
    for s in PERMS:
        for t in PERMS:
            if s != t and SIGN[s] == SIGN[t]:
                prod = sp.Poly(P[s] * P[t], *[x for row in LS for x in row]).terms()[0][0]
                ex = {x: prod[k] for k, x in enumerate([x for row in LS for x in row])}
                if not two_equal(ex):
                    ok = False
    check(ok, "P_s P_t (s != t) always contains a two-equal factor, so P_s^2 lies in the ideal (J_3)")
    # all-equal monomial nonzero at an isotropic point (all planes H_1)
    pt = {s: 0 for s in YSYMS}
    for t in range(3):
        pt[Y[t][1, 0]] = 1
        pt[Y[t][2, 1]] = 1
    vals = [A[k].subs(pt) for k in A]
    lv = [[c.subs(pt) for c in LY[t]] for t in range(3)]
    check(all(v == 0 for v in vals) and lv[0][0] * lv[1][0] * lv[2][0] != 0,
          "all planes = H_1: the 8 cube values vanish and l_0[1] l_1[1] l_2[1] != 0 (not in the radical)")
    # F == sum P_s^2 modulo two-equal monomials
    diff = sp.expand(F - sum(P[s] ** 2 for s in PERMS))
    gens = [x for row in LS for x in row]
    ok = True
    for mon, c in sp.Poly(diff, *gens).terms():
        if not two_equal({x: mon[k] for k, x in enumerate(gens)}):
            ok = False
    check(ok, "F - sum_s P_s^2 is a combination of monomials with a two-equal factor (F lies in (J_3))")


def main():
    random.seed(0)
    check_hyperdeterminant()
    check_slice_covariant()
    check_polarization()
    check_span()
    check_completeness()
    check_rank_one_in_S()
    check_degree_facts()
    print()
    if FAIL:
        print(f"FAIL: {len(FAIL)} check(s) failed")
        sys.exit(1)
    print("ALL CHECKS PASS")


if __name__ == "__main__":
    main()
