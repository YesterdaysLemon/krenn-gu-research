# Arc-lemma attempt record — 2026-10-08

This is a dated research record.  It is not a frontier entry and changes no
status.  The arc lemma stays **open**, the all-diagonal branch is **open**, and
the global Krenn–Gu conjecture remains **UNRESOLVED**.

## Target and outcome

**Obligation attacked.**  The arc lemma of the
[extra-edge document](../../claims/arbitrary-order/ALL_DIAGONAL_SUPPORT_LEVEL_AP_PRIME_TOP_MATCHING_EXTRA_EDGE_LEMMA.md)
(Section 5):

> In an AP' model with `G_0 = M_0` a perfect matching, there is a perfect
> matching `N ⊆ G_1` such that `C = M_0 ∪ N` is a Hamiltonian cycle and every
> `N`-ended arc of `C` lies in `S_1`.

Scope: AP' as in WB2/WB4, every even `n >= 6`, support level only.  Upstream:
Proposition 1 and Lemma 2 of the extra-edge document.  Downstream consumer:
that document's Lemma 5, which turns the arc lemma into (PM) ("no colour's
support graph is a perfect matching") at `n ≡ 2 (mod 4)`; (PM) implies the
extra-edge sub-lemma of the WB4 top-matching lemma.

**Outcome: the arc lemma is not proved.**  This attempt proves four things at
every order and records solver evidence at `n <= 12`:

| item | content | status |
|---|---|---|
| Theorem B + Lemma C | the arc lemma for **either** colour 1 or colour 2, together with forcing on four-element sets in the other colour, contradicts (H2) at **every** even `n >= 6` (Lemma 5 needed `n ≡ 2 mod 4`) | proved; finite cross-check of Lemma C |
| Corollary B1 | no AP' model has **two** colours whose support graphs are perfect matchings, at every even `n >= 6` | proved |
| Theorem A | colour-1 axioms plus "no proper `M_0`-union in `S_1`" do **not** imply the arc lemma, at every even `n >= 6` (an explicit "hole model"); colour 2 must enter | proved; brute-force cross-check at `n <= 12` |
| Theorem D | at every `n ≡ 0 (mod 4)`, `n >= 8`, a model of every AP' axiom except forcing in colour 1, with two perfect-matching colours and the arc lemma for one of them; so the forcing hypothesis of Theorem B and B1 cannot be dropped | proved; brute-force cross-check at `n = 8, 12` |
| computation | the ladder of relaxations in Section 6; in particular, at `n = 12`, the arc lemma for colour 1 holds in every model of "colour 1 with forcing but no Laplace axiom, colour 2 with Laplace but no forcing, (H2)", non-vacuously; and AP' with `G_0 = M_0` is UNSAT at `n = 12` (2043 s) | exploratory, uncertified, one order each |

**Proof-distance delta (for the integration owner; `docs/current-frontier.md`
was not edited, by instruction).**  Before: arc lemma ⇒ (PM) at
`n ≡ 2 (mod 4)` only.  After: the *disjunctive* arc lemma (for colour 1 or
colour 2) ⇒ (PM) at every even `n >= 6` (Theorem B), and the two-perfect-
matching case of (PM) is closed outright (Corollary B1).  The stall point is
the sharper lemma (AL1) of Section 7, whose hypotheses the solver ladder shows
to be minimal at `n = 12`.  No route was refuted; no AP' model was found.

## Setting and notation

As in the extra-edge document: `V`, `|V| = n` even, `G_0 = M_0`, so
`S_0` is the family of `M_0`-unions (Proposition 1) and (H2) is

> (R) no partition `V = U ⊔ A_1 ⊔ A_2` with `U` an `M_0`-union, `A_1 ∈ S_1`,
> `A_2 ∈ S_2`, and at least two classes nonempty.

Consequences used: (i) no proper nonempty `M_0`-union is in `S_1 ∪ S_2`;
(ii) `G_1 ∩ M_0 = G_2 ∩ M_0 = ∅`.

**Cycle coordinates.**  If `N` is a perfect matching with `C = M_0 ∪ N` a
Hamiltonian cycle, relabel `V = Z_n` along `C` so that `M_0 = {2i, 2i+1}` and
`N = {2i+1, 2i+2}` (indices mod `n`).  Put `X` = even vertices, `Y` = odd
vertices.  A **run** is a set of cyclically consecutive vertices.  An even run
is tiled in exactly one way by edges of `C`: by `M_0`-edges if it starts at an
even vertex, by `N`-edges if it starts at an odd vertex.  An `N`-tiled run is
exactly an `N`-ended arc (or empty).

## 1. Theorem A (the hole model): the arc lemma is not a colour-1 statement

**Theorem A.**  For every even `n >= 6` (with the convention `{0, 1} ∈ M_0`)
put `G_1 = K_n − M_0` and let `S_1`
consist of `∅`, `V`, and every even `A` with `|A| >= 2` that is neither an
`M_0`-union nor a **hole set** `{0, 1, x, y}` (with `x, y ∉ {0, 1}`,
`xy ∉ M_0`).  Then `(G_1, S_1)` satisfies (a), (L), (S), (F), `G_1 ∩ M_0 = ∅`
and (i), and for **every** perfect matching `N ⊆ G_1` with `M_0 ∪ N`
Hamiltonian, the `N`-ended arc `{N(0), 0, 1, N(1)}` is not in `S_1`.  So the
arc lemma fails.

*Proof.*  Members of size two are the non-`M_0` pairs, i.e. `G_1`: (a).
For `k >= 4` even, `K_k` minus a matching has at least two perfect matchings
(for `k = 4`: the three perfect matchings of `K_4` are edge-disjoint and a
removed matching of `K_4` kills at most one of them; for `k >= 6`: a vertex
has at least `k − 2 >= 4` neighbours and each leaves `K_{k−2}` minus a
matching).  Hence (S) holds and the only uniquely matchable sets are the
edges, so (F) holds.  (i) holds by construction.

(L): let `A ∈ S_1`, `v ∈ A`; we need `u ∈ A`, `u ≠ v'`, with
`R = A − {v, u} ∈ S_1`, i.e. `R` neither a proper nonempty `M_0`-union nor a
hole set.  *At most one* `u ≠ v'` makes `R` an `M_0`-union: if `A − {v, u}`
and `A − {v, w}` both are, then `u ∈ A − {v, w}` forces `u' ∈ A − {v}`, while
`u ∉ A − {v,u}` forces `u' ∉ A − {v, u}`, so `u' = v`, excluded.
`|A| = 2`: `R = ∅`.  `|A| = 4`: `A` has four singleton `M_0`-classes (any
`u ≠ v` works) or one pair `{p, p'} ≠ {0, 1}` and two singletons `x, y`; take
`u = x` for `v = p`, and `u = p` for `v = x`; the remainder is a non-`M_0`
pair.  `|A| = 6`: if `v ∈ {0, 1}` or `{0, 1} ⊄ A`, then `R` is never a hole
set and at least three of the `>= 4` candidates `u ≠ v'` are good; otherwise
`u = 0` leaves `R ∋ 1`, `R ∌ 0`, which is neither an `M_0`-union nor a hole
set.  `|A| >= 8` (including `A = V`): `R` is never a hole set and at most one
of the `>= 5` candidates is bad.

Arcs: in `C = M_0 ∪ N` the path `N(0), 0, 1, N(1)` has end edges in `N`; its
four vertices are distinct, and `N(0) N(1) ∉ M_0` because otherwise `C`
would contain a 4-cycle, impossible for a Hamiltonian cycle on `n >= 6`
vertices.  So it is a hole set.  ∎

**What Theorem A rules out.**  Mechanisms that use only colour-1 axioms and
(i): (a) coherence of widow-first chains (here almost every non-`M_0` pair
is a supported partner in every context, so the partner choices, and with
them the chain cycles, are unconstrained apart from avoiding the hole sets),
and (c) forcing of uniquely matchable arcs (here (F) is vacuous above size
two).  Any proof must use colour 2 through (R).

**Remark (how colour 2 can enter).**  (R) is preserved when `S_1` or `S_2` is
shrunk, so (R) never implies that a set *is* a member.  It can force an arc
into `S_1` only jointly with (L) or (F): by excluding every other supported
Laplace child of some member, or by deleting edges so that an arc becomes
uniquely matchable.  Mechanism (b) of the task ("an arc through `ab` whose
complement is an `M_0`-union plus a set in `S_2` would violate (R)") is a
non-membership statement and must be used in that pruning form.

## 2. Lemma C (an `M_0`-edge carries a crossing)

**Lemma C.**  Let `n ≡ 0 (mod 4)`, `n >= 8`, and let `F` be a perfect matching
of `Z_n` all of whose edges join vertices of equal parity.  Then some even
`x` has the chords `{x, F(x)}` and `{x+1, F(x+1)}` crossing.  Consequently the
four endpoints occur in the cyclic order `x, x+1, F(x), F(x+1)`, and the
complement of `{x, x+1, F(x), F(x+1)}` is a union of even runs of which at
most one is `N`-tiled.  For `n ≡ 2 (mod 4)` no such `F` exists.

*Proof.*  If `n ≡ 2 (mod 4)`, `|X| = n/2` is odd.  Otherwise let
`ℓ(v) = (F(v) − v) mod n ∈ {2, 4, ..., n−2}` (clockwise length).  For even
`x`, measured clockwise from `x`, the points `x+1`, `F(x)`, `F(x+1)` sit at
`1`, `ℓ(x)`, `1 + ℓ(x+1)`.  The chords do not cross exactly when `F(x+1)`
lies strictly between `x+1` and `F(x)`, i.e. `ℓ(x+1) <= ℓ(x) − 2`.  If this
held for every even `x`, summing would give
`Σ_{y odd} ℓ(y) <= Σ_{x even} ℓ(x) − n`.  But `ℓ(v) + ℓ(F(v)) = n`, so each
side sums to `(n/4)·n`: contradiction.  For a crossing `x`, the cyclic order
is `x, x+1, F(x), F(x+1)`; the gaps are `0`, `ℓ(x) − 2` (starting at the even
vertex `x+2`), `ℓ(x+1) − ℓ(x)` (starting at the odd vertex `F(x)+1`), and
`n − 2 − ℓ(x+1)` (starting at the even vertex `F(x+1)+1`); all are even and
only the third can be `N`-tiled.  ∎

## 3. Theorem B (the arc lemma closes (PM) at every order)

**Theorem B.**  Let an AP' model on `n >= 6` vertices have `G_0 = M_0`, and
let `{c, d} = {1, 2}`.  Suppose the arc lemma holds for colour `c`: some
perfect matching `N ⊆ G_c` has `C = M_0 ∪ N` Hamiltonian and every `N`-ended
arc of `C` in `S_c`.  Then (H2) fails.  The proof uses, besides
`S_0 ⊇ {M_0-unions}`, `∅ ∈ S_c` for every colour, and (H2), only: for colour `c`, the arcs; for colour
`d`, axiom (a), a perfect matching of `G_d` (from (S) and (H1)), and forcing
(F) on sets of size four.

*Proof.*  Use cycle coordinates for `C`.

*Step 1: every edge of `G_d` joins vertices of equal parity.*  Let
`ij ∈ G_d` with `i` even, `j` odd.  `ij ∉ M_0` by (ii).  The complement of
`{i, j}` consists of the run after `i` (starting at the odd vertex `i+1`,
hence `N`-tiled: an `N`-ended arc `Q` or empty) and the run after `j`
(starting at the even vertex `j+1`, hence an `M_0`-union `U`); both have even
length because `j − i` is odd.  Then `A_0 = U`, `A_c = Q ∈ S_c` (arc lemma),
`A_d = {i, j} ∈ S_d` (a) is a partition with at least two nonempty classes,
violating (H2).

*Step 2.*  `G_d` has a perfect matching `F` (by (S) at `V ∈ S_d`), whose edges
join equal-parity vertices.  If `n ≡ 2 (mod 4)` this is already impossible.
Otherwise Lemma C gives an even `x` with crossing chords `x x*`,
`(x+1) y*` of `F`.

*Step 3.*  `A = {x, x+1, x*, y*}`: by Step 1 the only possible `G_d`-edges
inside `A` are `x x*` and `(x+1) y*`, so `G_d[A]` has exactly one perfect
matching, and (F) gives `A ∈ S_d`.

*Step 4.*  By Lemma C, `V − A = U ⊔ Q` with `U` an `M_0`-union and `Q` an
`N`-ended arc or empty.  The partition `A_0 = U`, `A_c = Q`, `A_d = A` has
`A` and `V − A` nonempty, so at least two nonempty classes, violating (H2).  ∎

So the arc lemma for one colour implies (PM) at **every** even `n >= 6`,
which strengthens Lemma 5 of the extra-edge document (there: one colour, only
`n ≡ 2 mod 4`, no forcing used).  The two colours enter asymmetrically:
arcs in one, four-set forcing in the other.  In particular the *disjunctive*
arc lemma (for colour 1 **or** colour 2) suffices.

**Corollary B1 (two perfect-matching colours).**  No AP' model on `n >= 6`
vertices has two colours whose support graphs are perfect matchings.

*Proof.*  Permute colours so that `G_0 = M_0` and `G_2 = N`.  Every
`N`-union is uniquely matchable in `G_2`, so lies in `S_2` by (F).  `N ∩ M_0
= ∅` by (ii).  If `M_0 ∪ N` had a proper cycle component `K`, then `K ∈ S_0`
and `V − K ∈ S_2` would violate (H2); so `C = M_0 ∪ N` is Hamiltonian, its
`N`-ended arcs are `N`-unions, and Theorem B (with `c = 2`, `d = 1`)
applies.  ∎

Corollary B1 contains the uniform case of the extra-edge document
(Proposition 3, Corollary 3') at every order; the special case needed there
(three pairwise disjoint perfect matchings, every two forming a Hamiltonian
cycle) also has the reviewer's self-contained argument in
[the WB4 review](../audits/ALL_DIAGONAL_SUPPORT_LEVEL_AP_PRIME_BRANCHING_LEMMA_REVIEW_2026-10-08.md)
(Section 3), which Lemma C refines (the crossing can be found at an
`M_0`-edge, which is what lets a single arc replace two).  The extra-edge
sub-lemma ("every `E_c` a perfect matching ⇒ no `G_c = M_c`") is thereby
reduced to the case in which **exactly one** colour has a perfect-matching
support graph.

## 4. Theorem D (forcing in the second colour is necessary)

**Theorem D.**  Let `n ≡ 0 (mod 4)`, `n >= 8`, in cycle coordinates.  Put
`G_0 = M_0`, `S_0` = `M_0`-unions; `G_2 = N`, `S_2` = `N`-unions;
`G_1` = all pairs of equal parity; and `S_1 = {∅, V}` ∪ `{A : |A ∩ X|,
|A ∩ Y| even, |A| >= 2, A not alternating}`, where `A` is *alternating* if its
elements alternate in parity in cyclic order.  This satisfies every AP' axiom
except (F) in colour 1.  Colours 0 and 2 have perfect-matching support graphs
and colour 2 satisfies the arc lemma.

*Proof.*  Colours 0 and 2 are unions of a perfect matching (all axioms).
Colour 1: (a) because two-element members are the equal-parity pairs; (S)
because `G_1[A]` is two cliques of even order; (H1) by definition.
(L): let `A ∈ S_1`, `v ∈ A ∩ X` (the case `Y` is symmetric), `a = |A ∩ X|`,
`b = |A ∩ Y|`.  An alternating set has `a = b`, so if `a − 2 ≠ b` any
`u ∈ A ∩ X − {v}` gives a non-alternating child (or `∅`).  If `a − 2 = b >= 2`,
the `b` points of `A ∩ Y` cut the circle into `b` gaps holding the `b + 1`
points of `A ∩ X − {v}`; removing `u` leaves an alternating set only if every
gap then holds exactly one point, so choosing `u` in a gap with one point (or
any `u` if no such gap exists) gives a non-alternating child.  (H2): if
`V = U ⊔ A_1 ⊔ A_2` with `U` an `M_0`-union, `A_2` an `N`-union, and `A_1`
proper and nonempty, then `V − A_1` is covered by edges of `C`, so all gaps
of `A_1` are even and consecutive elements of `A_1` differ in parity:
`A_1` is alternating, hence not in `S_1`.  If `A_1 = ∅`, the partition is a
perfect matching of the cycle `C` using both `M_0` and `N`, which does not
exist.  If `A_1 = V`, only one class is nonempty.  (F) fails in colour 1: a
crossing pair from Lemma C gives an alternating, uniquely matchable 4-set.  ∎

Hence the four-set forcing hypothesis of Theorem B and of Corollary B1 cannot
be removed at any `n ≡ 0 (mod 4)`.  (At `n ≡ 2 (mod 4)` Lemma 5 needs no
forcing.)

## 5. What did not work

- (a) *Coherence of widow-first chains.*  Lemma 2 fixes the cycle of one
  chain, but the partner of a widow is chosen by the model and may depend on
  the history.  Theorem A shows that colour-1 axioms do not constrain the
  partners at all beyond (i), so coherence can only come from (R).  I found no
  argument that (R) with the colour-2 sets supplied by colour-2 chains forces
  coherence.
- (b) *(R) on arcs through `ab`.*  As posed it is a non-membership statement;
  see the Remark after Theorem A.
- (c) *Forcing on uniquely matchable arcs.*  Vacuous in the hole model; in the
  solver ladder, forcing restricted to four-sets in colour 1 is not enough for
  the arc lemma at `n = 12` (Section 6, row "`fmax1 = 4`").
- A Laplace-only route: the system "both colours with (a), (L), (S), no
  forcing" has models at `n = 12` in which the arc lemma fails for both
  colours, so some forcing is necessary for the arc lemma at that order (at
  `n = 8` the disjunctive form still holds without forcing, a small-order
  effect).

## 6. Computations (exploratory; not proof)

Script:
`claims/arbitrary-order/explore_all_diagonal_support_level_ap_prime_arc_lemma_relaxations.py`
(new; its own encoding with `G_0 = M_0` built in, colour-0 variables
eliminated by Proposition 1, (R) enumerated directly; no symmetry breaking).
`c1`, `c2` list the axioms imposed on colours 1, 2 (`L` = Laplace, `F` =
forcing; (a), (S), (H1) always; `S` alone = only those; `none` = colour 2
absent).  "neg" lists the colours for which the arc-lemma negation is added
(`0` = none).  CaDiCaL 1.5.3 through `python-sat`, single thread, Windows;
SAT models re-checked by the script's independent brute-force checker (all
PASS).  UNSAT answers carry no proof trace; each is evidence at one order
only.  A row is *vacuous* when the system without the negation is already
UNSAT.

| n | c1 | c2 | neg | extra | result | s | reading |
|---|---|---|---|---|---|---|---|
| 8 | LF | none | 1 | | SAT | 0.0 | hole-type model (Theorem A) |
| 8 | LF | S | 1 | | SAT | 0.0 | |
| 8 | LF | L | 0 / 1 | | SAT / UNSAT | 0.0 | non-vacuous, but every model has `G_1` a perfect matching (scratch query), so the arc lemma is trivial there |
| 8 | LF | F | 0 | | UNSAT | 0.0 | |
| 8 | L | L | 0 / 1 / 12 | | SAT / SAT / UNSAT | ≤ 0.3 | disjunctive arc lemma holds without forcing at `n = 8` only |
| 8 | L | LF | 1 | | SAT | 0.0 | |
| 10 | LF | S | 0 / 1 | | SAT / SAT | 0.1 | by Lemma 5 every such model violates the arc lemma |
| 10 | LF | L | 0 | | UNSAT | 4.9 | `G_0 = M_0` excluded without colour-2 forcing |
| 10 | S | L | 0 | | SAT | 0.1 | |
| 10 | L | L | 0 | | UNSAT | 1300.5 | `G_0 = M_0` excluded with **no forcing at all** (rows with neg 1, 12 are vacuous) |
| 12 | L | L | 0 / 12 | | SAT / SAT | ≤ 0.8 | arc lemma fails for both colours without forcing |
| 12 | L | LF | 1 | | SAT | 2.0 | colour 2 uniform, colour 1 non-uniform: arc lemma needs colour-1 forcing |
| 12 | LF | S | 0 / 1 | | SAT / SAT | ≤ 0.9 | arc lemma needs colour-2 Laplace or forcing |
| 12 | LF | L | 0 / 1 | | SAT / **UNSAT** | 0.5 / 999.5 | **non-vacuous: the arc lemma for colour 1 holds in every model at `n = 12`** |
| 12 | F | L | 0 / 1 | | SAT / **UNSAT** | 7.1 / 592.8 | **non-vacuous: colour-1 Laplace accessibility is not needed either** |
| 12 | LF, `fmax1 = 4` | L | 1 | | SAT | 0.4 | four-set forcing in colour 1 is not enough |
| 12 | F | S | 0 | `--force-c2 arc`, `fmax1 = 4` | UNSAT | 0.4 | Theorem B (cross-check) |
| 12 | L | S | 0 | `--force-c2 arc` | SAT | 0.3 | Theorem D direction (forcing needed) |
| 12 | F | LF | 0 | `--force-c2 matching`, `fmax1 = 4` | UNSAT | 0.3 | Corollary B1 (cross-check) |
| 12 | L | LF | 0 | `--force-c2 matching` | SAT | 0.4 | Theorem D (cross-check) |

Further `n = 12` rows (all under `tools/research/run_bounded.py`):

| n | c1 | c2 | neg | extra | result | s | reading |
|---|---|---|---|---|---|---|---|
| 12 | LF | LF | 0 | | **UNSAT** | 2043.3 | AP' with `G_0 = M_0` has no model at `n = 12`: (PM) at `n = 12`, direct, uncertified |
| 12 | LF | F | 0 / 1 | | UNSAT / UNSAT | 1466.0 / 1377.0 | `G_0 = M_0` excluded without colour-2 (L); the neg row is vacuous |
| 12 | LF | L | 0 | `--nonmatching1` | UNSAT | 1011.4 | every model of the "LF, L" row has `G_1` a perfect matching (run with an equivalent scratch encoding of the same clause; the flag reproduces it) |
| 12 | LF | LF | 1 | | stopped | — | redundant by Theorem B (every full model violates both arc lemmas); stopped by the agent, not evidence |
| 12 | LF | L | 12 | | stopped | — | redundant with the "LF, L, neg 1" row by Theorem B; stopped, not evidence |

Scratch cross-check, not reproduced by the committed script: a colour-1-only
encoding of the arc-relative system (colour 2 replaced by exactly the arcs of
a fixed cycle) with colour-1 forcing on four-sets is UNSAT at `n = 16` in
1.9 s, as Theorem B predicts.

**Reading.**  At `n = 12` the solver ladder isolates which axioms the arc
lemma for colour 1 needs: colour-1 forcing beyond four-sets, colour-2 (L),
and (R).  Neither colour-1 (L) nor colour-2 forcing is needed (both rows
non-vacuous).  Combined with
Theorem B (which uses colour-2 four-set forcing), the `n = 12` UNSAT row is a
computer-assisted, **uncertified** argument that (PM) holds at `n = 12`: an
AP' model with `G_0 = M_0` would satisfy the hypotheses of that row, hence
the arc lemma for colour 1, hence violate (H2) by Theorem B.  The direct run "LF, LF, neg 0" (UNSAT,
2043 s) agrees.  No DRAT
certificate was produced; the claim is not promoted.

The `n = 10` row "L, L" says that at this order `G_0 = M_0` is excluded by
Laplace accessibility and (H2) alone.  This is suggestive of a forcing-free
parity mechanism at `n ≡ 2 (mod 4)` (Lemma 5's mechanism), but it is one
uncertified run at one order.

## 7. Stall point and the sharpest next lemma

> **(AL1)** Let `G_0 = M_0` with `S_0` the family of `M_0`-unions (all
> colour-0 axioms, Proposition 1), let colour 1 satisfy (a), (S), (H1) and
> (F), let colour 2 satisfy (a), (L), (S), (H1), and let (H2) hold.  Then the
> arc lemma holds for colour 1.

(Statement corrected after the same-day
[review](../audits/docs/audits/AP_PRIME_ARC_LEMMA_ATTEMPT_REVIEW_2026-10-08.md), which found the colour-0
hypothesis missing; the review also reports an uncertified `n = 12` run
showing that every model of AL1's hypotheses there has `G_1` a perfect
matching, where the arc lemma holds trivially, so the solver data support
the sharper statement "AL1's hypotheses force `G_1` to be a perfect
matching" equally well.)

The colours play opposite roles: forcing in the arc colour, Laplace
accessibility in the other; Theorem B then needs forcing on four-sets in
the other colour.

- AL1 + Theorem B ⇒ (PM) at every even `n >= 6` (an AP' model with
  `G_0 = M_0` satisfies AL1's hypotheses; Theorem B then uses colour-2
  four-set forcing).  So AL1 is load-bearing for (PM), hence for the
  extra-edge sub-lemma.
- The hypotheses of AL1 are minimal at `n = 12` by the ladder: drop colour-1
  (F) — SAT (and Theorem D shows the companion phenomenon at every
  `n ≡ 0 mod 4`); restrict colour-1 (F) to four-sets — SAT; drop colour-2
  (L) (keeping (S)) — SAT; drop colour 2 entirely — fails at every order
  (Theorem A).  Adding colour-1 (L) is not needed (row "F, L").
- AL1 holds at `n = 12` (uncertified) non-vacuously; the stronger-hypothesis
  version with colour-1 (L) holds at `n = 8` only trivially (colour 1 is
  forced to be a perfect matching) and vacuously at `n = 10`.
- A possibly sharper form, suggested by the "`--nonmatching1`" row: **(U1)**
  under the hypotheses of AL1 with colour-1 (L) added, `G_1` is a perfect
  matching.  U1 implies AL1's conclusion (a perfect-matching colour has all
  its unions, and (i) makes `M_0 ∪ G_1` Hamiltonian) and, by Corollary B1,
  (PM).  Evidence: `n = 8` and `n = 12` only, uncertified.  U1 would say
  that a perfect-matching colour forces a second one; Theorem D shows the
  forcing in the second colour is what then excludes the pair.
- Where a proof is stuck: AL1 asks that colour-2 Laplace chains, through
  (R), prune colour-1 Laplace alternatives until the colour-1 widow-first
  chains become coherent.  Lemma 2 of the extra-edge document gives each
  chain's cycle; no argument here relates the cycles of two colour-1 chains
  through colour-2 sets.

## Boundary

- Proved at every even `n >= 6` (or every `n ≡ 0 mod 4`, `n >= 8`, for
  Theorem D): Theorems A, B, D, Lemma C, Corollary B1.  They are statements
  about the support abstraction AP' and its relaxations; none is a witness, an
  exclusion of a witness, or a status change.
- Theorems A and D are obstructions to proof *methods*, not models of AP'
  (Theorem A has no colour 2; Theorem D violates (F) in colour 1).
- Section 6 is exploratory: single solver runs, no proof traces, one order
  each.  The `n = 12` (PM) consequence is computer-assisted and uncertified.
- No external result is used.  No independent audit of this record exists.

## Verification

```text
python claims/arbitrary-order/verify_all_diagonal_support_level_ap_prime_arc_lemma_hole_model_and_closure.py
```

Expected `"result": "PASS"` in a few seconds.  It checks exactly, by brute
force: Theorem A at `n = 6, 8, 10, 12` (all colour-1 axioms, (i), and a
missing arc on every Hamiltonian cycle — exactly the four-arc through `01`);
Lemma C and the run decomposition for every equal-parity perfect matching at
every even `n <= 16` (11,025 matchings at `n = 16`), including the length
identity and the crossing criterion of the proof; Theorem D at `n = 8, 12`
(every AP' axiom, (H2) over all 132,858 partitions at `n = 12`, and failure
of colour-1 forcing).  These are finite cross-checks; the proofs above are
the evidence for all orders.

Section 6 rows, for example:

```text
python claims/arbitrary-order/explore_all_diagonal_support_level_ap_prime_arc_lemma_relaxations.py 8 --c2 none
python claims/arbitrary-order/explore_all_diagonal_support_level_ap_prime_arc_lemma_relaxations.py 12 --c1 F --c2 S --negate-arc 0 --fmax1 4 --force-c2 arc
python tools/research/run_bounded.py --run-id arc12-LF-L-neg1 --timeout-seconds 7000 --memory-mb 9000 -- python claims/arbitrary-order/explore_all_diagonal_support_level_ap_prime_arc_lemma_relaxations.py 12 --c1 LF --c2 L --negate-arc 1
python tools/research/run_bounded.py --run-id arc10-L-L-neg0 --timeout-seconds 3000 --memory-mb 6000 -- python claims/arbitrary-order/explore_all_diagonal_support_level_ap_prime_arc_lemma_relaxations.py 10 --c1 L --c2 L --negate-arc 0
```
