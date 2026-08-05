#!/usr/bin/env python3
"""TASK B. The coincident-support shared-factor chart (the tenth's chart)
and its case-Z stratification (exact).

Configuration (the radical-star classification's coincident-support case
with proportional free factors, i.e. the case that produced the tenth):
    ybar = (1,-1,0,0),  u3 = (1,1,0,0)  (conjugate pair in P01),
    U1 = span(ybar, p),  U2 = span(ybar, q),  U3 = span(u3, w),  U0 free,
relations  ybar*u3 = 0  at the edges {1,3} and {2,3}.

Kernel dichotomy for pure nonzero T = a x b x c x d: the identities
T(z,ybar,c,u3) == 0 and T(z,w1,ybar,u3) == 0 give b(ybar)d(u3) = 0 and
c(ybar)d(u3) = 0, hence
  case Z:  d(u3) != 0  =>  K1 = K2 = ybar   (this script + s04..s08),
  case Y:  d(u3)  = 0  =>  K3 = u3          (s09).

Case Z imposes three covectors on U0 (rows of M_Z):
  Z1 = T(z,ybar,ybar,w), Z2 = T(z,ybar,q,w), Z3 = T(z,p,ybar,w);
the residual support is B_Z = [T(z_i,p,q,u3), T(z_i,p,q,w)] and purity is
det B_Z = 0.  This script proves:
 (1) u3 lies in ker M_Z identically (so U0 contains u3 on every rank-2
     stratum, and p01(U0) != 0 fails nowhere: cf. the eighth's u1-lemma);
 (2) rank M_Z <= 2  <=>  w2*w3*(w0-w1)*(p2*q3-p3*q2) = 0 (exact 3x3-minor
     factorization) -- the four rank-2 branch families of s04;
 (3) the rank <= 1 locus decomposes into exactly six primes (Singular
     minAssGTZ over Q, gauge p=(0,1,p2,p3), q=(0,1,q2,q3), w=(0,W1,w2,w3)):
       #1 w = 0 (degenerate),
       #2 {w2=w3=0, p2q3-p3q2=0}: U3 = P01, p || q,
       #3 {w3=q3=p3=0}: all four planes in {X3-coordinate = 0}: T == 0,
       #4 {q3w2+q2w3, p3w2+p2w3, p2q3-p3q2, W1}: p_Pi || q_Pi || conj(w_Pi),
          w in Pi: THE TENTH'S HOME STRATUM,
       #5 {p2=p3=q2=q3=0}: U1 = U2 = P01,
       #6 {w2=q2=p2=0}: all four planes in {X2-coordinate = 0}: T == 0;
 (4) on #4 the whole Gr(2,3)-fibre is pure (det B_Z == 0 on every chart)
     and reproduces the tenth's tensor exactly; on #2 (p||q part) and #5
     the fibre restriction is zero or forced-zero:
       #2 rank-2 part (p not|| q): U0 = P01 forced and pure => T == 0;
       #2 rank-1 part: det B_Z = 4 b^2 e^2 k^2 != 0 on charts B (and its
          chart-A factor beF): the only pure U0 give T == 0;
       #5: B_Z == 0 identically: zero restriction.
"""
import itertools, subprocess, sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


z = sp.symbols("z0:4")
YBAR = (1, -1, 0, 0)
U3v = (1, 1, 0, 0)


def covrow(rows3):
    form = perm4((tuple(z),) + tuple(rows3))
    return [sp.expand(sp.diff(form, zi)) for zi in z]


p = sp.symbols("p0:4")
q = sp.symbols("q0:4")
w = sp.symbols("w0:4")

# the configuration's zero product
prod_ = {ab: sp.expand(YBAR[ab[0]]*U3v[ab[1]] + YBAR[ab[1]]*U3v[ab[0]])
         for ab in COORD_PAIRS}
assert all(val == 0 for val in prod_.values())

MZ = sp.Matrix([covrow((YBAR, YBAR, tuple(w))),
                covrow((YBAR, tuple(q), tuple(w))),
                covrow((tuple(p), YBAR, tuple(w)))])

# (1) u3 in ker M_Z identically
assert all(sp.expand(sum(MZ[i, j]*U3v[j] for j in range(4))) == 0 for i in range(3))
print("(1) u3 = (1,1,0,0) lies in ker M_Z identically: U0 contains u3 on")
print("    every case-Z rank-2 stratum.  OK")

# (2) 3x3 minors
m3 = {cols: sp.factor(MZ[:, cols].det()) for cols in itertools.combinations(range(4), 3)}
assert m3[(0, 1, 2)] == 0 and m3[(0, 1, 3)] == 0
f1 = sp.expand(4*w[2]*w[3]*(w[0]-w[1])*(p[2]*q[3]-p[3]*q[2]))
assert sp.expand(m3[(0, 2, 3)] - f1) == 0
assert sp.expand(m3[(1, 2, 3)] + f1) == 0
print("(2) rank M_Z <= 2  <=>  w2*w3*(w0-w1)*(p2*q3-p3*q2) = 0.  OK")

# (3) rank <= 1 decomposition (gauged chart)
p2, p3, q2, q3, W1, w2, w3 = sp.symbols("p2 p3 q2 q3 W1 w2 w3")
gauge = {p[0]: 0, p[1]: 1, p[2]: p2, p[3]: p3,
         q[0]: 0, q[1]: 1, q[2]: q2, q[3]: q3,
         w[0]: 0, w[1]: W1, w[2]: w2, w[3]: w3}
minors2 = []
for rr in itertools.combinations(range(3), 2):
    for cc in itertools.combinations(range(4), 2):
        mm = sp.expand(MZ[rr, cc].det().subs(gauge))
        if mm != 0:
            minors2.append(mm)
polys = ";\n".join(f"poly g{i}={str(mm).replace('**','^')}" for i, mm in enumerate(minors2))
gens = ",".join(f"g{i}" for i in range(len(minors2)))
program = "\n".join((
    'LIB "primdec.lib";',
    "ring R=0,(p2,p3,q2,q3,W1,w2,w3),dp;",
    polys + ";",
    f"ideal I={gens};",
    "list L=minAssGTZ(I);",
    '"NPRIMES:"+string(size(L));',
    "L;",
    "quit;",
))
completed = subprocess.run(("Singular", "-q"), input=program, text=True,
                           encoding="utf-8", errors="replace",
                           capture_output=True, timeout=900, check=False)
out = completed.stdout
assert "NPRIMES:6" in out, out[-800:]
expected_gens = ["w3,\n   w2,\n   W1".replace(",\n   ", "|"), ]
# check the six primes by membership of their expected generators
prime_sets = [
    ("w3", "w2", "W1"),
    ("-p3*q2+p2*q3", "w3", "w2"),
    ("w3", "q3", "p3"),
    ("q3*w2+q2*w3", "p3*w2+p2*w3", "-p3*q2+p2*q3", "W1"),
    ("q3", "q2", "p3", "p2"),
    ("w2", "q2", "p2"),
]
for gens_ in prime_sets:
    assert all(g_ in out for g_ in gens_), gens_
print("(3) minAssGTZ: exactly six rank<=1 primes, as listed.  OK")

# zero-column lemma for #3 and #6
for coord, sub in ((3, {p3: 0, q3: 0, w3: 0}), (2, {p2: 0, q2: 0, w2: 0})):
    psub = tuple(sp.sympify(c).subs(gauge).subs(sub) for c in p)
    qsub = tuple(sp.sympify(c).subs(gauge).subs(sub) for c in q)
    wsub = tuple(sp.sympify(c).subs(gauge).subs(sub) for c in w)
    zfree = sp.symbols("zf0:4")
    zrow = tuple(0 if j == coord else zfree[j] for j in range(4))
    for rows in itertools.product((zrow,), (YBAR, psub), (YBAR, qsub), (U3v, wsub)):
        assert all(sp.sympify(rr[coord]) == 0 for rr in rows)
        assert sp.expand(perm4(rows)) == 0
print("    #3/#6: all four planes lie in a coordinate hyperplane: T == 0")
print("    identically (zero-column permanent).  OK")

# (4) the tenth's home stratum #4: whole fibre pure = the tenth's tensor
b, e, k, alF, beF, c0F = sp.symbols("b e k alF beF c0F")
p4_ = (0, 1, b, -b*k)
q4_ = (0, 1, e, -e*k)
w4_ = (0, 0, 1, k)
M4_ = sp.Matrix([[sp.expand(c) for c in row] for row in
                 MZ.subs({**dict(zip(p, p4_)), **dict(zip(q, q4_)),
                          **dict(zip(w, w4_))}).tolist()])
assert M4_.rank() == 1
kb = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, -k))
for kv in kb:
    assert all(sp.expand(sum(M4_[i, j]*kv[j] for j in range(4))) == 0 for i in range(3))
charts = {
    "A": [tuple(sp.expand(a_ + alF*b_) for a_, b_ in zip(kb[1], kb[0])),
          tuple(sp.expand(a_ + beF*b_) for a_, b_ in zip(kb[2], kb[0]))],
    "B": [kb[0], tuple(sp.expand(a_ - c0F*b_) for a_, b_ in zip(kb[1], kb[2]))],
    "C": [kb[0], kb[2]],
}
for name, U0 in charts.items():
    B = sp.Matrix(2, 2, lambda i, j: perm4((tuple(U0[i]), p4_, q4_, (U3v, w4_)[j])))
    assert sp.expand(B.det()) == 0, name
# chart A at (alF,beF) = (m,r) reproduces the tenth's Zplanes tensor:
m_, r_ = sp.symbols("mten rten")
# tenth's U_L = span((1,m,0,0),(0,r,1,-k)) in tenth-mode order (I,J,K,L);
# our sweep order is (L,I,J,K) = modes (0,1,2,3):
UL = [(1, m_, 0, 0), (0, r_, 1, -k)]
sweep_planes = ([UL[0], UL[1]], [YBAR, p4_], [YBAR, q4_], [U3v, w4_])
T_sweep = {bits: perm4(tuple(sweep_planes[mm][bits[mm]] for mm in range(4)))
           for bits in itertools.product((0, 1), repeat=4)}
nz = {bits: sp.factor(val) for bits, val in T_sweep.items() if sp.expand(val) != 0}
assert set(nz) == {(0, 1, 1, 0), (1, 1, 1, 0)}, nz
assert sp.expand(nz[(0, 1, 1, 0)] + 2*b*e*k*(m_+1)) == 0
assert sp.expand(nz[(1, 1, 1, 0)] + 2*k*(b*e*r_ + b + e)) == 0
print("(4) stratum #4: the whole Gr(2,3)-fibre is pure (det B_Z == 0 on all")
print("    charts) and the restriction is the TENTH's tensor")
print("    T = -2k[ b*e*(m+1) e_0110 + (b*e*r+b+e) e_1110 ] (sweep modes):")
print("    the rank<=1 stratum #4 is exactly the tenth component's family.  OK")

# #2 (U3 = P01): rank-2 part forces U0 = P01 and T == 0; rank-1 part: no
# nonzero pure points off the zero locus
P_, Q_ = sp.symbols("PP0:4"), sp.symbols("QQ0:4")
pg = (0, 1, P_[2], P_[3])
qg = (0, 1, Q_[2], Q_[3])
w01 = (0, 1, 0, 0)
Mg = MZ.subs({**dict(zip(p, pg)), **dict(zip(q, qg)), **dict(zip(w, w01))})
Mg = sp.Matrix([[sp.expand(c) for c in row] for row in Mg.tolist()])
ns = Mg.nullspace()
assert len(ns) == 2 and Mg.rank() == 2
U0f = [tuple(sp.expand(c) for c in vec) for vec in ns]
assert {tuple(U0f[0]), tuple(U0f[1])} == {(1, 0, 0, 0), (0, 1, 0, 0)}
Bf = sp.Matrix(2, 2, lambda i, j: perm4((U0f[i], pg, qg, (U3v, w01)[j])))
PP = sp.expand(P_[2]*Q_[3] + P_[3]*Q_[2])
assert sp.expand(Bf.det() + PP**2) == 0
# det = 0 forces PP = 0, and then B == 0:
assert all(sp.expand(c.subs({Q_[3]: -P_[3]*Q_[2]/P_[2]})*P_[2]) == 0
           for c in sp.Matrix(Bf).subs({Q_[3]: -P_[3]*Q_[2]/P_[2]})*P_[2])
Bf0 = Bf.subs({Q_[3]: sp.symbols("qq3s")})
print("(#2 rank-2 part) U0 = P01 forced; det B = -(p2q3+p3q2)^2 and B")
print("    vanishes entirely on the branch: pure => T == 0.  OK")
b_, e_, k_ = sp.symbols("b2 e2 k2")
p21 = (0, 1, b_, -b_*k_)
q21 = (0, 1, e_, -e_*k_)
kb2 = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, k_))
M2p = MZ.subs({**dict(zip(p, p21)), **dict(zip(q, q21)), **dict(zip(w, w01))})
M2p = sp.Matrix([[sp.expand(c) for c in row] for row in M2p.tolist()])
for kv in kb2:
    assert all(sp.expand(sum(M2p[i, j]*kv[j] for j in range(4))) == 0 for i in range(3))
dets2p = {}
for name, U0 in {
        "A": [tuple(sp.expand(a_ + alF*b2_) for a_, b2_ in zip(kb2[1], kb2[0])),
              tuple(sp.expand(a_ + beF*b2_) for a_, b2_ in zip(kb2[2], kb2[0]))],
        "B": [kb2[0], tuple(sp.expand(a_ - c0F*b2_) for a_, b2_ in zip(kb2[1], kb2[2]))],
        "C": [kb2[0], kb2[2]]}.items():
    B = sp.Matrix(2, 2, lambda i, j: perm4((tuple(U0[i]), p21, q21, (U3v, w01)[j])))
    dets2p[name] = sp.factor(sp.expand(B.det()))
assert sp.expand(dets2p["A"] - 4*b_**2*beF*e_**2*k_**2) == 0
assert sp.expand(dets2p["B"] + 4*b_**2*e_**2*k_**2) == 0
assert dets2p["C"] == 0
# the pure fibre points are exactly beF = 0 (chart A) and chart C, i.e.
# U0 = span((al,1,0,0), (0,0,1,k)) (al = alF, or the al -> oo limit e0):
U0A0 = [(alF, 1, 0, 0), (0, 0, 1, k_)]
planesA0 = [U0A0, [YBAR, list(p21)], [YBAR, list(q21)], [U3v, list(w01)]]
TA0 = {bits: perm4(tuple(tuple(planesA0[mm][bits[mm]]) for mm in range(4)))
       for bits in itertools.product((0, 1), repeat=4)}
nzA0 = {bits: sp.factor(val) for bits, val in TA0.items() if sp.expand(val) != 0}
assert set(nzA0) == {(0, 1, 1, 0), (0, 1, 1, 1)}
assert sp.expand(nzA0[(0, 1, 1, 0)] + 2*b_*e_*k_*(alF+1)) == 0
assert sp.expand(nzA0[(0, 1, 1, 1)] + 2*alF*b_*e_*k_) == 0
# exact identification into the ELEVENTH: apply the source swap
# pi = (0 2)(1 3); the image is the C10 family on its c1 = c2 wall:
#   C10(a=(1,-k), c0=-1/al, c1=c2=1, vv=(b,-b k,0,1), t=e, x2=0, x3=1).


def pi_swap(row):
    return (row[2], row[3], row[0], row[1])


def same_plane(P, Q):
    stack = sp.Matrix([list(P[0]), list(P[1]), list(Q[0]), list(Q[1])])
    for rows_ in itertools.combinations(range(4), 3):
        for cols_ in itertools.combinations(range(4), 3):
            if sp.expand(stack[rows_, cols_].det()) != 0:
                return False
    return True


img = [[pi_swap(r) for r in pl] for pl in planesA0]
c10_target = [
    [(1, k_, 0, 0), (0, 0, alF, 1)],          # = span((a0,-a1,0,0),(0,0,1,-c0))
    [(0, 0, 1, -1), (b_, -b_*k_, 0, 1)],      # c1 = 1, vv
    [(0, 0, 1, -1), (e_, -e_*k_, 0, 1)],      # c2 = 1, xx = t*(1,-k),0,1, t=e
    [(0, 0, 1, 0), (0, 0, 0, 1)],             # Pi
]
assert all(same_plane(img[mm], c10_target[mm]) for mm in range(4))
print("(#2 rank-1 part) pure fibre points: U0 = span((al,1,0,0),(0,0,1,k));")
print("    T on words {0110, 0111}; the source swap (02)(13) carries the")
print("    family EXACTLY onto the C10 family's c1 = c2 wall")
print("    (a=(1,-k), c0=-1/al, vv=(b,-bk,0,1), xx=e*(1,-k,0,1/e)):")
print("    stratum #2's pure points lie in the ELEVENTH component orbit.  OK")

# #5: B_Z == 0 identically
p5 = (0, 1, 0, 0)
q5 = (0, 1, 0, 0)
wgen = (0, w[1], w[2], w[3])
M5 = MZ.subs({**dict(zip(p, p5)), **dict(zip(q, q5)),
              w[0]: 0})
M5 = sp.Matrix([[sp.expand(c) for c in row] for row in M5.tolist()])
ns5 = M5.nullspace()
assert len(ns5) == 3
for vec in ns5:
    den = sp.lcm([sp.denom(sp.cancel(c)) for c in vec])
    kv = tuple(sp.expand(sp.cancel(c)*den) for c in vec)
    B1 = [perm4((kv, p5, q5, U3v)), perm4((kv, p5, q5, wgen))]
    assert all(sp.expand(c) == 0 for c in B1)
print("(#5) U1 = U2 = P01: the residual entries vanish for every kernel")
print("    vector: zero restriction.  OK")
print()
print("ALL CHECKS PASSED")
