# Full binary cycle program: review handoff

The global Krenn--Gu conjecture is **UNRESOLVED**. This checkpoint proves a
new necessary reduction and excludes a larger structural branch of the
common-star family. It also gives exact countercontrols to two proposed
ways of closing the remaining branch. It does not prove the parent FB or
supply a normal form for arbitrary witnesses.

## Short prompt to give another model

> Review the common-star full-binary parent checkpoint dated 2026-09-20.
> Read AGENTS.md and docs/current-frontier.md, then the two owning claims
> linked below, their independent reviews, and the exterior-coupling note.
> Audit the proof and quantifiers, not just whether programs exit zero.
> Full binary targets now force each proper induced directed cycle into
> one connected binary state resource. Resources with disjoint physical
> shores force a singleton-port Hamilton cycle, excluded by three-color
> S1/S2. Exact controls realize a one-sided cycle face at every length,
> and both three-cycle faces plus all 90 binary singleton/double cuts on
> nine components. The latter still fails word 001011111 with amplitude
> (r^2+1)/(12r), and lacks third-color S1/distinct-color S2. The unresolved
> step is the paired exterior-coupling lemma: can the full three-color
> equations prevent the mixed permanent terms from cancelling the explicit
> nonzero cycle term, including the case where changing an exterior
> component both adds a row and removes a column? Look for a gap in the
> accepted reduction, a proof of that implication, or an exact control
> satisfying its complete antecedent. Keep FB, CSQ4, arbitrary-witness
> coverage, and the global conjecture distinct.

## Read in this order

1. [Exact parent and attempt record](full-binary-parent-attempt-2026-09-20.md).
   FB ranges over every finite k>=2 common-star array over C, with one
   unequal-color gadget label per component pair. Full CSQ4 supplies its
   antecedent; excluding that common-star branch is its named consumer.
2. [PSCL: induced-cycle localization](../../claims/arbitrary-order/PROTECTED_SCAFFOLD_FULL_BINARY_CYCLE_LOCALIZATION.md)
   and its [independent review](../audits/COMMON_STAR_BINARY_CYCLE_LOCALIZATION_REVIEW_2026-09-20.md).
   The proof retains all exterior source terms, uses exact matching-row
   deletion and a subset induction, and never divides by an unproved
   exterior amplitude. The disjoint-shore classification weakens the
   earlier complete-biclique consumer. A written algebraic construction
   realizes the remaining one-sided face for every cycle length r>=3.
3. [PSCT: two-sided binary low-order closure no-go](../../claims/arbitrary-order/PROTECTED_SCAFFOLD_TWO_SIDED_BINARY_CYCLE_NO_GO.md)
   and its [independent review](../audits/COMMON_STAR_TWO_SIDED_CYCLE_REVIEW_2026-09-20.md).
   The parameter tower has degrees 2,4,2, with nonzero denominators proved
   by polynomial gcds. All cuts of sizes 1,2,7,8 are covered exactly.
   Independent literal matching recursion reconstructs all 36 physical
   vertices. This tests one binary pair, not the full three-color S2 system.
4. [Exterior-coupling identities and open lemma](full-binary-exterior-coupling-obligation.md)
   and their [independent assessment](../audits/COMMON_STAR_EXTERIOR_COUPLING_REVIEW_2026-09-20.md).
   The identities are exact; the assertion that some necessary equation
   must fail under the full three-color supply is unproved.

## Critical distinctions for review

- The source is a sum of products of two actual permanents, not an ordinary
  matching polynomial. Unequal center and leaf matchings matter.
- A resource may contain both color states of one physical component
  without a diagonal edge. PSCL does not assume disjoint physical shores
  in its general localization theorem.
- PSCL's all-length countercontrol is a written arbitrary-order proof.
  Its finite replay does not establish the quantifier over all lengths.
- PSCT is a finite exact construction. The 90-cut case cover is exhaustive
  for its stated low-order subsystem, not for all binary or ternary words.
- The independent PSCL physical audit uses separate standard-library
  quadratic-field arithmetic. The PSCT audit uses a different matching
  reconstruction and triangular reduction but shares SymPy with the
  primary. Both are separate-agent reviews, not human refereeing or Lean.
- Even a proof of FB would require a further arbitrary-witness reduction
  before resolving the global conjecture.

## Reproduce the mathematical companions

From the repository root:

```text
python claims/arbitrary-order/verify_common_star_binary_cycle_localization.py
python claims/arbitrary-order/audit_common_star_binary_cycle_localization.py
python claims/arbitrary-order/verify_common_star_two_sided_cycle_control.py
python claims/arbitrary-order/audit_common_star_two_sided_cycle_control.py
python -m unittest -v tests.test_common_star_binary_cycle_localization tests.test_common_star_two_sided_cycle_control
```

These companions include eleven scientific tests. In particular, they
reject changing factors while preserving edge products, discarding
permanent interference, treating a face as a full binary target, and
silently assuming a generic algebraic ideal proves parameter existence.
The repository integrity floor and proof-map checks are separate from
these mathematical acceptance checks. The owning reviews pin exactly
the theorem, replay, audit and test bytes they inspected.

No GPU job or paid model API was needed for this chunk. The bounded local
processes completed; no research process is handed off as live. Research
stops at the declared exterior-coupling gap after the accepted package is
published. Resuming it requires an explicit continuation request.
