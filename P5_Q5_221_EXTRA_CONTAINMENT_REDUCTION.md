# Extra-containment frontier for normalized `q5_221`

## Status

This is the exact combinatorial reduction used in the completed
normalized `q5_221` exclusion.

The nine exact six-incidence strata are excluded in the preceding
obstruction theorems.  Every incidence pattern with an extra normal
containment contains one of exactly fourteen marked seven-incidence
patterns.  Therefore a complete normalized `q5_221` exclusion reduces
to fourteen **monotone** obstruction statements: each must forbid maps
having at least its seven displayed containments, whether or not still
more containments occur.

Six of the fourteen monotone obstructions are proved by the
distinguished-normal multiplicity theorem: covers `#0--#4,#9` all have
three `h_2` incidences and are impossible even with further
containments.  The two-all-normal theorem also closes cover `#5`
monotonically.  The `h_1,h_2`-partner all-normal theorem closes covers
`#6,#11` monotonically, and the remaining fixed-kernel theorem closes
`#7,#10`.  Separate exact theorems exclude `#8,#12,#13`; the final
monotone-boundary theorem reduces every strict extension to two
eight-incidence orbits and excludes both.  Thus all fourteen cover
orbits are closed, completing normalized `q5_221`.  The separate
normalized `q4_211` branch, `P_5 -> Delta_3`, and the arbitrary-order
Krenn--Gu conjecture remain open.

## Incidence-poset formulation

Let

```text
D_c={i:h_c in U_i},  c=0,1,2,
```

for the four remaining modes `i=A,B,C,D`.  The `P_4` rank-drop theorem
gives

```text
|D_c|>=2.                                             (1)
```

The two majority colours `0,1` may be swapped.  The singleton colour
`2` is distinguished.  Mode permutations give the other symmetry
group `S_4`.

The exact-minimal layer has

```text
|D_0|+|D_1|+|D_2|=6
```

and consists of the nine marked types in
[`P5_Q5_221_HYPERPLANE_INCIDENCE_REDUCTION.md`](P5_Q5_221_HYPERPLANE_INCIDENCE_REDUCTION.md).
All nine are now excluded over `C`.

Suppose instead that the total incidence number is at least seven.
Choose two incidences in each row of the `3 x 4` incidence matrix.
At least one unchosen incidence remains; choose one.  The selected
submatrix has row-size multiset

```text
{3,2,2}.                                              (2)
```

Consequently every extra-containment stratum lies above a
seven-incidence cover of the minimal layer.  This is the first cover
layer of the Boolean incidence poset, or equivalently the first
Schubert boundary reached by imposing one additional normal
containment on the four kernel planes.

## Fourteen marked cover orbits

Write each `D_c` as a four-bit word in mode order `A,B,C,D`.  Up to
`S_4` and the majority-colour swap, the fourteen covers are:

```text
 #   D_0   D_1   D_2     mode incidence degrees

 0   0011  0011  0111       3,3,1,0  M
 1   0011  0011  1101       3,2,1,1  M
 2   0011  0101  0111       3,2,2,0  M
 3   0011  0101  1011       3,2,1,1  M
 4   0011  0101  1110       2,2,2,1  M
 5   0011  0111  0011       3,3,1,0  M
 6   0011  0111  0101       3,2,2,0  M
 7   0011  0111  1001       3,2,1,1  M
 8   0011  0111  1100       2,2,2,1  M
 9   0011  1100  0111       2,2,2,1  M
10   0011  1101  0011       3,2,1,1  M
11   0011  1101  0101       3,2,1,1  M
12   0011  1101  0110       2,2,2,1  M
13   0011  1101  1100       2,2,2,1  M              (3)
```

Here `M` means that the entire monotone cover is excluded.  The first
six `M` rows follow from
[`P5_Q5_221_DISTINGUISHED_NORMAL_MULTIPLICITY_THEOREM.md`](P5_Q5_221_DISTINGUISHED_NORMAL_MULTIPLICITY_THEOREM.md).
Cover `#5` follows from
[`P5_Q5_221_TWO_ALL_NORMAL_MODES_OBSTRUCTION.md`](P5_Q5_221_TWO_ALL_NORMAL_MODES_OBSTRUCTION.md).
The two further `M` rows follow from
[`P5_Q5_221_H1_PARTNER_ALL_NORMAL_OBSTRUCTION.md`](P5_Q5_221_H1_PARTNER_ALL_NORMAL_OBSTRUCTION.md).
The remaining fixed-kernel rows `#7,#10` follow from
[`P5_Q5_221_REMAINING_FIXED_KERNEL_OBSTRUCTION.md`](P5_Q5_221_REMAINING_FIXED_KERNEL_OBSTRUCTION.md).
Covers `#8,#12,#13` are first excluded on their exact
seven-incidence strata: cover `#12` is handled in
[`P5_Q5_221_TRIANGLE_OBSTRUCTION.md`](P5_Q5_221_TRIANGLE_OBSTRUCTION.md),
cover `#8` in
[`P5_Q5_221_REPEATED_MAJORITY_PAIR_COVER_OBSTRUCTION.md`](P5_Q5_221_REPEATED_MAJORITY_PAIR_COVER_OBSTRUCTION.md),
and cover `#13` in
[`P5_Q5_221_COVER_13_OBSTRUCTION.md`](P5_Q5_221_COVER_13_OBSTRUCTION.md).
Their strict extensions are lifted in
[`P5_Q5_221_FINAL_MONOTONE_BOUNDARY_OBSTRUCTION.md`](P5_Q5_221_FINAL_MONOTONE_BOUNDARY_OBSTRUCTION.md).

The four degree profiles in (3) have a useful Grassmannian meaning.
A mode of incidence degree three has

```text
U_i=span(h_0,h_1,h_2),
K_i=ker L_i=span(u_0,u_1),                           (4)
```

so its kernel plane is fixed.  A degree-two mode places `K_i` inside
one of the three coordinate three-spaces

```text
h_0^perp intersect h_1^perp,
h_0^perp intersect h_2^perp,
h_1^perp intersect h_2^perp.                         (5)
```

Thus:

- nine covers in (3) contain at least one fixed kernel plane (4);
- five covers have degree profile `2,2,2,1` and contain three kernel
  planes on the pair-incidence Schubert divisors (5), but no fixed
  kernel plane.

The second group splits into two geometric shapes: either all three
normal pairs occur, giving the triangle of spaces in (5), or one pair
occurs twice.  This suggests treating the frontier with kernel-plane
intersection and sign-rectangle transport, not with ambient support
search.

## Completion of the lifting step

The exact six-incidence theorems are open-stratum statements: they use
absence of unselected normals to reject rank-one residual gates.  They
cannot simply be invoked on a seven-incidence superpattern.

The required monotone statement had the form:

```text
there are no normalized q5_221 maps for which
h_c in U_i at every displayed incidence.             (6)
```

Statement (6) must allow all undisplayed incidences.  It is now proved
for all fourteen rows.  Therefore:

1. total incidence six is impossible by the nine exact-minimal
   theorems;
2. total incidence at least seven contains one of (3), and every row is
   impossible by its monotone theorem or its exact theorem plus the
   final boundary lift.

Those two items exclude normalized `q5_221` completely.  The next
normalized `P_5` target is the structurally separate `q4_211` branch.

## Verification

Run:

```text
python verify_p5_q5_221_extra_containment_reduction.py
python audit_p5_q5_221_extra_containment_reduction.py
```

The primary verifier enumerates the `3 x 4` seven-incidence matrices
and quotients by `S_4` and the majority-colour swap.  The independent
audit starts from the nine minimal marked orbits, adds one incidence,
and canonicalizes the resulting covers.  Both obtain the fourteen
representatives in (3).  This is a 1,331-state incidence calculation,
not a row-space or tensor search.
