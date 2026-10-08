# Row-space / transported-binomial relations at all orders — 2026-10-08

Dated research record.  Global Krenn–Gu status: **UNRESOLVED**.  No frontier
change is proposed (this note does not edit `docs/current-frontier.md`; see
the last section for why).  Evidence labels: **[PROVED]** mathematical proof in
the linked theorem document; **[EXACT]** exact-arithmetic computation by a
listed script, primary only, no independent audit; **[SOLVER]** SAT status
without a checked proof; **[CONJECTURE]**; **[OBSERVATION]** a reading of
committed documents.

Inputs: the trunk record on `origin/claude/trunk-attempt-record-20261008`
(`docs/strategy/trunk-level-attempt-2026-10-08.md`), the source-cancellation,
physical-support and source-module notes of 2026-09-13/14, the row-space
discovery/packing tools, the n=6 row-space fixture, the 25-literal identity and
the two-slice transfer theorem (ST20).

## (1) What a row-space / transported-binomial relation is

Fix a support `S` (which entries `W_ij[a,b]` and, in the recursive version,
which induced coefficients `T_{W[A]}(w)` are nonzero).  Every coefficient
satisfies a Laplace identity along any vertex `v in A`,

```text
T_{W[A]}(w) = sum_{u in A-v} W_vu[w_v, w_u] T_{W[A-v-u]}(w),    T_{W[V]} = Delta.
```

Treat the nonzero entries and nonzero coefficients as coordinates `X` of a
complex torus.  Each identity is then a linear relation among Laurent
monomials.  [OBSERVATION]  The repository's mechanisms are:

- **binomial**: an identity with exactly two live terms (a zero result with
  two live products, or a nonzero result with one) gives `X^r = +-1`;
- **transport**: integer combinations of binomial exponent rows give
  `X^m = c X^{m'}` whenever `m - m'` lies in the lattice `Lambda` they span;
  an odd sign on a lattice relation `sum k_i r_i = 0` is a contradiction
  ("odd circuit");
- **row space**: after replacing each monomial by `c * Y_[class]`
  (`class` = coset of `Lambda`), rational combinations of the identities that
  isolate one class (`Y = 0`) are contradictions, and those isolating two
  classes are new binomials, fed back into `Lambda`.

So, plainly: a row-space relation is a consequence of the Laplace identities
of `T_W` and its sub-configurations that is **linear in the supported terms
after quotienting by the multiplicative relations forced by two-term
identities**.  The closure of the full-word version (subcoefficients not used)
is implemented exactly in `tools/explore/binomial_linear_closure.py` and
called BL below.

## (2) Validity at every order

- **[PROVED] Soundness is all-order and trivial.**  Laplace expansion and the
  matching expansion are polynomial identities for every `n`; dividing by a
  coordinate that the support declares nonzero is legitimate on the torus.
  So every transported-binomial or row-space deduction from a support `S` is a
  valid consequence of `T_W = Delta` for every witness with support `S`, at
  every even `n`.  The repository proves instances only because it applies
  the schema to particular supports; there is nothing further to prove for
  the schema itself.
- **What is inherently not all-order** is the *premise*: which identities are
  two-term depends on the support, and no theorem supplies a two-term
  identity from an arbitrary witness.  The schema is support-relative, not
  finite.
- **[PROVED] Two uniform families** extracted from the mechanisms are written
  as all-order division-free theorems in
  [`TWO_TERM_RELATION_CLOSURE_THEOREMS.md`](../../claims/arbitrary-order/TWO_TERM_RELATION_CLOSURE_THEOREMS.md):
  the *two-matching grid* (Theorem A; one nonzero corner monomial suffices)
  and the *odd opposite-ratio cycle* (Theorem B, any odd length).
- **[PROVED] Completeness on binomial supports** (Theorem C): if every mixed
  fibre has 0 or 2 live matchings and every constant fibre one, a witness with
  that support exists iff there is no odd sign circuit.  On this class the
  Krenn–Gu conjecture is exactly a combinatorial odd-circuit statement.
- **[PROVED] Inertness** (Theorem D): if every nonempty mixed fibre has at
  least three live matchings, the full-word closure derives nothing.  The full
  support satisfies this at every `n >= 4`.

## (3) The 27-entry six-vertex pattern

Pattern (as given): `01: 00 20 | 02: 11 | 03: 00 20 | 04: 02 22 |
05: 00 02 20 22 | 12: 00 02 | 13: 22 | 14: 11 | 15: 20 | 23: 00 20 |
24: 02 22 | 25: 00 02 20 22 | 34: 20 | 35: 11 | 45: 00`.

[EXACT] Of the 729 words, 691 have no live matching, 37 have exactly two and
`111111` has one; so every fibre has at most two terms and the single-term
conditions hold.  Two-term relations kill it **three independent ways**:

1. **Odd ratio triangle (mixed words only).**  Put `a=W03[2,0]`,
   `f=W04[2,2]`, `c=W05[2,0]` (vertex 0 in colour 2) and `d=W23[2,0]`,
   `e=W24[2,2]`, `b=W25[2,0]` (vertex 2 in colour 2).  The words
   `212010, 222020, 222220` each have exactly two live matchings, with common
   factors `W14[1,1], W15[2,0], W13[2,2]`, and give

   ```text
   ab = -cd,    ae = -fd,    fb = -ce.
   ```

   The first two give `fb = ce`; with the third, `2ce = 0`.  In ratio form,
   the three slot ratios `W0k/W2k` (k = 3,4,5) are pairwise opposite around a
   triangle.  This is Theorem B with `k = 3`; it is exactly the repository's
   coloured-slot parity mechanism.
2. **Two-matching grid at `000000`.**  With `P={0}`, `Q={2}`, background 0 on
   `{1,3,4,5}`, the words `000000, 002000, 200000, 202000` all have exactly the
   matchings `{01,23,45}` and `{03,12,45}`; the three mixed ones force the
   ratio at `000000` to be `-1`, so `T(000000) = 0`.  Theorem A needs only the
   five zeros `W13,W14,W15,W34,W35` at `[0,0]` and `W01[2,0]W23[2,0]W45[0,0] != 0`.
3. **Two-matching grid at `222222`**, symmetric, with guard
   `W14,W15,W34,W35,W45` at `[2,2]`.

The full-word closure finds the triangle first (round one, lattice value
`-1`).  [OBSERVATION] Neither mechanism is in the trunk record's Boolean model
(it has no ratio-parity or quotient clauses), which is why the pattern survived
there; both are in the eight-vertex programme.

## (4) The sharpest all-order lemma of this kind, and what blocks it

**What would be load-bearing.**  A family of relations valid at every `n`
refuting every support that survives the single-term conditions
((L), (F'), (G), killers).  The experiments below locate exactly how far
two-term relations go.

- **[PROVED] Without the killer theorem, no full-word two-term family can
  work, at any order.**  The full support passes (L), (F'), (G) (trunk record)
  and, by Theorem D, gives the full-word closure nothing.  So the trunk lemma
  must contain a relation among at least three supported terms, or use the
  killer theorem (which the full support violates).  [OBSERVATION, not
  proved] On the recursive branch where every induced coefficient is nonzero,
  the only two-term Laplace identities are the `|A| = 2` identifications, so
  the recursive lattice also has no transport; whether its row space alone
  derives anything there was not checked.
- **[SOLVER] With killers, two-term fibres are forced at n = 6.**
  `tools/explore/find_two_term_free_support.py --killers` reports UNSAT: no
  six-vertex support satisfying the single-term conditions and the killer
  condition has every nonempty mixed fibre of size at least three.  (CaDiCaL
  status only; no DRAT proof was produced.)
- **[EXACT + SOLVER] Two-term relations still do not suffice at n = 6.**
  `tools/explore/bl_support_cegar.py --killers` (SAT over physical supports
  with the single-term and killer conditions, each model tested by the
  full-word closure, cuts shrunk to 2–8 words and closed under all 4,320
  vertex/common-colour relabellings) refuted 58 supports and then returned a
  **51-entry survivor** (`tests/fixtures/bl_full_word_survivor_n6_51.json`):

  ```text
  01: 02 12 22 | 02: all | 03: all | 04: 00 10 20 | 05: 11 | 12: 20 21 22
  13: 22 | 14: 11 | 15: 00 | 23: all | 24: 00 | 25: 01 11 21
  34: 00 10 20 | 35: 01 11 21 | 45: 22
  ```

  Its fibres have sizes 2 (62 words), 3 (39), 4 (6) and 6 (1); the closure
  stops after two rounds (lattice rank 27, 148 classes, row rank 46) with no
  contradiction.  The size coincides with the earlier recorded 51-entry
  six-vertex survivor; identity of the two supports was not checked.
- **[EXACT] What kills the survivor.**  The triangle `{0,2,3}` carries full
  blocks; each of `1, 4, 5` meets it in one colour `sigma = (2, 0, 1)`.  On the
  27 words with `(w1,w4,w5) = (2,0,1)` the full hafnian is the six-term
  permanent tensor
  `F = sum_pi c_{0,pi0} (x) c_{2,pi2} (x) c_{3,pi3}` of the vectors
  `c_tu = W_tu[., sigma(u)]`, three of which are coordinate vectors on a
  transversal (`c24 ~ e0`, `c05 ~ e1`, `c31 ~ e2`).  After a valid torus
  normalization the 27 equations generate an ideal containing the normalized
  `W13[2,2]`; by hand, two-term fibres give
  `r0=r1, p0=p2, q1=q2, q1=-p0 r0`, three-term fibres give
  `r0(p1-p0) = -1`, `q0 = -r0(1+p0)` and `r2 = r0(1+s p0)`, and substituting
  these **multiplied by monomials** (`p1`, `s p1`) into the six-term fibre at
  `w = 120201` leaves `2s = 0`.  So the first relation beyond the closure
  multiplies three-term relations by monomials of degree at most two in the
  normalized coordinates (hand derivation; the verifier checks only the ideal
  membership).  (`claims/finite/n06/verify_51_entry_bl_survivor_slice.py`.)
  Slice contractions by annihilating covectors (the ST20 device) only
  reproduce two-term minors on this survivor; the decisive step is the
  product.

**Sharpest lemma that remains plausible — [CONJECTURE] uniform transported
Macaulay degree.**  Let `BL^D(S)` be the closure in which the row space is
taken over all products `mu * (fibre or Laplace identity)` with `mu` a monomial
of degree at most `D` in the supported coordinates (still modulo `Lambda`,
with binomial feedback).  `BL^0 = BL`.

> **(TM_D)** There is a `D`, independent of `n`, such that for every even
> `n >= 6` and every support satisfying (L), (F'), (G) and the killer
> condition, `BL^D(S)` contains a monomial (a contradiction).

Status of the pieces: `D = 0` fails at `n = 6` (the 51-entry survivor, full-word
version; the recursive version was not run on it).  `D <= 2` handles both
six-vertex obstructions recorded here (the 27-entry pattern at `D = 0`).  ST20 (two-slice transfer) is a
degree-two certificate valid at every `n` with `4(n-4)+2` zero premises, and
the eight-vertex 25-literal identity is of degree at most four in the
recursive coordinates.  Without the killer condition `TM_D` must also refute
the full support, where it reduces to a uniform-degree Nullstellensatz
statement for `T_W = Delta` itself; no evidence on that is recorded here.

What `TM_D` would need to be load-bearing: a proof that the `D`-bounded
certificate exists from the support conditions alone, i.e. an occurrence
theorem for a degree-`D` configuration like the permanent tensor above.  The
binomial-support case (Theorem C) shows the `D = 0` piece is an exact
odd-circuit occurrence problem; the general step is open.

## Commands

```text
python claims/arbitrary-order/verify_two_term_relation_closure_theorems.py
python claims/finite/n06/verify_27_entry_two_matching_grid.py
python claims/finite/n06/verify_51_entry_bl_survivor_slice.py
python tools/explore/binomial_linear_closure.py --pattern27
python tools/explore/binomial_linear_closure.py --support-json tests/fixtures/bl_full_word_survivor_n6_51.json
python tools/explore/binomial_linear_closure.py --n 4 --full
python tools/research/run_bounded.py --run-id <id> --timeout-seconds 900 --memory-mb 6144 -- python tools/explore/bl_support_cegar.py --killers --seconds 840 --output tmp/<new>.json
python tools/research/run_bounded.py --run-id <id> --timeout-seconds 600 --memory-mb 4096 -- python tools/explore/find_two_term_free_support.py --killers
```

Recorded runs: `bl-cegar-n6-killers-1` (BL_SURVIVOR after 59 models, 88.5 s,
216,000 cut images), `two-term-free-n6-k` (UNSAT).  The CEGAR is
model-order dependent; a different solver order may return a different
survivor.  Without the killer condition the first SAT model is the full
support, which the closure leaves CLOSED, consistent with Theorem D.

## Frontier

No frontier edge changes: Theorems A and B sharpen existing conditional
mechanisms, C and D are scope statements about a proof technique, and the
six-vertex results are exhibits inside an already proved order.  The
proposed next lemma `TM_D` is recorded here as a conjecture, not as a new
frontier node.
