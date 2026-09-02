# Fibre-exact targets brief — 2026-09-01

## Status and purpose

This is a coordination brief for the next Krenn–Gu research runs.  It is
not a theorem, proof, frontier entry, or change of mathematical status.  The
global Krenn–Gu conjecture remains **UNRESOLVED**, and
[`docs/current-frontier.md`](../current-frontier.md) remains the canonical live
proof map.  It supersedes the operating emphasis of the
[2026-08-31 resolution-first brief](resolution-first-ecology-run-2026-08-31.md)
only where the two conflict; the earlier brief's rules on packaging,
integration, and what counts as progress still apply.

Refresh `origin/main`, inspect active worktrees and processes, and recheck
open PRs before acting.

## The exact target, and why `d = 3` is the whole conjecture

Question 1 of Krenn, Gu, and Soltész asks for which `(n, d)` there is a
bi-coloured complex-weighted graph on `n` vertices whose `d` monochromatic
inherited colourings have unit weight while every other colouring cancels.
Chandran, Gajjala, and Illickan (MFCS 2024, Conjecture 6) state the Krenn–Gu
conjecture as: **if a graph has more than four vertices, its matching index
is at most 2**, with complex weights and bichromatic half-edge colourings
allowed.  Equivalently, for every even `n >= 6` and every `d >= 3` there is
no witness.  The two conditions are conjoined, not alternatives.

Working at `d = 3` loses nothing: restricting every block to three colours
turns any `d >= 4` witness into a `d = 3` witness, because the amplitude of a
word in the restricted alphabet uses only the restricted entries.  The
`n = 4` case is closed the other way (matching index at most 3, and the
problem page records that `d >= 4` is impossible at `n = 4`).  Every
repository result is therefore stated for `d = 3`, and a `d = 3` theorem at
all even `n >= 6` is the full conjecture.

## What changed since the last brief

The [GHZ closure theorem](../../claims/arbitrary-order/GHZ_CLOSURE_MATCHING_POLYTOPE_FACE_ASYMPTOTIC_REALIZABILITY_THEOREM.md)
(frontier node `BR1`) proves that for every even `n >= 4` the ternary GHZ
tensor is a Euclidean limit of matching tensors: monochromatic matrix units
`eps^(nu(e))` on a cubic three-edge-coloured graph whose colour classes form
a face of the perfect-matching polytope.  Three consequences reorganize the
work.

1. **Every proof must be fibre-exact.**  No polynomial identity of the
   hafnian image, no flattening, slice, or border-rank bound, and no other
   condition closed under limits of `T_W` alone can separate the target.  A
   valid argument derives structure of `W` from the exact equation
   `T_W = Delta`, as the killer, anchor, Laplace, and Wick identities do.
   Sensor-rank and flattening arguments are legitimate only as consequences
   of exact identities in `W`.
2. **Unconstrained numerics are blind.**  The infimum of every continuous
   loss is zero at every even `n`, attained along unbounded weights.  A
   search report must fix a vertex gauge and bound the weights, or it says
   nothing.  The repository's exploratory optimizer must be read this way.
3. **The limit families are exactly Bogdanov structures.**  Every limiting
   family is all-diagonal (monochromatic edges), cubic, with three
   monochromatic perfect matchings and extra matchings suppressed, not
   cancelled.  An exact witness must achieve with cancellation what these
   families achieve only in the limit.  The all-diagonal case is therefore
   the border-critical core of the problem.

## Non-negotiable rules for this run

- No route whose only input is the tensor `T_W`.  If a task's conclusion
  would survive replacing the fibre by its closure, stop.
- No numerical claim without a stated gauge normalization and bound; report
  bounded-gauge infima only, and never call a cost tending to zero evidence.
- No new local chart, factor, divisor, or support-profile sibling unless the
  spine owner has shown it is a necessary child in an exhaustive cover of one
  of the parents below.  The H4/Q6 lane is parked.
- Every result states its `d = 3` scope and whether it is fibre-exact.
- The 2026-08-31 packaging rules stand: one integrator, exact verification and
  independent review as gates, no one-PR-per-worker theorem surfaces.

## Parent A (primary): weighted Bogdanov — exclude all-diagonal witnesses

**Proposition.**  Let `n >= 6` be even and let `Z^0, Z^1, Z^2` be hollow
symmetric complex `n x n` matrices.  It is impossible that

```text
haf(Z^c[V]) = 1                                for c = 0,1,2, and
haf(Z^0[V_0]) haf(Z^1[V_1]) haf(Z^2[V_2]) = 0   for every ordered partition
                                              V = V_0 + V_1 + V_2 into even
                                              parts not all in one class,
```

with `haf(Z^c[empty]) = 1`.  Equivalently, as a polynomial identity in vertex
variables `t_v, s_v`,

```text
haf( Z^0_ij t_i t_j + Z^1_ij s_i s_j + Z^2_ij ) = prod_v t_v + prod_v s_v + 1
```

has no solution.  This is the Krenn–Gu conjecture restricted to blocks that
are diagonal, i.e. to monochromatic edges with arbitrary complex weights.

**Why this parent, and its honest scope.**  It is where all `BR1` limit
families live, so it is the sharpest place where exactness must bite.  It
generalizes Bogdanov's theorem (positive weights) to complex weights and
would be publishable on its own.  Its formal downstream consequence is thin:
a proof shows only that every witness has at least one bichromatic entry.
Its value is mechanistic, namely whatever exact invariant of hafnian
cancellation defeats the all-diagonal case is the first candidate for the
general fibre.  Until a bridge from "some bichromatic block exists" into an
accepted global consumer is proved, Parent A is a **scoped branch sprint**,
not a resolution-first parent in the sense of the 2026-08-31 brief.

**Relation to the all-bridge lane (correction).**  An earlier draft called
this parent "exactly" the simultaneous balanced all-bridge branch.  That is
wrong.  The all-bridge normal form (`A1`--`A3`) has three off-diagonal
singleton killers per vertex with normal types `f(c) != c`; the all-diagonal
case has no bichromatic entry at all and lies outside that normal form.  What
transfers is exactly what depends only on the inherited identities
`haf(Z^c[V]) = 1` and `haf(Z^c[A]) haf(Z^d[V-A]) = 0`, which hold verbatim in
the all-diagonal case because every mixed word factorizes:

- active-deck exclusivity (Laplace plus the two-part identity) transfers;
- the cubic saturated-diagonal exclusion transfers and simplifies, since the
  Bogdanov rainbow word is then a single nonzero monomial with no zero-layer
  potential needed;
- the degree-four exclusion, the resulting `Delta(D) >= 5`, and the
  all-degree trichotomy with bipartite least core do **not** transfer
  verbatim: their proofs use the normal-type bit flips (every saturated
  colour-`c` edge flips the two other bits) to make active cycles even and to
  place Hamiltonian-chord endpoints in opposite classes.  Recovering an
  evenness statement for active colour-`c` cycles in the all-diagonal case is
  the first concrete lemma this sprint should settle or refute.

**Upstream.**
[`UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM`](../../claims/arbitrary-order/UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md),
[`ALL_BRIDGE_ACTIVE_DECK_EXCLUSIVITY_AND_CUBIC_DIAGONAL_EXCLUSION`](../../claims/arbitrary-order/ALL_BRIDGE_ACTIVE_DECK_EXCLUSIVITY_AND_CUBIC_DIAGONAL_EXCLUSION.md),
[`ALL_BRIDGE_ACTIVE_DECK_MAXIMUM_DEGREE_FOUR_EXCLUSION`](../../claims/arbitrary-order/ALL_BRIDGE_ACTIVE_DECK_MAXIMUM_DEGREE_FOUR_EXCLUSION.md),
[`ALL_BRIDGE_ACTIVE_DECK_ALL_DEGREE_LOCALIZED_PURE_CANCELLATION_AND_BIPARTITE_CORE_REDUCTION_THEOREM`](../../claims/arbitrary-order/ALL_BRIDGE_ACTIVE_DECK_ALL_DEGREE_LOCALIZED_PURE_CANCELLATION_AND_BIPARTITE_CORE_REDUCTION_THEOREM.md).

**Mechanisms worth a serious attempt.**

- *Support families.*  Let `S_c` be the family of even sets `A` with
  `haf(Z^c[A]) != 0`.  Laplace expansion makes `S_c` downward accessible from
  `V` by removing colour-`c` edges, and its complement family `S_d^*` upward
  accessible from the empty set.  The two-part condition says
  `S_c` meets `S_d^*` only in the empty set and `V`; the three-part condition
  forbids rainbow partitions.  Find the combinatorial contradiction between
  two oppositely accessible families and the three-part condition, using
  cancellation only through exact Laplace identities.
- *The polynomial identity.*  Specialize `t_Z = 0` on vertex sets `Z`, take
  derivatives at `t = s = 1`, and compare Hessians; every specialization
  gives exact linear relations among pair- and quadruple-deletion cofactors.
- *Induction through an active edge.*  An edge with nonzero colour-`c` weight
  and nonzero colour-`c` cofactor has zero weights and cofactors in the other
  colours.  Determine exactly which conditions descend to `V` minus that
  edge, and whether a minimal counterexample can have one.
- *Adversarial.*  Search for exact all-diagonal witnesses at `n = 8, 10` on
  structured supports with the vertex gauge fixed, using exact algebra over
  `Q` rather than floating point.  An exact witness here refutes the whole
  conjecture and must be escalated to the counterexample audit.

**Success.**  A proof; or an exact all-diagonal witness; or an exact no-go
that eliminates one of the mechanisms above across the whole parent and
leaves one strictly sharper lemma.

**Progress (later on 2026-09-01).**  The even-cycle lemma is settled:
[`WB1`](../../claims/arbitrary-order/ALL_DIAGONAL_WEIGHTED_BOGDANOV_MAXIMUM_DEGREE_FOUR_EXCLUSION_THEOREM.md)
proves that in the all-diagonal branch active colour-`c` cycles are
components of `supp(Z^c)`, hence even, and that no all-diagonal witness has
`Delta(D) <= 4`.  The proof needs no bit flips and no Hamiltonian-chord
argument.  The sprint's first open lemma is now **all-diagonal degree five**:
exclude, or localize to a supported pure cancellation, every all-diagonal
witness with `Delta(D) = 5`, where an active graph may have a degree-three
vertex and a cycle vertex may carry a residual edge.

**Progress (later still on 2026-09-01).**  Support-level SAT triage
([`WB2`](../../claims/arbitrary-order/ALL_DIAGONAL_SUPPORT_LEVEL_WEIGHTED_BOGDANOV_FINITE_EXCLUSION_THEOREM.md))
shows the all-diagonal branch is excluded at `n = 6` and `n = 8` for every
degree using only Laplace accessibility, single-matching forcing, and
rainbow-freeness, with no weight values.  Degree five is therefore subsumed.
The sprint's target is now the **support-level weighted Bogdanov
conjecture**: the abstraction (AP') has no model at any even `n >= 6`.  It is
purely combinatorial.  Adversarial work should look for a model of (AP') at
`n = 10` or `n = 12` (a model is not a witness; it would locate exactly where
weights must be consulted), and constructive work should turn the `n = 8`
unsatisfiability into a human argument using the third colour.

## Parent B (finite milestone): complete the eight-vertex exclusion

Extend the six-vertex certificate chain to all of `n = 8`, `d = 3`, hence to
all `d >= 3` at `n = 8`.  Excluded so far: every 4-regular skeleton, every
essential skeleton with a degree-four vertex and at most 17 edges, and
several dense singleton families.  Open: denser skeletons with a degree-four
vertex, minimum-degree-five skeletons, and dense supports with many
bichromatic entries.  The `BR1` families at `n = 8` (truncated prism, 12
edges) lie inside the excluded region, so the remaining work is exactly the
region where cancellation, not suppression, must be excluded.

This is not a mere engineering exercise: the excluded region is where
suppression suffices, and the open dense region with many bichromatic entries
may need exact-cancellation tooling beyond the current support/Laurent chain.

**Success.**  A fail-closed, independently replayed certificate chain and a
finite theorem document with the same status discipline as
[`SIX_VERTEX_CERTIFICATE`](../../claims/finite/n06/SIX_VERTEX_CERTIFICATE.md).
This would make the conjecture a theorem for `n` in `{6, 8}` and supply the
exact-cancellation patterns a general proof must defeat.

## Parent C (structural, after A): non-coordinate killer exclusion

For every vertex `v` and colour `c` a witness has a column-killer block
`W_(v,u) = w e_c^T`.  At degree three every killer is a monochromatic matrix
unit; at degree four at least one is.  **Proposition to decide:** in every
witness, every killer block is a monochromatic matrix unit, i.e. `w` is
proportional to `e_c`.  If true, every vertex carries three monochromatic
singleton edges of distinct colours, and the constant words inherit Bogdanov
structure that Parent A then attacks with the remaining blocks as the only
source of cancellation.  If false, the adversarial team must exhibit an exact
non-coordinate local model that survives all equations at `n = 8`, which
would sharpen the deeper-blocker branch into a precise obligation.

## Remarks for physics-facing write-ups

`BR1` also answers the asymptotic version of Question 3 of Krenn, Gu, and
Soltész for `d = 3`: the monochromatic fidelity can be made arbitrarily close
to one at every even `n` with monochromatic edges only, although the exact
value one is conjectured unreachable.  Any such write-up must keep the
closure/image distinction explicit and cite the six-vertex exclusion for the
only unconditional unbounded-weight statement.

## What does not count

Everything listed in the 2026-08-31 brief, plus: any argument whose
hypotheses are satisfied by the `BR1` limit families in the limit; any
numerical report without gauge normalization; any new `d >= 4` statement not
reduced to `d = 3`; and any frontier, visualizer, ledger, or field-note pass
that is not required by a merged mathematical delta.

## Copy/paste launch prompt

> Run a fibre-exact Krenn–Gu ecology from fresh `origin/main`.  Read
> `AGENTS.md`, `docs/current-frontier.md` (node `BR1` first), and this dated
> brief.  Protect every active worktree and process.  The single primary
> target is weighted Bogdanov, run as a scoped branch sprint unless and until
> a bridge into an accepted global consumer is proved: exclude all-diagonal
> complex witnesses at every even `n >= 6`, stated as the polynomial identity
> `haf(Z^0 t t^T + Z^1 s s^T + Z^2) = prod t + prod s + 1`.  Assign workers by
> method: support-family combinatorics, exact polynomial-identity
> specializations, active-edge induction, and exact adversarial search with a
> fixed vertex gauge.  A second team may pursue the complete eight-vertex
> exclusion as a finite milestone.  No tensor-level invariant routes, no
> unbounded numerical claims, no new H4/Q6 or other chart siblings, and one
> integrator for publication.  Success is a proved parent, an exact witness
> escalated to audit, an exact mechanism no-go with one sharper lemma, or a
> complete finite chain.  Preserve the global `UNRESOLVED` status unless the
> dedicated resolution gate is actually met.
