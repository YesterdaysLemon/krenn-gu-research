#!/usr/bin/env python3
"""Replay the identities of THREE_COLUMN_BILINEAR_GRID_THEOREM.md (exact, SymPy).

This is a primary verifier of displayed polynomial identities and of the
finite linear-algebra facts quoted in the theorem document.  The proofs of
Theorems 1-3 are the hand arguments in the document; this script checks their
algebraic content.  It is not an independent audit.

Checks:
  [1] two-vertex expansion (Theorem 1): generic blocks, every pair {a,b},
      sample words, n = 4, 6 (all words at n = 4) and n = 8 (sample);
  [2] hollow 3x3 determinant det H = 2 h12 h13 h23, and the certificate
      identity det G = det Z * det H * det Y with the explicit cofactor
      multipliers g_ij of Theorem 2, for every (p, q);
  [3] staircase minors are monomials;
  [4] Theorem 3 ingredients: perm(x,y,z) = y^T B_x z, det B_x = 2 x1 x2 x3,
      explicit full-support vectors in non-coordinate planes, coordinate-plane
      triples isotropic, distinct coordinate planes not isotropic;
  [5] Proposition 4 (degree-3 cube): the product of three minors with two
      equal row pairs is in the span of trilinear multiples of the eight cube
      permanents; the all-equal and all-distinct choices are not;
  [6] k-vs-k slice = perm_k (k = 3, 4) and single-entry contraction to perm_3;
  [7] boundary examples: k = 2 plane rigidity fails, k = 4 full-row bound fails.

Run:
    python claims/arbitrary-order/verify_three_column_bilinear_grid_theorem.py
"""

from __future__ import annotations

import itertools
import random
import sys

import sympy as sp

FAIL: list[str] = []


def check(cond, msg):
    print(("  PASS  " if cond else "  FAIL  ") + msg)
    if not cond:
        FAIL.append(msg)


def matchings(vs):
    if not vs:
        yield ()
        return
    v = vs[0]
    for k in range(1, len(vs)):
        rest = vs[1:k] + vs[k + 1:]
        for m in matchings(rest):
            yield ((v, vs[k]),) + m


def generic_blocks(n):
    sym = {}
    for i, j in itertools.combinations(range(n), 2):
        for a, b in itertools.product(range(3), repeat=2):
            sym[i, j, a, b] = sp.Symbol(f"w{i}_{j}_{a}{b}")

    def W(i, j, a, b):
        return sym[i, j, a, b] if i < j else sym[j, i, b, a]
    return W


def coeff(W, verts, word):
    """T_{W[A]}(word|A) for the vertex tuple A; T_{} = 1."""
    return sp.Add(*[sp.Mul(*[W(i, j, word[i], word[j]) for i, j in m]) for m in matchings(tuple(verts))])


def perm_form(vecs):
    k = len(vecs)
    return sp.Add(*[sp.Mul(*[vecs[i][p[i]] for i in range(k)]) for p in itertools.permutations(range(k))])


# --------------------------------------------------------------------- [1]
def check_two_vertex_expansion():
    print("[1] Theorem 1: T(w) = W_ab[b,g] T_R(c) + sum_{u != v in R} W_au W_bv T_{R-u-v}(c)")
    rng = random.Random(20261008)
    for n, samples in [(4, None), (6, 6), (8, 2)]:
        W = generic_blocks(n)
        ok = True
        count = 0
        pairs = [(0, 1), (2, 5), (3, 7)] if n == 8 else list(itertools.combinations(range(n), 2))
        for a, b in pairs:
            R = [v for v in range(n) if v not in (a, b)]
            words = (list(itertools.product(range(3), repeat=n)) if samples is None
                     else [tuple(rng.randrange(3) for _ in range(n)) for _ in range(samples)])
            for w in words:
                lhs = coeff(W, range(n), w)
                rhs = W(a, b, w[a], w[b]) * coeff(W, R, w)
                for u, v in itertools.permutations(R, 2):
                    rest = [x for x in R if x not in (u, v)]
                    rhs += W(a, u, w[a], w[u]) * W(b, v, w[b], w[v]) * coeff(W, rest, w)
                ok &= sp.expand(lhs - rhs) == 0
                count += 1
        check(ok, f"n = {n}: identity holds on {count} (pair, word) cases")


# --------------------------------------------------------------------- [2], [3]
def check_hollow_certificate():
    print("[2] hollow determinant and the explicit degree-two cofactor certificate")
    h12, h13, h23 = sp.symbols("h12 h13 h23")
    H = sp.Matrix([[0, h12, h13], [h12, 0, h23], [h13, h23, 0]])
    check(sp.expand(H.det() - 2 * h12 * h13 * h23) == 0, "det H = 2 h12 h13 h23")
    y, yp, z, zp = (sp.Matrix(sp.symbols(f"{s}1:4")) for s in ("y", "yq", "z", "zq"))
    E = sp.eye(3)
    ok = True
    for p, q in itertools.product(range(3), repeat=2):
        Y = sp.Matrix.hstack(y, yp, E[:, p])
        Z = sp.Matrix.hstack(z, zp, E[:, q])
        G = Z.T * H * Y
        # G[i,j] for i,j < 2 are the four grid values z_i^T H y_j
        g = {(0, 0): G[1, 1] * G[2, 2] - G[1, 2] * G[2, 1],
             (0, 1): -(G[1, 0] * G[2, 2] - G[1, 2] * G[2, 0]),
             (1, 0): G[0, 2] * G[2, 1],
             (1, 1): -G[0, 2] * G[2, 0]}
        cert = sum(g[i, j] * G[i, j] for i in range(2) for j in range(2))
        ok &= sp.expand(cert - G.det()) == 0
        ok &= sp.expand(G.det() - Z.det() * H.det() * Y.det()) == 0
        ok &= all(sp.expand(G[i, j] - (Z[:, i].T * H * Y[:, j])[0]) == 0 for i in range(2) for j in range(2))
    check(ok, "for all p, q: sum g_ij G_ij = det G = det Z * 2 h12 h13 h23 * det Y")
    print("[3] staircase minors")
    ok = True
    for p in range(3):
        u, j = [r for r in range(3) if r != p]
        Y = sp.Matrix.hstack(y, yp.subs(sp.Symbol(f"yq{u + 1}"), 0), E[:, p])
        d = sp.factor(Y.det())
        ok &= sp.expand(d**2 - (y[u] * yp[j]) ** 2) == 0
    check(ok, "y'_u = 0  =>  det[y, y', e_p] = +- y_u y'_j  ({u, j, p} = {1,2,3})")


# --------------------------------------------------------------------- [4]
def check_plane_rigidity_ingredients():
    print("[4] Theorem 3 ingredients")
    x, y, z = (sp.symbols(f"{s}1:4") for s in "xyz")
    Bx = sp.Matrix([[0, x[2], x[1]], [x[2], 0, x[0]], [x[1], x[0], 0]])
    check(sp.expand(perm_form([x, y, z]) - (sp.Matrix(y).T * Bx * sp.Matrix(z))[0]) == 0,
          "perm(x,y,z) = y^T B_x z")
    check(sp.expand(Bx.det() - 2 * x[0] * x[1] * x[2]) == 0, "det B_x = 2 x1 x2 x3")
    l1, l2, l3 = sp.symbols("l1 l2 l3", nonzero=True)
    v = (1 / l1, 1 / l2, -2 / l3)
    check(sp.simplify(l1 * v[0] + l2 * v[1] + l3 * v[2]) == 0,
          "full l: (1/l1, 1/l2, -2/l3) lies in l-perp, all coordinates nonzero (char != 2)")
    v = (1 / l1, -1 / l2, 1)
    check(sp.simplify(l1 * v[0] + l2 * v[1]) == 0, "l = (l1, l2, 0): (1/l1, -1/l2, 1) lies in l-perp")
    E = sp.eye(3)
    ok = True
    for u in range(3):
        basis = [E[:, r] for r in range(3) if r != u]
        ok &= all(perm_form([list(a), list(b), list(c)]) == 0 for a in basis for b in basis for c in basis)
    check(ok, "perm vanishes on H_u x H_u x H_u for each coordinate plane H_u")
    ok = True
    for us in itertools.product(range(3), repeat=3):
        if len(set(us)) == 1:
            continue
        ok &= any(all(pi[t] != us[t] for t in range(3)) for pi in itertools.permutations(range(3)))
    check(ok, "(u0,u1,u2) not all equal => a permutation pi with pi(t) != u_t exists "
              "(so perm(e_pi0, e_pi1, e_pi2) = 1 on H_u0 x H_u1 x H_u2)")


# --------------------------------------------------------------------- [5]
def check_cube_proposition():
    print("[5] Proposition 4: degree-3 cube certificates")
    Y = [sp.Matrix(3, 2, lambda r, c, t=t: sp.Symbol(f"y{t}_{r}{c}")) for t in range(3)]
    gens = [s for M in Y for s in M]
    A = {(i, j, k): sp.expand(perm_form([list(Y[0][:, i]), list(Y[1][:, j]), list(Y[2][:, k])]))
         for i, j, k in itertools.product(range(2), repeat=3)}
    unknowns, expr = [], 0
    for (i, j, k), a in A.items():
        for r in itertools.product(range(3), repeat=3):
            c = sp.Symbol(f"c{i}{j}{k}_{r[0]}{r[1]}{r[2]}")
            unknowns.append(c)
            expr += c * Y[0][r[0], 1 - i] * Y[1][r[1], 1 - j] * Y[2][r[2], 1 - k] * a
    expr = sp.expand(expr)

    def minor(M, I):
        return M[I[0], 0] * M[I[1], 1] - M[I[1], 0] * M[I[0], 1]

    def solvable(I):
        target = sp.expand(sp.Mul(*[minor(Y[t], I[t]) for t in range(3)]))
        eqs = sp.Poly(expr - target, *gens).coeffs()
        return sp.linsolve(eqs, unknowns)

    def phi(a, b, c):  # phi(a,b,c) = c1 (a1 b2 + a2 b1) - a1 b1 c2  (coordinates 1,2,3)
        return c[0] * (a[0] * b[1] + a[1] * b[0]) - a[0] * b[0] * c[1]

    closed = sum((-1) ** (i + j + k) * phi(Y[0][:, 1 - i], Y[1][:, 1 - j], Y[2][:, 1 - k]) * A[i, j, k]
                 for i, j, k in itertools.product(range(2), repeat=3))
    target = 2 * minor(Y[0], (0, 1)) * minor(Y[1], (0, 1)) * minor(Y[2], (0, 2))
    check(sp.expand(closed - target) == 0,
          "closed form: sum_ijk (-1)^(i+j+k) phi(Y0[1-i], Y1[1-j], Y2[1-k]) A_ijk "
          "= 2 D12(Y0) D12(Y1) D13(Y2)")
    check(solvable(((0, 1), (0, 1), (0, 2))) != sp.EmptySet,
          "I = ({1,2},{1,2},{1,3}) is in the degree-3 span (linear solve, cross-check)")
    check(solvable(((0, 1), (0, 1), (0, 1))) == sp.EmptySet,
          "I all equal: not in the degree-3 span (not even in the radical: H_3^3 is isotropic)")
    check(solvable(((0, 1), (0, 2), (1, 2))) == sp.EmptySet,
          "I pairwise distinct: not in the degree-3 span (in the radical by Theorem 3)")


# --------------------------------------------------------------------- [6]
def check_cut_slices():
    print("[6] k-vs-k slices and single-entry contraction")
    for k in (3, 4):
        n = 2 * k
        W = generic_blocks(n)
        T, U = list(range(k)), list(range(k, n))
        sigma = {u: (u - k) % 3 for u in U}

        def Wz(i, j, a, b):  # U independent at sigma
            if i in U and j in U:
                return sp.Integer(0)
            return W(i, j, a, b)
        rng = random.Random(k)
        ok = True
        for _ in range(4 if k == 4 else 27):
            w = [0] * n
            for t in T:
                w[t] = rng.randrange(3)
            for u in U:
                w[u] = sigma[u]
            lhs = coeff(Wz, range(n), w)
            rows = [[W(t, u, w[t], w[u]) for u in U] for t in T]
            ok &= sp.expand(lhs - perm_form(rows)) == 0
        check(ok, f"k = {k}: on words with U pinned and U independent, T(w) = perm_k(rows)")
    for k in (4, 5):
        vecs = [list(sp.symbols(f"v{i}_1:{k + 1}")) for i in range(3)]
        lam = sp.symbols(f"lam1:{k - 2}")
        singles = []
        for i in range(k - 3):
            e = [0] * k
            e[3 + i] = lam[i]
            singles.append(e)
        lhs = perm_form(singles + vecs)
        rhs = sp.Mul(*lam) * perm_form([vec[:3] for vec in vecs])
        check(sp.expand(lhs - rhs) == 0,
              f"k = {k}: perm_k(lam e_4, ..., lam e_k, y, z, v) = prod(lam) perm_3(y|C, z|C, v|C)")


# --------------------------------------------------------------------- [7]
def check_boundaries():
    print("[7] boundary examples")
    check(perm_form([[1, 1], [1, -1]]) == 0,
          "k = 2: lines <(1,1)>, <(1,-1)> are perm_2-isotropic, neither a coordinate line")
    x, xp = [1, 1, 1, 1], [1, -4, -4, -1]
    y, z = sp.symbols("y1:5"), sp.symbols("z1:5")
    form = sp.expand(perm_form([x, xp, list(y), list(z)]))
    B = sp.Matrix(4, 4, lambda i, j: form.coeff(y[i]).coeff(z[j]))
    ker = B.nullspace()
    ok = B.det() == 0 and len(ker) == 1
    if ok:
        zz = list(ker[0])
        ok = sp.expand(perm_form([x, xp, list(y), zz])) == 0
    check(ok, "k = 4: x = (1,1,1,1), x' = (1,-4,-4,-1) full, B_{x,x'} singular; "
              "perm_4 vanishes on <x> x <x'> x F^4 x <kernel vector> (dims 1+1+4+1)")


def main() -> int:
    check_two_vertex_expansion()
    check_hollow_certificate()
    check_plane_rigidity_ingredients()
    check_cube_proposition()
    check_cut_slices()
    check_boundaries()
    if FAIL:
        print(f"RESULT: FAIL ({len(FAIL)} checks)")
        return 1
    print("RESULT: PASS (identities of the three-column bilinear grid theorem replayed exactly)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
