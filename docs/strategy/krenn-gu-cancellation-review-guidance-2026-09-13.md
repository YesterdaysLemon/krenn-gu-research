# Krenn–Gu cancellation-consistency: review and next-run guidance

**Reviewed snapshot:** `cb556ab3223134085ca7823497e648a98b77c1e6`
**Review date:** September 13, 2026
**Global mathematical status:** unresolved. This document is guidance, not a theorem or authorization to publish or begin an unattended run.

## Assessment

The work follows the intended cancellation-consistency direction. It implements truthful recursive edge/cofactor support variables; preserves the distinction between RZP and AP′; uses integer monomial relations rather than invalid general parity reductions; retains complete-fibre escape conditions; and tests compatibility between equations from one physical source. Moving beyond odd binomial circuits to larger sums was appropriate, not drift.

The main finite deliverable is the reported, locally replayed thirteen-case n=10 all-diagonal RZP exclusion. The main conceptual advance is the small two-sum contradiction. The main remaining computational obstacle is projection: a contradiction for one cofactor assignment is not automatically a contradiction for its physical support. The main global obstacle remains a proved occurrence theorem or a source-preserving reduction.

The review inspected the mathematical notes, recursive encoder, quotient and row-space replay code, physical-core checker, relevant tests, and the evidence manifest. It did not execute the repository test suite or replay the roughly 500 MB DRAT payload. Independent small checks reconstructed all 945 ten-vertex perfect matchings, constructive matching-stabilizer transporters, the stated recursive instance counts, and all 4,096 ordered four-vertex graph pairs underlying the coverage lemma. These are limited checks, not certification of the full finite exclusion.

## Source records

All paths below refer to the reviewed commit.

- `docs/strategy/cancellation-consistency-handoff-2026-09-13.md`
- `docs/strategy/recursive-cancellation-consistency-experiment-2026-09-12.md`
- `docs/strategy/recursive-cancellation-consistency-evidence-2026-09-12.json`
- `docs/strategy/cancellation-consistency-continuation-2026-09-13.md`
- `docs/strategy/full-model-recursive-cancellation-attempt-2026-09-13.md`
- `docs/strategy/source-cancellation-mechanisms-2026-09-13.md`
- `docs/strategy/four-vertex-cofactor-coverage-2026-09-13.md`
- `src/krenn_gu/recursive_hafnian_support.py`
- `src/krenn_gu/recursive_tensor_quotient.py`
- `src/krenn_gu/recursive_tensor_row_space.py`
- `src/krenn_gu/source_quotient_core.py`
- `src/krenn_gu/laplace_incidence_support.py`
- `tests/test_recursive_tensor_row_space.py`

## 1. Finish the finite result without changing its meaning

The claim to package is that the strengthened RZP model has no model at n=10, and therefore there is no complex all-diagonal witness at n=10. This is neither the unrestricted n=10 conjecture nor an exclusion of the weaker AP′ model.

The certificate cover consists of six nonshared matching-pair types and seven third-matching subcases of the shared-pair case. The third-matching normalization is justified precisely because the first two selected matchings coincide; do not generalize that normalization to the other cases without proving the relevant stabilizer action.

Prepare a theorem-sized statement and proof bridge, a complete manifest, a portable proof bundle outside ordinary Git history, and a replay path that does not require the author's original machine layout. Obtain independent review of the witness-to-CNF bridge, the cover, and the certificate interpretation. Preserve exact source and proof hashes. Do not start another large replay merely because one exists; replay after relevant changes or as part of the agreed independent audit.

The older WB2 AP′ DRAT gap remains a separate evidence issue. Keep that distinction explicit. Finishing the stronger finite result need not be delayed by rerunning a weaker formulation unless the weaker theorem itself is being promoted as certificate-backed.

**Completion criterion:** an auditable, portable n=10 all-diagonal result with its exact scope and evidence limitations. Distribution, publication, or repository promotion requires the user's authorization and the repository's review gates.

## 2. Connect the new algebra to the existing physical projection checker

At the reviewed snapshot, `source_quotient_core.py` explicitly accepts `recursive_quotient_singleton` algebraic certificates. The separate row-space replay uses `recursive-laurent-row-space-v1`. Thus the newest algebraic mechanism is not yet accepted by the existing physical-support projection format.

Add a small typed dispatch boundary for the existing quotient-singleton, exact binomial-kernel, and new row-space certificates, not a replacement proof framework. Each allowed certificate kind needs its own validated origin/dependency reconstruction and must return its replayed guarded clause. A supplied cut or a generic success flag is not a replacement for certificate-specific replay. The core checker must then verify that every remaining premise is either a regenerated base clause or an explicit physical-support assumption, and check the propositional proof. An arbitrary caller-supplied “verified” flag or cut is not acceptable.

Retain tests for incomplete fibres, wrong signs, incorrect integer transports, zero divisors, unguarded variables, changed source targets, invalid DAG dependencies, and extra unproved core premises. A core may eventually require multiple algebraic clauses; each must be independently replayed and included explicitly, not inherited from a hidden learning history.

Move the reusable row-space discovery/packing entry points out of ignored `tmp/` once they are part of the ongoing workflow. Keep discovery separate from the small exact replay.

**Completion criterion:** an independently scrutinized row-space clause can be consumed by a small physical-source core, with every guard and premise accounted for.

## 3. Work at the physical-support level, not merely the assignment level

Use the latest 136-entry eight-vertex physical support as a fixed diagnostic source. Leave its proper coefficient supports free. The handoff says its displayed cofactor assignment already fails a cheaper unit-quotient test, so do not require the newest row-space machinery merely for novelty.

For each fixed support:

1. Run the cheapest sound source propagation and algebraic tests first.
2. Add only replayed guarded clauses, retaining all escape terms.
3. Test whether the fixed-support necessary model is UNSAT after refinement.
4. If UNSAT, obtain a replayable proof core and a physical-entry cut.
5. If the fixed support remains open, report that explicitly, including which cofactor assignments were excluded and which stronger tests were attempted.

Cache learned results by physical support and avoid presenting repeated cofactor assignments on one support as independent physical progress. Track distinct physical supports, support-level exclusions, guard sizes, and coverage of a declared parent. Test cumulative physical cuts under proved vertex/global-colour symmetries. Arbitrary independent local colour permutations do not preserve the GHZ target.

The existing full-orbit SAT countermodel shows that the three current physical cuts are insufficient for the eight-vertex parent. It does not refute the broader cancellation method.

**Completion criterion:** a support-level exclusion with a checked physical core, a complete declared-parent exclusion, or an explicitly characterized obstruction to the chosen projection method. A long list of assignment cuts alone does not satisfy this goal.

## 4. Make larger-sum compatibility a bounded algebraic method

The two-sum control reduces to

    -A - B + C = 0
    -A + B - C = 0

with A, B, C nonzero. Their sum gives -2A=0. Each equation separately admits nonzero solutions; their shared monomial values make the pair inconsistent. This is the relevant phenomenon.

After sound integer binomial transport, assemble selected complete source equations as rows of an exact rational matrix R, with columns for shared Laurent monomials known to be nonzero. A coordinate vector in the row space of R proves that a nonzero monomial must vanish. Equivalently, deleting that monomial's column lowers the rank. Use exact arithmetic and replay the row combination.

For this fixed linear system, the absence of such a coordinate vector is the exact stopping criterion for singleton row-space obstructions: over an infinite field, a linear subspace not contained in any coordinate hyperplane contains a vector with all coordinates nonzero. But monomial values are not independent variables. They still satisfy multiplicative identities, so passing this test is not a physical realization.

Only if a relevant survivor passes the cheaper stages should bounded monomial multiples of the source equations be introduced. Track all multipliers and produce an explicit identity. A particularly clean physical-support certificate has the form

    M(W) = sum_i q_i(W) F_i(W),

where the F_i are exact original target equations after the assumed zero entries are substituted, and M is a nonzero scalar times a monomial in entries explicitly required to be nonzero. This contradicts F_i(W)=0 without guessing any proper cofactor support. This is a target for certificate design, not a promise of low degree or practical completeness.

Do not divide by a proper hafnian merely because it was nonzero in one Boolean assignment. Such division requires a guard, followed by a valid projection or an exhaustive cover of its alternatives.

## 5. Keep one all-order mathematical question active

The four-vertex coverage proof is a good example of turning a diagnostic into a uniform argument. It does not need more tests at higher orders in its already-covered dense family.

A more focused remaining object is the family, for each colour c,

    U_c = {U subset V : |U|=4 and h_c(V minus U) != 0}.

In a hypothetical all-diagonal witness, each U_c is nonempty by two Laplace expansions. For each U in U_c, the two other colour supports cannot contain a mixed perfect matching on U, and cannot both have perfect matchings on U. These are necessary restrictions on the locations of genuinely live cofactors, not permission to select arbitrary uncovered four-sets.

Investigate compatibility of these three families with recursive accessibility and signed-ratio transport. A useful next theorem would show that those jointly supplied constraints force an incompatible cancellation system, or exhibit a genuine globally constrained Boolean countermodel to that proposed implication. A patch omitting the full target is only a local mechanism control.

Keep this all-diagonal programme separate from unrestricted n=8. Either continue the full-model encoder with a declared full-parent goal, or use the exhaustive residual root split r=2 or r=3. Do not quietly restrict to invertible root edges, and do not replace the common physical outside graph by independently realizable local tensors.

## Stop rules and reporting

Do not reopen H4/Q6 merely because it is unfinished. Do not extend an unchanged n=12 timeout without a new reason to expect different information. Freeze the useful n=6 control as a regression example rather than launching a second six-vertex proof project. Do not use external-review timeouts as approvals, or stretch an older review to cover newer code.

At the next checkpoint, distinguish explicitly:

- fixed-assignment contradictions;
- fixed-physical-support exclusions;
- exhaustive parent coverage;
- all-order mathematical implications;
- certificate availability and independent review.

The intended outcome is fewer, stronger, physically interpretable obstructions—not another indefinitely growing catalogue of local successes.
