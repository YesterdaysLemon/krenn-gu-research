# Simultaneous-pencil reduction for normalized `q4_211`

## Status

This is an exact structural reduction over `C` for the last normalized
high-coordinate branch of a possible restriction

```text
P_5 -> Delta_3.
```

It does **not** exclude normalized `q4_211`, prove
`P_5` does not restrict to `Delta_3`, or solve the arbitrary-order
Krenn--Gu prize conjecture.

The reduction replaces the remaining support-chart problem by a
simultaneous tensor-pencil condition.  Four rank-three local maps would
have to diagonalize a three-dimensional space of contractions of
`P_5`.  Equivalently, a natural off-diagonal contraction matrix must
have rank at most two.  The published positive support-four
construction and every point of its two-parameter family have rank
four.  Thus that construction cannot be lifted to `q4_211`; the
unresolved branch lies in a different, exceptional determinantal locus.

## Normal form

Suppose a distinguished local map has four coordinate rows with
multiplicities `2,1,1` and one noncoordinate row.  Permute the source
coordinates and target colours so the coordinate rows have colours

```text
0,0,1,2.
```

One simultaneous diagonal rescaling of the five source coordinates in
all modes changes `P_5` only by a nonzero overall scalar.  It therefore
normalizes the three pullbacks of the target-coordinate covectors to

```text
u_0=(a,1,1,0,0),
u_1=(b,0,0,1,0),
u_2=(c,0,0,0,1),                                    (1)
```

where at least two of `a,b,c` are nonzero.  The last condition says
that the row over source coordinate zero is genuinely noncoordinate.

Let

```text
L_i:C^5 -> C^3,   i=1,2,3,4,
```

be the other four local maps.  They all have rank three because the
target tensor is concise.  Define the linear contraction map

```text
Phi(z)=(tensor_i L_i)(z contract P_5).                (2)
```

If the original restriction has diagonal coefficients
`lambda_c != 0`, then

```text
Phi(u_c)=lambda_c e_c tensor e_c tensor e_c tensor e_c
for c=0,1,2.                                         (3)
```

The vectors in (1) are independent.  Hence their span `U` is a
three-plane, and `Phi` maps `U` isomorphically onto the diagonal
three-plane

```text
D=span(e_0^4,e_1^4,e_2^4).                           (4)
```

This simultaneous statement is strictly stronger than the existence
of one support-four contraction restricting to `Delta_3`.

## The support-four pencil

For `t=(t_0,t_1,t_2)`, equation (1) gives

```text
z(t)=t_0 u_0+t_1 u_1+t_2 u_2
    =(a t_0+b t_1+c t_2,t_0,t_0,t_1,t_2).            (5)
```

Intersect `U` with the source-coordinate hyperplane `z_0=0`.  In
target coordinates this is the projective line

```text
a t_0+b t_1+c t_2=0.                                 (6)
```

Because at least two coefficients in (6) are nonzero, the line contains
points with all three `t_c` nonzero.  Every such point gives a
support-four contraction

```text
z(t)=(0,t_0,t_0,t_1,t_2)
```

which the same four maps send to the rank-three diagonal tensor

```text
lambda_0 t_0 e_0^4+
lambda_1 t_1 e_1^4+
lambda_2 t_2 e_2^4.                                  (7)
```

Thus a hypothetical `q4_211` solution simultaneously diagonalizes the
entire pencil (6), rather than choosing one isolated support-four
contraction.

When `a b c != 0`, the three coordinate-boundary points of (6) are

```text
t_0=0: (0,c,-b),   z=(0,0,0,c,-b),
t_1=0: (c,0,-a),   z=(0,c,c,0,-a),
t_2=0: (b,-a,0),   z=(0,b,b,-a,0).                   (8)
```

The first is a support-two contraction and the other two are
support-three contractions.  Their target images are the three
two-colour diagonal boundary tensors.  This explains geometrically why
the known support-at-most-three obstruction is sharp but does not close
`q4_211`: the line meets that obstruction exactly in its
`Delta_2`-compatible boundary.

## Two embedded `P_4` tensors

The singleton-colour contractions in (1) always factor:

```text
u_1 contract P_5
  = Sym(e_1,e_2,e_4,e_0+b e_3),

u_2 contract P_5
  = Sym(e_1,e_2,e_3,e_0+c e_4).                      (9)
```

Their source hyperplanes have independent normals

```text
h_1=(b,0,0,-1,0),
h_2=(c,0,0,0,-1).                                    (10)
```

Write `R_i` for the three-dimensional row space of `L_i`.  Restriction
to the corresponding hyperplane has rank two exactly when
`h_j in R_i`.  The decomposable-`P_4` rank-drop theorem therefore gives

```text
|{i:h_1 in R_i}| >= 2,
|{i:h_2 in R_i}| >= 2.                               (11)
```

Selecting two incidences for each normal produces only three minimal
types under permutations of the four modes and interchange of the two
singleton colours: the two selected edges are parallel, adjacent, or
disjoint.  Extra normal containments must still be retained.

The doubled-colour contraction is

```text
u_0 contract P_5
  = x_3 x_4 (a x_1 x_2+x_0 x_2+x_0 x_1).             (12)
```

If `a=0`, it is a third embedded `P_4`, with normal
`h_0=(0,1,-1,0,0)`, and the three-normal incidence method applies.
If `a != 0`, the ternary quadratic in (12) has symmetric matrix

```text
[[0,1,1],
 [1,0,a],
 [1,a,0]]
```

of determinant `2a`.  Thus (12) is the nondegenerate `a b q` tensor
from the support-three contraction theorem.  That theorem excludes a
restriction of (12) to `Delta_3`, but (3) asks only for one nonzero pure
tensor, so no contradiction may be inferred.

## Determinantal formulation

Let `pi_off` delete the three diagonal target coordinates from
`(C^3)^{tensor 4}` and set

```text
M_L=pi_off composed with Phi:
    C^5 -> C^78.                                      (13)
```

Equation (3) says

```text
U subset ker(M_L).
```

Consequently every `q4_211` solution satisfies the basis-free
degeneracy condition

```text
rank(M_L) <= 2,                                       (14)
```

while the diagonal part of `Phi` has rank three on `ker(M_L)`.
Condition (14), together with the two Grassmannian incidence edges in
(11), is the new non-brute-force frontier.

## First incidence refinement

The generic parallel edge type now has an exact diagonal-pencil
reduction.  Assume `b c != 0`, and suppose two modes `A,B` contain both
normals in (10).  Double contraction by the two normals shows that the
image

```text
G=(L_C tensor L_D)(Sym(e_1,e_2))
```

through the complementary modes is either zero or a pure tensor on one
singleton target line.  The three doubled-colour contractions of
`u_0 contract P_5` force

```text
L_C(e_1+e_2) tensor L_D(v)
+L_C(v) tensor L_D(e_1+e_2)

in span(e_0 tensor e_0,G)
```

for every `v in span(e_0,e_3,e_4)`.

A two-dimensional diagonal matrix-pencil lemma then forces

```text
L_C(e_1+e_2)=L_D(e_1+e_2)=0.
```

If `G=0`, one of the two maps kills all of
`span(e_1,e_2)`.  Its row space is therefore
`span(e_0^*,e_3^*,e_4^*)` and contains both normals, producing a third
common incidence.  If `G` is nonzero, both complementary maps have
kernel `span(e_1+e_2)` on `span(e_1,e_2)` and map that source
two-plane onto the same singleton target line.  Quotienting the
original common modes by the opposite singleton line then gives two
rank-two maps with common kernel
`span(e_0+b e_3+c e_4)`.  One embedded `P_4` tensor would have to
vanish in this quotient, but it reduces to `-2b e_3^2` or
`-2c e_4^2`, both nonzero.  Thus the nonzero residual is impossible,
and the parallel type always reduces to an adjacent extra-incidence
boundary.

See
[`P5_Q4_211_PARALLEL_INCIDENCE_KERNEL_REDUCTION.md`](P5_Q4_211_PARALLEL_INCIDENCE_KERNEL_REDUCTION.md).

At any common-normal mode on `bc != 0`, quotient the target by the
image line of `span(e_1,e_2)`.  The induced rank-two map has source
kernel

```text
span(e_0+b e_3+c e_4).
```

The two cross residuals assemble into an order-four permanent tensor.
If exactly one cross scalar is nonzero, its image is pure, so the
decomposable-`P_4` rank-drop theorem forces another mode to contain

```text
(0,0,0,c,b).
```

If both cross scalars are nonzero, the same tensor maps to
`Delta_2`; this is sharp because `P_4` has exact subrank two.  Thus the
adjacent type first reduces to a fourth-normal incidence or a marked
`P_4 -> Delta_2` boundary.  Subsequent two-slice and alternating-gate
classifications exclude the entire marked boundary.  The
all-rank-two family violates a complement-pairing flattening, while the
two rank-one determinant strata violate respectively a triple-`n`
contraction and a double-`n` `P_3` sign-support condition.  Hence only
the one-cross fourth-normal incidence remains.  A projective-pencil
refinement shows that `n` always pulls back from target colour zero
and forces a whole opposite normal pencil into one remaining row
space.  Polarizing the permanent on the pure-slice pencil leaves only
the third root `u_1` or `u_2`, unless a double-normal or common-kernel
gate occurs.

See
[`P5_Q4_211_ADJACENT_P4_PENCIL_REDUCTION.md`](P5_Q4_211_ADJACENT_P4_PENCIL_REDUCTION.md).
The marked-slice classification and pair-image obstruction are:

- [`P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md`](../../p4/classifications/P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md)
- [`P5_Q4_211_MARKED_DELTA2_PAIR_IMAGE_OBSTRUCTION.md`](P5_Q4_211_MARKED_DELTA2_PAIR_IMAGE_OBSTRUCTION.md)
- [`P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md`](../../p4/classifications/P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md)
- [`P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md`](P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md)
- [`P5_Q4_211_ONE_CROSS_PENCIL_SATURATION_REDUCTION.md`](P5_Q4_211_ONE_CROSS_PENCIL_SATURATION_REDUCTION.md)
- [`P5_Q4_211_ONE_CROSS_DIRECTION_CONIC_REDUCTION.md`](P5_Q4_211_ONE_CROSS_DIRECTION_CONIC_REDUCTION.md)
- [`P5_Q4_211_ONE_CROSS_TWO_GATE_REDUCTION.md`](P5_Q4_211_ONE_CROSS_TWO_GATE_REDUCTION.md)
- [`P5_Q4_211_ONE_CROSS_DIRECTION_PLANE_OBSTRUCTION.md`](P5_Q4_211_ONE_CROSS_DIRECTION_PLANE_OBSTRUCTION.md)
- [`P5_Q4_211_ONE_CROSS_COMMON_KERNEL_OBSTRUCTION.md`](P5_Q4_211_ONE_CROSS_COMMON_KERNEL_OBSTRUCTION.md)

For the exact disjoint type on `abc != 0`, the mixed contraction

```text
(u_0,h_1,h_2) contract P_5
```

is a nondegenerate quadratic on

```text
H=span(e_1+e_2,e_1-e_2,e_0-b e_3-c e_4).
```

All four cross-pair images have matrix rank at most one.  Exact
disjointness and Sylvester's inequality force every local restriction
to `H` to have rank two.  Their four kernel lines lie in
`span(e_1+e_2,e_1-e_2)` and form a `K_(2,2)` polarity configuration.
The inverse quadratic restricts there to a rank-one form, so one whole
normal pair has common kernel `span(e_1+e_2)`.  This is an exact
common-kernel reduction.  A later propagation theorem leaves only
kernel patterns `(s,s,s,s)` and `(s,s,d,s)`, then excludes both.  Hence
the exact disjoint type is empty on `abc != 0`.

See:

- [`P5_Q4_211_DISJOINT_CONIC_POLARITY_REDUCTION.md`](P5_Q4_211_DISJOINT_CONIC_POLARITY_REDUCTION.md)
- [`P5_Q4_211_DISJOINT_EXCLUSION_THEOREM.md`](P5_Q4_211_DISJOINT_EXCLUSION_THEOREM.md)

The adjacent one-cross direction-plane and common-kernel gates are now
excluded as well.  Since the parallel case reselects as adjacent, the
adjacent and exact-disjoint theorems exhaust the two singleton-normal
containment sets.  Hence normalized `q4_211` is empty on `abc != 0`;
see
[`P5_Q4_211_GENERIC_EXCLUSION_THEOREM.md`](P5_Q4_211_GENERIC_EXCLUSION_THEOREM.md).

## The known support-four family is transverse

Apply (13) to the four integer maps in
[`SUPPORT_FOUR_P5_CONTRACTION_RESTRICTION.md`](../../arbitrary-order/SUPPORT_FOUR_P5_CONTRACTION_RESTRICTION.md).
Exact row reduction gives

```text
rank(M_L)=4,
ker(M_L)=span(1,1,1,1,0).                            (15)
```

The diagonal image of the displayed generator is `(12,12,12)`.
For example, the minor using off-diagonal target words

```text
0001, 0010, 0011, 1000
```

and missing-source columns `0,1,2,4` has determinant `128`.

For every point of the published parametric family satisfying

```text
u v w-u v-u w-u-v w-v-w-1=0,                          (16)
```

the vector `(1,1,1,1,0)` remains in the kernel because that contraction
is diagonal.  Hence the rank is at most four throughout the family.

It is exactly four everywhere on (16).  On the chart

```text
d=u v-u-v-1 != 0,
w=(u+1)(v+1)/d,
```

five explicit `4 x 4` minors first reduce a possible common zero to

```text
v in {0,1,-1,2,-2,-1/2,2/3}
or v^2+v+1=0.                                         (17)
```

Fourteen complementary minors have no common zero at any value in
(17), except `(v,u)=(0,-1)` and `(-1,0)`, where `d=0` and the chart
does not apply.  The locus `d=0` in (16) consists exactly of the two
parameter lines

```text
(u,v)=(-1,0) or (0,-1),
```

and the same minors have polynomial gcd one on each line.  Thus
`rank(M_L)=4` at every family point.  The whole family diagonalizes
only one contraction direction, two dimensions short of (14).

This does not classify all support-four restrictions.  It proves that
no point, including no exceptional degeneration, of the known positive
family lifts to `q4_211`.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q4_211_simultaneous_pencil.py
python claims/p5/frontier/audit_p5_q4_211_simultaneous_pencil.py
python claims/p5/frontier/verify_p5_q4_211_parallel_incidence.py
python claims/p5/frontier/audit_p5_q4_211_parallel_incidence.py
python claims/p5/frontier/verify_p5_q4_211_adjacent_p4_pencil.py
python claims/p5/frontier/audit_p5_q4_211_adjacent_p4_pencil.py
python claims/p4/classifications/verify_p4_marked_delta2_slice_classification.py
python claims/p4/classifications/audit_p4_marked_delta2_slice_classification.py
python claims/p5/frontier/verify_p5_q4_211_marked_delta2_pair_image.py
python claims/p5/frontier/audit_p5_q4_211_marked_delta2_pair_image.py
python claims/p4/boundaries/verify_p4_marked_delta2_alternating_gate.py
python claims/p4/boundaries/audit_p4_marked_delta2_alternating_gate.py
python claims/p5/frontier/verify_p5_q4_211_alternating_gate_obstruction.py
python claims/p5/frontier/audit_p5_q4_211_alternating_gate_obstruction.py
python claims/p5/frontier/verify_p5_q4_211_one_cross_pencil_saturation.py
python claims/p5/frontier/audit_p5_q4_211_one_cross_pencil_saturation.py
python claims/p5/frontier/verify_p5_q4_211_one_cross_direction_conic.py
python claims/p5/frontier/audit_p5_q4_211_one_cross_direction_conic.py
python claims/p5/frontier/verify_p5_q4_211_disjoint_conic_polarity.py
python claims/p5/frontier/audit_p5_q4_211_disjoint_conic_polarity.py
python claims/p5/frontier/verify_p5_q4_211_disjoint_exclusion.py
python claims/p5/frontier/audit_p5_q4_211_disjoint_exclusion.py
```

The primary verifier expands (9), (12), the pencil and its boundary,
enumerates the three two-edge incidence types, computes (15) and the
determinant `128` over `Q`, and performs the exact two-variable
elimination in (17).  The independent audit rebuilds the off-diagonal
map from the missing-coordinate rule over `F_5` and `F_7`, checks its
one-dimensional kernel and diagonal image at every finite-field point
of (16), and audits the pencil support formulas without importing the
primary code.  The parallel, adjacent, marked-slice, pair-image, and
disjoint incidence programs independently check the source
contractions, diagonal-pencil classification, marked `P_4` quotient,
slice compatibility, complement-pairing ranks, and conic-polarity
kernel configurations over `Q`, `F_3`, and `F_5`.  The finite-field
checks audit the formulas and case splits; the reductions and
elimination above are over `C`.
