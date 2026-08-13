# Self-review: `m=3` full-joint-cross-rank monomial-root-edge localization

Date: 2026-08-12

## Claim boundary

The theorem applies only on the S2Q common-three-space stratum `dim U=3`
and only when the joint `9 x 9` root--nonroot colour-column map is invertible.
Physical full-sensor rank does not imply this joint-rank hypothesis.  The
conclusion is a normal-form localization, not nonexistence.

The proof has three load-bearing inputs:

1. invertibility of the joint cross map identifies the singleton span with
   the full image of the shared derivative `D_B`;
2. S2R excludes a fully supported decomposable annihilator of that image.
3. The accepted exact six-vertex theorem excludes the graph reconstructed
   from an off-diagonal monomial by the explicit global pair formulas.

The first input reduces `dim U=3` to a statement about the three fixed
root--root blocks.  The second converts a single surviving bilinear block
into a Laurent polynomial with no torus zero, hence a monomial.

## Adversarial checks

- Two nonzero root blocks can intersect in a line when both are pure and
  share their common endpoint factor.  The proof uses the sharp lower bound
  `3+3-1=5`; it does not incorrectly assert a direct sum.
- A nonzero entangled root block still contributes a three-dimensional
  derivative subspace.  No matrix-rank assumption on the block is used.
- The Laurent argument needs algebraic closure.  The prize problem is over
  `C`; the characteristic-zero extension follows by the usual finitely
  generated-field embedding, and is stated at that scope.
- One coordinate monomial really has no zero on the coordinate torus, so the
  conclusion is sharp at the annihilator level.
- The sparse identity `G_N=J mod U` is inherited from S2R and does not assume
  that the rational pair deck is regular.
- If the two monomial endpoint colours differ, GHZ has no coefficient on the
  exceptional root line.  Grouping the six matchings by root `1` gives three
  exact `2 x 2` permanents, and division only by the fixed nonzero root-edge
  scalar makes them global physical pair blocks.  This is sufficient to use
  the six-vertex theorem; no Cramer regularity is assumed.
- Before the six-vertex exclusion, the exceptional words are `(a,p,q)`.
  The off-diagonal case is then eliminated, leaving `(a,s,s)`; exactly one
  GHZ diagonal word is exceptional.
- Numerical rank-loss searches were used only to select the next question.
  They are absent from the proof and evidence status.
- A tempting general claim was that every invertible joint cross map has
  block-permanent rank at least six.  Finite-field and numerical probes
  support it in this size but do not prove it, so the theorem does not use
  it.  The exact argument is restricted to monomial joint cross maps, where
  the rank is the permanent of a `3 x 3` integer count matrix.
- The Latin monomial equality control has rank exactly six.  Its sixth mixed
  matching is load-bearing: overlooking that matching would produce a false
  five-row target-incidence claim.

## Evidence independence

The primary replay uses SymPy column matrices and one exact two-term torus
construction.  The no-import audit uses standard-library `Fraction` row
reduction, transposed sparse column storage, a complete monomial-pair census,
and different coefficients for its torus cancellation.  It also reconstructs
the six matching terms independently before grouping them into pair blocks.
It separately builds the Latin `9 x 9` permutation and checks its output rank.
The arbitrary block intersection and arbitrary Laurent-support steps are the
written proofs, not claims of exhaustive symbolic search.

## Remaining obligation

The full-joint-rank branch is reduced to the block-permanent question

```text
invertible H and G_N in J + A_i tensor e_s tensor e_s.
```

The numerical experiments suggest rank loss for the required five-row
support but do not establish it.  The exact monomial subcase is excluded;
general nonmonomial cancellation, the joint-rank-at-most-eight branch, the
other S2Q strata, higher balanced order,
the all-rank-drop branch, and global Krenn--Gu remain open.  Repository and
global status therefore remain **UNRESOLVED**.
