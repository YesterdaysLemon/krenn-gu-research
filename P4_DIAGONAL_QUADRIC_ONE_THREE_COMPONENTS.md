# Three further pure `P_4` components from the diagonal-quadric map

## Status

This is an exact algebraic-geometric theorem over `C`.

The all-rank-two locus on which `P_4` restricts to a nonzero
decomposable tensor has at least three more irreducible components.
Each has dimension five.  They are mutually inequivalent, and they are
inequivalent to both components previously proved in
[`P4_PURE_RANK_TWO_COMPONENT_THEOREM.md`](P4_PURE_RANK_TWO_COMPONENT_THEOREM.md)
and
[`P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md`](P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md)
under source-coordinate permutations, diagonal source rescaling, and
mode permutations.

Thus there are at least five symmetry-inequivalent all-rank-two pure
`P_4` components.  This is a lower bound, not a classification.
The generic marked `H31` fibres of the three new components have since
been excluded in
[`P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md);
their generic weighted `H22` incidences have since been excluded in
[`P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md`](P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md).
Their special parameter/projective boundaries remain.  Nothing here
settles all of `H22` or resolves the global prize problem.

## The diagonal-quadric map

Work in the squarefree Frobenius algebra

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).   (1)
```

The coefficient of `X_0X_1X_2X_3` in a product of four linear forms is
their `P_4` permanent.  For a plane `U subset R_1`, let
`ell_U=P(U^perp)` be its annihilator line and let

```text
D(ell_U)={
 (d_0,d_1,d_2,d_3):
 sum_i d_i X_i^2 vanishes identically on ell_U
}.                                                   (2)
```

If `ell` is spanned by rows `r=(r_i)` and `s=(s_i)`, put

```text
p_ij=r_i s_j-r_j s_i.
```

The `3 x 4` restriction matrix of the coordinate squares is

```text
r_i^2
2 r_i s_i
s_i^2.                                              (3)
```

Its signed maximal minors give the rational cubic map

```text
delta: Gr(2,4) ---> P^3,

d_i=(-1)^i product_{j<k, j,k != i} p_jk.            (4)
```

Away from its base locus, (4) is the unique diagonal quadric through
`ell`.  The base locus is precisely the jump locus
`dim D(ell)>=2`.  Geometrically, these are block lines: the line joins
one point in each block of a nontrivial coordinate partition.

There are two permutation-invariant jump types:

```text
2+2: D(ell) is not contained in any {d_i=0};
1+3: D(ell) is contained in one coordinate hyperplane {d_i=0}.  (5)
```

This small cubic map is the useful replacement for a search through
plane coefficients.

There is also a quick pair-product constraint.  Put

```text
r_ij=dim(U_i U_j subset R_2).
```

For a pure restriction, the perfect pairing on `R_2` restricts to
rank one on opposite pair images.  Since `dim R_2=6`,

```text
r_ij+r_kl <= 7                                     (6)
```

for each partition `{ij|kl}`.  Therefore every perfect matching of
`K_4` contains an exceptional pair with `r_ij<=3`.  The new families
below have the star profile

```text
(r_01,r_02,r_03,r_12,r_13,r_23)=(4,4,3,4,3,3).     (7)
```

## A `1+3` radical-plane normal form

Fix

```text
y_1=(0,1,-1,0),       y_2=(0,1,0,-1),
z_1=(0,1, 1,0),       z_2=(0,1,0, 1).              (8)
```

Double contraction of `P_4` by `y_1,y_2` is the symmetric matrix

```text
 0  1 -1 -1
 1  0  0  0
-1  0  0  0
-1  0  0  0.                                       (9)
```

It has rank two and radical `span(z_1,z_2)`.  This is the radical
plane attached to the `1+3` base stratum of (4).

Let `S,D,G,T` be parameters and put

```text
P=G-T,      Q=D-S,

u_0=(2,P+Q,Q-P,0),       u_1=(0,0,1,1),
x_1=(1,0,S,D),           x_2=(1,0,G,T).             (10)
```

The rows `u_0,u_1` are the common kernel of

```text
(P,-1, 1,-1),       (Q,-1,-1,1).                   (11)
```

Define

```text
U_0=span(u_0,u_1),
U_1=span(y_1,x_1),
U_2=span(x_2,y_2),
U_3=span(z_1,z_2).                                  (12)
```

All restricted coefficients vanish except

```text
T_0100 = 2D(D+G-S+T),
T_0101 = D^2+2DG+2DT+G^2-2GT-S^2+T^2,
T_1100 = D+G+S+T,
T_1101 = D+G+S+T.                                  (13)
```

Regard (13) as a `2 x 2` matrix in modes zero and three.  Its
determinant is the completely split cubic

```text
(D-G-S+T)(D+G-S-T)(D+G+S+T).                       (14)
```

This split is the key conclusion of the radical-plane reframe.
It yields three irreducible parameter branches:

```text
L_1: T=-D+G+S,
L_2: T= D+G-S,
L_3: T=-D-G-S.                                     (15)
```

On the three branches, the nonzero tensor simplifies respectively to

```text
L_1:
 T_0100=T_0101=4DG,
 T_1100=T_1101=2(G+S);

L_2:
 T_0100=T_0101=4D(D+G-S),
 T_1100=T_1101=2(D+G);

L_3:
 T_0100=-4DS,
 T_0101=4G(D+G+S).                                 (16)
```

These formulas exhibit a nonzero decomposable restriction on a dense
open set of each branch.

## Dimension-five family certificates

Apply the projective diagonal source torus

```text
diag(t_0,t_1,t_2,1)                                 (17)
```

to all four planes in (12).  Use the Grassmann pivot charts

```text
(02),(01),(01),(12)                                 (18)
```

for modes zero through three.  At the sample parameters

```text
L_1: (S,D,G)=(1,3,4),
L_2: (S,D,G)=(1,3,4),
L_3: (S,D,G)=(1,2,3),                              (19)
```

the raw plane matrices are:

```text
L_1:
U_0=((2,4,0,0),(0,0,1,1)),
U_1=((0,1,-1,0),(1,0,1,3)),
U_2=((1,0,4,2),(0,1,0,-1)),
U_3=((0,1,1,0),(0,1,0,1));

L_2:
U_0=((2,0,4,0),(0,0,1,1)),
U_1=((0,1,-1,0),(1,0,1,3)),
U_2=((1,0,4,6),(0,1,0,-1)),
U_3=((0,1,1,0),(0,1,0,1));

L_3:
U_0=((2,10,-8,0),(0,0,1,1)),
U_1=((0,1,-1,0),(1,0,1,2)),
U_2=((1,0,3,-6),(0,1,0,-1)),
U_3=((0,1,1,0),(0,1,0,1)).                         (20)
```

Differentiate the sixteen chart coordinates with respect to

```text
(S,D,G,t_0,t_1,t_2).
```

The following `5 x 5` minors are nonzero:

```text
branch   chart-coordinate rows   parameter columns       determinant
L_1      (0,3,4,5,8)             (S,D,G,t_1,t_2)          -2
L_2      (1,3,4,6,8)             (S,D,G,t_1,t_2)          -1
L_3      (0,1,3,4,5)             (S,D,G,t_1,t_2)           5.  (21)
```

Thus each irreducible family has dimension five.

## Smooth incidence certificates

In the mixed charts (18), let `a_0,...,a_15` be the plane coordinates.
Use the target Segre anchor `0000` and ratios `z_0,...,z_3`.  The
fifteen affine equations are

```text
T_w=T_0000 product_{i:w_i=1} z_i,
                         w in {0,1}^4 - {0000}.     (22)
```

At (19), the only nonzero row-reduced tensor coefficients and target
ratios are

```text
branch   nonzero coefficients             (z_0,z_1,z_2,z_3)
L_1      T_0000=24, T_1000=10             (5/12,0,0,0)
L_2      T_0000= 8, T_1000=14             (7/4, 0,0,0)
L_3      T_0000=36, T_0001=-40            (0,0,0,-10/9).  (23)
```

The `15 x 20` Jacobian of (22) has rank fifteen at every listed point.
Taking all fifteen rows, the following column sets give nonzero
`15 x 15` determinants:

```text
L_1,L_2:
 (a_0,a_1,a_2,a_3,a_4,a_5,a_6,a_7,
  a_10,a_11,a_12,a_14,z_1,z_2,z_3),

 det(L_1)=163840,
 det(L_2)=6193152;

L_3:
 (a_0,a_1,a_2,a_3,a_4,a_5,a_6,a_7,
  a_10,a_11,a_12,a_14,z_0,z_1,z_2),

 det(L_3)=-737280.                                  (24)
```

Hence the Segre-incidence locus is smooth of dimension five at every
sample.  Each irreducible family in (15), (17) already has dimension
five by (21), so its closure is an irreducible component.  For a
nonzero decomposable tensor, the four projective target factors are
unique; consequently projection from the incidence chart to the plane
locus is locally an isomorphism.  This proves three component
statements.

## The three components are genuinely different

For a generic point, count the jump planes in (2) by the two types
(5).  The five certified component samples have signatures

```text
component                         (# 2+2, # 1+3)
first known component                  (2,1)
second known diagonal component        (1,0)
L_1                                    (1,1)
L_2                                    (0,2)
L_3                                    (0,1).       (25)
```

These ranks and types persist on a nonempty open subset of each
displayed irreducible family.  The ordered pair in (25) is invariant
under coordinate permutations, diagonal source rescaling, and mode
permutations.  Since all five pairs differ, the five component orbits
are distinct.  In particular, none of the three linear factors in
(14) may be discarded as a disguised copy of another.

## Consequence for the prize frontier

The generic marked `H31` fibres and generic weighted `H22` incidences
of all three components above are empty, but their special
parameter/projective boundaries remain.  For `H22`, all six binary
marking projections and five survivor-sheet Fitting ideals are exact.
Moreover, (25) proves only that five component orbits exist; two
further component orbits have since been certified, and the pure
`P_4` incidence is still not known to be exhaustive.

The next exact task on these branches is therefore their boundary
marked fibre, alongside the conceptual component classification.

## Verification

Run:

```text
python verify_p4_diagonal_quadric_one_three_components.py
python audit_p4_diagonal_quadric_one_three_components.py
```

The primary verifier checks the cubic map (4), the radical calculation
(9), the coefficient formulas (13), the factorization (14), all
family and incidence minors (21)--(24), the pair profiles, and the
jump signatures (25) over the rationals.  The independent audit uses a
separate dynamic-programming permanent, finite-field dual numbers,
modular Grassmann reduction, and modular rank computations at two
primes.  Those modular calculations replay the certificates without
importing the primary verifier; the displayed rational identities and
smooth-point argument prove the theorem over `C`.
