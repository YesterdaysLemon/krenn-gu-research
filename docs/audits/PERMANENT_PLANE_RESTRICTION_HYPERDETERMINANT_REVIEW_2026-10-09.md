# Adversarial review: permanent plane-restriction hyperdeterminant theorem and the plane-rigidity clause family

Date: 2026-10-09

Review type: **same-day agent review**.  A separate agent session in its own
worktree was briefed adversarially.  This is not independent human
refereeing, not an independent re-derivation by a different research group,
and not formal kernel verification.  No Lean counterpart exists.

Global Krenn–Gu status: **UNRESOLVED** (unchanged by this review).

Reviewed objects (commit `c585e467827c1638332c784fb59c5345bb64dc0b`, branch
`origin/claude/hyperdeterminant-20261009`; git blob ids):

| file | blob |
|---|---|
| `claims/arbitrary-order/PERMANENT_PLANE_RESTRICTION_HYPERDETERMINANT_THEOREM.md` | `55822adb2c009c8077d82625426f3915c67e02c2` |
| `claims/arbitrary-order/verify_permanent_plane_restriction_hyperdeterminant_theorem.py` | `8ba80345a991ba35af1d5cdd6f1160d5a66301d3` |
| `docs/strategy/hyperdeterminant-crossing-2026-10-09.md` | `cc0f0dae91df5c4dfc86c467668794d05ce73ad8` |
| `claims/finite/n08/explore_general_block_recursive_support_model.py` (`--plane-rigidity`, `check_plane`) | `ff47d417fec7814791deed75d3d62432e3659e1f` |
| `claims/arbitrary-order/THREE_COLUMN_BILINEAR_GRID_THEOREM.md` (input) | `aaf3bbec0f4991852d5d42e504285fc084da270c` |
| `tests/fixtures/bl_full_word_survivor_n6_51.json` (input) | `f72d7dc3b7b39b2a636c3755998db32b3870b1f7` |

The reviewed documents and the script were not edited.  The reviewer's
scripts are scratch files, not committed; Section 8 lists what each one
does so that it can be rewritten.

## Summary verdict

| item | verdict |
|---|---|
| (a) Soundness of the plane-rigidity rule (PR), modes `value` and `deg3` | **PASS.**  Every PR clause is satisfied by the exact zero pattern of **every** complex configuration (witness or not), at every even order and every level `\|A\| >= 6`.  Hand proof re-derived; the load-bearing rigidity step re-proved by a second route (chart-wise Gröbner bases, unit ideal in all 24 non-coaxial charts).  Independent exact random test: 0 violations.  New: at the support level the `value` and `deg3` premises are **equivalent** (proof and exhaustive check), so the radical-level case never arises for PR |
| (b) Theorem 1, Theorem 2, Corollaries 3–4 | **PASS.**  All quantitative claims recomputed with independent code: polarization identity over `Z`; `dim J_3 = 22`, kernel exactly `S`; completeness ranks 208/213/22; `F` (21 terms) equals Cayley's `Det`, both alternative forms, symmetry, irreducibility ingredients, special values, `F in (J_3)`; Corollary 4 (iii) exhaustively.  One cosmetic verifier-message inaccuracy |
| (c) Symmetry block | **PASS.**  Distinct generator namespaces (four at `n = 6`, five at `n = 8`); the isolated block accepts exactly the per-generator lex-leaders (0 mismatches over 7,154 orbit members at `n = 6` and 3,142 at `n = 8`) and every orbit keeps a member |
| (d) Reproduction | **REPRODUCED.**  Verifier ALL PASS (2.6 s); BL51, P41, P63 refuted by PR alone (also `deg3`, also top-only for BL51); P27 SAT with PR, UNSAT with H2/H3; `n = 4` SAT, checker PASS; `n = 6` killers + H2 + H3 + PR under `run_bounded.py`: **UNSAT**, 161.6 s, 77 rounds, 322,856 lazy instances (576 PR, all level 6), identical counts to the note.  With **no lex-leader clauses** (chain normalization only) the run is still UNSAT (1,065 s, 292 rounds); fully symmetry-free runs were inconclusive at 3,600 s |
| (e) `n = 8` models, gluing, OCC-PR | **PASS with wording notes.**  Both printed `n = 8` supports admit `m`-assignments passing `check_model`, `check_plane` (all levels) and, for the 156-entry one, top-level `check_holonomy`; the reviewer's own PR predicate finds 0 violations on both.  OCC-PR is correctly described as equivalent to the exclusion it would give.  Two imprecisions (Section 6) |
| (f) Gaps | Section 7 |

No exact counterexample to the Krenn–Gu conjecture appeared.  No order is
closed by anything reviewed here: the `n = 6` UNSAT concerns an order already
excluded by other means, and it carries no DRAT certificate.

## 1. Item (a): soundness of PR

### 1.1 Exact statement reviewed

Notation of the strategy note, Section 3.  `A` even with `|A| >= 6`;
`T = (t_0, t_1, t_2) subset A`; `R = A - T`; `c` a word on `R`; a 3-set
`C subset R`; colour pairs `alpha_t != alpha'_t` (one of `PAIRS`) at each
`t`; the eight cube words `w_ijk` (colour `alpha_t` or `alpha'_t` at `t`,
`c` on `R`).  For a configuration `W`, `g` and `m` are the **exact** zero
patterns: `g[t,u,a,b]` iff `W_tu[a,b] != 0`, `m[B,v]` iff `T_B(v) != 0`
(`m[{},()]` true, `m` on a pair equal to `g`).

Premises:

1. `m[R - C, c]`.
2. For every cube word: every injection `T -> R` (ordered image `img`, as a
   set different from `C`) has a false factor among the three entries
   `g[t_k, img_k, w_{t_k}, c]` and `m[R - img, c]`; and for every inner pair
   `{t_i, t_j}`, either `g[t_i t_j]` at the cube colours is false, or for
   every `u in R`, `g[t_k u]` or `m[R - u, c]` is false.
3. With `y, y'` the rows of `t` at `alpha_t, alpha'_t` restricted to `C`
   (in the order of `C`) and `l_t[a] = y_b y'_d - y_d y'_b`
   (`b, d = a+1, a+2 mod 3`), let
   `K_t = {a : exactly one of the two products has both factors supported}`
   and `Z_t = {a : neither product has both factors supported}`.
   - mode `value`: some `(a_0, a_1, a_2) in K_0 x K_1 x K_2` is not
     all-equal;
   - mode `deg3`: such a tuple is two-equal, or is a permutation `s` with a
     same-parity `s' != s` and some `t` with `s'_t in Z_t`.

Conclusion: `m[A, w_ijk]` for some cube word.

This is exactly what `GSM._plane_clause` / `_plane_choice` encode (read in
full) and what `check_plane` re-evaluates.  In particular the code demands a
zero factor for each **ordered** injection, which is stronger than needed
(the six injections onto one image could cancel inside a permanent) and
therefore sound.  The encoder's clause literals are exactly the false
literals witnessing premises 1–3 plus the eight cube `m`-literals.

### 1.2 Proof check

- **T-expansion (3.1).**  A perfect matching of `A` either matches `T`
  injectively into `R` or contains exactly one `T`–`T` edge (`|T| = 3` is
  odd).  Each matching is counted once.  Correct.  Reviewer check: 5.9
  million exact tests of `T_A(w) = h * perm(rows on C)` on instances where
  premises 1–2 hold, 0 failures (Section 1.4).
- **Reduction.**  A false `g`/`m` literal is an exactly zero factor, so
  premise 2 kills every summand except the injections onto `C`, whose sum
  is `h * perm(Y_0[:,i], Y_1[:,j], Y_2[:,k])` with `h = T_{R-C}(c) != 0`.
  If all eight words vanish, the cube tensor of `(Y_0, Y_1, Y_2)` vanishes.
- **Minors.**  `a in K_t` gives `l_t[a] != 0` (one nonzero monomial,
  the other product exactly zero), so `l_t != 0`.
- **Rigidity.**  Corollary 3 gives a common axis `e_u` for all `l_t`, so
  `l_t[a_t] != 0` forces `a_t = u` for all `t`, contradicting premise 3.

The GHZ condition is not used; witnesses enter only through `(G)`.  The
argument is valid over `C` for every configuration `W` at every even order
and every level.  **PASS.**

**Second route for the rigidity step (reviewer, `gb_chart.py`).**  The proof
rests entirely on "cube = 0 and every `l_t[a_t] != 0` with the `a_t` not all
equal is impossible".  Independently of `J_3`, the polarization identity
and Corollary 3: if `l_t[a] != 0`, right multiplication by a `GL_2` matrix
(which preserves `V_t` and maps the cube to `(g_0 x g_1 x g_2) . A`, so
preserves its vanishing) normalizes `Y_t` to rows `b, d` equal to `I_2` and
row `a` equal to `(p_t, q_t)`.  For each of the 27 charts `(a_0, a_1, a_2)`
the reduced Gröbner basis over `Q` of the eight cube permanents in
`Q[p_0, q_0, p_1, q_1, p_2, q_2]` is:

- `[1]` for all **24** charts with the `a_t` not all equal;
- `[p_0, q_0, p_1, q_1, p_2, q_2]` for the 3 all-equal charts (the only
  zero is `V_0 = V_1 = V_2 = H_a`).

So in characteristic zero the PR conclusion follows with no use of the
theorem document, and even a chart-local degree certificate exists.

### 1.3 Mode `deg3`

- Every `deg3` clause is the `value` clause for a not-all-equal tuple, plus
  extra literals that are false in the model (the identically zero minor of
  `s'`).  It is a weakening of a `value` clause, hence sound whenever
  `value` is.  It is also sound on its own: a two-equal monomial lies in
  `I` (Proposition 4); for a permutation, `P_s - P_s' in I` and `P_s'`
  vanishes identically on the support.
- **New: the two modes fire on exactly the same instances, at every order.**
  Proof.  Suppose a not-all-equal tuple exists but none is two-equal.  Some
  tuple is then a permutation `s`.  If some `|K_t| >= 2`, replacing `s_t` by
  another element of `K_t` gives a two-equal tuple, so every `K_t = {s_t}`.
  Fix `t` and write `a = s_t`, `b, d` for the other two indices.  If
  neither other minor were identically zero, both would have both products
  supported (they are not in `K_t`).  `l_t[b]` involves
  `y_d, y'_a, y_a, y'_d` and `l_t[d]` involves `y_a, y'_b, y_b, y'_a`, so
  `y_b, y_d, y'_b, y'_d` would all be supported, and `l_t[a]` would have
  both products supported, contradicting `a in K_t`.  So some
  `x_t != s_t` lies in `Z_t`.  The two same-parity
  permutations `s' != s` differ from `s` in every position and take the two
  values other than `s_t` at position `t`, so one of them has
  `s'_t = x_t`.  QED.
- Reviewer exhaustive check (`value_vs_deg3.py`): over all `64^3` support
  triples (15 distinct `(K_t, Z_t)` patterns per vertex, 3,375 pattern
  triples), `value` fires on 997, `deg3` on 997, `value and not deg3` on 0;
  the repository's `_plane_choice` agrees with the reviewer's predicate on
  all 3,375 in both modes.

Consequence.  The note's sentence "the `deg3` run matches the `value` run
instance for instance ... the radical-level (exponent 2) case is never
needed" is true, but it is **forced** at every order and every level, not
an `n = 6` observation.  Corollary 4 (iii)'s residual permutation case
(no same-parity zero partner) can occur for a fixed `mu = P_s`, but then
another single-monomial tuple is two-equal.  This strengthens the note.

### 1.4 Independent exact random test (`pr_soundness.py`)

Written from the statement above, not from `check_plane`.  Random integer
configurations, five generators of zero patterns (sparse `{0, +-1, +-2}` at
densities 0.2–0.5; `{0, +-1}` at 0.3–0.7; rank-one blocks with zero
coordinates, which force many cancellations; single-column "killer-like"
blocks; and a planted mode that zeroes most entries of three inner
vertices in one outer column, to push minors onto a common axis).  Every
`T_A(w)` is computed exactly by Laplace recursion; the zero pattern is used
as `(g, m)`.  For every instance with premises 1–2, the exact identity
`T_A(w) = h * perm` is tested on a random fraction of instances.

| order | configs | premise 1–2 instances | expansion tests (failures) | `value` fires | `deg3` fires | fires with zero cube (violations) | zero cube, premises 1–2, minors fail |
|---|---|---|---|---|---|---|---|
| 6 | 600 | 3,684,316 | 5,894,336 (0) | 146,588 | 146,588 | **0** | 2,278,178 |
| 8 | 10 | 3,481,996 | 297,160 (0) | 89,501 | 89,501 | **0** | 2,507,013 |

The `n = 8` rows cover both levels `|A| = 6` and `|A| = 8` (runs
`rev-pr-sound-n8-1..3` with three configurations each, plus one timing
run).

Premise 3 cannot fire on a zero cube if the theorem is true, so the
violation count is a test of the implementation and of the reduction; the
proof is Section 1.2.  The large last column shows that zero cubes with
premises 1–2 are common and are stopped exactly at the minors.

**Encoder/checker agreement.**  On the BL51 support with an `m`-assignment
solved without PR (`fixed_g_driver.py ... nopr`), the reviewer's predicate
finds exactly 8 violated instances (all `A = V`, `T = {0,2,3}`,
`c = (2,0,1)` on `{1,4,5}`, `C = {1,4,5}`), the same number the encoder
adds in the BL51 refutation.  On the `n = 6` killers + PR SAT model (63
entries) it finds 0 violations and 1,162 zero cubes stopped at the minors,
equal to `check_plane`'s `some_vertex_without_single_monomial_minor` count.

## 2. Item (b): the theorem document

Reviewer recomputation with separate code (`thm_checks.py`,
`cor4iii.py`; SymPy and python-flint, exact):

| claim | result |
|---|---|
| Theorem 2 (a) polarization identity, all 27 `r`, over `Z` | 0 failures |
| shapes: `Phi_(a,a,a) = 0`; two-equal `r`: sum of two two-equal monomials; permutation `r`: same-parity difference | all 27 confirmed |
| Theorem 2 (b): rank of the 27 forms | 22 over `Q`, 22 over `F_3`, 16 over `F_2`; kernel over `Q` has dimension 5 and equals `S` |
| Theorem 2 (c): rank of 216 products / with 27 Plücker monomials / Plücker alone | 208 / 213 / 27, intersection 22; the projected coefficient space of the full nullspace has dimension 22 and annihilates `S`, so it is `J_3` |
| Theorem 1: `Det(A(Y)) = F(l(Y))` with Cayley's formula | identity holds; `F` has 21 terms |
| `F = det(L)^2 - 8(e2(P_even) + e2(P_odd)) = 4 det[[Q_12, l_0], [l_0^T, 0]]` | both hold |
| symmetry; irreducibility ingredients | symmetric under `0<->1`, `0<->2`; `l_0`-Hessian rank 3 at `((2,-3,5),(7,1,-4))`; gcd of its entries `2`; one factor over `Q`, `Q(i)`, `Q(sqrt 2)`, `Q(sqrt 3)`, `Q(sqrt -3)` (sanity only) |
| special values | `F(e_1,e_2,e_3) = 1`, `F(e_1,e_1,e_1) = 0`, `F(l,l,l) = -48 (l_1 l_2 l_3)^2`, `F(l,l,m) = -8 l_1 l_2 l_3 perm(l,m,m)` |
| Theorem 1 (d): `F in (J_3)` in degree `(2,2,2)` | rank of `J_3 x` trilinear monomials is 213 with and without `F` |
| Corollary 4 (iii) | exhaustive over all 27 `mu` and all zero-minor patterns with `mu`'s minors nonzero (1,728 cases): the linear-algebra criterion and the stated classification agree in every case |

Hand arguments checked:

- **Irreducibility.**  Factors of a tri-homogeneous polynomial are
  tri-homogeneous.  An `l_0`-degree split `1 + 1` makes the `l_0`-Hessian
  rank `<= 2` everywhere; a split `2 + 0` makes the `l_0`-free factor divide
  every Hessian entry.  The `l_0` analysis alone already excludes every
  nontrivial factorization; the appeal to symmetry is not needed.  Correct
  over every algebraically closed field of characteristic zero.
- **Corollary 3** (rank-one tensors in `S`).  The two bullet arguments are
  correct; the converse (`H_u^3` isotropic; `Y_t = 0` gives `l_t = 0`) is
  correct.  The "iff all three Plücker vectors coaxial" statement for planes
  is confirmed independently by the chart Gröbner bases of Section 1.2.
- **Corollary 4 (i)–(ii).**  `I` is multigraded by the six columns, so
  membership of `P_s` is decided in multidegree `(1^6)`, where Theorem 2 (c)
  shows `P_s` is not in `I`.  `P_s P_s'` for distinct same-parity `s, s'`
  regroups as a product containing a two-equal monomial (the permutations
  differ in every position).  Exponent 2 is correct.
- **Theorem 2 (c) hand remark** (Reynolds operator).  Not checked; the
  document already says the verifier checks only the ranks.

Verifier remarks:

- Check [7] prints "`P_s P_t (s != t)` always contains a two-equal factor"
  but loops only over same-parity pairs.  The transposition pairs needed
  for Theorem 1 (d) are covered by the last check of [7].  Cosmetic.
- The verifier hard-codes `F` as text and then proves `Det = F(l)`; this is
  legitimate.  It replays identities and ranks; it is not the proof of the
  hand arguments, as its header says.

**PASS.**

## 3. Item (c): the symmetry block

The `n = 6` UNSAT uses chain normalization plus lex-leader clauses for the
endpoint swaps `(0 1), (2 3), (4 5)` and the colour swap `1 <-> 2`.

- **Soundness argument.**  Chain normalization along `0^n` is valid (Laplace
  at the lowest unplaced vertex).  The generators fix the chain clauses
  (`g[2k-2, 2k-1, 0, 0]` and `m[{2k, ..., n-1}, 0...0]`), map witnesses to
  witnesses (global colour permutations preserve the GHZ pattern), and map
  every rule family (Laplace, `(G)`, killers, H2, H3, PR) onto itself.  The
  lex-least `g`-vector of an orbit of chain-normalized witnesses satisfies
  `x <= h(x)` for every generator `h`.  Lazily added clauses are instances
  of valid rules, true for that representative whatever subset is added.
  The auxiliary `sig`/`can` variables of H2/H3 have semantic values for a
  witness (bipartite colouring; "both terms nonzero and cancelling").
- **Namespaces.**  The pool contains exactly four `eq` namespaces at
  `n = 6`: `('swap',0,1)`, `('swap',2,3)`, `('swap',4,5)`, `'colour12'`.
  The 2026-10-08 `id(image)` defect is repaired.
- **Orbit test (`orbit_test.py`).**  The clauses that `GSM(6, symmetry=True)`
  adds over `GSM(6, symmetry=False)` (2,128 clauses; the one `m`-unit dropped;
  `TRUE` re-asserted) were loaded into CaDiCaL.  For 1,500 random
  `g`-vectors containing the chain (densities 0.03–0.5, symmetrized under
  random generator subsets to create long ties), every member of the
  orbit under the group generated by the four generators was fixed by
  assumptions and compared with a direct Python evaluation of "chain
  present and `x <=_lex h(x)` for each generator".  7,154 members: **0
  mismatches**; **no orbit without an accepted member** (orbit sizes
  1–16; 1 or 2 accepted members).  The WB4-review orbit (chain plus one
  colour-0 edge `{a,b}`, `a in {0,1}`, `b in {4,5}`) is accepted exactly at
  `{1,5}`, as the per-generator predicate requires.
- `n = 8` (run id `rev-orbit-n8`): five namespaces
  (`('swap',0,1)`, `('swap',2,3)`, `('swap',4,5)`, `('swap',6,7)`,
  `'colour12'`); 4,086 symmetry clauses; 400 orbits, 3,142 members (orbit
  sizes 1–32): **0 mismatches**, no orbit without an accepted member; the
  WB4-style orbit (`b in {6,7}`) accepted exactly at `{1,7}`.

**PASS.**  The block is exactly the per-generator lex-leader predicate on
the tested vectors and never removes a whole orbit.

## 4. Item (d): reproduction

CaDiCaL 1.5.3 via python-sat, Python 3.13, Windows; wall-clock times on a
loaded machine.

| command | note's result | reviewer |
|---|---|---|
| verifier | ALL PASS, ~5 s | ALL PASS, 2.6 s |
| `4 --plane-rigidity --killers` | SAT, 0 PR, checker PASS | SAT, 0 PR, checker PASS |
| `4 --plane-rigidity --holonomy` | SAT, checker PASS | same |
| `6 --pattern P27 --killers --no-symmetry --plane-rigidity` | SAT; 11,356 / 2,744 failure reasons | SAT, checker PASS, same counts |
| same `+ --holonomy` | UNSAT | UNSAT, 2 rounds |
| `6 --pattern P41 ... --plane-rigidity --plane-mode deg3` | UNSAT, 8 PR | UNSAT, 2 rounds, 8 PR (level 6) |
| `6 --pattern P63 ... --plane-mode deg3` | UNSAT, 8 PR | same |
| `6 --pattern-file bl_full_word_survivor_n6_51.json --killers --no-symmetry` | SAT (survivor) | SAT, checker PASS |
| same `--plane-rigidity` / `--plane-mode deg3` / `--plane-top-only` | UNSAT, 8 PR | UNSAT, 2 rounds, 8 PR, in all three |
| `6 --killers --plane-rigidity` | SAT, 63 entries, 32 PR | SAT, 63 entries, 3 rounds, 32 PR, checker PASS |
| `6 --killers --holonomy --plane-rigidity` (run id `rev-hdx-n6-kh-pr-sym`, cap 3,600 s) | UNSAT, 145 s, 77 rounds, 322,856 (576 PR) | **UNSAT, 161.6 s, 77 rounds, 322,856 instances** (H2 14,540; E 71,548; C 73,256; S 162,936; PR 576, all at level 6) |
| lex-leader-free and symmetry-free cross-checks | not done (the note's `--no-symmetry` run timed out) | Section 5 |
| `8 --killers --plane-rigidity` (run id `rev-hdx-n8-k-pr`) | SAT, 52–58 s, 128 entries, checker PASS, census of Section 4.2 | SAT, 63.6 s, 1 round, checker PASS; support **identical** entry by entry to the printed 128-entry support; census identical (`h` dead 1,801,200; top-level live outside summand 1,859,520; level 6: 1,476 / 4,762 / 7; 0 fires) |

## 5. Item (d), continued: removing the lex-leader block

The note flags that both `n = 6` UNSAT answers rely on the repaired
symmetry block and that its own `--no-symmetry` run timed out.  The
reviewer ran three cross-checks (all `n = 6`, killers + H2 + H3 + PR, value
mode, CaDiCaL 1.5.3, under `run_bounded.py`):

| run id | symmetry clauses | lazy strategy | result |
|---|---|---|---|
| `rev-n6-chain-only` | chain normalization only (`g[2k-2,2k-1,0,0]`, `m[{2k..5}, 0000]`); **no lex-leader clauses** | repository CEGAR loop | **UNSAT**, 1,065 s, 292 rounds, 524,037 lazy instances (H2 24,101; E 112,572; C 114,900; S 270,168; PR 2,296) |
| `rev-n6-nosym-crosscheck` | **none** | the 322,856 lazy instances harvested from the symmetric run (each is a valid rule instance, independent of the symmetry block), then the repository CEGAR loop without symmetry | **inconclusive** (bound 3,600 s, exit 124): about 400 symmetry-free rounds, 584,105 instances; late rounds each added 8 PR instances; no SAT model passed the checkers |
| `rev-n6-nosym-orbit` | **none** | as above, plus every PR clause closed under all `720 x 6` vertex and colour relabellings (842,400 PR clauses at the start, and for every new PR clause) | **inconclusive** (bound 3,600 s, exit 124): PR violations stopped after closure, but holonomy rounds became slow (20 rounds by 3,575 s, 390,422 instances); no SAT model passed the checkers |

The chain-only run removes every lex-leader clause; what remains is the
WLOG relabelling along a nonzero Laplace chain of the constant word `0^6`,
which is valid because `T_V(0^6) != 0` and Laplace expansion at the lowest
unplaced vertex always has a live term.  So the `n = 6` UNSAT **does not
depend on the lex-leader block**, the component that was defective on
2026-10-08.  It still depends on the chain normalization and on the
relabelling invariance of every rule family, both of which hold (Section 3).
A fully symmetry-free UNSAT was **not** obtained within two one-hour
bounds; that remains open, together with certification (Section 7).

## 6. Item (e): the `n = 8` models and the gluing discussion

### 6.1 The two printed supports

The note prints only `g`-supports; the `m`-part of its models is not
recorded.  The reviewer therefore fixed `g` to each printed support (no
symmetry block) and re-solved `m` with the repository encoder, adding PR
(all levels) and, for the 156-entry support, top-level H2/H3 lazily.

| support | rounds | repository checkers | reviewer's own `(L)(F')(G)` + PR predicate |
|---|---|---|---|
| 128 entries (killers + PR; also reproduced from scratch, Section 4) | 1 (46 s) | `check_model` 0 violations, `check_plane` (all levels) 0 | 0 `(L)(F')(G)` violations; 0 PR violations; 45,697 premise-1–2 instances, 4,446 fire, all on live cubes; 4,635 zero cubes stopped at the minors |
| 156 entries (killers + top-level H2/H3 + PR) | 1 (36 s) | `check_model` 0, `check_plane` (all levels) 0, `check_holonomy` (top) 0 | 0 `(L)(F')(G)` violations; 0 PR violations; 14,078 premise-1–2 instances, 11 fire, all on live cubes; no zero cube passes premises 1–2 |

So both supports admit an `m`-assignment that passes the extended checker
and the reviewer's independent PR predicate.  The `m`-assignments are
re-solved, not the original runs' (which were not saved), so the
156-entry census numbers of the note are not re-derived; the 128-entry
census is re-derived exactly by the from-scratch rerun.  Lower-level
holonomy was not imposed on the 156-entry support, as the note says.
These are relaxation models only; nothing here bears on the existence of
an eight-vertex witness, and the note does not claim otherwise.

### 6.2 Gluing and OCC-PR

- **OCC-PR(n)** is stated as a top-level (`A = V`) occurrence statement.
  The note's remark that it "is exactly as strong as the exclusion it would
  give" is correct: OCC-PR(n) implies "no witness of order `n`" by Section
  3.2 with Corollary 3, and conversely is vacuously true if no witness
  exists.  It is correctly called the statement a gluing theorem would
  have to supply, not a lemma toward one.  **No overstatement.**
- The "evidence against deriving OCC-PR(8) from the support axioms with
  killers" is correctly scoped (a relaxation model, not a witness).
- **Imprecision 1 (Section 4.1, last paragraph).**  "At `n = 6` the first
  three conditions reduce to 'the outer triangle is independent at `c`'".
  Independence of the outer triangle is sufficient but not necessary: at
  `n = 6`, `A = V`, premise 2 says that for every cube word and every inner
  pair, either the inner entry vanishes or, for each outer `u`, `W_{t_k u}`
  at the cube colours or the outer edge `R - u` at `c` vanishes.  Section
  3.2's version ("or that the inner entries vanish") is the accurate one.
  No consequence for any result.
- **Imprecision 2 (Section 4.3, sharper next lemma).**  "The polarization
  identity applies verbatim, with `l_t` replaced by the Plücker vector of
  `V_t` in `Lambda^2 C^{|R|}`": correct as the contraction identity (the
  contracted vectors are `iota_{e_r}(y wedge y')`).  But for `|R| >= 4`
  the Plücker vectors are confined to the decomposable cone (the Plücker
  relations), Theorem 2 (c) (completeness) and the rank-one classification
  are `|R| = 3` facts, and nothing shows that the degree-three forms cut out
  the zero set.  The question "which rank-one tensors lie in its kernel" must
  be read over decomposable `l_t`.  The lemma is labelled "not attempted",
  so this is a precision note, not an overstatement.

## 7. Item (f): gaps

1. **The `n = 6` UNSAT is uncertified.**  No DRAT/LRAT proof (the reviewer
   had no `drat-trim` on this host); it rests on CaDiCaL 1.5.3 and on the
   Python encoder.  It concerns an order already excluded by other means
   and closes nothing.  It no longer depends on the lex-leader block
   (Section 5), but a fully symmetry-free UNSAT was not obtained.
2. **Other rule families.**  The UNSAT also uses the killer theorem
   (`THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md`) and H2/H3 (Lemmas A'
   and B' of the holonomy note).  This review read the Lemma A'/B' proofs
   and checked that the auxiliary `sig`/`can` variables have consistent
   semantic values for a witness (bipartite colouring; square closure of
   `alpha(x) beta(y) = -1` with nonzero factors), but it is not an audit of
   those families.  No dedicated review of the holonomy note exists under
   `docs/audits/`.
3. **No independent audit and no Lean** for the theorem document; this is a
   same-day agent review.  The scratch computations that found `F` and the
   binomial certificates, and the note's smoke tests, are uncommitted (as
   the documents say); so are this review's scripts (Section 8).
4. **Theorem 2 (c) hand remark** (Reynolds operator) is unverified; the
   completeness claim rests on the exact ranks, which were recomputed.
5. **`deg3` versus `value`.**  The equality of the two runs is structural
   (Section 1.3), not an `n = 6` observation; the note understates this.
6. **Verifier message** in check [7] says "`s != t`" but checks same-parity
   pairs only (cosmetic; the needed transposition case is covered by the
   last check).
7. **Wording** in Section 4.1 (`n = 6` reduction) and Section 4.3
   (`Lambda^2` extension), Section 6.2 above.
8. **Reproducibility of SAT artifacts.**  The note's run logs live in the
   untracked `.research-runs/`; the `n = 8` models are printed as
   `g`-supports only.  Checker PASS for the 156-entry support could be
   re-established here only by re-solving `m` (Section 6.1).
9. **Scope of PR.**  PR needs every non-`C` summand to vanish exactly at the
   support level and a single-monomial minor at each inner vertex; Theorem
   2 of the bilinear-grid document (hollow grid with a full row) is not
   encoded; no occurrence theorem supplies PR's premises in a witness at any
   order (the note says all three).
10. **Field scope.**  The reviewer's second route (Section 1.2) is over `Q`,
    hence valid over every field of characteristic zero; PR is used over
    `C`, so this suffices.  The characteristic-not-two statements of the
    theorem document rest on the Smith-form argument, which was replayed
    (ranks over `F_2`, `F_3`) but not by a second route.

## 8. Commands and reviewer scripts

Repository commands replayed (Section 4):

```text
python claims/arbitrary-order/verify_permanent_plane_restriction_hyperdeterminant_theorem.py
python claims/finite/n08/explore_general_block_recursive_support_model.py 4 --plane-rigidity --killers
python claims/finite/n08/explore_general_block_recursive_support_model.py 6 --pattern P41 --killers --no-symmetry --plane-rigidity --plane-mode deg3
python claims/finite/n08/explore_general_block_recursive_support_model.py 6 --pattern-file tests/fixtures/bl_full_word_survivor_n6_51.json --killers --no-symmetry --plane-rigidity
python tools/research/run_bounded.py --run-id rev-hdx-n6-kh-pr-sym --timeout-seconds 3600 --memory-mb 8000 -- \
  python claims/finite/n08/explore_general_block_recursive_support_model.py 6 --killers --holonomy --plane-rigidity --out OUT.json
python tools/research/run_bounded.py --run-id rev-hdx-n8-k-pr --timeout-seconds 1800 --memory-mb 10000 -- \
  python claims/finite/n08/explore_general_block_recursive_support_model.py 8 --killers --plane-rigidity --out OUT.json
```

Every reviewer computation expected to exceed 60 s ran under
`tools/research/run_bounded.py`, except one 258 s `n = 8` timing run of
`pr_soundness.py` that was launched directly; it completed normally.  No
reviewer process was left running.

Reviewer scripts (scratch, not committed):

- `gb_chart.py`: chart-wise Gröbner bases (Section 1.2).
- `value_vs_deg3.py`: exhaustive support-level comparison of the two modes
  and of `_plane_choice` (Section 1.3).
- `pr_soundness.py N CONFIGS SEED PROB [OFFSET]`: exact random soundness
  test (Section 1.4).
- `eval_model.py`, `fixed_g_driver.py`: re-solve `m` for a fixed published
  support with the repository encoder, then evaluate the reviewer's own
  `(L)/(F')/(G)` and PR predicates on it (Sections 1.4, 6).
- `thm_checks.py`, `cor4iii.py`: Section 2.
- `orbit_test.py REPO N TRIALS`: Section 3.
- `chain_only.py`, `nosym_crosscheck.py`, `nosym_orbit.py`: Section 5.

## Scope

The theorem document's statements (Theorem 1, Theorem 2, Corollaries 3–4)
are correct as stated, with exact recomputation of every quantitative claim
and a second, `J_3`-free proof of the rigidity step in characteristic zero.
The plane-rigidity clause family is sound for every configuration at every
even order and every level `|A| >= 6`, in both modes; the two modes fire on
the same instances at the support level.  The repaired symmetry block is a
faithful per-generator lex-leader block, and the `n = 6` killers + H2 +
H3 + PR UNSAT reproduces with identical counts and survives removal of the
lex-leader clauses.  It is an uncertified SAT experiment at an order
already excluded by other means.

None of this closes an order, creates a reduction edge, or changes
`docs/current-frontier.md` or the global **UNRESOLVED** status.  PR remains
a conditional local implication whose premises no occurrence theorem
supplies in a witness.
