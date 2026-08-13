# Hostile self-review: `m=3` joint-rank-five derivative and torus localization

## Scope under review

This review covers
[`BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md`](../../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md),
its focused SymPy verifier, and its independent standard-library audit.

The claimed result is a characteristic-zero localization at **joint rank
exactly five** on the normalized, target-consistent physical `m=3`
common-three-space stratum.  It does not exclude all rank-five points, joint
rank at most four, another S2T/S2Q component type, a higher order, a witness,
or a counterexample.  Global Krenn--Gu remains **UNRESOLVED**.

## Adversarial claim inventory

1. The old shared-factor derivative-rank-five contradiction is independent
   of `rank H` once its two-block normal form is assumed.
2. At `rank H=5`, the derivative has rank at most seven.  Exactly two blocks
   give the transverse rank-six case; three blocks give rank seven and a
   two-dimensional kernel contained in `K`.
3. In the two-block transverse case, an injective uninvolved row is excluded
   by the existing three-plane arguments even though its row image now meets
   the involved row image in one line.
4. A surviving uninvolved row has rank two.  Its kernel functional uses at
   most two target colours.
5. In the three-block equality case, Hilbert--Burch gives projection profiles
   `(2,2,2)`, `(1,2,2)`, `(1,1,2)`, or `(1,1,1)`.  The first is impossible;
   the last three satisfy the stated coordinate clauses.

## Hostile checks

### 1. Was `rank H=6` silently used in the shared-factor contradiction?

No.  It was used in S2AC to derive the bound `rank D_B<=6` and the dimension
of `K intersect ker D_B`.  Neither fact is used after the shared-factor
normal form is reached.  The actual contradiction uses only the coordinate
common factor, two unaffected target slices, the involved-row ranks, the
zero-diagonal matrix rank floor, and the rank-free crossed-pair lemma.  The
new theorem restates that argument rather than promoting the old scope by
name alone.

### 2. Is the derivative upper bound reversed or missing a quotient term?

No.  Since `D_B(K)=U`, the restriction has rank three.  Adding four domain
directions spanning the nine-dimensional domain modulo the five-plane `K`
can increase image rank by at most four.  Thus `rank D_B<=7`.  Separately,
rank--nullity on the restriction gives
`dim(K intersect ker D_B)=5-3=2`.

### 3. Does three-block rank seven really force `ker D_B subset K`?

Yes.  The three-nonzero-summand theorem gives nullity at most two, while the
upper bound gives nullity at least two.  Hence the full derivative kernel is
two-dimensional.  Its intersection with `K` already has dimension two, so
the two spaces agree.  The stronger identity `K=D_B^(-1)(U)` follows because
both sides have dimension `2+3=5`.

### 4. Is the Hilbert--Burch normal form being asserted only generically?

No.  Pairwise intersection bounds make every coordinate projection of the
two-dimensional syzygy space nonzero.  Over an infinite field, one syzygy
has all three components nonzero.  The exact argument from S2X writes the
three blocks as the signed `2 x 2` minors of two syzygy rows.  Dependent
components of the second row are retained and are precisely what produce
the `(1,2,2)`, `(1,1,2)`, and `(1,1,1)` boundary profiles.

### 5. Does beta zero annihilate only `U`, or the whole derivative image?

For the Hilbert--Burch blocks, the three contractions are the three pairwise
`2 x 2` determinants of the evaluation pairs.  When they vanish,
`D_B^*(alpha tensor beta tensor gamma)=0`.  The product therefore annihilates
the entire `image D_B`, which is stronger than annihilating `U`.  Applying
S2R is valid.

### 6. Could the `(2,2,2)` avoidance argument miss a coordinate divisor?

No.  Fixing one common evaluation pair and adding the three one-dimensional
annihilators parametrizes a five-dimensional beta-zero family.  For each
root separately, its pair and kernel parameters cover the whole dual
three-space.  Every target-coordinate evaluation is therefore a nonzero
linear form on the parameter space.  A finite union of its nine hyperplanes
cannot cover that space in characteristic zero, so a fully supported point
exists and contradicts S2R.

### 7. Are the boundary clauses for the lower projection profiles complete?

The component ideals were recomputed from the determinant equations:

```text
(1,2,2):  (a det(B,C), a B_2, a C_2) by cases a=0/a!=0;
(1,1,2):  (ab, a h, b g);
(1,1,1):  (ab, ag, bg).
```

Their components give respectively

```text
x and (c or w) coordinate;
(x or y), (x or z), (y or w) coordinate;
(x or y), (x or z), (y or z) coordinate.
```

The primary verifier and the independent audit separately replay the ideals
and Boolean covers.  These are necessary coordinate localizations, not
claims that the remaining cases exist or are excluded.

### 8. Does the rank-six three-plane proof require complementary row spaces?

The transferred parts do not.  S2AD's relation-plane argument uses only
`P`, `P^perp`, `U=D(P)`, and target consistency.  S2AE and S2AF use the row
relation in `P`, coefficientwise target identities, and that `image theta`
is a three-plane (or has a local projection of dimension at least two).
Their square-pencil and five-product lemmas never use
`V intersect image(theta)=0`.  At joint rank five, an injective `theta` has
a one-dimensional overlap with `V`, but all cited identities remain valid.

### 9. Is the uninvolved-row support bound too strong?

No.  If `eta` spans `ker theta`, then `eta(G_N)=0`.  Every target colour in
`support eta` supplies a distinct coordinate diagonal to `eta(U)`.  That
space lies in

```text
A_1 tensor b_eta+c_eta tensor A_2.
```

After quotienting both fixed factor lines, a decomposable tensor survives
only if its first factor is `c_eta` or its second factor is `b_eta`.  Two
fixed lines cover at most two distinct coordinate diagonals.  The theorem
does not infer which rank-two-row support-one or support-two cases survive.

### 10. What do the scripts not prove?

They exactly replay canonical derivative matrices, kernels, ranks,
transverse extension dimensions, beta-zero component equations, boundary
truth tables, and the two-line diagonal cover.  They do not replace the
arbitrary-vector Hilbert--Burch argument, the finite-hyperplane avoidance
argument, or the transfer audit of S2AD--S2AF.  Those arguments are written
in the theorem.  The independent audit imports no code from the primary
verifier and uses a separate `Fraction` elimination implementation.

## Verdict

The package supports the stated exact localization.  It closes the
rank-five shared-factor mechanism, every transverse case with an injective
uninvolved row, and the full-projection three-block Hilbert--Burch profile.
It leaves the transverse rank-two row, three explicit Hilbert--Burch
coordinate atlases, joint rank at most four, and all other global obligations
open.  Global status must remain **UNRESOLVED**.
