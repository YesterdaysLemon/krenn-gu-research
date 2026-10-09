# Cut-tensor (bipartite slice) rigidity — attempt record, 2026-10-09

Dated research record.  The global Krenn–Gu status is **UNRESOLVED**.
`docs/current-frontier.md` is not edited (see the last section).

Evidence labels:

- **[PROVED]**: a hand proof given here.  The displayed identities and
  finite facts are replayed by
  `claims/finite/n06/verify_bipartite_cut_tensor_rigidity_small_cuts.py`
  (primary verifier only; no independent audit, no Lean).
- **[EXACT]**: an exact computation by that script.
- **[NUMERICAL]**: floating-point least squares
  (`tools/explore/probe_bipartite_cut_tensor_least_squares.py`); evidence
  only, never a proof.
- **[OBSERVATION]**: a reading of committed documents.

Inputs: the trunk record, the row-space note, the multilinear-certificate
note, `THREE_COLUMN_BILINEAR_GRID_THEOREM.md` with its 2026-10-08 review, and
Section 5 of the holonomy note.

## Summary

| version of the target | `\|P\| = \|Q\| = 2` | `\|P\| = \|Q\| = 3` | `\|P\| = \|Q\| >= 4` | `\|P\| != \|Q\|` |
|---|---|---|---|---|
| F/N: all `3^{2k}` words | **impossible** [PROVED] | **impossible** [PROVED] | **open** (the bipartite case of Krenn–Gu at order `2k >= 8`); residual 1 [NUMERICAL, k = 4] | trivially impossible (no cross perfect matching) |
| R: only the words where the inside is killed | **false**: exact countermodel, the `n = 4` matrix-unit witness | vacuous on witnesses (six-vertex theorem) | — | — |

The mechanism is a **one-vertex contraction rank bound** (Lemma C):
contracting one vertex with a full vector turns the target into a rank-3
diagonal bilinear form, while the permanent has only two terms that survive
a suitable contraction, so it has rank at most 2.  This is the bipartite
analogue of the full-row lemma of Theorem 3 in the bilinear-grid document,
and its last step is Theorem 3(b).  It needs no certificate, but it uses
every word.  It closes `k <= 3`, gives only partial constraints at
`k = 4`, and provably cannot by itself close `k >= 5`, for a dimension
reason (Section 6).

## 1. Exact statements

Let `P, Q` be disjoint vertex sets, `|P| = k`, `|Q| = m`, and let
`B_pq in F^{3x3}` (`p in P`, `q in Q`) be arbitrary (the *cut tensor*).  For a
colouring `a` of `P ∪ Q` put `A_a[p, q] = B_pq[a_p, a_q]`.  `F` is an
infinite field (for example `C`); characteristic two is allowed.

- **Version F (full words, value 1).**  For every `a in [3]^{P ∪ Q}`:
  `per(A_a) = 1` if `a` is constant and `0` otherwise.
- **Version N (full words, "nonzero").**  `per(A_a) = 0` for every mixed
  `a`, and `per(A_c) != 0` for the three constant words.
- **Version R (restricted words).**  Inside blocks `W_pp'`, `W_qq'` are also
  given, and `Omega_W` is the set of words at which every perfect matching of
  `P ∪ Q` that uses a `P`–`P` edge vanishes.  On `Omega_W` the hafnian equals
  `per(A_a)`, and the hypothesis is `per(A_a) = Delta(a)` for `a in Omega_W`
  only.  (With a pinned outside, the inside factor is a fixed scalar; the
  same discussion applies.)

**Unequal sides.**  If `k != m` and both sides are independent at `a`, no
perfect matching of `P ∪ Q` exists, the slice is identically `0`, and none of
the versions can hold.  (For `|P| = 2`, `|Q| = 3` the vertex count is odd.)
If only `P` is independent, the slice is
`sum_iota prod_p B_{p iota(p)} * haf(W on Q - iota(P))`: an inside factor
that depends on the injection `iota`.  That is the gluing situation of
Section 8, not a permanent.  Everything below has `k = m`.

**[PROVED] F ⟺ N.**  F implies N.  Conversely, replacing `B_pq` by
`diag(per(A_0), per(A_1), per(A_2))^{-1} B_pq` for one fixed `p` and all `q`
multiplies `per(A_a)` by `per(A_{a_p})^{-1}`.  This leaves mixed values zero
and makes the constant values `1`.  So "the constant value `1` may be
unachievable" is not an issue: N is the right statement and is equivalent.

**[PROVED] Polynomial form.**  With vector variables `x_p, y_q in F^3` and
`M(x, y)[p, q] = x_p^T B_pq y_q`,

```text
per M(x, y) = sum_a ( prod_p x_{p, a_p} prod_q y_{q, a_q} ) per(A_a),
```

because each term of the permanent uses every row and column exactly once.
So N says `per M(x, y) = sum_c lambda_c prod_p x_{p,c} prod_q y_{q,c}` with all
`lambda_c != 0`, a weighted GHZ tensor.  Version F is therefore exactly the
Krenn–Gu question for the complete bipartite graph `K_{k,k}` with arbitrary
complex `3 x 3` edge blocks.  [EXACT] check [1] replays the identity (symbolic
at `k = 2`, all 729 coefficients at `k = 3`).

## 2. Lemma C (one-vertex contraction), every `k >= 2` — [PROVED]

**Lemma C.**  Assume N.  Fix `p in P`, distinct `q, q' in Q`, and full vectors
(no zero coordinate) `u_{p'}` for `p' in P - p` and `w_{q''}` for
`q'' in Q'' = Q - {q, q'}`.  Then no full `delta` satisfies
`delta^T B_{pq''} w_{q''} = 0` for every `q'' in Q''`.

*Proof.*  Substitute `x_p = delta`, `x_{p'} = u_{p'}`, `y_{q''} = w_{q''}`, and
leave `y = y_q`, `y' = y_{q'}` free.  Group the permutations by the partner of
`p`:

```text
F(y, y') = (delta^T B_pq y) l(y') + (delta^T B_pq' y') l'(y)
         + sum_{q'' in Q''} (delta^T B_pq'' w_q'') N_q''(y, y'),
```

where `l`, `l'` are linear forms (the other open vertex is matched to a
closed `P` vertex) and `N_q''` are bilinear forms.  Under the hypothesis on
`delta`, the last sum vanishes and `F` is a bilinear form of rank `<= 2`.  The
target contracts to `sum_c lambda_c delta_c prod_{p'} u_{p',c}
prod_{q''} w_{q'',c} y_c y'_c`, a diagonal bilinear form of rank `3`.  ∎

[EXACT] Checks [2] and [3] replay the split: symbolically at `k = 2`
(`det = 0` identically), and at `k = 3` on 25 random rational instances.  At
`k = 3` the replay checks the explicit two-term decomposition, not only the
rank.

**Hyperplane fact** (Theorem 3(b) of the bilinear-grid document, in a
characteristic-free form).  For `v in F^3`, the hyperplane `v^⊥` contains a full
vector unless `v` is a nonzero multiple of a coordinate vector `e_c`.  Proof:
if `v = 0` every full vector works.  Otherwise, if `v^⊥` is not a coordinate
plane, it is not the union of its three proper subspaces `v^⊥ ∩ H_c` (an
infinite field).  Explicit vectors are in check [4].

## 3. Theorem (two- and three-vertex sides) — [PROVED]

**Theorem.**  Over an infinite field, no cut tensor with `|P| = |Q| = 2` or
`|P| = |Q| = 3` satisfies Version N (equivalently F).

*Proof for `k = 2`.*  `Q'' = ∅`, so Lemma C applies with any full `delta`.  ∎

*Proof for `k = 3`.*

1. **Single-entry forcing.**  Fix `p`, `q''`, and let `B = B_pq''`.  By
   Lemma C and the hyperplane fact, `Bw` is a nonzero multiple of a
   coordinate vector for every full `w`.
   - The full vectors are Zariski dense, so `B(F^3)` lies in the union of
     the three coordinate lines.  Being a subspace, it lies in one line
     `F e_c`, and `B != 0`.  So `B = e_c b^T`.
   - `b . w != 0` for every full `w`.  If `b` had two nonzero coordinates,
     some full `w` would satisfy `b . w = 0`.  So `b = beta e_d`.

   Since `p` and `q''` are arbitrary, **every block is a nonzero
   single-entry matrix** `beta_pq E_{c_pq d_pq}`.
2. **Colour classes.**  `per(A_c) != 0` gives a permutation `sigma_c` whose
   three edges all have type `(c, c)`.  An edge has one type, so
   `sigma_0, sigma_1, sigma_2` are pairwise edge-disjoint.  They therefore
   cover all nine edges of `K_{3,3}` ([EXACT] check [5]: all 12 such ordered
   triples).  Every edge type is diagonal, and `L(p, q) = c_pq = d_pq` is a
   Latin square.
3. **A surviving mixed word.**  Take `sigma` outside `{sigma_c}` and let
   `a_sigma` give each vertex the colour of its `sigma`-edge.
   - This word is mixed: otherwise all edges of `sigma` would lie in one
     class, forcing `sigma = sigma_c`.
   - Any `sigma'` contributing to `per(A_{a_sigma})` needs
     `L(p, sigma' p) = L(p, sigma p)` for every `p`, so `sigma' = sigma`.
   - Hence `per(A_{a_sigma}) = prod_p beta_{p sigma p} != 0`, a
     contradiction.  ([EXACT] check [5] replays this for every Latin square
     and every such `sigma`.)  ∎

**Scope.**  At `k = 3` this is the bipartite special case of the six-vertex
exclusion, which the repository already proves by certificate.  The new
content is a conceptual, certificate-free proof, and Lemma C, which is
valid at every `k`.

**[PROVED] Corollary at `n = 4`.**  Every four-vertex witness, over any
infinite field, has all six blocks nonzero.  Suppose instead that, say,
`W01 = 0`.  Then the matching `{01, 23}` vanishes on every word, so
`T_W(a) = per(A_a)` for the cut `P = {0, 1}`, `Q = {2, 3}` on all 81 words.
That is Version F at `k = 2`, which is impossible.

## 4. Exact and numerical tests

- [EXACT] Verifier: all checks pass (about 6 s).
- [EXACT] A direct SymPy Gröbner basis (grevlex over `Q`) of the 81 Version F
  equations in 36 unknowns at `k = 2` is `[1]` (run `cut-gb-k2-a`, 738 s).
  This is a second exact check by a different route (elimination, no
  saturation, no use of Lemma C), by the same author, so it is not an
  independent audit.  It confirms Version F at `k = 2` over `Q-bar`.  No
  Gröbner computation was attempted at `k = 3` (81 unknowns, 729
  equations).
- [NUMERICAL] Levenberg–Marquardt over complex blocks, minimizing the
  residual norm of all `3^{2k}` word equations:

  | k | starts | best residual norm |
  |---|---|---|
  | 2 | 26 | `1.000000` (every start) |
  | 3 | 18 | `1.000000` (every start) |
  | 4 | 1 completed (run stopped at its 900 s bound during the second start) | `1.000` |

  A residual of exactly `1` is what a two-colour configuration attains:
  all mixed words `0`, two constant words `1`, the third `0`.  At
  `k = 2, 3` this is consistent with the Theorem.  At `k = 4` it is
  evidence, not proof, that Version N fails and that the true minimum is
  two-of-three.  It also suggests that GHZ is not even a border point of
  bipartite permanental tensors, in contrast to general hafnian tensors
  (border realizability at every even `n`).
- **Questions answered.**  Do the equations force the matrix-unit shape?  At
  `k = 2, 3` there is no solution at all, so the claimed first half
  ("monochromatic matrix-unit configuration") is vacuous there.  The proof
  passes through it: at `k = 3`, Version N forces single-entry blocks with a
  Latin-square diagonal type, which is exactly the monochromatic matrix-unit
  shape, and then fails.

## 5. Relation to Theorems 2 and 3 of the bilinear-grid document — [OBSERVATION]

- **They are not the `|P| = 2` cases.**  Both live on the `|P| = |Q| = 3`
  cut of the six-vertex inner/outer triangle, restricted to the 27 words with
  the outer side pinned to an injective `sigma`.  All those words are mixed,
  so they conclude vanishing (plane rigidity, or the hollow-grid certificate),
  never a contradiction with constant words.
  - Theorem 3 is the restriction of Version F with `Q` frozen.
  - Theorem 2 freezes one more inner vertex at its full row.
- **Shared mechanism.**
  - Theorem 3(a) is a rank statement: a full `x` makes `perm(x, ·, ·)`
    nondegenerate.  Lemma C is the matching statement for the bipartite
    contraction.
  - The last step of both is the hyperplane fact, Theorem 3(b).
  - The difference is the source of rank 3.  In Theorem 3 it comes from the
    hollow determinant `2 x1 x2 x3`.  Here it comes from the target: a
    contracted GHZ is diagonal of full rank.
- **The two-vertex analogue.**  The `|P| = 2` case of this note is the
  four-cycle.  Its two permutations are the rank-two (two-matching)
  situation of Theorem A in `TWO_TERM_RELATION_CLOSURE_THEOREMS.md`, here
  with all words available.

## 6. Where the mechanism stops (`k >= 4`)

- **[PROVED] Necessary conditions at every `k`.**  By Lemma C and the
  hyperplane fact, a Version-N cut tensor satisfies the following.  For every
  `p`, every `(k-2)`-set `Q''` and all full `w_{q''}`, the span of the
  vectors `B_{pq''} w_{q''}` contains a coordinate vector.  The same holds on
  the `Q` side, with transposes.
- **[PROVED] At `k = 4`** (two closed columns) this is a genuine pair
  constraint.  For example, if one block `B_pq` is invertible, every other
  block in row `p` (and, by the transpose, in column `q`) is single-entry.
  - *Proof:* take `Q'' = {q, q4}` and fix a full `w4`; put
    `v4 = B_pq4 w4`.
  - The image of the full vectors under `B_pq` is dense in `F^3`.
  - If `v4 = 0`, a generic `v = B_pq w` spans a non-coordinate line.
  - If `v4` is not a multiple of a coordinate vector, a generic `v` lies
    outside the three planes `span(v4, e_c)`.
  - In both cases `span(v, v4)` contains no `e_c`, which the necessary
    condition forbids.  So `B_pq4 w4` is a nonzero multiple of a
    coordinate vector for every full `w4`.
  - The single-entry argument of Section 3 then applies.

  Other pairs are allowed, for example two rank-2 blocks with the same
  image plane containing some `e_c`.  The `k = 4` case analysis and its
  combinatorial endgame (weighted single-entry `K_{4,4}`, where mixed
  monomials can cancel) were not completed.
- **[PROVED] Boundary of the mechanism at `k >= 5`.**  Suppose every block
  is invertible.  Then, for every `p` and every `Q''` with `|Q''| >= 3`,
  generic full `w_{q''}` make the vectors `B_{pq''} w_{q''}` span `F^3`.  The
  same holds on the `Q` side.  So the necessary condition holds
  automatically, and Lemma C excludes no all-invertible configuration.
  - A one-vertex contraction has `k - 2` junk terms, and three colours
    leave two dimensions to kill them.  This is the exact reason the
    argument closes only `k <= 3`.
  - [OBSERVATION, heuristic] More open vertices do not help in the obvious
    way.  With `p` and `r` open `Q` vertices, the contraction is a sum of
    `r` terms, each of slice rank one in some factor.  A full `GHZ_r` has
    slice rank 3, so this gives no contradiction for `r >= 3`.
- **[OBSERVATION]** Version F at `k >= 4` contains the bipartite all-diagonal
  case (all blocks diagonal).  For general graphs the analogous all-diagonal
  question, the open `(AP')`/weighted-Bogdanov leaves `WB1`/`WB2`, is open.
  So a proof for all `k` would at least settle a bipartite weighted-Bogdanov
  statement.  It is not a routine extension.

## 7. Version R is false as stated — exact countermodel [EXACT]

The `n = 4` matrix-unit witness: `W01 = W23 = E00`, `W02 = W13 = E11`,
`W03 = W12 = E22`, with cut `P = {0, 1}`, `Q = {2, 3}`.

- `T_W = Delta` on all 81 words.
- `Omega_W` (words with `W01[a0,a1] W23[a2,a3] = 0`) is every word except
  `0000`.
- On `Omega_W`, `per(A_a) = [a constant]`, including the constant words
  `1111` and `2222`.

So the cut tensor `{E11, E11, E22, E22}` satisfies Version R with
`|P| = |Q| = 2`.  It *is* a monochromatic matrix-unit configuration, which
matches the first half of the claim, but the second half ("impossible")
fails.  The excluded word is a constant word, and there `per(A_0000) = 0`:
exactly the two-of-three configuration that the numerics converge to.  So the
`n = 4` witness is a bipartite two-colour slice glued to a one-colour inside.
This is the prototype of what the gluing step has to exclude at `n >= 6`.

Version R with arbitrary (non-witness) inside blocks is vacuous: all-ones
inside blocks make `Omega_W` empty.

## 8. What remains for an all-`n` proof (the `GL` node)

1. **The full-word theorem at every `k`** (bipartite Krenn–Gu): open from
   `k = 4`.  Lemma C closes `k <= 3` and provably cannot close `k >= 5`
   alone (Section 6).  The next lemma would be a contraction that kills
   `k - 2` junk terms, or a non-rank invariant separating GHZ from
   bipartite permanental tensors.  The numerics suggest the separation is
   closed (residual exactly 1), so a polynomial invariant may exist.
2. **Gluing.**  In a witness, the slice is a permanent only on `Omega_W`.
   - Off `Omega_W`, matchings with equal numbers of `P`–`P` and `Q`–`Q`
     edges contribute, and the inside factor is not 1.
   - Lemma C contracts every vertex with a full vector, so it uses every
     word; it does not survive restriction to `Omega_W`.
   - Section 7 shows the restriction is fatal in general: one constant
     word may be lost.

   The sharpest gluing statement suggested here is a "two-of-three
   transfer": if a cut slice of a witness vanishes on all mixed words of
   `Omega_W`, then the constant word it loses must be carried by
   inside-matching terms.  At `n >= 6` this would need an occurrence
   theorem; none is proved.

## Frontier

No frontier change.

- The Theorem closes no order: `k = 3` is inside the proved six-vertex
  exclusion, and `k = 2` is at `n = 4`.
- Lemma C is a conditional implication valid at every `k`, with no
  occurrence theorem supplying its full-word premise in a witness.
- Version R is refuted only as a standalone local statement.  No
  repository route depended on it.

## Commands

```text
python claims/finite/n06/verify_bipartite_cut_tensor_rigidity_small_cuts.py      # ~6 s
python tools/explore/probe_bipartite_cut_tensor_least_squares.py --k 2 --trials 20 --seed 5
python tools/research/run_bounded.py --run-id <id> --timeout-seconds 600 --memory-mb 3000 -- \
  python tools/explore/probe_bipartite_cut_tensor_least_squares.py --k 3 --trials 15 --seed 7
python tools/research/run_bounded.py --run-id <id> --timeout-seconds 900 --memory-mb 4000 -- \
  python tools/explore/probe_bipartite_cut_tensor_least_squares.py --k 4 --trials 4 --seed 1
```

```text
python tools/research/run_bounded.py --run-id <id> --timeout-seconds 1200 --memory-mb 4000 -- \
  python tools/explore/groebner_bipartite_cut_tensor_k2.py                         # GB [1], ~740 s
```

Recorded runs:

| run id | result |
|---|---|
| `cutnum-k3-b` | 15/15 starts at `1.000000` |
| `cutnum-k4-a` | one start completed at `1.000`; timed out (exit 124) during the second; run from an earlier scratch copy of the probe with the same numerics |
| `cut-gb-k2-a` | `[1]`, 737.7 s |

The `k = 2` figure of 26 starts combines 20 starts of the committed probe
and 6 scratch starts.
