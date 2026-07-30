# Zero-slope `H22` boundary on the disjoint mixed-star component

## Status

This is an exact characteristic-zero slope-endpoint theorem over the
generic point of the eighth pure-`P_4` component.

At `r=0`, the weighted `D_01` contraction admits no genuine binary
neighbour.  The `D_23` contraction does acquire a rank-six binary
degeneration, but every genuine direction violates one of two
mode-zero one-marked rank conditions.  Hence neither direction lifts
to `H22`.

If weighted slopes are restricted to the residual torus `r!=0`, this
endpoint is outside that open chart.  The theorem closes it in the
natural projective compactification of the contraction pencil.

This does not close special parameter or projective boundaries,
component exhaustiveness, the complete `P_5 -> Delta_3` obstruction,
or the global prize conjecture.  No graph satisfying the prize equation
and no global nonexistence proof is claimed.

## The intrinsic `D_01` content ledger

The generic `D_01` proof chooses seven base rows

```text
0,1,2,3,7,8,10
```

of the `14 x 8` mixed matrix and adjoins rows

```text
4,5,6,9,11,12,13
```

to obtain seven maximal minors.  It also uses the `7 x 7` pivot on
columns

```text
0,1,2,4,5,6,7.                                    (1)
```

Reduce these eight determinants by the component relation

```text
Phi =
 a^2 b f phi^2+a^2 f^2
 -b^2 f^2+b^2 phi^2-bf-1.                         (2)
```

Their exact parameter contents factor over `C[a,b,f,r]`.  The seven
maximal minors have common square-free numerator support

```text
a f r(af-1)(af+1)K(r-1)(r+1)(bf+1),               (3)
```

where

```text
K=-a^2 f^2+b^2 f^2+bf+1.                          (4)
```

The rank pivot has common support

```text
(af-1)(af+1)K(r-1)(r+1)(bf+1),                    (5)
```

but not `a`, `f`, or `r`.  Four maximal minors also contain

```text
X=afr+af-r+1,                                      (6)
```

while the other three do not.  Every denominator is a power of

```text
b(a^2 f+b).                                        (7)
```

The verifier checks the exact constants and multiplicities of all
eight contents.

Thus `a`, `f`, `r`, and `X` are not common base divisors of the
determinantal rank chart.  Every factor common with the pivot has
already been closed: `af=+/-1` by the `af/aphi` theorem, `r=+/-1` by
the equal/opposite theorem, and the `K`, `bf+1`, `b`, and `a^2f+b`
pieces by the parameter-pivot decompositions.

Although `r=0` is not a rank-chart base divisor, it makes all seven
maximal minors vanish and changes the mixed-kernel dimension.  That
geometric degeneration is addressed directly below.

## The two endpoint contractions

At `r=0`, the contractions become coordinate deletions:

```text
D_01^0(u)=(u_1,u_2,u_3,u_4),
D_23^0(u)=(u_0,u_1,u_3,u_4).                      (8)
```

For either direction let

```text
M_D(t)z=0                                          (9)
```

be the fourteen mixed binary equations, with diagonal coefficients
`A_D(z),B_D(z)`.

## Direct binary obstruction for `D_01^0`

Over the component field

```text
K=C(a,b,f)[phi]/(Phi),                             (10)
```

exact standard-basis reduction gives

```text
(
 Phi,
 M_01^0(t)z,
 A_01^0(z)-1
)=(1).                                             (11)
```

If a vector in the mixed kernel had `A_01^0!=0`, it could be scaled to
a point of (11).  Therefore the mixed equations force

```text
A_01^0=0.                                          (12)
```

A genuine binary neighbour requires both diagonals nonzero, so the
`D_01^0` binary incidence is empty.

## Unsplit Fitting obstruction for `D_23^0`

The second endpoint is different: its mixed matrix can have rank six
and genuine binary extension lines do occur.  Normalize them by

```text
A_23^0(z)=1,       wB_23^0(z)-1=0.                 (13)
```

Let `H_0137,H_0157` be the determinants of rows `0137` and `0157` of
the mode-zero one-marked map.  Without first classifying the rank locus,
exact reduction gives the unsplit identity

```text
(
 Phi,
 M_23^0(t)z,
 A_23^0(z)-1,
 wB_23^0(z)-1,
 H_0137,
 H_0157
)=(1).                                             (14)
```

A ternary lift factors this marked map through a three-dimensional
target local space and would have rank at most three.  Equation (14)
says every genuine binary direction has marked rank four.  Hence none
lifts to `H22`.

## Geometric interpretation

At a generic nonzero slope, the selected `D_23` Fitting scheme is a
line and the `D_01` scheme has degree five.  At the projective endpoint,
the roles simplify differently:

```text
D_01^0: mixed kernel lies in a diagonal hyperplane;
D_23^0: rank-six kernel, but transverse marked rank four.
```

This is a vector-bundle degeneration.  The correct invariant is not
the degree of a chosen determinantal chart, which jumps, but whether
the kernel bundle meets the open two-diagonal locus and then the
rank-at-most-three marked degeneracy locus.  Equations (11) and (14)
show that it does not.

## Honest frontier

The compactified slope fibres `r=0,+1,-1` are now closed over the
generic component point.  The two nonzero fibres `+1,-1` already fail
at binary level; at zero, `D_01` fails at binary level and `D_23`
requires the two-minor ternary obstruction.

The intrinsic contents of the selected `D_23` minors and the selected
`D_01` minors plus their rank pivot are now recorded.  Denominators of
the final three generic `D_01` Fitting unit certificates still need an
intrinsic treatment, as do deeper component-parameter intersections.
Other pure components may exist.  The global Krenn--Gu conjecture
remains unresolved.

## Verification

Run:

```text
tmp/codex_verify_env/Scripts/python.exe \
  verify_p5_h22_disjoint_mixed_star_zero_slope_boundary_obstruction.py

tmp/codex_verify_env/Scripts/python.exe \
  audit_p5_h22_disjoint_mixed_star_zero_slope_boundary_obstruction.py
```

The primary verifier reconstructs the component family, checks all
eight exact `D_01` determinant contents, and requires (11) and (14) to
reduce to `(1)` over characteristic zero.

The independent audit imports nothing from the primary verifier.  It
exhausts every affine marking at the two generic component points over
`F_11` and `F_13`.  It finds no genuine `D_01^0` binary direction.  For
`D_23^0`, each field has one genuine marking, mixed rank six, and
respectively `10` and `12` genuine projective directions; every one has
mode-zero marked rank four and at least one selected minor nonzero.
This finite-field census is corroboration only; (11) and (14) are the
proof over `C`.
