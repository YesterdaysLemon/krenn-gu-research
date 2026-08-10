# Component twenty-three `s=0,k=infinity` unit-parameter-line obstruction

## Status

**Exact characteristic-zero normalized-line theorem.**  On component
twenty-three's simultaneous `s=0,k=infinity` corner, the complete homogeneous
weighted-`H22` incidence is empty on the four punctured finite parameter lines

```text
r=+1,   r=-1,   t=+1,   t=-1,                    (1)
```

away from their intersections with

```text
r=0, t=0, r=t, rt=1, r=-t,
r=infinity, or t=infinity.                        (2)
```

The theorem covers every affine marking and every homogeneous weight in the
fixed normalized `D01/D23` contraction order.  On the ordinary and
projective weight charts a genuine shared-binary survivor line occurs; a
uniform missing-third-row determinant excludes every genuine member from a
ternary lift.  Thus a claim of shared-module emptiness on these lines would
be false even though the full ternary fibre is empty.

All intersections in (2) are covered by separately replayable normalized
coordinate-axis, diagonal, `rt=1`, antidiagonal, and projective-parameter
boundary packages.  Consequently this theorem closes the last finite
special divisors left by the generic corner proof.  It remains a result only
for this displayed component chart and fixed order.  Arbitrary ambient or
source changes, arbitrary order, other compactifications, global gluing, and
the global Krenn--Gu conjecture remain **UNKNOWN** or **UNRESOLVED**.  No
finite-field calculation is used.

## The base line `r=1`

Put

```text
A=(1,1,0,0),   C=(1,-1,0,0),
B=(0,0,1,1),   D=(0,0,1,-1).
```

On the corner, after the legal `k=infinity` row rescaling,

```text
alpha=(A,D,B+rD,B+tD),
beta =(B,B,C,C).                                   (3)
```

It is enough initially to take

```text
r=1,       t=u,       u*(u-1)*(u+1)!=0.           (4)
```

All sixteen pure coefficients vanish except `T1111=-4`.  In edge order
`01,02,03,12,13,23`, the pair profile is

```text
(3,3,3,3,3,4),                                    (5)
```

and the gcd of the nonzero edge-`23` maximal minors is

```text
8*(u-1)^2.                                         (6)
```

Thus the punctured line (4) remains all-pair; it is not silently assigned to
a lower-pair stratum.

Mark every plane by

```text
marked_i=beta_i+h_i alpha_i.                      (7)
```

Every genuine marked basis is represented this way.  Let
`x=(x0,...,x3;y0,...,y3)` be the common extension, and let `M` be the combined
`28 x 8` matrix of all mixed binary coefficients for `D01` and `D23`.
In diagonal order

```text
(A01,B01,A23,B23),                                (8)
```

genuineness requires both beta diagonals and at least one alpha diagonal to
be nonzero.

## Ordinary finite weights

Use `[lambda:1]` with `lambda^2!=1` and put

```text
C=256*(lambda-1)^4*(lambda+1)^4*(u-1)^2*(u+1).
```

The verifier checks the following exact eight-by-eight minors:

| rows | restriction | determinant |
|---|---|---|
| `(0,1,2,3,8,9,13,16)` | none | `C*h2*h3*u` |
| `(0,1,3,5,8,9,13,16)` | none | `-C*h2*(h1*u-1)` |
| `(0,1,3,4,8,9,13,16)` | none | `-C*h3*u*(h1-1)` |
| `(0,1,3,7,8,9,13,16)` | none | `C*h0*u` |
| `(0,1,3,8,9,12,13,16)` | `h0=h3=0,h1=1/u` | `-256*(lambda-1)^5*(lambda+1)^3*(u-1)^2*(u+1)` |
| `(0,1,3,8,9,12,13,16)` | `h0=h2=h3=0` | `256*u*(lambda-1)^5*(lambda+1)^3*(h1-1)*(u-1)*(u+1)` |

They give a complete branch tree.  Full mixed rank fails precisely on

```text
h=(0,1,0,H),       H arbitrary.                  (9)
```

On (9), use the polynomial kernel generator

```text
z_H=(0,0,-1,-1;0,1,0,H*u).                       (10)
```

The mixed matrix kills (10), while the seven-by-seven minor on rows
`(0,1,3,8,9,13,16)` and columns `(0,1,2,3,4,6,7)` is

```text
128*u*(lambda-1)^4*(lambda+1)^3*(u-1)^2.         (11)
```

Hence the residual mixed rank is exactly seven.  Its diagonals are

```text
(2*(lambda+1)*(u+1),
 2*H*(lambda-1)*(u+1),
 0,
 -2*(lambda+1)).                                  (12)
```

At `H=0`, `B01=0`, so the residual is nongenuine.  At `H!=0`, all required
diagonals are nonzero and the shared binary incidence is genuine.

Append (10) to the four alpha and four marked rows.  For the sixteen
one-`gamma_0` equations from the two contractions, the five-by-five minor on
rows `(0,1,2,7,9)` is

```text
8*H*(lambda-1)^4*(lambda+1)*(u-1)*(u+1)^2.       (13)
```

It is nonzero on exactly the genuine ordinary open.  Thus the missing third
row in mode zero is forced to vanish, contradicting a ternary local lift.

At `lambda=1`, exact mixed-module reduction gives membership pattern

```text
(A01,B01,A23,B23) in M = (no,yes,yes,no),         (14)
```

so `B01` vanishes on every mixed kernel.  At `lambda=-1`, the pattern is

```text
(yes,no,yes,yes),                                 (15)
```

and `B23` vanishes.  Equations (13)--(15) close every finite weight.

## Projective weight

At `[1:0]`, saturating all mixed equations by `A01*B01*B23` and eliminating
the extension coordinates gives, in both directions,

```text
<h2,h1-1,h0>.                                     (16)
```

Thus the complete genuine shared-binary projection is again (9).  On the
same kernel (10), the rank minor and diagonals are

```text
128*u*(u-1)^2,
(2*(u+1),2*H*(u+1),0,-2).                         (17)
```

Genuineness is exactly `H!=0` on (4).  The projective one-`gamma_0` minor is

```text
8*H*(u-1)*(u+1)^2,                                (18)
```

which is nonzero on that open.  This closes projective weight without
mistaking the genuine binary family for a counterexample.

## Legal transfer to all four lines

Two exact corner symmetries suffice.

First, the tensor-mode transposition `(2 3)` acts by

```text
(r,t)->(t,r),
h->(h0,h1,h3,h2),
x->(x0,x1,x3,x2;x4,x5,x7,x6),                    (19)
```

and fixes the ambient coordinates, both contractions, and `[mu:nu]`.

Second, the signed ambient involution

```text
J(v0,v1,v2,v3)=(-v1,-v0,v3,v2)                  (20)
```

acts on the corner by

```text
(r,t)->(-r,-t),
h->(-h0,-h1,h2,h3),
x->(-x0,-x1,x2,x3;x4,x5,x6,x7),
[mu:nu]->[nu:mu].                                 (21)
```

The first two alpha rows acquire signs `(-1,-1)` and the last two do not.
For every binary row word `epsilon`, the exact coefficient covariance is the
product of those alpha-row signs and an additional factor `-1` for `D01` or
`+1` for `D23`.  Both primary and audit check all sixteen words for both
contractions and both symmetries.  The audit also verifies the generic
five-by-five permanent is invariant under (20), so arbitrary missing-third
rows and the obstruction determinants transport legally.

Because (19) fixes weight and (21) bijects the entire projective weight line,
the complete `r=1` theorem transfers first to `r=-1` and then to both
`t=+/-1` lines without losing zero or projective weight.

## Remaining loci

Within this package, each line omits only the four values

```text
u=0,+1,-1,infinity.                               (22)
```

They are exactly the intersections listed in (2), already assigned to the
separate coordinate-axis, diagonal/`rt=1`, antidiagonal, and projective
boundary packages.  No additional finite residual locus survives on the
four unit-parameter lines.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/component23-s-zero-k-infinity-unit-parameter-lines/verify_p5_h22_component23_s_zero_k_infinity_unit_parameter_lines_obstruction.py
uv run --with sympy python claims/p5/h22/component23-s-zero-k-infinity-unit-parameter-lines/audit_p5_h22_component23_s_zero_k_infinity_unit_parameter_lines_obstruction.py
```

The primary checks the complete ordinary branch cover, exceptional-weight
modules, projective saturation, finite and projective ternary determinants,
and both symmetry covariances.  The audit imports no repository code: it
rebuilds all permanents by subset dynamic programming and repeats every
certificate independently over exact characteristic zero.
