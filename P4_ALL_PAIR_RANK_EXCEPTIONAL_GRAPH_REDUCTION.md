# The all-pair-rank `P_4` frontier is an eight-cell graph problem

## Status

**Exact characteristic-zero reduction.** Let four marked planes
`U_0,...,U_3` restrict `P_4` to a nonzero pure tensor, and suppose every pair
image has dimension at least three.  Then the rank-three exceptional graph
contains either a three-edge star or a three-edge triangle.  On each chosen
edge the unique relation has coefficient-matrix rank one or two.  Up to the
shape of the chosen graph and the number of rank-two relations, the
all-pair-rank component-exhaustiveness problem therefore has only eight
coarse cells.

All eight cells are now resolved by exact repository theorems: the all-rank-two
star is empty, the `(2,2,1)` star is component ten or lower-pair, the
all-rank-two triangle is a component-eleven divisor, the `(2,2,1)` triangle
is empty, every stratum of the rank-one triangle lies in a certified
component closure, and the `(2,1,1)` triangle is completely classified with
one new orbit, component twenty-two.  The complete `(2,1,1)` star adds
components twenty-three through twenty-five.  The `(1,1,1)` star is closed by
the all-center and all-double obstructions, the one- and two-double-spoke
classifications, and the two no-double endpoint ledgers.  No twenty-sixth
component occurs.

For the dated continuation map, including the now-certified
common-singleton component and the residual strata in the last triangle
cell, see
[`NEXT_INSTANCE_HANDOFF_2026-07-31.md`](docs/NEXT_INSTANCE_HANDOFF_2026-07-31.md).

Combined with the separately proved lower-pair exhaustion, this is now a
component-exhaustiveness theorem for the pure-`P_4` incidence: the twenty-five
certified component closures exhaust it.  It is not a proof of the
Krenn--Gu conjecture.

## Perfect pairing forces an exceptional transversal

Work in the squarefree Frobenius algebra

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Its multiplication pairing `R_2 x R_2 -> R_4=C` is perfect and
`dim R_2=6`.  Put

```text
W_ij=U_i U_j,       r_ij=dim W_ij.                 (1)
```

For complementary pairs `ij|kl`, purity makes the restricted pairing
`W_ij x W_kl -> C` have rank one.  For subspaces of a six-dimensional
perfect pairing, the restricted rank is at least
`r_ij+r_kl-6`.  Consequently

```text
r_ij+r_kl<=7.                                      (2)
```

On the present locus each `r_ij` is three or four.  Equation (2) says that
the rank-four edges can never contain one of the three perfect matchings

```text
01|23,       02|13,       03|12.                  (3)
```

Equivalently, the rank-three exceptional graph meets every matching in
(3).  Choose one exceptional edge from each matching.  The three selected
edges contain no disjoint pair.  A three-edge graph on four vertices with
that property is exactly one of

```text
star:      degree sequence (3,1,1,1),
triangle:  degree sequence (2,2,2,0).              (4)
```

There are four labelled stars and four labelled triangles.  This is the
entire graph-theoretic alternative; configurations with four, five, or six
rank-three edges still contain one of these minimal transversals.

## Every exceptional edge has relation rank one or two

Choose pure bases `(y_i,x_i)`, with `y_i` spanning the kernel line of the
nonzero pure factor.  A rank-three pair has a unique nonzero multiplication
relation

```text
a*y_i*y_j+b*y_i*x_j+c*x_i*y_j+d*x_i*x_j=0.        (5)
```

Multiply (5) by the two remaining active rows and evaluate in `R_4`.  The
first three terms are mixed coefficients of the pure tensor and vanish;
the last is `d` times the nonzero all-active coefficient.  Hence `d=0`, so
the relation matrix is

```text
M_ij=(a b; c 0).                                   (6)
```

It has rank two exactly when `bc!=0`.  Otherwise it has rank one and
factors through a kernel row at one or both endpoints:

```text
b=0:       (a*y_i+c*x_i)*y_j=0,
c=0:       y_i*(a*y_j+b*x_j)=0.                   (7)
```

Thus each selected edge receives the intrinsic label `1` or `2`.  Permuting
the three selected edges leaves only the number of rank-two labels.  Combining
that number `0,1,2,3` with (4) gives eight coarse cells.

## Exact frontier ledger

| selected graph | relation ranks | exact current status |
|---|---|---|
| star | `(2,2,2)` | empty by [`P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md`](claims/p4/classifications/star/rank-two-relation-star-obstruction/P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md) |
| star | `(2,2,1)` | component ten on the rank-three stratum, with the support-two chart lower-pair, by [`P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_CLASSIFICATION.md`](claims/p4/classifications/star/two-rank-two-spoke-mixed-star-classification/P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_CLASSIFICATION.md) |
| triangle | `(2,2,2)` | the complete family in [`P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md`](claims/p4/classifications/triangle-211/rank-two-relation-triangle-corrected/P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md), contained in component eleven by [`P4_ALL_RANK_TWO_RELATION_TRIANGLE_COMPONENT_INCLUSION.md`](claims/p4/classifications/triangle-211/all-rank-two-relation-triangle-inclusion/P4_ALL_RANK_TWO_RELATION_TRIANGLE_COMPONENT_INCLUSION.md) |
| triangle | `(2,2,1)` | empty by [`P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md`](P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md) |
| star | `(2,1,1)` | exhausted: the outward common-center-kernel orientation supplies component twenty-three, the complete mixed-center support ledger has component twenty-four as its sole all-pair survivor, the complete unequal-endpoint two-inward ledger has component twenty-five as its sole all-pair survivor, and the equal-endpoint inward stratum is empty; see [`P4_COMMON_CENTER_KERNEL_STAR_211_COMPONENT.md`](claims/p4/classifications/star/common-center-kernel-star-211/P4_COMMON_CENTER_KERNEL_STAR_211_COMPONENT.md), [`P4_SPLIT_CENTER_MIXED_STAR_211_COMPONENT.md`](claims/p4/classifications/triangle-211/split-center-mixed-star-211/P4_SPLIT_CENTER_MIXED_STAR_211_COMPONENT.md), [`P4_MIXED_CENTER_STAR_211_COMPLETE_CLASSIFICATION.md`](claims/p4/classifications/triangle-211/mixed-center-star-211-complete/P4_MIXED_CENTER_STAR_211_COMPLETE_CLASSIFICATION.md), [`P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPONENT.md`](claims/p4/classifications/star/unequal-endpoint-inward-star-211/P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPONENT.md), [`P4_EQUAL_ENDPOINT_INWARD_STAR_211_OBSTRUCTION.md`](claims/p4/classifications/star/equal-endpoint-inward-star-211-obstruction/P4_EQUAL_ENDPOINT_INWARD_STAR_211_OBSTRUCTION.md), and [`P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPLETE_CLASSIFICATION.md`](claims/p4/classifications/triangle-211/unequal-endpoint-inward-star-211-complete/P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPLETE_CLASSIFICATION.md) |
| star | `(1,1,1)` | exhausted: the strict all-three-arrows-to-center and all-three kernel--kernel orientations are empty; one- and two-double-spoke stars lie in known closures; no-double signature `(2,1,0,0)` is lower-pair or a completed triangle; and signature `(1,1,1,0)` lies in component 21, `L_1/L_2/L_3`, or a completed exterior triangle.  See [`P4_ALL_CENTER_KERNEL_STAR_111_OBSTRUCTION.md`](claims/p4/classifications/star/all-center-kernel-star-111-obstruction/P4_ALL_CENTER_KERNEL_STAR_111_OBSTRUCTION.md), [`P4_ALL_DOUBLE_ENDPOINT_STAR_111_OBSTRUCTION.md`](claims/p4/classifications/star/all-double-endpoint-star-111-obstruction/P4_ALL_DOUBLE_ENDPOINT_STAR_111_OBSTRUCTION.md), [`P4_ONE_DOUBLE_ENDPOINT_STAR_111_CLASSIFICATION.md`](claims/p4/classifications/star/one-double-endpoint-star-111/P4_ONE_DOUBLE_ENDPOINT_STAR_111_CLASSIFICATION.md), [`P4_TWO_DOUBLE_ENDPOINT_STAR_111_COMPLETE_CLASSIFICATION.md`](claims/p4/classifications/star/two-double-endpoint-star-111-complete/P4_TWO_DOUBLE_ENDPOINT_STAR_111_COMPLETE_CLASSIFICATION.md), [`P4_MIXED_ENDPOINT_STAR_111_COMPLETE_CLASSIFICATION.md`](claims/p4/classifications/star/mixed-endpoint-star-111-complete/P4_MIXED_ENDPOINT_STAR_111_COMPLETE_CLASSIFICATION.md), and [`P4_NO_DOUBLE_ENDPOINT_STAR_1110_COLLISION_CLASSIFICATION.md`](claims/p4/classifications/star/no-double-endpoint-star-1110-collision/P4_NO_DOUBLE_ENDPOINT_STAR_1110_COLLISION_CLASSIFICATION.md) |
| triangle | `(2,1,1)` | exhausted by the six Borel-flag orbits; component twenty-two is the sole new orbit, by [`P4_211_TRIANGLE_COMPLETE_CLASSIFICATION.md`](claims/p4/classifications/triangle-211/211-triangle-complete/P4_211_TRIANGLE_COMPLETE_CLASSIFICATION.md) |
| triangle | `(1,1,1)` | exhausted: tournament strata lie in known closures, the fully kernel--kernel stratum lies in components sixteen or eighteen, the exactly-two-kernel stratum lies in component eleven, and the exactly-one-kernel ledger closes through components eight, eleven, twelve, eighteen, nineteen, twenty, and twenty-one; see [`P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md`](P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md) |

The lower-pair locus `min r_ij<=2` is exhausted separately in
[`P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md`](P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md).
Every all-pair row in the table is now exhausted as well.  Therefore the
current twenty-five-component list is exhaustive.

Even that would not by itself prove `P_5 -> Delta_3` impossible: the marked
`H31/H22` theorems are generic on several components, so special fibres must
also be controlled or ruled out by a separate generic-to-global argument.

## Across the mathematical fence

The six pair ranks form a binary labelling of the edges of the tetrahedron.
Perfect pairing says that the rank-four edges avoid every 1-factor, so the
rank-three edges form a blocker of the 1-factorization of `K_4`.  Its minimal
blockers are precisely the four vertex stars and four complementary
triangles.  This is a tiny transversal-matroid statement hiding inside the
permanent tensor geometry.

The rank-one relations in (7) then turn the selected blocker into a directed
gain graph, while rank-two relations are synchronizer edges.  The remaining
classification problem is therefore a finite quiver-stratum problem with
continuous gain/annihilator data, not an unstructured polynomial search.

## Replay

```text
uv run --with sympy python verify_p4_all_pair_rank_exceptional_graph_reduction.py
python audit_p4_all_pair_rank_exceptional_graph_reduction.py

uv run --with sympy python claims/p4/classifications/star/no-double-endpoint-star-1110-collision/verify_p4_no_double_endpoint_star_1110_collision_classification.py
uv run --with sympy python claims/p4/classifications/star/no-double-endpoint-star-1110-collision/audit_p4_no_double_endpoint_star_1110_collision_classification.py
```

The primary verifier checks all admissible rank profiles, all minimal
matching transversals, their star/triangle classification, and the eight
relation-rank cells.  The independent audit reconstructs the minimal
transversals from subsets of `E(K_4)` and checks the rank-one factorization
of every nonzero matrix `(a b; c 0)` over `F_5`.  These finite checks audit
the constant-size combinatorics; equations (2) and (5)--(7) are the
characteristic-zero proof.
