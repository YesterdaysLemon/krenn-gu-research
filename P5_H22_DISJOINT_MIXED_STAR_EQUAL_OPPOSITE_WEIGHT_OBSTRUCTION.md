# Equal- and opposite-weight `H22` obstruction on the disjoint mixed-star component

## Status

This is an exact characteristic-zero slope-boundary theorem over the
generic point of the eighth pure-`P_4` component.

For each of the two weighted `H22` contractions, neither equal source
weight `r=1` nor opposite source weight `r=-1` admits even a genuine
binary `Delta_2` extension.  Thus no ternary lifting argument is needed
on these two residual-torus divisors.

This extends
[`P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md)
across two special slope fibres.  It does not close all exceptional
slopes, component-parameter divisors, projective marking boundaries,
component exhaustiveness, or the global Krenn--Gu conjecture.

## Component and weighted contractions

Use the component family with relation

```text
Phi =
 a^2 b f phi^2+a^2 f^2
 -b^2 f^2+b^2 phi^2-bf-1 = 0.                    (1)
```

Work over the generic component-parameter field

```text
F=C(a,b,f),       K=F[phi]/(Phi).                  (2)
```

For marked bases

```text
beta_i(t)=beta_i+t_i alpha_i,                      (3)
```

the two source contractions are

```text
D_01^r(u)=(r u_0+u_1,u_2,u_3,u_4),
D_23^r(u)=(u_0,u_1,r u_2+u_3,u_4).                (4)
```

Fix

```text
epsilon in {1,-1}.                                 (5)
```

For either direction `D`, let

```text
z=(x_0,...,x_3,y_0,...,y_3)
```

be the eight extension coordinates.  Expanding the binary matching
tensor gives fourteen mixed coefficients

```text
g_(D,epsilon,1),...,g_(D,epsilon,14),              (6)
```

linear in `z`, and two diagonal coefficients

```text
A_(D,epsilon), B_(D,epsilon).                      (7)
```

A genuine binary neighbour is precisely a nonzero extension with

```text
g_(D,epsilon,j)=0  for all j,
A_(D,epsilon) B_(D,epsilon) != 0.                  (8)
```

## Diagonal-annihilation ideals

The special slopes select opposite diagonal obstructions.  Define

```text
J_(D,1) = (
  Phi,
  g_(D,1,1),...,g_(D,1,14),
  A_(D,1)-1
),

J_(D,-1) = (
  Phi,
  g_(D,-1,1),...,g_(D,-1,14),
  B_(D,-1)-1
).                                                  (9)
```

in

```text
F[phi,t_0,t_1,t_2,t_3,z_0,...,z_7].               (10)
```

Exact standard-basis reduction gives all four identities

```text
J_(D_01, 1)  = (1),
J_(D_23, 1)  = (1),
J_(D_01,-1)  = (1),
J_(D_23,-1)  = (1).                               (11)
```

If a mixed-kernel vector had `A_(D,1) != 0`, scaling it would give a
point of `J_(D,1)`.  Thus the mixed equations force

```text
A_(D,1)=0.                                         (12)
```

Likewise they force

```text
B_(D,-1)=0.                                        (13)
```

A genuine binary neighbour requires both diagonals nonzero.  Therefore
the equal- and opposite-weight binary incidences are empty over the
generic point of the component.

## Why this is a useful translation

The generic-slope theorem first classified the determinantal marking
scheme and then used ternary Fitting minors.  At `r^2=1`, that chosen
determinantal chart degenerates, but the full incidence simplifies.
Normalizing just the obstructed diagonal turns the apparently
exceptional slope into four unit-ideal calculations.

In geometric language, the kernel bundle of the mixed-coefficient
matrix acquires special fibres, but at `r=1` it lies in the first
diagonal hyperplane and at `r=-1` it lies in the second.  Either way it
misses the open set where both diagonal linear forms are nonzero.

## Honest frontier

The eighth component is now excluded:

1. at its generic weighted slope by the determinantal/Fitting theorem;
2. at the equal-weight slope `r=1`; and
3. at the opposite-weight slope `r=-1`.

The remaining work is to extract the other coefficient denominators
from the generic standard-basis certificates, specialize their
irreducible slope/parameter divisors, cover the projective marking
charts, and decide component exhaustiveness.  The complete
`P_5 -> Delta_3` obstruction and the global prize conjecture remain
unresolved.

Two subsequent theorems close twelve generic parameter/coordinate
branches and the principal coupled slope-parameter divisor:
[`P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md),
[`P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md).

## Verification

Run:

```text
tmp/codex_verify_env/Scripts/python.exe \
  verify_p5_h22_disjoint_mixed_star_equal_opposite_weight_obstruction.py

tmp/codex_verify_env/Scripts/python.exe \
  audit_p5_h22_disjoint_mixed_star_equal_opposite_weight_obstruction.py
```

The primary verifier reconstructs the component family and all four
characteristic-zero diagonal-normalization ideals in (11), then
requires each reduced basis to be exactly the unit ideal.

The independent audit imports nothing from the primary verifier.  At
two component points over independent finite fields, it exhausts all
affine marked bases for both directions and both slopes and verifies
that no mixed-matrix kernel meets the two-diagonal open set.  This
finite-field audit is corroboration only; (11) is the proof over `C`.
