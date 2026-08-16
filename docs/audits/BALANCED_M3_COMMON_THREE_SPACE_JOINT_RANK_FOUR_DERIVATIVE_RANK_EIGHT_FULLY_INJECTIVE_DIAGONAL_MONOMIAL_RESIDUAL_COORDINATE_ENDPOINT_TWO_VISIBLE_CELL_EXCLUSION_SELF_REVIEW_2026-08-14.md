# Self-review: diagonal two-visible-cell exclusion

Date: 2026-08-14

## Verdict

Accept the stated characteristic-zero exclusion of the complete two-visible
cell at both surviving diagonal monomial coordinate endpoints, subject to the
repository validation below.  The proof gives an exact fourteen-mask support
cover and excludes its four central and ten boundary masks by two analytic
tensor lemmas, independently replayed at their algebraic interfaces.

Together with S2CH and S2CJ this closes both diagonal monomial coordinate
endpoints.  S2CE already closes the off-diagonal endpoints, so the monomial-
residual branch of the fully-injective joint-rank-four/derivative-rank-eight
cell is closed.  No theorem reduces an arbitrary nonmonomial residual to this
branch.  Global Krenn--Gu remains **UNRESOLVED**.

## Load-bearing chain checked

1. S2CF's two visibility predicates and the upstream exclusions leave exactly
   fourteen ordered support masks: four central masks in
   `{01,012} by {01,012}` and ten boundary masks.  The cover retains every
   nonzero coordinate value and introduces no projective specialization.
2. On each central mask the perpendicular covectors
   `(x_1,-x_0,0)` and `(y_1,-y_0,0)` have zero correction and give one mixed
   map whose three values are nonzero multiples of `T_0,T_1,0`.  Thus its
   image contains the full transverse secant.
3. The mixed-map lemma is exhaustive in the number of source components of
   one row.  A pure row fixes one factor.  A two-source row reduces at its own
   value to zero or a secant endpoint and then forces a fixed factor or a
   Segre tangent.  A full-support row is controlled by retractions to the
   endpoint `2 x 2 x 2` factors: Cayley's hyperdeterminant vanishes on the
   projected tangent and is nonzero on the secant interior.
4. The zero and endpoint forks in the full-support case are explicit.  The
   square kernel keeps the zero fork in one tangent space.  In the endpoint
   fork, quotienting the tangent equation fixes two row factor lines and
   confines all decomposable image points to sharing one of them.  Neither
   fork contains the transverse mate.
5. For each boundary mask the theorem displays bases `(c,A)` of `x^perp` and
   `(d,B)` of `y^perp`.  Coordinate multiplication gives
   `M(r_c,p_d)|Q=0`, while exactly two of the other three rectangle corners
   are correction-free nonzero rank-one maps on `T_0,T_1`.  All coefficients
   used as nonzero are forced nonzero by the named support.
6. If the structural zero pair is independent, S2CG makes it a conjugate
   pair in a split two-source plane.  Since `dim Q=3` and `Alt(Q)!=0`, the
   omitted-source projection is one nonzero line.  Every permanent of three
   rows in `Q` shares that factor, so two corner images cannot be fully
   transverse.
7. If the zero pair is dependent, S2CG makes its common row pure.  The two
   adjacent shores already share its factor.  For an adjacent/diagonal pair,
   symmetry makes their common value zero.  When both omitted-source
   components of the remaining row are nonzero, pure-tensor cancellation
   confines the diagonal image to the union of two factor-sharing slabs.
   When either component vanishes, rank one forces the complementary
   projection of `Q` onto a single line and yields the same contradiction.
8. The four central masks plus the ten boundary rows exhaust the two-visible
   cell.  There is no solver count, generic chart, saturation, degeneration,
   or unproved boundary passage in this conclusion.

## Adversarial checks and scope controls

- Three independent research lanes reconstructed the central mixed-map
  obstruction, the boundary zero-corner obstruction, and the exact fourteen-
  mask atlas.  Each returned a mathematical PASS; one separately audited the
  actual written theorem and requested three load-bearing clarity repairs.
  The retraction boundary, endpoint quotient, and source-symmetry wording were
  repaired before promotion.
- The support-two mixed-map proof checks both the zero and endpoint cases.
  The full-support proof explicitly handles a projected base component that
  vanishes rather than assuming a generic retraction.
- The dependent zero-corner proof retains `t=0`, `a=0`, and `b=0`; it divides
  by no coordinate.  Characteristic zero is more than sufficient for the
  displayed factors of two and the polynomial/secant arguments.
- S2CG is used only through its proved coordinate-free zero-pair and radical
  classification on a three-space with `Alt(Q)!=0`.  The canonical-binomial
  residual excluded in S2CG is not imported as a premise.
- The result closes only the monomial residual branch in this one physical
  rank cell.  Other nonmonomial residuals, derivative ranks, components,
  poles, higher orders, all-rank-drop, and local-to-global extraction remain
  open.

## Verifier independence

The primary SymPy replay exhausts all fourteen support masks, checks every
perpendicular basis, structural zero, correction term, and target corner,
and verifies the tensor-coordinate and hyperdeterminant interfaces used by
both analytic lemmas.

The independent audit imports neither the primary verifier nor SymPy.  It
uses standard-library `Fraction` arithmetic and reverses colour-mask,
source-coordinate-triple, permanent-summand, and chart traversal.  It has
its own permanent/rank routines and independent fixtures for the central and
boundary interfaces.  Both scripts explicitly leave the source-support
classifications and S2CG theorem to the written proof.

## Validation

Validation at the candidate checkpoint completed as follows:

```text
primary SymPy replay:                         PASS
independent no-import Fraction audit:         PASS
Python byte compilation:                      PASS
Ruff:                                         PASS
candidate-tree hygiene:                       PASS
candidate-tree census:                        2,004 Python / 1,147 Markdown / 223 ledger entries
migration-tool unit tests:                    191 PASS
fourteen-vertex cycle-cover lattice tests:     14 PASS
link rewrite:                                 zero changes
```

## Remaining obligations

The smallest surviving residual in this cell is now genuinely nonmonomial.
The S2BQ tangent-quotient atlas and complete-target root/source flattenings
must be coupled without assuming a target-preserving degeneration to one of
the closed monomial endpoints.  Wider lower-rank cells, pair gates, other
physical components and pole strata, higher orders, and the all-balanced
rank-drop branch remain open.  The dedicated global resolution gate is not
triggered.
