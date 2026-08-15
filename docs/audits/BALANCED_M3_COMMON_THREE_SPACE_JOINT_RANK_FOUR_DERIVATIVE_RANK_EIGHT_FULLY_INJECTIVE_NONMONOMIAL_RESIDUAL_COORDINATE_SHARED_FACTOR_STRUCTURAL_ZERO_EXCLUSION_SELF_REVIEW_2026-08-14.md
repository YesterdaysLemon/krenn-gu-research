# Self-review: coordinate shared-factor structural-zero exclusion

Date: 2026-08-14

## Verdict

Accept the stated characteristic-zero exclusion of every structural-zero
successor having coordinate `x` or coordinate `y` in the fully-injective
joint-rank-four/derivative-rank-eight actual-nonmonomial residual cell,
subject to the staged validation below.

Together with S2CL--S2CN, this closes that actual-nonmonomial residual
branch.  Together with the monomial endpoint chain and the earlier row-profile
exclusions, it closes the complete joint-rank-four/derivative-rank-eight
common-three-space cell.  It does not close joint-rank-three/rank-eight or
derivative-rank-seven cells, other components or poles, higher orders, or
all-rank drop.  Global Krenn--Gu remains **UNRESOLVED**.

## Exhaustive case split checked

After a first/second-root exchange, normalize `x=e_s`; the exchange carries
the actual residual block to `-C^T` up to the harmless derivative-image sign
and preserves nonmonomiality, tangent-plane exclusion, complete faces, and
structural-zero conditions.

1. If `y_s!=0`, projection of `y^perp` to the two complementary coordinates
   identifies the restricted residual with an exact nonzero `2 x 2` matrix.
   Structural pairs are exactly its two cross-entry zeros.
2. With exactly one cross zero, independent rows force a common omitted
   physical-source factor.  Dependent rows are pure.  Nonzero diagonal
   entries then contradict transverse target factors, while either one-zero
   diagonal boundary is converted by an exact row shift into the S2CK
   zero-corner rectangle obstruction.
3. With both cross entries zero and both diagonals nonzero, the two-cross
   source geometry and the weighted diagonal difference contradict target
   transversality.  With one diagonal nonzero, the split-three-space/equal-
   plane dichotomy recovers the source quotient; a retained face is either
   immediately impossible or makes the actual `C` diagonal monomial.
4. If `y_s=0` and `y` is noncoordinate on the complementary two colours,
   `C(-,e_s)` is nonzero by the radical-line bound.  Its kernel gives the
   structural pair.  An independent pair forces two transverse targets into
   one omitted-factor slab.  A dependent full kernel does the same in a pure
   slab.  A dependent singleton kernel is aligned with `q_s` by exact
   symmetry, after which the retained `s`-face is impossible, including
   `s=t` because every tangent-source term dies in the source quotient.
5. If `y=e_r` is coordinate, the complementary restricted matrix is exhausted
   by rank one, rank two with nonzero corner, and rank two with zero corner.
   The first two have two structural pairs and a nonzero weighted `T_k`
   diagonal combination, so the S2CI incidence split aligns the quotient and
   a retained colour in `{s,r}\{t}` contradicts its target.
6. On the last rank-two zero-corner boundary, an independent zero pair first
   forces `R=P=ker(lambda_k)` before any whole-slice quotient is used.  For a
   dependent pure pair, radical uniqueness gives the common plane and a
   rank-one pure-row pencil.  Missing-source and full-support pencil forks are
   closed using only the retained diagonal coefficient `P_(h,h,h)-T_h`, with
   `h in {s,r}\{t}`.

These cases are disjoint and exhaustive.  Every division is by a coefficient
proved nonzero in the named rank/support cell.

## Adversarial corrections retained

- An earlier one-projection argument incorrectly claimed that a physical-
  source quotient killed an entire full root slice.  The final proof first
  proves the stronger equal-plane geometry in the independent boundary and
  uses only one diagonal coefficient in the dependent boundary.
- A related exploratory claim treated a one-sided source extension as if both
  source projections were fixed.  It was retracted; no such step occurs here.
- A draft called a weighted difference of two diagonal maps a visible corner.
  The final theorem uses the difference only to show that at least one
  diagonal map is nonzero, invokes S2CI, and then aligns the common incidence
  slab with `T_k`.
- The proof never replaces the actual residual block by its tangent quotient
  when claiming monomiality.  The promotion to actual `C` occurs only through
  a complete retained face.

## Evidence matrix

| Evidence axis | Result |
|---|---|
| Mathematical status | proved exact exclusion |
| Scope | coordinate-shared-factor structural successor in the fully-injective rank-four/rank-eight actual-nonmonomial cell |
| Case coverage | `y_s!=0`; `y_s=0` noncoordinate; coordinate `y`; all matrix ranks and dependent/independent forks |
| Primary replay | deterministic SymPy exact arithmetic |
| Independent audit | separate adversarial proof reconstruction; no-import exact rational replay in the package |
| Formalization | not formalized in Lean |
| Global status | **UNRESOLVED** |

## Validation

The focused primary and independent replays, Ruff, candidate-tree hygiene,
the migration and lattice unit suites, and the zero-change link rewrite must
all pass on the staged candidate tree before checkpointing.

## Remaining obligation

The complete joint-rank-four/derivative-rank-eight common-three-space cell is
closed.  The next unresolved proof-topology obligations are the localized
joint-rank-three/rank-eight and derivative-rank-seven cells, pair regularity
elsewhere, other physical components and pole strata, higher balanced orders,
all-rank drop, and the global extraction/synchronization bridge.  Owner
wind-down forbids starting any of those successors in this checkpoint.
