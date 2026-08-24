# Proof-obligation architecture

## Status

The global Krenn–Gu conjecture is **UNRESOLVED**.

This document describes how analytic arguments, reductions,
computational certificates, independent audits, and formal methods can
compose into a proof.

It does not assert that the required obligations are currently closed.

Vocabulary, lifecycle, evidence/audit semantics, typed relationship
rules, and the theorem-ledger boundary are authoritative in
`docs/evidence-semantics-contract.md`.

## 1. The target shape

The desired end state is a proof DAG, not a pile of successful
computations.

Conceptually:

```text
                       GLOBAL THEOREM
                             |
                    master implication
                             |
          +------------------+------------------+
          |                  |                  |
       COVER               FAMILY A           FAMILY B
          |                  |                  |
      case split        component/divisor  weighted/parameter
          |              obligations        obligations
          |                  |                  |
       leaves            proof leaves        proof leaves
      /certs/etc.       /certs/etc.         /certs/etc.
```

Every edge must be justified.

Every load-bearing leaf in the claimed proof route must be closed.
Unrelated, abandoned, or superseded branches need not be closed merely
because the repository preserves them.

The global theorem is not established while an unresolved leaf or
unjustified implication remains.

## 2. What an obligation must say

A proof obligation should eventually have enough information to
answer:

- What exact proposition must be proved?
- What are its quantifiers?
- Over what field/domain/characteristic?
- What nonzero or generic assumptions apply?
- Which divisors/boundaries are excluded?
- Is it generic or pointwise?
- What upstream results imply that this obligation is relevant?
- What downstream theorem depends on it?
- What evidence currently supports it?
- Is that evidence a mathematical proof, exact computation,
  certificate, independent audit, experiment, or formal theorem?
- Is there a Lean counterpart?
- What remains open?

Stage 11.5 reviewed the theorem ledger's semantics and reserved its
empty `dependencies` arrays as unpopulated.  Do not create a
machine-readable proof-DAG schema until the actual post-migration
obligations have been inventoried under the evidence-semantics
contract.

## 2A. Parent-theorem discipline and proof-distance accounting

Research progress is measured by justified edges in the proof DAG, not by
the number of nearby leaves.  Apply the operating rule:

> **No third sibling theorem without a serious parent-theorem attempt.**

For this purpose, two results are *siblings* when they refine nearby cells,
supports, ranks, divisors, or response profiles under the same open parent
obligation, while neither result:

- closes a proved exhaustive child cover;
- supplies a reusable implication used by at least two distinct downstream
  branches;
- refutes a proposed parent route by an exact control; or
- is already identified as load-bearing inside a recorded parent proof
  attempt.

The count follows the mathematical parent, not filenames, node labels,
branches, agents, or PR boundaries.  Splitting a census or changing notation
does not create a new lane.

A *serious parent-theorem attempt* must leave a durable research note, claim,
or frontier entry with all of the following:

1. the exact parent statement, including quantifiers, field, generic or
   pointwise scope, nonzero conditions, and exceptional fibres;
2. the upstream theorem that supplies its hypotheses and at least two sibling
   results it is intended to consume;
3. the downstream node or theorem that would become applicable;
4. an exact synthesis attempt using the siblings' mechanisms, not only their
   conclusions;
5. hostile tests against every relevant committed control and no-go result;
6. one of three honest outcomes: a proved implication, an exact
   countermodel/no-go, or a sharply stated obstruction naming the next
   load-bearing lemma; and
7. an explicit proof-distance delta.

The proof-distance delta is qualitative, not a scalar score.  State which of
the following occurred:

- an exhaustive child or implication edge closed;
- one parent obligation was replaced by strictly smaller typed obligations;
- two or more branches acquired a common reusable theorem;
- a proposed route was eliminated by an exact countermodel; or
- no frontier distance changed.

Every PR adding a local mathematical result must identify its parent
obligation and say which item above applies.  If no frontier distance changed,
the PR must state why the result is nevertheless load-bearing or why it falls
outside sibling research (for example an integrity repair, independent audit,
exact-counterexample escalation, or execution of an already proved exhaustive
finite cover).  This reporting requirement does not change the evidence
status of the result.

## 3. Certificate discharge rule

A computational certificate closes a mathematical obligation only
when the necessary bridge is present.

A robust certificate-backed proof leaf has:

### R — reduction soundness

A proved theorem shows that any forbidden mathematical object in the
obligation would produce an instance accepted by the computational
encoding.

Depending on the direction of the reduction, prove the exact
implication needed.

Do not assume an implementation "obviously represents" the
mathematics.

### X — exhaustive coverage

If many instances are used, prove that they cover every relevant
mathematical case after all stated symmetries and normalizations.

Coverage is itself a theorem.

### E — exact instance construction

Instance generation and canonicalization must be deterministic or
otherwise reproducibly pinned.

Inputs should be hashable and attributable to the mathematical case
they represent.

### C — checker soundness

Acceptance by the checker must imply the certificate's mathematical
meaning.

Prefer small checkers and exact arithmetic.

The generator/solver may be large and heuristic if its output is
independently checkable.

### Z — accepted witness

The actual certificate is present or reproducibly obtainable and the
checker accepts it.

### A — auditability

The certificate, instance, checker version, command, hashes, external
requirements, and expected outcome are recorded.

When R, any necessary X, E, C, Z, and A hold, the computational
certificate can serve as a rigorous proof leaf.

Without R/X, correct certificates may prove many cases without
proving the intended mathematical coverage.

Without C, the proof trusts the entire producer implementation.

Without Z, there is no checked witness.

## 4. Evidence classes are not a single ladder

Treat these as orthogonal evidence modes:

### Experimental evidence

Examples:

- random search;
- floating-point optimization;
- sampled finite fields;
- modular probes;
- heuristic solver failures;
- timeouts.

Useful for discovery.

Not proof by themselves.

### Reproducible exhaustive computation

All cases are enumerated by a specified program.

Potentially proof-producing, but the trusted computing base may be
large unless the enumeration or output is independently certified.

### Checkable certificate

An expensive producer emits a smaller witness accepted by a simpler
checker.

Examples may include SAT proof traces, explicit algebraic identities,
or exact elimination witnesses.

### Direct exact symbolic proof replay

A script checks identities or finite symbolic derivations that are
already mathematically explained in the theorem document.

The mathematical proof and its replay should not be conflated.

### Formal proof

A proof assistant kernel checks a proposition from explicit
definitions and assumptions.

Its relevance to the informal theorem still depends on statement
correspondence.

## 5. Generic to pointwise closure

A generic/function-field theorem is not automatically pointwise.

A typical valid closure pattern is:

```text
generic theorem
   +
explicit excluded divisor list
   +
proof/certificate for every divisor
   +
specialization/coverage theorem
   =
pointwise theorem
```

The excluded-divisor list is part of the proof obligation.

"No generic counterexample was found" is not a pointwise theorem.

## 6. Graph layers and typed relationships

A proof-obligation inventory must not collapse three different graphs:

```text
filesystem/classification
  where an artifact lives or appears structurally owned

executable/provenance
  what code imports, calls, replays, or hashes

mathematical proof obligations
  what claim, reduction, case cover, specialization, or boundary
  is needed for another mathematical conclusion
```

The graphs can legitimately disagree.  An imported row constructor may
be shared implementation rather than a theorem premise.  A hash may pin
a historical or corroborating artifact rather than establish logical
dependence.  Conversely, theorem prose can express a case union even
when no parent verifier executes every child.

A future graph should distinguish at least the following contract
relationships.  Their named endpoint roles and direction semantics are
defined in `docs/evidence-semantics-contract.md`; do not replace them with an
untyped generic arrow.

Mathematical relationships:

- **`mathematical_dependency`** — one dependent claim requires another
  claim as a premise;
- **`reduction_dependency`** — a proved transformation replaces an
  obligation with another precise obligation;
- **`case_coverage`** — children jointly exhaust a split, so no child
  alone proves the parent;
- **`specialization`** — a generic result descends to a locus under
  proved hypotheses;
- **`boundary_obligation`** — a divisor, fibre, endpoint, or projective
  chart remains after a generic result;
- **`residual_refinement`** — a partial factor/minor cover narrows the
  remaining obligation; and
- **`symmetry_transfer`** — a proved relabelling or involution transports
  closure between charts.

Evidence and implementation relationships:

- **`primary_evidence`** — a primary verifier checks or replays a claim;
- **`provenance_dependency`** — an immutable artifact is recorded or
  hashed for lineage or replay;
- **`implementation_dependency`** — code imports, calls, or subprocesses
  other code;
- **`shared_implementation`** — claims reuse machinery without one
  mathematically implying another;
- **`independent_audit`** — a distinct audit supports a claim at a stated
  layer but is not a
  mathematical premise; and
- **`corroboration`** — computation supports confidence without being the
  proof route.

Lifecycle and synthesis relationships:

- **`frontier_consumer`** — a broader, possibly open synthesis
  incorporates a local result;
- **`historical_evidence`** — superseded, withdrawn, failed, or earlier
  lineage is preserved but not
  proof-active; and
- **`refutation_of_argument`** — an attempted route is invalidated
  without necessarily deciding its target claim.

Node status, scope, and edge type are orthogonal.  Candidate, partial,
withdrawn, superseded, and refuted nodes may remain visible, but must
not become live premises merely because they are nearby, imported, or
hashed.  An independent audit must likewise be represented as evidence,
not as an extra mathematical hypothesis.

Generic-to-boundary closure is commonly a tree rather than one edge:

```text
generic claim
  -> divisor or specialization obligations
       -> branch cover
            -> exceptional fibres or residual factors
  -> projective boundary
  -> exhaustive closure theorem
```

Represent the exhaustive union explicitly.  Do not infer it from a
directory listing or from all child verifiers returning success.

## 7. Withdrawn and superseded lineage

Failed proofs are scientifically useful when clearly labeled.

A corrected theorem does not inherit the scope of an overstrong
withdrawn predecessor.

The proof DAG may record a historical edge:

```text
withdrawn claim
    --superseded_by-->
corrected live claim
```

but the withdrawn node cannot be used as a live proof dependency.

## 8. Formalization target

If the global conjecture already has a Lean formulation, that
formalization can become the semantic endpoint of the DAG.

The eventual strongest architecture is approximately:

```text
research/search code
        |
        v
certificate/witness
        |
        v
small exact checker
        |
        v
mathematical obligation
        |
        v
proved/formalized reduction
        |
        v
Lean obligation theorem
        |
        v
Lean master implication
        |
        v
Lean statement of Krenn–Gu
```

Not every intermediate theorem must be formalized immediately.

The highest-value formalization targets are the load-bearing
interfaces:

1. exact conjecture statement;
2. normalization and reduction soundness;
3. exhaustive-cover implications;
4. certificate/checker soundness;
5. final master implication.

## 9. How may the global status change?

Never because:

- one more verifier passes;
- a large search finds no examples;
- every currently known component is closed;
- all entries in a partial ledger are green;
- a generic theorem has no known bad divisor;
- an agent says there are no remaining cases.

The global conjecture may be resolved either by a complete proof or
by a rigorous counterexample/refutation.  A transition away from
**UNRESOLVED** therefore requires a dedicated resolution audit of one
of two kinds.

### Route A — proof

A claimed proof requires a dedicated proof-consolidation audit that
reconstructs the global DAG from first principles and adversarially
checks every definition, quantifier, normalization, case-cover edge,
specialization step, certificate bridge, and proof leaf used **by the
claimed proof route**:

- quantifier order;
- definitions;
- normalization legality;
- symmetry quotients;
- field and characteristic assumptions;
- exhaustive case coverage;
- generic-to-pointwise specialization;
- every excluded divisor;
- certificate encoding soundness;
- checker soundness;
- hashes/provenance;
- independence claims;
- Lean statement correspondence;
- Lean axiom/admission footprint;
- every final implication edge.

Only after no unresolved leaf or edge load-bearing **for that proof
route** remains should the repository consider changing global
status.  Unrelated, abandoned, or superseded research branches need
not be closed merely because they exist in the repository.

### Route B — counterexample/refutation

A claimed counterexample does not require closing the proof DAG.  It
requires a dedicated counterexample-validation audit checking at
minimum:

- exact original conjecture formulation;
- correct graph/matching/color conventions;
- coefficient domain;
- all quantifiers and dimension restrictions;
- exact witness data;
- all nonzero/support conditions;
- exact rather than numerical verification;
- deterministic/reproducible checking;
- provenance and immutable witness hash;
- at least one independent verification route where practical;
- correspondence to the Lean formulation if formal refutation is
  claimed.

A valid counterexample resolves the conjecture negatively even if
attempted proof programmes still contain open obligations.

Keep the global status **UNRESOLVED** during either audit, and do not
change it merely because one agent reports success.

## 10. Future machine-readable obligation graph

After the layout migration is substantially complete, perform a
dedicated proof-DAG inventory.

Stage 11.5 chose the safe boundary: the theorem ledger remains a
partial curated claim index, and a future typed proof-obligation graph
must be separate.  Do not create two overlapping status databases:
the graph should reference claim/evidence records under the shared
contract rather than copy composite ledger status as truth.

The current ledger `dependencies: []` means `not recorded`, never
`none`.  Do not mechanically derive mathematical dependencies from
imports, hashes, subprocess inventories, display-name prefixes, or
filename families.  Record executable, provenance, audit,
corroboration, frontier, and historical relationships separately from
direct live proof premises.

A future schema may need separate fields for:

```text
node_kind
mathematical_status
scope
lifecycle_status
verification_status
attempt_outcome
typed_relationships
evidence_mode
certificate
primary_checker
audit_outcome
audit_independence_scope
formalization_status
formal_theorem
formal_assumptions
open_boundaries
```

but that design should be driven by real post-migration obligations.
