# Nonzero additive holonomy is impossible

## Status

This is an exact characteristic-zero obstruction for the
`delta!=0` branch of
[`P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md`](P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md).
The proof reuses the already proved support, anchor, and
coordinate-hyperplane lemmas; no elimination or component search is
used.

Consequently the complete all-rank-two-relation triangle frontier is
now confined to

```text
Omega=0,                         delta=0,                            (1)
```

the flat affine connection whose multiplication factors through a
compressed binary cubic `Sym^3(C^2) -> R_3`.

The final flat branch has since been classified in
[`P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION.md`](P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION.md).
It has one lower-dimensional balanced `2+2` survivor.  Component
exhaustiveness, the other exceptional/lower-rank graphs, and the
global Krenn--Gu conjecture remain open.

## The tangent branch supplies three cuts

Use the normalized resonant relations

```text
A_ij y_i y_j+y_i x_j-x_i y_j=0
```

and

```text
delta=A_12+A_23-A_13 != 0.
```

The affine-holonomy theorem proves

```text
y_1y_2y_3=0,

x_1y_2y_3=y_1x_2y_3=y_1y_2x_3=0.                  (2)
```

For each pair put

```text
q_ij=y_i y_j.                                                     (3)
```

No `q_ij` is zero.  If, for example, `y_1y_2=0`, then
`y_1 tensor y_2` is a decomposable tensor in the one-dimensional
kernel of

```text
U_1 tensor U_2 -> R_2.
```

That unique relation would have coefficient-matrix rank one,
contradicting the triangle hypothesis that it has rank two.

Both rows of the opposite plane annihilate (3) by (2).  Since a
nonzero symmetric zero-diagonal catalecticant cannot have rank one,

```text
U_k=Ann_R1(q_ij),
rank C(q_ij)=2,                   {i,j,k}={1,2,3}.                   (4)
```

Thus all three kernel-pair products are weighted cuts.

## Proper supports are impossible

Suppose one `q_ij` has proper cut support.  It has either one edge or
two adjacent edges.

The proof of
[`P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md)
uses only:

1. the opposite-plane identity `U_k=Ann(q_ij)`;
2. rank-three products of `U_k` with each remaining plane; and
3. rank-two unique relations on those two edges.

All three statements hold here by (4) and the triangle hypotheses.
The one-edge case forces a partner product rank at most one; the
two-edge case puts all three planes in one coordinate hyperplane and
forces pair rank at most two.  Both contradict rank three.

Hence every `q_ij` has full cut support.

## A `2+2` cut is impossible

Suppose, after relabelling, that

```text
q_12=ab
```

is a full `2+2` cut across two binary coordinate blocks.  Its
annihilator is

```text
U_3=span(a_bar,b_bar).
```

The crossed-graph lemma in
[`P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md)
again uses only the two rank-three partner relations.  It proves that
neither `U_1` nor `U_2` contains either anchor line `C a,C b`.

But every factorization of `ab` contains one of those anchors, while

```text
ab=q_12=y_1y_2
```

is a factorization with one factor in each of `U_1,U_2`.  This is the
same anchor contradiction.  Therefore no `q_ij` has type `2+2`.

## Three full `1+3` cuts cannot close

Every `q_ij` is now a full-support `1+3` cut.  Let `s_k` be the
singleton coordinate of `q_ij`, so (4) gives

```text
U_k subset H_(s_k).                                                 (5)
```

Consider the factorization

```text
q_ij=y_i y_j.
```

Each factor already lies in a coordinate hyperplane by (5), applied
to the other two cuts.  The full `1+3` factorization lemma from
[`P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md)
says that the non-internal factorization sheet is fully supported.
It is therefore impossible here.  Both factors lie inside the
three-coordinate block of their cut:

```text
y_i,y_j in H_(s_k).                                                 (6)
```

Cyclically,

```text
y_i in H_(s_1) intersection H_(s_2) intersection H_(s_3)
                                                                  (7)
```

for every `i`.

If the labels have three distinct values, (7) is a coordinate line
and all pair products `y_iy_j` vanish, contradicting (3).

If the labels have exactly two values, (7) is a coordinate two-plane.
Every pair product is then supported on at most its single internal
edge, contradicting the full three-edge support of a `1+3` cut.

Thus all three labels agree:

```text
s_1=s_2=s_3=s.
```

Equation (5) puts all three planes `U_1,U_2,U_3` in `H_s`.  The
nonzero pure `P_4` restriction suspends a nonzero pure `P_3`
restriction.  Perfect pairing in the three-variable squarefree
algebra gives

```text
dim(U_iU_j)+2-3<=1,
```

so every pair rank is at most two.  This final contradiction proves
that `delta!=0` is empty.

## Consequence

The triangle reductions now read:

```text
Omega != 0                 empty,
Omega = 0, delta != 0      empty,
Omega = 0, delta = 0       compressed binary cubic; now classified. (8)
```

Thus no tangent-Segre first-jet component can occur on the
all-rank-two-relation triangle.  At this checkpoint the only remaining
triangle geometry was the flat synchronized binary cubic; the later
flat-triangle classification reduces it to one balanced `2+2` family
of dimension at most four.

## Verification

Run:

```text
python verify_p4_resonant_nonzero_additive_holonomy_obstruction.py
python audit_p4_resonant_nonzero_additive_holonomy_obstruction.py
```

The primary verifier replays the cut ranks, support alternatives,
anchor exclusion, label intersections, and final `P_3` pairing.  The
independent audit uses the opposite singleton convention and the
complete 64-label table.  These are exact proof replays, not searches.
