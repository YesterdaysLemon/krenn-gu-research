#!/usr/bin/env python3
"""Deliverable 1: the eighth component's closure in the disjoint chart.

Conventions are those of verify_p4_inout_path_stratum_working_note.py:
squarefree ring R=C[X0..X3]/(Xi^2); disjoint chart normalization
u1=(0,0,1,-1), y3=(0,0,1,1), u3=(1,1,0,0), y2=(1,-1,0,0),
U1=span(u1,v), U2=span(y2,x), U3=span(y3,u3), U0=ker of the covector
matrix M(v,x).  Eighth-component embedding (coordinate swap (02)(13),
mode map (0,1,2,3)<-(2,1,0,3), torus t3=-t2, t1=t0):
   v_img=(f+phi, f-phi, -a*f*t+t, a*f*t+t),
   x_img=(0, 2, (a+b)*t, (-a+b)*t)   modulo   Phi=0.

Certified statements (all asserted below):
 (1) M(v,x)*u1 == 0 identically  =>  u1 lies in ker M for EVERY (v,x);
     equivalently the Pluecker coordinate p01(ker M) == 0 identically.
 (2) detB = (v2+v3)*S*Q6 exactly, S the symmetric pivot cofactor and Q6
     an irreducible sextic (Singular factorize).
 (3) Elimination of (a,b,f,phi,t, mu,nu,lam_v,lam_x) from the graph
     ideal of the gauge-saturated embedding gives the PRINCIPAL ideal
     J8 = (Q6): the Zariski closure of the eighth's (v,x)-image is
     exactly the irreducible sextic hypersurface V(Q6).
 (4) Q6 vanishes identically on the deep stratum v3=-v2, x3=-x2.
     Hence BOTH deep branches (A: alpha=beta; B: v0+v1=0) lie in V(J8):
     the (v,x)-level test does NOT separate them from the eighth.
 (5) The separation happens at the U0 level: every tuple in the
     incidence closure of the rank-2 strata (open stratum + pivot
     sheets) has u1 in U0 -- a closed condition -- while the deep-branch
     tuples U0=span(k1+alpha*k3, k2+beta*k3) NEVER contain
     u1=k3=(0,0,1,-1) (their Pluecker p01 = 1).  So no deep-branch
     point (any finite alpha, beta) is a limit of chart open-stratum
     tuples; in particular the eighth's chart closure meets the deep
     stratum only inside the p01=0 boundary of the U0 Grassmannian.
"""
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

import itertools
import subprocess
import sympy as sp

v = sp.symbols("v0:4")
x = sp.symbols("x0:4")
U1_A = (0, 0, 1, -1)
Y3 = (0, 0, 1, 1)
U3_disj = (1, 1, 0, 0)
Y2_disj = (1, -1, 0, 0)
COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
COMPLEMENT = {ab: tuple(sorted(set(range(4)) - set(ab))) for ab in COORD_PAIRS}
PERMS4 = tuple(itertools.permutations(range(4)))


def rmul(u, w):
    return {ab: sp.expand(u[ab[0]] * w[ab[1]] + u[ab[1]] * w[ab[0]]) for ab in COORD_PAIRS}


def pairing(P, Q):
    return sp.expand(sum(P[ab] * Q[COMPLEMENT[ab]] for ab in COORD_PAIRS))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[kk][pi[kk]] for kk in range(4)) for pi in PERMS4))


def run_singular(program):
    cp = subprocess.run(("Singular", "-q"), input=program, text=True,
                        capture_output=True, timeout=1500, check=False)
    assert cp.returncode == 0, (cp.returncode, cp.stdout[-2000:], cp.stderr[-2000:])
    return cp.stdout


# ---------- covector matrix and identity (1) ----------
zsym = sp.symbols("z0:4")
rows = []
for cpair in (rmul(Y2_disj, Y3), rmul(list(x), Y3)):
    zw = rmul(list(zsym), list(v))
    form = pairing(zw, cpair)
    rows.append([sp.expand(sp.diff(form, zi)) for zi in zsym])
M = sp.Matrix(rows)
Mu1 = M * sp.Matrix(4, 1, list(U1_A))
assert all(sp.expand(entry) == 0 for entry in Mu1), "M*u1 must vanish identically"

minors = {}
for a_, b_ in itertools.combinations(range(4), 2):
    minors[(a_, b_)] = sp.expand(M[0, a_] * M[1, b_] - M[0, b_] * M[1, a_])
pivot = minors[(0, 1)]
S = sp.expand((v[2] + v[3]) * (x[0] + x[1]) + (v[0] + v[1]) * (x[2] + x[3]))
assert sp.expand(pivot + (v[2] + v[3]) * S) == 0
# columns 2 and 3 of M coincide (same fact as (1)); hence minor (2,3)=0 and
# the Pluecker p01 of ker M = span(w2,w3) is  P*m23 = 0 identically:
assert minors[(2, 3)] == 0
assert sp.expand(minors[(0, 2)] - minors[(0, 3)]) == 0
assert sp.expand(minors[(1, 2)] - minors[(1, 3)]) == 0
w2 = (minors[(1, 2)], -minors[(0, 2)], pivot, 0)
w3 = (minors[(1, 3)], -minors[(0, 3)], 0, pivot)
p01_kernel = sp.expand(w2[0] * w3[1] - w2[1] * w3[0])
assert sp.expand(p01_kernel - pivot * minors[(2, 3)]) == 0  # = 0 identically
# and w2, w3 really span ker M where pivot != 0:
for wvec in (w2, w3):
    for r_ in range(2):
        assert sp.expand(sum(M[r_, c_] * wvec[c_] for c_ in range(4))) == 0

# ---------- active determinant and factorization (2) ----------
B = sp.zeros(2, 2)
for i0, u0row in enumerate((w2, w3)):
    for i1, u1row in enumerate((U1_A, tuple(v))):
        B[i0, i1] = perm4((tuple(u0row), u1row, tuple(x), U3_disj))
detB = sp.expand(B.det())
Q6, rem = sp.div(sp.cancel(detB / (v[2] + v[3])), S, v[2])
assert rem == 0
Q6 = sp.expand(Q6)
assert sp.expand(detB - (v[2] + v[3]) * S * Q6) == 0

# Q6 irreducible (Singular factorize returns a single nontrivial factor)
out = run_singular("\n".join((
    "ring R=0,(v0,v1,v2,v3,x0,x1,x2,x3),dp;",
    f"poly q={str(Q6).replace('**', '^')};",
    "list L=factorize(q);",
    '"CODEX_NFACTORS:"+string(size(L[1])-1);',
    "quit;")))
assert "CODEX_NFACTORS:1" in out, out

# ---------- elimination (3): J8 = (Q6) ----------
elim_program = "\n".join((
    "ring R=0,(a,b,f,p,t,mu,nu,lv,lx,v0,v1,v2,v3,x0,x1,x2,x3),dp;",
    "ideal I=",
    "  v0-lv*(f+p),",
    "  v1-lv*(f-p),",
    "  v2-lv*(-a*f*t+t+mu),",
    "  v3-lv*(a*f*t+t-mu),",
    "  x0-lx*(nu),",
    "  x1-lx*(2-nu),",
    "  x2-lx*(a+b)*t,",
    "  x3-lx*(-a+b)*t,",
    "  a^2*b*f*p^2+a^2*f^2-b^2*f^2+b^2*p^2-b*f-1;",
    "ideal J=eliminate(I,a*b*f*p*t*mu*nu*lv*lx);",
    '"CODEX_NGEN:"+string(size(J));',
    "J;",
    "quit;",
))
out = run_singular(elim_program)
assert "CODEX_NGEN:1" in out, out
gen_text = out.split("J[1]=")[1].splitlines()[0].strip()
symmap = {f"v{i}": v[i] for i in range(4)}
symmap.update({f"x{i}": x[i] for i in range(4)})
J1 = sp.sympify(gen_text.replace("^", "**"), locals=symmap)
assert sp.expand(J1 + Q6) == 0, "elimination generator must be -Q6"
print("J8 = (Q6): principal, generated by the irreducible sextic Q6 (checked)")

# ---------- deep stratum (4) ----------
deep = {v[3]: -v[2], x[3]: -x[2]}
assert sp.expand(Q6.subs(deep)) == 0
assert sp.expand(S.subs(deep)) == 0 and sp.expand(pivot.subs(deep)) == 0
print("Q6|deep == 0: the whole deep stratum v3=-v2, x3=-x2 lies in V(J8);")
print("  branch A (alpha=beta) and branch B (v0+v1=0) both PASS the (v,x)-level test")

# generic-sample double check on both branches
sampleA = {v[0]: 3, v[1]: 5, v[2]: 7, v[3]: -7, x[0]: 2, x[1]: -9, x[2]: 4, x[3]: -4}
sampleB = {v[0]: 2, v[1]: -2, v[2]: 5, v[3]: -5, x[0]: 3, x[1]: 7, x[2]: 4, x[3]: -4}
assert Q6.subs(sampleA) == 0 and Q6.subs(sampleB) == 0

# ---------- U0-level obstruction (5) ----------
alpha, beta = sp.symbols("alpha beta")
k1 = (1, 0, 0, 0)
k2 = (0, 1, 0, 0)
k3 = (0, 0, 1, -1)  # = u1
u0a = tuple(k1[j] + alpha * k3[j] for j in range(4))
u0b = tuple(k2[j] + beta * k3[j] for j in range(4))
# p01 of the branch U0:
p01_branch = sp.expand(u0a[0] * u0b[1] - u0a[1] * u0b[0])
assert p01_branch == 1
# u1 in span(u0a,u0b) would force rank 2 of the 3x4 stack; show rank 3 always:
stack = sp.Matrix([list(u0a), list(u0b), list(U1_A)])
minors3 = [sp.expand(stack[:, cols].det())
           for cols in itertools.combinations(range(4), 3)]
# the (0,1,2) minor equals 1 identically:
assert sp.expand(stack[:, (0, 1, 2)].det() - 1) == 0
print("U0-level obstruction: p01(ker M) == 0 identically on every rank-2 chart")
print("  stratum (u1 in U0 is closed under limits), while the deep-branch")
print("  U0 = span(k1+alpha*k3, k2+beta*k3) has p01 = 1 and never contains u1.")
print("  => no deep-branch point (any finite alpha,beta; in particular branch A")
print("     and branch B) is a limit of the chart's rank-2 pure strata, hence")
print("     none lies in the eighth component's chart closure.")

# the eighth's own chart-U0 always contains u1: image of its U2-plane row
# x2^(8)=(1,1,0,0) under swap (02)(13) + torus(1,1,t,-t) is (0,0,t,-t) ~ u1:
a8, b8, f8, p8, t8 = sp.symbols("a8 b8 f8 p8 t8")
x2_img = (0 * a8, 0 * a8, t8, -t8)  # sigma_torus((1,1,0,0))
assert tuple(sp.expand(x2_img[j] - t8 * U1_A[j]) for j in range(4)) == (0, 0, 0, 0)
print("consistency: the eighth family's chart-U0 contains sigma(x2)=t*u1 exactly.")
print("ALL CHECKS PASSED")
