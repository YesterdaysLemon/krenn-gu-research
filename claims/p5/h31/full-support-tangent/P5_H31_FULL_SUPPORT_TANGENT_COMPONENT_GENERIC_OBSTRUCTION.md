# Generic `H31` exclusion for the full-support tangent component

## Status

**Exact characteristic-zero generic-fibre theorem.** The complete marked
`H31` fibre over the generic point of pure-`P_4` component fourteen is
empty.

The proof uses a two-parameter source-torus quotient, exact open Fitting
projections, and three binary resultants.  It treats every marked basis,
every deleted source coordinate, and every projective extension direction.
The weighted `H22` fibre is closed in the subsequent theorem.  Special
parameter/projective boundaries, pure-`P_4` component exhaustiveness, and
the global Krenn--Gu conjecture remain open.

## The five-parameter family has a two-parameter quotient

Start from the polar-graph family in
[`P4_FULL_SUPPORT_TANGENT_PAIR_COMPONENT.md`](claims/p4/classifications/pair-geometry/full-support-tangent-pair/P4_FULL_SUPPORT_TANGENT_PAIR_COMPONENT.md),
with parameters `(a,b,c,d,t)`.  On the generic torus chart put

```text
p=c/a,       q=d/b,
D=diag((2tab)^(-1),1,a^(-1),b^(-1)).                (1)
```

Applying `D` to the source coordinates and rescaling rows sends the four
planes exactly to

```text
e =(1,0,0,0),          w =(0,1,1,1),
u =(0,1,p,q),
s1=(1-p,1+q,-p-q,0),
s2=(1-q,1+p,0,-p-q),

U0=U1=span(e,w),       U2=span(e,u),
U3=span(s1,s2).                                      (2)
```

Thus the quotient function field is `K=C(p,q)`.  This is the geometric
invariant-theory step: three apparent parameters are source-torus gauge,
not moduli.

Put `S=p+q+1`.  Pure-factor bases are

```text
alpha=(e,e,S*e-u,(q-1)*s1-(p-1)*s2),
beta =(w,w,e,s1).                                    (3)
```

In these bases the only nonzero coefficient is

```text
T_1111=-2(p-1).                                      (4)
```

Every other basis of the same marked planes is

```text
beta_i(h)=beta_i+h_i alpha_i.                        (5)
```

## Six marking sheets, exactly

For deleted source coordinate `j`, let `M_j(h)z=0` be the fourteen mixed
binary equations in the extension vector `z in K^8`, and let `A_j(z)` and
`B_j(z)` be the two diagonal coefficients.  A genuine neighbour requires
`A_jB_j!=0`.  Normalize `A_j=1`, invert `B_j`, and eliminate `z`.

The `j=0` projection is the unit ideal.  Each of `j=1,2,3` has two reduced
rational points:

| `j` | `H_j` | `K_j` | marking points `(h0,h1,h2,h3)` |
|---:|---|---|---|
| 1 | `S/(p+q)` | `q/((p-q)(p+q-1))` | `(H_1,0,0,K_1)`, `(0,H_1,0,K_1)` |
| 2 | `S/(q+1)` | `q(q+1)/((p+q)(q-1)(p-q-1))` | `(H_2,0,0,K_2)`, `(0,H_2,0,K_2)` |
| 3 | `S/(p+1)` | `q/((p+q)(p-q+1))` | `(H_3,0,0,K_3)`, `(0,H_3,0,K_3)` |

The verifier proves the four projected ideals in both directions, so no
marking curve or hidden embedded sheet has been omitted.

## Three pencils and one exact symmetry

Because `U0=U1` with identical pure bases, swapping modes zero and one
exchanges the two points in every row of the table.  It permutes extension
coordinates by

```text
(0 1)(4 5)                                             (6)
```

and identifies the mode-zero marked map on the first sheet with the
mode-one marked map on the second.  The verifier checks the mixed matrices,
both diagonal rows, and the marked maps entry by entry.  Only the first
sheet of each row therefore needs a resultant.

On all three prototypes the mixed matrix has rank six.  Rows
`(3,4,5,7,8,11)` and columns `(0,1,2,3,4,5)` give a nonzero pivot, leaving
homogeneous kernel coordinates `[x:y]=[z6:z7]`.  For the mode-zero marked
map take the two `4 x 4` minors with row sets `0147` and `0457`.  Their
binary gcd is

```text
gcd(Delta_0147,Delta_0457)=R_j A_j B_j,              (7)
```

where

```text
R_1=-2(p+q)(p+q+1),
R_2=-2p/((p+q)(p-q-1)^2),
R_3= 2q/((p+q)(p-q+1)^2).                           (8)
```

Every `R_j` is nonzero in `C(p,q)`.  Two homogeneous binary forms have a
common projective zero exactly when their gcd has a nonconstant factor.
On the genuine-neighbour open `A_jB_j!=0`, equations (7)--(8) therefore
force at least one marked minor to be nonzero.  The marked map has rank
four, contradicting the rank-at-most-three factorization required by an
`H31` lift.

## Consequence and proof boundary

All six projected marking sheets are empty after the marked-rank condition,
and the fourth deleted coordinate has no genuine binary neighbour at all.
Therefore

```text
generic H31 fibre(component 14)=empty.              (9)
```

This closes the marked `H31` side of component fourteen.  The subsequent
weighted theorem closes its `H22` side as well.  Neither marked fibre of
component fifteen nor the special boundary fibres of any component are
settled here.

## Exact replay

```text
uv run --with sympy python verify_p5_h31_full_support_tangent_component_generic_obstruction.py
python audit_p5_h31_full_support_tangent_component_generic_obstruction.py
```

The primary verifier works over `C(p,q)`.  It launches each of the three
prototype pencil factorizations in a fresh interpreter to bound peak memory;
the exact mode-swap identities cover their partners.  The independent audit
uses separately implemented subset-DP permanents and finite-field linear
algebra.  At `(p,q)=(2,4)` over `F_11` it exhausts all markings, finds exactly
`0+2+2+2` sheets, and checks all 60 genuine projective extensions.  The
finite-field census is corroboration, not the characteristic-zero proof.
