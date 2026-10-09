# Adversarial review: AP' arc-lemma attempt (Theorems A, B, D, Lemma C, Corollary B1, AL1)

Date: 2026-10-08

Reviewed package (branch `origin/claude/arc-lemma-20261008`, commit
`14a9a0ad`):

- `docs/strategy/arc-lemma-attempt-2026-10-08.md` (the "note")
- `claims/arbitrary-order/verify_all_diagonal_support_level_ap_prime_arc_lemma_hole_model_and_closure.py`
  (the verifier)
- `claims/arbitrary-order/explore_all_diagonal_support_level_ap_prime_arc_lemma_relaxations.py`
  (exploratory solver script; read, and cheap rows rerun)

Context consulted on `main`:
`claims/arbitrary-order/ALL_DIAGONAL_SUPPORT_LEVEL_AP_PRIME_TOP_MATCHING_EXTRA_EDGE_LEMMA.md`
(Proposition 1, Lemma 2, Proposition 3, Lemma 5, the arc-lemma statement),
WB2 (`ALL_DIAGONAL_SUPPORT_LEVEL_WEIGHTED_BOGDANOV_FINITE_EXCLUSION_THEOREM.md`)
for the AP' axioms (a), (L), (S), (F), (H1) `V ∈ S_c`, (H2), and the WB4
review (`ALL_DIAGONAL_SUPPORT_LEVEL_AP_PRIME_BRANCHING_LEMMA_REVIEW_2026-10-08.md`,
§3) for the earlier self-contained proof of the uniform special case.

The reviewed documents were not edited.  This review changes no status; the
arc lemma, (PM), the extra-edge sub-lemma, and the all-diagonal branch stay
open, and the global Krenn–Gu conjecture remains **UNRESOLVED**.

## Independence disclosure

This is a **same-day review by one automated agent** (Claude), commissioned by
the coordinating agent of the run that produced the note.  The reviewer did
not write the note or its scripts, but it is not an external referee, it ran
on the same host with the same toolchain (Python 3.13, `python-sat`
CaDiCaL 1.5.3), and it has not itself been reviewed.  Its solver reruns are
uncertified; no DRAT trace was produced or checked.  Its brute-force
cross-checks are scratch scripts (not committed; described in §9) written
independently of the verifier, but by an agent of the same model family.

## Verdict

**The hand-proved content passes.  No mathematical error was found in
Theorem A, Lemma C, Theorem B, Corollary B1, or Theorem D.  The gaps are
statement-exactness and scope-wording defects, chiefly in the stall lemma AL1
and in the "no forcing" readings of the solver ladder (§6, §7).**

| item | verdict |
|---|---|
| (1) Theorem B + Lemma C | **PASS.**  Parity bookkeeping, the `n ≡ 0 (mod 4)` case, and the single-arc claim are correct.  Minor: the "uses only" list omits `∅ ∈ S_c` (needed when the `N`-tiled gap is empty). |
| (2) Corollary B1 | **PASS.**  Re-derived independently below; every axiom used is an AP' axiom.  It gives an elementary proof of the uniform (CGI special) case at every order, which makes one sentence of the extra-edge document stale (G8). |
| (3) Theorem A (hole model) | **PASS.**  Every colour-1 axiom, (i), `G_1 ∩ M_0 = ∅`, and the arc failure verified by hand; brute force reproduced at `n = 6, 14` by the reviewer.  Minor: the text uses `{0,1} ∈ M_0` without saying so. |
| (4) Theorem D | **PASS.**  A model of every AP' axiom except colour-1 (F), including full (H2); brute force reproduced at `n = 8, 12, 16` by an independent (H2) method. |
| (5) verifier | **PASS** (1.8 s, `"result": "PASS"`).  It checks what the note says it checks, with one tautological sub-check (the `n ≡ 2 (mod 4)` emptiness in Part B).  It does not check Theorem B or B1, and the note does not claim it does. |
| (6) solver ladder / AL1 | Ladder **correctly labelled** exploratory and uncertified; cheap rows reproduce.  **AL1 is not stated exactly (GAP):** it omits the colour-0 hypothesis `S_0 ⊇ {M_0-unions}` on which both its solver evidence and "AL1 + Theorem B ⇒ (PM)" rely.  "No forcing at all" readings overstate scope (colour-0 forcing is built in).  New reviewer run: at `n = 12` every model of AL1's hypotheses has `G_1` a perfect matching, so AL1's non-vacuity is only the trivial case (at `n = 8` likewise; `n = 10` vacuous). |
| (7) gaps | Listed in §8 (G1–G11).  None invalidates a proved statement. |

No counterexample, no AP' model, and no exact countermodel to any proved
statement was found.

## 1. Item (1): Lemma C and Theorem B

**Lemma C.**  In cycle coordinates (`M_0 = {2i, 2i+1}`, `N = {2i+1, 2i+2}`),
`F` an equal-parity perfect matching, `ℓ(v) = F(v) − v mod n ∈ {2, ..., n−2}`
(even, nonzero because `F(v) ≠ v` has the parity of `v`).  Measured clockwise
from an even `x`, the four points are at `0, 1, ℓ(x), 1 + ℓ(x+1)`, all
distinct (parities `E, O, E, O`).  The chord `x F(x)` separates `x+1`
(position 1, always inside `(0, ℓ(x))`) from `F(x+1)` iff
`1 + ℓ(x+1) > ℓ(x)`, i.e. (both even) `ℓ(x+1) >= ℓ(x)`; non-crossing iff
`ℓ(x+1) <= ℓ(x) − 2`.  Correct.

The counting: `F` maps `X` to `X` and `Y` to `Y`; `ℓ(v) + ℓ(F(v)) = n`; `X`
splits into `n/4` `F`-pairs (here `n ≡ 0 (mod 4)` is used: `|X| = n/2` even),
so `Σ_X ℓ = Σ_Y ℓ = n²/4`.  Non-crossing at all `n/2` even `x` would give
`Σ_Y ℓ <= Σ_X ℓ − n`.  Contradiction.  Correct.

Gaps for a crossing `x`: `0`; `ℓ(x) − 2` starting at `x + 2` (even);
`ℓ(x+1) − ℓ(x)` starting at `F(x) + 1` (odd, since `F(x)` is even);
`n − 2 − ℓ(x+1)` starting at `F(x+1) + 1` (even).  All even; an even run is
`M_0`-tiled iff it starts at an even vertex, so exactly the third gap can be
`N`-tiled.  So `V − A = U ⊔ Q` with `U` an `M_0`-union and `Q` one
`N`-ended arc **or empty** (empty when `ℓ(x+1) = ℓ(x)`).  **Only one arc is
needed**: this is what the refinement "crossing at an `M_0`-edge" buys over
an arbitrary crossing (which can leave two `N`-tiled gaps, and a union of two
arcs is not an arc).  For `n ≡ 2 (mod 4)` the class `X` has odd size `n/2`
and no equal-parity perfect matching exists.  **PASS.**

**Theorem B, Step 1.**  For `ij ∈ G_d`, `i` even, `j` odd: `ij ∉ M_0` by
Proposition 1(ii); the run after `i` has length `j − i − 1 mod n`, even, starts
at the odd vertex `i+1`, hence is `N`-tiled and nonempty (it is empty only if
`j = i+1`, an `M_0`-edge); the run after `j` has even length
`n − 1 − (j − i) mod n` and starts at the even vertex `j+1`, hence is an
`M_0`-union (possibly empty, when `ij ∈ N`).  The partition
`(U, Q, {i, j})` has `{i, j}` and its complement nonempty.  Correct.

**Steps 2–4.**  `F` exists by (S) at `V` (H1).  `n ≡ 2 (mod 4)` ends here,
with no forcing used, which matches Lemma 5 of the extra-edge document.  For
`n ≡ 0 (mod 4)` (so `n >= 8`), Lemma C gives `A = {x, x+1, x*, y*}`; after
Step 1 every `G_d`-edge inside `A` joins equal-parity vertices, and the only
equal-parity pairs in `A` are `x x*` and `(x+1) y*`, both in `F ⊆ G_d`, so
`G_d[A]` has exactly one perfect matching and four-set forcing gives
`A ∈ S_d`.  The partition `(U, Q, A)` has `A` and `V − A` nonempty.  All
classes are even.  **PASS.**

Bookkeeping remark (G1): the hypothesis list "for colour `c`, the arcs" omits
`∅ ∈ S_c`, used when `Q = ∅` in Step 4 and inside Proposition 1(ii).  It is
axiom (a) in AP', so nothing changes for AP'; it matters only when Theorem B
is applied to relaxed systems.  The proof also never uses `N ⊆ G_c`, so
Theorem B holds as stated with that hypothesis dropped.

The reviewer's independent check R1 (§9) tests the *conclusion* of Steps 1
and 3–4 directly, without the run-parity reasoning: for every non-`M_0`
opposite-parity pair at `n = 6, ..., 16`, and for every equal-parity perfect
matching at `n = 8, 12, 16` (9, 225, 11,025 of them), it finds an explicit
split `V − A = U ⊔ Q` by enumerating `Q` over the arc list.  No failure.

## 2. Item (2): Corollary B1, derived independently

Let an AP' model on `n >= 6` vertices have two colours with perfect-matching
support graphs.  The AP' axioms are invariant under permuting colours ((H2)
quantifies over all ordered partitions), so relabel them `G_0 = M_0`,
`G_2 = N`.

1. `S_0 = {M_0-unions}` and `S_2 ⊇ {N-unions}`: an `M_0`-union (resp.
   `N`-union) is uniquely matchable in `G_0` (resp. `G_2`); (F) for colours 0
   and 2.
2. `N ∩ M_0 = ∅`: Proposition 1(ii), which uses (a) for colour 2 (edges are
   members), `∅ ∈ S_1` ((a) for colour 1), and (H2).
3. `M_0 ∪ N` is 2-regular with alternating even cycles.  A proper component
   `K` gives the partition `(K, ∅, V − K)`, with `K ∈ S_0`, `∅ ∈ S_1`,
   `V − K ∈ S_2`, two nonempty classes: (H2) fails.  So `C = M_0 ∪ N` is a
   Hamiltonian cycle.
4. Every `N`-ended arc of `C` is an `N`-union, hence in `S_2`.  So the arc
   lemma holds for colour 2 (with `N ⊆ G_2`).
5. Theorem B with `c = 2`, `d = 1` needs: `S_0 ⊇ {M_0-unions}` (step 1),
   the arcs and `∅` in `S_2` (step 4, (a)), and for colour 1: (a), a perfect
   matching of `G_1` ((S) at `V`, (H1)), (F) on four-sets.  All are AP'
   axioms.  (H2) fails: contradiction.

Every axiom used is an AP' axiom; the colour-0 axioms used are (a), (S), (F),
(H1) (through Proposition 1).  **PASS.**

*Consequence the note understates (G8).*  Specialised to uniform models
(all three `G_c` perfect matchings), B1 is an elementary proof that a simple
cubic graph on `n >= 6` vertices with a proper 3-edge-colouring has a perfect
matching other than its colour classes, i.e. the special case of the
Chandran–Gajjala–Illickan/Bogdanov statement used by WB1 and WB4.  It is a
second self-contained proof (the first is in §3 of the WB4 review; the two
differ only in how the crossing is found).  The extra-edge document's
sentence that the `n ≡ 0 (mod 4)` uniform configurations are "the hard core
of the CGI theorem, which this document does not reprove" is now stale, and
its Proposition 3 remark ("any hand proof of the sub-lemma must contain a
proof of that theorem or import it") is satisfied by B1 rather than being an
obstacle.  The reviewer's check R2 confirms the specialisation exhaustively
for `C = 0-1-...-(n-1)` and every compatible `M_1` at `n = 6, 8, 10, 12`
(4, 31, 293, 3,326 choices; every resulting cubic graph has at least four
perfect matchings).  The reduction of the extra-edge sub-lemma to "exactly
one perfect-matching colour" is correct.

## 3. Item (3): Theorem A (hole model)

Fix the `M_0`-edge `{0, 1}` (the note uses this implicitly; G2).
`G_1 = K_n − M_0`; `S_1 = {∅, V} ∪ {even A, |A| >= 2, not an M_0-union, not a
hole set {0, 1, x, y}, xy ∉ M_0}`.

- (a): `∅, V ∈ S_1`; the two-element members are the non-`M_0` pairs, which
  are exactly `G_1` (hole sets have size 4).  Correct.
- (H1): `V ∈ S_1` by definition.
- (S): `G_1[A]` is `K_A` minus a matching; it has a perfect matching for even
  `|A| >= 2` when `A` is not an `M_0`-pair.  Correct.
- (F): `K_k` minus a matching has at least two perfect matchings for even
  `k >= 4` (`k = 4`: the three perfect matchings of `K_4` are edge-disjoint and
  a removed matching of `K_4` is contained in at most one of them; `k >= 6`:
  `v` has `>= k − 2` neighbours, each leaving `K_{k−2}` minus a matching, which
  has a perfect matching).  So the uniquely matchable sets are `∅` and the
  `G_1`-edges, all in `S_1`.  Correct.
- (i) and `G_1 ∩ M_0 = ∅`: by construction.
- (L): "at most one `u ≠ v'` makes `A − {v, u}` an `M_0`-union" — if both
  `A − {v,u}` and `A − {v,w}` are, then `u ∈ A − {v,w}` gives `u' ∈ A − {v,w}`,
  while `u ∉ A − {v,u}` gives `u' ∈ {v, u} ∪ (V − A)`; so `u' = v`, excluded.
  Correct.  The case split by `|A|` was checked line by line: `|A| = 4` with
  a pair `{p, p'}` cannot have `{p, p'} = {0, 1}` (then `A` would be a hole
  set, since its two singletons are not `M_0`-partners); both prescribed
  moves (`v = p`, `u = x` and `v = x`, `u = p`) leave the non-`M_0` pair
  `{p', y}`.  `|A| = 6` with `{0,1} ⊆ A`, `v ∉ {0,1}`: `u = 0` is a
  `G_1`-neighbour of `v` and `A − {v, 0}` contains `1` but not `0`.
  `|A| >= 8`: at least six candidates, at most one bad.  For `A = V`,
  `V − {v, u}` is an `M_0`-union only if `u = v'`.  Correct.
- Arc failure: the path `N(0), 0, 1, N(1)` is an `N`-ended arc; its four
  vertices are distinct (`N ∩ M_0 = ∅`); `N(0) N(1) ∈ M_0` would close a
  4-cycle inside the Hamiltonian cycle, impossible for `n >= 6`.  So it is a
  hole set and not in `S_1`.  Correct.

The verifier output shows exactly one missing arc per Hamiltonian cycle
(8, 48, 384, 3,840 cycles and incidences at `n = 6, 8, 10, 12`), consistent
with "exactly the four-arc through `01`".  The reviewer's independent
implementation R4 reproduces the axioms and the arc failure at `n = 6` and
`n = 14` (46,080 Hamiltonian cycles).  **PASS.**

The interpretation is also right: since (R) is antitone in `S_1`, `S_2`, it
can never assert membership, and with `S_2` absent the only surviving
instances of (R) are (i).  So any proof of the arc lemma must use colour 2
through (R) jointly with (L) or (F), as the Remark says.

## 4. Item (4): Theorem D

Cycle coordinates, `n ≡ 0 (mod 4)`, `n >= 8`.  Colours 0 and 2 are the
unions of the perfect matchings `M_0` and `N`, so they satisfy (a), (L), (S),
(F), (H1).  Colour 1:

- (a): a 2-set has both parity counts even iff it is an equal-parity pair, and
  such a pair is never alternating.  Correct.
- (S), (H1): `G_1[A]` is the disjoint union of cliques on `A ∩ X`, `A ∩ Y`,
  both even; `|X| = |Y| = n/2` is even.  Correct.
- (L): the child `A − {v, u}` has counts `(a − 2, b)`; alternating sets have
  equal counts; in the critical case `a − 2 = b >= 2`, the `b + 1` points of
  `A ∩ X − {v}` sit in the `b` gaps of `A ∩ Y`; if some gap holds exactly one
  point, removing it empties a gap; if none does, after removing any `u` some
  other gap still holds `0` or `>= 2` points (there are `b >= 2` gaps).  The
  case `a − 2 = b = 0` gives `∅`.  Correct.
- (H2): for proper nonempty `A_1`, every edge of the matching
  `M_0|A_0 ∪ N|A_2` joins two cyclically consecutive vertices of `V − A_1`,
  so each gap of `A_1` is even and `A_1` is alternating, hence not in `S_1`.
  `A_1 = ∅`: the even cycle `C` has exactly two perfect matchings, `M_0` and
  `N`, so no partition uses both.  `A_1 = V`: one class.  Correct.
- (F) fails in colour 1: `{0, 1, 2, 3}` is alternating and `G_1[{0,1,2,3}]`
  has the unique perfect matching `{02, 13}`.

So Theorem D is a model of every AP' axiom except colour-1 (F); colours 0
and 2 have perfect-matching support graphs; colour 2 satisfies the arc
lemma; and Theorem B (with `c = 2`, `d = 1`) fails in it only through the
missing four-set forcing.  The necessity claim for the forcing hypothesis of
Theorem B and B1 at every `n ≡ 0 (mod 4)` is therefore correct (even full
colour-1 (L) cannot replace it).  The reviewer's check R3 reproduces (a),
(S), (L), and (H2) at `n = 8, 12, 16` by a different (H2) method (for every
`A_1 ∈ S_1`, test whether `C[V − A_1]` has a perfect matching), with
mutation testing (admitting alternating sets produces (H2) violations).
**PASS.**

## 5. Item (5): the verifier

Run on this branch: `"result": "PASS"` in 1.8 s.  Reading of its parts:

- **Part A** builds the hole family exactly as defined (the `len(A) == 4`
  branch excludes `{0,1,x,y}` with `xy ∉ M_0`; `xy ∈ M_0` is already an
  `M_0`-union) and checks (a), (S), (F), (L), (i), and the missing arc on every
  Hamiltonian cycle `M_0 ∪ N` (enumerated once each, `(n/2 − 1)!·2^{n/2−1}`
  orders).  The `N`-ended arcs are generated from odd positions with even
  length `< n`, which is the right family.  Faithful.
- **Part B** checks, for every equal-parity perfect matching at even
  `n <= 16`, the length identity, the crossing criterion
  `cross ⇔ ℓ(x+1) >= ℓ(x)`, the existence of an `M_0`-adjacent crossing, and
  the run decomposition.  **The `n ≡ 2 (mod 4)` check is tautological**: the
  generator `same_parity_pms` returns nothing by construction when `|X|` is
  odd, so `"same_parity_perfect_matchings": 0` is not evidence (the fact is a
  one-line parity argument anyway).  G7.
- **Part C** checks every axiom of all three colours and (H2) over all
  ordered even partitions (1,638 at `n = 8`, 132,858 at `n = 12`), and that
  colour-1 (F) fails (20 and 105 sets).  Faithful.
- Not covered by the verifier: Theorem B and Corollary B1 themselves (only
  Lemma C's combinatorics).  The note's table says "finite cross-check of
  Lemma C" for that row, which is accurate.  The reviewer's R1 and R2 fill
  this at small orders.

The verifier is a finite cross-check, as the note says; the proofs are the
evidence for all orders.  **PASS.**

## 6. Item (6): the solver ladder and the stall lemma AL1

**Labelling.**  Section 6 is headed "exploratory; not proof", the summary
table says "exploratory, uncertified, one order each", the Boundary repeats
it, the script is named `explore_...` and says "Research tool, not a
verifier", the `n = 12` (PM) consequence is called "computer-assisted,
uncertified" and "not promoted", and stopped runs are marked "not evidence".
**Correctly labelled.**  Two qualifications: the script's SAT re-check is
called "independent" but is an internal brute-force re-check in the same file
by the same author (not independent in the sense of AGENTS.md §5), and it does
not re-check the `--force-c2` hypotheses (disclosed in the docstring).

**Encoding read.**  The arc-lemma negation clause (for every Hamiltonian
`M_0 ∪ N`: some `N`-edge not in `G_c` or some arc of size `>= 4` not in
`S_c`) is the exact negation of the arc lemma.  Uniqueness `uq[A]` and
matchability `mt[A]` are encoded correctly by first-vertex expansion; (R) is
enumerated over all ordered partitions with `U` an `M_0`-union;
`--nonmatching1` correctly encodes "some vertex has `G_1`-degree `>= 2`".

**Reproduction.**  Rerun under `tools/research/run_bounded.py`:

| n | c1 | c2 | neg | extra | note's result | rerun |
|---|---|---|---|---|---|---|
| 8 | LF | none | 1 | | SAT | SAT 0.0 s, check PASS |
| 8 | LF | L | 1 | | UNSAT | UNSAT 0.0 s |
| 12 | F | S | 0 | `--force-c2 arc --fmax1 4` | UNSAT | UNSAT 0.3 s |
| 12 | L | S | 0 | `--force-c2 arc` | SAT | SAT 0.4 s, check PASS |
| 12 | F | LF | 0 | `--force-c2 matching --fmax1 4` | UNSAT | UNSAT 0.3 s |
| 12 | L | LF | 0 | `--force-c2 matching` | SAT | SAT 0.3 s, check PASS |
| 12 | LF, `fmax1 = 4` | L | 1 | | SAT | SAT 0.5 s, check PASS |

New rows (AL1's own hypothesis system, not in the note):

| n | c1 | c2 | neg | extra | result | reading |
|---|---|---|---|---|---|---|
| 8 | F | L | 0 / 1 | | SAT / UNSAT | AL1 holds at `n = 8` |
| 8 | F | L | 0 | `--nonmatching1` | UNSAT | ... but only trivially: every model has `G_1` a perfect matching |
| 10 | F | L | 0 / 1 | | UNSAT / UNSAT (2.3 s / 1.8 s) | AL1 is vacuous at `n = 10` |
| 12 | F | L | 0 | `--nonmatching1` | UNSAT (363.2 s) | every model of AL1's system at `n = 12` has `G_1` a perfect matching |

The long rows (2043 s, 1466 s, 1377 s, 1011 s, 999 s, 593 s, 1300 s) were not
rerun.

**AL1 is not stated exactly (G4).**  As written, AL1 says "Let `G_0 = M_0`"
and "let (H2) hold" but places no hypothesis on `S_0`.  (H2) involves `S_0`;
with `S_0` unconstrained (e.g. `S_0 = {∅, V}` plus `M_0`), (H2) is much weaker
than (R).  Everything the note says about AL1 uses `S_0 ⊇ {M_0-unions}`:
the solver rows eliminate colour 0 by Proposition 1 (which uses colour-0 (S)
and (F)), and "AL1 + Theorem B ⇒ (PM)" needs it in Theorem B.  The exact
statement should read, for instance:

> **(AL1, exact)**  Let `n >= 6` be even, `M_0` a perfect matching of `V`,
> `G_0 = M_0` and `S_0` the family of `M_0`-unions.  Let colour 1 satisfy (a),
> (S), (H1), (F); colour 2 satisfy (a), (L), (S), (H1); and let (H2) hold
> (equivalently (R)).  Then there is a perfect matching `N ⊆ G_1` such that
> `M_0 ∪ N` is a Hamiltonian cycle and every `N`-ended arc of it lies in
> `S_1`.

(Replacing "`S_0` = `M_0`-unions" by "`S_0 ⊇` `M_0`-unions" gives an
equivalent statement, since (R) is antitone in `S_0`; either is fine, but it
must be stated.)  With this correction, "AL1 + Theorem B ⇒ (PM) at every even
`n >= 6`" is correct: an AP' model with `G_0 = M_0` satisfies the hypotheses
by Proposition 1, and Theorem B with `c = 1`, `d = 2` uses colour-2 four-set
forcing, which AP' supplies.  AL1 is therefore load-bearing for (PM) as
claimed.

**"Minimal at `n = 12`" (G5).**  The inferences are valid where stated:
dropping colour-1 (F) is witnessed by the "L, L, neg 12" model (a model of a
stronger system), restricting it to four-sets by the "LF `fmax1 = 4`, L,
neg 1" model, dropping colour-2 (L) by the "LF, S, neg 1" model, dropping
colour 2 by Theorem A.  But "minimal" is relative to these four named moves
only, each witnessed by one uncertified run at one order; the hypotheses (a),
(S), (H1) of either colour and the colour-0 hypothesis were not tested, and
the SAT witnesses do not show minimality at other orders.  "Minimal among the
tested relaxations at `n = 12`" is the accurate phrasing.

**Evidence for AL1 itself (G9).**  The note reports AL1's system only at
`n = 12` ("F, L": SAT / UNSAT).  The reviewer's rows add: AL1 holds at
`n = 8` only because every model has `G_1` a perfect matching (so the arc
lemma is automatic from (F) and (i)), and AL1 is vacuous at `n = 10`.
At `n = 12` the reviewer's "F, L, `--nonmatching1`" run is UNSAT
(363.2 s, uncertified): **every model of AL1's hypothesis system at `n = 12`
has `G_1` a perfect matching**, so the note's "AL1 holds at `n = 12`
non-vacuously" is true but is witnessed only by models in which the arc
lemma is automatic (a perfect-matching colour with (F) contains all its
unions, and (i) makes `M_0 ∪ G_1` Hamiltonian).  The computations therefore
support, at `n = 8, 12` only, the sharper statement

> **(U1')** under the hypotheses of AL1 (without colour-1 (L)), `G_1` is a
> perfect matching,

which implies AL1's conclusion and, by Corollary B1, (PM).  U1' is the note's
U1 with the colour-1 (L) hypothesis removed; the solver data give no reason
to prefer AL1 to U1' as the stall lemma, and no evidence at all that the arc
lemma is ever attained non-trivially.  The note does mark the corresponding fact for the
stronger "LF, L" system at `n = 12` (its `--nonmatching1` row and U1), but
its highlighted reading "the arc lemma for colour 1 holds in every model at
`n = 12`" in the "LF, L" row should carry the same qualifier it carries at
`n = 8` ("every model has `G_1` a perfect matching, so the arc lemma is
trivial there").

**Scope of "no forcing" (G3).**  The ladder never drops colour-0 forcing:
colour 0 is eliminated by Proposition 1, whose `S_0 = {M_0-unions}` uses
colour-0 (F).  So the readings "`G_0 = M_0` excluded with **no forcing at
all**" (`n = 10`, "L, L"), "excluded by Laplace accessibility and (H2)
alone" (§6, last paragraph), "a Laplace-only route" (§5), and "the
disjunctive arc lemma holds without forcing at `n = 8`" (§6 table) should
say "without forcing in colours 1 and 2 (colour-0 forcing is built in)".  An
UNSAT for `S_0 = {M_0-unions}` does not transfer to a colour 0 without (F),
whose family could be smaller.

**Provenance of the `--nonmatching1` row (G6).**  The 1011.4 s UNSAT was
produced, per the note, by "an equivalent scratch encoding of the same
clause"; the committed flag is said to reproduce it, but no run of the
committed flag is recorded.  The reviewer read the flag's clauses and they
encode the stated hypothesis; equivalence with the scratch run is unverified.

## 7. What the note gets right about its own status

- The arc lemma is reported as **not proved**; the outcome table separates
  proved items, finite cross-checks, and exploratory computation.
- Theorems A and D are correctly called obstructions to proof methods, not
  AP' models.
- The `n = 12` "(PM) via the ladder plus Theorem B" argument is correctly
  called computer-assisted and uncertified, and is not promoted.
- `docs/current-frontier.md` was not edited, and the proof-distance delta is
  stated for the integration owner.  The delta is correct: Theorem B upgrades
  Lemma 5's implication from `n ≡ 2 (mod 4)` to every even `n >= 6` (now with
  the disjunctive arc lemma and four-set forcing in the other colour), and B1
  closes the two-perfect-matching case of (PM) outright.

## 8. Gaps (complete list)

- **G1** (Theorem B, cosmetic).  The "uses only" list omits `∅ ∈ S_c`.  It
  also does not use `N ⊆ G_c`, so the hypothesis can be dropped.
- **G2** (Theorem A, cosmetic).  `{0, 1} ∈ M_0` is used without being
  stated; cycle coordinates are defined relative to a fixed `N`, while
  Theorem A quantifies over all `N`.
- **G3** (scope wording, §5–§6).  "No forcing (at all)" readings omit the
  built-in colour-0 forcing.
- **G4** (AL1 exactness, substantive for the stall lemma).  AL1 omits the
  colour-0 hypothesis `S_0 = {M_0-unions}` (or `⊇`), and refers to the arc
  lemma whose quoted statement is phrased for AP' models; the corrected
  statement is in §6.
- **G5** ("minimal" wording).  Minimality is relative to four named
  relaxations, by single uncertified runs at `n = 12`.
- **G6** (provenance).  The `--nonmatching1` UNSAT row was run with a scratch
  encoding; no run of the committed flag is recorded.
- **G7** (verifier).  The Part B `n ≡ 2 (mod 4)` check is tautological; the
  verifier does not test Theorem B or B1 (not claimed).
- **G8** (cross-document staleness, not a defect of the note).  B1 gives an
  elementary proof of the uniform (CGI special) case at every order; the
  extra-edge document's "hard core of the CGI theorem, which this document
  does not reprove" (end of its §3) is stale once B1 is integrated, and the
  integration owner should cross-link B1, the WB4 review §3 proof, and the
  CGI registry entry.  Once B1 is independently reviewed, the uniform case
  (and the identical special case used by WB1 Step 10 and WB4 Step 3) need
  not rest on the CGI import; this review does not change those documents.
- **G9** (AL1 evidence).  At `n = 8` AL1 holds only trivially and at `n = 10`
  vacuously; at `n = 12` every model of its hypotheses has `G_1` a perfect
  matching (reviewer's uncertified run), so the arc lemma is only ever
  attained trivially in the data.  The sharper U1' (§6) is equally supported.
- **G10** (independence).  No independent audit of the note exists besides
  this same-day agent review; the explore script's SAT re-check is internal.
- **G11** (uncertified computation).  All UNSAT rows, including the `n = 12`
  "LF, LF" (PM) row and the AL1 row, have no proof trace; the `n = 16`
  arc-relative cross-check is a scratch encoding not reproduced by any
  committed script.

None of G1–G11 affects the truth of Theorems A, B, D, Lemma C, or
Corollary B1.  G4 must be fixed before AL1 is recorded as the next lemma in
the frontier.

## 9. Reproduction of the reviewer's checks

```text
python claims/arbitrary-order/verify_all_diagonal_support_level_ap_prime_arc_lemma_hole_model_and_closure.py
python tools/research/run_bounded.py --run-id <id> --timeout-seconds 600 --memory-mb 4000 -- \
  python claims/arbitrary-order/explore_all_diagonal_support_level_ap_prime_arc_lemma_relaxations.py 12 --c1 F --c2 S --negate-arc 0 --fmax1 4 --force-c2 arc
python tools/research/run_bounded.py --run-id <id> --timeout-seconds 1500 --memory-mb 4000 -- \
  python claims/arbitrary-order/explore_all_diagonal_support_level_ap_prime_arc_lemma_relaxations.py 10 --c1 F --c2 L --negate-arc 0
python tools/research/run_bounded.py --run-id <id> --timeout-seconds 2400 --memory-mb 8000 -- \
  python claims/arbitrary-order/explore_all_diagonal_support_level_ap_prime_arc_lemma_relaxations.py 12 --c1 F --c2 L --negate-arc 0 --nonmatching1
```

(and the other rows of the §6 tables with the flags shown).  The reviewer's
scratch script (not committed, ~2.4 s) implements, independently of the
verifier:

- **R1**: Theorem B's conclusion at `n = 6, ..., 16`, with splits
  `V − A = U ⊔ Q` found by enumerating `Q` over the explicit arc list;
- **R2**: the uniform specialisation of B1 (fourth perfect matching of
  `C ∪ M_1`) at `n = 6, ..., 12`;
- **R3**: Theorem D's colour-1 (a), (S), (L) and (H2) at `n = 8, 12, 16`,
  (H2) via perfect matchings of `C[V − A_1]`;
- **R4**: Theorem A at `n = 6, 14`.

Each check was mutation-tested (admitting alternating sets in Theorem D,
admitting hole sets in Theorem A, and removing the arcs in R1 all produce
failures).  No project-specific axiom, admitted step, external result, or
Lean claim is involved.
