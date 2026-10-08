# Review: complete eight-vertex protected-scaffold source exclusion (N8PS)

Date: 2026-10-08

Review status: **PASS (no mathematical gap found; accepted at the stated
finite scope)**.  This is a same-day agent review by an adversarial reviewer
working in the same repository on the same day; it is not separate-human
refereeing and not a Lean formalization.  The global Krenn--Gu status remains
**UNRESOLVED**.

Reviewed document:
[`EIGHT_VERTEX_PROTECTED_SCAFFOLD_EXCLUSION.md`](../../claims/finite/n08/EIGHT_VERTEX_PROTECTED_SCAFFOLD_EXCLUSION.md)
(ledger `document_sha256_16` `bcb2c12151fd2000`, matches the LF-normalized
file).  Ledger status `verified_finite`; verifier provenance
`script_is_the_verifier`; audit provenance `independent_exact_identity_audit`.

## Exact claim as restated

Over `C`, with `L={0,1,2,3}`, `R={4,5,6,7}` and in each block
`M0={01,23}`, `M1={02,13}`, `M2={03,12}`: every internal edge of `M_c` carries
the matrix unit `E_cc`; every crossing pair carries an arbitrary hollow
(zero-diagonal) `3x3` matrix, so 16 pairs x 6 off-diagonal entries = 96 free
parameters, zeros allowed, no genericity.  No source in this 96-parameter
family has the normalized ternary GHZ matching tensor.  The three pure
amplitudes are identically one.  Not claimed: arbitrary `n=8` sources, a
reduction of witnesses to this scaffold, other or larger scaffolds, crossing
entries with equal colours (they are zero by hollowness), or any order other
than eight.  The family is the `k=2` instance of the scaffold family of the
[structural-gate no-go](../../claims/arbitrary-order/PURE_MATCHING_SCAFFOLD_STRUCTURAL_GATE_NO_GO_THEOREM.md),
which is stated there for `k>=5` blocks; the document defines the `k=2` family
itself, so no scope is borrowed.  "Complete" refers to the whole declared
96-parameter family, which the document says explicitly.

## Bridge from computation to the mathematical claim

Mathematical content is three steps: (1) the source equations; (2) a necessary
Boolean CNF for a witness; (3) refutation of the CNF.  I checked each.

1. Equations.  For a word `w`, a perfect matching contributes iff each internal
   edge is monochromatic in the colour of its `M_c`, and each crossing edge has
   distinct endpoint colours.  I rebuilt this word-first in a third, separate
   script (not committed): all 6,561 rows, all coefficients `+1`,
   33,696 nonconstant term incidences = 33,696 distinct monomials (each
   monomial lies in exactly one row; degrees 2 and 4 only, as 4 minus the
   crossing count must be even), nine rows with a constant monomial, of which
   the three pure ones vanish after subtracting the target, and no
   single-factor monomials.  This reproduces the document's 33,702 terms
   (33,696 + 6 constants).
2. CNF bridge.  With `b_x := (x != 0)` and `z_m := (all factors of m nonzero)`,
   `z_m <=> AND b_x` is exact in an integral domain.  A zero-constant row whose
   monomial values sum to zero cannot have exactly one nonzero monomial; a row
   with constant `1` needs a nonzero monomial.  These are necessary only, and
   every witness (including every zero pattern of the crossing entries)
   produces a model, so no case cover is needed.  Variable count `96+33,696
   =33,792` and clause count `196,806` (`sum (deg+1)` for the `z` definitions
   plus one clause per row-with-constant or per support monomial otherwise)
   were reproduced by my independent count.  The bridge uses only the
   absence of zero divisors and coefficients `+1`, so it in fact also holds
   over any field; stating `C` is conservative, not a gap.
3. Refutation.  The fixture gives 1,521 original clause indices and 108
   ordered RUP additions ending in the empty clause.  The primary regenerates
   the full CNF, requires the pinned equation hash
   `f10ab786...80ee` and CNF hash `024f9b3a...84b6a`, checks index validity and
   uniqueness, and checks each addition by plain unit propagation from the
   preceding clauses (I read `rup_conflict`; it is sound).  The independent
   audit reconstructs everything word-first with its own bitmask recursion and
   its own propagation engine and compares the same two digests.  Unit
   propagation replay of a RUP chain proves each lemma and hence
   unsatisfiability of the core and of the full CNF.  Hashes are pinned in
   both the primary and the fixture; the omission of deletions is sound.

Case-cover exhaustion is not at issue because the family is a parameter
family, not a case split; the 96 parameters are all free.

## Independence

The audit imports nothing from `src/krenn_gu` and differs in enumeration
(word-first bitmask versus matching-first permutation quotient) and in the
RUP engine.  Both implement the same CNF specification and agree on the same
canonical hash, so independence is of implementation, not of the bridge
semantics.  The bridge itself is "in-document proof only"; I re-derived it
above and via the third script, which supports it.  This is a same-session
reconstruction, as the ledger `note` and the document state.

## Commands run (under `run_bounded.py`, 900 s / 8 GiB; nothing skipped)

```text
python claims/finite/n08/verify_eight_vertex_scaffold_full_source_exclusion.py       # EXACT_FULL_SCAFFOLD_RUP_PASS, 2 s
python claims/finite/n08/audit_eight_vertex_scaffold_full_source_exclusion.py        # PASS_PORTABLE_RUP_REPLAY, 4 s
python claims/finite/n08/verify_eight_vertex_scaffold_subsystem_controls.py          # EXACT_LAURENT_SUBSYSTEM_CONTROLS_PASS, 1 s
python claims/finite/n08/audit_eight_vertex_scaffold_shore_countermodel.py --output <scratch>   # PASS, 3 s
python -m unittest -v tests.test_scaffold_full_source                                # 5 tests OK, 7 s
```

Outputs match the document: 6,561 words, 33,792 variables, 196,806 clauses,
1,521 core clauses, 108 additions, empty clause derived, both hashes equal.
Controls: 477, 1,065 and 1,869 subsystem words with 27, 29 and 27 nonzero
full-word Laurent errors, displayed errors `P_00012121=-r02/r12`,
`P_00020011=-r01/r21`, `P_00010221=-r01/r10`.  I checked by inclusion-exclusion
that 477 (shore-constant words) and 1,065 (their union with the 765 words of
at most two colours) are the right counts.  The controls are countermodels to
proper subsystems only and do not enter the exclusion.

## Frontier and ledger consistency

The `N8PS` row of `docs/current-frontier.md` matches: proved finite exclusion
over `C`, 1,521-clause core and 108 RUP steps, independent reconstruction and
propagation, three Laurent controls, neither unrestricted `n=8` nor
larger-order.  It does not overstate.  Ledger `verified_finite` is apt: an
exact finite computation with a stated bridge.  The ledger `note` ("not merely
a sampled support or weight grid") is accurate because the 96 parameters are
free.  The document's inventory of the older 129-entry survivor is consistent
with the frontier's `ST20` row.

## Remarks and minor gaps (none blocks acceptance)

1. The external DRAT check (`drat-trim` v05.22.2023, binary and DRAT hashes
   quoted) and the failed native CaDiCaL child are recorded as discovery
   provenance only.  The full DRAT file and the binary are not in the
   repository, so I could not re-run that corroboration; the document correctly
   makes the portable RUP replays, not drat-trim, the acceptance gate.
2. Formatting defects in recorded text: the fixture `scope` string and the
   ledger `assumptions_and_excluded_divisors` entries have dropped spaces
   (`all96hollow`, `with33792variables and196806clauses`, `Tracked1521original
   clauses and108RUPadditions deriveempty`).  Content is correct; the ledger
   text should be tidied by its owner.
3. The `k=2` family is an extension of the `k>=5` definition in the parent
   no-go; this is stated, and nothing relies on inheriting a `k>=5` result.
4. The larger-order paragraph (twelve-vertex control, resource sums) points to
   another theorem document and was not re-reviewed here.
5. Native Glucose4 proof truncation is documented as a rejected calibration;
   it has no bearing on acceptance.

## Verdict

The finite exclusion is sound at its stated scope: the family is exhaustively
parameterized, the witness-to-CNF bridge is valid, the CNF is unsatisfiable by
a hash-pinned, twice-replayed RUP chain, and the document keeps countermodels,
discovery failures and larger-order limits separate.  Frontier row and ledger
status agree with the document and do not overstate.  Same-day agent review
only; global status unchanged.
