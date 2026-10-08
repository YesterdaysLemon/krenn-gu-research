# Trunk-level attempt record — 2026-10-08

This is a dated research record, not a theorem, frontier entry, or change of
status.  The global Krenn–Gu conjecture remains **UNRESOLVED**.

## Target

A move on the trunk of the proof map rather than inside a branch: either a
reduction that drives an arbitrary witness into a normal form the repository
already excludes, or a quantitative mechanism valid at every order.  Scope:
`d = 3`, arbitrary `3 x 3` blocks, every even `n >= 6`.

## Candidates examined and where they already live

Each first-order mechanism below was derived independently during this
attempt and then found in the repository.  None is new; the pointers are
recorded so the next attempt starts past them.

| mechanism | statement | already in |
|---|---|---|
| diagonal-torus degeneration / polystability | a witness degenerates along any one-parameter subgroup of the GHZ stabilizer with nonnegative exponents to a witness of smaller support, so a support-minimal witness has a strictly positive endpoint-balanced weighting | matrix-unit form in `MATRIX_UNIT_GHZ_DIAGONAL_TORUS_POLYSTABILITY_ENDPOINT_BALANCE_AND_ACTIVE_TRANSPORT_SHARPNESS_THEOREM.md`; the general-block form is the same argument with entries in place of edges and has the same thin downstream (balance does not exclude active transport) |
| moment-balanced gauge (Kempf–Ness) | a polystable witness has a representative with colour-wise constant squared row norms at every vertex | `MATRIX_UNIT_GHZ_MOMENT_BALANCED_GAUGE_AND_UNIT_PHASE_ACTIVE_TRANSPORT_SHARPNESS_THEOREM.md` |
| vertex-variable polynomial identity | `T_W = Delta` is equivalent to `haf([x^(i)T W_ij x^(j)]) = sum_c prod_i x^(i)_c` for all `x^(i) in C^3`; the all-diagonal specialization is the `t, s` identity of the fibre-exact brief | `docs/strategy/fibre-exact-targets-2026-09-01.md` (Parent A) and the double-star annihilation lemma |
| two-open matrix identity | for any pair `p, q` and any word `b` on `V - {p,q}`: `T_{W'}(b) W_pq + sum_{i != j} tau_ij(b) r_i(b_i)^T s_j(b_j) = [b constant c] E_cc`, with `r_i`, `s_j` the rows of the blocks at `p`, `q`; a regrouping of the fibre equation | the two-open and Hamming-one machinery (`BALANCED_TWO_OPEN_*`, `EIGHT_VERTEX_ADJACENT_CUT_MONOMIAL_HAMMING_ONE_*`) |
| pinned-row anchors | contracting a vertex with `e_a` instead of a generic vector gives, for every `(v, a)`, a neighbour whose row `a` is a nonzero multiple of `e_a^T` | the diagonal-anchor theorem cited by the GHZ closure document |
| non-coordinate killer exclusion (Parent C) | every column-killer block `w e_c^T` has `w` proportional to `e_c` | open in the fibre-exact brief; no mechanism found here; see Section 3 for the support-level test |

## The one experiment: a general-block recursive support model

`claims/finite/n08/explore_general_block_recursive_support_model.py` encodes,
for arbitrary blocks, the zero pattern of every sub-configuration's word
coefficients `T_{W[A]}(w)`, with the two exact Laplace consequences used by
the all-diagonal RZP model — accessibility (L) and singleton noncancellation
(F') — and the full GHZ zero pattern (G); optionally the column-killer
theorem.  It uses the constant-word chain normalization (sound by
relabelling) and lex-leader symmetry breaking, and an independent brute-force
checker re-verifies any SAT model.

| order | hypotheses | result | note |
|---|---|---|---|
| 4 | (L), (F'), (G) | SAT | correct: witnesses exist at `n = 4`; checker PASS |
| 6 | (L), (F'), (G) | SAT, 0.2 s | a full 135-entry support satisfies every condition |
| 6 | + killers | SAT, 4.5 s | **minimum 27 nonzero entries** (26 is UNSAT); the model is displayed below |
| 6 | + killers + a non-coordinate killer | SAT, 4.3 s | Parent C is not decidable at the support level at `n = 6` |
| 8 | (L), (F'), (G) | SAT, 5.6 s | 1,081,148 variables, 4,399,552 clauses |
| 8 | + killers | SAT, 27 s | |

The 27-entry six-vertex model (blocks `ij` with the nonzero entries `ab`,
`a` the colour at `i`, `b` the colour at `j`):

```text
01: 00 20    02: 11    03: 00 20    04: 02 22    05: 00 02 20 22
12: 00 02    13: 22    14: 11       15: 20       23: 00 20
24: 02 22    25: 00 02 20 22        34: 20       35: 11       45: 00
```

**What this says.**  The six-vertex exclusion, which is a theorem, cannot be
reached by zero-pattern reasoning of this kind: Laplace accessibility,
singleton noncancellation, the complete GHZ zero pattern, and the killer
theorem are all satisfied by a 27-entry pattern on six vertices.  Every
proof, at six vertices or at every order, must use quantitative cancellation
among at least two supported terms.  This matches what the repository's
eight-vertex programme already does: its recursive full-target model
(`tools/explore/discover_recursive_row_space.py`, see
`docs/strategy/source-cancellation-mechanisms-2026-09-13.md`) is the same
abstraction and is refuted support by support with transported binomial
("row-space") relations, which are weight-level consequences.  The
experiment here is therefore a rediscovery with one new exact exhibit, the
minimum-entry six-vertex pattern, and one new support-level fact about
Parent C.

## Outcome and the sharper statement

No trunk-level theorem.  No countermodel.  The attempt's honest product is a
negative result about mechanisms: **no Boolean (support-level) abstraction of
the fibre equation with only single-term consequences can exclude any order,
not even six.**  The quantitative input that the six-vertex certificate and
the eight-vertex row-space refutations use is a *relation between the
values* of at least two supported terms.  The next load-bearing trunk lemma
is therefore the one the `P25` boundary already names: a weighted
source-isolation consequence valid at every order, that is, a family of
binomial or row-space relations that follow from `T_W = Delta` for every `n`
and refute the support patterns that survive (L), (F'), (G) and the killers.
Until such a family exists, finite orders can only be closed one support
pattern at a time.

Proof-distance delta: none.  The record is kept because it maps the
first-order mechanisms to their existing owners and fixes the minimum
quantitative content a trunk proof must have.
