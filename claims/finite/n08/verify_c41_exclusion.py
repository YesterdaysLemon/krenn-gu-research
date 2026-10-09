#!/usr/bin/env python3
"""Exact computer-assisted exclusion of C_{4,1}.

C_{4,1} (the order-6 instance of the pair-contraction route of
docs/strategy/c61-exact-attack-2026-10-09.md): four three-colour vertices
0..3 with arbitrary complex 3x3 blocks W, two one-colour vertices a, b with
rows r_z, s_z in C^3, NO a-b edge.  Claim: the matching tensor is never
GHZ(4,3) with three nonzero weights mu_c.

Reduction (hand; see the note, Section 5):

1. (AK) [THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM, m = 4]: for each
   colour c, a has a vertex z_c with r_{z_c} a nonzero multiple of e_c, and
   b has a vertex w_c with s_{w_c} a nonzero multiple of e_c; the z_c are
   distinct, and so are the w_c.
2. Relabel vertices so that z_c = c.  Torus scaling at (c, c) makes
   r_c = e_c (c = 0, 1, 2); r_3 = rho is arbitrary.  The b-units are
   s_{w_c} = beta_c e_c for an injective w; the remaining vertex u carries an
   arbitrary row sigma.  The remaining torus freedom and a global scaling
   of b (which rescales mu) set further nonzero entries to 1, as described
   in stratum(); every other nonzero entry is an independent nonzero symbol.
3. Strata: injective w (24), support of rho (8), support of sigma (8); the
   nonzero entries are independent nonzero symbols.  Simultaneous
   permutation of colours and of vertices 0, 1, 2 acts on strata; one
   representative per orbit is checked.
4. The tensor is linear in W:  P = L(r, s) vec(W).  A target with mu_c != 0
   for all c needs, for every c,
       e_{cccc} in Im L + span(e_{c'c'c'c'} : c' != c).
   For each stratum the script finds a colour c and a vector Lambda whose
   entries are rational functions of the stratum's symbols with monomial
   denominators, such that
       Lambda^T [L | e_{c'c'c'c'} (c' != c)] == 0   identically
   (checked by explicit multiplication), and
       Lambda[cccc] = monomial * prod_j f_j.
   At every point of the stratum where all f_j != 0 this excludes the
   point.  Each hypersurface f_j = 0 is handled recursively after
   substituting x = -b/a for a variable x in which f_j = a x + b is linear
   with a monomial coefficient a (nonzero on the torus).  The script fails
   loudly if this cannot be done.
   Candidates are tried first in the rank-one KR2 form
   Lambda = l_0 (x) l_1 (x) l_2 (x) l_3, where l_s lies in the common kernel
   of the two ancilla rows for the two vertices s outside a pair {i, j},
   and l_i^T C_ij l_j == 0 (C_ij = r_i s_j^T + s_i r_j^T).  A general
   left-nullspace search over the fraction field is the fallback.  The
   recorded run (about 30 s) used 295 certificate leaves and 79 hypersurface
   branches; 119 search nodes needed the fallback.

Self-test: L is checked against a generic perfect-matching engine.
Exact arithmetic throughout (sympy fraction fields).  This is a replay-type
certificate check written by the same author as the hand reduction; it is
not an independent audit.
"""
from __future__ import annotations

import itertools
import random
import sys
import time

import sympy as sp
from sympy.polys.matrices import DomainMatrix

V = range(4)
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
WORDS = list(itertools.product(range(3), repeat=4))
WIDX = {w: i for i, w in enumerate(WORDS)}


def build_L(r, s):
    cols = []
    for p in PAIRS:
        k, kp = p
        i, j = [z for z in V if z not in p]
        for x in range(3):
            for y in range(3):
                col = [0] * 81
                for w in WORDS:
                    if w[k] == x and w[kp] == y:
                        col[WIDX[w]] = r[i][w[i]] * s[j][w[j]] + s[i][w[i]] * r[j][w[j]]
                cols.append(col)
    return sp.Matrix(81, 54, lambda a, b: cols[b][a])


def pure(c):
    v = sp.zeros(81, 1)
    v[WIDX[(c,) * 4]] = 1
    return v


def generic_tensor(W, r, s):
    def pms(vs):
        if not vs:
            yield []
            return
        u = vs[0]
        for k in range(1, len(vs)):
            for m in pms(vs[1:k] + vs[k + 1:]):
                yield [(u, vs[k])] + m
    allpm = list(pms(list(range(6))))
    out = []
    for g in WORDS:
        tot = 0
        for pm in allpm:
            prod = 1
            for (u, v) in pm:
                if u >= 4 and v >= 4:
                    prod = 0
                    break
                if v == 4:
                    prod *= r[u][g[u]]
                elif v == 5:
                    prod *= s[u][g[u]]
                else:
                    prod *= W[(u, v)][g[u]][g[v]]
            tot += prod
        out.append(tot)
    return sp.Matrix(out)


def self_test(seed=7):
    rng = random.Random(seed)
    for _ in range(3):
        W = {p: [[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)] for p in PAIRS}
        r = [[rng.randint(-3, 3) for _ in range(3)] for _ in V]
        s = [[rng.randint(-3, 3) for _ in range(3)] for _ in V]
        wvec = sp.Matrix([W[p][x][y] for p in PAIRS for x in range(3) for y in range(3)])
        assert build_L(r, s) * wvec == generic_tensor(W, r, s)
    print("self-test: L agrees with the perfect-matching engine  OK", flush=True)


def is_monomial(e, syms):
    e = sp.expand(e)
    if e == 0:
        return False
    if not syms:
        return True
    return len(sp.Poly(e, *syms).terms()) == 1


def polynomial_columns(M):
    """Scale each column by the lcm of its denominators (does not change the
    left nullspace) so that all entries are polynomials."""
    M = M.applyfunc(lambda x: sp.cancel(sp.sympify(x)))
    for j in range(M.shape[1]):
        dens = [sp.fraction(sp.together(M[i, j]))[1] for i in range(M.shape[0]) if M[i, j] != 0]
        if dens:
            d = sp.lcm(dens)
            if d != 1:
                for i in range(M.shape[0]):
                    M[i, j] = sp.expand(sp.cancel(M[i, j] * d))
    return M


def _cross(u, v):
    return [sp.expand(u[1] * v[2] - u[2] * v[1]), sp.expand(u[2] * v[0] - u[0] * v[2]),
            sp.expand(u[0] * v[1] - u[1] * v[0])]


def _dot(u, v):
    return sp.expand(sum(a * b for a, b in zip(u, v)))


def _nz(u):
    return any(sp.cancel(x) != 0 for x in u)


UNIT = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


def _kernel_cands(rz, sz):
    """Polynomial vectors in K_z = ker r_z^T  cap  ker s_z^T."""
    k = _cross(rz, sz)
    if _nz(k):
        return [k]
    v = rz if _nz(rz) else sz
    if _nz(v):
        return [x for x in (_cross(v, e) for e in UNIT) if _nz(x)]
    return UNIT + [[1, 1, 1]]


def rank_one_candidates(r, s, syms):
    """KR2-type certificates Lambda = l_0 (x) l_1 (x) l_2 (x) l_3 with
    l_s in K_s for the two vertices s outside a pair {i, j} and
    l_i^T C_ij l_j == 0.  Then Lambda^T L == 0 (every pair contraction has a
    factor a_x b_y + b_x a_y that vanishes)."""
    out = []
    for (i, j) in PAIRS:
        S = [z for z in V if z not in (i, j)]
        Cij = [[sp.expand(r[i][x] * s[j][y] + s[i][x] * r[j][y]) for y in range(3)] for x in range(3)]
        Ki = UNIT + _kernel_cands(r[i], s[i])
        for l1 in _kernel_cands(r[S[0]], s[S[0]]):
            for l2 in _kernel_cands(r[S[1]], s[S[1]]):
                for li in Ki:
                    wv = [_dot([Cij[x][y] for x in range(3)], li) for y in range(3)]
                    Kj = [x for x in (_cross(wv, e) for e in UNIT) if _nz(x)] if _nz(wv) else UNIT
                    for lj in Kj:
                        lam = {i: li, j: lj, S[0]: l1, S[1]: l2}
                        diag = [sp.cancel(lam[0][c] * lam[1][c] * lam[2][c] * lam[3][c]) for c in range(3)]
                        for c in range(3):
                            if diag[c] != 0 and all(diag[cc] == 0 for cc in range(3) if cc != c):
                                vec = sp.Matrix([[sp.expand(lam[0][g[0]] * lam[1][g[1]] * lam[2][g[2]] * lam[3][g[3]])
                                                  for g in WORDS]])
                                out.append((c, vec))
    return out


def classify(vec, M0, row, syms):
    prod = (vec * M0).applyfunc(lambda x: sp.expand(sp.cancel(x)))
    if not all(x == 0 for x in prod):
        return None
    num = sp.factor(sp.cancel(vec[row]))
    _, facs = sp.factor_list(num)
    bad = [f for f, _ in facs if f.free_symbols and not is_monomial(f, syms)]
    deg = sum(sp.Poly(f, *syms).total_degree() for f in bad) if syms else 0
    return (len(bad), deg, bad)


def candidates(r, s, syms):
    L = build_L(r, s)
    out = []
    M0s = {c: sp.Matrix.hstack(L, *[pure(cc) for cc in range(3) if cc != c]) for c in range(3)}
    for c, vec in rank_one_candidates(r, s, syms):
        res = classify(vec, M0s[c], WIDX[(c,) * 4], syms)
        if res is not None:
            out.append((res[0], res[1], c, res[2]))
            if res[0] == 0:
                return out
    if out:
        out.sort(key=lambda t: (t[0], t[1]))
        return out
    STATS["fallback"] += 1
    K = sp.QQ.frac_field(*syms) if syms else sp.QQ
    for c in range(3):
        M0 = polynomial_columns(sp.Matrix.hstack(L, *[pure(cc) for cc in range(3) if cc != c]))
        row = WIDX[(c,) * 4]
        ns = DomainMatrix.from_Matrix(M0.T).convert_to(K).nullspace().to_Matrix()
        for i in range(ns.shape[0]):
            v = ns.row(i)
            if v[row] == 0:
                continue
            v = v.applyfunc(sp.together)
            den = sp.lcm([sp.fraction(x)[1] for x in v]) if syms else 1
            v = (v * den).applyfunc(lambda x: sp.expand(sp.cancel(x)))
            if any(sp.fraction(sp.together(x))[1].free_symbols for x in v):
                continue  # not polynomial
            prod = (v * M0).applyfunc(lambda x: sp.expand(sp.cancel(x)))
            if not all(x == 0 for x in prod):
                continue
            num = sp.factor(sp.cancel(v[row]))
            _, facs = sp.factor_list(num)
            bad = [f for f, _ in facs if f.free_symbols and not is_monomial(f, syms)]
            deg = sum(sp.Poly(f, *syms).total_degree() for f in bad) if syms else 0
            out.append((len(bad), deg, c, bad))
    out.sort(key=lambda t: (t[0], t[1]))
    return out


STATS = {"leaves": 0, "branches": 0, "fallback": 0}


def certify(r, s, syms, depth=0):
    cands = candidates(r, s, syms)
    if not cands:
        print(f"FAIL: no certificate (depth {depth})", flush=True)
        return False
    nb, _, c, bad = cands[0]
    if nb == 0:
        STATS["leaves"] += 1
        return True
    if depth >= 6:
        print(f"FAIL: depth limit, remaining factors {bad}", flush=True)
        return False
    ok = True
    for f in bad:
        branched = False
        for x in sorted(f.free_symbols, key=str):
            p = sp.Poly(f, x)
            if p.degree() != 1:
                continue
            a, b = p.all_coeffs()
            if not is_monomial(a, list(syms)):
                continue
            sub = {x: sp.cancel(-b / a)}
            r2 = [[sp.cancel(sp.sympify(e).subs(sub)) for e in row] for row in r]
            s2 = [[sp.cancel(sp.sympify(e).subs(sub)) for e in row] for row in s]
            STATS["branches"] += 1
            ok = certify(r2, s2, [y for y in syms if y != x], depth + 1) and ok
            branched = True
            break
        if not branched:
            print(f"FAIL: cannot branch on factor {f}", flush=True)
            ok = False
    return ok


def stratum(w, rs, ss):
    """Rows of the stratum after torus normalization.

    Torus parameters tau(z, c) multiply r_z[c] and s_z[c]; a global factor
    kappa multiplies all of s (and mu).  tau(c, c), c = 0, 1, 2, are spent on
    r_c = e_c.  Greedy normalization:
      * beta_c with w_c != c  -> 1 via tau(w_c, c);
      * rho[c] != 0           -> 1 via tau(3, c) if still unused;
      * sigma[c] != 0         -> 1 via tau(u, c) if still unused;
      * one entry that only kappa moves (beta_c with w_c = c, or sigma[u]
        when u < 3)            -> 1 via kappa.
    Everything else nonzero is an independent nonzero symbol."""
    u = [z for z in range(4) if z not in w][0]
    used = {(c, c) for c in range(3)}
    syms = []
    r = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]]
    s = [[0, 0, 0] for _ in V]
    kappa_only = []
    for c in range(3):
        if w[c] == c:
            kappa_only.append((w[c], c))
        else:
            s[w[c]][c] = 1
            used.add((w[c], c))
    for c in range(3):
        if rs[c]:
            if (3, c) not in used:
                r[3][c] = 1
                used.add((3, c))
            else:
                x = sp.Symbol(f"p{c}"); syms.append(x); r[3][c] = x
    for c in range(3):
        if ss[c]:
            if (u, c) in used and u < 3 and c == u:
                kappa_only.append((u, c))
            elif (u, c) not in used:
                s[u][c] = 1
                used.add((u, c))
            else:
                x = sp.Symbol(f"q{c}"); syms.append(x); s[u][c] = x
    for k, (z, c) in enumerate(kappa_only):
        if k == 0:
            s[z][c] = 1
        else:
            x = sp.Symbol(f"t{z}{c}"); syms.append(x); s[z][c] = x
    return r, s, syms


def canon(w, rs, ss):
    best = None
    for pi in itertools.permutations(range(3)):
        vh = lambda z: pi[z] if z < 3 else 3
        w2 = [None] * 3
        rs2 = [0] * 3
        ss2 = [0] * 3
        for c in range(3):
            w2[pi[c]] = vh(w[c])
            rs2[pi[c]] = rs[c]
            ss2[pi[c]] = ss[c]
        key = (tuple(w2), tuple(rs2), tuple(ss2))
        if best is None or key < best:
            best = key
    return best


def main():
    self_test()
    reps = {}
    for w in itertools.permutations(range(4), 3):
        for rs in itertools.product([0, 1], repeat=3):
            for ss in itertools.product([0, 1], repeat=3):
                reps.setdefault(canon(w, rs, ss), (w, rs, ss))
    print(f"strata: {24 * 64}, orbit representatives: {len(reps)}", flush=True)
    t0 = time.time()
    allok = True
    for k, key in enumerate(sorted(reps)):
        w, rs, ss = key
        r, s, syms = stratum(w, rs, ss)
        ts = time.time()
        ok = certify(r, s, syms)
        if "--verbose" in sys.argv:
            print(f"  stratum {k}: w={w} rho={rs} sigma={ss} symbols={len(syms)} "
                  f"ok={ok} {time.time() - ts:.1f}s", flush=True)
        allok = allok and ok
        if not ok:
            print(f"  stratum w={w} rho-support={rs} sigma-support={ss}: NOT EXCLUDED", flush=True)
        if (k + 1) % 20 == 0:
            print(f"  {k + 1}/{len(reps)} strata done, {time.time() - t0:.0f}s", flush=True)
    print(f"certificate leaves: {STATS['leaves']}, hypersurface branches: {STATS['branches']}, "
          f"fallback nullspace searches: {STATS['fallback']}")
    if allok:
        print("ALL STRATA EXCLUDED: C_{4,1} is empty")
    else:
        print("SOME STRATA NOT EXCLUDED")
        sys.exit(1)


if __name__ == "__main__":
    main()
