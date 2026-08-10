# Generic weighted `H22` obstruction on the disjoint mixed-star component

## Status

This is an exact characteristic-zero theorem on a dense open subset of
the eighth pure-`P_4` component proved in
[`P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`](../../../p4/components/disjoint-mixed-star/P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md).

The complete weighted `H22` incidence over the generic point of that
component is empty.  Thus all eight pure-component orbits certified at
that checkpoint have empty generic marked `H31` and weighted `H22`
fibres.  The later embedded-`P_3` ninth component is not covered by
this theorem, but its generic fibres have since been excluded by their
own apolar insertion theorems:
[`P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md`](../../h31/embedded-p3/P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md),
[`P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md`](../embedded-p3/P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md).
The special equal- and opposite-weight slopes have since been closed
by a stronger binary obstruction:
[`P5_H22_DISJOINT_MIXED_STAR_EQUAL_OPPOSITE_WEIGHT_OBSTRUCTION.md`](boundaries/P5_H22_DISJOINT_MIXED_STAR_EQUAL_OPPOSITE_WEIGHT_OBSTRUCTION.md).
The compactified endpoint `r=0` is also closed: `D_01^0` has a binary
diagonal obstruction, while `D_23^0` has an unsplit two-minor Fitting
obstruction:
[`P5_H22_DISJOINT_MIXED_STAR_ZERO_SLOPE_BOUNDARY_OBSTRUCTION.md`](boundaries/P5_H22_DISJOINT_MIXED_STAR_ZERO_SLOPE_BOUNDARY_OBSTRUCTION.md).
Twelve generic parameter/coordinate branches and the principal
coupled slope-parameter divisor are closed in the companion boundary
theorems:
[`P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md`](boundaries/P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md),
[`P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md`](boundaries/P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md).
An intrinsic factorization of the seven selected `D_23` minor contents
has additionally exposed and closed four rational branches
`af=+/-1,a phi=+/-1`:
[`P5_H22_DISJOINT_MIXED_STAR_AF_APHI_BOUNDARY_OBSTRUCTION.md`](boundaries/P5_H22_DISJOINT_MIXED_STAR_AF_APHI_BOUNDARY_OBSTRUCTION.md).
A normalized coefficient divisor has also produced one new irreducible
quadratic branch, closed in both directions by full unsplit Fitting
ideals:
[`P5_H22_DISJOINT_MIXED_STAR_COEFFICIENT_QUADRATIC_BOUNDARY_OBSTRUCTION.md`](boundaries/P5_H22_DISJOINT_MIXED_STAR_COEFFICIENT_QUADRATIC_BOUNDARY_OBSTRUCTION.md).
Three further linear slope graphs are closed by six unsplit ideals; one
of them requires a cross-mode repair from mode zero to mode one:
[`P5_H22_DISJOINT_MIXED_STAR_LINEAR_SLOPE_BOUNDARY_OBSTRUCTION.md`](boundaries/P5_H22_DISJOINT_MIXED_STAR_LINEAR_SLOPE_BOUNDARY_OBSTRUCTION.md).
The dense component chart also admits an exact source-torus quotient
`(a,b,f,phi)~(af,bf,1,phi/f)`, reducing the base to a surface without
changing either slope:
[`P5_H22_DISJOINT_MIXED_STAR_TORUS_QUOTIENT.md`](boundaries/P5_H22_DISJOINT_MIXED_STAR_TORUS_QUOTIENT.md).

This does not close special parameter, slope, or projective boundary
points, prove that the nine known components are exhaustive, settle the
remaining partial-row geometries, or resolve the global prize problem.

## Component field and weighted deletions

Use the pure-factor bases `(alpha_i,beta_i)=(y_i,x_i)` from the component
theorem and write

```text
Phi =
 a^2 b f phi^2+a^2 f^2
 -b^2 f^2+b^2 phi^2-bf-1 = 0.                    (1)
```

The irreducibility of `Phi` gives the component field

```text
K=C(a,b,f)[phi]/(Phi).                             (2)
```

Every marked basis on the four planes is

```text
beta_i(t)=beta_i+t_i alpha_i.                      (3)
```

The two weighted `H22` source contractions are

```text
D_01^r(u)=(r u_0+u_1,u_2,u_3,u_4),
D_23^r(u)=(u_0,u_1,r u_2+u_3,u_4).                (4)
```

For either direction let `z=(x_0,...,x_3,y_0,...,y_3)` be the eight
extension entries.  The fourteen mixed binary coefficients form a
linear matrix

```text
M_D(t) z,       M_D(t) in Mat_(14 x 8)(K[t]).      (5)
```

Let `A_D(z)` and `B_D(z)` be the two diagonal coefficients.  A genuine
binary neighbour is exactly a vector satisfying

```text
M_D(t)z=0,             A_D(z)B_D(z) != 0.          (6)
```

Mixed rows below are ordered lexicographically by the binary words
other than `0000,1111`; columns are `(x_0,...,x_3,y_0,...,y_3)`.

## The `D_23^r` marking line

Take the seven base rows

```text
0,1,3,5,7,8,10
```

and form seven `8 x 8` determinants by adjoining rows

```text
2,4,6,9,11,12,13.                                 (7)
```

Let `J_23` be their ideal together with `Phi`, over the coefficient
field `C(a,b,f,r)`.  Exact characteristic-zero saturation gives

```text
J_23 : t_1^infinity = (1),
J_23 : t_2^infinity = (1),
J_23 : t_3^infinity = (1).                        (8)
```

Every rank-drop marking therefore lies on

```text
t_1=t_2=t_3=0.                                    (9)
```

On (9), impose the fourteen mixed equations, normalize `A_23=1`,
invert `B_23`, and add the mode-zero one-marked minors in rows

```text
0137, 0157.                                       (10)
```

The resulting ideal is the unit ideal.  Hence no genuine `D_23^r`
binary neighbour has one-marked rank at most three.

## The degree-five `D_01^r` rank locus

For `D_01^r`, use base rows

```text
0,1,2,3,7,8,10
```

and adjoin

```text
4,5,6,9,11,12,13.                                 (11)
```

Let `J_01` be the corresponding seven-minor ideal with `Phi`.  The
`7 x 7` base minor obtained by deleting column `x_3` is nonzero at
every point of `J_01`:

```text
J_01 + (pivot) = (1).                              (12)
```

Consequently the selected minors define the complete rank-at-most-seven
locus, rather than merely a necessary relaxation.  Exact standard-basis
reduction gives

```text
dim J_01=0,
vdim_(C(a,b,f,r)) J_01=10.                         (13)
```

Since `Phi` has degree two, the marking scheme has degree five over
`K`.  This explains the five survivors in each earlier finite-field
census without using those censuses as proof.

The same basis contains

```text
t_1 t_2.                                          (14)
```

On `t_1=0`, define

```text
L_3 =
 f(a^2-b^2)(r-1)t_3
 -b(bf+1)(a(r+1)+b(r-1)),                         (15)

L_2 =
 (bf+1)(
   a^2 f(r-1)+abf(r+1)+a(r+1)+b(r-1)
 )t_2
 -(r+1)(a^2 f+b).                                 (16)
```

Then

```text
t_3 L_3 in J_01+(t_1),
t_3 L_2 in J_01+(t_1).                            (17)
```

On the generic coefficient field, (14)--(17) give the complete cover

```text
B_1: t_2=0,
B_2: t_1=t_3=0,
B_3: t_1=L_3=L_2=0.                               (18)
```

The third branch is the nonzero-`t_3` sheet; the coefficients omitted
from the dense open set make (15)--(16) equivalent to explicit rational
values of `t_3,t_2`.

## Ternary Fitting obstruction on all five markings

On each branch in (18), impose the mixed equations and the genuine
binary conditions by

```text
A_01=1,              w B_01-1=0.                  (19)
```

The seven maximal minors used to derive the marking cover are
redundant in these final ideals: `A_01=1` makes `z` nonzero, and
`M_01(t)z=0` then already forces `rank M_01(t)<=7`.

Let `H_0137,H_0157` denote the two mode-zero one-marked determinants.
Exact standard-basis calculations give

```text
B_1 + (mixed,19,H_0137,H_0157) = (1),
B_2 + (mixed,19,H_0137)        = (1),
B_3 + (mixed,19,H_0137)        = (1).             (20)
```

Thus every genuine `D_01^r` binary neighbour has mode-zero one-marked
rank four.  A ternary lift factors this map through a
three-dimensional target local space, so its rank would be at most
three.  Equations (8)--(10) and (12)--(20) exclude both weighted
directions and prove that the generic marked `H22` fibre is empty.

## Geometric interpretation

The broad elimination in the earlier working note mixed eight extension
coordinates with four marking coordinates.  The useful translation is
to the Fitting scheme of the `14 x 8` mixed-coefficient matrix:

```text
binary neighbour
  -> rank M_D(t) <= 7
  -> a small determinantal marking scheme
  -> one- or two-minor ternary obstruction.
```

For `D_23^r` the Fitting scheme is one line.  For `D_01^r` it is a
degree-five finite scheme with a three-chart factor cover.  No ambient
map tuple, support catalogue, or graph is enumerated.

## Honest frontier

All eight component orbits known at this theorem checkpoint are
generically closed for both `H31` and weighted `H22`.  A ninth,
embedded-`P_3` component has since been certified and its generic
marked fibres are now closed as well.  The next geometric tasks are:

1. classify the ninth component's special marked boundaries;
2. extract the remaining hidden certificate denominators and classify
   their parameter/slope/projective boundaries;
3. finish the exceptional mixed-star/triangle and lower-pair-rank
   strata to decide component exhaustiveness; and
4. lift a complete `P_5 -> Delta_3` obstruction back into the
   arbitrary-order blocker hierarchy.

The global Krenn--Gu conjecture remains unresolved.

The two residual-torus divisors `r=1` and `r=-1` are no longer part of
item 1: on them the mixed kernel forces one binary diagonal to vanish
before the ternary obstruction is reached.
The projective slope endpoint `r=0` is no longer open either.  There
the `D_01` kernel has the same kind of diagonal obstruction, while the
`D_23` mixed rank drops to six and is excluded by an unsplit two-minor
Fitting ideal.
Nor are the twelve coordinate/pivot branches or the principal coupled
slope graph recorded in the companion boundary theorems.  The four
new `af=+/-1,a phi=+/-1` branches are no longer open either; in the
`D_23` direction they satisfy the stronger statement that the genuine
binary incidence itself is empty.
The new quadratic branch cut out by
`a^2 f^2+2bf+1=0` after normalization is also closed by unsplit
two-minor ideals, so its proof does not assume specialization of the
degree-five marking cover.
The three rational graphs
`(a+b)r+/-(a-b)=0` and `(af-1)r+(af+1)=0` are now closed as well.
The last graph has a genuine mode-zero degeneracy in `D_01`, but its
mode-one `0457` minor excludes every ternary lift.
The remaining visible factors of the first reduced final certificate,
including two unresolved slope divisors and all null computations, are
listed in
[`P5_H22_DISJOINT_MIXED_STAR_CERTIFICATE_DIVISOR_FRONTIER.md`](boundaries/P5_H22_DISJOINT_MIXED_STAR_CERTIFICATE_DIVISOR_FRONTIER.md).

## Verification

Run:

```text
python \
  claims/p5/h22/disjoint-mixed-star/verify_p5_h22_disjoint_mixed_star_component_generic_obstruction.py

python \
  claims/p5/h22/disjoint-mixed-star/audit_p5_h22_disjoint_mixed_star_component_generic_obstruction.py
```

The primary verifier reconstructs the component family, both weighted
mixed matrices, the exact determinantal schemes, the degree-five and
pivot claims, the factor cover, and all four characteristic-zero
Fitting unit ideals.  The final `D_01` ideals omit the redundant
maximal minors after diagonal normalization.

The independent audit imports nothing from the primary verifier.  At
two generic finite-field component points it exhausts every marked
basis, recovers the five `D_01` points and the `D_23` line, and checks
the one-marked rank obstruction on every genuine projective extension
direction.  That census is corroboration only; the standard-basis
identities prove the theorem over `C`.
