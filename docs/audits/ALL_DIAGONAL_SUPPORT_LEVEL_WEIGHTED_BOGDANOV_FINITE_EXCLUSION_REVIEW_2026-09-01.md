# Adversarial review: all-diagonal support-level finite exclusion at n = 6, 8

Date: 2026-09-01

Reviewed package:

- `claims/arbitrary-order/ALL_DIAGONAL_SUPPORT_LEVEL_WEIGHTED_BOGDANOV_FINITE_EXCLUSION_THEOREM.md`
- `claims/arbitrary-order/verify_all_diagonal_support_level_weighted_bogdanov_finite_exclusion.py`
- `claims/arbitrary-order/audit_all_diagonal_support_level_weighted_bogdanov_finite_exclusion.py`

## Independence disclosure

Same-session self-review by the authoring agent (Claude).  Not an
independent audit in the sense of `AGENTS.md` section 5.  The two scripts are
independent of each other in encoding and solver, but both were written by
the same agent.

## Verdict

**PASS as a finite computer-assisted exclusion with a stated evidence gap.**
No all-diagonal witness exists on six or eight vertices; at both orders the
exclusion is support-level.  The general statement for every even `n` is
recorded as a conjecture, not a theorem.

## 1. Attacks on the bridge lemma

Each clause family must be a *necessary* condition of an exact witness;
otherwise UNSAT would prove nothing.

- (a): trivial.
- (L): Laplace expansion of a hafnian along a vertex; a nonzero sum has a
  nonzero term, and that term's edge weight and sub-hafnian are both
  nonzero.  Correct.
- (S): implied by (L) inductively; kept in the primary, dropped in the
  audit.  Harmless either way.
- (F): a hafnian is a sum over perfect matchings of the support graph; with
  exactly one such matching it is one nonzero monomial.  Correct.  The
  encoding says "`p_M` true and every other `p_M'` false implies `m_A`",
  which is exactly (F).
- (H2): exact for diagonal blocks by factorization; the constant words give
  (H1).  The word enumeration includes every ordered even partition with at
  least two nonempty classes, and empty classes contribute no literal.

No clause encodes a sufficient-only or value-level condition, so UNSAT is
sound.

## 2. Attacks on the computation

- Solvers: CaDiCaL 1.5.3 (primary) and Glucose 4.1 (audit), both through the
  pinned `python-sat`.  Two encodings differ in auxiliary structure and
  rainbow generation.  Agreement on UNSAT at `n = 6` and `n = 8`.
- No DRAT trace.  `drat-trim` is not on the reference host, and the
  `python-sat` CaDiCaL binding does not expose proof output.  This is the
  package's evidence gap and is stated in the theorem and the ledger.
- The relaxation runs are SAT and their decoded supports are printed, so a
  reader can see that each dropped ingredient is load-bearing at `n = 8`.
  The two-part-only model is the classical three-disjoint-matching
  configuration, which is reassuring: the encoding recovers Bogdanov's
  setting exactly when the three-part clauses are removed.
- Runtime is dominated by the unrestricted `n = 8` instances (about four and
  two minutes).  The DIMACS files are deleted after hashing so that no
  generated artifact is tracked.

## 3. Attacks on the interpretation

- "Support-level" is not "trivial": the `n = 8` instance takes minutes and
  each relaxation is satisfiable.  The theorem does not claim a short human
  proof exists at `n = 8`; it claims no weights are needed.
- The conjecture for all `n` is clearly labelled.  `WB1` excludes actual
  weighted witnesses at `Delta(D) <= 4`; it does not prove the weaker AP'
  abstraction unsatisfiable there because its numerical score and
  noncancellation steps are absent after the one-way bridge.  `WB3` now
  records the valid support-only degree-four reduction and the remaining
  open implication.
- The `n = 8` result is new relative to the eight-vertex finite frontier,
  which covered sparse skeletons and singleton families.  The `n = 6` result
  is a re-derivation inside a narrower branch and is labelled as such.

## 4. Frontier consequence

`WB2` is the finite theorem and owner of the all-order AP' conjecture, not a
specialization of the weighted `WB1` proof.  The live frontier removes that
unsupported edge and records `WB3` as an exact residual refinement.  The
finite `n=6,8` status and global status do not change.
