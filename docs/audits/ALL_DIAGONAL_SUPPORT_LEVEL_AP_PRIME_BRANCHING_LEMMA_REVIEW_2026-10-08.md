# Adversarial review: AP-prime branching lemma, normalizations, and the n = 10 certificate (WB4)

Date: 2026-10-08

Reviewed package (the version on branch
`origin/claude/ap-prime-top-matching-20261008`, commit `281b2b28`, which adds
Section 8 to the version merged in PR #361):

- `claims/arbitrary-order/ALL_DIAGONAL_SUPPORT_LEVEL_AP_PRIME_BRANCHING_LEMMA_AND_PARENT_ATTEMPT.md`
- `claims/arbitrary-order/explore_all_diagonal_support_level_ap_prime_bounded_search.py`
- `claims/arbitrary-order/audit_all_diagonal_support_level_ap_prime_chain_normalized.py`
  (read only; not rerun)

Also consulted: WB2
(`ALL_DIAGONAL_SUPPORT_LEVEL_WEIGHTED_BOGDANOV_FINITE_EXCLUSION_THEOREM.md`, for
the AP' axioms), WB1 Step 10
(`ALL_DIAGONAL_WEIGHTED_BOGDANOV_MAXIMUM_DEGREE_FOUR_EXCLUSION_THEOREM.md`),
the RZP10 theorem
(`claims/finite/n10/TEN_VERTEX_ALL_DIAGONAL_RECURSIVE_HAFNIAN_EXCLUSION_THEOREM.md`),
and the registry entry `chandran-gajjala-illickan-2024-sparse-graphs` in
`catalog/literature/sources.json`.

## Independence disclosure

This is a **same-day review by one automated agent** (Claude), commissioned by
the coordinating agent of the run that produced WB4.  The reviewer did not
write WB4 or its scripts, but it is not an external referee, it ran on the
same host with the same toolchain, and it has not itself been reviewed.  Its
reproduction runs below are uncertified solver runs through `python-sat`; no
native solver or `drat-trim` replay was performed by the reviewer.

## Verdict

**The hand-proved content passes.  The finite `n = 10` certificate claim does
not, as stated: the DRAT-checked CNFs are not sound encodings of AP' under
Lemma 2, because the script's lex-leader block is implemented incorrectly.**

| item | verdict |
|---|---|
| (a) Lemma 1 (normalization) | PASS.  The (F') caveat is correct as a statement about the proof and about the per-colour axioms; "does not preserve" is unproved for full AP'+(F') models (see §1). |
| (b) Theorem 3, Step 1 | PASS.  Both directions are needed and both are proved. |
| (c) the Bogdanov/CGI import | PASS mathematically (the use is a special case of the reported statement, and the reviewer supplies a self-contained proof of that special case, §3).  Provenance defects: the locator "Theorem 1.7" does not match the arXiv rendering, and neither WB1 nor WB4 has a registry usage record. |
| (d) Lemma 2' and lex-leader compatibility | PASS mathematically (the hypothesis is invariant under every generator).  The encoded hypothesis is faithful.  But every lex-leader result, including `--branching`, inherits the defect of §6. |
| (e) Lemma 4 and the (F') ladder | PASS with two corrections: the identification RZP = AP'+(F') needs the unstated step "(L) and (a) imply (S)", and "strictly between" is unproved. |
| (f) cheap reproduction | PASS: `8` is UNSAT in 0.2 s; `8 --relax two_part_only` is SAT with `independent_check: PASS`. |
| **finite claim: AP' UNSAT at `n = 10` by a checked certificate** | **GAP.**  The pinned DIMACS files (SHA-256 `b74ec570…` and `1a96f77c…`) contain an unsound symmetry block (§6).  The DRAT traces certify the UNSAT of those CNFs, not AP' at `n = 10`. |

No counterexample was found.  A corrected encoding is UNSAT at `n = 6, 8`;
at `n = 10` it is UNSAT for AP'+(F') and timed out at the reviewer's
3,000 s cap for AP' (§6.4).  These runs are uncertified.  The sound support for
AP' at `n = 10` is currently WB4's uncertified run of the audit encoding,
which has no lex-leader clauses.  The global status
remains **UNRESOLVED**, and nothing in this review changes the status of WB1,
WB2, WB3, or RZP10.

## 1. Item (a): Lemma 1

Write `S'_c = R_c ∪ U_c`.  The inclusion `S'_c ⊆ S_c` uses `R_c ⊆ S_c` (by the
closure definition) and `U_c ⊆ S_c` (this is (F); the proof does not cite it
but it is immediate).

- (a): `∅ ∈ U_c`, `V ∈ R_c`; two-element members of `R_c` are edges by (a)
  for `S_c`; two-element members of `U_c` are exactly the edges.  Correct.
- (L) for `A ∈ R_c`: the original child lies in `S_c` and is reachable by the
  closure definition.  Correct.
- (L) for `A ∈ U_c`: if `N` is the unique perfect matching of `G_c[A]` and
  `v ∈ A`, then `N - vN(v)` is a perfect matching of `A - {v,N(v)}`, and a
  second one would extend by `vN(v)` to a second perfect matching of `A`.  So
  `A - {v,N(v)} ∈ U_c ⊆ S'_c` and `vN(v) ∈ G_c`.  The child need not be
  reachable and does not have to be.  **Correct; (L) is preserved for sets in
  `U_c`.**
- (S), (F), (H1), (H2): correct as written.

One point the document leaves implicit: the "consequently" sentence refers to
reachability *in the new model*.  That reachable family equals `R_c`: a
supported child in `S'_c` of a set in `R_c` is in particular in `S_c`, hence in
`R_c`, and conversely every `R_c` step lands in `R_c ⊆ S'_c`.  So the
corollary is correct.

**The (F') caveat.**  The text says that shrinking `S_c` "can create a set
outside `S'_c` with exactly one `S'_c`-child".  As a statement about the
per-colour axioms this is true; the reviewer found an explicit single-colour
instance at `n = 8`:

- `G = K_8 - {01}`;
- `S` = the empty set, the edges of `G`, every 6- and 8-subset of `V`, and
  every 4-subset except the four 4-subsets of `{3,4,5,6,7}` that contain `3`.

This satisfies (a), (L), (S), (F), (F') and `V ∈ S` (checked by brute force).
Since `01 ∉ G`, the set `A = {2,...,7}` is not reachable, and it has several
perfect matchings, so the normalization drops it.  In `S'`, at `v = 2` the
only supported child is `A - {2,3} = {4,5,6,7}` (reachable through
`V - {1,3}` and then the edge `02`), so (F') fails at `(A, 2)`.  No
three-colour AP'+(F') model is known at any `n >= 6`, so the stronger reading
"Lemma 1 fails for AP'+(F')" is unproved (and vacuous wherever AP'+(F') has no
models).  The safe wording is "the proof does not carry (F') across, and the
per-colour mechanism genuinely breaks it".  The search's refusal to combine
`--normalize` with `--fprime` is the correct conservative consequence.

## 2. Item (b): Theorem 3, Step 1

*Forward direction.*  Let `F' = {A ∈ R_c : A = V - ∪J for some J ⊆ M_c}`.
`V ∈ F'`.  If `A ∈ F'` and `A - e` is a supported child, then `A - e ∈ R_c` by
closure, so `e ∈ M_c` by the definition of `M_c`; `e ⊆ A` is disjoint from
`∪J`, so `A - e = V - ∪(J ∪ {e})` with `J ∪ {e} ⊆ M_c`.  Thus `F'` contains
`V` and is closed under supported children, and minimality of `R_c` gives
`R_c ⊆ F'`.  This is exactly the document's "induction along the generating
closure"; it is airtight.  (That `M_c` is perfect uses (L) at `V` at every
vertex, which is stated.)

*Converse.*  It **is** needed: Step 4 uses `A_c = V - ∪(M_c - F) ∈ R_c` for an
arbitrary sub-matching `M_c - F`, and Step 2 uses `V - e ∈ R_c` for every
`e ∈ M_c`.  It is proved by induction on `|J|`: if `V - ∪J ∈ R_c` and
`e ∈ M_c - J`, pick `v ∈ e`; `v ∉ ∪J` because `M_c` is a matching; (L) gives a
supported child `V - ∪J - {v,u}`, which is reachable, so `vu ∈ M_c`, so
`vu = e`.  Correct.

Steps 2–4 were also checked: exclusivity uses only the two-part rainbow with
`n >= 4`; the union of three pairwise edge-disjoint perfect matchings is a
simple cubic graph with a proper 3-edge-colouring; `A_c = V(F ∩ M_c)` and
`V - A_c = V(M_c - F)` because `M_c` is perfect; at least two classes are
nonempty because a perfect matching contained in one `M_c` equals it.
The equivalence "`M_c` is a matching" ⇔ "`R_c` is generated by one perfect
matching" used in the "What the theorem says" paragraph also holds (if `R_c`
is generated by `N`, any step edge is the difference of two `N`-unions, hence
an `N`-edge).  The `n = 4` sharpness example (three colour classes of `K_4`)
satisfies every AP' axiom.  **PASS.**

## 3. Item (c): the imported nonmonochromatic-perfect-matching theorem

**What Step 3 needs.**  A simple cubic graph `K` on `n >= 6` vertices that is
the edge-disjoint union of three perfect matchings `M_0, M_1, M_2` has a
perfect matching other than the three `M_c`.  WB1 Step 10 uses exactly the
same statement (three pairwise disjoint perfect matchings `P_0, P_1, P_2`,
`n > 4`), with the same citation.  The two imports agree.

**What the source says.**  A fetch of the arXiv HTML rendering of
arXiv:2407.00303 (v1 is the only version; the MFCS 2024 paper is its
published form) shows the statement as **Theorem 7** in Section 1.2, reported
as an observation of Bogdanov with an informal web reference: in a coloured
multigraph with more than four vertices, if there are three monochromatic
perfect matchings of different colours, then there is a non-monochromatic
perfect matching.  This hypothesis is weaker than what WB1 and WB4 have (no
cubicity, simplicity, or disjointness needed), and "non-monochromatic" for a
graph whose edges are all monochromatic means "uses at least two colours",
i.e. "is not a colour class".  So the use is a special case.  This reading
was tool-mediated (an HTML fetch summarized by a model), not a PDF
inspection, and the MFCS PDF numbering was not checked.

**Provenance defects (not mathematical).**

1. The locator "Theorem 1.7" used by WB1, WB4, and about ten other
   repository documents was not found in the arXiv rendering, whose theorems
   are numbered sequentially; this is consistent with the September 20
   strategy note, which cites MFCS "Theorems 9–12" and "Theorem 15".  The
   locator should be re-checked against the MFCS PDF.
2. The registry entry has identity verified, but its only `imported_result`
   usage is `metadata_only` (another claim) with the open obligation "inspect
   the full theorem statement".  Neither WB1 nor WB4 has a usage record.
3. CGI report the result as Bogdanov's; the original source is unidentified
   (already a recorded limitation).

**A self-contained proof of the special case** (supplied by the reviewer, so
that WB1 Step 10 and WB4 Step 3 need not rest on the secondary report; it has
not been independently reviewed):

> Let `K = M_0 ∪ M_1 ∪ M_2` be as above with `n >= 6`.  If `M_0 ∪ M_1` has two
> or more (alternating, even) cycles, take `M_0` on one and `M_1` on the
> rest.  Otherwise `M_0 ∪ M_1` is a Hamiltonian cycle `v_0 v_1 ... v_{n-1}`,
> and the `M_2` edges are chords.  A chord `v_a v_b` with `a`, `b` of
> opposite parity splits the cycle into two paths with an even number of
> vertices each; it and the path matchings form a perfect matching that
> contains a chord and (as `n - 2 > 0`) a cycle edge.  So assume every chord
> joins positions of equal parity.  If an even chord `v_p v_q` and an odd
> chord `v_r v_s` cross (cyclic order `p, r, q, s`), then all four arcs have an
> even number of vertices, and the two chords with the arc matchings form a
> perfect matching that contains a chord and, since `n - 4 > 0`, a cycle
> edge.  Finally, if no even chord crosses an odd chord, choose a chord and one
> of its two sides with the fewest interior vertices.  The interior between
> two equal-parity positions contains at least one vertex of the other
> parity; its chord has the other parity, does not cross, and so lies
> strictly inside, with fewer interior vertices: a contradiction.  ∎

Exhaustive check (reviewer's script, scratch only): with `M_0` fixed, the 32
configurations at `n = 6` and 1,884 at `n = 8` all have a fourth perfect
matching; at `n = 4` both configurations (`K_4`) do not, as expected.

**PASS** for the mathematics; the provenance items above are open
book-keeping obligations.

## 4. Item (d): Lemma 2' and the lex-leader clauses

*The lemma.*  Correct, and the proof is longer than needed: once colour 0 is
the non-uniform colour, `M_0` is not a matching, while the chain edges are a
perfect matching inside `M_0`; so `M_0` contains a non-chain edge, and its
endpoint `v` has a non-chain supported partner in some reachable set.  Any
colour-0 chain works.  The displayed statement is garbled ("a supported
Laplace partner `u != v`'s chain partner"); the intended reading is "a
partner different from `v`'s chain partner".  Lemma 2' must be applied after
Lemma 1 when combined with `--normalize`; this is fine because normalization
leaves `R_c`, hence uniformity, unchanged (§1).

*Invariance.*  The hypothesis "some vertex has, in some reachable colour-0
set, a supported partner other than its chain partner" is invariant under
every endpoint swap `(2i-2 2i-1)` (it maps chain partners to chain partners
and reachable sets to reachable sets of the image model) and under the
colour swap `(1 2)` (which fixes colour 0).  Hence the set of normalized
models satisfying it is a union of orbits of the generated group, and correct
lex-leader constraints remain sound on it.  **The claim in the document is
correct.**

*Encoding.*  `_branching` makes colour-0 reachability exact in both
directions (well-founded because sets shrink), and requires the witness set to
have at least four elements.  That restriction is harmless but undocumented:
if the only non-chain step occurs at a reachable pair `{v,u}`, its reachable
4-set parent `B` contains `v` but not `v`'s chain partner, so (L) at `B` at `v`
gives a non-chain partner with `|B| = 4`.  The encoding is faithful.

However, every `--branching` run also contains the lex-leader block, so its
`n = 10` result is affected by §6.

## 5. Item (e): Lemma 4 and the ladder

*Validity of (F').*  A Laplace expansion of a zero hafnian cannot have exactly
one nonzero term.  Correct.

*(a), (S), (F') ⇒ (F).*  Correct.  Two steps are implicit: the base case is
`A = ∅ ∈ S_c` by (a) (the inductive step needs `A ≠ ∅` to pick `v`), and
"by induction `A - {v,N(v)} ∈ S_c`" needs that `A - {v,N(v)}` again has a
unique perfect matching (the Lemma 1 argument).  Both are routine.

*RZP = AP'+(F').*  RZP (Section 1 of RZP10) consists of (a) (empty set,
`V`, and pairs identified with edges), (L), singleton noncancellation (F'),
and the rainbow clauses; it does **not** list (S) or (F).  So the inclusion
RZP ⊆ AP'+(F') needs (S), which follows from (L) and (a) by induction on
`|A|`, and then (F) by Lemma 4.  With that one-line addition the identification
is correct.

*"Strictly between".*  Lemma 4 proves inclusions only.  Strictness is not
shown in either direction: AP'+(F') and AP' both have no models at
`n = 6, 8` (and, modulo §6, at `n = 10`); at `n = 4` the `K_4` model satisfies
(F') automatically and is an actual witness.  "Strictly" should be dropped or
read as "possibly strictly"; the same wording is in the ledger entry.

## 6. The finite `n = 10` certificate: an implementation defect

### 6.1 The defect

`Encoder._symmetry` names the auxiliary prefix-equality variables of each
lex-leader constraint by

```python
eq = self.pool.id(("eq", id(image), key))
```

where `image` is the generator function.  The endpoint swaps are closures
created in a loop; once a closure is released, CPython reuses its address for
a later one.  In practice the `n/2 + 1` generators share **two** namespaces:

```text
n=10: 226 eq variables instead of 330; 2 distinct namespaces for 6 generators
```

(The same count appears at `n = 6` and `n = 8`.)  When two generators share a
namespace, a key moved by both gets one variable that is defined twice, as
"prefix equal for generator 1" and "prefix equal for generator 2".  That
equates two unrelated conditions and can exclude whole orbits.

### 6.2 A concrete excluded orbit

Isolating the script's own symmetry block (chain clauses plus lex-leader
clauses) and fixing `g`: colour 0 is the chain matching plus one edge
`{a,b}` with `a ∈ {0,1}` and `b ∈ {4,5}`, and colours 1 and 2 are empty.  The
four choices of `{a,b}` form one orbit.  A direct Python check of every
generator's lex-leader inequality accepts exactly `{1,5}`.  The script's block
is **unsatisfiable for all four**, at `n = 6` and at `n = 10`.  For `{1,5}`,
generator `(0 1)` meets its first strict inequality at key `(0,{0,5})`, so its
prefix-equality variable there must be false, while generator `(4 5)` still
has an equal prefix at that key, so its variable must be true; the two
generators share a namespace, so it is the same variable.  So the block
can remove every member of an orbit, the property Section 3 of WB4 correctly
says a lex-leader block must not have.

### 6.3 Consequence

The DIMACS files pinned in WB4 Section 6 are regenerated by the current
script with exactly the pinned hashes:

```text
AP'        44,858 vars  179,829 clauses  2 namespaces  b74ec5702e370d3396e544bbf0593586baf9c39b03bd4b1a273e27dd86c748a5
AP' + (F') 44,858 vars  214,119 clauses  2 namespaces  1a96f77c033118ad5ab12c9c270d37d5f5af1565db640b29e3b1ed248c07d65f
```

So the `drat-trim` `s VERIFIED` results certify the unsatisfiability of CNFs
that are **not** implied by AP' under Lemma 2.  In the terms of AGENTS.md
Section 4, link 7 ("the accepted certificate implies the mathematical
obligation") is broken.  The certificate does not establish "AP' has no model
at `n = 10`", nor the AP'+(F') version.  The following WB4 statements depend
on the same block and are equally unsupported as stated: the `n = 10`
normalized, top-matching, and `--branching` UNSAT results; every Section 8.2
timing (a quick refutation may come from the over-constraint); the "0.3 s"
remark in Section 8.3; and any `n = 12` verdict from these runs.  The `n = 6`
and `n = 8` rows of the Section 6 table are also affected, but those orders
are independently settled by WB2.  The minimal-unsatisfiable-subset counts
(22 and 207) were computed "in the chain-normalized instances" and are
presumably affected too.

The mathematics of Lemma 2 and the orbit argument in Section 3 are correct;
only the implementation is wrong.  The pinned-hash, byte-for-byte
reproducibility claim also depends on CPython's allocator reusing addresses
the same way, so the CNF is not portable even as an object.

### 6.4 What still supports `n = 10`

- The independent audit encoding (`audit_..._chain_normalized.py`, read in
  full by the reviewer) has no lex-leader clauses, so it is unaffected.  WB4
  records it as UNSAT at `n = 10` (Glucose 4.1, 3,634 s), with a truncated
  and therefore unusable DRAT trace: an uncertified run.
- The reviewer patched a scratch copy of the script so that the namespace is
  a per-generator counter (one changed key; nothing else).  The patched block
  accepts the true lex-leader `{1,5}` in §6.2 and has 330 equality variables
  in 6 namespaces at `n = 10`.  Patched results (CaDiCaL 1.5.3 through
  `python-sat` 1.9.dev7, Python 3.13, Windows; uncertified):

  | instance | vars | clauses | result | solve |
  |---|---|---|---|---|
  | `n = 6` | 1,072 | 4,145 | UNSAT | 0.0 s |
  | `n = 8` | 7,455 | 28,987 | UNSAT | 0.6 s |
  | `n = 8 --relax two_part_only` / `no_forcing` / `no_laplace` | 7,455 | — | SAT, independent check PASS | ≤ 0.1 s |
  | `n = 8 --fprime` / `--normalize` / `--top-matching` / `--normalize --branching` | — | — | UNSAT | ≤ 0.8 s |
  | `n = 10` AP' | 44,962 | 179,829 | **timeout** (3,000 s cap) | — |
  | `n = 10` AP'+(F') | 44,962 | 214,119 | UNSAT | 1,816 s |

  Both `n = 10` runs used `tools/research/run_bounded.py` (3,000 s, 6 GB) and
  ran concurrently on a host shared with other workers' solver runs, so the
  times are not comparable with WB4's.  The AP' timeout is a timeout, not
  evidence either way.  The patched AP'+(F') UNSAT is about the stronger
  model (fewer models), so it does not imply the AP' statement.  The patched
  instances are harder than the defective ones (1,816 s against WB4's 109 s
  for AP'+(F'), even allowing for load), which is what an over-constrained
  defective CNF would predict.

  The patched `n = 10` DIMACS SHA-256 values (written by the same
  `CNF.to_file` path as `--proof`) are
  `2c6d1990f3d6de2a57becfa8910eb00e94133e2a1fc19728a05d4fa92d7c4217` (AP')
  and `a95034fdb6820dc24322cf406426ca7bc782561589aded356714e0fb8073d7c9`
  (AP'+(F')).

So AP' at `n = 10` is plausibly UNSAT, but at present its only sound
support is the uncertified audit-encoding run recorded in WB4, not a checked
certificate of a sound encoding.  AP'+(F') at `n = 10` is unaffected as a
mathematical fact, because RZP10 already excludes it with checked
certificates (and RZP = AP'+(F'), §5); only WB4's claim of an *independent*
certificate for it falls.

### 6.5 Repair (not performed here)

1. Key the equality variables by a generator index (or create them with
   `pool._next()`); add a regression test that the number of equality
   variables equals the number of moved keys summed over generators, and the
   §6.2 orbit test.
2. Regenerate both `n = 10` DIMACS files, re-solve natively with a DRAT
   trace, replay with the pinned `drat-trim`, and pin the new hashes.
3. Until then, WB4 Section 6/7, the ledger entry (`status: verified`, the
   "DRAT-checked n=10 exclusion" in its name and assumptions), WB2's boundary
   note, and the `WB2`, `RZP10`, and `WB4` nodes of
   `docs/current-frontier.md` overstate the `n = 10` evidence.  Correcting them
   is an integration-owner decision; this review edits none of them.

## 7. Item (f): reproduction

Run by the reviewer in its worktree (merged script on `main`; identical
encoding for these cases to the branch version):

```text
python claims/arbitrary-order/explore_all_diagonal_support_level_ap_prime_bounded_search.py 8
  -> 7,391 vars, 28,987 clauses, UNSAT, 0.2 s
python claims/arbitrary-order/explore_all_diagonal_support_level_ap_prime_bounded_search.py 8 --relax two_part_only
  -> 7,391 vars, 27,727 clauses, SAT, independent_check PASS
```

The branch version also reproduced `--relax no_forcing` and `no_laplace`
(SAT, PASS) and `--fprime`, `--normalize`, `--top-matching`,
`--normalize --branching` (UNSAT) at `n = 8`.  These match the document, but
the UNSAT rows inherit §6; the SAT rows are unaffected in the direction that
matters (a SAT model is rechecked by brute force).

## 8. Other remarks

- Section 7's proof-distance delta ("computation for `n <= 10`") should read
  that `n = 10` is supported by uncertified runs until §6.5 is done.
- The ledger entry's assumption string repeats "lies strictly between" (§5)
  and "Theorem 1.7" (§3).
- Section 8.3 is correctly labelled a partial argument.  Its counting step
  ("`|W| ∈ {0,2}`") was not audited in depth by this review.
- No project-specific axiom, admitted step, or Lean claim is involved.

## 9. Reproduction of the reviewer's checks

The reviewer's scratch scripts were not committed.  The namespace count of
§6.1 is reproduced by:

```python
import importlib.util, sys
spec = importlib.util.spec_from_file_location("s", "claims/arbitrary-order/explore_all_diagonal_support_level_ap_prime_bounded_search.py")
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
enc = s.Encoder(10)
keys = [k for k in enc.pool.obj2id if isinstance(k, tuple) and k and k[0] == "eq"]
print(len(keys), len({k[1] for k in keys}))   # 226 2 ; a sound block has 330 6
```

The §6.2 test instantiates `Encoder._symmetry` on a stub with only the `g`
and `m` variables and solves it under the four fixed `g` assignments; the
§6.4 patch replaces `id(image)` by a counter incremented at each
`lex_leader` call.
