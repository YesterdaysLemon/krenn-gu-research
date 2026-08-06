# A coefficient-quadratic `H22` boundary of the disjoint mixed-star component

## Status

This is an exact characteristic-zero theorem at the generic point of a
new irreducible quadratic branch on the eighth pure-`P_4` component.

For both weighted directions, the complete genuine binary incidence is
disjoint from the mode-zero marked-rank-at-most-three locus.  Hence the
generic weighted `H22` incidence is empty on this branch.

This does not close special divisors inside the branch, classify every
factor appearing in generic Bezout certificates, prove component
exhaustiveness, finish `P_5 -> Delta_3`, or resolve the global prize
conjecture.  No graph satisfying the prize equation and no global
nonexistence proof is claimed.

## How the divisor appeared

After removing redundant maximal minors from the three final generic
`D_01` Fitting ideals, one cleared Bezout certificate contained

```text
A=a^2 f^2+2bf+1.                                  (1)
```

One certificate can contain accidental syzygy factors, so (1) was not
treated as geometry merely because it appeared there.  Instead,
normalize the divisor itself.  Since `f!=0` at its generic point,

```text
b=-(a^2 f^2+1)/(2f).                              (2)
```

Substitution into the component relation

```text
Phi =
 a^2 b f phi^2+a^2 f^2
 -b^2 f^2+b^2 phi^2-bf-1                         (3)
```

gives

```text
Phi|_A =
 -(af-1)(af+1)Q/(4f^2),                           (4)

Q =
 (a^2 f^2+1)phi^2+f^2(a^2 f^2-3).                (5)
```

The factors `af=+/-1` belong to previously closed branches.  The new
sheet is

```text
A=0,       Q=0.                                   (6)
```

Its function field is the quadratic extension

```text
C(a,f,r)[phi]/(Q),                                (7)
```

with `b` given by (2).

The discriminant of `Q` in `phi` is

```text
-4 f^2(a^2 f^2-3)(a^2 f^2+1).                    (8)
```

After removing the square factor `-4f^2` over `C(a,f)`, the two
remaining irreducible factors occur with odd multiplicity.  Thus the
discriminant is not a square and `Q` is irreducible.

## Unsplit Fitting ideals

For either direction `D` let

```text
M_D(t)z=0                                         (9)
```

be the fourteen mixed binary equations, and write `A_D(z),B_D(z)` for
the two diagonal coefficients.  Normalize the genuine binary open set
by

```text
A_D(z)=1,       wB_D(z)-1=0.                      (10)
```

Let `H_0137,H_0157` be the determinants of rows `0137` and `0157` of
the mode-zero one-marked map.

Work over `C(a,f,r)` with `b,phi` algebraic variables satisfying
(1) and (3).  Exact standard-basis reduction gives, independently for
`D_01` and `D_23`,

```text
(
 A,
 Phi,
 M_D(t)z,
 A_D(z)-1,
 wB_D(z)-1,
 H_0137,
 H_0157
)=(1).                                            (11)
```

These are full, unsplit incidence ideals.  They do not assume that the
generic degree-five marking cover specializes flatly to (6).

A ternary lift factors every one-marked map through a
three-dimensional target local space, so all its `4 x 4` minors vanish.
Equation (11) says that every genuine binary neighbour on the branch
has mode-zero marked rank four.  Therefore no neighbour lifts to
`H22`.

## Geometric interpretation

The normalization (2)--(5) turns an opaque coefficient factor into a
double cover of the `(a,f)`-plane.  The branch divisor is therefore
not best viewed as a bad Gröbner denominator.  It is a quadratic base
change of the component family, and Fitting ideals commute with that
base change.

The proof also avoids a subtle specialization error.  Rather than
specializing the generic three-chart marking cover, which might acquire
new components, (11) intersects the complete binary incidence directly
with the marked degeneracy locus.  This is the determinantal-geometry
translation doing real work: normalization first, unsplit Fitting
incidence second.

## Honest frontier

The generic points of the new branch (6) are now closed in both
weighted directions.  Its deeper parameter and slope intersections
remain open unless covered by an earlier boundary theorem.

Other factors in the one cleared Bezout certificate have not been
promoted to geometric divisors.  Some are already known chart factors
or the closed coupled slope divisor; the remaining candidates require
either independent certificate comparison or their own normalized
incidence calculation.  Three subsequent linear slope graphs have now
passed that test and are closed in
[`P5_H22_DISJOINT_MIXED_STAR_LINEAR_SLOPE_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_LINEAR_SLOPE_BOUNDARY_OBSTRUCTION.md).
Other pure components may also exist.  The global Krenn--Gu conjecture
remains unresolved.

## Verification

Run:

```text
python \
  verify_p5_h22_disjoint_mixed_star_coefficient_quadratic_boundary_obstruction.py

python \
  audit_p5_h22_disjoint_mixed_star_coefficient_quadratic_boundary_obstruction.py
```

The primary verifier derives (4), checks irreducibility of `Q`, builds
the complete mixed and one-marked maps, and requires both
characteristic-zero ideals (11) to reduce to `(1)`.

The independent audit imports nothing from the primary verifier.  It
exhausts all affine markings at generic points of the new sheet over
`F_7` and `F_13`.  Across both directions it checks every genuine
projective extension against both minors and marked rank four.  At the
`F_13` point, the two genuine `D_01` directions are split between the
two minors, showing that the two-minor presentation is genuinely
needed there.  The finite-field census is corroboration only; (11) is
the characteristic-zero proof.
