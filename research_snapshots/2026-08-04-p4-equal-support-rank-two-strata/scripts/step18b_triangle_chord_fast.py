#!/usr/bin/env python3
"""Fast, check-only replay of the triangle chord conclusion (step18).

step18 as written solves an 8x8 left-kernel system over the function
field Q(n2,n3) (sympy nullspace + simplify); local replays exceeded
2400 s.  The conclusions the note actually uses are:

  (i)  rank Lambda <= 2 identically on the stratum surface
       kappa^2 = -n2 (n3-1)(n2-n3)   (all 3x3 minors vanish);
  (ii) at the rational stratum point (n2,n3,kappa) = (2,3,2) the rank
       is exactly two, and the two independent left-kernel section
       polynomials in the pencil coordinate r share NO root, r = oo
       included: the chord condition is a PROPER closed condition on
       the irreducible stratum surface.

(i) is symbolic and cheap (it is step18's first checkpoint, replayed
green); (ii) is exact rational arithmetic at the sample, replacing the
function-field solve by a specialize-then-solve.  Properness of a
closed condition on an irreducible surface needs exactly one witness
point, so (i)+(ii) support the note's consequence in full:
pure points in the all-rank-two triangle chart live over a proper
chord curve, giving walls of dimension <= 4 and NO component."""
import itertools, json, pathlib, sympy as sp

kappa, n2, n3 = sp.symbols("kappa n2 n3")
rsym = sp.Symbol("r")
HERE = pathlib.Path(__file__).resolve().parent
tw = {eval(k): sp.sympify(v)
      for k, v in json.loads((HERE / "triangle_data.json").read_text()).items()}
p = sp.symbols("p0:4")
Lam = sp.zeros(4, 4)
for w in range(4):
    for j in range(4):
        Lam[w, j] = sp.expand(sp.diff(tw[(0, w)], p[j]))

krel = kappa**2 + n2*(n3-1)*(n2-n3)

def kred(expr):
    return sp.expand(sp.rem(sp.Poly(sp.expand(expr), kappa),
                            sp.Poly(krel, kappa)).as_expr())

# (i) all 3x3 minors of Lambda vanish modulo the stratum relation
for rows in itertools.combinations(range(4), 3):
    for cols in itertools.combinations(range(4), 3):
        assert sp.simplify(kred(Lam[rows, cols].det())) == 0, (rows, cols)
print("(i) all 3x3 minors of Lambda vanish on the stratum: True")

# (ii) the rational stratum point (n2,n3,kappa) = (2,3,2)
point = {n2: 2, n3: 3, kappa: 2}
assert sp.simplify(krel.subs(point)) == 0, "sample not on the stratum"
L = sp.Matrix(4, 4, lambda i, j: sp.nsimplify(Lam[i, j].subs(point)))
assert L.rank() == 2, L.rank()
print("(ii) rank Lambda at (2,3,2) is exactly 2: P(Im Lambda) is a line")

kernel = L.T.nullspace()
assert len(kernel) == 2
sections = []
for vec in kernel:
    cub = sp.expand(sum(sp.nsimplify(vec[i])*rsym**i for i in range(4)))
    den = sp.lcm([sp.denom(c) for c in sp.Poly(cub, rsym).all_coeffs()])
    sections.append(sp.expand(cub*den))
# normalize the pair to the primitive echelon basis of the kernel span
basis = sp.Matrix([[sp.Poly(s_, rsym).coeff_monomial(rsym**k) for k in range(4)]
                   for s_ in sections]).rref()[0]
norm = []
for i in range(2):
    row = [sp.nsimplify(basis[i, k]) for k in range(4)]
    den = sp.lcm([sp.denom(c) for c in row])
    norm.append(sp.expand(sum(c*den*rsym**k for k, c in enumerate(row))))
print("section polynomials (echelon):", [str(s_) for s_ in norm])
# the note records the basis {r^2-3r+2, r^3-9r+9} of the same kernel
# span; assert span equality (common roots depend only on the span)
coeff_rows = lambda polys: sp.Matrix(
    [[sp.Poly(s_, rsym).coeff_monomial(rsym**k) for k in range(4)]
     for s_ in polys])
recorded = [rsym**2 - 3*rsym + 2, rsym**3 - 9*rsym + 9]
assert coeff_rows(norm).rank() == 2
assert coeff_rows(norm + recorded).rank() == 2, "recorded pair not in span"
print("recorded pair {r^2-3r+2, r^3-9r+9} spans the SAME kernel")
# no common affine root of the span: resultant of a basis is nonzero
R = sp.resultant(sp.Poly(norm[0], rsym), sp.Poly(norm[1], rsym))
assert R != 0, "sections share an affine root"
print("affine resultant of the echelon basis:", R, "(nonzero)")
# r = oo: a common root at [1:0] of the degree-3 binary forms needs
# both r^3-coefficients to vanish; both echelon leaders are nonzero.
lead = [sp.Poly(s_, rsym).coeff_monomial(rsym**3) for s_ in norm]
assert all(c_ != 0 for c_ in lead), lead
print("no common root at r = oo (leading coefficients %s)" % (lead,))
print()
print("CHORD CONDITION IS PROPER at the witness (2,3,2): the")
print("all-rank-two triangle carries pure points only over a proper")
print("chord curve -> dimension <= 4 walls, NO component.")
