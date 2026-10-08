# Adversarial review: two-slice shared-hafnian transfer obstruction (ST20)

Date: 2026-10-08

Reviewed package:

- `claims/arbitrary-order/TWO_SLICE_SHARED_HAFNIAN_TRANSFER_OBSTRUCTION.md`
  (ledger hash `b54c21f3cfc47559`, unchanged by this review)
- `claims/finite/n08/verify_eight_vertex_two_slice_transfer.py` with
  `src/krenn_gu/two_slice_transfer.py` (primary, companion point check)
- `claims/finite/n08/audit_eight_vertex_two_slice_transfer.py` with its helper
  `claims/finite/n08/audit_eight_vertex_degree6_source_134.py` (independent audit)
- `tests/fixtures/eight_vertex_two_slice_transfer.json`,
  `tests/test_two_slice_transfer.py`
- the `ST20` node, its two edges and its frontier table row in
  `docs/current-frontier.md`, and the ledger entry in
  `catalog/theorem-ledger.json`

## Independence disclosure

This is a **same-day agent review**: one automated reviewer, working on
2026-10-08 in a separate worktree from the authoring session, with no access to
that session beyond the committed tree.  It is not separate-human refereeing,
not an external audit by an unrelated author, and not a Lean formalization.
The reviewer re-derived the proof by hand and wrote an uncommitted third-route
polynomial check (own matching enumeration and polynomial arithmetic, no
repository imports); that script is reviewer scratch evidence, not a new
verifier.

## Verdict

**PASS as a proved conditional source obstruction at exactly its stated
scope.**  No mathematical gap was found.  The ledger status `verified` and the
frontier wording do not overstate the document.  The items in section (e) are
disclosure and coverage notes, none of which affects the theorem.  The theorem
does not supply its own premises; occurrence, unrestricted n=8 exclusion and
all-order coverage remain open, and global Krenn–Gu remains **UNRESOLVED**.

## (a) Exact statement

Let `K` be any field and `n >= 4` even (odd `n` is vacuous).  Work with the
physical source `W_ij[a,b]` (colour `a` at `i`, `b` at `j`, with
`W_ji[b,a] = W_ij[a,b]`) and its generated tensor
`T_W(w) = haf(W_ij[w_i,w_j])`.  Fix distinct vertices `x,p,q,y`, put
`F = V \ {x,p,q,y}`, a colour `c`, and colours `alpha, beta, s` each different
from `c` (not necessarily mutually distinct).  Assume the `4(n-4)+2` zeros

```text
for all i in F:  W_ip[c,c] = W_iq[c,s] = W_iy[c,beta] = W_iy[c,c] = 0,
                 W_pq[c,s] = W_pq[c,c] = 0,
```

and the two nonzeros `B_alpha = W_xq[alpha,s] != 0`,
`C_beta = W_py[c,beta] != 0`.  Then `T_W` is not equal to any tensor that
vanishes on every non-monochromatic word and has `T(c^n) = lambda_c != 0`.
No other entry, cofactor, hafnian or determinant is assumed nonzero.

The proof actually uses only the eight words with `F` and `p` in colour `c`,
`x in {alpha,c}`, `q in {s,c}`, `y in {beta,c}`, and only the target values on
them: zero except `lambda_c` at `c^n`.  The conclusion is therefore also valid
for a projective realization `T_W = mu * target`, `mu != 0`, and for any
target that is diagonal on these eight words.  This is a reading of the
statement, not a strengthening of the ledger claim.

## (b) Proof-step check

1. **q=s slice.**  `p` (colour `c`) cannot meet `F` (`W_ip[c,c]=0`) or `q`
   (`W_pq[c,s]=0`); `q` (colour `s`) cannot meet `F` (`W_iq[c,s]=0`).  So `p`
   and `q` occupy `{x,y}`; `F` is matched internally.  Hence
   `T_s(a,d) = H*(A_a*E_d + B_a*C_d)` with `H = haf(W[F]; all c)`.  Correct;
   the `W_iy` zeros are not needed in this slice.
2. **q=c slice.**  `p` can meet only `x` or `y` (`W_ip[c,c]=W_pq[c,c]=0`).  If
   `p-x`, then `y` (colour `beta` or `c`) cannot meet `F` (`W_iy[c,beta]`,
   `W_iy[c,c]`), so `y-q` and `F` is internal: `H*A_a*D_d`.  If `p-y`, the rest
   is exactly `R_a = haf(F ∪ {x,q})`.  Hence `T_c = H*A_a*D_d + R_a*C_d`.
   Correct.  The document does not say which zero is used where; the
   assignment above is the reviewer's and every class is needed (see (c)).
3. **Covectors.**  `u_Z = Z_alpha e_c^* - Z_c e_alpha^*` on the 2-dimensional
   `x`-colour space (`alpha != c` is used); `u_Z(Z)=0` and
   `u_Q(Z) = -u_Z(Q)` hold in every commutative ring.  Same for `v_Z`.
4. **Transfer.**  `(u_A⊗v_D)(T_s) = H u_A(B) v_D(C)` because the `A⊗E` term is
   killed by `u_A(A)=0`; `(u_B⊗v_C)(T_c) = H u_B(A) v_C(D)` because the `R⊗C`
   term is killed by `v_C(C)=0`.  The two products agree since both signs
   flip.  Identity (2) is therefore a polynomial identity in the entries,
   valid for every specialization, including `H = 0`.  **No division by any
   cofactor occurs**; `H` and `R_a` are never inverted or assumed nonzero.
5. **Target.**  On the q=s slice every word has `p=c`, `q=s != c`, so the
   target vanishes.  On the q=c slice the only monochromatic word is
   `x=y=c` (because `alpha, beta != c`), including `n=4` with `F` empty.
   Evaluating (2) on the target gives
   `-lambda_c u_B(e_c) v_C(e_c) = -lambda_c B_alpha C_beta`, which is nonzero
   in a field.  Correct.
6. **Genericity.**  None is used.  The statement is pointwise for every source
   satisfying the listed equalities and inequations.
7. **Imported results.**  None.  The ledger lists no dependencies and the
   proof uses only the hafnian expansion; the boundary relation `rho` is not
   used (the n=8 identities close exactly with no `rho` term; the scripts'
   `uses_rho`/`rho_reduction_used` fields are labels, not the check).
   Links to P17, the degree-five limitation and the resolution attempt are
   context, not premises.
8. **Count.**  The `4(n-4)+2` zeros are pairwise distinct (`beta != c`
   separates the two `W_iy` classes).
9. **Closing remark.**  "Replacing that common source coefficient by two
   unrelated values loses the implication" is explanatory and unproved in the
   text, but immediate: with slice cofactors `H_1 != H_2` the left side of (2)
   acquires `(H_1 - H_2) u_A(B) v_D(C)`.  Not load-bearing.

## (c) Computational evidence

| Check | Result |
|---|---|
| `python claims/finite/n08/verify_eight_vertex_two_slice_transfer.py` | PASS, 4 patterns, term counts `6,6,6,6,18,18,18,18`, 0.2 s |
| `python claims/finite/n08/audit_eight_vertex_two_slice_transfer.py` | PASS, 4 patterns, 105 matchings, guard size 18, 0.6 s |
| `python -m unittest -v tests.test_two_slice_transfer` | 5 tests OK |
| displayed zeros/IDs in the document vs fixture | identical (zeros `99,...,234`; nonzeros `47=W06[0,1]`, `241=W57[2,0]`; multipliers `39,45,47,53,241,243,250,252` and signs of (3)) |

What they check: the primary builds the eight-row identity from the template
and `replay` expands each of the eight full eight-vertex hafnians with the
eighteen zeros imposed, subtracts `1` on pure words, and requires the
residual `sum coeff*mult*P_w - B_x C_z` to vanish exactly.  The audit uses a
separately written bitmask matching enumerator, closed-form entry numbering
and `Counter` polynomials; it confirms the exact identity, the 48-pair
cancellation of all 96 degree-six contributions, and the mutation controls
(each single deleted zero breaks the identity; a flipped sign or omitted row
breaks it; dropping the pure target leaves exactly `-B_x C_z`; forcing either
nonzero premise to zero makes the identity trivial).  This matches the text.
Both scripts are finite n=8, three-colour point checks of the displayed
identity; **neither is the all-order proof**, which the ledger's
`companion_point_check_script` provenance states correctly.

Reviewer third-route check (uncommitted, run under `run_bounded.py`): own
matching recursion and sparse integer polynomials, random vertex placement,
**four colours** and symbolic `lambda_c`.  It verified both lines of (1),
identity (2) and the target value `-lambda_c B_alpha C_beta` for every
`(c,alpha,beta,s)` at n=4, 6, 8 (108 colour cases each, covering all five
equality types including the all-distinct one) and one representative of each
of the five types at n=10; deleting any one of the six zero classes at n=8
leaves a nonzero residual (12 to 144 terms).

Parent-relation claims in the document, outside the named verifier/audit:

| Command (bounded) | Result |
|---|---|
| `probe_two_edge_shore_parent.py --include-two-slice --replay-assignment tests/fixtures/eight_vertex_two_slice_parent_survivor.json` | `PASS_FROZEN_BOOLEAN_ASSIGNMENT`, 600,063 variables, 4,748,964 clauses, CNF SHA-256 `ccfb1128…d296`, 66 s |
| `audit_eight_vertex_degree6_pure_coupling.py` | PASS, 20,280 grades, 142,328 rows, high rank 142,328, kernel 0, 0 augmented coloops |
| reviewer orbit scan of both survivor supports against all 4 x 10,080 ST20 images | 134-entry survivor satisfies exactly one image of type `(z,t)=(0,1)` and one of `(1,0)`; the 129-entry survivor satisfies none |

So the claims "excludes the P17-orbit survivor" and "129-entry support avoids
all twelve tested orbits" are confirmed.

## (d) Ledger and frontier

- Ledger `status: verified`: per `docs/evidence-semantics-contract.md`,
  `verified` means the stated proof/evidence passed the recorded procedure and
  cannot enlarge scope.  The written proof is correct and the point checks
  pass; the assumptions list states the all-order/finite split honestly.
  Not overstated.
- Frontier node `ST20` ("PROVED all-order conditional identity; n=8 20-literal
  exclusions"), edge `G0 -> ST20` ("exact shared source slices"), boundary edge
  `ST20 -> GL` ("guard occurrence and parent coverage open") and both table
  rows state the conditional nature and the open occurrence/coverage
  obligations.  The `P17` row's "survivor is excluded by ST20" was confirmed
  above.  Not overstated.

## (e) Gaps and notes

No mathematical gap.  Exact notes:

1. **Implicit zero bookkeeping.**  The proof text does not say which zero
   class is used in which slice (see (b)1–2).  Correct as written; a reader
   must reconstruct it.
2. **Colour coverage of the finite evidence.**  "All four ternary
   colour-equality types" is exact for three colours (entry IDs 1..252).  With
   four or more colours the all-distinct type `alpha, beta, s` pairwise
   distinct exists; it is covered by the written proof only (and by this
   review's uncommitted scratch check), not by a committed script.
3. **Audit independence scope.**  The audit independently implements the
   matching and polynomial arithmetic, but its eight source rows and signs are
   transcribed from the same mathematical template rather than independently
   derived, and both scripts share the 1..252 entry-numbering convention.  Its
   fixture cross-check covers only the `(z,t)=(0,1)` fixture.  This is an
   independent replay of a given identity, which is what the ledger's
   `independent_exact_identity_audit` label says.
4. **Verifier coverage of the parent paragraph.**  The quantitative claims in
   "Relation to the parent" (SAT survivor, 129-entry support, rank 142,328)
   are not checked by the ledger's named verifier or audit; they rely on the
   separate bounded commands in
   `docs/strategy/source-module-resolution-attempt-2026-09-14.md`, which this
   review re-ran successfully.
5. **Review provenance.**  That strategy document says the human proof was
   "independently reviewed"; before this file the ledger recorded
   `review: null`, with only same-session reconstruction noted.  This file is
   the first committed review record, and it is itself only a same-day agent
   review.

## Reproduction

```text
python claims/finite/n08/verify_eight_vertex_two_slice_transfer.py
python claims/finite/n08/audit_eight_vertex_two_slice_transfer.py
python -m unittest -v tests.test_two_slice_transfer
python tools/research/run_bounded.py --run-id <fresh-id> --timeout-seconds 900 --memory-mb 8192 -- python tools/explore/probe_two_edge_shore_parent.py --include-two-slice --replay-assignment tests/fixtures/eight_vertex_two_slice_parent_survivor.json --output-dir tmp/<fresh-dir>
python tools/research/run_bounded.py --run-id <fresh-id> --timeout-seconds 1500 --memory-mb 8192 -- python claims/finite/n08/audit_eight_vertex_degree6_pure_coupling.py
```

Global Krenn–Gu status: **UNRESOLVED**.
