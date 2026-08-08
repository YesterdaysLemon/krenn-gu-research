# Weighted `H22` on the diagonal-quadric component

## Status

**SUPERSEDED EXPLORATORY FRONTIER; NOT A THEOREM OR A CERTIFICATE.**

This note records the exploratory route that reached the seventh,
diagonal-quadric component.  Its generic incidence has since been
excluded by the projective Segre-join/properness theorem in
[`P5_H22_DIAGONAL_QUADRIC_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_DIAGONAL_QUADRIC_COMPONENT_GENERIC_OBSTRUCTION.md).
The calculations below remain useful provenance, including their null
timeout outcomes, but they are not the proof.  Special component and
slope divisors, unclassified pure components, all of `H22`, and the
global prize problem remain open.

The useful conclusion is structural.  The remaining calculation can be
posed over a quadratic function field as a Fitting-ideal problem for a
linear extension map.  Small finite-field scans were used only to choose
charts and reject misleading specializations.  They are not proof over
characteristic zero.

## A smaller diagonal-quadric basis

On the dense normal-form chart put

```text
U=C+H,       S=1+CH,       T=H+CE^2,
S^2=UT.                                             (1)
```

Use the four rows

```text
y_1=(1,0,0,-1),       y_2=(0,1,-1,0),
k_0=(1,0,0,1),        k_1=(0,1,1,0),
x_1=(1,C+1,C-1,1),    x_2=(H+E,1,1,H-E),
u_0=(E,-1,-1,-E),     u_1=(1,-1,1,1).
```

After harmless row scalings, a pure basis is

```text
alpha_0=U u_0+S u_1,   beta_0=u_0,
alpha_1=y_1,           beta_1=x_1,
alpha_2=y_2,           beta_2=x_2,
alpha_3=T k_0-S k_1,   beta_3=k_0.                  (2)
```

Direct symbolic expansion modulo (1) gives

```text
T_w=0 for every w in {0,1}^4 except w=1111,
T_1111=-4S.                                         (3)
```

Thus (2) represents the desired pure compression wherever the displayed
row scalings and `S` are nonzero.

## Quadratic-function-field chart

Set

```text
l=S/U.
```

After scaling `alpha_0,alpha_3,beta_2`, equations (1)--(2) become

```text
alpha_0=u_0+l u_1,
alpha_3=l k_0-k_1,

(1-l^2) beta_2
  =(C(l^2-E^2)+E(1-l^2), 1-l^2, 1-l^2,
    C(l^2-E^2)-E(1-l^2)),                           (4)
```

over

```text
K=Q(C,l,r)[E] /
  (-C^2 E^2+C^2 l^2+C E^2 l-C l-l^2+1),            (5)
```

where `r` is the weighted diagonal slope.  The relation is linear in
`E^2`:

```text
E^2=(C^2 l^2-C l-l^2+1)/(C(C-l)).                  (6)
```

This replaces the earlier elliptic coordinates by a quadratic extension
of a rational function field.  It is the main reframe: the remaining
generic problem is no longer an unrestricted chart search.

For either diagonal direction `D01` or `D23`, form the `14 x 8` matrix
`M(t)` of the fourteen mixed binary coefficients.  Its entries are
three-row permanents, so they can be built directly without expanding
four-row permanents.  A binary extension exists precisely on the
rank-drop scheme

```text
rank M(t) <= 7,                                     (7)
```

subject to nonvanishing of the two pure diagonal coefficients.  If (7)
has genuine points, a ternary lift also requires all four one-marked
maps to have rank at most three.

## Exact special fibres

Two rational elliptic-chart fibres were eliminated exactly with
Singular.

At

```text
(e,x,Y)=(2,-3,-12),
```

the `D01` marking ideal is

```text
(r-1)t_2+12r-3,
t_1,
(12r-12)t_0+(2r-1)t_3-2r+2,
t_3^2-t_3,                                         (8)
```

while the `D23` marking ideal is the unit ideal.  Thus the first
direction has two affine sheets on this fibre.

At

```text
(e,x,Y)=(2,-3/4,3/8),
```

both affine marking ideals are the unit ideal.

These calculations are exact but do not prove generic emptiness.
Affine marking space is not proper.  In a projective compactification,
invalid markings with `beta_i` proportional to `alpha_i` survive on the
boundary, so a survivor may escape to infinity under specialization.
The attempted one-fibre properness argument therefore fails.

## Finite-field reconnaissance

The following scans are deliberately small and diagnostic.

At the integral surface point

```text
(C,E,H,r)=(1,1,2,2),
```

which has `l=1`, complete affine marking scans gave:

| field | direction | rank-eight markings | rank-seven markings | genuine |
|---|---:|---:|---:|---:|
| `F_5` | `D01` | 624 | 1 | 1 |
| `F_5` | `D23` | 623 | 2 | 2 |
| `F_7` | `D01` | 2400 | 1 | 1 |
| `F_7` | `D23` | 2399 | 2 | 2 |

Every genuine survivor in this table has the mode-zero marked minor on
rows `0267` nonzero.  The `D01` survivors also have extension coordinate
`z_6` nonzero and share the cofactor row chart

```text
(0,1,3,7,8,9,11),
```

while the `D23` survivors have `z_4` nonzero and share

```text
(0,1,2,3,5,7,9).                                  (9)
```

This initially suggested a compact one-minor Fitting certificate.
However, the sample lies on the excluded divisor `1-l^2=0`.

There are no points satisfying the nonzero ratio-chart gates over
`F_5`.  Over `F_7` there are exactly four such points:

```text
(C,E,H)=(3,3,5),(3,4,5),(4,3,2),(4,4,2).
```

At slope `r=2`, complete scans of all `7^4` affine markings in both
directions found no genuine extension.  Seven of the eight
point/direction scans had rank eight everywhere.  The remaining `D23`
scan had one rank-drop marking, but its diagonal nonvanishing gate
failed.  Therefore the isolated survivors and the common `0267` minor
seen above may be boundary phenomena; they are not evidence for the
generic survivor scheme.

The finite-field calculations concern rational markings only.  They do
not exclude points over algebraic extensions and are not a
characteristic-zero argument.

## Exact computations that did not finish

Several exact characteristic-zero formulations were tried:

- direct elimination in the original elliptic function field;
- maximal-minor ideals in the normal form and in the ratio chart;
- projective extension-kernel charts;
- cofactor substitution on the two charts in (9);
- adjoining the mode-zero `0267` marked minor to the cofactor equations.

Each generic Gröbner-basis job exceeded its 600-second cap.  One
algebraic-minimal-polynomial formulation was rejected because Singular
does not accept the required nested transcendental/algebraic
coefficient field in that form.  These are null computational outcomes,
not mathematical evidence.

One exact inspection did finish.  Thirteen selected maximal minors were
reduced by (5) and factored.  Recurrent simple factors include

```text
t_3,  l t_3+1,  t_2+(l^2-1),
```

and, in the two diagonal directions, the sign-related factors

```text
(l-1)t_0-1,     (l+1)t_0+1.                         (10)
```

Every selected minor also has a large remaining factor, and several
have no simple marking factor at all.  Thus (10) is useful for choosing
branches but does not imply that the rank-drop scheme is supported on
those hyperplanes.  The Gröbner basis of the selected-minor ideal still
timed out.  Substituting `t_3=0` and `l t_3+1=0` before determinant
expansion reduced the expressions, but all four direction/branch
Gröbner jobs also exceeded their 300-second caps.

## Historical next proof target

The clean next task is:

1. work over the quadratic field (5), reducing every coefficient to
   `a+bE` by (6);
2. determine whether the saturated maximal-minor ideal of `M(t)` is the
   unit ideal on `C(C-l)(1-l^2)r` and the two diagonal gates;
3. if it is not unit, compute the finite survivor algebra and test the
   four marked Fitting ideals there;
4. cover the cofactor and marking-at-infinity boundaries separately.

The simple factors in (10) suggest doing step 2 branchwise, while
retaining the complementary large-factor branch explicitly.  Dropping
that complement would be an invalid case split.

The generic quadratic-field calculation was ultimately bypassed.  The
successful proof fixes the unmarked extension eight-plane, identifies
binary marking with a Segre join, proves one exact projective fibre
empty (including the join base-point exceptional divisor), and invokes
properness.  Nothing in the unfinished computations above is promoted
to evidence for that theorem.

## Reproduction

The current exploratory scripts are:

```text
tmp/explore_p5_h22_diagonal_quadric_specialized_exact.py
tmp/explore_p5_h22_diagonal_quadric_factor_ratio_rankdrop.py
tmp/explore_p5_h22_diagonal_quadric_random_modular.py
tmp/explore_p5_h22_diagonal_quadric_generic_samples.py
tmp/explore_p5_h22_diagonal_quadric_kernel_cofactor_fitting.py
```

Only successful exact eliminations and completed finite scans are
reported above.  A timeout or a finite-field sample must not be promoted
to a generic theorem.
