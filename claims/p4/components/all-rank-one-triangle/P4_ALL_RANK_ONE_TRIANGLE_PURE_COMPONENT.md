# A ninth pure `P_4` component: the all-rank-one relation triangle

## Status

This is an exact algebraic-geometric component theorem over `C`.

The all-rank-two locus on which `P_4` restricts to a nonzero
decomposable tensor has a ninth generically smooth, five-dimensional
irreducible component.  Its three generic rank-one exceptional
relations fill the full pair triangle

```text
{12}, {13}, {23},                                   (1)
```

oriented as a directed three-cycle `1 -> 3 -> 2 -> 1`, with no
rank-two relation and with mode `0` in no relation at all.  This is
precisely the configuration slot left open by the directed
classifications: the first component realizes the triangle with one
rank-two relation, the radical-star and mixed-star charts treat star
shapes, and the in-out path `1 -> 3 -> 2` closes into a cycle only
here.  The certified lower bound is therefore nine component orbits:
eight fivefolds and one sixfold.

The component was located on the deep `x_3=0` wall of the in-out
path chart in
[`P4_INOUT_PATH_STRATUM_WORKING_NOTE.md`](../../../../P4_INOUT_PATH_STRATUM_WORKING_NOTE.md).
This document is its standalone theorem: a gauge-reduced free
rational normal form, the smooth-incidence certificate replayed from
that normal form, and the separating invariants.

This is not a classification.  The generic `H31` and weighted `H22`
obstruction theorems proved for the other components are **open** for
this one; only clearly-labeled finite-field exploration data exists.
The component's boundaries, component exhaustiveness, and the global
prize problem remain open.

## Squarefree support geometry

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).     (2)
```

Choose pure-factor bases `(y_i,x_i)`, with `y_i` the kernel row.  The
three exceptional relations are

```text
y_1 x_2 = 0,      x_1 y_3 = 0,      y_2 x_3 = 0.    (3)
```

Each relation has exactly one kernel endpoint; drawing the arrow into
the kernel endpoint gives the directed three-cycle

```text
2 -> 1,      1 -> 3,      3 -> 2.                   (4)
```

By the zero-product support lemma each relation lives in a coordinate
two-plane:

```text
supp(y_1)=supp(x_2)={0,1},
supp(x_1)=supp(y_3)={2,3},
supp(y_2)=supp(x_3)={0,2}.                          (5)
```

The three supports are pairwise distinct, cover all four coordinates,
and meet pairwise in `0`, `1`, `1` coordinates.

The configuration arises from the in-out path chart as follows.  On
its overlap-one deep stratum the two pure-vanishing covectors drop to
the single covector `(-d v_1,-d v_0,v_1,v_1)`, whose kernel is
spanned by the two free relation directions `x_2, x_3` and the
auxiliary vector `w=(1,0,0,d)`.  On the branch `x_3=0` of the wall
determinant, **every** plane `U_0` inside that kernel gives a pure
restriction.  The gauge freedoms — shifting `v` by `x_1`, shifting
the mode-`2` free row by `y_2`, the two row scales, and the residual
chart torus — reduce the branch to the two-parameter normal form
below with `d=1`.

## The free rational family

Let `p,q` be free parameters and take rows

```text
y_0=(pq+1, 1, p, pq+1),      x_0=(q+1, 0, 1, q),
y_1=(p, 1, 0, 0),            x_1=(0, 0, 1, -1),
y_2=(1, 0, -1, 0),           x_2=(-p, 1, 0, 0),
y_3=(0, 0, 1, 1),            x_3=(1, 0, 1, 0),     (6)
```

with

```text
U_i=span(y_i,x_i).                                  (7)
```

Geometrically, with `w=(1,0,0,1)`,

```text
U_0=span(x_2+w, x_3+q w),
y_0=x_2+p x_3+(pq+1)w:                              (8)
```

`U_0` is a moving plane inside the covector kernel
`span(x_2,x_3,w)`, and `p` couples `U_1,U_2` (through
`y_1,x_2`) to the mode-`0` kernel row.

Direct permanent expansion gives only

```text
T_1111=-2,                                          (9)
```

and all fifteen other coefficients vanish **identically** in `(p,q)`.
There is no defining hypersurface: unlike the eighth component's
irreducible `Phi` in
[`P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`](../disjoint-mixed-star/P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md),
the family (6) is free.  Every parameter pair gives a nonzero pure
restriction, all four planes stay rank two for all `(p,q)`, and the
component is rational: the parametrization by
`A^2 x (C^*)^3` (parameters times torus) is total, so the closure of
its image is irreducible.

## Exact component certificate

Apply the projective diagonal source torus

```text
diag(t_0,t_1,t_2,1)                                 (10)
```

to all four planes.  Use Grassmann pivots

```text
(12),(12),(01),(02),                                (11)
```

whose pivot minors on the family are the unit monomials

```text
t_1 t_2,   t_1 t_2,   t_0 t_1,   -t_0 t_2:          (12)
```

the chart covers the entire family times torus.  The scaled tensor
has the single coefficient `T_1111=-2 t_0 t_1 t_2`.

At

```text
(p,q,t_0,t_1,t_2)=(2,3,1,1,1),                      (13)
```

differentiate the sixteen Grassmann-chart coordinates in the five
parameter directions.  The tangent matrix has rank five.  Rows

```text
(0,1,2,3,4)
```

(the four mode-`0` chart coordinates and the first mode-`1`
coordinate) against all five columns have determinant

```text
-1.                                                 (14)
```

For the independent local upper bound, adjoin the unique projective
Segre point of the nonzero pure tensor.  In the charts (11), use
tensor anchor `0110`; its four adjacent ratios at (13) are

```text
(-1/2,0,0,0).                                       (15)
```

The fifteen universal Segre-incidence equations have Jacobian rank
fifteen in the twenty plane/target variables.  Columns

```text
(0,2,4,5,6,7,8,9,10,11,12,14,17,18,19)              (16)
```

give determinant

```text
860160 = 2^13*3*5*7.                                (17)
```

The incidence locus is therefore smooth of dimension five at (13).
The free family already has a rank-five image by (14), so its closure
is the unique local irreducible component.  A nonzero pure tensor has
a unique Segre factor point, and projection to the plane locus is
locally an isomorphism.  This proves the component statement.

The normal form is an exact chart transport of the wall branch: with
`p=d v_0/(v_1 alpha)` and `q=beta`, the deep-stratum branch family of
the working note, scaled by `diag(d,alpha,1,1)`, equals (6)--(8)
plane by plane as an identity in `(d,v_0,v_1,v_2,x_1,x_2,alpha,beta)`.
The note's certified rational sample lands at

```text
(p,q)=(9/5,-1/2).                                   (18)
```

## Distinctness from the eight earlier orbits

At (13), and hence generically, the lexicographic pair-image profile
is

```text
(r_01,r_02,r_03,r_12,r_13,r_23)
  =(4,4,4,3,3,3):                                   (19)
```

the rank-three edges form the **triangle** (1) on modes `{1,2,3}`.
All three exceptional relations have coefficient-matrix rank one,
oriented as the cycle (4), so the pure-kernel endpoint indegrees are

```text
(1,1,1,0).                                          (20)
```

The diagonal-quadric jump signature (`2+2`,`1+3`) counts are

```text
(1,2).                                              (21)
```

At the certified generic samples of the eight earlier orbits the same
invariants are:

```text
orbit               rank-3 edges   relation ranks   jumps
first               triangle       {1,1,2}          (2,1)
diagonal-quadric    star           {1,1,2}          (1,0)
1+3 branch L1       star           {1,1,1}          (1,1)
1+3 branch L2       star           {1,1,1}          (0,2)
1+3 branch L3       star           {1,1,1}          (0,1)
sixth               star           {1,1,1}          (0,1)
seventh             (dimension six)
eighth              star           {1,1,1}          (1,0)
ninth               triangle       {1,1,1}          (1,2)  (22)
```

These data separate the new component:

- the six-dimensional seventh component is separated by dimension;
- the first component realizes the triangle, but with one rank-two
  relation;
- the diagonal-quadric, the three `1+3`, the sixth, and the eighth
  components all have rank-three stars, not triangles;
- the jump signature (21) moreover differs outright from every
  earlier five-dimensional orbit.

Rank-three edge shape (triangle against star), relation rank,
pure-kernel direction, pair-image rank, jump signature, and dimension
are invariant under the allowed source coordinate permutations,
diagonal source rescaling, mode permutations, and row-basis changes.
Hence the new component is inequivalent to all eight earlier orbits.

## Honest frontier

The ninth component fills the last announced gap of the in-out path
sweep: the mixed-orientation cycle configuration that neither the
radical-star theorem (both arrows out) nor the mixed-star charts (a
star centre) could produce.  Its identification resolves the deep
`x_3=0` wall of the overlap-one chart; the note's other deep branch
is the first component.

The immediate exact targets are now:

1. the generic marked `H31` fibre and the generic weighted `H22`
   incidence of this component — both **open**; the finite-field
   marking-locus exploration
   (`explore_p5_h31_all_rank_one_triangle_modular.py`, primes `11`
   and `13`) is corroborating data only, not a theorem.  At both
   primes the binary-extension survivor marking loci are the
   `t_0`-line for distinguished coordinate `0`, the union of the
   `t_0`- and `t_2`-lines for `2`, one isolated marking for `3`, and
   empty for `1`; every genuine direction is killed by a rank-four
   one-marked map at a distinguished-dependent mode (`1`, `3`, and
   `1`/`3` respectively), so the modular fibre is empty — but unlike
   the eighth component's uniform one-minor identity, no single
   `4 x 4` row minor certifies the whole sweep;
2. its parameter/projective boundaries;
3. component exhaustiveness — nine is a certified lower bound, not a
   census.

The global prize conjecture remains unresolved.

## Verification

Run:

```text
python claims/p4/components/all-rank-one-triangle/verify_p4_all_rank_one_triangle_pure_component.py

python claims/p4/components/all-rank-one-triangle/audit_p4_all_rank_one_triangle_pure_component.py
```

The primary verifier reconstructs (6)--(9), proves the single-word
identity and the zero-product relations symbolically, replays the
exact chart transport (18) from the working-note wall, checks the
exact tangent and incidence minors (14)--(17), and verifies the
generic invariants (19)--(22) against the certified samples of the
earlier orbits.

The independent audit imports nothing from the primary verifier.  It
uses a subset-dynamic-programming permanent, separately rebuilds the
exact rational family and universal incidence Jacobian, rechecks the
component and invariant certificates over `Q`, and replays the
tangent and incidence Jacobians modulo the two primes `101` and
`103` by dual-number differentiation, recovering the same minors.
