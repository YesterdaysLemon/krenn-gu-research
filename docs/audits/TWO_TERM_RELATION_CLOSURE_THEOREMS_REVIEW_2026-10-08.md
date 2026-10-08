# Adversarial review: two-term relation closure theorems (A–D) and the row-space attempt note

Date: 2026-10-08

Review type: **same-day agent review** (a separate agent session in its own
worktree, adversarially briefed).  It is not independent human refereeing, not
an independent re-derivation by a different research group, and not formal
kernel verification.  No Lean counterpart exists.

Global Krenn–Gu status: **UNRESOLVED** (unchanged by this review).

Reviewed objects (commit `6b7867e99c644aa3b16a5d4e6d4ea3fa7de71b8a`, branch
`origin/claude/trunk-rowspace-20261008`; git blob ids):

| file | blob |
|---|---|
| `claims/arbitrary-order/TWO_TERM_RELATION_CLOSURE_THEOREMS.md` | `4d0560a4fecfb65475a8da7e4dba78932c400b67` |
| `claims/arbitrary-order/verify_two_term_relation_closure_theorems.py` | `ada63fdb318718754892c3a87fd566976963a63b` |
| `docs/strategy/row-space-all-orders-attempt-2026-10-08.md` | `5bbd8a1ac21e4788a45bc77e3c53b39324746d4b` |
| `tools/explore/binomial_linear_closure.py` | `7ab7517ae08ce64738fdba06264a63f50b59e3a7` |
| `tools/explore/bl_support_cegar.py` | `40efad5fffdbf4963467981813f9904b63568d8a` |
| `tools/explore/find_two_term_free_support.py` | `a096e904d52b8fc0cd97207943b3d9757e96ac06` |
| `tests/fixtures/bl_full_word_survivor_n6_51.json` | `f72d7dc3b7b39b2a636c3755998db32b3870b1f7` |
| `claims/finite/n06/verify_27_entry_two_matching_grid.py` | `ad364b4dc2606d32bf9fdc173210beca931ffc43` |
| `claims/finite/n06/verify_51_entry_bl_survivor_slice.py` | `fa3c21eff00d13be09042c5d5386506a271b2d5d` |

The reviewed documents were not edited.

## Summary verdict

| item | verdict |
|---|---|
| Theorem A (two-matching grid) | **PASS**; holds over every commutative ring (stronger than stated) |
| Theorem B (odd opposite-ratio cycle) | **PASS with a boundary correction**: the identity needs `k >= 3` |
| Theorem C (completeness on binomial supports) | **PASS**; both directions hold, the witness is genuinely constructed; the BL-detection step of the proof is a sketch (repaired below) |
| Theorem D (inertness) | **PASS**; the note's paraphrase drops a premise |
| Verifier and closure tool | **PASS** (all commands reproduce) |
| 51-entry survivor | **REPRODUCED exactly** (identical support, same iteration count) |
| Evidence labels in the note | **Mostly accurate**; four labelling/wording defects listed in Section 6 |

None of the findings changes a mathematical status, a frontier edge, or the
global status.  No exact counterexample appeared.  The six binomial supports
found at `n = 4` are genuine witnesses.  This was expected: `n = 4`, `d = 3`
GHZ states are realizable, the trunk record says so, and the conjecture
concerns `n >= 6`.

## 1. Statements and quantifiers (attack item a)

- **Field.**  The witness entries are complex.  Theorem C uses that `C^*` is
  divisible, so it is genuinely a statement over `C` (or any field whose
  multiplicative group contains the needed roots of unity).  It fails
  verbatim over `R`, where `X^2 = -1` has no solution.  The status line says
  this correctly.  For Theorem A this review found integer cofactors of
  degree at most two for all four corner products, so A holds over every
  commutative ring, including characteristic two.  Theorem B's identity is
  integral, and its conclusion needs `2 != 0` in a domain.  As stated, B is
  correct.
- **Order `n`.**  All four theorems are stated for every even `n`, including
  `n = 2` and `n = 4`, where witnesses exist.  This is harmless, because
  each theorem is an equivalence or a conditional.  The closing sentence of
  Theorem C, "the Krenn–Gu conjecture at order `n` is equivalent to …", is
  meaningful only for `n >= 6`.
- **"Fibre" and "live term."**  A live matching is one whose `n/2` physical
  entries all lie in the declared support `S`.  `S` is the *exact* nonzero
  set, so every theorem is support-relative: it is one branch of a case split
  over supports, and nothing supplies the support from a hypothetical
  witness.  The Boundary section states this correctly.
- **Sub-coefficients as torus variables.**  Theorems A–D and the BL tool use
  only physical entries (the full-word closure).  In A and B the induced
  coefficient `C_t = T_{W[V-{a,b,v_t,v_{t+1}}]}` occurs only as a polynomial
  factor and is never treated as an independent variable, so no soundness
  question arises.  In the *recursive* variant of note Section 1, declaring
  the nonzero induced coefficients as extra torus coordinates is a **sound
  relaxation**.  Every Laplace identity is a polynomial identity, and each
  declared coordinate is nonzero at any witness with that extended support.
  The relaxation has two costs:
  - It forgets that the coordinates are polynomials in the entries, so it is
    incomplete.
  - Its "support" is an extra case split over the zero pattern of the induced
    coefficients, which the physical support does not determine.

  The note's wording ("which induced coefficients are nonzero") declares this
  premise, so the soundness claim stands.  No result reviewed here depends on
  the recursive variant.

## 2. Proofs (attack item b)

### Theorem A — PASS

The factorisation `m_M(w_ab) = x_a u_b` is correct, because no `M`-edge joins
`P` to `Q`, and likewise for `N`.  The displayed eight-variable identity
expands to zero.  Specialising variables that share factors (edges inside
`R`) is legitimate because the statement is a polynomial identity.

This review searched for cofactor certificates by linear algebra with
multipliers of degree at most two.  All four products `T00*x1*u1`, `T00*y1*v1`,
`T00*x1*v1` and `T00*y1*u1` lie in the `Z`-ideal `(T01, T10, T11)`, each with
integral cofactors.  The repository verifier checks the last three only
through a Groebner basis over `Q`.

The "in particular" clause is correct as stated: a constant `w_00`, three
mixed corners, the zero premises, and one nonzero product at `w_11`.  At the
27-entry pattern, the five-zero guard really does reduce every one of the
other thirteen matchings to zero at all four words.  A hand check agrees:
with `13,14,15,34,35` dead at `[0,0]`, vertices `1,3` must use `0,2`, which
forces `45`, so only `M` and `N` survive.

### Theorem B — PASS with a boundary correction

The telescoping argument is correct for odd `k >= 3`.  **At `k = 1` the
displayed identity is false.**  There `p_1 = 2 A_1 B_1`, so the left side
equals `2 A_1 B_1` while the right side is `2 A_1`.  The theorem says only
"`k` odd", so `k >= 3` should be stated.  A distinct-vertex condition is also
implicit: `v_t != v_{t+1}` or `gamma_t = gamma_{t+1}` is needed for the word
`w_t` to exist.  Neither point affects any use in the repository, since the
27-entry triangle has `k = 3` and distinct vertices.

The consequence is stated correctly as "a witness needs one of these factors
to vanish", which is not by itself a contradiction.  A contradiction follows
only when `A_1`, the `B_j` and the `C_t` are known to be nonzero.  At the
27-entry pattern each `C_t` is a single supported entry.

### Theorem C — PASS

The system on `(C^*)^S` is exactly the binomial system: `X^{m_M - m_N} = -1`
for each mixed two-term word, and `X^{m_c} = 1` for each constant word.
Mixed words with no live matching hold automatically.

- **(3) ⇒ (1).**  The witness is genuinely constructed.  The sign
  assignment is a well-defined homomorphism `Lambda -> {±1} ⊂ C^*` exactly
  when no relation has odd mixed coefficient sum.  Divisibility of `C^*`
  extends it to `Z^S`.  Constructively, a Smith normal form gives values that
  are roots of unity.  Setting the entries off `S` to zero, each word's
  coefficient is then the sum over its live matchings, so `T_W = Delta`.
  The case where every mixed fibre is empty was checked at `n = 4` (below):
  all-ones weights on the three perfect matchings of `K_4`, one colour per
  matching, give an actual witness.
- **(1) ⇒ (3).**  This direction is immediate.
- **(1) ⇒ (2).**  This is soundness of BL.  The review checked the
  implementation's soundness: class substitution with the stored values,
  "`Y = 0`" contradictions, proportional-expression detection of
  `Y_u = c Y_v`, and the residue map.  The residue is a canonical coset
  representative because the stored basis is echelon with positive pivots,
  and pivots are reduced in increasing order.
- **(2) ⇒ (3), i.e. an odd circuit makes BL report a contradiction.**  The
  written proof is a sketch.  It says that "a relation … with odd sign
  reaches the zero vector with value `-1`", but a particular relation is
  never reduced as such.  The correct argument has two steps:
  1. In round one every two-term row is itself a support-two vector of the
     row space.  So BL inserts generators of `Lambda` with exactly the values
     of `sigma`: `±(m_N - m_M)` with value `-1`, and the `m_c` (or their
     differences) with value `1`.
  2. Hermite insertion acts unimodularly on the tuple (current basis, new
     generator).  The stored rows have distinct pivots and are therefore
     independent, so the zero vectors produced during insertion generate the
     whole relation module.  Every such zero vector has its value tested.
     If all tested values are `1`, then `sigma` vanishes on every relation
     and is well defined.  Conversely, an inconsistency is reported.

  The conclusion is correct.  The paragraph should carry this
  generating-set argument.
- **Empirical cross-check.**  This review enumerated *all* binomial supports
  at `n = 4` by SAT with blocking clauses (exhausted: there are exactly 6).
  It also compared BL with an independent odd-circuit test, which reads a
  `Z`-basis of the left kernel off an integer row reduction of `[R | I]`.
  The two agree on all 6: no odd circuit, BL CLOSED.  These 6 supports are
  the `3! = 6` colourings of the three perfect matchings of `K_4`, and they
  are genuine witnesses.  This is the predicted behaviour, since `n = 4` is
  realizable.
- **Binomial supports at `n = 6`.**  The same search at `n = 6` produced no
  SAT answer: the first SAT call timed out under both a 420 s and a 600 s
  bound, with two different cardinality encodings.  The outcome is
  **UNKNOWN**, which is a run outcome, not evidence either way.  Whether
  binomial supports exist at `n >= 6` is therefore **not known** from this
  review.  If none exists, then
  Theorem C is true but vacuous at that order.  The theorem document does not
  claim nonemptiness.

### Theorem D — PASS

The distinct-monomial lemma holds: a perfect-matching monomial records every
vertex's colour and its partner.  The verifier checks it at
`n = 4, 6, 8`, but the one-line argument is the proof.

The row-ownership argument is correct:

- A row-space vector with support at most two cannot involve a mixed row with
  at least 3 terms.
- It cannot involve a constant row with at least 2 terms, because that row
  together with `Y_0` already has at least 3 nonzero entries.
- Combinations of single-term constant rows give only `X^{m_c} = 1` and
  their quotients.

The second-round coset argument is also correct.  The `m_c` have disjoint
supports, so every lattice coefficient lies in `{-1,0,1}`.  A weight-`n/2`
0/1 vector `m` containing `m_c` equals `m_c`, so two distinct matching
monomials share a class only if both are among the `m_c`.  Rows that were
single-term constants become empty, nothing else merges, no insertion
happens, and the closure stops at round two (or round one if there are no
single-term constants) without contradiction.

The phrase "would need some row with at most two nonzero entries in total" is
loose but repairable, as just shown.

`--n 4 --full` gives CLOSED, round 1, lattice rank 0.  This is consistent
with D, because at `n = 4` every constant fibre of the full support has three
terms.

**Paraphrase defect.**  The note (Section 2) and the review brief state D as
"if every nonempty mixed fibre has at least three live matchings, the
full-word closure derives nothing".  This drops the premise that **every
constant word has at least one live matching**.  Without that premise BL
returns a contradiction at once ("pure word has no live matching").  It also
drops the exception that BL does derive `X^{m_c} = 1` for single-term
constant fibres.  The theorem document states both correctly.

## 3. Reproduction (attack item c)

All runs were on Windows with Python 3.13, python-flint 0.9.0 and python-sat
(CaDiCaL 1.5.3).  Runs that could exceed 60 s used `run_bounded.py`.  No
process remains.

- `python claims/arbitrary-order/verify_two_term_relation_closure_theorems.py`
  gives A PASS, B PASS for `k = 3,5,7,9` and even `k = 4,6`, and D PASS at
  `n = 4, 6, 8` (243 / 10,935 / 688,905 pairs).  About 3 s.
- `python tools/explore/binomial_linear_closure.py --pattern27` gives
  `CONTRADICTION`, "lattice inconsistency: `X^0 = -1`", round 1.
- `python tools/explore/binomial_linear_closure.py --support-json tests/fixtures/bl_full_word_survivor_n6_51.json`
  gives `CLOSED`, 2 rounds, 148 classes, lattice rank 27, row rank 46, as
  recorded.
- `python tools/explore/binomial_linear_closure.py --n 4 --full` gives
  `CLOSED`, 1 round, lattice rank 0.
- `python claims/finite/n06/verify_27_entry_two_matching_grid.py` and
  `python claims/finite/n06/verify_51_entry_bl_survivor_slice.py` both PASS.
- `python tools/research/run_bounded.py --run-id review-bl-cegar-n6-killers-20261008 --timeout-seconds 900 --memory-mb 6144 -- python tools/explore/bl_support_cegar.py --killers --seconds 840 --output tmp/review-bl-cegar-n6-killers.json`
  gives `BL_SURVIVOR` after **59 iterations**, **216,000** unique cut images,
  81.4 s.  The survivor's 51 entries are **identical** to the committed
  fixture, and the note's displayed block list equals the fixture.  The
  recorded run took 88.5 s, so the CEGAR is deterministic for this solver and
  model order.
- `python tools/research/run_bounded.py --run-id review-two-term-free-n6-k-20261008 --timeout-seconds 600 --memory-mb 4096 -- python tools/explore/find_two_term_free_support.py --killers`
  gives `UNSAT` in 138.8 s.  This reproduces the [SOLVER] claim (status
  only, no DRAT).
- **Independent recount** (a scratch script with no repository imports).
  - Pattern27: 691 empty mixed fibres, 35 two-term mixed fibres, constant
    fibres of sizes 1 (`111111`) and 2 (`000000`, `222222`).  This matches
    "37 two-term words".
  - 51-entry survivor: mixed fibres of sizes 0 (621), 2 (62), 3 (36), 4 (6)
    and 6 (1), and all three constant fibres have size 3.  This matches the
    note's "3 (39)".
  - Both supports pass the single-term conditions and the column-killer
    condition.  The killer encoding matches
    `THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md`: `W_vu[:,j] = 0` for
    `j != c` and `W_vu[:,c] != 0`, with rows indexed by the colour at `v`.
- **Binomial supports.**  The `n = 4` enumeration is reported above.  At
  `n = 6` the first encoding's first SAT call did not finish within the
  420 s bound (`timed_out`).  A sequential-counter retry under a 600 s bound
  also timed out before the first SAT answer.  The result is **UNKNOWN**.
  Both child process trees were terminated by the runner (Job Object).

## 4. The 51-entry survivor against the conjecture's hypotheses

The note's conjecture (TM_D) quantifies over supports satisfying the trunk
record's *recursive* conditions (L), (F'), (G) and the killers.  The CEGAR,
however, enforces only the full-word single-term conditions and the killers.
The note does not check that the survivor satisfies (L), (F'), (G).

This review closed that gap.  It used the trunk record's GSM encoder (the
general-block recursive support model script under `claims/finite/n08/` on
`origin/claude/trunk-attempt-record-20261008`; it is not present on this
branch), with symmetry breaking off and the physical support fixed by
assumptions.  The extension is **SAT** for
both the 51-entry survivor and the 27-entry pattern (control).  The encoder's
brute-force `check_model` reports zero violations for each model.  So the
survivor satisfies (L), (F'), (G) and the killers, and "`D = 0` fails at
`n = 6`" is consistent with TM_D's hypotheses.

Conversely, (L), (F'), (G) imply the full-word single-term conditions.  The
reason is that (L) forces induced coefficients without a live matching to be
zero, and (F') then forces any single-live-matching coefficient to be
nonzero.  So the [SOLVER] UNSAT of `find_two_term_free_support.py --killers`
transfers to the recursive hypothesis set.

The slice exclusion is valid.  The torus normalisation is a vertex-colour and
right-vertex rescaling of the `c_tu` that preserves the zero set of the
all-mixed slice.  This review solved it explicitly: the eleven conditions fix
`lambda_{t,a}`, `mu_4` and `mu_5` with `mu_1` free.  Then `s in` the ideal,
with `s` a supported entry, is a contradiction.

The note's hand claim "degree at most two" was tested by a pure Macaulay test
in the normalised coordinates.  That test asks whether the span of
`mu * (slice equation)` with `deg mu <= D` contains a monomial, and it uses
no lattice quotient.  The results:

| `D` | rows | columns | rank | monomial in the span? |
|---|---|---|---|---|
| 0 | 27 | 26 | 18 | no |
| 1 | 297 | 213 | 177 | no |
| 2 | 1,782 | 981 | 894 | yes, e.g. `s` |

This supports the claim in those coordinates.  "Degree" is not invariant
under the torus normalisation used, which is a definitional point for TM_D
(Section 6).

## 5. Pattern27: more than three independent kills

The note says the 27-entry pattern dies "three independent ways" and that
"the full-word closure finds the triangle first".

The first statement is true as a lower bound, but it undercounts.  Removing
the triangle words, and then also both grids, still leaves a round-one
lattice inconsistency.  Greedy shrinking yielded **seven further
word-disjoint odd triangles** among the two-term mixed words, for eight in
total.  The seven are

- `{210012, 220020, 220222}`
- `{202000, 202202, 212012}`
- `{200121, 200200, 220220}`
- `{002000, 002200, 012010}`
- `{010010, 020020, 020220}`
- `{000121, 000202, 020222}`
- `{012012, 022020, 022222}`

The second statement is not established.  The tool reports only the kind and
round of the contradiction, not which circuit it found.

## 6. Evidence labels in the note (attack item d)

Accurate:

- [PROVED] soundness of the schema.
- [PROVED] Theorems A–C as summarised.
- [SOLVER] for the two-term-free UNSAT, explicitly status-only.
- [EXACT + SOLVER] for the survivor.
- [EXACT] for the 27-pattern counts.
- [CONJECTURE] for TM_D.
- The "no frontier change" rationale.

The theorem document correctly says that its verifier replays identities and
is not the proof of C and D, and that no independent audit exists.

Defects (wording or labelling only; no status change):

1. **Theorem D paraphrase.**  Section 2 drops the premise "every constant
   word has at least one live matching" and the `X^{m_c} = 1` exception
   (Section 2 of this review).
2. **"[PROVED] Without the killer theorem, no full-word two-term family can
   work, at any order."**
   - The proved content is Theorem D together with the fact that the full
     support satisfies (L), (F'), (G) at every `n >= 4`.
   - The note cites the trunk record for the latter, but that record is an
     `n = 6` SAT model.  The all-order fact is easy but unstated: declare
     every induced coefficient nonzero except mixed full words, so (L) holds
     trivially and (F') sees `n - 1 >= 3` nonzero terms.
   - The follow-on "so the trunk lemma must contain a relation among at least
     three supported terms" is interpretive, since "relation among" is not
     defined.  It should be labelled as a methodological reading, not
     [PROVED].
3. **"The full-word closure finds the triangle first."**  This is
   unsupported (Section 5).  The "three independent ways" claim should read
   "at least three".
4. **TM_D status paragraph.**
   - "`D <= 2` handles both six-vertex obstructions" rests on a hand
     derivation in normalised coordinates.  The verifier checks only ideal
     membership, which the note says.  This review's Macaulay test supports
     it in those coordinates.
   - `BL^D` is not fully specified.  It is unclear in which coordinates
     degree is measured, given torus normalisation and the Laurent monomials
     that `Lambda` introduces.  It is also unclear whether the recursive
     coordinates count, and whether multipliers interact with binomial
     feedback.
   - The ST20 "degree-two" and the 25-literal "degree at most four" remarks
     carry no evidence label.  This review did not check them.

Not checked by this review:

- The provenance remark that A and B sharpen the ratio mechanisms in
  `source-cancellation-mechanisms-2026-09-13.md`.  The cited sections exist
  and describe four-corner ratios and coloured-slot triangles.
- Whether the new 51-entry survivor coincides with the earlier recorded
  51-entry survivor.  That survivor exists only as ignored local artifacts.

## 7. Exact gaps (attack item e)

1. Theorem B must state `k >= 3` (false at `k = 1`), and implicitly
   `v_t != v_{t+1}` or `gamma_t = gamma_{t+1}`.
2. The written proof of Theorem C, direction "odd circuit ⇒ BL contradiction",
   omits the generating-set argument for Hermite insertion.  The repair is in
   Section 2; the conclusion stands.
3. Nonemptiness of the binomial-support class at `n >= 6` is open.  Theorem C
   may be vacuous at those orders.  It is not claimed otherwise, but the
   sentence "on this class the Krenn–Gu conjecture is exactly a combinatorial
   odd-circuit statement" should be read with that in mind.
4. The note's Theorem D summary omits a premise (Section 6, defect 1).
5. Section 4 of the note:
   - The "at any order" input is not cited correctly (defect 2).
   - The survivor's (L), (F'), (G) status was unchecked in the note.  It is
     now checked here: SAT, with zero brute-force violations.
   - `BL^D` / TM_D is under-specified (defect 4).
6. Theorem A's three cross-product memberships are verified in the repository
   only over `Q` (Groebner).  This review supplies integral cofactors, which
   confirms the stated field range and in fact extends it to all
   characteristics.

## Scope

Theorems A–D are correct within their stated scope, up to the `k >= 3`
correction to B.  They are conditional, support-relative statements about a
proof technique.  None is an occurrence theorem, none excludes a witness
without explicit support premises, and none changes the frontier or the
global **UNRESOLVED** status.

The 51-entry survivor is a support-level object, not a weight realisation,
and it is excluded by the six-vertex theorem and by the slice certificate.
Scratch scripts used for the independent checks are not committed.  They are
exploratory review aids, not certificates:

- the cofactor search;
- the fibre recount;
- the recursive-extension test;
- the binomial-support enumeration with the `[R | I]` odd-circuit test;
- the slice Macaulay test;
- the pattern27 word-set shrinking.
