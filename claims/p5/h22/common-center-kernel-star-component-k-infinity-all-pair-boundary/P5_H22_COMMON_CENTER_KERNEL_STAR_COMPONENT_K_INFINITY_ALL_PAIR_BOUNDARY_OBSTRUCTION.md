# Component twenty-three `k=infinity` all-pair weighted-`H22` obstruction

## Status

**Exact characteristic-zero normalized-boundary theorem.**  The component-
twenty-three chart omitted by the affine coordinate `k` has no weighted-`H22`
extension on its all-pair locus.  More precisely, over

```text
S=Q[r,1/((r-1)(r+1))]
```

every finite weight and the projective weight are obstructed, for every
marking.  This includes the equal-complement point `r=0`.

The points `r=1,-1` are lower-pair and are not part of this theorem.  The
result concerns the displayed normalized source and the two certified
`D01`/`D23` contractions.  It does not cover arbitrary source or ambient
changes, other omitted component charts, arbitrary-order gluing, or the
global Krenn--Gu conjecture, which remains **UNRESOLVED**.

## The omitted `k` chart

Put `q=1/k`, fix the nonzero `s` chart by `s=1`, and rescale the first row of
plane one.  With

```text
A=(1,1,0,0),   C=(1,-1,0,0),
B=(0,0,1,1),   D=(0,0,1,-1),
```

the rows before setting `q=0` are

```text
alpha=(A, qA+D, A-C+B+rD, -A-C+B+tD),
beta =(B, B+C,  C,          C).
```

All mixed tensor coefficients vanish identically, while

```text
T0000=-4*(t-r+q*(r*t-1)),   T1111=-4.             (1)
```

Thus the pure `q=0` divisor has `t=r` and normalized rows

```text
alpha=(A, D, A-C+B+rD, -A-C+B+rD),
beta =(B, B+C, C, C).                              (2)
```

The tensor in (2) is nonzero and pure for every `r`.

## Exact pair locus and component placement

In edge order `01,02,03,12,13,23`, the pair-image ranks over `Q(r)` are

```text
(3,3,3,4,4,3).                                    (3)
```

The gcd of all nonzero three-by-three minors on edge `23` is

```text
4*(r-1)*(r+1).                                    (4)
```

At either `r=1` or `r=-1`, the exact profile is

```text
(3,3,3,4,4,2),                                    (5)
```

so these and only these parameter values leave the all-pair locus.  On the
open (4), the rank-three relation ranks are one on edges `01,02,03` and two
on edge `23`.

This boundary is not a new `P_4` component.  Permute the modes by

```text
(0,1,2,3) -> (1,2,3,0)
```

and right-multiply every source row by

```text
diag(1,-1,1/(r+1),1/(1-r)) * swap(0,1).           (6)
```

The resulting four Grassmann wedges are respectively proportional to the
standard component-twenty-two representative

```text
component_rows(A=-1,R=2,D=r)
```

by the nonzero factors

```text
4/((r-1)*(r+1)^2),  1,  1,  2/((r-1)*(r+1)).     (7)
```

Hence `r!=0,+-1` lies on component twenty-two.  At `r=0`, its complementary
directions agree (`D=0`), so it is the component-thirteen intersection.  At
`r=+-1`, (5) places it in the certified lower-pair locus.  Notice that the
component-twenty-two coordinate `2A+R` is zero all along this curve.  The
generic component-twenty-two weighted-fibre packages therefore cannot be
specialized to prove this theorem; in particular, the prior `rho=0` theorem
closes only one finite `D23` weight on the generic component.

## Every finite weight

Mark (2) by replacing

```text
beta_i -> beta_i+h_i*alpha_i.
```

For a common finite weight `lambda`, form the fourteen mixed `D01` rows and
the fourteen mixed `D23` rows in the eight extension coordinates.  Let `M`
be their combined row module over

```text
S[h0,h1,h2,h3,lambda].
```

The verifier computes a standard basis and compares both module inclusions
against an explicit 27-generator normal form.  In diagonal order

```text
(A01,B01,A23,B23),
```

exact reduction gives

```text
(not in M, in M, in M, not in M).                 (8)
```

Thus every common mixed-kernel vector kills both `B01` and `A23`.  In the
certified paired-contraction criterion, a genuine binary weighted-`H22`
extension requires both beta diagonals `B01,B23` to be nonzero and at least
one alpha diagonal to be nonzero.  The membership `B01 in M` alone is
therefore decisive; `A23 in M` is an additional obstruction.  Hence (8)
obstructs every finite weight uniformly.  No weight factor and no marking
factor is inverted.

## Projective weight

At the projective weight, the same combined mixed-row module is exactly

```text
S[h0,h1,h2,h3]^8.                                 (9)
```

The verifier checks both inclusions with the coordinate module, not merely
its standard-basis size.  Hence the common mixed kernel is zero and the
projective weight is obstructed.

Equations (8) and (9) close the complete projective weight line on the
normalized all-pair boundary `r^2!=1`, including `r=0`.  No finite-field
calculation is used.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-k-infinity-all-pair-boundary/verify_p5_h22_common_center_kernel_star_component_k_infinity_all_pair_boundary_obstruction.py
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-k-infinity-all-pair-boundary/audit_p5_h22_common_center_kernel_star_component_k_infinity_all_pair_boundary_obstruction.py
```

The primary uses the repository contraction builder.  The audit has no
repository imports: it rebuilds the tensor, pair matrices, projected
permanent coefficients, localized modules, and component-twenty-two mapping
independently over characteristic zero.
