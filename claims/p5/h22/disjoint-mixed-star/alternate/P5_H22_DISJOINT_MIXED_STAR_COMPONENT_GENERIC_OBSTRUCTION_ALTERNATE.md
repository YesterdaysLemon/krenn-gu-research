# Generic weighted `H22` obstruction on the disjoint mixed-star component — alternate proof

## Status

**Alternate independent proof.**  This document is the weighted-`H22`
theorem for the eighth pure-`P_4` component as proved on the former
`main` line (commit `21f77b3`, merged into the canonical line in
`72780ac`).  The canonical line reached the same conclusion by a
materially different argument (a determinantal marking chart with a
degree-five `01` Fitting scheme and seven selected `8 x 8` minors);
that proof is
[`P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](../P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md).
Both proofs are retained: identical claim, disjoint computation paths.
The overlap and independence ledger is in
[`MERGE_AUDIT_REPORT.md`](../../../../../docs/audits/MERGE_AUDIT_REPORT.md).

This is an exact characteristic-zero obstruction on the generic
diagonal-source orbit of the eighth pure-`P_4` component proved in
[`P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`](../../../../p4/components/disjoint-mixed-star/P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md).

For the two weighted diagonal-hyperplane pencils required by `H22`:

1. every marking with a nonzero binary-extension kernel in the `01`
   pencil satisfies `t_1 t_2 = 0`, by a single one-minor locus
   certificate; and every marking with a nonzero kernel in the `23`
   pencil satisfies `t_1 = t_2 = t_3 = 0`, by three exact unit-ideal
   chart certificates; and
2. on every marking stratum, each genuine binary survivor has a
   rank-four mode-zero one-marked contraction and therefore cannot
   extend to a ternary local map.

Thus a relevant pure binary plane cannot be generic on this component
in a hypothetical `H22` restriction.  All eight certified pure-`P_4`
component orbits are now generically closed for weighted `H22`, as
they already were for marked `H31`.

This does **not** close special parameter or slope divisors, the
component's projective boundary, all of `H22`, component
exhaustiveness, or the global prize problem.

This theorem replaces the exploratory finite-field working note
[`P5_H22_DISJOINT_MIXED_STAR_WORKING_NOTE.md`](../P5_H22_DISJOINT_MIXED_STAR_WORKING_NOTE.md),
whose two modular marking loci are exactly the characteristic-zero
loci proved here.

## Component function field and weighted pencils

Use the pure-factor bases `(alpha_i,beta_i)` of the component
theorem, marked by `beta_i(t)=beta_i+t_i alpha_i`, over

```text
K=C(a,b,f)[phi]/(Phi),
```

with `Phi` the irreducible component equation.  As in the earlier
weighted `H22` theorems, the two `H22` diagonal-hyperplane pencils
act on every local row `u` by

```text
D_01^r(u)=(r u_0+u_1,u_2,u_3,u_4),
D_23^r(u)=(u_0,u_1,r u_2+u_3,u_4),                  (1)
```

with the slope `r` transcendental over the component field.  Write
`x_i,y_i` for the fifth-coordinate extensions of `alpha_i` and
`beta_i(t)`, and `z=(x,y)`.  For either pencil the fourteen mixed
binary coefficients form a linear system `M(t)z=0`; the two diagonal
coefficients are `A(z)` and `B(z)`, and a genuine binary survivor has
`A(z)B(z) != 0`.

## A `t`-free elimination of the marked extensions

The mixed word `e_m` (a single `1` in mode `m`) contains `y_m` with a
coefficient equal to the `3 x 3` weighted permanent of the other
three `alpha` rows.  These four coefficients are independent of `t`.
In the `01` pencil they are, modulo `Phi` and up to nonzero constants,

```text
(r-1)(af-1)(af+1)(bf+1)/(b(a^2 f+b)),
phi(r-1)(bf+1),
phi(r-1),
a phi(r+1)(bf+1)(a^2f^2+2bf+1)/(a^2 f+b),           (2)
```

and in the `23` pencil

```text
(r+1)(af-1)(af+1)(bf+1)/(a^2 f+b),
(r-1)(bf+1),
(r-1),
(r-1)(bf+1)(a^2bf^2+2a^2f+b)/(a^2 f+b).             (3)
```

Every factor has a nonzero resultant with `Phi`, so each coefficient is
nonzero in `K(r)` and therefore invertible on the declared generic dense
open; its zero locus is contained in the explicitly excluded
parameter/slope divisors.  Solving the four single-`1` words for `y` and
substituting into the ten remaining mixed words therefore converts
the binary-extension condition exactly: the kernel of the `14 x 8`
mixed matrix is nonzero at a marking if and only if the reduced
`10 x 4` system

```text
G(t)x=0                                              (4)
```

has a nonzero solution, and every kernel vector arises from such an
`x`.  The primary verifier checks the vanishing of the substituted
single-`1` words identically and extracts (4) with exact linearity
certificates.

## The `01` pencil: one factored minor

Select the four rows of (4) labelled by the mixed words

```text
0011, 0110, 1001, 1011.
```

Their `4 x 4` determinant satisfies the exact identity

```text
det G_(0011,0110,1001,1011) = u * t_1 t_2   (mod Phi),   (5)
```

where `u` is nonzero in `K(r)`, hence invertible on the declared generic
dense open; its factors lie in the list

```text
2, a, b, f, r, r-1, r+1, af-1, af+1, bf+1, a^2f+b,
a^2f^2+2bf+1, b^2f^2+bf+1-a^2f^2, af(r+1)-(r-1), phi,
```

each with a nonzero resultant against `Phi`, hence invertible in `K(r)`
on the declared dense open.  The replayed certificate inverts
`t_1 t_2` and returns the unit ideal, and the determinant's exact
factorization is recorded in the verifier ledger.  A nonzero kernel
forces all `4 x 4` minors of (4) to vanish; by (5) this forces

```text
t_1 t_2 = 0.                                         (6)
```

This is precisely the marking locus observed modularly in the working
note, now as a one-line function-field identity.

The two sheets of (6) refine the same way.  Restricting (4) to
`t_1=0` and to `t_2=0`, the rows

```text
0011, 1001, 1010, 1011      on t_1=0,
0011, 0101, 1001, 1011      on t_2=0
```

give the exactly factored determinants

```text
det = u_1 (phi(t_0-1)-f) t_2                (mod Phi, t_1=0),
det = u_2 ((af(r+1)-(r-1))t_1-(r+1)) t_3    (mod Phi, t_2=0),  (5')
```

with `u_1,u_2` nonzero in `K(r)` and invertible on the declared dense
open, certified by the same inverted-product unit-ideal calculations.
Hence the complete `01` marking locus is the union of four explicit
strata:

```text
t_1=t_2=0;          t_1=0, phi(t_0-1)=f;
t_2=t_3=0;          t_2=0, (af(r+1)-(r-1))t_1=r+1.       (6')
```

## The `23` pencil: three chart certificates

For each chart `t_1 != 0`, `t_2 != 0`, `t_3 != 0`, the ideal
generated by all `4 x 4` minors of (4), the component equation
`Phi`, and the chart inversion is the unit ideal.  Exact
characteristic-zero calculation proves all three.  Hence every
marking with a nonzero kernel satisfies

```text
t_1 = t_2 = t_3 = 0,                                 (7)
```

with `t_0` free, again exactly the modular locus of the working note.

## Rank-four one-marked contractions

For a ternary `H22` lift, the mode-zero one-marked contraction
through the other three binary planes must have rank at most three.
Let `P(z)` be its `8 x 4` coefficient matrix; its last column is
`z`-free and its first three columns are linear in `z`, so its
`4 x 4` minors are cubic in `z` and transform covariantly under the
kernel substitution.

On each of the five marking strata — the four strata (6') for the
`01` pencil and the line (7) for the `23` pencil — adjoin to the
reduced system (4) the two minors of `P` in rows

```text
(0,1,3,7),        (0,1,5,7),
```

and the saturation `w A(z)B(z)-1`.  All five resulting ideals are
the unit ideal over `K(r)`.  Consequently no genuine binary survivor
has both selected minors zero: every genuine survivor's mode-zero
one-marked map has rank four, and no ternary lift exists.

## Why this closes generic weighted `H22`

By the frontier reduction, an `H22` local family needs the `Delta_2`
image of at least one weighted pencil to be sharp, in every subfamily
of `(a,b)` supports: for `a b != 0` both pencils are sharp, and for
exactly one of `a,b` nonzero the corresponding single pencil is
sharp.  A sharp pencil requires a genuine binary survivor that lifts
ternarily.  Both pencils are closed above, so the generic point of
the disjoint mixed-star component supports no weighted `H22`
incidence in any subfamily.

## Honest frontier

The theorem is over the function field; denominators and the
displayed factors exclude special parameter and slope divisors, and
the component's projective boundary is untreated.  Component
exhaustiveness for the pure-`P_4` compression locus and the rest of
`H22` remain open, as does the global prize problem.

Update: the excluded slope divisors `r in {0, 1, -1, infinity}` of
both pencils are now closed over the generic component point —
`r = +-1` at binary level by universal reconstruction kernels and
two-row unit identities, `r = 0/infinity` by exact identification
with the four `H31` coordinate frames and transport of the verified
`H31` theorem:
[`P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md`](../../../../../P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md),
`verify_p5_h22_disjoint_mixed_star_slope_r1_binary_obstruction.py`,
`verify_p5_h22_disjoint_mixed_star_slope_rm1_binary_obstruction.py`,
`verify_slope_boundary_frame_identifications.py`.  The coupled
divisor `af(r+1)-(r-1)=0` of the `01` pencil, slope-parameter
intersections, and the projective boundary remain open.

## Verification

Run:

```text
python claims/p5/h22/disjoint-mixed-star/alternate/verify_p5_h22_disjoint_mixed_star_component_generic_obstruction_alternate.py

python claims/p5/h22/disjoint-mixed-star/alternate/audit_p5_h22_disjoint_mixed_star_component_generic_obstruction_alternate.py
```

The primary verifier reconstructs the marked weighted systems for
both pencils, certifies the `t`-free elimination (2)--(3) with
nonzero resultants against `Phi`, checks the substituted single-`1`
words vanish identically, extracts (4) with exact linearity
certificates, proves the three one-minor locus certificates behind
(5)--(5') with recorded factorizations, and proves the eight
unit-ideal certificates behind (7) and the five Fitting strata.

The independent audit imports nothing from the primary verifier.  At
two finite-field component points and two slopes per point, it
exhausts all affine markings of both pencils, confirms full column
rank off the loci (6)--(7), confirms rank seven and genuineness on
them, and replays the rank-four mode-zero contraction and the
selected minors on every genuine projective direction.  The censuses
are corroboration only; the theorem is the characteristic-zero
calculation.
