# Adversarial review: cut-tensor (bipartite slice) rigidity attempt

Date: 2026-10-09

Review type: **same-day agent review**.  A separate agent session in its own
worktree was briefed adversarially.  This is not independent human
refereeing, not an independent re-derivation by a different research group,
and not formal kernel verification.  No Lean counterpart exists.

Global Krenn–Gu status: **UNRESOLVED** (unchanged by this review).

Reviewed objects (commit `9917aaae3ab734983b82bd36dd9b6c01ac361dd7`, branch
`origin/claude/cut-tensor-rigidity-20261009`; git blob ids):

| file | blob |
|---|---|
| `docs/strategy/cut-tensor-rigidity-attempt-2026-10-09.md` | `4eac67128e6676e6344a760d33a2d3891610169d` |
| `claims/finite/n06/verify_bipartite_cut_tensor_rigidity_small_cuts.py` | `fe9781b3d0e316cfa6f8477cef6ee83d953c8db4` |
| `tools/explore/groebner_bipartite_cut_tensor_k2.py` (exploratory) | `90f8092d97abeddc2e1ffdca9d631cad33248849` |
| `tools/explore/probe_bipartite_cut_tensor_least_squares.py` (exploratory) | `284c6ee8ed6190eef8517a51bb58ede527fb3d40` |
| `claims/arbitrary-order/THREE_COLUMN_BILINEAR_GRID_THEOREM.md` (input, Theorem 3(b)) | `aaf3bbec0f4991852d5d42e504285fc084da270c` |

The reviewed documents were not edited.

## Summary verdict

| item | verdict |
|---|---|
| (1) F ⟺ N by rescaling one vertex's rows | **PASS**; all three constant values become `1` with one rescaling; re-checked exactly at `k = 2, 3` |
| (2) Lemma C; `k = 2` and `k = 3` proofs of Version F | **PASS**; full vectors exist over any infinite field (char 2 included); rank bound correct; `k = 3` case analysis complete.  Understated: the `k = 2` case holds over **every** field |
| (3) Version R refuted by the `n = 4` matrix-unit witness | **PASS**; all 81 slice permanents recomputed with independent code |
| (4) "Lemma C is vacuous on all-invertible blocks at `k >= 5`" | **FAIL: the [PROVED] claim is false.**  Lemma C excludes every all-invertible configuration at every `k >= 2` (proof and exact replay in Section 4).  The `k = 4` "allowed pair" example is also excluded.  The headline "Lemma C cannot close `k >= 4` by itself" survives, for a different reason |
| (5) Unequal sides; corollary "every `n = 4` witness has all six blocks nonzero" | **PASS** (trivial / correct); the corollary holds over every field |
| (6) Verifier and Gröbner run | **REPRODUCED**: verifier passes all 13 checks (7.3 s) and replays what the note says it replays; the `k = 2` Gröbner basis is `[1]` (1055 s under `run_bounded.py`) |
| (7) "Version F for all `k` is exactly the bipartite Krenn–Gu problem" | **PASS with scope wording**: true for support graphs with no `P`–`P` or `Q`–`Q` edges, three colours, and arbitrary (possibly zero) cross blocks.  It is not a statement about cut slices of a general witness |
| (8) Gaps | twelve items, Section 8 |

The finding in item (4) is a false [PROVED] statement in the strategy note
(Section 6, "Boundary of the mechanism at `k >= 5`").  It does not affect the
`k = 2, 3` Theorem, the `n = 4` corollary, or the Version R countermodel.  It
changes the description of where Lemma C stops, not any order, frontier edge,
or the global status.  No exact counterexample to the Krenn–Gu conjecture
appeared.

## 1. F ⟺ N (attack item 1)

- Replace `B_pq` by `D^{-1} B_pq` for one fixed `p` and all `q`, with
  `D = diag(per(A_0), per(A_1), per(A_2))` (constant words).  Row `p` of
  `A_a` is scaled by `D^{-1}[a_p, a_p] = per(A_{a_p})^{-1}`, and the
  permanent is linear in row `p`.  So `per'(A_a) = per(A_a) / per(A_{a_p})`.
- Mixed words stay `0`.  For the constant word `c`, `a_p = c`, so
  `per'(A_c) = 1`.  The factor depends only on `a_p`, so **all three**
  constant values become `1` simultaneously.  One rescaling suffices.
- Reviewer check R1 (exact, `Fraction` arithmetic, random rational blocks):
  `per'(a) per(A_{a_p}) = per(a)` on all 81 (`k = 2`) and all 729 (`k = 3`)
  words; all three constant values equal `1` afterwards.
- Scope: this is a local statement about a bare cut tensor.  Inside a
  witness, the same rescaling also rescales inside blocks at `p`; the note
  does not claim otherwise.

**Verdict: PASS.**

## 2. Lemma C and the `k = 2, 3` proofs (attack item 2)

### 2.1 Lemma C

- Grouping by the partner of `p` is exhaustive.  If the partner is the open
  `q`, the minor on `P - p`, `Q - q` has all rows closed and exactly one
  open column `q'`, so it is linear in `y'`.  The same holds symmetrically.
  If the partner is a closed `q''`, the factor is
  `delta^T B_pq'' w_q''`.  Under the hypothesis the junk terms vanish, and
  `F = a l^T + l' b^T` has rank `<= 2`.
- The contracted target is `diag(lambda_c delta_c prod u_{p',c} prod
  w_{q'',c})`.  It has rank `3` exactly when all of these vectors are full
  and all `lambda_c != 0` (Version N).  Correct.
- Reviewer check R3 (exact, `k = 4`, two closed columns, 6 instances):
  rank `<= 2` when `delta` is orthogonal to both closed images.  Fullness
  of `delta` is irrelevant to the rank identity.

### 2.2 Existence of full vectors

- The hyperplane fact is correct over any field with at least three
  elements.
  - If `v = 0`, every full vector works.
  - If `v` has one nonzero coordinate, `v^⊥` is a coordinate plane and
    contains no full vector.
  - Otherwise the note's formulas work: `(1/v1, t/v2, -(1+t)/v3)` with
    `t not in {0, -1}`, and `(1/v1, -1/v2, 1)`.
- This is the characteristic-free variant of Theorem 3(b).  Theorem 3(b) as
  written uses `-2/l3` and needs characteristic not two.  The note supplies
  the variant, so characteristic two over an infinite field is covered.
  Only 3(b) is used, not Theorem 3 itself (which needs characteristic not
  two).

### 2.3 `k = 2`

`Q'' = ∅`, so any full `delta`, for example `(1, 1, 1)`, satisfies the
hypothesis.  **Correct.**

**Understatement.**  The `k = 2` argument needs only the all-ones vectors.  So
Version N at `k = 2` is impossible over **every** field, finite fields
included.  Reviewer check R6: over `F_2`, 200 random block sets all give a
contraction with determinant `0`, against the rank-3 target.  The `n = 4`
corollary therefore also holds over every field.

**Reviewer remark (border).**  At `k = 2` Lemma C is a closed condition.  For
**every** cut tensor, the contraction with `delta = u = (1,1,1)` has rank
`<= 2`.  Its entries are sums of nine word values, so
`||C(T) - I||_F <= 3 ||T - Delta||_2`.  By Eckart–Young, a rank-`<= 2`
matrix is at Frobenius distance at least `1` from `I_3`.  Hence every
`k = 2` cut tensor has residual norm at least `1/3`.  This proves the
"not a border point" suggestion of note Section 4 at `k = 2`.  The bound
`1/3` is weaker than the numerical `1`.  At `k = 3` the hypothesis on `delta`
depends on the configuration, and the argument does not transfer directly.
This remark is a hand argument only; no verifier replays it.

### 2.4 `k = 3`

1. **Single-entry forcing.**  For `k = 3`, each `q''` is the complement of
   a pair, so every block is reached.
   - The set `{w : Bw in union of coordinate lines}` is Zariski closed and
     contains the dense set of full vectors, so it is `F^3`.
   - A subspace inside a union of three lines over an infinite field lies in
     one of them.
   - `B != 0`, because `Bw = 0` would admit every full `delta`.
   - The step `b = beta e_d` again uses the hyperplane fact.

   Correct.  This needs an infinite field: the density step fails over
   finite fields.  The Theorem is stated over infinite fields.
2. **Colour classes.**  Single-entry blocks have one type each.
   `per(A_c) != 0` gives `sigma_c` inside the type-`(c, c)` edges.  Three
   pairwise edge-disjoint perfect matchings of `K_{3,3}` cover all 9 edges,
   so all types are diagonal and `L` is a Latin square.  Correct.
3. **Surviving mixed word.**
   - The word of `sigma` is well defined, because `sigma` is a bijection.
   - It is mixed, because a constant word would put `sigma` inside one
     class.
   - Latin rows force `sigma' = sigma`.
   - The value is a single nonzero product.  Correct.

Reviewer check R5 enumerates the 12 Latin squares directly.  This encoding
differs from verifier check [5], which enumerates disjoint matching triples.
For every Latin square and every non-class `sigma`, the word is mixed with
value equal to the product of the three weights.  It also confirms
`per(A_c) = prod beta` on the class matchings.

**Cross-check.**  The reviewer's delta-first form of Lemma C (Section 4)
forces, at `k = 3`, every block to be both single-column and single-row,
hence single-entry.  This is an independent derivation of step 1 that agrees
with the note.

**Verdict: PASS.**  At `k = 3` this is a certificate-free proof of a case the
six-vertex theorem already covers.  It extends to every infinite field,
including characteristic two.

## 3. Version R countermodel (attack item 3)

Reviewer check R2 recomputes everything with independent code: plain Python
`Fraction`s, and a recursive perfect-matching enumerator of `K_4`, not
hard-coded matchings.

- `T_W = Delta` on all 81 words.
- `Omega_W` (both terms of the `{01, 23}` matching vanish) is all 80 words
  except `0000`.
- On `Omega_W`, `per(A_a) = W02 W13 + W03 W12 = [a constant]`, including
  `1111 -> 1` and `2222 -> 1`.
- `per(A_0000) = 0`.
- The cut tensor is `B00 = B11 = E11`, `B01 = B10 = E22`.

The definition of `Omega_W` mentions only `P`–`P` edges.  This is
sufficient: with `|P| = |Q|`, a matching with `j` edges inside `P` has
exactly `j` edges inside `Q`.

**Wording defect.**  "Version R with arbitrary (non-witness) inside blocks is
vacuous: all-ones inside blocks make `Omega_W` empty."  This is literally
true at `k = 2`, and for even `k`, where an all-inside matching exists.  For
odd `k`, every inside-using matching also uses a cross edge.  `Omega_W` then
depends on the cross blocks, and all-ones inside blocks need not empty it.
The intended point is that inside blocks and cross blocks can be chosen
together to empty `Omega_W`, so unrestricted Version R is trivially
satisfiable.  That is correct, but not as worded.

**Verdict: PASS** (countermodel exact; one wording defect).

## 4. The `k >= 5` "boundary of the mechanism" (attack item 4)

### 4.1 The claim is false

Note Section 6 states, as [PROVED], that if every block is invertible, then
for `|Q''| >= 3` generic full `w_{q''}` make the vectors `B_{pq''} w_{q''}`
span `F^3`, so the necessary condition "holds automatically", and Lemma C
excludes no all-invertible configuration.

The necessary condition quantifies over **all** full `w_{q''}`, not generic
ones.  Exhibiting generic `w` that satisfy it proves nothing.  Choose `delta`
first:

**Reviewer proposition (delta-first form of Lemma C).**  Let `F` be infinite,
assume Version N, and let `k >= 2`.  Fix `p in P` and distinct
`q, q' in Q`, and put `Q'' = Q - {q, q'}`.  Then for every full `delta` there
are `q'' in Q''` and a colour `c` with `B_{pq''}^T delta in F^× e_c`.

*Proof.*  Suppose instead that some full `delta` makes every
`v_{q''} = B_{pq''}^T delta` either `0` or not a multiple of a coordinate
vector.  By the hyperplane fact,
each `v_{q''}^⊥` contains a full `w_{q''}`.  Then
`delta^T B_{pq''} w_{q''} = v_{q''} . w_{q''} = 0` for all `q''`, and Lemma C
(with any full `u`) is contradicted.  ∎

**Consequence.**  Call `B` *single-column* if `B = b e_c^T` with `b != 0`.
Assume Version N over an infinite field and `k >= 3`.

- Every row `p` contains at least three single-column blocks.
- Dually, by transposes, every column `q` contains at least three
  *single-row* blocks `e_c b^T` with `b != 0`.

*Proof.*  Suppose row `p` has at most two single-column blocks.  Choose the
open pair `{q, q'}` to contain them.  For each closed `q''` with
`B = B_{pq''} != 0`, consider `S_c = (B^T)^{-1}(F e_c)`.  If `S_c = F^3`, then
`B` is single-column, which is excluded.  So every `S_c` is a proper
subspace.  Over an infinite field, a full `delta` avoids the finitely many
proper `S_c`.  For that `delta`, each `B_{pq''}^T delta` is `0` or lies on no
coordinate line, contradicting the proposition.  ∎

In particular:

- **Every all-invertible configuration is excluded by Lemma C at every
  `k >= 2`.**  More generally, so is every configuration with a row
  containing `k - 2` blocks that are not single-column, such as blocks of
  rank `>= 2`.
- At `k = 3` the consequence says that every block is single-column and
  single-row, hence single-entry.  This re-derives step 1 of the note.
- **The `k = 4` "allowed pair" is not allowed.**  The note offers "two
  rank-2 blocks with the same image plane containing some `e_c`" as an
  allowed closed pair.  Rank-2 blocks are not single-column, so the pair is
  excluded.  The note's generic span argument again ignores special full
  `w`.  The note's other `k = 4` statement (one invertible block forces the
  rest of its row to be single-entry) is proved with a correct for-all
  quantifier and is **correct**.

**Exact replay** (reviewer script, `Fraction` arithmetic).  For each case
below, the script constructs a full `delta`, full closed `w_{q''}` with every
junk term exactly `0`, and full `u`.  It then computes the contraction's
`3 x 3` coefficient matrix from the actual `k x k` permanents.

| case | contraction rank | contracted target rank |
|---|---|---|
| D1: `k = 5`, all 25 blocks random invertible | 2 | 3 |
| D3: `k = 4`, all blocks invertible | 2 | 3 |
| D3: `k = 6`, all blocks invertible | 2 | 3 |
| D2: `k = 4`, the note's two rank-2 closed blocks with common image plane `span(e_0, (0,1,1))` | 2 | 3 |

### 4.2 What survives

- **Lemma C does not exclude all-single-entry configurations at any
  `k >= 3`.**  For `B = beta E_cd` and full `delta`,
  `B^T delta = beta delta_c e_d in F^× e_d`.  So the hypothesis of Lemma C
  is never met, and Lemma C excludes nothing.
- Hence the headline "Lemma C alone closes `k <= 3` and not `k >= 4`" is
  still true.  The reason is combinatorial, not dimensional.  At `k = 3` the
  counting forces every block to be single-entry, and the Latin-square
  endgame closes.  At `k >= 4` the rank-one conditions leave room, and the
  single-entry `K_{k,k}` endgame is open.
- The explanation "`k - 2` junk terms, and three colours leave two
  dimensions to kill them" is wrong.  Each junk term can be killed by its
  own closed vector `w_{q''}`, whatever `k` is.
- The heuristic about several open vertices (slice rank `<= r` versus 3)
  is labelled heuristic.  As a heuristic it is unaffected.

**Verdict: FAIL** for the [PROVED] boundary claim and for the `k = 4`
"allowed pair" example.  The corrected statement is the reviewer
proposition above (proved here by hand and replayed on instances; not yet in
any verifier).

## 5. Unequal sides and the `n = 4` corollary (attack item 5)

- With no inside edges and `k != m`, a perfect matching of `P ∪ Q` would
  need a bijection `P -> Q`, so none exists and every value is `0`.  The
  constant words cannot be nonzero, so no version holds.  Trivially
  correct.
- Wording: "both sides are independent **at `a`**" makes the single value
  `T(a)` zero.  "The slice is identically 0" needs independence at every
  word, as in the bare cut-tensor setting.  Harmless.
- The formula for one independent side (a sum over injections with an
  inside hafnian on `Q - iota(P)`) is correct.
- **Corollary.**  Suppose `W_ij = 0`.  Put `i, j` on one side.  The matching
  `{ij, kl}` vanishes on every word, and `T_W(a)` equals the permanent of
  the `2 x 2` cut on all 81 words.  That is Version F at `k = 2`, which is
  impossible.  The argument applies to each of the six blocks by symmetry.
  It is consistent with the matrix-unit witness, whose six blocks are all
  nonzero.
- By Section 2.3, the corollary holds over every field, not only infinite
  fields.

**Verdict: PASS.**

## 6. Reproduction (attack item 6)

| run | command | result | elapsed |
|---|---|---|---|
| direct | `python claims/finite/n06/verify_bipartite_cut_tensor_rigidity_small_cuts.py` | ALL CHECKS PASSED (13 checks) | 7.3 s |
| direct | `python tools/explore/probe_bipartite_cut_tensor_least_squares.py --k 2 --trials 5 --seed 5` | 5/5 starts at residual `1.000000` | 1.2 s |
| `review-cut-gb-k2-20261009` | `run_bounded.py --timeout-seconds 1500 --memory-mb 4000 -- python tools/explore/groebner_bipartite_cut_tensor_k2.py` | `GB: [1] len 1`; status succeeded, exit 0 | 1055 s (the note records 738 s; the cause of the timing difference was not investigated, and the result is the same) |
| direct | reviewer scratch checks R1–R7 (Sections 1–3, 5) | all pass | < 1 s |
| direct | reviewer scratch check D1–D3 (Section 4) | all pass | < 5 s |

The reviewer scripts are not committed.  They are review aids, not
certificates.

### What the verifier checks

| check | note claim | what it does | comment |
|---|---|---|---|
| [1] | polynomial form | symbolic at `k = 2`; one random integer instance at `k = 3`, all 729 coefficients | `k = 3` is a sampled replay of a one-line multilinearity identity |
| [2] | Lemma C, `k = 2` | symbolic `det = 0` | correct; the second sub-check (`det diag = prod`) is tautological |
| [3] | Lemma C, `k = 3` | 25 random rational instances; rank `<= 2` and the explicit two-term split | `delta = v x z` is not checked to be full, so this replays the identity, not an instance of the Lemma C hypothesis.  The rank-3 target is not computed.  Both are fine for an identity replay |
| [4] | hyperplane fact | symbolic orthogonality of the two formulas | fullness for `t not in {0, -1}` is by inspection |
| [5] | `k = 3` endgame | 12 triples cover 9 edges; mixed word value is one monomial | exhaustive; matches the text |
| [6] | Version R | all 81 words | exhaustive; matches the text |

**Not checked by any verifier:**

- F ⟺ N;
- the single-entry forcing step (Zariski density; hand only);
- the `n = 4` corollary;
- all of Section 6, including the false boundary claim;
- the border remark.

The note's label convention ("[PROVED]: hand proof; displayed identities
replayed") is accurate for Sections 1–3.  The Section 6 [PROVED] items are
hand-only.

**Gröbner script.**  It encodes exactly the 81 Version F equations
`per(A_a) - [a constant]` in the 36 block entries over `Q` (grevlex).  A basis
`[1]` means that no solution exists over any field of characteristic zero,
since `1` lies in the ideal over `Q`.  So "over `Q-bar`" in the note is
understated.  It says nothing about positive characteristic; the hand proof
covers every field.  It is by the same author and replays the same
statement, so it is a second route, not an independent audit, as the note
says.

**Numerics.**  The `k = 2` figure of 26 starts and the `k = 4` run used
uncommitted scratch code ("an earlier scratch copy … same numerics").  The
`k = 4` row is therefore not reproducible from committed code.  It is a
single completed start and is labelled [NUMERICAL].  It is not
load-bearing.  A two-colour configuration with residual exactly `1` exists
at every `k`: two single-entry perfect matchings (colours 1 and 2) whose
union is a Hamiltonian `2k`-cycle.  Reviewer check R7 confirms this exactly
at `k = 2, 3, 4`.  So the numerical `1` is an upper bound that is attained.

## 7. "Version F is exactly the bipartite Krenn–Gu problem" (attack item 7)

Correct, with this scope:

- **Inside structure assumed.**  The inside blocks `W_pp'` and `W_qq'` are
  identically zero: no `P`–`P` or `Q`–`Q` edge in any colour pair, and no
  loops.  Then the perfect matchings of `P ∪ Q` are exactly the
  permutations `P -> Q`, and `T(a) = per(A_a)`.
- **Graph class.**  Cross blocks may be zero, so Version F at `k` is the
  Krenn–Gu question for every graph on `2k` vertices whose support across
  all colour pairs is bipartite with sides of size `k`.  Unbalanced
  bipartite supports have no perfect matching.  So "Version F for all `k`"
  is exactly "no bipartite GHZ(`2k`, 3) witness".
- **Colours and values.**  Three colours, with constant value `1` (or any
  nonzero values, by item 1).  A `d >= 3`-colour witness restricts to a
  3-colour witness, so the 3-colour case is the strongest.  The note does
  not say this, but it is consistent with it.
- **Field.**  Krenn–Gu is over `C`.  The note works over any infinite field.
- **Not covered.**  Version F is **not** the statement that a cut slice of
  a general witness is a permanent.  In a witness the inside is nonzero, and
  the slice equals `per(A_a)` only on `Omega_W`.  The note says this
  correctly in Sections 1, 7 and 8.  The summary table's phrase "the
  bipartite case of Krenn–Gu at order `2k >= 8`" should be read with the
  zero-inside assumption.
- **Novelty.**  "Open from `k = 4`" is a repository-internal assessment.  No
  literature search on bipartite (permanental) GHZ realizations is recorded
  under `docs/literature/provenance.md`.

**Verdict: PASS with scope wording.**

## 8. Gaps (attack item 8)

1. **False [PROVED] claim** (note Section 6, "Boundary of the mechanism at
   `k >= 5`").  Lemma C excludes every all-invertible configuration at every
   `k >= 2` (Section 4.1).  Its conclusion "Lemma C excludes no
   all-invertible configuration" must be withdrawn, and so must the
   dimension-count explanation ("`k - 2` junk terms, two dimensions").
2. **False example** (note Section 6, `k = 4`).  "Two rank-2 blocks with the
   same image plane containing some `e_c`" is not allowed by Lemma C.
3. **The summary sentence** "provably cannot by itself close `k >= 5`, for a
   dimension reason" (note Summary) rests on gap 1.  The true statement is
   that Lemma C is silent on all-single-entry configurations at every
   `k >= 3`, so it cannot close `k >= 4` without a combinatorial endgame.
4. **Unrecorded strengthening.**  Lemma C actually gives: at least three
   single-column blocks in every row and at least three single-row blocks
   in every column (Section 4.1).  This is a sharper necessary condition at
   every `k`.  It is not in the note, and no verifier replays it.  At
   `k = 4` it does not yet force single-entry blocks.  Finer pair
   conditions exist (for two single-column closed blocks `b3 e^T`,
   `b4 e^T`, no full vector may be orthogonal to both `b3` and `b4`).
   These were not worked out.
5. **`k = 4` is open** in every respect.  The rank-one case analysis and the
   weighted single-entry `K_{4,4}` endgame, where mixed monomials can
   cancel, are not done.  The note says so.
6. **Field scope understated.**  The `k = 2` Theorem and the `n = 4`
   corollary hold over every field.  The Gröbner basis covers every field of
   characteristic zero, not only `Q-bar`.  The `k = 3` proof needs an
   infinite field (density), as stated.
7. **Version R wording.**  "All-ones inside blocks make `Omega_W` empty"
   is false for odd `k` without a condition on the cross blocks
   (Section 3).
8. **Border statement.**  "Not even a border point" is proved at `k = 2` by
   the reviewer remark (residual `>= 1/3`).  It is unproved at `k = 3` and
   `k = 4`, where the note's numerical evidence is only local optimisation
   from random starts.
9. **Reproducibility.**  The `k = 4` numerical run and 6 of the 26 `k = 2`
   starts came from uncommitted scratch code.
10. **Verifier coverage.**  F ⟺ N, single-entry forcing, the `n = 4`
    corollary, and all of Section 6 are hand-only (Section 6 table).  The
    verifier sits in `claims/finite/n06/`, but no `n06` claim document
    references it.  Its owner is a strategy note.
11. **Gluing.**  No occurrence theorem supplies Version F's full-word
    premise for a cut slice of a witness at any `n >= 6`.  The proposed
    "two-of-three transfer" is unformulated.  The note says so.
12. **Evidence status.**  Primary verifier plus this same-day agent review
    only.  The Gröbner run is a second route by the same author.  No
    independent audit, no Lean formalization, and no literature provenance
    for the "open" status of bipartite `k >= 4`.

## Scope

The `k = 2` and `k = 3` impossibility of Version F/N, Lemma C itself, the
F ⟺ N equivalence, the `n = 4` all-blocks-nonzero corollary, and the Version
R countermodel are correct.  The `k = 2` parts hold over every field.  The
strategy note's Section 6 contains one false [PROVED] claim (all-invertible
vacuity at `k >= 5`) and one false example (the `k = 4` rank-2 pair).  Both
come from replacing "for all full `w`" with "for generic full `w`".  The
corrected statement makes Lemma C stronger than the note says, not weaker.

None of this closes an order, creates a reduction edge, or changes
`docs/current-frontier.md` or the global **UNRESOLVED** status.  The
`k = 3` case lies inside the proved six-vertex exclusion, and `k = 2` is at
`n = 4`.  The corrected Lemma C remains a conditional implication whose
full-word premise no occurrence theorem supplies in a witness.
