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

A future graph should distinguish at least the following conceptual
relationships.  These names describe semantics; they do not freeze
machine-readable field names.

Mathematical relationships:

- **logical dependency** — one claim requires another as a premise;
- **reduction dependency** — a proved transformation replaces an
  obligation with another precise obligation;
- **case coverage** — children jointly exhaust a split, so no child
  alone proves the parent;
- **specialization** — a generic result descends to a locus under
  proved hypotheses;
- **boundary descendant** — a divisor, fibre, endpoint, or projective
  chart remains after a generic result;
- **residual refinement** — a partial factor/minor cover narrows the
  remaining obligation; and
- **symmetry transfer** — a proved relabelling or involution transports
  closure between charts.

Evidence and implementation relationships:

- **primary evidence** — a primary verifier checks or replays a claim;
- **provenance dependency** — an immutable artifact is recorded or
  hashed for lineage or replay;
- **executable dependency** — code imports, calls, or subprocesses
  other code;
- **shared implementation** — claims reuse machinery without one
  mathematically implying another;
- **audit edge** — a distinct audit supports a claim but is not a
  mathematical premise; and
- **corroboration** — computation supports confidence without being the
  proof route.

Lifecycle and synthesis relationships:

- **frontier consumer** — a broader, possibly open synthesis
  incorporates a local result;
- **historical or superseded** — lineage is preserved but not
  proof-active; and
- **refutation of argument** — an attempted route is invalidated
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
