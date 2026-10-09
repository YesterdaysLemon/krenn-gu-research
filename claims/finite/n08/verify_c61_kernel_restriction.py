#!/usr/bin/env python3
"""Exact replay of the kernel-restriction identities for the class C_{6,1}.

Scope (see docs/strategy/c61-exact-attack-2026-10-09.md):

* C_{6,1}: six three-colour vertices B = {0..5} with 3x3 blocks W[u,v],
  two one-colour vertices a, b with rows r[z], s[z] in C^3, and NO a-b edge.
* For S a subset of B and v_s in K_s = ker r_s^T  cap  ker s_s^T, the
  contraction of the matching tensor at every s in S with v_s equals the
  matching tensor of the configuration on F = B - S plus the one-colour
  vertices a, b and S (rows W[s,f]^T v_s, weights v_s^T W[s,s'] v_s'),
  in which a and b are adjacent to no one-colour vertex.
* |S| = 3: the restriction is the image of the 3 x 3 x 3 "permanental"
  tensor Per_3 under N_1^T (x) N_2^T (x) N_3^T.
* |S| = 4: the restriction is h_S(v) * (y_k^T C_kk' y_k'),
  C_kk' = r_k s_k'^T + s_k r_k'^T (rank <= 2).
* The slice span of Per_3 contains no rank-one matrix; the slice span of
  the unit tensor <3> does.  Hence Per_3 is not GL^3-equivalent to <3>.

Everything is exact (integers / Fractions / sympy).  This is a replay of the
displayed identities and of the elementary rank fact; the logical argument
is the hand proof in the strategy note.  It is not an independent audit.
"""
from __future__ import annotations

import itertools
import random
from fractions import Fraction

import sympy as sp

COLS = range(3)


# ---------------------------------------------------------------- generic engine
def perfect_matchings(verts):
    verts = list(verts)
    if not verts:
        yield []
        return
    u = verts[0]
    for k in range(1, len(verts)):
        v = verts[k]
        rest = verts[1:k] + verts[k + 1:]
        for m in perfect_matchings(rest):
            yield [(u, v)] + m


def matching_tensor(dims, weight, coloured):
    """dims[v] in {1,3}; weight(u, v, i, j) -> exact number (0 if no edge);
    returns dict word(tuple over `coloured`) -> value."""
    verts = list(range(len(dims)))
    pms = list(perfect_matchings(verts))
    pos = {v: k for k, v in enumerate(coloured)}
    out = {}
    for word in itertools.product(COLS, repeat=len(coloured)):
        col = lambda v: word[pos[v]] if dims[v] == 3 else 0
        tot = Fraction(0)
        for pm in pms:
            prod = Fraction(1)
            for (u, v) in pm:
                w = weight(u, v, col(u), col(v))
                if w == 0:
                    prod = Fraction(0)
                    break
                prod *= w
            tot += prod
        out[word] = tot
    return out


# ---------------------------------------------------------------- configuration
def random_config(rng, lo=-3, hi=3):
    W = {}
    for u in range(6):
        for v in range(u + 1, 6):
            W[(u, v)] = [[Fraction(rng.randint(lo, hi)) for _ in COLS] for _ in COLS]
    r = [[Fraction(rng.randint(lo, hi)) for _ in COLS] for _ in range(6)]
    s = [[Fraction(rng.randint(lo, hi)) for _ in COLS] for _ in range(6)]
    return W, r, s


def Wget(W, u, v, i, j):
    return W[(u, v)][i][j] if u < v else W[(v, u)][j][i]


def c61_tensor_generic(W, r, s):
    """8-vertex engine: vertices 0..5 coloured, 6 = a, 7 = b, no a-b edge."""
    dims = [3] * 6 + [1, 1]

    def weight(u, v, i, j):
        if u > v:
            u, v, i, j = v, u, j, i
        if v < 6:
            return Wget(W, u, v, i, j)
        if u >= 6:
            return Fraction(0)  # no a-b edge (kappa = 0)
        return r[u][i] if v == 6 else s[u][i]

    return matching_tensor(dims, weight, list(range(6)))


def c61_tensor_formula(W, r, s):
    """Phi(gamma) = sum_{z != z'} r_z[g_z] s_z'[g_z'] Haf_4(B - z - z')."""
    out = {}
    for g in itertools.product(COLS, repeat=6):
        tot = Fraction(0)
        for z in range(6):
            for zp in range(6):
                if z == zp:
                    continue
                rest = [t for t in range(6) if t not in (z, zp)]
                p, q, t, u = rest
                h = (Wget(W, p, q, g[p], g[q]) * Wget(W, t, u, g[t], g[u])
                     + Wget(W, p, t, g[p], g[t]) * Wget(W, q, u, g[q], g[u])
                     + Wget(W, p, u, g[p], g[u]) * Wget(W, q, t, g[q], g[t]))
                tot += r[z][g[z]] * s[zp][g[zp]] * h
        out[g] = tot
    return out


def kernel_vector(rs, ss):
    M = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in rs],
                   [sp.Rational(x.numerator, x.denominator) for x in ss]])
    ns = M.nullspace()
    assert ns, "kernel is nonzero for two rows in C^3"
    v = ns[0]
    return [Fraction(int(sp.fraction(x)[0]), int(sp.fraction(x)[1])) for x in v]


def contract(T, S, vs):
    """Contract the order-6 tensor T at positions in S with vectors vs[s]."""
    F = [z for z in range(6) if z not in S]
    out = {}
    for gF in itertools.product(COLS, repeat=len(F)):
        tot = Fraction(0)
        for gS in itertools.product(COLS, repeat=len(S)):
            g = [0] * 6
            for k, z in enumerate(F):
                g[z] = gF[k]
            coef = Fraction(1)
            for k, z in enumerate(S):
                g[z] = gS[k]
                coef *= vs[z][gS[k]]
            if coef:
                tot += coef * T[tuple(g)]
        out[gF] = tot
    return out


def restricted_config_tensor(W, r, s, S, vs):
    """Matching tensor of F + {a, b} + S (S one-colour, contracted with vs)."""
    F = [z for z in range(6) if z not in S]
    order = F + ["a", "b"] + list(S)
    dims = [3] * len(F) + [1] * (2 + len(S))
    lab = {k: lbl for k, lbl in enumerate(order)}

    def weight(u, v, i, j):
        U, V = lab[u], lab[v]
        if isinstance(U, str) and isinstance(V, str):
            return Fraction(0)  # a-b
        if isinstance(V, str):  # U in F u S, V ancilla
            U, V, i, j = V, U, j, i
            u, v = v, u
        if isinstance(U, str):  # U ancilla a/b, V vertex of B
            row = r if U == "a" else s
            if V in S:
                return sum(row[V][x] * vs[V][x] for x in COLS)
            return row[V][j]
        # both in B
        inS_U, inS_V = U in S, V in S
        if inS_U and inS_V:
            return sum(vs[U][x] * Wget(W, U, V, x, y) * vs[V][y] for x in COLS for y in COLS)
        if inS_U:
            return sum(vs[U][x] * Wget(W, U, V, x, j) for x in COLS)
        if inS_V:
            return sum(Wget(W, U, V, i, y) * vs[V][y] for y in COLS)
        return Wget(W, U, V, i, j)

    return matching_tensor(dims, weight, list(range(len(F))))


def per3_image(N):
    """sum over bijections F -> roles (a, b, S) of prod_i (N_i y_i)[role]."""
    out = {}
    for g in itertools.product(COLS, repeat=3):
        tot = Fraction(0)
        for perm in itertools.permutations(range(3)):
            prod = Fraction(1)
            for i in range(3):
                prod *= N[i][perm[i]][g[i]]
            tot += prod
        out[g] = tot
    return out


def check_slice_span_fact():
    a, b, c = sp.symbols("a b c")
    M = sp.Matrix([[0, c, b], [c, 0, a], [b, a, 0]])  # a M1 + b M2 + c M3 for Per_3
    minors = [M.extract(list(rr), list(cc)).det()
              for rr in itertools.combinations(range(3), 2)
              for cc in itertools.combinations(range(3), 2)]
    sol = sp.solve(minors, [a, b, c], dict=True)
    assert sol == [{a: 0, b: 0, c: 0}], sol
    # unit tensor <3>: slices E_00, E_11, E_22; E_00 has rank one.
    assert sp.Matrix([[1, 0, 0], [0, 0, 0], [0, 0, 0]]).rank() == 1
    # Per_3 slices: (Per_3)_{x,.,.} for x = 0 is e1 e2^T + e2 e1^T etc.
    for x in COLS:
        S = sp.zeros(3, 3)
        for p in itertools.permutations(range(3)):
            if p[0] == x:
                S[p[1], p[2]] += 1
        assert S.is_symmetric() and all(S[i, i] == 0 for i in COLS)
    return True


def main(seed=20261009, trials=3):
    rng = random.Random(seed)
    assert check_slice_span_fact()
    print("slice-span fact: Per_3 slice span has no rank-one matrix; <3> does  OK")
    for t in range(trials):
        W, r, s = random_config(rng)
        T = c61_tensor_formula(W, r, s)
        T2 = c61_tensor_generic(W, r, s)
        assert T == T2
        vs = {z: kernel_vector(r[z], s[z]) for z in range(6)}
        for z in range(6):
            assert sum(r[z][x] * vs[z][x] for x in COLS) == 0
            assert sum(s[z][x] * vs[z][x] for x in COLS) == 0
        for size in (1, 2, 3, 4):
            for S in itertools.combinations(range(6), size):
                lhs = contract(T, list(S), vs)
                rhs = restricted_config_tensor(W, r, s, list(S), vs)
                assert lhs == rhs, (t, S)
                F = [z for z in range(6) if z not in S]
                if size == 3:
                    N = []
                    for i, f in enumerate(F):
                        u = [Fraction(0)] * 3
                        for k, sv in enumerate(S):
                            rest = [x for x in S if x != sv]
                            cS = sum(vs[rest[0]][x] * Wget(W, rest[0], rest[1], x, y) * vs[rest[1]][y]
                                     for x in COLS for y in COLS)
                            for j in COLS:
                                u[j] += sum(Wget(W, f, sv, j, x) * vs[sv][x] for x in COLS) * cS
                        N.append([r[f], s[f], u])
                    assert lhs == per3_image(N), (t, S)
                if size == 4:
                    k, kp = F
                    Sl = list(S)
                    def A(p, q):
                        return sum(vs[p][x] * Wget(W, p, q, x, y) * vs[q][y] for x in COLS for y in COLS)
                    h = A(Sl[0], Sl[1]) * A(Sl[2], Sl[3]) + A(Sl[0], Sl[2]) * A(Sl[1], Sl[3]) \
                        + A(Sl[0], Sl[3]) * A(Sl[1], Sl[2])
                    for (x, y), val in lhs.items():
                        C = r[k][x] * s[kp][y] + s[k][x] * r[kp][y]
                        assert val == h * C, (t, S)
        print(f"trial {t}: tensor engines agree on 729 words; kernel restriction identities "
              f"hold for all S with |S| in 1..4; |S|=3 Per_3 image and |S|=4 rank-2 form OK")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
