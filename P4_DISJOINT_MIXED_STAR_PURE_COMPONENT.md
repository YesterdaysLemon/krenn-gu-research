# An eighth pure `P_4` component from a disjoint mixed star

## Status

This is an exact algebraic-geometric component theorem over `C`.

The all-rank-two locus on which `P_4` restricts to a nonzero
decomposable tensor has a further generically smooth,
five-dimensional irreducible component.  Its three generic rank-one
exceptional relations have mixed star orientation, as on the sixth
component, but their source coordinate-pair supports have pattern

```text
{01,01,23}: two equal supports and one disjoint support.   (1)
```

The sixth component instead has one-coordinate overlap between the two
distinct supports.  This invariant, together with pair-relation ranks
and dimension, separates the new component from all seven previously
certified orbits.  The certified lower bound is therefore eight
component orbits: seven fivefolds and one sixfold.

This is not a classification.  A subsequent exact function-field
theorem excludes the generic marked `H31` fibre:
[`P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md).
Its generic weighted `H22` incidence is now excluded as well:
[`P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md).
The equal- and opposite-weight slope fibres are excluded by the
stronger binary theorem
[`P5_H22_DISJOINT_MIXED_STAR_EQUAL_OPPOSITE_WEIGHT_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_EQUAL_OPPOSITE_WEIGHT_OBSTRUCTION.md).
Twelve generic parameter/coordinate branches and the principal coupled
slope-parameter divisor are excluded in
[`P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md)
and
[`P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md).
The component's boundaries, component exhaustiveness, and the global
prize problem remain open.  The earlier finite-field structure and
timed-out broad route remain as provenance in
[`P5_H22_DISJOINT_MIXED_STAR_WORKING_NOTE.md`](P5_H22_DISJOINT_MIXED_STAR_WORKING_NOTE.md).

## Squarefree support geometry

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).   (2)
```

Choose pure-factor bases `(y_i,x_i)`, with `y_i` the kernel row.  Take
the exceptional-edge star centred at mode three.  Two relations point
to the centre and one points to a leaf:

```text
x_1 y_3=0,       x_2 y_3=0,       y_0 x_3=0.       (3)
```

For a fixed nonzero squarefree zero-product factor, the opposite
factor is unique on its coordinate two-plane.  Thus the first two
relations in (3) have the same support.  The chart treated here is the
disjoint alternative

```text
supp(x_1)=supp(x_2)=supp(y_3)={0,1},
supp(y_0)=supp(x_3)={2,3}.                          (4)
```

Diagonal source scaling and row gauges normalize

```text
y_0=(0,0,1,-1),          y_3=(1,-1,0,0),
x_1=x_2=(1,1,0,0),       x_3=(0,0,1,1).            (5)
```

This disjoint support configuration was absent from the earlier
overlapping-support determinantal chart.

## The irreducible family

Let `a,b,f,phi` be parameters and put

```text
j     = f+b phi^2,
kappa = phi(bf+1),
eta   = -(bf+1).                                   (6)
```

Define

```text
x_0=(a+b,a-b,0,2),

y_1=(-af+1,-af-1,f+phi,f-phi),

y_2=(-aj+eta,-aj-eta,j+kappa,j-kappa),             (7)
```

and take

```text
U_i=span(y_i,x_i)
```

with the fixed rows (5).

Direct permanent expansion gives only

```text
T_1001=-4 Phi,
T_1111=4,                                          (8)
```

where

```text
Phi =
 a^2 b f phi^2+a^2 f^2
 -b^2 f^2+b^2 phi^2-bf-1.                          (9)
```

Hence `Phi=0` gives a nonzero pure restriction on every rank-two
plane chart in (5)--(7).

The determinant in (9) is forced, not guessed.  Before selecting
`y_2`, the remaining three kernel equations are linear in its
sum/difference coordinates `(j,kappa,eta)`, with matrix

```text
N =
 0              1             phi
 bf+1           1-b phi       f+phi
 a^2 f+b        0             bf+1.                (10)
```

Its determinant is

```text
det N=Phi.                                         (11)
```

The vector in (6) is the cross product of the first two rows of (10),
so the third equation is exactly (9).

The polynomial `Phi` is irreducible.  Regard it as a quadratic in
`a`:

```text
Phi=a^2 f(b phi^2+f)
    -(b^2 f^2-b^2 phi^2+bf+1).                     (12)
```

The two coefficients in (12) are coprime.  Over
`C(b,f,phi)`, reducibility would require their ratio to be a square.
Its valuation at `f=0` is odd (`-1`), so it is not a square.  Gauss's
lemma proves irreducibility.  Therefore `Phi=0` is an irreducible
threefold in the four-parameter normalized chart.

## Exact component certificate

Apply the projective diagonal source torus

```text
diag(t_0,t_1,t_2,1)                                 (13)
```

to all four planes.  Use Grassmann pivots

```text
(02),(01),(01),(02).                                (14)
```

At

```text
(a,b,f,phi,t_0,t_1,t_2)
 =(-12,-10,3/4,-5/28,1,1,1),                       (15)
```

equation (9) vanishes and

```text
partial Phi/partial phi=350.
```

Thus `phi` is locally a function of `(a,b,f)`.  Differentiate the
sixteen Grassmann-chart coordinates in the three resulting
hypersurface tangent directions and the three source-torus directions.
The tangent matrix has rank five.  Rows

```text
(0,1,3,4,5)
```

and columns corresponding to

```text
(a,b,f,t_0,t_2)
```

have determinant

```text
4129/365226400.                                    (16)
```

For the independent local upper bound, adjoin the unique projective
Segre point of the nonzero pure tensor.  In the charts (14), use tensor
anchor `0001`; its four adjacent ratios at (15) are

```text
(0,-5/4,44/5,0).                                   (17)
```

The fifteen universal Segre-incidence equations have Jacobian rank
fifteen in the twenty plane/target variables.  Columns

```text
(0,1,2,3,4,5,6,7,8,9,10,13,14,16,19)
```

give determinant

```text
46800000/34179505129.                              (18)
```

The incidence locus is therefore smooth of dimension five at (15).
The irreducible family already has a rank-five image by (16), so its
closure is the unique local irreducible component.  A nonzero pure
tensor has a unique Segre factor point, and projection to the plane
locus is locally an isomorphism.  This proves the component statement.

## Distinctness from the seven earlier orbits

At (15), and hence generically, the lexicographic pair-image profile is

```text
(r_01,r_02,r_03,r_12,r_13,r_23)
  =(4,4,3,4,3,3).                                  (19)
```

All three exceptional relations have coefficient-matrix rank one.
Their pure-kernel endpoint indegrees are

```text
(2,1,0,0),                                         (20)
```

and their coordinate-pair supports are precisely (1).

These data separate the new component:

- the first component has pair profile `(4,4,4,3,3,3)`;
- the diagonal-quadric component has a rank-two exceptional relation;
- the three split-cubic components have indegrees `(1,1,1,0)`;
- the overlapping mixed component has indegrees (20), but its two
  distinct zero-product supports meet in one coordinate;
- the six-dimensional component is separated by dimension.

Relation rank, pure-kernel direction, coordinate support intersection,
pair-image rank, and dimension are invariant under the allowed source
coordinate permutations, diagonal source rescaling, mode
permutations, and row-basis changes.  Hence the new component is
inequivalent to all seven earlier orbits.

## Honest frontier

The new component repairs an actual gap in the rank-one star analysis:
the earlier five-prime chart treated overlapping mixed supports, while
the radical-star theorem treated the two outward relations.  The
disjoint mixed-support stratum is component-sized rather than a
boundary.

The immediate exact targets are now:

1. extract and classify its still-hidden standard-basis denominators
   and remaining projective boundaries;
2. finish the remaining exceptional triangle and the compatibility of
   the rank-two pair pencils to decide component exhaustiveness.  A
   single exact rank-two pair is now forced into a secant
   `2+2`/`1+3` block center or a coincident-plane tangent through a
   coordinate line by
   [`P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md`](P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md).

The global prize conjecture remains unresolved.

## Verification

Run:

```text
tmp/codex_verify_env/Scripts/python.exe \
  verify_p4_disjoint_mixed_star_pure_component.py

tmp/codex_verify_env/Scripts/python.exe \
  audit_p4_disjoint_mixed_star_pure_component.py
```

The primary verifier reconstructs (5)--(11), proves irreducibility,
checks the exact tangent and incidence minors (16)--(18), and verifies
the generic invariants (19)--(20).

The independent audit imports nothing from the primary verifier.  It
uses a subset-dynamic-programming permanent, separately rebuilds the
exact rational family and universal incidence Jacobian, and rechecks
the component and support certificates over `Q`.
