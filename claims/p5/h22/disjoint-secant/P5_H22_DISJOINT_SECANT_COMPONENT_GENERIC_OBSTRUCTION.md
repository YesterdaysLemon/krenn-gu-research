# Generic weighted `H22` exclusion for the disjoint-secant component

## Status

**Exact characteristic-zero generic-fibre theorem.** The complete weighted
`H22` fibre over the generic point of pure-`P_4` component fifteen is empty.

The first weighted contraction alone supplies the obstruction.  Its finite
open Fitting image is one constant marking section; three marked minors
cover every ordinary slope, the two isotropic slopes have empty binary
incidence, and the point at infinity is the already-excluded component-
fifteen `H31` deletion.  Special component-parameter boundaries, pure-`P_4`
component exhaustiveness, and the global Krenn--Gu conjecture remain open.

## The three-modulus pure basis

Work over `K=C(p,q,rho)` in the source-torus quotient and pure bases of
[`P5_H31_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md`](../../h31/disjoint-secant/P5_H31_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md):

```text
a=(1,1,0,0),          a_bar=(1,-1,0,0),
b=(0,0,1,1),          b_bar=(0,0,1,-1),

ell=a+b_bar,          ell_bar=a-b_bar,
k=a_bar+p*b,          k_bar=b+q*a_bar,
o=ell_bar+rho*a_bar,

alpha=(a,b_bar,ell,p*rho*k_bar-(p*q+1)*o),
beta =(b,a_bar,k,k_bar).                            (1)
```

Only `T_1111=-4(p*q+1)` is nonzero.  Mark the same four planes by

```text
beta_i(h)=beta_i+h_i*alpha_i.                       (2)
```

## One weighted direction is enough

On the finite `01` slope chart use the contraction

```text
D_01^u(x,e)=(u*x0+x1,x2,x3,e).                    (3)
```

Let `M(u,h)z=0` be the fourteen mixed binary equations and let `A(z),B(z)`
be the two binary diagonals.  Normalize `A=1`, invert `B`, and eliminate the
extension vector while retaining the slope `u`.  The exact total projection
ideal is

```text
J_01^fin=<h3,rho*h2-p*q-1,h1,h0>.                  (4)
```

Thus every genuine finite-slope neighbour has the same marking

```text
h=(0,0,(p*q+1)/rho,0).                             (5)
```

The elimination keeps `u` in the target block, so (4) does not discard a
vertical slope component.  The two exceptional slopes below are empty; the
closure in (4) harmlessly retains their limiting marking.

An `H22` lift would require this `01` neighbour as well as its opposite
weighted contraction.  Excluding (3) is therefore already sufficient; no
second-direction intersection is needed.

## The ordinary-slope projective cover

For `u^2!=1`, the mixed matrix at (5) has rank six.  A kernel basis is

```text
v=(0,0,0,-rho,0,0,1,0),
w=(-(u+1),0,-(u+1),0,0,u-1,0,q(u-1)).             (6)
```

Indeed, rows `0123,7,11` and columns `0,...,5` give the minor

```text
64*p^2*q*rho*(u-1)^3*(u+1)^3*(p*q+1)^2.           (7)
```

Write `z=xv+yw` and put

```text
F(u)=(p*q+rho+1)u+p*q-rho+1.                      (8)
```

For the mode-zero marked map, take the `4 x 4` minors with row sets
`0127,0137,0157`.  After dividing by the required nonzero factor `A*B`,
their residuals are, up to elements of `K^*`,

```text
x*(u-1)*F(u)/(u+1),
(u-1)^2*(rho*x+F(u)y)/(u+1),
y*(u-1)^3/(u+1).                                  (9)
```

If `F(u)!=0`, the first and third residuals are nonzero multiples of `x`
and `y`, so they have no common projective zero.  If `F(u)=0`, the second
and third become nonzero multiples of `rho*x` and `y`, again with no common
projective zero.  Notice

```text
F(1)=2(p*q+1),       F(-1)=-2*rho,                 (10)
```

so this case split introduces no new collision with the exceptional slopes.
Every genuine ordinary-slope extension therefore has marked rank four.

## The isotropic and infinite slopes

At `u=1` and `u=-1`, impose the mixed equations and invert both diagonal
forms without making any assumption on the marking.  In each case the exact
ideal is the unit ideal.  These are the two isotropic directions of the
normalized hyperbolic `{0,1}` source block, and neither supports a genuine
binary neighbour.

At slope infinity, (3) becomes

```text
D_01^infinity(x,e)=(x0,x2,x3,e).                  (11)
```

This is literally the marked `H31` problem obtained by deleting source
coordinate one.  Its mixed matrix, both diagonal rows, and the mode-zero
marked map agree entry by entry with the component-fifteen `H31` model at
(5).  The preceding exact two-minor theorem excludes it.

## Consequence and proof boundary

Equations (4) and (9) exclude every finite ordinary slope, the unit-ideal
certificates exclude `u=+/-1`, and (11) excludes the unique point at
infinity.  Therefore

```text
generic H22 fibre(component 15)=empty.             (12)
```

Together with the marked `H31` theorem, all seventeen currently known
pure-`P_4` component orbits are now generically excluded for both fifth-
coordinate partition types.  This is a clean completion of the known-
component generic ledger, not a global proof: the pure-`P_4` component list
is not exhaustive away from the classified lower-pair locus, and generic
arguments do not settle every special parameter boundary.

## Exact replay

```text
uv run --with sympy python claims/p5/h31/disjoint-secant/verify_p5_h31_disjoint_secant_component_generic_obstruction.py
uv run --with sympy python claims/p5/h22/disjoint-secant/verify_p5_h22_disjoint_secant_component_generic_obstruction.py
python claims/p5/h22/disjoint-secant/audit_p5_h22_disjoint_secant_component_generic_obstruction.py
```

The primary verifier works over `C(p,q,rho)` and proves the retained-slope
Fitting ideal, the kernel and pivot identities, all three determinant
factorizations, both exceptional unit ideals, and the infinity/`H31`
identity.  The independent audit uses separately implemented finite-field
permanents and linear algebra.  At `(p,q,rho)=(2,2,3)` over `F_7`, it checks
all eight projective slopes and every marking.  The two isotropic slopes are
empty; each other slope has only (5); and all thirty-six genuine projective
extensions have a rank-four marked map.  This finite-field census is
corroboration, not the characteristic-zero proof.
