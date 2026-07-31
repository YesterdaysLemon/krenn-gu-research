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

Four cells are already resolved by exact repository theorems: the all-rank-
two star is empty, the `(2,2,1)` star is component ten or lower-pair, the
all-rank-two triangle is a component-eleven divisor, and the `(2,2,1)`
triangle is empty.  The four cells containing at least two rank-one
relations have substantial orientation/support classifications but are not
yet globally exhausted.

For the dated continuation map, including a strictly unverified
common-singleton lead in the last triangle cell, see
[`NEXT_INSTANCE_HANDOFF_2026-07-31.md`](NEXT_INSTANCE_HANDOFF_2026-07-31.md).

This is a reduction of the pure-`P_4` component problem, not component
exhaustiveness and not a proof of the Krenn--Gu conjecture.

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
| star | `(2,2,2)` | empty by [`P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md`](P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md) |
| star | `(2,2,1)` | component ten on the rank-three stratum, with the support-two chart lower-pair, by [`P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_CLASSIFICATION.md`](P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_CLASSIFICATION.md) |
| triangle | `(2,2,2)` | the complete family in [`P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md`](P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md), contained in component eleven by [`P4_ALL_RANK_TWO_RELATION_TRIANGLE_COMPONENT_INCLUSION.md`](P4_ALL_RANK_TWO_RELATION_TRIANGLE_COMPONENT_INCLUSION.md) |
| triangle | `(2,2,1)` | empty by [`P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md`](P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md) |
| star | `(2,1,1)` | partially classified by the exact-pair, common-factor, and mixed-star normal forms; a global orientation/support closure is still missing |
| star | `(1,1,1)` | directed radical and mixed orientations are substantially classified, including the projective disjoint and overlapping mixed charts; a global orientation/support closure is still missing |
| triangle | `(2,1,1)` | crossed, common-factor, common-kernel, and support-one charts produce components one and eleven through thirteen or obstructions; their union is not yet proved exhaustive |
| triangle | `(1,1,1)` | cyclic and transitive tournament orientations are classified, but kernel--kernel/doubly oriented degeneracies still need a common closure theorem |

The lower-pair locus `min r_ij<=2` is already exhausted separately in
[`P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md`](P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md).
Therefore a proof that the last four rows of this table lie in the known
component closures would prove that the seventeen-component list is
exhaustive.

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
```

The primary verifier checks all admissible rank profiles, all minimal
matching transversals, their star/triangle classification, and the eight
relation-rank cells.  The independent audit reconstructs the minimal
transversals from subsets of `E(K_4)` and checks the rank-one factorization
of every nonzero matrix `(a b; c 0)` over `F_5`.  These finite checks audit
the constant-size combinatorics; equations (2) and (5)--(7) are the
characteristic-zero proof.
