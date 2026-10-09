# Adversarial review: three-column bilinear grid, permanent plane rigidity, and the 51-entry certificate shape

Date: 2026-10-08

Review type: **same-day agent review** (a separate agent session in its own
worktree, adversarially briefed).  It is not independent human refereeing, not
an independent re-derivation by a different research group, and not formal
kernel verification.  No Lean counterpart exists.

Global Krenn–Gu status: **UNRESOLVED** (unchanged by this review).

Reviewed objects (commit `4594375dcb82bf956bcae24e288be1f064848b7e`, branch
`origin/claude/multilinear-shape-20261008`; git blob ids):

| file | blob |
|---|---|
| `claims/arbitrary-order/THREE_COLUMN_BILINEAR_GRID_THEOREM.md` | `44855dcc87f89dcf23ba6de4535bf60f1b4cdc88` |
| `claims/arbitrary-order/verify_three_column_bilinear_grid_theorem.py` | `0346449b3f749acf58c62f8cb4a48d5e2e268f9b` |
| `docs/strategy/multilinear-certificate-shape-2026-10-08.md` | `22fe04e297e274fac852188e4fb243b8e69ff9c5` |
| `claims/finite/n06/search_51_entry_survivor_multilinear_certificates.py` | `e66737ef77b8900ea05e6791e96f3219cc39257d` |
| `claims/finite/n06/verify_51_entry_survivor_bilinear_grid_certificates.py` | `b8035b59192f569543c1edf76a5468244cd13549` |
| `tests/fixtures/bl_full_word_survivor_n6_51.json` | `f72d7dc3b7b39b2a636c3755998db32b3870b1f7` |
| `docs/strategy/holonomy-support-model-2026-10-08.md` (input, Section 5.4) | `62107f68cdb24f5c1a555e8513cb732ff00dc96c` |

The reviewed documents were not edited.

## Summary verdict

| item | verdict |
|---|---|
| (a) Statements, quantifiers, field, literal semantics | **PASS with wording gaps**: Theorem 2 is vacuous at `n = 4`; the note's clause listing omits hypothesis 2; at `n >= 8` the premises are model literals (`m`), not physical-support literals |
| (b) Theorem 2 identity (constant `2`, signs, cofactors) | **PASS**; re-expanded independently for all nine `(p, q)`, and replayed at `n = 8` and `n = 10` against the full matching sum with genuinely recursive `H_uv` |
| (c) Theorem 3 (plane rigidity) | **PASS**; proof complete; brute force over `F_3`, `F_5`, `F_7` agrees; `char != 2` is necessary (fails over `F_2`) |
| (c) Corollary 5 (i) | **PASS** (support-level, as stated) |
| (c) Corollary 5 (ii) | **PASS as a value-level statement; FAILS as the support-level / unit-ideal statement paraphrased in the note, Section 4** — explicit counterexample below |
| (c) `k = 2`, `k = 4` boundary examples | **PASS** (reproduced); they refute the stated naive lemmas only, not `k = 4` hyperplane rigidity |
| Proposition 4 | **PASS**; all 27 minor-pair choices checked (not just the three class representatives); one wording defect |
| (d) Reproduction | **REPRODUCED exactly** (all four commands); the full-system `D <= 2` run tests exactly what is claimed |
| (e) Identity of the two 51-entry survivors | **PASS** (6 isomorphisms reproduced with independent code; transcription matches Section 5.4) |
| (f) Gaps | eleven items, Section 7 |

No finding changes a mathematical status, a frontier edge, or the global
status.  No exact counterexample to the Krenn–Gu conjecture appeared.  The
one false statement found (Section 3.2) is a paraphrase in the strategy note
about an ideal on an abstract slice; it does not affect the 51-entry
survivor, whose rows satisfy the corrected condition.

## 1. Statements, quantifiers and literals (attack item a)

- **Field.**  Theorem 1 is a ring identity.  Theorem 2's displayed identity
  is a ring identity (re-expanded below); its conclusion divides by `2` and
  needs a domain of characteristic `!= 2`, as stated.  Theorem 3 needs
  `char != 2` twice: `det B_x = 2 x1 x2 x3` and the full vector
  `(1/l1, 1/l2, -2/l3)`.  Over `F_2` the theorem is false (Section 3.1).
  Proposition 4 is integral.  The status line is accurate.
- **Order.**  Theorem 2 is stated "for every even order `n >= 4`", but at
  `n = 4` the set `R = V - {a, b}` has two elements and cannot contain the
  three columns `C`.  The theorem is vacuous there; its effective range is
  `n >= 6`.  Harmless, but the status line overstates the range.
- **"Complementary coefficient."**  Defined precisely in Theorem 1:
  `H_uv = T_{R - {u, v}}(c)`, an order-`(n - 4)` matching sum restricted to
  the word `c`.  Hypothesis 1 is the value statement `H_uv = 0` for every
  pair not inside `C` (including pairs with both ends outside `C` when
  `n >= 8`).  This is correct and complete.
- **"Killed a–b term."**  Hypothesis 2, `W_ab[beta, gamma] T_R(c) = 0` for
  the four colour pairs.  Precise.  At `n = 6` it follows from hypothesis 1,
  because every perfect matching of the four-set `R = C + r` has an edge
  inside `C`.  Checked.
- **Support-checkability.**
  - At `n = 6`, all hypotheses are physical-support statements on the torus:
    hypothesis 1 is "`C` independent at `c`", `h_kl != 0` is "`r` joined to
    all of `C` at `c`", and staircases are `g`-literals.  The theorem
    document says exactly this.
  - At `n >= 8`, `H_uv` and `T_R(c)` are recursive coefficients.  Their
    vanishing is **not** determined by the physical support.  In the
    recursive model of the holonomy note (Section 2: `m[A, w]` means
    `T_A(w) != 0` for every even `A`), they are `m`-literals.  So the
    statement "premises and conclusion are literals of the model" (note,
    Section 5) is correct, and the clause is valid for every complex `W`.
    "Support-level" at `n >= 8` must be read as "model-literal level".
  - **Defect.**  The literal list in note Section 5 ("`not m[...]` for the
    vanishing coefficients, `m[...]` for the three `h`'s, and `g`-literals
    for the staircases") omits hypothesis 2.  At `n >= 8` it is not
    automatic and must be encoded as `not m[R, c]`, or as `not g` on the
    four `W_ab` entries.  A clause without it would be unsound.
- **Staircase.**  The definition ("exactly one of `y_u y'_j`, `y_j y'_u` is
  supported", with `{u, j, p} = {1, 2, 3}`) is a conjunction of
  `g`-literals, and it makes `det[y, y', e_p] = +-` a nonzero monomial on
  the torus.  The staircase is relative to the index `p` (resp. `q`) used in
  `Y` (resp. `Z`).  The text leaves this implicit; it is clear from the
  formula.
- **Conclusion as a clause.**  "Premises imply one of `T_A(w_ij)` is
  nonzero" is valid at every level `A`.  At `A = V`, mixed words force all
  four `m[V, w_ij]` false, giving the exclusion.  Correct.

## 2. Theorem 2 identity (attack item b)

Independent checks (scratch script, not committed; run under
`run_bounded.py`, run id `review-bg-scratch-checks`, 4.6 s):

- **Cofactor identity.**  With generic `y, y', z, z'` and hollow symmetric
  `H_C`, I built `G = Z^T H_C Y` directly from bilinear forms (not by matrix
  products), took the cofactors **exactly as printed in the document**, and
  expanded
  `g11 G11 + g12 G12 + g21 G21 + g22 G22 - 2 h12 h13 h23 det Y det Z`.  It is
  `0` for all nine `(p, q)`.  `det H_C = +2 h12 h13 h23`.  The constant `2`
  and every sign are as printed.  By hand, the Leibniz/cofactor grouping
  also matches: `G13`'s coefficient `G21 G32 - G22 G31` is split as
  `g21 = G13 G32` and `g22 = -G13 G31`.
- **`G_ij = T(w_{beta_j gamma_i})`.**  `G = Z^T H Y` has
  `G_ij = z_i^T H y_j`, and `H` is symmetric, so this is the bilinear form
  of Theorem 1 with `beta_j` at `a` and `gamma_i` at `b`.  The index
  transposition in the document is correct.
- **Theorem 1 at higher order.**  An independent bitmask matching-sum DP
  (mod `1000003`, random entries) confirms the expansion at `n = 8`
  (all 28 pairs, 56 words) and `n = 10` (all 45 pairs, 45 words).  The
  committed verifier only samples 6 cases at `n = 8`.
- **Theorem 2 with recursive coefficients.**  At `n = 8` and `n = 10`
  (`a, b = 0, 1`; `C = {2, 3, 4}`; `C` independent at `c`; only one outside
  vertex joined to `C` at `c`; `W_ab` killed; all other entries random),
  the script evaluates every `H_uv` by the full DP.  It confirms
  hypothesis 1, `h_kl != 0`, that the four grid values equal the actual
  `T(w)`, and the certificate identity for all `(p, q)`.
  - Limitation: in this test, hypothesis 1 holds through support zeros.  A
    configuration in which an order-`(n - 4)` coefficient vanishes by
    cancellation was not constructed.  Theorem 1 and the linear algebra do
    not care how `H_uv = 0` arises, so this is not a proof gap.
- **Degree bookkeeping** (`n = 6`): `deg g_ij = 4`, certificate monomial of
  degree 7 times 2.  Correct.

**Verdict:** the proof is complete and correct.  It is a two-line argument:
Theorem 1 plus multiplicativity of `det` plus a cofactor grouping.

## 3. Theorem 3, Corollary 5, boundaries (attack item c)

### 3.1 Theorem 3

The proof is complete:

- **(a)** `B_x` is invertible for full `x` when `char != 2`, so
  `perm(x, V1, V2) = 0` forces `V2 ⊂ (B_x V1)^perp`, and
  `dim V1 + dim V2 <= 3`.
- **(b)** The case split on the number of nonzero coordinates of `l` is
  exhaustive (one nonzero coordinate gives a coordinate plane).
- **(c)** Uses the existence of `pi` with `pi(t) != u_t` for all `t` when
  the `u_t` are not all equal.  By Hall's theorem, each row of the 0/1
  matrix has two ones, and a column is empty only if all `u_t` coincide.

Brute force over all triples of 2-planes: over `F_3` (13 planes), `F_5`
(31) and `F_7` (57), the only isotropic triples are the three
`(H_u, H_u, H_u)`.  Over `F_2`, where `perm = det`, there are 7 isotropic
triples, including the non-coordinate `V x V x V` with `V = (0,1,1)^perp`.
So `char != 2` is necessary, as the status line says.

### 3.2 Corollary 5

- **Slice formula.**  `T(w) = perm(...)` on `U`-pinned words is correct.
  A matching with a `T`–`T` edge leaves one `T` vertex and three `U`
  vertices, so it has a `U`–`U` edge, which vanishes at `sigma`.
- **(i)** Correct and support-level.  It is Theorem 2 at `n = 6`, with the
  full row supplying the three `h`'s.
- **(ii)** Correct when read as a statement about the witness's **values**:
  "no witness's rows satisfy (ii)".  This is exactly Theorem 3.  But
  "spanning a plane that contains a full vector" is not a support property:
  two rows with the same support can be proportional at some torus points.
  The note (Section 4) paraphrases (ii) as a support-level condition:
  "the saturated ideal of the 27 cross permanents is the unit ideal
  whenever … (ii) three planes containing full vectors".

  **That paraphrase is false.**  Counterexample (checked exactly), on the
  abstract slice: give each inner vertex two full rows (colours 0, 1) and an
  unsupported colour-2 row, so the 19 permanents involving colour 2 vanish
  identically.  At the torus point
  - `r_{t,1} = lambda_t r_{t,0}` (`lambda = 2, 3, 5`);
  - `r_{0,0} = r_{2,0} = (1,1,1)`, `r_{3,0} = (1,1,-2)`;

  all eight cube permanents vanish and every entry is nonzero
  (`perm((1,1,1),(1,1,1),(1,1,-2)) = 2(1+1-2) = 0`).  So the saturated
  ideal of this support is not the unit ideal, although at generic points
  of the same support the three row planes contain full vectors.

  **Corrected support-level form of (ii)** (follows from Theorem 3; proof
  in one line):
  - each inner vertex has two rows with **distinct** supports whose union
    is all three columns, and the 8 words used are mixed;
  - then on the torus the rows are independent (proportional vectors have
    equal support), and their span is not a coordinate plane, so it
    contains a full vector by Theorem 3(b).

  The 51-entry survivor satisfies this corrected form: full row plus one
  killer-plane row at each inner vertex.  So nothing about the survivor
  changes.
- **"The correct condition"** (note, Section 4).  Corollary 5 gives
  *sufficient* conditions.  Necessity is neither claimed in the theorem
  document nor proved.  The note's wording "the correct condition"
  suggests a characterization and should be read as "a sufficient
  condition".

### 3.3 `k`-ary boundaries

- `perm_2((1,1),(1,-1)) = 0` is reproduced, and is a valid counterexample to
  "hyperplane (line) rigidity" at `k = 2`.
- At `k = 4`, for `x = (1,1,1,1)` and `x' = (1,-4,-4,-1)`, the matrix
  `B_{x,x'}` has rank 3 (reproduced).  The scratch claim also reproduces:
  generic `det B_{x,x'}` has content `4`, and a 12-term primitive part of
  bidegree `(4, 4)`.  The sign of the primitive part depends on
  normalisation.
- **Scope note.**  The `k = 4` example refutes only the naive
  *full-row lemma* ("two full vectors make `perm_4(x, x', ., .)`
  nondegenerate").  It is not a counterexample to rigidity of triples or
  quadruples of hyperplanes for `perm_4`.  That statement is untested
  either way, and the document does not claim otherwise.
- The `k`-vs-`k` slice and single-entry contraction identities are
  elementary.  They are reproduced by the committed verifier (sampled at
  `k = 4`).

### 3.4 Proposition 4

- The closed form is reproduced.
- I re-ran the membership test for **all 27** ordered triples
  `(I_0, I_1, I_2)` with exact `fmpq_mat` ranks.  The committed verifier
  checks only one representative per class.  The result:
  - in the trilinear span exactly when two pairs are equal and the third
    differs (18 cases);
  - not in the span when all three pairs are equal (3 cases) or pairwise
    distinct (6 cases).
- The verifier restricts the multipliers of `A_ijk` to
  `Y_0[., 1-i] Y_1[., 1-j] Y_2[., 1-k]`.  This is **without loss of
  generality**:
  - the eight `A_ijk` and the target are homogeneous for the
    six-fold column grading;
  - so any polynomial certificate projects to one with exactly these
    multipliers.
- **Wording defect.**  By the same homogeneity, "not in the degree-3 span"
  means the product is **not in the ideal at all**, at any multiplier
  degree.  The sentence "the pairwise-distinct product is in the radical
  … but needs multipliers of higher degree" should say that only a power
  (or a multiple) of it lies in the ideal.  The radical claim itself is
  correct by Theorem 3 (rank-deficient `Y_t` give a zero minor) and the
  Nullstellensatz over `Q-bar`.

## 4. Reproduction (attack item d)

All commands were run in this worktree under
`tools/research/run_bounded.py`.  The run logs are in the ignored
`.research-runs/`.

| run id | command | result | elapsed |
|---|---|---|---|
| `review-bg-verify-thm` | `verify_three_column_bilinear_grid_theorem.py` | PASS, all 22 checks | 2.5 s |
| `review-bg-apply` | `verify_51_entry_survivor_bilinear_grid_certificates.py` | BL51/HOL51/HOL50/P63: 48 grid + 96 cube; P41: 0 + 288; P27: 0 + 0 — matches note Section 6 | 22 s |
| `review-bg-slice-d3` | search `--system slice --max-degree 3` | `D = 0, 1, 2`: none (27 / 1,377 / 35,802 rows; 27 / 810 / 10,620 blocks); `D = 3`: 632,502 rows, 86,509 blocks, 48 hit blocks, 48 monomials, every block 14 rows on a `2x2x2` cube of 8 words; minimal word count 8 | 12.8 s |
| `review-bg-full-d2` | search `--system full --max-degree 2` | 108 equations in 51 unknowns; `D = 0, 1, 2`: none (108 / 5,616 / 148,824 rows; 106 / 3,244 / 42,454 blocks) | 1.8 s |
| `review-bg-scratch-checks` | reviewer scratch checks (Sections 2, 3, 6) | all pass | 4.6 s |

**What the full-system `D <= 2` run actually tests.**  I read the search
code.

- **Unknowns.**  The 51 physical supported entries, with no torus
  normalisation and no recursive coordinates.
- **Equations.**  105 nonzero mixed equations and 3 constant equations
  `T(c) - 1`.  I recounted these independently: 105 + 3, with 621 mixed
  words having no live matching.
- **Multipliers.**  Every monomial of total degree `<= D` in all 51
  unknowns (non-homogeneous system, so `range(D + 1)`).
- **Saturation.**  The target is an arbitrary monomial `c * mu`, including
  `1`.  "A monomial in the `Q`-span" is the bounded-degree form of
  "`1` lies in the ideal saturated by the product of entries".
- **Blocks.**  The 18-dimensional vertex-colour grading, modulo the
  lattice spanned by the three constant-word degrees `kappa_c`.  The
  canonical representative (subtract, per colour, the minimum over
  vertices) is a correct normal form for that quotient.  Every equation,
  including `T(c) - 1`, is homogeneous for the quotient grading, so any
  monomial certificate projects onto the block of its target.  The block
  split loses nothing.
- **Unit-row test.**  A unit vector `e_k` lies in a row space iff some row
  of the RREF equals `e_k`.  The rows of a full-rank RREF are determined
  by their pivots, so the test is exact.  The arithmetic is exact over `Q`
  (`fmpq_mat`).

So "no degree-`<= 2` certificate for the 108 equations" is a correct exact
statement **in physical entries over `Q`**.  Together with the slice
certificate at degree 3, "minimal multiplier degree exactly 3" is
established in that coordinate system.  The note correctly records:

- the full system was not searched at `D = 3`, so "needs all 8 words" is a
  slice-only statement;
- the minimal degree is coordinate-dependent (normalised coordinates absorb
  one degree).

The "8 words" minimality test uses only the first monomial of each hit
block.  That is sufficient here, because every hit block contains exactly
one monomial.  It takes the minimum over blocks; since every block has
exactly 8 words, minimum 8 means every block needs all 8.

## 5. Identity of the two survivors (attack item e)

- The transcription `HOLONOMY_SURVIVOR` in the search script matches the
  table in Section 5.4 of the holonomy note entry by entry.
- With independently written relabelling code (all `720 x 6` vertex and
  global colour permutations), HOL51 maps onto the BL fixture by exactly 6
  maps, for example vertex map `(0,2,1,3,5,4)` with colour map `(2,0,1)`.
  This agrees with the fixture's automorphism group of order 6.
- Both kinds of map are genuine symmetries of the witness problem.  Vertex
  relabelling and a common colour permutation preserve the set of constant
  words.
- The inner/outer data match:
  - holonomy inner `{0,1,3}` maps to fixture `{0,2,3}`;
  - outer colours `2:0, 4:2, 5:1` map to `1:2, 5:1, 4:0`.
- Row patterns on the slice (columns 1, 4, 5):
  - vertex 0: `xx.` / `xxx` / `xx.`;
  - vertex 2: `xxx` / `x.x` / `x.x`;
  - vertex 3: `.xx` / `.xx` / `xxx`.

  This confirms "one full row and two killer-plane rows, zero at columns
  5, 4, 1 respectively".

## 6. Labels and wording in the strategy note

1. Section 3 says "each inner vertex's rows span a 2-plane".  The two
   killer-plane rows of a vertex lie in the same coordinate plane, so all
   three rows generically span `F^3`.  The intended statement is that the
   full row together with either killer-plane row spans a 2-plane
   containing a full vector.
2. Section 2's sentence "the torus normalization sets 11 entries to 1 and
   absorbs one degree" sits under an [EXACT] heading but is an unverified
   heuristic.  It should be labelled [OBSERVATION].
3. Section 3 says "the degree-3 identity exists exactly when two of the
   three minors use the same pair of outer columns".  This is the
   *generic* classification of Proposition 4.  On a specific support,
   other degree-3 certificates are not excluded by it.
4. Section 4: the (ii) paraphrase and "the correct condition"
   (Section 3.2 above).
5. Section 5: hypothesis 2 is missing from the literal list (Section 1
   above).

## 7. Gaps (attack item f)

1. **Corollary 5 (ii) at support level** (note, Section 4): false as
   paraphrased.  Corrected sufficient condition: distinct row supports with
   full union at each inner vertex, and mixed cube words (Section 3.2).
2. **Necessity** of the Corollary 5 conditions for the unit ideal is not
   proved.  "The correct condition" overstates.
3. **Hypothesis 2 is omitted** from the `n >= 8` clause-literal list in
   note Section 5.  Encoding the clause without it would be unsound.
4. Theorem 2's stated range `n >= 4` is vacuous at `n = 4`.
5. Proposition 4 wording: the pairwise-distinct (and all-equal) products
   are not in the ideal at any degree.  Only a power of the
   pairwise-distinct product is.
6. Note Section 3: "rows span a 2-plane" is misworded (Section 6, item 1).
7. Note Section 2: the normalisation remark is mislabelled [EXACT].
8. The theorem document's remark that two-term Theorem A is "the special
   case … `H` has rank two on the live coordinates" is not replayed by any
   verifier and was not checked here.  It is not load-bearing.
9. The full system was not searched at `D = 3`.  The minimality of 8 words
   and of the cube shape is slice-only.  The minimal degree is a statement
   in physical coordinates over `Q`.
10. The `n >= 8` clause family is not implemented in the recursive model.
    Whether it changes any SAT/UNSAT outcome is untested (the note says
    so).  `k = 4` hyperplane rigidity is untested.
11. **Evidence status.**  Primary verifiers plus this same-day agent
    review only.  No independent implementation of the Macaulay search
    exists beyond the reviewer's recount of the equations.  No Lean
    formalisation exists.  No occurrence theorem supplies the premises of
    Theorems 2–3 at any order.

## Scope

Theorems 1–3 and Proposition 4 are correct within their stated scope.
Corollary 5 is correct as a value-level statement, and (i) is correct at
support level.  The strategy note's support-level paraphrase of (ii) is
false and needs the distinct-support repair above.  All computations
reproduce exactly.

These are conditional implications and a measurement on one already-excluded
six-vertex support.  None closes an order, creates a reduction edge, or
changes `docs/current-frontier.md` or the global **UNRESOLVED** status.

The scratch script used for Sections 2, 3 and 5 is not committed.  It is a
review aid, not a certificate.  It contains:

- the cofactor re-expansion;
- the bitmask-DP replay at `n = 8, 10`;
- the finite-field plane enumeration;
- the Corollary 5 counterexample;
- the 27-case Proposition 4 rank test;
- the fixture recounts and the isomorphism recount.
