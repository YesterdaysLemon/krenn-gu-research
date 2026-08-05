#!/usr/bin/env python3
"""Generic invariants (profile, relation ranks, kernel-kernel test) at exact
sample points of the certified components 2nd, L1, 6th, 8th, and the W-branch.

kernel-kernel test: for each rank-3 edge with rank-one relation u_a (x) u_b,
check whether u_a in K_a and/or u_b in K_b (K_i = pure kernel line of T on U_i,
computed from the mode-i flattening of the restricted tensor).
"""
import itertools, sympy as sp

PERMS4 = tuple(itertools.permutations(range(4)))
COORD_PAIRS = tuple(itertools.combinations(range(4), 2))

def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))

def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}

def invariants(planes, name):
    planes = [[[sp.nsimplify(c) for c in row] for row in pl] for pl in planes]
    T = {}
    for bits in itertools.product((0,1), repeat=4):
        T[bits] = perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4)))
    assert any(val != 0 for val in T.values()), "zero restriction"
    # mode-i kernels from mode-i flattening (2 x 8), rank must be 1
    kernels = []
    for m in range(4):
        mat = sp.zeros(2, 8)
        for bits in itertools.product((0,1), repeat=4):
            rest = tuple(bits[j] for j in range(4) if j != m)
            col = rest[0]*4 + rest[1]*2 + rest[2]
            mat[bits[m], col] = T[bits]
        assert mat.rank() == 1, (name, m, "not pure")
        ns = mat.T.nullspace() if False else sp.Matrix(mat).nullspace()
        # nullspace of the 2x8 as map C^2 -> C^8? we want kernel combination of ROWS:
        # coefficients (l0,l1) with l0*row0+l1*row1 = 0
        nsL = sp.Matrix(mat.T).nullspace()
        assert len(nsL) == 1
        l = nsL[0]
        kernels.append([sp.expand(l[0]*planes[m][0][t] + l[1]*planes[m][1][t]) for t in range(4)])
    profile = []
    rels = []
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
            K = sp.Matrix(2, 2, k)
            rk = K.rank()
            info = {"edge": (a_, b_), "rank": rk}
            if rk == 1:
                lv = K[:, 0] if any(c != 0 for c in K[:, 0]) else K[:, 1]
                rv = (K[0, :] if any(c != 0 for c in K[0, :]) else K[1, :]).T
                ua = [sp.expand(lv[0]*planes[a_][0][t] + lv[1]*planes[a_][1][t]) for t in range(4)]
                ub = [sp.expand(rv[0]*planes[b_][0][t] + rv[1]*planes[b_][1][t]) for t in range(4)]
                pr = rmul(ua, ub)
                assert all(sp.simplify(val) == 0 for val in pr.values())
                def in_kernel(u, K_):
                    return sp.Matrix([u, K_]).rank() == 1
                info["a_endpoint_in_kernel"] = in_kernel(ua, kernels[a_])
                info["b_endpoint_in_kernel"] = in_kernel(ub, kernels[b_])
                info["supp_a"] = tuple(t for t in range(4) if sp.simplify(ua[t]) != 0)
                info["supp_b"] = tuple(t for t in range(4) if sp.simplify(ub[t]) != 0)
            rels.append(info)
    print(f"== {name}")
    print("   profile:", tuple(profile))
    for info in rels:
        print("  ", info)
    kk = any(info.get("a_endpoint_in_kernel") and info.get("b_endpoint_in_kernel")
             for info in rels if info["rank"] == 1)
    print("   has kernel-kernel rank-one relation:", kk)
    return tuple(profile), rels, kk

# --- 2nd component (diagonal quadric 2+2), radical-star normal form (6)-(9)
A, B, C, E, F, H = 1, 1, 5, 1, 1, 1   # Psi = 0 identically on this line (checked)
Psi = A**3*F**3 + A**2*C*F**2*H - A*B**2*F*H**2 - A*C**2*E**2*F + A*C**2*F*H**2 - B**2*C*E**2*H
assert Psi == 0
planes2 = [
    [[E, -F, -F, -E], [A, -B, B, A]],
    [[1, 0, 0, -1], [A, C+B, C-B, A]],
    [[0, 1, -1, 0], [H+E, F, F, H-E]],
    [[1, 0, 0, 1], [0, 1, 1, 0]],
]
invariants(planes2, "2nd (diagonal-quadric 2+2)  [A,B,C,E,F,H]=(1,1,5,1,1,1)")

# --- L1 (1+3), radical-star (10)-(14): T = -D+G+S
S, D, G = 2, 3, 5
Tv = -D + G + S
P_ = G - Tv; Q_ = D - S
planesL = [
    [[2, P_+Q_, Q_-P_, 0], [0, 0, 1, 1]],
    [[0, 1, -1, 0], [1, 0, S, D]],
    [[0, 1, 0, -1], [1, 0, G, Tv]],
    [[0, 1, 1, 0], [0, 1, 0, 1]],
]
invariants(planesL, "L1 (1+3 split cubic)  S,D,G=(2,3,5), T=-D+G+S")

# --- 6th component (from verifier sixth_component_invariants), d,p,q = 2,3,5
dd, pp, qq = 2, 3, 5
n = qq*(dd + pp + qq)
planes6 = [
    [[-dd*pp, dd+qq, n, 0], [dd*pp, -dd-qq, 0, n]],
    [[0, 0, 1, 1], [-dd, 1, -pp-qq, dd]],
    [[pp, 1, 0, qq], [-1, 0, 1, 0]],
    [[1, 0, 1, 0], [0, 0, -1, 1]],
]
invariants(planes6, "6th (mixed orientation)  d,p,q=(2,3,5)")

# --- 8th component (disjoint mixed star), doc (5)-(7), sample a,b,f,phi=(1,1,2,1)
a8, b8, f8, p8 = 1, 1, 2, 1
Phi8 = a8**2*b8*f8*p8**2 + a8**2*f8**2 - b8**2*f8**2 + b8**2*p8**2 - b8*f8 - 1
assert Phi8 == 0, Phi8
j8 = f8 + b8*p8**2
kap8 = p8*(b8*f8 + 1)
eta8 = -(b8*f8 + 1)
planes8 = [
    [[0, 0, 1, -1], [a8+b8, a8-b8, 0, 2]],
    [[-a8*f8+1, -a8*f8-1, f8+p8, f8-p8], [1, 1, 0, 0]],
    [[-a8*j8+eta8, -a8*j8-eta8, j8+kap8, j8-kap8], [1, 1, 0, 0]],
    [[1, -1, 0, 0], [0, 0, 1, 1]],
]
invariants(planes8, "8th (disjoint mixed star)  a,b,f,phi=(1,1,2,1)")

# --- W-branch sample (equal-support in-out)
e_ = 3
vv = (2, 5, 7, -11); xx = (2, 5, 13, -4)
planesW = [
    [[vv[0], -vv[1], 0, 0], [0, 0, 1, -1]],
    [[0, 0, 1, -1], list(vv)],
    [[0, 0, 1, -e_], list(xx)],
    [[0, 0, 1, 1], [0, 0, 1, e_]],
]
invariants(planesW, "W-branch  e=3, v=(2,5,7,-11), x=(2,5,13,-4)")
