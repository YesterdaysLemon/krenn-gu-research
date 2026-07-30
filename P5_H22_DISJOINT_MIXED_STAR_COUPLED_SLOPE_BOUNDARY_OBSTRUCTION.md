# Coupled slope-parameter `H22` boundary on the disjoint mixed-star component

## Status

This is an exact characteristic-zero theorem over the generic point of
the principal coupled slope-parameter divisor omitted by the
degree-five `D_01` marking cover on the eighth pure-`P_4` component.

Both weighted directions are excluded by a single one-marked
determinant, in different local modes.  Together with the companion
parameter-boundary theorem, the denominator chart used below covers
the whole visible coupled factor.

This does not extract every hidden coefficient denominator in the
standard-basis certificates, close every special/projective boundary,
prove component exhaustiveness, finish `P_5 -> Delta_3`, or resolve the
global Krenn--Gu conjecture.

## The coupled factor

The generic degree-five marking cover contains the coefficient

```text
C =
 a^2 f(r-1)+abf(r+1)+a(r+1)+b(r-1).               (1)
```

Write

```text
P = a^2 f+abf+a+b,
Q =-a^2 f+abf+a-b,                                 (2)
```

so that

```text
C=rP+Q.                                             (3)
```

On the chart `P!=0`, the divisor `C=0` is the rational slope graph

```text
r=-Q/P
 =(a^2 f-abf-a+b)/(a^2 f+abf+a+b).                (4)
```

The component relation remains

```text
Phi =
 a^2 b f phi^2+a^2 f^2
 -b^2 f^2+b^2 phi^2-bf-1=0.                       (5)
```

Thus the branch function field is

```text
K=C(a,b,f)[phi]/(Phi),                              (6)
```

with the rational slope (4).

## The missing denominator chart

The identities

```text
P+Q=2a(bf+1),
P-Q=2(a^2 f+b)                                     (7)
```

show what happens when `P=0` on `C=0`.  Then `Q=0` as well.  The case
`a=0` would force `b=0`, contradicting `Phi=-1`; hence `bf=-1`.
The other equation gives

```text
a^2 f+b=0.
```

Substituting `f=-1/b` yields `a^2=b^2`.  Therefore the missing chart is
contained in

```text
bf=-1,       a=b or a=-b,                           (8)
```

which is already excluded by
[`P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md).

## One-minor Fitting obstruction

For either direction, let

```text
M_D(t)z=0                                           (9)
```

be the fourteen mixed binary equations, and normalize a genuine binary
extension by

```text
A_D(z)=1,       wB_D(z)-1=0.                       (10)
```

After substituting (4), exact standard-basis reduction gives:

```text
D_01:
(
 Phi,
 M_01(t)z,
 A_01-1,
 wB_01-1,
 H^(mode 1)_0457
)=(1),                                             (11)

D_23:
(
 Phi,
 M_23(t)z,
 A_23-1,
 wB_23-1,
 H^(mode 0)_0137
)=(1).                                             (12)
```

For a ternary lift, every one-marked map factors through a
three-dimensional target local space and therefore has rank at most
three.  Equations (11)--(12) say that every genuine binary neighbour
has rank four in mode one for `D_01` or mode zero for `D_23`.
Consequently no neighbour on the coupled divisor lifts to `H22`.

## Geometric interpretation

The generic proof used factor relations to cover a degree-five Fitting
scheme.  Setting the last linear coefficient to zero removes that
chart, but it also exposes a transverse local mode: the four finite
survivors in a generic modular fibre all have the mode-one `0457`
minor nonzero.  Translating the incidence from mode zero to mode one
turns the exceptional divisor into the unit ideal (11).

This is a useful general lesson for the remaining boundaries: a
degenerate Fitting chart in one local mode can become a single
determinantal obstruction in another.

## Honest frontier

The visible factors in the generic branch cover are now addressed:

```text
r^2-1,
a b f phi,
a^2-b^2,
bf+1,
a^2 f+b,
C.
```

Some of these factors meet in deeper strata, and a complete
denominator extraction from every standard-basis certificate is still
required before claiming the full component incidence is closed.
Other pure components may also exist.  No satisfying graph and no
global nonexistence proof is claimed.

## Verification

Run:

```text
tmp/codex_verify_env/Scripts/python.exe \
  verify_p5_h22_disjoint_mixed_star_coupled_slope_boundary_obstruction.py

tmp/codex_verify_env/Scripts/python.exe \
  audit_p5_h22_disjoint_mixed_star_coupled_slope_boundary_obstruction.py
```

The primary verifier reconstructs the rational slope, checks (1)--(8),
builds the one-marked maps in modes one and zero, and requires the two
characteristic-zero ideals (11)--(12) to reduce to `(1)`.

The independent audit imports nothing from the primary verifier.  At a
component point over `F_11`, it computes the coupled slope, exhausts all
marked bases, and checks the selected determinant on every genuine
projective extension direction.  This is corroboration only;
(11)--(12) prove the theorem over `C`.
