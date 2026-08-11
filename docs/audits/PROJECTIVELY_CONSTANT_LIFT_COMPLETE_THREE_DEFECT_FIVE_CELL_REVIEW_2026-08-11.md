# Adversarial review of the complete three-defect five-cell detector

## Review status and provenance

This record reviews
[`PROJECTIVELY_CONSTANT_LIFT_COMPLETE_THREE_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md`](../../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_THREE_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md)
as a conditional characteristic-zero detector theorem and fixed-layer
boundary reduction.

Codex reconstructed the fixed-`P_5` incidence argument, the arbitrary-ratio
collision intersections, and all four inactive-set contradictions separately
from the focused verifier.  The standard-library audit imports no repository
code or computer algebra and rebuilds the collision matrices through a
recursive permanent.  This is durable adversarial reasoning, not independent
human review.

Review verdict: **accept exclusion of every `b=0` defect at the fixed
five-cell layer and complete two-open detection for every exactly-three-defect
`R/B` cell**, after the focused and repository-wide replay gates pass.
Together with the preceding results, every aligned projective `q=0,r=5` cell
with at most three defects is detected.  Four- and five-defect `R/B` cells
remain open.  No witness is excluded, and global Krenn--Gu remains
**UNRESOLVED**.

## 1. Reconstructed obligation

The preceding endpoint detects every cell with at most two local defects.  In
an exactly-three-defect cell, collective invisibility gives an inactive set
at each defect:

```text
I_w={p:P_4(h_p,a,a,b;B-{w})=0},       |I_w|>=2.       (1)
```

The reviewed proof must turn the three large subsets of a four-root set into
a contradiction.  This requires exact information about intersections of
retained collision kernels; dimension counts alone are insufficient.

The fixed five-mode layer is

```text
P_5(h_1,h_2,h_3,h_4,b)=sum_c X_c e_c^(tensor 5),
X_0 X_1 X_2!=0.                                      (2)
```

Every local source-row span in (2) has dimension three, and each persistent
root row family has full cross-mode span.

## 2. The fixed layer removes `A` and `Z`

At a mode with `b_w=0`, the source pair `{b,h_p}` spans only the line of
`h_(p,w)`.  Five-mode row-pair incidence says that every such line contains a
target coordinate covector.  Hence all four roots are nonzero coordinate
rows at that mode.

Local rank three forces their coordinate multiplicities to be `2+1+1`; the
fifth source row `b` is zero.  The two singleton target colours therefore
have pullbacks supported on two distinct singleton source rows.  The exact
two-singleton `P_5` obstruction excludes this profile.

The review checked two scope points.

1. Nonzero weights in (2) can be normalized at one target mode without
   changing source supports.
2. Although the imported obstruction is written over `C`, any hypothetical
   characteristic-zero restriction descends to a finitely generated field
   over `Q`, which embeds in `C`; zero patterns and nonzero minors are
   preserved.

Thus an actual dependent mode has `b_w!=0` and is exactly

```text
R: a_w=lambda_w b_w, lambda_w!=0;       or       B: a_w=0.    (3)
```

This strengthens the fixed-layer classification.  It does not retroactively
change the scopes of the earlier `A/Z` detector theorems.

## 3. Exact collision interface

With three defects and two transverse modes, every retained four-mode word is
one of

```text
RRTT,                     RBTT,                     BBTT.      (4)
```

Direct labelled expansion of `P_4(h,a,a,b)` gives ranks `10,9,5` on the
twelve retained local coordinates.  More importantly, it gives the following
structural consequences.

- In `RRTT`, both regular values of a kernel row lie on their `b` lines and
  both transverse values lie in their local `a/b` planes.
- In `RBTT`, the retained regular and `B` values lie on their `b` lines and
  both transverse values lie in their `a/b` planes.
- In `BBTT`, the two `B` values lie on their `b` lines; transverse values may
  be arbitrary.

The review reconstructed the decisive common kernels.

### `RRB`

Either regular deletion kernel has zero intersection with the `B` deletion
kernel.  The two regular deletion kernels have a three-dimensional common
kernel contained in the local `a/b` planes at both transverse modes.

### `RRR`

For regular ratios `lambda_u,lambda_v`, the two deletion kernels have zero
intersection unless `lambda_u=lambda_v`.  A pinned full-rank minor is

```text
196608 lambda_v^3 lambda_w^7
       (lambda_u-lambda_v)^2.                         (5)
```

At equality the intersection has dimension two and remains on the defect
`b` lines and transverse `a/b` planes.  The triple intersection is zero
unless all three ratios agree.  When they agree, it is one-dimensional, zero
at all three defects, and supported only at the two transverse modes.

This ratio distinction is load-bearing.  Treating the normalized
all-ratios-equal chart as generic would overstate the common kernel and was
explicitly rejected during review.

### `RBB`

The triple common kernel has dimension two and is zero at both `B` defects.
At the transverse modes it consists of independent multiples of the local
`a` rows; the regular value is the corresponding compensating multiple of
`b`.

### `BBB`

A pair common kernel puts the row on the `b` line at all three defects.  The
triple common kernel is exactly zero at the three defects and arbitrary at
the two transverse modes.

These are collision-kernel statements only.  The proof connects them to (2)
through inactive-set size, local rank, full root span, and permanent
incidence; it does not call a kernel vector a witness.

## 4. Reconstruction of the four type cases

### `RRB`

The `B` inactive set is disjoint from both regular inactive sets.  Since all
three sets have size at least two inside four roots, the `B` set is a pair and
both regular sets are its complementary pair.  The first pair lies in an
`RRTT` kernel and the second in the common regular kernel.  At either
transverse mode all four roots and `b` lie in the local `a/b` plane,
contradicting rank three.

### `RRR`

Each inactive set has size exactly two: three inactive roots at one deletion
would lie with `b` on one line at another regular defect and leave local rank
at most two.

- Three distinct ratios would make the three inactive pairs pairwise
  disjoint, impossible on four roots.
- If exactly two ratios agree, both equal-ratio inactive pairs are the
  complement of the third.  Their common kernel and the third deletion
  kernel put all roots in the transverse `a/b` planes.
- If all ratios agree, no root can be triple-inactive because its row family
  would be supported at only two modes.  The only membership degree sequences
  are `(2,2,1,1)` and `(2,2,2,0)`.  The first puts every root in a deletion
  kernel and hence in the transverse planes.  The second puts three roots in
  pair common kernels and hence on the `b` line at every defect.  Both violate
  local rank three.

### `RBB`

The two `B` inactive sets are pairs.  Their union cannot be all four roots,
or every root would lie in the transverse planes.  A proper three-root
diamond would put three roots with `b` on the regular defect line.  Therefore
the two `B` sets are one common pair `J`.

At either `B` defect, the complementary two roots must both escape the `b`
line to give rank three.  A root inactive at the regular deletion lies on the
`b` line at both `B` defects, so the regular inactive set is also `J`.  The
triple kernel makes the two `J` rows zero at either `B` mode.

Pair incidence between a zero row and each of the three nonzero rows forces
those three rows to be coordinate rows.  Rank three makes their axes
distinct.  The resulting three-singleton-plus-two-zero profile violates the
two-singleton `P_5` obstruction.

### `BBB`

All three inactive sets are pairs, and their triple intersection is empty by
full root-row span.  In degree pattern `(2,2,2,0)`, three pair-inactive roots
lie with `b` on one line at every defect.  In pattern `(2,2,1,1)`, local rank
at a chosen defect would require both singleton-membership roots to have
their sole membership there; the same requirement cannot hold at either
other defect.  Both patterns fail.

## 5. Computational independence

The SymPy primary verifier reconstructs the labelled collision matrices and
checks:

- 36 rank-three coordinate profiles with `b=0`;
- retained collision ranks `RRTT/RBTT/BBTT = 10/9/5`;
- `RRB` common-kernel nullities `3/0/0`;
- the arbitrary-ratio `RRR` determinant (5), equality kernels, and the
  one-dimensional all-equal triple kernel;
- the two-dimensional `RBB` triple kernel and `BBB` pair/triple nullities
  `7/6`;
- all inactive-set ledgers; and
- the structural zero of the pair tensor with four or five `B` modes.

The audit imports no repository modules and no computer algebra.  It builds
each coefficient with a recursive four-row permanent and performs its own
`Fraction` row reduction.  It checks 64 `RRR` ratio charts and 192 pair
intersections, 16 `RRB` charts and 32 mixed intersections, four `RBB` charts,
the `BBB` kernels, and an independent bitmask census.  Its ratio grid contains
equal, unequal, and opposite nonzero values.

Neither bounded verifier proves the arbitrary-field theorem.  The written
labelled-expansion, incidence, inactive-set, and local-rank proof supplies the
mathematical implication; the scripts audit its formulas and case boundaries.

## 6. Exact acceptance boundary

Accepted:

- no actual fixed five-cell restriction has an `A` or `Z` defect;
- the exact `RRB`, ratio-sensitive `RRR`, `RBB`, and `BBB` collision
  interfaces;
- a nonzero collective two-open detector in every exactly-three-defect cell;
- conditional detection of every aligned projective `q=0,r=5` cell with at
  most three local defects, after importing the preceding detector theorems.

Still open:

- aligned projective `q=0,r=5` cells with four or five `R/B` defects;
- fixed-root injectivity and existence or exclusion of a witness;
- `q=0,r>=6`, every `q>=1` cell, and the unfactorized branch;
- universal extraction/gluing; and
- the global Krenn--Gu conjecture.

The four-/five-defect boundary is not cosmetic.  With four `B` modes, the
pair tensor `P_5(h_p,h_q,a,a,b)` is structurally zero because only three
non-`a` rows are available.  A different sensor or a fixed-layer exclusion is
needed there.

## Replay record

Before publication, run:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_complete_three_defect_five_cell_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_complete_three_defect_five_cell_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_complete_three_defect_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_complete_three_defect_five_cell_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_complete_three_defect_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_complete_three_defect_five_cell_detector.py
```
