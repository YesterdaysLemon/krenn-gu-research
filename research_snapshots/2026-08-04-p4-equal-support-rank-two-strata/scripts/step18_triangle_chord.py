#!/usr/bin/env python3
"""Triangle stratum: rank Lambda == 2 identically on kappa^2 = -n2(n3-1)(n2-n3);
left-kernel cubics and the chord condition (resultant)."""
import itertools, json, pathlib, sympy as sp

kappa, n2, n3 = sp.symbols("kappa n2 n3")
rsym = sp.Symbol("r")
tw = {eval(k): sp.sympify(v) for k, v in json.loads(pathlib.Path("triangle_data.json").read_text()).items()}
p = sp.symbols("p0:4")
Lam = sp.zeros(4, 4)
for w in range(4):
    for j in range(4):
        Lam[w, j] = sp.expand(sp.diff(tw[(0, w)], p[j]))

krel = kappa**2 + n2*(n3-1)*(n2-n3)

def kred(expr):
    """reduce modulo kappa^2 = -n2(n3-1)(n2-n3)"""
    return sp.expand(sp.rem(sp.Poly(sp.expand(expr), kappa), sp.Poly(krel, kappa)).as_expr())

# (i) all 3x3 minors vanish mod the relation
all0 = True
for rows in itertools.combinations(range(4), 3):
    for cols in itertools.combinations(range(4), 3):
        m = Lam[rows, cols].det()
        if sp.simplify(kred(m)) != 0:
            all0 = False
            print("nonzero 3x3 minor", rows, cols)
print("all 3x3 minors of Lambda vanish on the stratum:", all0)

# (ii) left kernel symbolically: solve phi^T Lam = 0 mod krel.
# use two covectors from adjoint-style construction: rows of adj won't work at rank 2;
# instead solve linear system over the quotient field: treat kappa algebraic.
K = sp.QQ.algebraic_field if False else None
# brute: find covectors with entries polynomial in (kappa,n2,n3):
phi = sp.symbols("f0:4")
eqsys = [kred(sum(phi[i]*Lam[i, j] for i in range(4))) for j in range(4)]
# write as linear system in phi with coefficients in Q(n2,n3)[kappa]/(krel):
# each coefficient is c0 + c1*kappa; a covector may need kappa-linear entries.
g = sp.symbols("g0:8")
phi_k = [g[2*i] + g[2*i+1]*kappa for i in range(4)]
eqsys = [kred(sum(phi_k[i]*Lam[i, j] for i in range(4))) for j in range(4)]
lin = []
for e_ in eqsys:
    pe = sp.Poly(e_, kappa)
    for c_ in [pe.coeff_monomial(1), pe.coeff_monomial(kappa)]:
        lin.append(sp.expand(c_))
M8 = sp.Matrix([[sp.expand(sp.diff(l_, gg)) for gg in g] for l_ in lin])
M8 = sp.Matrix([[sp.cancel(c) for c in row] for row in M8.tolist()])
nsp = M8.nullspace()
print("left-kernel solution dim over the g-parametrization:", len(nsp))
covs = []
for vec in nsp[:4]:
    cv = [sp.cancel(sp.together(vec[2*i] + vec[2*i+1]*kappa)) for i in range(4)]
    # verify
    ok = all(sp.simplify(kred(sp.expand(sum(cv[i]*Lam[i, j] for i in range(4))))) == 0 for j in range(4))
    if ok and any(sp.simplify(c_) != 0 for c_ in cv):
        covs.append(cv)
print("verified covectors:", len(covs))
cubics = []
for cv in covs[:3]:
    cub = sp.expand(kred(sp.expand(sum(cv[i]*rsym**i for i in range(4)))))
    cub = sp.cancel(sp.together(cub))
    cubics.append(sp.numer(cub))
# pick two independent cubics and take resultant in r
seen = []
for cub in cubics:
    if all(sp.simplify(sp.expand(cub*sp.LC(sp.Poly(c2, rsym)) - c2*sp.LC(sp.Poly(cub, rsym)))) != 0 for c2 in seen) or not seen:
        seen.append(cub)
print("independent section polynomials:", len(seen))
if len(seen) >= 2:
    R = sp.resultant(sp.Poly(seen[0], rsym), sp.Poly(seen[1], rsym))
    R = sp.factor(kred(sp.expand(R)))
    print("chord resultant R (mod stratum) =", R)
    pathlib.Path("triangle_chord.json").write_text(json.dumps(
        {"cubic1": str(seen[0]), "cubic2": str(seen[1]), "R": str(R)}, indent=1))
