# Generic `H31` exclusion for the disjoint-secant component

## Status

**Exact characteristic-zero generic-fibre theorem.** The complete marked
`H31` fibre over the generic point of pure-`P_4` component fifteen is empty.

The proof quotients the six-parameter component by the diagonal source
torus, computes all four open Fitting images, and reduces every surviving
extension family to two coprime binary minors.  The weighted `H22` fibre is
closed in the subsequent theorem.  Special parameter/projective boundaries,
pure-`P_4` component exhaustiveness, and the global Krenn--Gu conjecture
remain open.

## Three moduli, not six

Use the notation of
[`P4_DISJOINT_SECANT_LOWER_PAIR_COMPONENT.md`](../../../p4/classifications/pair-geometry/disjoint-secant-lower-pair/P4_DISJOINT_SECANT_LOWER_PAIR_COMPONENT.md).
On the generic torus chart apply

```text
D=diag(1,s^(-1),lambda^(-1),(lambda*t)^(-1))
```

to the source coordinates, and rescale the second rows of `U0,U1` and the
first row of `U3` by `lambda`.  Put

```text
p=m/lambda,       q=lambda*n.                       (1)
```

Then the planes become

```text
a=(1,1,0,0),          a_bar=(1,-1,0,0),
b=(0,0,1,1),          b_bar=(0,0,1,-1),

ell=a+b_bar,          ell_bar=a-b_bar,
k=a_bar+p*b,          k_bar=b+q*a_bar,
o=ell_bar+rho*a_bar,

U0=<a,b>,       U1=<a_bar,b_bar>,
U2=<k,ell>,     U3=<k_bar,o>.                       (2)
```

Thus the quotient function field is `K=C(p,q,rho)`.  Three apparent
parameters were source-coordinate gauge.

Pure-factor bases are

```text
alpha=(a,b_bar,ell,p*rho*k_bar-(p*q+1)*o),
beta =(b,a_bar,k,k_bar).                            (3)
```

In these bases the only nonzero coefficient is

```text
T_1111=-4(p*q+1).                                   (4)
```

Every marked basis of the same four planes is

```text
beta_i(h)=beta_i+h_i*alpha_i.                       (5)
```

## All four marking projections are one point

For deleted source coordinate `j`, let `M_j(h)z=0` denote the fourteen
mixed binary equations in the extension vector `z in K^8`.  Write
`A_j(z),B_j(z)` for the two diagonal coefficients.  A genuine binary
neighbour requires `A_j*B_j!=0`.

Normalize `A_j=1`, invert `B_j`, and eliminate the eight extension
coordinates.  For every `j=0,1,2,3`, the exact projected ideal is

```text
J_j=<h3,rho*h2-p*q-1,h1,h0>.                       (6)
```

The verifier proves equality of ideals in both directions.  Hence all four
deletions share the unique marking

```text
h=(0,0,(p*q+1)/rho,0).                             (7)
```

There are no hidden marking curves or embedded sheets on the generic open.

## Four projective extension lines

At (7), every mixed matrix has rank six.  Write its kernel as
`z=x*v_j+y*w_j`.  Exact bases are

```text
v0=v1=(0,0,0,-rho,0,0,1,0),
w0=( 1/q,0, 1/q,0,0,1/q,0,1),
w1=(-1/q,0,-1/q,0,0,1/q,0,1),

v2=v3=(0,0,0,rho,0,0,1,0),
w2=(0, 1, 1,0,1,0,0,1),
w3=(0,-1,-1,0,1,0,0,1).                           (8)
```

For the mode-zero marked map, take the following two `4 x 4` minors.  After
dividing by the two required diagonal forms `A_j B_j`, their residuals are:

| `j` | minor rows | first residual | second residual, up to a nonzero scalar |
|---:|---|---|---|
| 0 | `0127,0137` | `x` | `q*rho*x+(rho-p*q-1)*y` |
| 1 | `0127,0137` | `x` | `q*rho*x+(p*q+rho+1)*y` |
| 2 | `0127,0237` | `y` | `rho*x+(p*q-p*rho+1)*y` |
| 3 | `0127,0237` | `y` | `rho*x-(p*q+p*rho+1)*y` |

The omitted factors belong to `K^*`.  Each pair has homogeneous binary gcd
one over `K[x,y]`.  Therefore the two marked minors cannot vanish together
at any projective extension direction on which `A_j B_j` is nonzero.  At
least one marked map has rank four, contradicting the rank-at-most-three
factorization required by an `H31` lift.

## Consequence and proof boundary

The four Fitting images in (6) are exhaustive on the genuine-binary open,
and (8) covers every projective extension above them.  Thus

```text
generic H31 fibre(component 15)=empty.              (9)
```

All seventeen presently known pure-`P_4` component orbits are now
generically excluded for `H31`.  The subsequent weighted theorem closes
component fifteen's `H22` fibre as well.  Special parameter boundaries and
the possibility of additional pure-`P_4` components away from the completely
classified lower-pair locus remain.  This is therefore not a global proof
of the conjecture.

## Exact replay

```text
uv run --with sympy python claims/p5/h31/disjoint-secant/verify_p5_h31_disjoint_secant_component_generic_obstruction.py
python claims/p5/h31/disjoint-secant/audit_p5_h31_disjoint_secant_component_generic_obstruction.py
```

The primary verifier works over `C(p,q,rho)` and proves the source-torus
normalization, pure-basis identity, four Fitting ideal equalities, four
kernel identities, all eight determinant factorizations, and the four
coprimality statements.  The independent audit uses separately implemented
subset-DP permanents and finite-field linear algebra.  At
`(p,q,rho)=(2,3,3)` over `F_11`, it exhausts every marking, finds one point
for each deletion, and checks all forty genuine projective extensions.  The
finite-field census is corroboration, not the characteristic-zero proof.
