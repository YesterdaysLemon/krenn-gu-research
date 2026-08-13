# Self-review: complete `m=3` full-joint-cross-rank exclusion

## Claim audited

The full-joint-rank S2U sparse block-permanent normal form is empty over
characteristic zero.  The proof uses only its eighteen off-diagonal output
zeros.

## Scope and status

- S2U supplies the physical reduction, the unique diagonal monomial
  root--root edge, and the sparse target support.
- This theorem excludes only `rank H=9` in the common-three-space stratum.
- It does not touch `rank H<=8`, other S2T component types, other S2Q pole
  strata, higher orders, or the all-balanced branch.
- Global status remains **UNRESOLVED**.

## Adversarial proof checks

1. **Could three nonzero derivative summands have a three-dimensional
   kernel?**  No.  A kernel vector with all source components nonzero puts
   the pair tensors in the signed `2 x 2`-minor normal form.  Its degree-one
   syzygies are the two rows of the Hilbert--Burch matrix.  Their minors have
   three distinct complementary multidegrees and no common nonconstant
   factor.
2. **Was a finite-field atlas silently promoted to characteristic zero?**
   No.  Both scripts reconstruct rational kernel representatives and use
   exact rational elimination.  More importantly, the written derivative
   lemma proves the dichotomy without the atlas.
3. **Does derivative noninjectivity have more than the two synchronized
   forms?**  One nonzero pair tensor kills a source projection; three are
   ruled out by the syzygy lemma.  Two require the unique shared-factor line,
   whose kernel is a four-space.  A full-support three-plane in that
   four-space has exactly rank-two or rank-three projection to the remaining
   source.
4. **Does the regular zero-divisor classification fail in characteristic
   two?**  Yes: the all-three-source proportionality leaves a factor `2`.
   The theorem is deliberately characteristic zero and makes no
   characteristic-two claim.
5. **Could exceptional `q` vectors evade the displayed table?**  Solving
   `C=0`, `A=y tensor t`, `B=-x tensor t` first fixes the `X,Y` rank-one
   directions.  The remaining equation is (22), which separates the pure,
   synchronized, mixed, and generic cases exhaustively.
6. **Does the pigeonhole use independence correctly?**  For each `q_c`, the
   two rows `p_b`, `b!=c`, are independent because all nine rows of `H` are a
   basis.  Pairwise kernel intersections then control the remaining row.
7. **Is the permitted diagonal target support needed?**  No.  Only `b!=c`
   rows are used, so no coefficient on the five allowed rows is assumed.

## Mistakes found during development

The first attempted two-source splitting statement incorrectly asserted
rank six for every three-plane in a six-space.  Exact replay found the two
pure source planes have rank three.  Those cases were separated and routed
to the source-aligned theorem; all other 1393 binary three-planes have rank
six.  The universal proof here avoids extrapolating that splitting lemma to
three sources and instead classifies the shared-derivative kernel exactly.

A second discarded route tried to obtain the full result from the monomial
rank floor by torus degeneration.  Row and column torus weights give every
perfect matching the same total weight, so they cannot select a determinant
matching.  No such degeneration is used here.

## Evidence independence

The primary uses SymPy matrices, a rational 20-chart kernel atlas, and direct
symbolic orbit representatives.  The audit imports neither SymPy nor the
primary verifier; it has its own `Fraction` RREF/nullspace implementation,
reconstructs projection maps from kernel equations, and separately checks
the sharp syzygy, pair-product, and category boundaries.

The scripts replay identities and exhaustive finite normal forms.  The
written tensor and syzygy arguments are the proof over characteristic zero.
