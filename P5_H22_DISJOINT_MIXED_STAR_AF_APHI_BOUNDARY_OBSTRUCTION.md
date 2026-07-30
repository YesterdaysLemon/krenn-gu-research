# The `af`/`aphi` boundary of the disjoint mixed-star component

## Status

This is an exact characteristic-zero theorem at the generic points of
four rational rank-two branches of the eighth pure-`P_4` component.
They are the previously hidden pieces of the selected `D_23` Fitting
chart on `af=+/-1`.

For `D_23`, every one of the four branches has empty genuine binary
incidence.  For `D_01`, every genuine binary neighbour violates one of
two mode-zero one-marked rank conditions.  Hence the generic weighted
`H22` incidence is empty on all four branches.

This does not close special divisors inside the branches, all remaining
parameter or projective boundaries, component exhaustiveness, the
complete `P_5 -> Delta_3` obstruction, or the global prize conjecture.
No graph satisfying the prize equation and no global nonexistence proof
is claimed.

## An intrinsic minor-content ledger

The generic `D_23` proof chooses seven base rows of the `14 x 8` mixed
matrix,

```text
0,1,3,5,7,8,10,
```

and adjoins rows

```text
2,4,6,9,11,12,13
```

to obtain seven maximal minors `q_0,...,q_6`.  Reduce each minor by the
component equation

```text
Phi =
 a^2 b f phi^2+a^2 f^2
 -b^2 f^2+b^2 phi^2-bf-1.                         (1)
```

Factoring over `C(a,b,f,r)[phi,t_0,t_1,t_2,t_3]` and then factoring the
coefficient contents over `C[a,b,f,r]` gives a common square-free
numerator support

```text
a(af-1)(af+1)K r(r-1)(r+1)(bf+1),                 (2)
```

where

```text
K=-a^2 f^2+b^2 f^2+bf+1.                          (3)
```

The last four contents have the additional factor

```text
L=a^2 b f^2+2a^2 f+b,                              (4)
```

but the first three do not.  All seven denominators are powers of

```text
P=a^2 f+b.                                         (5)
```

The verifier checks the exact contents including constants and
multiplicities, not merely this square-free summary.

This ledger is smaller and more geometric than a denominator extracted
from one large Bezout certificate: accidental factors belonging only
to a chosen syzygy never enter (2).

## Removing already closed factors

On the component, (3) satisfies

```text
Phi+K=b phi^2(a^2 f+b).                            (6)
```

Thus `K=0` is contained in `b=0`, `phi=0`, or `P=0`.  The first two
divisors are already covered by the parameter-pivot theorem.  On
`P=0`, substituting `f=-b/a^2` gives

```text
a^4 Phi=-(a-b)^2(a+b)^2.                           (7)
```

Hence its rank-two points lie on `a=+/-b, bf=-1`, also already covered.
The divisor `bf+1` splits into those same rank-two branches plus two
rank-one branches.  The slope divisors `r=+/-1` are covered by the
equal/opposite-weight binary theorem.  The factor `a=0` is another
closed parameter-pivot branch.  The factor `L` is not common to all
seven minors and therefore is not a base divisor of this chart.

The remaining common parameter factor is `af=+/-1`.

## Splitting `af=+/-1`

Exact substitution in (1) gives

```text
a^2 Phi|_(af=1)
 = b(a+b)(a phi-1)(a phi+1),

a^2 Phi|_(af=-1)
 =-b(a-b)(a phi-1)(a phi+1).                      (8)
```

The `b=0` pieces and the pieces `a=-b,af=1` and `a=b,af=-1` are among
the twelve previously closed branches.  The genuinely new rational
branches are therefore

```text
F_(epsilon,delta):
 af=epsilon,       a phi=delta,
 epsilon,delta in {+1,-1}.                         (9)
```

Their function fields are `C(a,b,r)`, with

```text
f=epsilon/a,       phi=delta/a.                    (10)
```

All four local planes retain rank two at each generic point.

## Strong binary obstruction for `D_23`

For either weighted direction, let

```text
M_D(t)z=0                                          (11)
```

be the fourteen mixed binary equations, and write `A_D(z),B_D(z)` for
the two diagonal coefficients.  Normalize a genuine binary neighbour
by

```text
A_D(z)=1,       wB_D(z)-1=0.                       (12)
```

On every branch (9), exact standard-basis reduction over `C(a,b,r)`
gives

```text
(
 M_23(t)z,
 A_23(z)-1,
 wB_23(z)-1
)=(1).                                             (13)
```

Thus `D_23` has no genuine binary neighbour at the generic point.  No
ternary rank argument is needed in this direction.

## Two-minor Fitting obstruction for `D_01`

Let `H_0137,H_0157` be the determinants of rows `0137` and `0157` of
the mode-zero one-marked map.  On every branch (9),

```text
(
 M_01(t)z,
 A_01(z)-1,
 wB_01(z)-1,
 H_0137,
 H_0157
)=(1).                                             (14)
```

A ternary lift factors this one-marked map through a three-dimensional
target local space, so its rank is at most three.  Equation (14) says
that every genuine binary neighbour has rank four.  Hence no such
neighbour lifts to `H22`.

Equations (13)--(14) are eight independently replayed characteristic-
zero unit ideals.

## Geometric interpretation

The seven selected maximal minors are a local presentation of a
Fitting ideal.  Taking their parameter contents is the algebraic
analogue of locating the base divisor of a rational determinantal
chart.  Normalizing that divisor splits it into four rational sheets.
On those sheets the apparently degenerate `D_23` chart becomes
stronger: its genuine binary incidence disappears.  The other
direction is transverse to the same sheets and is cut out by two
small minors.

This is precisely the gain from translating the matching problem into
determinantal geometry before computing: the boundary of a large
certificate becomes a normalization problem for four rational
divisors.

## Honest frontier

The new theorem closes the generic points of all four new branches in
(9).  Deeper intersections inside them remain open unless covered by
one of the earlier boundary theorems.  The factor `r=0` in (2) is a
projective endpoint of the weighted-slope chart and is now closed in
[`P5_H22_DISJOINT_MIXED_STAR_ZERO_SLOPE_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_ZERO_SLOPE_BOUNDARY_OBSTRUCTION.md).
That theorem also records the intrinsic contents of the selected
`D_01` maximal minors and rank pivot.  The final `D_01` Fitting
incidence certificates still need the same treatment.

Other pure components may exist.  No satisfying graph and no global
nonexistence proof is claimed.

## Verification

Run:

```text
tmp/codex_verify_env/Scripts/python.exe \
  verify_p5_h22_disjoint_mixed_star_af_aphi_boundary_obstruction.py

tmp/codex_verify_env/Scripts/python.exe \
  audit_p5_h22_disjoint_mixed_star_af_aphi_boundary_obstruction.py
```

The primary verifier reconstructs the component family, derives the
seven exact `D_23` minor contents, checks the divisor decompositions
(6)--(8), checks generic rank two of every local plane, and requires
all eight ideals (13)--(14) to reduce to `(1)`.

The independent audit imports nothing from the primary verifier.  At a
generic point of each branch over `F_7`, it exhausts all `7^4` affine
markings at slope two.  It finds no genuine `D_23` binary direction and
checks both selected minors and marked rank four on every genuine
`D_01` projective direction.  This census is corroboration only;
(13)--(14) are the characteristic-zero proof.
