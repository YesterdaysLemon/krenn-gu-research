# Classification of the radical-star pure `P_4` stratum

## Status

This is an exact generic-stratum classification over `C`.

Let `U_0,...,U_3` be planes for which the restriction of `P_4` is
nonzero and decomposable, and let `K_i` be the kernel line of its
nonzero factor on `U_i`.  Suppose, after permuting the modes, that

```text
dim(U_1 U_3)=dim(U_2 U_3)=3
```

and that the two one-dimensional multiplication kernels are rank-one
relations

```text
ker(U_1 tensor U_3 -> R_2)=span(y_1 tensor w_3),
ker(U_2 tensor U_3 -> R_2)=span(y_2 tensor v_3),    (1)
```

where `y_i` spans `K_i`, `w_3,v_3` are independent, and

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

On the dense stratum where the two zero products in (1) have distinct
two-coordinate supports, the tuple belongs to one of exactly four
already certified component closures:

1. the irreducible `2+2` diagonal-quadric component;
2. one of the three `1+3` components `L_1,L_2,L_3`.

Thus no further pure-`P_4` component can arise generically from this
directed radical-star configuration.  The theorem does not classify
the other mixed edge orientations, the triangle configuration,
coincident coordinate-pair supports, rank-two-or-lower pair images, or
the whole pure-compression locus.  A disjoint-support mixed orientation
has since produced an eighth component in
[`P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`](../../../components/disjoint-mixed-star/P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md).

## Why exceptional pairs form a small graph

The degree-two part `R_2` has dimension six and its multiplication
pairing

```text
R_2 tensor R_2 -> R_4=C
```

is perfect.  Put

```text
r_ij=dim(U_i U_j subset R_2).
```

The flattening between opposite pair images has rank one because the
restricted four-tensor is nonzero and pure.  For subspaces of a
six-dimensional perfect pairing, its rank is at least
`r_ij+r_kl-6`.  Hence

```text
r_ij+r_kl <= 7                                     (2)
```

for every perfect matching `{ij|kl}`.

If every pair rank is at least three, choose one rank-three edge from
each of the three opposite edge pairs of `K_4`.  The chosen edges
contain no opposite pair, so they form either a star or a triangle.
Pair ranks at most two are a separate, more degenerate boundary.

Choose bases `(y_i,x_i)` with `y_i` spanning `K_i`.  If `r_ij=3`,
the unique multiplication relation has coefficient matrix

```text
( A B )
( C 0 ).                                           (3)
```

The lower-right entry is zero because the active-active coefficient
is detected nontrivially by an opposite active product.  A rank-one
matrix in (3) therefore factors through the pure kernel line at at
least one endpoint.  This gives the directed rank-one relations in
(1).

## Zero products are coordinate-pair objects

For nonzero linear forms `u,v`, the equation `uv=0` in `R_2` is

```text
u_a v_b+u_b v_a=0,    a<b.                         (4)
```

If `u` has a nonzero coordinate outside the support of `v`, (4)
immediately forces the corresponding coordinates of `v` to vanish.
On a common support of size at least three, the ratios `v_a/u_a`
would have to be pairwise negatives, which is impossible in
characteristic zero.  Therefore both forms lie in one coordinate
two-plane, and on a genuine two-coordinate support they are the two
opposite isotropic directions of the binary product.

Consequently the two independent vectors `w_3,v_3` in (1) carry two
coordinate-pair labels.  Distinct labels have only two possibilities:

```text
disjoint supports       -> 2+2 block plane,
one-coordinate overlap  -> 1+3 block plane.        (5)
```

Moreover `y_1 w_3=y_2 v_3=0` implies

```text
P_4(y_1,y_2,w_3,z)=P_4(y_1,y_2,v_3,z)=0
```

for every `z`.  Thus

```text
U_3=span(w_3,v_3)
```

is the radical of the double contraction
`P_4(y_1,y_2,-,-)` on the dense rank-two stratum.  This proves that
the radical-plane normal forms are forced by the directed
zero-product geometry.

## The `2+2` normal form

Diagonal source scaling and a coordinate permutation normalize the
disjoint support case to

```text
y_1=(1,0,0,-1),       y_2=(0,1,-1,0),
k_0=(1,0,0, 1),       k_1=(0,1, 1,0),
U_3=span(k_0,k_1).                                  (6)
```

Every plane containing `y_1` has, on a dense chart, a complementary
row

```text
x_1=(A,C+B,C-B,A),
```

because shifting by `y_1` equalizes coordinates zero and three.
Likewise every plane containing `y_2` has a complementary row

```text
x_2=(H+E,F,F,H-E).                                  (7)
```

The remaining one-kernel vanishing equations force `U_0` to be the
common kernel of

```text
(-F,-E,-E,F),       (-B,-A,A,-B),
```

hence

```text
U_0=span((E,-F,-F,-E),(A,-B,B,A)).                 (8)
```

The four planes (6)--(8) are precisely the normal form in
[`P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md`](../../../components/diagonal-quadric/P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md).
Only a `2 x 2` active block remains, and its determinant is `-16 Psi`,
where

```text
Psi =
 A^3 F^3+A^2 C F^2 H-A B^2 F H^2
 -A C^2 E^2 F+A C^2 F H^2-B^2 C E^2 H.             (9)
```

The `(3,3)` polynomial `Psi` is irreducible.  Its diagonal-source
orbit is the previously certified second component.  Therefore the
dense `2+2` radical-star stratum has no additional component.

## The `1+3` normal form

The overlapping support case normalizes to

```text
y_1=(0,1,-1,0),       y_2=(0,1,0,-1),
z_1=(0,1, 1,0),       z_2=(0,1,0, 1),
U_3=span(z_1,z_2).                                  (10)
```

On the chart where the complementary rows have nonzero coordinate
zero, row scaling and shifts by `y_1,y_2` give

```text
x_1=(1,0,S,D),       x_2=(1,0,G,T).                (11)
```

Put `P=G-T`, `Q=D-S`.  The one-kernel equations force

```text
U_0=span(
 (2,P+Q,Q-P,0),
 (0,0,1,1)).                                       (12)
```

The surviving active determinant is

```text
(D-G-S+T)(D+G-S-T)(D+G+S+T).                       (13)
```

Thus the dense `1+3` radical-star pure locus has exactly the three
branches

```text
L_1: T=-D+G+S,
L_2: T= D+G-S,
L_3: T=-D-G-S.                                     (14)
```

Their component status and mutual inequivalence were certified in
[`P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md`](../../../../../P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md).

## What remains

The structural component question is now narrower than “find every
plane tuple.”  Its unresolved generic alternatives are:

1. rank-one exceptional relations whose kernel endpoint orientations
   are mixed, including the known triangle component and orientations
   outside the now-certified disjoint-support chart;
2. configurations containing rank-two exceptional relations.  Each
   individual exact rank-two pair is now reduced, without elimination,
   to a secant `2+2`/`1+3` block center or a coincident-plane tangent
   through a coordinate line in
   [`P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md`](../../../../../P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md);
   compatibility among several pencils and with rank-one edges is now
   partially classified.  A proposed pure rank-two-star obstruction and a
   proposed mixed `(2,2,1)` triangle obstruction were withdrawn after a
   Borel-gauge audit; their historical records are
   [`P4_RANK_TWO_RELATION_STAR_OBSTRUCTION_WITHDRAWN_OVERSTRONG.md`](../../../../../P4_RANK_TWO_RELATION_STAR_OBSTRUCTION_WITHDRAWN_OVERSTRONG.md),
   [`P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION_WITHDRAWN_PENDING_BOREL_AUDIT.md`](../../../../../P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION_WITHDRAWN_PENDING_BOREL_AUDIT.md).
   The triangle where all three pair images have rank three and all
   three relation matrices have rank two has an intrinsic holonomy.
   Away from its resonant divisor it reduces to
   three cyclic cut forms in
   [`P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md`](../../../../../P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md).
   The full-support all-`1+3` cycle is now impossible: cut-factor
   reflection forces a common singleton coordinate, after which the
   triangle becomes an embedded pure `P_3` and all three pair ranks
   drop to at most two:
   [`P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md`](../../../../../P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md);
   a hyperbolic anchor/crossed-graph argument also excludes every
   full-support cycle containing a `2+2` cut:
   [`P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md`](../../../../../P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md).
   The one-edge and two-edge cut boundaries force a coordinate-plane
   rank collapse or a common embedded-`P_3` hyperplane:
   [`P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md`](../../../../../P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md).
   Hence the entire nonresonant triangle is empty.  On resonance, the
   additive holonomy separates a tangent-Segre cut cycle from a compressed
   `Sym^3(C^2) -> R_3` map:
   [`P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md`](../../../../../P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md).
   The tangent branch is empty.  On the flat branch, the true
   Borel-generic and one-kernel-zero otherwise-distinct charts are
   empty by
   [`P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md`](../../../../../P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md)
   and
   [`P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md`](../../../../../P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md).
   The projective sheets over the generic center are also excluded from the
   triangle after their three additive-parallelogram pure curves are shown
   to have a lower-rank partner pair:
   [`P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md`](../../../../../P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md).
   The full-support collisions are also excluded: the `2+1+1` and `3+1`
   active cubes vanish, while every pure `2+2` point has a lower-rank
   partner pair:
   [`P4_RESONANT_FLAT_FULL_KERNEL_COLLISION_CLASSIFICATION.md`](../../../../../P4_RESONANT_FLAT_FULL_KERNEL_COLLISION_CLASSIFICATION.md).
   The smaller-support strata are now classified.  Their unique
   rank-three survivor is the support-two annihilator-line family in
   [`P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md`](../../triangle-211/rank-two-relation-triangle-corrected/P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md);
   the dependent rank-two-relation star has also been reproved with the
   Borel markings retained:
   [`P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md`](../rank-two-relation-star-obstruction/P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md).
   The mixed `(2,2,1)` rank-three triangle has likewise been excluded in the
   corrected marked charts; the last `2+2` chart reduces to a presymplectic
   commutator determinant:
   [`P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md`](../../../../../P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md).
   The full-support mixed star with two rank-two spokes and one rank-one spoke
   is not empty: its Cayley-toric two-parameter chart has a smooth
   five-dimensional diagonal-source closure and supplies a tenth component:
   [`P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md`](../two-rank-two-spoke-mixed-star-component/P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md).
   A reverse marked-chart theorem proves that this family exhausts the whole
   rank-three `{1,2,2}` star stratum:
   [`P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_CLASSIFICATION.md`](../two-rank-two-spoke-mixed-star-classification/P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_CLASSIFICATION.md).
   The known first component's dense one-rank-two triangle orientation now has
   a fixed-triangle/apolar-`P^2` normal form:
   [`P4_FIRST_COMPONENT_APOLAR_TRIANGLE_NORMAL_FORM.md`](../../../../../P4_FIRST_COMPONENT_APOLAR_TRIANGLE_NORMAL_FORM.md).
   Its other Borel orientations/support collisions and special lower-pair-rank
   boundaries remain open;
3. the lower pair-image-rank and coincident/support-one zero-product
   boundaries.  One rank-two-edge stratum now supplies the
   six-dimensional component in
   [`P4_SIX_DIMENSIONAL_PURE_COMPONENT.md`](../../../components/six-dimensional/P4_SIX_DIMENSIONAL_PURE_COMPONENT.md),
   while the common `1+3` triple-rank-drop stratum supplies a distinct
   six-dimensional embedded-`P_3` component in
   [`P4_EMBEDDED_P3_PURE_COMPONENT.md`](../../../components/embedded-p3/P4_EMBEDDED_P3_PURE_COMPONENT.md).
   The full lower-rank boundary is still not classified.

The common smooth diagonal-quadric semisimple case is separately
excluded in
[`P4_COMMON_SMOOTH_DIAGONAL_QUADRIC_OBSTRUCTION.md`](../../../../../P4_COMMON_SMOOTH_DIAGONAL_QUADRIC_OBSTRUCTION.md).

## Verification

Run:

```text
python \
  claims/p4/classifications/star/radical-star/verify_p4_radical_star_component_classification.py

python claims/p4/classifications/star/radical-star/audit_p4_radical_star_component_classification.py
```

The primary verifier reconstructs the perfect-pairing bound, both
double contractions, the dense complement normalizations, the forced
common-kernel planes, and the two active determinants.  It also checks
the generic exceptional-edge relation ranks and source support
patterns.

The independent audit imports nothing from the primary verifier.  It
uses a dynamic-programming permanent and modular linear algebra at
`101,103` to replay both normal forms, their pair profiles, rank-one
zero-product directions, and determinant factorizations.  The
displayed characteristic-zero identities and the cited irreducibility
and component certificates prove the theorem over `C`.
