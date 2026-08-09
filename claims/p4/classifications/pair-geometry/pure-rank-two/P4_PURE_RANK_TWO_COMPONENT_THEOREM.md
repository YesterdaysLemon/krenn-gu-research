# A generically smooth component of pure rank-two `P_4` compressions

## Status

This is an exact local algebraic-geometric theorem over `C`.

Let `X` be the locus of ordered four-tuples of planes

```text
(U_0,U_1,U_2,U_3) in Gr(2,4)^4
```

for which the restriction of `P_4` to
`U_0 tensor U_1 tensor U_2 tensor U_3` is nonzero and decomposable.
The closure of the five-parameter family in
[`P4_DECOMPOSABLE_RANK_TWO_FAMILY.md`](../decomposable-rank-two-family/P4_DECOMPOSABLE_RANK_TWO_FAMILY.md)
is a five-dimensional irreducible component of the closure of `X`.
Moreover, that component is generically smooth and has the expected
codimension eleven in `Gr(2,4)^4`.

This result does **not** classify every component of `X`.  In fact, a
second five-dimensional component has since been constructed using the
squarefree intersection algebra and lines on diagonal quadrics:

- [`P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md`](../../../components/diagonal-quadric/P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md)

Thus exhaustiveness of the family in this note is false.  Its component
and complete marked-fibre theorems remain valid with their stated
scope.

The same component now has a simpler dense presentation as a fixed
`(2,1,1)` exceptional triangle with a `Gr(2,3)` apolar opposite-plane fibre:
[`P4_FIRST_COMPONENT_APOLAR_TRIANGLE_NORMAL_FORM.md`](../../P4_FIRST_COMPONENT_APOLAR_TRIANGLE_NORMAL_FORM.md).
That normal form is exactly Pluecker-equivalent to the family used here.

## A Grassmann chart

Use the following affine charts for the four planes:

```text
R_0 = ((1,0,a,b), (0,1,c,d)),
R_1 = ((e,1,0,f), (g,0,1,h)),
R_2 = ((i,1,0,j), (k,0,1,l)),
R_3 = ((1,m,n,0), (0,o,p,1)).                         (1)
```

For `beta in {0,1}^4`, let `T_beta` be the permanent of the `4 x 4`
matrix whose row in mode `r` is row `beta_r` of `R_r`.  These are the
sixteen coefficients of the restricted `P_4`.

Work in the target Segre chart centered at

```text
alpha=(1,0,0,0),   T_alpha != 0.
```

If `z_r` is the ratio of the factor coordinate opposite `alpha_r` to
the coordinate at `alpha_r`, decomposability is exactly the fifteen
incidence equations

```text
F_beta =
  T_beta - T_alpha product_{r: beta_r != alpha_r} z_r = 0,
beta != alpha.                                        (2)
```

Thus the incidence variety lives in affine `20`-space with coordinates

```text
a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,z_0,z_1,z_2,z_3.
```

Because a nonzero decomposable tensor has unique projective factors,
the projection from this incidence variety to the plane tuple is an
isomorphism onto `X` on this chart.

## A smooth point of expected dimension

Take the family parameters

```text
e_family=i_family=l_family=j_family=1,   c_family=0.
```

Row-reducing the four family planes into (1) gives

```text
(a,b,c,d) = (-1,-2,1,0),
(e,f,g,h) = ( 1, 0,0,1),
(i,j,k,l) = ( 0, 1,-1,0),
(m,n,o,p) = ( 0, 1,0,-1).                            (3)
```

At this point the restricted tensor is

```text
2 (y_0-x_0)(x_1+y_1)x_2x_3,
```

so in the chosen Segre chart

```text
T_1000=2,   (z_0,z_1,z_2,z_3)=(-1,1,0,0).            (4)
```

Let `J` be the `15 x 20` Jacobian of (2), with rows ordered
lexicographically by `beta != 1000`.  The columns

```text
a,b,c,e,f,g,h,i,j,k,l,m,o,z_2,z_3                   (5)
```

form a square minor with

```text
det J_(5) = -4096.                                    (6)
```

Therefore `J` has rank fifteen.  The incidence variety, and hence `X`,
is smooth of dimension

```text
20-15=5
```

at (3)--(4).  Equivalently, its image in `Gr(2,4)^4`, of dimension
sixteen, has the expected codimension eleven of the Segre variety in
projective fifteen-space.

## The family fills the local component

On the nonvanishing chart used above, row reduction sends the five
family parameters `(E,I,L,Q,C)` to the sixteen plane coordinates

```text
a = -Q(C+EIL)/E,       b = -CQ-EI(LQ+1),
c = C/E+IL,            d = C,
e = L,                 f = 0,
g = 0,                 h = E,
i = 0,                 j = EIL,
k = -1/I,              l = 0,
m = 0,                 n = I,
o = 0,                 p = -1/E.                     (7)
```

At `(E,I,L,Q,C)=(1,1,1,1,0)`, the Jacobian of (7) has rank five.
Indeed, its rows `a,b,c,d,e` form a `5 x 5` minor of determinant `2`.
Consequently the closure of the family image has dimension at least
five.

The family parameter space is irreducible, so its image closure is
irreducible.  It lies in the incidence locus by the exact permanent
identities already verified for the family.  At (3)--(4), that
incidence locus is smooth of dimension five and hence has a unique
local irreducible component.  The five-dimensional family closure must
be that component.  This proves the theorem.

## Consequence for the `H31` frontier

This theorem identifies a full generically smooth component of the
all-rank-two pure-`P_4` **plane** locus.  It does not by itself exclude
that component from `H31`.  An `H31` local map also marks, inside each
plane, a kernel row and a complementary pure-colour row.  Shifting the
complementary row by the kernel row preserves the plane and the pure
deletion but changes the neighbouring `Delta_2` equations.

The displayed-family obstruction by itself excludes one marked section,
not the complete marked-basis fibre.  The distinction is witnessed
exactly in
[`P5_H31_MARKED_BASIS_OPEN_BRANCH.md`](../../../../../P5_H31_MARKED_BASIS_OPEN_BRANCH.md):
the same generic plane tuple has a shifted marking with a genuine binary
`Delta_2` extension, although that explicit branch is subsequently
excluded by a ternary marked determinant.

The complete affine Borel fibre over every finite member of the family
has since been classified in
[`P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md`](../../../../../P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md).
Every binary survivor, including all special divisors, is ternarily
obstructed.  Thus the marked-basis gap is closed on the finite family
chart.

The 21 genuine toric base-plane/orientation cases have since been
closed at complete marked-fibre level in
[`P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md`](../../../../p5/h31/toric-marked-fibre/P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md).
The nonzero divisor inside the preferred component chart is likewise
closed at complete marked-fibre level in
[`P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md`](../../../../../P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md).
The complete marked fibre of this component, including its finite
chart and all boundary divisors, has since been excluded.  The second
diagonal-quadric component is genuinely distinct: at a rational point
only one annihilator line lies in the block-line jump locus, whereas
three do throughout the component proved here.  The complete marking
fibre at that rational point is excluded in
[`P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md`](../../../../../P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md),
but the generic and boundary marked fibres of the second component
remain open, as does the existence of any further component.

The rank-one pure-hyperplane boundary has already been excluded in
[`P5_H31_SECONDARY_GATE_EXCLUSION.md`](../../../../p5/h31/secondary-gate-exclusion/P5_H31_SECONDARY_GATE_EXCLUSION.md).

## Consequence for the `H22` frontier

The generic weighted `H22` incidence on this component has since been
excluded in
[`P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md`](../../../../p5/h22/first-rank-two/P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md).
The weighted `01` mixed matrix is injective for every marking by an
eight-chart projective-kernel cover.  The weighted `23` projection has
two sheets, excluded by mode-two marked minors `0147` and `0137`.
Parameter/slope divisors and projective boundaries remain open.

## Verification

Run:

```text
python claims/p4/classifications/pair-geometry/pure-rank-two/verify_p4_pure_rank_two_component.py
python claims/p4/classifications/pair-geometry/pure-rank-two/audit_p4_pure_rank_two_component.py
```

The primary verifier expands all permanents symbolically, evaluates the
exact rational Jacobian, checks the determinant `-4096`, verifies the
family chart formulas, and checks the independent family tangent minor
`2`.  The audit uses a separate dynamic-programming permanent and
forward-mode dual numbers over `F_101`; it checks the same ranks without
importing the primary verifier.  The modular audit is independent QA;
the written and primary determinant computation is the characteristic
zero certificate.
