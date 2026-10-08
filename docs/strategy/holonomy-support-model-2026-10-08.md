# Holonomy-strengthened support model — 2026-10-08

This is a dated research record of a bounded SAT experiment, not a theorem,
frontier entry, or change of status.  The global Krenn–Gu conjecture remains
**UNRESOLVED**.  `docs/current-frontier.md` is not edited: no order is closed
and no reduction edge is created (see Section 6).

## 1. Question

The general-block recursive support model (GSM) of
`claims/finite/n08/explore_general_block_recursive_support_model.py` is SAT
at `n = 6` and `n = 8`, although six vertices is a proved exclusion.  The
script and its record `docs/strategy/trunk-level-attempt-2026-10-08.md` come
from branch `claude/trunk-attempt-record-20261008`.  The script is carried
here with a symmetry-breaking repair (Section 5.1); the record is not
carried.  The three six-vertex survivor patterns `P27`, `P41`, `P63` were
refuted exactly by two-term "holonomy" relations.  The refutations are in
`claims/finite/n06/SIX_VERTEX_SUPPORT_SURVIVOR_PATTERNS_EXACT_REFUTATION.md`
(Lemmas A and B), on branch `claude/n6-pattern-refutation-20261008`.  Question: does adding those relations to the GSM, as valid
support-level clause families, make the model UNSAT at `n = 6` or `n = 8`?

## 2. Notation and the exact identity used

`W_ij` in `C^{3x3}` (`i < j`), `W_ji = W_ij^T`.  For an even vertex set `A`
and a word `w` on `A`, `T_A(w)` is the matching sum of `W` restricted to `A`
(`T_{} = 1`).  For every `p in A` the Laplace (row) expansion is the exact
identity

```text
T_A(w) = sum_{u in A - p}  W_pu[w_p, w_u] * T_{A - {p,u}}(w|).          (1)
```

The term of `u` is **live** iff `W_pu[w_p,w_u] != 0` and
`T_{A-{p,u}}(w|) != 0`; a non-live term is exactly `0`.  The GSM variables
are interpreted semantically: `g` = entry nonzero, `m[A,w]` =
`T_A(w) != 0`, `t[A,w,p,u]` = term live.  "Live set of `(A,w)` at `p`" means
`{u : t[A,w,p,u]}`.  Lemmas A' and B' below hold for **every** `W` (not only
witnesses) and every `n`; they never use the GHZ target.  A witness adds only
`m[V,w] = [w constant]`.

## 3. Statements encoded and their proofs

### Lemma A' (signed `K_{2,3}` balance) — rule `H2`

Fix hub data `h = (p, c_p, q, c_q)`, `p != q`.  For a vertex `k` not in
`{p,q}` and a colour `c_k`, put `r_k = W_pk[c_p,c_k] / W_qk[c_q,c_k]` when both
entries are nonzero.  Let `Gamma_h` be the graph on the nodes `(k, c_k)` with
an edge `{(a,c_a),(b,c_b)}` whenever some even `A` containing `p,q,a,b` and a
word `w` on `A` with those colours at `p,q,a,b` satisfy:

1. `T_A(w) = 0`;
2. the live set at `p` is exactly `{a, b}`;
3. the live set of `(A - {p,a}, w|)` at `q` is exactly `{b}`, and the live set
   of `(A - {p,b}, w|)` at `q` is exactly `{a}`.

Then every edge has `r_a = -r_b` with both sides defined, and `Gamma_h` is
bipartite.

*Proof.*  By (1) at `p` and condition 2,
`0 = X_a H_a + X_b H_b`, with `X_k = W_pk[c_p,c_k]` and
`H_k = T_{A-{p,k}}(w|)`.  By (1) at `q` and condition 3,
`H_a = Y_b S` and `H_b = Y_a S`, with `Y_k = W_qk[c_q,c_k]` and
`S = T_{A-{p,q,a,b}}(w|)`.  Both remainders are the same set and word.
Liveness gives `X_a, X_b, Y_a, Y_b, S != 0`.  Hence
`S (X_a Y_b + X_b Y_a) = 0`, so `r_a = -r_b`, both nonzero.  In one connected
component fix a node value `r_0 != 0`.  Every node then has value `+r_0` or
`-r_0`, and every edge joins opposite values.  Since `r_0 != -r_0`
(characteristic 0), the sign is a proper 2-colouring.  QED.

The document's Lemma A (odd triangle with matching-level liveness) is a
special case.  If a word has exactly two live matchings
`{pa_i, qa_j} + N` and `{pa_j, qa_i} + N`, then conditions 1–3 hold:
`A - {p, a_i}` has exactly one live matching, so its coefficient is a
nonzero monomial, and every other partner of `p` or `q` has no live matching
and a zero term.

**Encoding.**  One sign variable `sigma[h, k, c_k]` per node (hub pair stored
with `p < q`; `r` is replaced by `1/r` under the swap, which preserves
`r_a = -r_b`).  For each instance, `premise -> sigma_a != sigma_b` as two
clauses, where the premise is `not m[A,w]` plus the exact live sets of
conditions 2 and 3 written in `t`/`g` literals.  This excludes **every** odd
cycle of `Gamma_h`, not only triangles.

### Lemma B' (rank-one grid transport) — rule `H3`

Fix an even `A`, a vertex `p in A`, two partners `k1 != k2` of `p`, and an
unordered pair of distinct "varied" vertices `{u, v}` of `A` such that
`|{u,v} ∩ {p, k_i}| = 1` for `i = 1, 2`.  Fix the colours of `A - {u,v}`.
Write `w_xy` for the word with colour `x` at `u` and `y` at `v`.  The two
shapes are:

- I: `p` is not in `{u,v}` and `{k1,k2} = {u,v}`;
- II: `p = u` and `v` is not in `{k1,k2}`.

In both shapes each of the two terms of (1) factors as `f_i(x) g_i(y)`: one
varied vertex lies in the edge `p k_i`, the other in the remainder
`A - {p, k_i}`.  So `R(x,y) = term_k1 / term_k2 = alpha(x) beta(y)` wherever
both terms are nonzero.  Let `E` be the set of corners `(x,y)` with
`T_A(w_xy) = 0` and live set at `p` exactly `{k1,k2}`.  On `E`, `R = -1`.
If `x` and `y` are connected in the bipartite graph `(rows, columns, E)`,
then at `w_xy` both terms are nonzero and `R(x,y) = -1`.  The reason is that
along a path `x = x_0, y_0, x_1, ..., x_m, y_m = y` the alternating product
of `R` over its `2m+1` edges equals `alpha(x) beta(y)`, and the path gives
nonzero `f_i(x)`, `g_i(y)`.  So the two terms cancel exactly, and

```text
T_A(w_xy) = sum of the live terms at p other than k1, k2.
```

Consequences (encoded): both terms are live; if `T_A(w_xy) != 0` then some
other partner is live; if `T_A(w_xy) = 0` then the number of other live
partners is not one.

**Encoding.**  One variable `CAN[fam, (x,y)]` per family and corner,
meaning "both terms nonzero and they cancel".  The clauses are:

- edge: `premise(E) -> CAN`;
- square: `CAN(x,y) & CAN(x,y') & CAN(x',y) -> CAN(x',y')`, whose iteration
  is exactly path-connectivity in a `3 x 3` grid;
- consequence: as listed above, in `t` and `m` literals.

The document's Lemma B is stated for **matching** terms and is not encoded
literally.  `H3` is its analogue for Laplace terms.  The P63 square of the
refutation document (vertices 2 and 5) is a Shape II instance at `p = 2`
with partners `{1, 3}`: these are the GSM terms carrying the matchings
`{12,..}` and `{23,..}`, and the extra term at the fourth corner is
partner 5.

### What is not encoded

- The full binomial-propagation calculus of the refutation document
  (arbitrary torus-lattice relations) is not encoded.  Neither is the
  transport of a `Gamma_h` path ratio into a longer equation ("transported
  `K_{2,3}`"), nor matching-level squares that are not GSM-level grids.
- Equations with three or more live terms contribute only through
  (L)/(F') and the `H3` consequences.

## 4. Implementation and soundness of the search

The flags are `--holonomy` (both rules, every level `|A| >= 4`),
`--holonomy-top-only` (only `A = V`), `--holonomy-rules H2|H3|H2,H3`, and
`--pattern P27|P41|P63` (fix every `g`, validation only, with
`--no-symmetry`).  `--max-entries K` adds a cardinality bound.  The holonomy
clauses are added lazily (CEGAR).  The loop solves, decodes `g` and `m`,
runs the independent checker `check_holonomy`, and, on a violation, adds the
clauses of every `H2`/`H3` instance whose premises hold in the model.  Every
added clause is an instance of Lemma A' or B', so an UNSAT answer is UNSAT
for a sub-formula of a valid formula.  A SAT answer is accepted only when
`check_model` ((L), (F'), (G)) and `check_holonomy` both pass.

`check_holonomy` works from the decoded supports only.  It rebuilds the
`Gamma_h` graphs and the grids without SAT variables, tests bipartiteness by
BFS 2-colouring, and closes the grids by square completion (the encoder uses
union-find).  It is a separate implementation of the same rule, **not an
independent audit** of the lemmas.  The symmetry breaking stays sound
because both rule families are invariant under vertex relabelling and colour
permutation.

Soundness smoke test (scratch, not committed): for 1,300 random sparse
integer configurations at `n = 4, 6` (entries in `{±1}` or `{±1,±2}`,
densities 0.25–0.5), every `T_A(w)` was computed exactly and its zero pattern
was used as `m`.  The checker reported no violation of (L), (F'), `H2`, `H3`.
In those configurations the rules fired on about 208,000 `H2` edges and
786,000 `H3` grid edges, with 2,191 transported corners.  This is evidence
for correct implementation, not a proof; the proofs are Section 3.

## 5. Results

CaDiCaL 1.5.3 via python-sat on Windows, wall-clock times.  Runs over 60 s
went through `tools/research/run_bounded.py`.

### 5.1 Integrity finding: the inherited symmetry breaking was unsound

The inherited script derived its lex-leader chain variables from
`("eq", id(image), key)`.  The three endpoint-swap generators are
loop-local closures.  After garbage collection CPython gave them the same
`id`, so the three generators shared one chain of auxiliary variables.  The
encoding at `n = 6` has two distinct generator keys instead of four.  The
shared chains impose conflicting definitions, so the symmetry clauses are
**stronger than lex-leader** and can exclude every member of an orbit.

Observed consequences:

- `6 --killers --holonomy` with the inherited symmetry: **UNSAT**, 75 s.
  Without symmetry the same formula is **SAT** (Section 5.3).  The UNSAT
  answer is an artifact and is withdrawn here.  Glucose 4 also returns
  UNSAT on the dumped CNF (35 s), which confirms only that the artifact is
  not a solver error.
- The trunk record's claim "minimum 27 nonzero entries (26 is UNSAT)" under
  killers comes from the same symmetry clauses.  It is **refuted**:
  `6 --killers --max-entries 26` is SAT both with repaired symmetry and with
  `--no-symmetry`.  Both runs found **23-entry** models, and the
  independent checker passed.  The exact minimum was not determined:
  bounded `--no-symmetry` probes at 22, 20 and 18 were stopped after about 40 minutes without an answer.  The earlier "minimum 27 entries" figure was produced by the faulty symmetry block and is **not established**; neither is any other minimum.
  The trunk record's SAT results are unaffected, because SAT models are
  re-checked without the symmetry clauses.

Repair: each generator gets an explicit unique key, `("swap", a, b)` or
`"colour12"`.  The encoding then has four generator chains.  Every result
below uses the repaired symmetry or `--no-symmetry`.  Re-validation with the repair: `n = 4` is SAT with and without symmetry, with and without killers and holonomy.  At `n = 6` (killers + H2 + H3) the repaired-symmetry run and the symmetry-free run agree (both SAT).  A coordinator review reports the same `id(image)` pattern in the AP' encoder; that encoder is outside this branch and was not touched.

### 5.2 Validation

| run | result | time | note |
|---|---|---|---|
| `4 --holonomy` | SAT | <0.1 s | full 54-entry support; no instance fires; checker PASS |
| `4 --holonomy --killers` | SAT | <0.1 s | 6-entry GHZ-type witness pattern; checker PASS |
| `6 --pattern P27 --killers --no-symmetry` (no holonomy) | SAT | 0.1 s | survivor confirmed |
| same, `--holonomy` | **UNSAT** | 0.3 s | 2 rounds; H2 alone UNSAT, H3 alone UNSAT |
| `6 --pattern P41 ...` (no holonomy) | SAT | 0.1 s | survivor confirmed |
| same, `--holonomy` | **UNSAT** | 0.4 s | H2 alone UNSAT; H3 alone SAT (matches "no refuting square") |
| `6 --pattern P63 ...` (no holonomy) | SAT | 0.1 s | survivor confirmed |
| same, `--holonomy` | **UNSAT** | 1.2 s | H3 alone UNSAT; H2 alone SAT (matches "binomial subsystem consistent") |

`--holonomy-top-only` also refutes all three patterns.  The split by rule
reproduces the T2/T3 classification of the refutation document exactly.

### 5.3 Main runs

| n | hypotheses | symmetry | result | time | rounds / instances | model |
|---|---|---|---|---|---|---|
| 6 | (L)(F')(G) + H2 + H3 | inherited* | SAT | 0.2 s | 1 / 0 | dense 135 entries (valid: SAT models are checked) |
| 6 | + killers + H2 + H3 | repaired | **SAT** | 24 s | 9 / 205,072 | 51 entries, checker PASS |
| 6 | + killers + H2 + H3 | none | **SAT** | 174–197 s | 13 / 472,102 | 50 entries, checker PASS |
| 6 | + killers + H2 only | inherited* | SAT | 8 s | 2 / 544 | 63 entries (P63-type) |
| 6 | + killers + H3 only | inherited* | SAT | 5 s | 1 / 0 | exactly P41 |
| 8 | (L)(F')(G) + H2 + H3 | inherited* | SAT | 4.7 s (+10 s encode) | 1 / 0 | dense 252 entries |
| 8 | + killers + H2 + H3 | repaired | **inconclusive** (stopped) | 1,816 s at last round | 26 / 8,036,317 | each round still found 2,000–12,000 violations; 10.9 GB resident when stopped |

*A SAT answer under the inherited symmetry clauses is still valid, because
those clauses only add constraints and the model is re-checked.  Base sizes:
`n = 6` has 38,620 variables and 156,412 clauses before symmetry and
holonomy; `n = 8` has 1,081,560 variables and 4,400,752 clauses with
killers.

The holonomy rules cannot act on dense supports.  A dense support has no
two-term Laplace equation, so (a) without killers is SAT at both orders for
a structural reason.

### 5.4 The surviving six-vertex pattern

Repaired-symmetry run, `6 --killers --holonomy`, 51 entries (`ij: ab` =
colour `a` at `i`, colour `b` at `j`; `ALL` = all nine entries):

```text
01: ALL        02: 00 10 20   03: ALL        04: 22         05: 01 11 21
12: 00 10 20   13: ALL        14: 02 12 22   15: 11         23: 00
24: 11         25: 22         34: 02 12 22   35: 01 11 21   45: 00
```

It is an inner triangle `{0,1,3}` with full blocks and an outer triangle
`{2,4,5}`.  Each outer vertex has one "inner" colour (`2:0`, `4:2`, `5:1`),
joined to the inner triangle by killer columns.  Its two "outer" colours
are joined only around the outer triangle (`24: 11`, `25: 22`, `45: 00`).
The exact binomial-propagation calculus of
refutation document's verifier (imported unchanged from that branch) gives
the following census:

```text
census (live terms, constant): {(0,F): 621, (2,F): 62, (3,F): 36, (3,T): 3, (4,F): 6, (6,F): 1}
forbidden binomials 62, integer relations 35, odd relations 0
binomial-propagation calculus: no contradiction
```

So this pattern is **not refuted by T2/T3 at all**, even at matching level.
It needs a relation of a further type.  The 27 words with the outer
vertices at their inner colours give the clearest view.  There `T_W` is
the `3 x 3` permanent of the inner-to-outer matrix
`P[i,o] = W_io[c_i, inner colour of o]`, with rows

```text
row_0(c) = (W02[c,0], [c=2] W04[2,2], W05[c,1])
row_1(c) = (W12[c,0], W14[c,2], [c=1] W15[1,1])
row_3(c) = ([c=0] W23[0,0], W34[c,2], W35[c,1])
```

All 27 permanents vanish.  The two-term ones give the rank-one ratios
`(W02/W05)`, `(W14/W12)`, `(W35/W34)` with product `-1`.  This the calculus
does see, and it is consistent.  The remaining equations have three or
more terms and are not closed by merging.  The relation this pattern needs
is therefore of **multilinear (row-space) type**: the vanishing of a
trilinear form (the permanent) on the product of the three row families.
This is the type used by the repository's eight-vertex row-space
refutations.

This block alone already kills the pattern.  A sympy Gröbner basis (grevlex,
over `Q`) was computed for the 27 block equations in their 21 unknowns,
together with the saturation equation `t * prod(unknowns) - 1`.  It is `[1]`
(369 s).  The 27 equations have 2–6 live terms each.  So the pattern has no
solution with all its entries nonzero.  This is an exact computation with
one tool.  It was run from a scratch script, not committed, and has no
independent check.  It is not packaged as a claim.  The six-vertex theorem
already covers this pattern.

The no-symmetry run's 50-entry survivor has the same inner/outer shape, on
the inner triangle `{0,1,5}`:

```text
01: ALL  02: 01 11 21  03: 02 12 22  04: 00  05: all but 01  12: 01 11 21  13: 22
14: 00 10 20  15: ALL  23: 00  24: 22  25: 11  34: 11  35: 20 21 22  45: 00 01 02
```

The binomial-propagation calculus refutes it by a monomial kill after
merging, at word `011202`.  This is matching-level transport, which the
GSM-level rule H3 does not see.

## 6. Scope

- **Answer to (a):** at `n = 6` the strengthened model ((L), (F'), (G),
  killers, H2, H3, all levels) is **SAT**.  It is not a new six-vertex
  exclusion mechanism.  The six-vertex theorem is unaffected: it is proved
  separately and computer-assisted.
- **Answer to (b):** at `n = 8` it is SAT without killers (dense support).
  With killers the run is **inconclusive**.  The lazy loop was stopped after 26 rounds and 8.0 million added instances, with no SAT or UNSAT answer.  The lazy encoding does not scale to `n = 8` within this budget.  An eager top-level-only encoding, or a smarter instance selection, is the obvious next step.
- What is established: two support-level clause families, each proved valid
  for every `W` at every even order (Lemmas A', B').  The validation shows
  they reproduce the document's T2/T3 refutations of `P27`, `P41` and
  `P63` with no pattern-specific input.  There is also one surviving
  six-vertex pattern that is immune to the whole T2/T3 calculus.  That
  pattern locates the next relation type (multilinear/row-space) at the
  first order where it is needed.
- Integrity: the inherited symmetry breaking was unsound (Section 5.1), and
  the trunk record's "minimum 27 entries" claim is refuted.  The owner of
  that record should correct it.  This branch does not carry or edit it.
- Evidence modes: SAT answers are checked by a separate implementation of
  the same rules (`check_model`, `check_holonomy`).  That is not an
  independent audit.  No UNSAT result here is used as evidence.  No DRAT
  proofs were produced.  The soundness lemmas are proved by hand in Section
  3 and are not formalized.
- Frontier: unchanged.  No order is closed, no reduction edge is created,
  and no proof route is refuted, so `docs/current-frontier.md` needs no
  update.  Global status **UNRESOLVED**.

## 7. Commands

```text
python claims/finite/n08/explore_general_block_recursive_support_model.py 4 --holonomy [--killers]
python claims/finite/n08/explore_general_block_recursive_support_model.py 6 --holonomy --killers --no-symmetry --pattern P27   # P41, P63
python claims/finite/n08/explore_general_block_recursive_support_model.py 6 --holonomy --holonomy-rules H2 --killers --no-symmetry --pattern P63
python tools/research/run_bounded.py --run-id ID --timeout-seconds 3600 --memory-mb 6000 -- \
  python claims/finite/n08/explore_general_block_recursive_support_model.py 6 --killers --holonomy [--no-symmetry] --out OUT.json
python tools/research/run_bounded.py --run-id ID --timeout-seconds 5400 --memory-mb 16000 -- \
  python claims/finite/n08/explore_general_block_recursive_support_model.py 8 --killers --holonomy --out OUT.json
python claims/finite/n08/explore_general_block_recursive_support_model.py 6 --killers --max-entries 26 [--no-symmetry]
```
