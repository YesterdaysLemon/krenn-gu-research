# S156 is excluded by the diagonal-anchor lemma; the hub-2 trichotomy is not needed — 2026-10-09

This is a dated research record.  The global Krenn–Gu status is
**UNRESOLVED**, and nothing here changes it.  `docs/current-frontier.md` is
not edited; Section 7 says which rows are now stale.

Evidence labels:

- **[EXACT]**: a hand proof together with an exact integer polynomial
  identity checked by the committed verifier
  [`verify_s156_diagonal_anchor_exclusion.py`](../../claims/finite/n08/verify_s156_diagonal_anchor_exclusion.py)
  (sympy, 5 s).
- **[SAT-RUN]**: a bounded run of
  [`explore_general_block_recursive_support_model.py`](../../claims/finite/n08/explore_general_block_recursive_support_model.py).
  No DRAT proof is attached, so an UNSAT answer is evidence, not a proof.
- **[OBSERVATION]**: a reading or comparison, not a theorem.

## 1. Question and inputs

S156 is the 156-entry eight-vertex zero pattern of
[`hyperdeterminant-crossing-2026-10-09.md`](hyperdeterminant-crossing-2026-10-09.md),
Section 3.4.  It has sixteen full `3 x 3` blocks on a 4-regular graph `F` and
twelve single entries on the complementary cubic graph `H`.  The
realizability note
[`n8-support-realizability-2026-10-09.md`](n8-support-realizability-2026-10-09.md)
left it open, and the unmerged multi-partner note on branch
`claude/k4-grid-transport-20261009` (commit `de8754b7`,
`docs/strategy/multi-partner-grid-transport-2026-10-09.md`) proved a hub
trichotomy (a)/(b)/(c) at hub 2 and asked for each case to be made exact.

The brief for this note was: exclude S156 fibre-exactly, from the
equations, or find the exact reason it cannot be excluded locally.

Conventions are those of the model script: `W_ij[a,b]` for `i < j`, with
`a` the colour at `i`; `T_W(w)` sums over the 105 perfect matchings of
`K_8`.  For a vertex `v` and partner `u`, **row `c` at `v`** means the
vector `l_u = (W_vu[c, d])_d`, with the colour `c` at `v`.  A witness has
`T_W = GHZ` up to the torus: nonconstant words vanish and the constant word
`c^8` has value `lambda_c != 0`.

## 2. Summary

| object | verdict | evidence | mechanism |
|---|---|---|---|
| S156, exact support | **not realizable** | [EXACT] 16-word identity, for each of 10 tasks | diagonal anchor |
| S156, within support | excluded whenever, for one anchor-less task, the 4–5 named entries are nonzero | [EXACT] same identities | diagonal anchor |
| S128, exact support | not realizable (already known) | [EXACT] census: 11 anchor-less tasks | diagonal anchor (a second, independent reason) |
| proper sub-patterns of S156 | **undecided** | [SAT-RUN] timed out at 2,400 s (Section 5) | support model with anchors |
| hub-2 trichotomy (a)/(b)/(c) | not needed for the exact-support exclusion; not made exact | — | Section 4 |

**The single most load-bearing fact:** row 0 at vertex 2 of S156 meets only
the four full blocks `W_21, W_23, W_26, W_27` (its three `H` entries all have
colour 2 at vertex 2).  So no block at vertex 2 has row 0 equal to a nonzero
multiple of `e_0`.  The already-established diagonal-anchor lemma forbids
exactly this, through a 16-word identity.  The general-block recursive
support model that produced S156 (and S128) never encoded that lemma.

## 3. The diagonal-anchor exclusion  [EXACT]

### 3.1 The lemma

This is the "Diagonal-anchor refinement" of
[`docs/research-notes.md`](../research-notes.md), cited as the
diagonal-anchor theorem by the GHZ closure document.  It is restated here
because the whole argument rests on it.

**Lemma (diagonal anchor).**  At any witness, for every vertex `v` and
colour `c`, some partner `u` has row `c` at `v` equal to `alpha e_c` with
`alpha != 0`.

**Proof.**  For each `u != v` choose `y_u` in `ker(l_u)`.  Contract `T` with
`e_c` at `v` and with `y_u` at each `u`.  Every perfect matching contains
one edge `vu`, and that edge contributes the factor `l_u . y_u = 0`; the
other edges factor separately.  Hence, as a polynomial identity in `W`,

```text
sum_{w : w_v = c} T(w) * prod_{u != v} y_u[w_u] = 0.                       (*)
```

At a witness the only constant word in the sum is `c^8`, so the left side
equals `lambda_c * prod_u y_u[c]`.  If no `l_u` were a nonzero multiple of
`e_c`, each `ker(l_u)` would contain a vector with `y_u[c] != 0`, and the
product would be nonzero.  ∎

Verifier part A checks (*) as a polynomial identity on the generic `K_8`
configuration (252 independent entries, 128 words) for `(v, c) = (0, 0)`.

### 3.2 S156 has ten anchor-less tasks

On S156 every `F` block is full, so its row `c` has three nonzero entries
and is never an anchor.  An anchor must be an `H` single entry of the form
`(colour c at v, colour c at u)`.  Verifier part B lists the tasks with no
such entry:

```text
(0,2) (1,0) (2,0) (2,1) (3,2) (4,0) (4,2) (6,0) (6,1) (7,2)
```

Only vertex 5 has all three anchors (`W57[0,0]`, `W15[1,1]`, `W25[2,2]`).

### 3.3 The explicit identity at `(v, c) = (2, 0)`

Take polynomial kernel vectors:

- `y_u = W_2u(0,1) e_0 - W_2u(0,0) e_1` for `u` in `F(2) = {1, 3, 6, 7}`,
  where `W_2u(x, z)` is the entry with colour `x` at 2 and `z` at `u`;
- `y_u = e_0` for `u` in `{0, 4, 5}`, whose row 0 at vertex 2 is zero on
  S156.

Then (*) is a sum over 16 words.  Write `w_s` for the word with colour 0 at
vertices 0, 2, 4, 5 and colour `s_u` in `{0, 1}` at `u` in `{1, 3, 6, 7}`.
With every entry outside S156 set to zero, the verifier checks exactly that

```text
T(0^8) * W12[1,0] W23[0,1] W26[0,1] W27[0,1]
    = sum_{s != 0} (-1)^(|s|+1) T(w_s) * prod_{s_u = 0} W_2u(0,1) * prod_{s_u = 1} W_2u(0,0).
```

The fifteen words on the right are nonconstant.  At a witness the right
side is 0 and `T(0^8) = lambda_0 != 0`.  So

```text
W12[1,0] * W23[0,1] * W26[0,1] * W27[0,1] = 0
```

at every witness supported within S156.  `T(0^8)` restricted to S156 is a
nonzero polynomial with 21 monomials, so the identity is not vacuous.

### 3.4 The other nine tasks

Part C builds the analogous identity for every anchor-less task.  On a
full row it uses `y_u = W(c, d_u) e_c - W(c, c) e_{d_u}`, with `d_u` the
least off-diagonal colour.  On a row whose only entry is off-diagonal it
uses `y_u = W(c, d) e_c`, and on a zero row `y_u = e_c`.  Each identity is
exact on S156, has 16 words, and its constant-word coefficient is a product
of support entries:

| task | entries forced to have product 0 |
|---|---|
| (0,2) | `W01[2,0] W05[2,0] W06[2,0] W07[2,0]` |
| (1,0) | `W01[1,0] W12[0,1] W13[0,1] W14[0,1]` |
| (2,0) | `W12[1,0] W23[0,1] W26[0,1] W27[0,1]` |
| (2,1) | `W12[0,1] W23[1,0] W26[1,0] W27[1,0]` |
| (3,2) | `W13[0,2] W23[0,2] W34[2,0] W35[2,0]` |
| (4,0) | `W14[1,0] W34[1,0] W45[0,1] W47[0,1]` |
| (4,2) | `W14[0,2] W34[0,2] W45[2,0] W47[2,0]` |
| (6,0) | `W06[1,0] W26[1,0] W46[1,0] W56[1,0] W67[0,1]` |
| (6,1) | `W06[0,1] W26[0,1] W56[0,1] W67[1,0]` |
| (7,2) | `W07[0,2] W27[0,2] W47[0,2] W67[0,2]` |

The `(6,0)` row includes the single entry `W46[1,0]`.  Its row 0 at vertex 6
is off-diagonal, so `y_4 = W46[1,0] e_0`.

### 3.5 Statement

**Proposition.**  Over every field, no configuration supported within S156
in which, for at least one of the ten tasks, the four or five entries of
Section 3.4 are nonzero has matching tensor `GHZ(8,3)` up to the torus.  In
particular S156 is not fibre-realizable with exact support.

The proof uses no division and no genericity.  It uses only the identity
(*), the GHZ values of 16 words, and the zero pattern of S156 on the rows
named.

**Scope.**  This is a finite statement about one Boolean pattern.  It does
not exclude configurations supported within S156 in which every one of the
ten tasks has a degenerate `F` row.  The lemma then forces, for each task
`(v, c)`, an `F` block at `v` whose row `c` is `alpha e_c`.  That is two
zeros per task.  One off-diagonal entry `(v:c, u:d)` can serve at most two
tasks, `(v, c)` and `(u, d)`, so such a configuration has at least ten
zeros inside S156, hence at most 146 nonzero entries.  It is a different
zero pattern, which must pass the support model on its own (Section 5).

### 3.6 S128 and the six-vertex patterns  [OBSERVATION; census only]

The same census on S128, already excluded by the four-word `H3` identity,
finds eleven anchor-less tasks:

```text
(1,1) (1,2) (2,0) (2,1) (3,1) (3,2) (4,1) (4,2) (5,2) (6,1) (7,2)
```

So S128 is also excluded with exact support by the anchor lemma.  That is a
second, independent reason; no identity for S128 is committed.  On the
six-vertex survivor patterns embedded in the model script, P27 has four
anchor-less tasks, P63 has twelve, and P41 satisfies every anchor (scratch
census, not committed).

## 4. The hub trichotomy, and why both routes missed the anchor  [OBSERVATION]

The brief asked for the three cases of the hub-2 trichotomy to be made
exact.  For exact support this is no longer needed: Section 3 excludes
S156 without any case split.  The cases (a), (b) and (c) were **not** made
exact here, and no local-satisfiability computation was run for them.  The
brief's item 2 (find the smallest inconsistent subsystem if a case
survives) has a direct answer instead.  The 16 words of Section 3.3 are
inconsistent with the exact support of S156.  They are one constant word
and fifteen nonconstant words, all with colour 0 at vertices 0, 2, 4 and 5.
Minimality of this 16-word set was not examined.

Why the earlier tools did not see it:

- **Hub flattening (Lemma 1 of the multi-partner note)** states
  `R_A Phi_c = 0` only for colourings `c` other than the constants `a^7`
  with `a` in `A`.  The trichotomy used `A = {0,1,2}` on the `H`-dead box
  `C_gamma`.  That box contains no constant word.  The anchor uses
  `A = {0}`, keeps the constant word `0^7`, and contracts the whole family
  `Phi_c` with a product test vector.  It needs the multilinear fact that
  `Phi_c(u, .)` does not depend on `c_u`, not only linear algebra on
  `Phi`.
- **The support model** encodes the column-killer theorem (`--killers`),
  which is the nonconstant, `|A| = 1` instance of Lemma 1.  It never encoded
  the pinned-row diagonal-anchor lemma, although that lemma has been in the
  research notes since before the model was written.  Both n = 8 survivors
  violate it.  The model script now has an `--anchors` flag (Section 5).
- **The trichotomy itself is still a valid necessary condition** on any
  witness supported within S156.  It is superseded only as a route to the
  exact-support exclusion.

## 5. Support-level follow-up runs  [SAT-RUN]

The model script gained two additive options in this change:

- `--anchors`: for every `(v, c)`, a clause that some block at `v` has row
  `c` supported exactly on colour `c`.  Soundness is the lemma of 3.1.  The
  independent checker `check_anchors` re-verifies decoded SAT models.
- `--within-pattern-file P`: `g = 0` outside the fixture `P`, `g` free inside.
  It requires `--no-symmetry`.

All runs used `tools/research/run_bounded.py`.

| run id | hypotheses | result |
|---|---|---|
| `s156tri-exact-ka` | `g` = S156 exactly, killers + anchors, no symmetry | **UNSAT**, 1.9 s (sanity check of the clause; the proof is Section 3) |
| `s156tri-n8-kapr` | general `n = 8`, killers + anchors + PR, repaired symmetry | **SAT**, 65 s, 1 round, checker PASS (including `check_anchors`); a 121-entry model, below |
| `s156tri-within-kahpr` | `g` within S156, killers + anchors + H2/H3 at all levels + PR, no symmetry | **inconclusive**: timed out at 2,400 s after 29 CEGAR rounds and 4.2 million lazy instances; every round still had 400–7,000 holonomy violations |
| `s156tri-n8-kahtoppr` | general `n = 8`, killers + anchors + top-level H2/H3 + PR, repaired symmetry | **inconclusive**: timed out at 2,400 s after 12 rounds and 3.3 million lazy instances |

So:

- Whether some proper sub-pattern of S156 survives the support model with
  anchors is **not decided**.  No such sub-pattern was found within the
  bound, and none was excluded.
- Anchors do not by themselves close the `n = 8` support model.  Killers,
  anchors and PR admit the following 121-entry model.  Whether it survives
  holonomy was not tested; the top-holonomy run that would have tested
  the family did not finish.

```text
01: ALL | 02: ALL | 03: ALL | 04: 00 10 20 | 05: 00 10 11 20 21 22 | 06: 11 | 07: 02 12 22
12: ALL | 13: ALL | 14: ALL | 15: 00 10 20 | 16: 02 12 22 | 17: 11 | 23: 00 10 20
24: 02 12 22 | 25: 22 | 26: 22 | 27: 01 11 21 | 34: 10 11 | 35: 11 | 36: 00
37: 22 | 45: 00 01 02 10 11 12 21 22 | 46: 22 | 47: 00 10 20 | 56: ALL | 57: 00 | 67: ALL
```

It is a support-level object only, recorded to show that the anchor clause
is not decisive on its own.  No weights were sought for it.

## 6. Status and scope

- **S156**: excluded fibre-exactly with exact support, and within support
  under the entry conditions of Section 3.5 [EXACT].  It is a finite
  statement about one Boolean pattern.  It uses an existing lemma, so it
  creates no new reduction edge.
- The **diagonal-anchor lemma** is not new; it is restated and its
  polynomial identity checked generically (verifier part A).  There is no
  independent audit and no Lean formalization.
- The **hub trichotomy** of the multi-partner note remains a valid,
  unexercised necessary condition.  It was not made exact here.
- Nothing here concerns unrestricted `n = 8` configurations, except
  through the support-model runs of Section 5, which carry no proof trace.

## 7. Frontier

`docs/current-frontier.md` is **not edited** in this commit; the
integration owner should update two rows, which now misdescribe S156:

- the `SL6` boundary row ("the 156-entry one survives every encoded family
  and every closure test tried");
- the eight-vertex refuted-route row ("the 156-entry pattern satisfies
  killers, holonomy at every level and plane rigidity ...; the named sharper
  lemma is a multi-partner (`k = 4`) grid-rank transport").

Suggested replacement fact: both recorded `n = 8` survivors violate the
diagonal-anchor lemma, which the support model did not encode, so both are
excluded fibre-exactly with exact support (S156 by a 16-word anchor
identity).  With anchors added, killers + anchors + PR is still SAT at
`n = 8` (121-entry model), and the runs with holonomy were inconclusive
(Section 5).  No theorem, branch closure or
reduction edge changes, so no node or edge of the proof topology changes.

## 8. Commands and runs

```text
python claims/finite/n08/verify_s156_diagonal_anchor_exclusion.py
```

Model runs (the fixture `pattern_S156.json` is the S156 listing in
`physical-support-v1` form, written to an untracked scratch directory):

```text
python tools/research/run_bounded.py --run-id s156tri-exact-ka --timeout-seconds 600 --memory-mb 8000 -- \
  python claims/finite/n08/explore_general_block_recursive_support_model.py 8 --pattern-file pattern_S156.json \
  --no-symmetry --killers --anchors                                                    # UNSAT, 1.9 s
python tools/research/run_bounded.py --run-id s156tri-n8-kapr --timeout-seconds 1800 --memory-mb 12000 -- \
  python claims/finite/n08/explore_general_block_recursive_support_model.py 8 --killers --anchors --plane-rigidity
                                                                                       # SAT, 65 s, 121 entries
python tools/research/run_bounded.py --run-id s156tri-within-kahpr --timeout-seconds 2400 --memory-mb 12000 -- \
  python claims/finite/n08/explore_general_block_recursive_support_model.py 8 --within-pattern-file pattern_S156.json \
  --no-symmetry --killers --anchors --holonomy --plane-rigidity --proof proof_within  # timeout, 29 rounds
python tools/research/run_bounded.py --run-id s156tri-n8-kahtoppr --timeout-seconds 2400 --memory-mb 14000 -- \
  python claims/finite/n08/explore_general_block_recursive_support_model.py 8 --killers --anchors \
  --holonomy-top-only --plane-rigidity                                                 # timeout, 12 rounds
```

The base DIMACS of the within-S156 run has SHA-256
`73972a41cccdd5b042771fd2ce45d6fb46c1ae45c32e24e52727fe694cc301cf`.  Total
compute was about 82 minutes.  No WSL or Singular job was used, and no
process was left running.
