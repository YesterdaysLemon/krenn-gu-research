#!/usr/bin/env python3
"""RESOLUTION OF TAIL 1: the Zc wall lies in the SEVENTH component (exact).

The census-thirteen sweep (s09/s13) left the ambient component of the Zc
branches open: profile (3,3,2,4,3,3), rank-2 pair edge at {0,3}, family
tangent 5, incidence tangent 7 (doubly singular), five-slice `ds` timed
out; the sieve left 'a wall of the seventh' or 'a new component'.

THIS SCRIPT CLOSES THE TAIL EXACTLY: the Zc1 family is the image of the
b = e wall of the SEVENTH component's parametrized family under an
explicit census symmetry.  No slice computation is needed.

The seventh component (P4_SIX_DIMENSIONAL_PURE_COMPONENT.md), with the
source torus diag(t0,t1,t2,1) (coordinates scaled v |-> (t0 v0, t1 v1,
t2 v2, v3)) and h = a + c - d:

    S0 = span((t0,0,0,-1),(0,0,t2,1)),
    S1 = span((t0,t1*b,0,1-b*h),(0,t1*e,t2,1-e*h)),
    S2 = span((t0,0,-t2,0),(0,t1,-t2*(a+c),-d)),
    S3 = span((t0,0,0,1),(0,0,t2,-1)).

The Zc1 family (s04/s09/s13; sweep modes (0,1,2,3) = (U0, ybar-p,
ybar-q, u3-w); Wc = -(p3+q3) w2 / (p2 q3 + p3 q2); w2 scales out of the
planes projectively, so put s := -Wc/w2 = (p3+q3)/(p2 q3 + p3 q2)):

    U0 = span((1,1,0,0), (-s,0,1,0)),
    U1 = span((1,-1,0,0), (0,1,p2,p3)),
    U2 = span((1,-1,0,0), (0,1,q2,q3)),
    U3 = span((1,1,0,0), (0,-s,1,0)).

THE IDENTIFICATION.  Apply to the seventh's family the census symmetry

    g = (mode identity) o (source relocation pi: 0->0, 1->3, 2->1, 3->2,
         i.e. (v0,v1,v2,v3) |-> (v0, v2, v3, v1))

and substitute the parameter values (A := a + c is a free gauge, set
a = 1, c = 0; all rational in (p2,p3,q2,q3)):

    b = e = -p3/q3,          t0 = t2 = s = (p3+q3)/(p2 q3 + p3 q2),
    d = s*q2,                t1 = -s*q3.

Then g(S_m) = U_m for m = 0,1,2,3 IDENTICALLY over Q(p2,p3,q2,q3): the
whole Zc1 family (dense chart q3 != 0, p3+q3 != 0, p2 q3 + p3 q2 != 0,
w2 != 0) consists of images of seventh-family points.  Since the
seventh component is the closure of its parametrized family, and census
images of components are closed,

    closure(F_Zc1)  is contained in  g(seventh component),

and Zc2 = (01)-source-swap image of Zc1 (s09) lies in ((01) o g)(seventh).
The restriction at the matched parameters is nonzero (both seventh words
carry the factor 1 - b(a+c) = (p3+q3)/q3 != 0 on the chart), matching
Zc's nonzero single-word tensor.

VERDICT: the Zc wall is a WALL OF THE SEVENTH component; NO fourteenth
component arises from the Zc branches.  (Consistency: the seventh is
six-dimensional, so the local dimension of the pure locus at the Zc
sample is >= 6; a five-hyperplane slice there has local dimension >= 1,
which is why the s13 five-slice could never return 0.  The doubly
singular incidence tangent 7 > 6 remains an honest tangent gap, exactly
as at the tenth's A/B walls.)"""
import itertools, sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


def same_plane(P, Q):
    """Exact projective equality of two row-span 2-planes."""
    stack = sp.Matrix([list(P[0]), list(P[1]), list(Q[0]), list(Q[1])])
    for rows in itertools.combinations(range(4), 3):
        for cols in itertools.combinations(range(4), 3):
            if sp.simplify(sp.together(stack[rows, cols].det())) != 0:
                return False
    # fail-closed: each pair must itself be a genuine 2-plane
    return (sp.Matrix([list(P[0]), list(P[1])]).rank() == 2
            and sp.Matrix([list(Q[0]), list(Q[1])]).rank() == 2)


# ---------------------------------------------------------------- seventh ----
a, c, d, b, e, t0, t1, t2 = sp.symbols("a c d b e t0 t1 t2")
h = a + c - d


def seventh_planes(sub=None):
    S = [
        [(1, 0, 0, -1), (0, 0, 1, 1)],
        [(1, b, 0, 1 - b*h), (0, e, 1, 1 - e*h)],
        [(1, 0, -1, 0), (0, 1, -a - c, -d)],
        [(1, 0, 0, 1), (0, 0, 1, -1)],
    ]
    out = []
    for pl in S:
        rows = []
        for row in pl:
            row = tuple(sp.sympify(x) for x in row)
            if sub:
                row = tuple(sp.together(x.subs(sub)) for x in row)
            rows.append((sp.together(t0.subs(sub) if sub else t0)*row[0],
                         (t1.subs(sub) if sub else t1)*row[1],
                         (t2.subs(sub) if sub else t2)*row[2], row[3]))
        out.append(rows)
    return out


# replay the seventh's identical purity + support (torus off; support is
# torus-invariant since the torus scales T word-by-word):
Tsev = {bits: perm4(tuple(tuple(sp.sympify(x) for x in
                                seventh_planes({t0: 1, t1: 1, t2: 1})[m][bits[m]])
                          for m in range(4)))
        for bits in itertools.product((0, 1), repeat=4)}
nz = {bits: sp.factor(v) for bits, v in Tsev.items() if sp.expand(v) != 0}
assert set(nz) == {(1, 0, 1, 0), (1, 1, 1, 0)}, nz
assert sp.expand(nz[(1, 0, 1, 0)] - 2*(1 - b*(a + c))) == 0
assert sp.expand(nz[(1, 1, 1, 0)] - 2*(1 - e*(a + c))) == 0
for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
    m = sp.zeros(4, 4)
    for bits in itertools.product((0, 1), repeat=4):
        m[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = Tsev[bits]
    for r1, r2 in itertools.combinations(range(4), 2):
        for c1, c2 in itertools.combinations(range(4), 2):
            assert sp.expand(m[r1, c1]*m[r2, c2] - m[r1, c2]*m[r2, c1]) == 0
print("seventh family replay: identically pure, support {1010, 1110},")
print("  values 2(1-b(a+c)), 2(1-e(a+c)).  OK")

# ------------------------------------------------------------------- Zc1 ----
p2, p3, q2, q3, w2 = sp.symbols("p2 p3 q2 q3 w2")
P = p2*q3 + p3*q2
Wc = -(p3 + q3)*w2/P
s_ = -Wc/w2                      # = (p3+q3)/P
assert sp.simplify(s_ - (p3 + q3)/P) == 0
YBAR = (1, -1, 0, 0)
U3v = (1, 1, 0, 0)
Zc1_full = [
    [U3v, (Wc, 0, w2, 0)],
    [YBAR, (0, 1, p2, p3)],
    [YBAR, (0, 1, q2, q3)],
    [U3v, (0, Wc, w2, 0)],
]
# w2 scales out projectively:
Zc1 = [
    [U3v, (-s_, 0, 1, 0)],
    [YBAR, (0, 1, p2, p3)],
    [YBAR, (0, 1, q2, q3)],
    [U3v, (0, -s_, 1, 0)],
]
assert all(same_plane(Zc1_full[m], Zc1[m]) for m in range(4))
print("Zc1 planes: w2 scales out projectively (planes depend only on")
print("  (p2,p3,q2,q3) through s = (p3+q3)/(p2 q3 + p3 q2)).  OK")

# ------------------------------------------------- the exact identification -
SUB = {a: 1, c: 0, d: s_*q2, b: -p3/q3, e: -p3/q3, t0: s_, t1: -s_*q3, t2: s_}


def pi_reloc(row):
    """source relocation pi: (v0,v1,v2,v3) |-> (v0,v2,v3,v1)."""
    return (row[0], row[2], row[3], row[1])


S_at = seventh_planes(SUB)
G = [[pi_reloc(tuple(sp.together(sp.sympify(x)) for x in row)) for row in pl]
     for pl in S_at]
for m in range(4):
    assert same_plane(G[m], Zc1[m]), ("mode", m)
print("IDENTIFICATION: g(S_m) == U_m(Zc1) for m = 0,1,2,3 identically")
print("  over Q(p2,p3,q2,q3) with g = (source relocation (v0,v1,v2,v3)")
print("  |-> (v0,v2,v3,v1)) o torus(t0=t2=s, t1=-s q3), at the seventh's")
print("  parameters a=1, c=0, d=s q2, b=e=-p3/q3.  OK")

# on the wall b = e the seventh's tensor is nonzero iff 1 - b(a+c) != 0:
val = sp.simplify((1 - b*(a + c)).subs(SUB))
assert sp.simplify(val - (p3 + q3)/q3) == 0
print("  nonzeroness on the wall: 1 - b(a+c) = (p3+q3)/q3 != 0 on the Zc")
print("  chart (p3+q3 = 0 is the degenerate s = 0 boundary).  OK")

# sanity cross-check at the s13 sample (p2,p3,q2,q3,w2) = (2,3,5,7,1):
smp = {p2: 2, p3: 3, q2: 5, q3: 7, w2: 1}
G_s = [[tuple(sp.nsimplify(sp.cancel(x.subs(smp))) for x in row) for row in pl]
       for pl in G]
Z_s = [[tuple(sp.nsimplify(sp.cancel(sp.sympify(x).subs(smp))) for x in row)
        for row in pl] for pl in Zc1_full]
assert all(same_plane(G_s[m], Z_s[m]) for m in range(4))
T_s = {bits: perm4(tuple(tuple(Z_s[m][bits[m]]) for m in range(4)))
       for bits in itertools.product((0, 1), repeat=4)}
nz_s = {bits for bits, v in T_s.items() if v != 0}
assert nz_s == {(0, 1, 1, 0)}
print("  numeric cross-check at the s13 sample (2,3,5,7,1): planes match,")
print("  nonzero pure single-word tensor e_0110.  OK")

# ------------------------------------------------------------- Zc2 mirror ---
swap01 = lambda row: (row[1], row[0], row[2], row[3])
Zc2 = [
    [U3v, (-Wc, 0, w2, 0)],
    [YBAR, (0, 1, p2, p3)],
    [YBAR, (0, 1, q2, q3)],
    [U3v, (0, -Wc, w2, 0)],
]
img = [[swap01(tuple(sp.sympify(x) for x in row)) for row in pl] for pl in Zc1_full]
assert all(same_plane(img[m], Zc2[m]) for m in range(4))
print("Zc2 = (01)-source-swap image of Zc1 (replayed): Zc2 lies in")
print("  ((01) o g)(seventh component).  OK")
print()
print("VERDICT (tail 1 CLOSED): closure(F_Zc1) and closure(F_Zc2) are")
print("contained in census images of the SEVENTH component -- the Zc wall")
print("is the seventh's b = e wall; NO fourteenth component arises here.")
print("(Corollary: the local pure-locus dimension at the Zc sample is >= 6,")
print("so the s13 five-slice could never have local dimension 0; its")
print("timeout is now moot.)")
print()
print("ALL CHECKS PASSED")
