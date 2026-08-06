# Three linear-slope `H22` boundaries of the disjoint mixed-star component

## Status

This is an exact characteristic-zero theorem over the generic points of
three rational slope graphs on the eighth pure-`P_4` component.

For both weighted directions, every genuine binary neighbour violates
a fixed one-marked rank condition.  Two graphs use the mode-zero
`0137/0157` minors throughout.  The third has a genuine mode-zero
degeneration in direction `D_01`, repaired by the mode-one `0457`
minor.

This does not close special divisors inside the graphs, the remaining
quadratic slope candidate, every factor of the generic Bezout
certificates, component exhaustiveness, `P_5 -> Delta_3`, or the global
prize conjecture.  No graph satisfying the prize equation and no
global nonexistence proof is claimed.

## The three graphs

Use the component relation

```text
Phi =
 a^2 b f phi^2+a^2 f^2
 -b^2 f^2+b^2 phi^2-bf-1.                         (1)
```

The three slope divisors are

```text
S_+ = (a+b)r+(a-b),
S_- = (a+b)r-(a-b),
X   = (af-1)r+(af+1).                              (2)
```

On their principal charts they are the rational graphs

```text
S_+: r=-(a-b)/(a+b),
S_-: r= (a-b)/(a+b),
X:   r=-(af+1)/(af-1).                             (3)
```

The first two have no missing component point when `a+b=0`: imposing
`S_+=0` or `S_-=0` then gives `a=b=0`, while `Phi=-1`.  The third has
no point with `af-1=0`, because its constant term becomes `2`.
Therefore the algebraic equations in (2) represent the complete graphs,
not only the rational charts in (3).

## Six unsplit Fitting identities

For either direction `D`, let

```text
M_D(t)z=0                                          (4)
```

be the fourteen mixed binary equations, with diagonal coefficients
`A_D(z),B_D(z)`.  Normalize a genuine binary neighbour by

```text
A_D(z)=1,       wB_D(z)-1=0.                       (5)
```

For the two source-ratio graphs `S_+` and `S_-`, let
`H_0137,H_0157` be the mode-zero one-marked determinants.  Exact
standard-basis reduction gives, for each sign and each direction,

```text
(
 Phi,
 S_+ or S_-,
 M_D(t)z,
 A_D(z)-1,
 wB_D(z)-1,
 H_0137,
 H_0157
)=(1).                                             (6)
```

These are four full, unsplit incidence identities.

On the basis-ratio graph `X`, direction `D_23` obeys the same mode-zero
two-minor identity.  Direction `D_01` is different: some genuine binary
neighbours have mode-zero marked rank three.  Move the distinguished
local mode from zero to one and let `H^(1)_0457` be rows `0457` of that
one-marked map.  Then

```text
(
 Phi,
 X,
 M_01(t)z,
 A_01(z)-1,
 wB_01(z)-1,
 H^(1)_0457
)=(1).                                             (7)
```

Equations (6)--(7), together with the mode-zero `D_23` identity on
`X`, give six characteristic-zero unit ideals.

A ternary lift factors every one-marked map through a
three-dimensional target local space.  Its rank in every distinguished
mode is therefore at most three.  The displayed identities force rank
four in at least one fixed mode, excluding every lift.

## Why the cross-mode repair matters

The graph `X` is not merely a denominator where the generic proof
becomes slow.  It supports a real degeneration: the mode-zero
rank-at-most-three incidence in `D_01` is nonempty.  A proof that
silently specialized the generic mode-zero certificate would fail.

The target tensor, however, imposes the rank-at-most-three condition in
all four local modes.  Modes one and two remain transverse to the
binary extension scheme, and the fixed mode-one `0457` minor cuts it
away.  This cross-mode repair is the same determinantal principle that
closed the earlier coupled slope-parameter divisor.

In geometric language, one Fitting chart acquires a vertical component,
but the intersection of all local Fitting degeneracy loci remains
empty.

## Honest frontier

The generic points of all three rational slope graphs in (2) are now
closed in both directions.  Their deeper intersections remain open
unless covered by an earlier parameter or slope theorem.

One remaining cleared-certificate candidate is quadratic in `r`; a
further linear graph with larger coefficients has exact finite-field
rank-four evidence but its current characteristic-zero calculations
timed out.  Those timeouts are null results.  Neither candidate is
claimed closed.

Both candidates descend to the exact two-dimensional source-torus
quotient in
[`P5_H22_DISJOINT_MIXED_STAR_TORUS_QUOTIENT.md`](P5_H22_DISJOINT_MIXED_STAR_TORUS_QUOTIENT.md).
Their equations and stopped calculations are recorded in
[`P5_H22_DISJOINT_MIXED_STAR_CERTIFICATE_DIVISOR_FRONTIER.md`](P5_H22_DISJOINT_MIXED_STAR_CERTIFICATE_DIVISOR_FRONTIER.md).

Other certificate factors may be syzygy artifacts and have not been
promoted without a normalized incidence calculation.  Other pure
components may exist.  The global Krenn--Gu conjecture remains
unresolved.

## Verification

Run:

```text
python \
  verify_p5_h22_disjoint_mixed_star_linear_slope_boundary_obstruction.py

python \
  audit_p5_h22_disjoint_mixed_star_linear_slope_boundary_obstruction.py
```

The primary verifier reconstructs the component, all three algebraic
slope graphs, both mixed matrices, the relevant one-marked maps, and
requires all six full incidence ideals to reduce to `(1)`.

The independent audit imports nothing from the primary verifier.  It
exhausts every affine marking at generic component points over `F_11`
and `F_13`, for all three graphs and both directions.  Every genuine
projective direction has marked rank four and a selected minor
nonzero; the `X,D_01` cases use mode one.  The finite-field census is
corroboration only; (6)--(7) are the proofs over `C`.
