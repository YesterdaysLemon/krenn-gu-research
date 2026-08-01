# The `p+q=0` valuative boundary of component twenty

## Status

**DERIVED after independent replay.**  The corrected wedge, invariant
valuation formulas, all four min-plus equivalences, and the displayed charts'
pure tensors and pair profiles have independent exact replays.  The stronger
claim that arbitrary diagonal source-torus arcs exhaust exactly these charts
and the cited lower-pair placements remains derived rather than independently
verified.

This is a `P_4` valuative classification.  It is **not** an `H31` or `H22`
boundary exclusion, does not prove that the two displayed charts equal any
older named component orbit, and does not resolve the global Krenn--Gu
conjecture.

## Normalized family and the corrected mode-zero wedge

Put

```text
delta=p+q,                  s=p-q+1,                  e=X0.
```

Use

```text
alpha0=(0,-p(p+1),q(q-1),s),
beta0 =(-s,-delta,delta,0),

alpha1=e,                  beta1=(0,p+1,q-1,1),
alpha2=e,                  beta2=(0,p,q,1),
alpha3=(1,1,1,0),          beta3=e.                  (1)
```

The squarefree permanent has only

```text
T_1111=2 delta s.                                      (2)
```

For a diagonal source torus

```text
D=diag(tau0,tau1,tau2,tau3),
xi=v(taui),                  x3=0,
ai=v(D alpha_i),             ui=v(D alpha_i wedge D beta_i),
```

the row-normalization-invariant valuation of the surviving pure scalar is

```text
E=v(2 delta s)+x0+x1+x2+sum_i(ai-ui).                (3)
```

Thus `E=0` is necessary and sufficient for a nonzero pure limit after
projective ambient normalization; `E>0` gives the zero restricted tensor.

The essential correction is that mode zero uses the wedge of the selected
pure rows, not raw Pluecker coordinates of a convenient plane basis:

```text
alpha0 wedge beta0 =
 (-p(p+1)s, q(q-1)s, s^2, -delta^2 s, delta s, -delta s)
```

in coordinate order `(01,02,03,12,13,23)`.  Omitting the extra `delta*s`
factors gives spurious negative tensor valuations.

## Finite generic centre: the complete min-plus split

Assume

```text
p -> a,             q -> -a,
a not in {0,-1,-1/2},
d=v(delta)>0.
```

Define

```text
m=min(x1,x2,0),
n=min(x1,x2),
ell=min(x1+x2+d,x1,x2).                              (4)
```

Substituting the valuations of (1) and the corrected wedge into (3) gives

```text
E=d+x1+x2-m+min(x0,n)-n-min(x0+m,d+ell).             (5)
```

The complete 72-cell linear case split of the five minima proves

```text
E=0
iff
x1=x2=y,             -d<=y<=0,             x0>=d.   (6)
```

The primary verifier constructs every linear counterexample query explicitly
and checks exact rational unsatisfiability with a returned proof object,
including `E<0`, failure of necessity, and failure of sufficiency.  Its output
records digests rather than standalone proof artifacts.  It also checks the
sufficiency branch directly:
on (6), `m=n=ell=y`, `min(x0,n)=y`, and
`min(x0+m,d+ell)=d+y`, so (5) is identically zero.

## Negative equal weights are lower-pair

For `y<0`, residue-leading coefficients `c1,c2` give

```text
U1=U2=<e,c1 A-c2 B>.                                  (7)
```

Hence `dim(U1 U2)=2`.  This is not a new all-pair-rank chart.  The replayed
rank-two-pair and tangent-purity classifications place the support-two
tangent strata in the old six-dimensional lower-pair closure and the
full-support tangent endpoint at infinity in component fourteen.

## The two `y=0` boundary charts

Only `y=0` retains higher-rank pair geometry.  Put

```text
L=A-B,                         M=A+B.
```

### `B_full`: `x0=d`

Let `Delta,c0` be the nonzero leading coefficients supplied by the arc and
set

```text
lambda=Delta/(c0(2a+1)),       mu=-a(a+1)/(2a+1).
```

Then

```text
U0=<e+lambda L, C+mu L>,
U1=<e,(a+1)L+C>,
U2=<e,aL+C>,
U3=<e,M>.                                             (8)
```

With ordered bases

```text
alpha=(e+lambda L,e,e,e),
beta =(C+mu L,(a+1)L+C,aL+C,M),
```

the only possibly displayed pure coefficients are

```text
T_0110=-2 lambda(2a+1),          T_1110=0,            (9)
```

and all other coefficients vanish.  The generic pair profile, in edge order
`01,02,03,12,13,23`, is

```text
(4,4,4,3,3,3).                                       (10)
```

This is a genuine component-twenty boundary chart with its generic pair-rank
signature.

### `B_drop`: `x0>d`

The deeper chart is

```text
U0=<C,L>,
U1=<e,(a+1)L+C>,
U2=<e,aL+C>,
U3=<e,M>.                                             (11)
```

With `alpha0=C,beta0=L` and the other ordered bases as above,

```text
T_0110=-2a(a+1),              T_1110=-2(2a+1),       (12)
```

all other pure coefficients vanish, and the generic pair profile is

```text
(4,4,3,3,3,3).                                       (13)
```

Construction places `B_drop` in the component-twenty closure.  Its possible
equivalence to, or intersection with, the singleton sheet or any other named
component remains unknown.  The profile (13) alone is not an orbit
certificate.

## Exceptional finite centres

The exceptional centres introduce no additional candidate family.

At `a=0`, put

```text
P=v(p)>0, Q=v(q)>0, R=min(P,Q), d>=R,
g=min(x1+P,x2+Q,0), z=min(x0,x1,x2).
```

The raw expression and exact split are

```text
E=d+x1+x2-m+z-n-min(x0+g,d+ell),                   (14)
E=0 iff x1=x2=y, -d<=y<=0, x0>=max(d-R,d+y).         (14)
```

Here `P<Q` forces `d=P`, `Q<P` forces `d=Q`, and `d>R` is possible only
when `P=Q=R` and the leading terms cancel.

At `a=-1`, the same statement holds with

```text
P=v(p+1), Q=v(q-1), R=min(P,Q),                      (15)
```

and the same raw formula and cancellation law.

At `a=-1/2`, where `s` tends to zero,

```text
g=min(x1,x2,h), h=v(s)>0,
E=d+x1+x2+g-2m+z-n-min(x0+g,d+ell),                 (16)
E=0 iff x1=x2=y, -d<=y<=0, x0>=d.                   (16)
```

In all three cases `y<0` is caught by the rank-two-pair theorem.  At
`a=-1/2`, direct substitution in `B_full` is invalid because `2a+1=0`.
With `L=c1 A-c2 B`, `M=c1 A+c2 B`, and
`k=c0/(4 Delta)`, the exact `y=0,x0=d` chart is instead

```text
U0=<L,C-k e>, U1=<e,(1/2)L+C>, U2=<e,-(1/2)L+C>, U3=<e,M>.
```

Its mode-zero wedge is `(k c1,-k c2,0,0,c1,-c2)` and its pair profile is
`(4,4,3,3,3,3)`; for `x0>d`, put `k=0`.  This direct chart is a
`B_drop`-type degeneration, not an identification with a named orbit.

## Centre at infinity

Assume

```text
v(p)=v(q)=v(s)=r<0,                  v(delta)=d>0.
```

Put

```text
g=min(x1+2r,x2+2r,r), b=min(x1+r,x2+r,0),
z=min(x0,x1,x2).
```

The raw expression and exact split are

```text
E=d+x1+x2+g-2b+z-n-min(x0+g,d+ell),                 (17)
E=0 iff
x1=x2=y,             -d<=y<=-r,      x0>=d-2r.       (17)
```

Here `U1=U2` throughout.  For `y<-r` the tangent direction has support two;
at `y=-r` it has full support and lies in component fourteen.  Infinity
therefore produces no new candidate component.

For completeness, let `L=c1 A-c2 B`, `M=c1 A+c2 B`,
`kappa=c0 P0^2/Delta`, and `alpha=2c0 P0/Delta`.  In wedge-coordinate order
`(01,02,03,12,13,23)`, the five mode-zero charts are

```text
<L,C>                         (0,0,0,0,c1,-c2)
<L,C+kappa e>                (-kappa c1,kappa c2,0,0,c1,-c2)
<L,C-(Delta/2)M>             (0,0,0,-Delta c1 c2,c1,-c2)
<L,C+kappa e-(Delta/2)M>     (-kappa c1,kappa c2,0,-Delta c1 c2,c1,-c2)
<L+alpha e,C+kappa e>        (-kappa c1,kappa c2,alpha,0,c1,-c2).
```

They respectively retain the interior baseline, the `x0=d-2r` wall, the
`y=-d` wall, their intersection, and the `y=-r,x0=d-2r` wall.  The two
`y` endpoints cannot coincide because that would require `d=r` with
`d>0>r`.

## Retained failed lemmas

The following tempting shortcuts are explicitly rejected.

1. **"Every `p+q=0` limit has zero pure tensor" is refuted.**  It holds for a
   fixed torus but fails when `x0>=d` and the `A/B` weights are equal.
2. Tracking only the triple permanent of `U1,U2,U3` is insufficient: mode
   three's pure kernel is `e+A+B`, not `e`.
3. Raw mode-zero plane Plueckers cannot replace the corrected
   `alpha0 wedge beta0`.
4. Pair profile `(4,4,3,3,3,3)` does not identify the singleton-sheet orbit.
5. Bounded integer tropical scans support the case split only as audits; they
   are not proofs.

## Exact replay

```text
uv run --with sympy --with z3-solver python \
  verify_p4_common_active_binary_triangle_p_plus_q_boundary.py

uv run --with sympy python \
  audit_p4_common_active_binary_triangle_p_plus_q_boundary.py

uv run --with sympy python verify_p4_rank_two_pair_kernel_geometry.py
uv run --with sympy python verify_p4_tangent_rank_two_pair_purity_classification.py
uv run --with sympy python verify_p4_support_two_tangent_flag_boundary_inclusion.py
uv run --with sympy python verify_p4_full_support_tangent_pair_component.py
```

The first command reconstructs (1)--(3), checks the generic min-plus theorem,
the exceptional and infinite inequality schemas, the two chart tensors and
pair profiles, and then replays the four named classification verifiers.  The
audit independently rebuilds the exterior and permanent formulas and uses a
bounded integer-weight scan only as non-probative regression evidence.

## Scope wall

Only diagonal source-coordinate tori, row changes inside each local plane,
and one common projective ambient normalization are used.  An arbitrary
`GL4` coordinate change is not allowed: it is not a symmetry of the
squarefree permanent algebra.

The exact placement of `B_full` and `B_drop` in intersections with older
named components remains open.  Their marked `H31` and weighted `H22` fibres
have not been analyzed.  Projective parameter charts beyond this valuative
classification, arbitrary-order gluing, and the global Krenn--Gu conjecture
remain unknown.
