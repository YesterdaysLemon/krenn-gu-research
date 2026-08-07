# Proof-obligation architecture

## Status

The global Krenn–Gu conjecture is **UNRESOLVED**.

This document describes how analytic arguments, reductions,
computational certificates, independent audits, and formal methods can
compose into a proof.

It does not assert that the required obligations are currently closed.

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

Every leaf must be closed.

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

Do not create a machine-readable schema for these fields until the
actual post-migration proof DAG has been inventoried and the existing
theorem ledger has been reviewed for overlap.

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

## 6. Withdrawn and superseded lineage

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

## 7. Formalization target

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

## 8. When may the global status change?

Never because:

- one more verifier passes;
- a large search finds no examples;
- every currently known component is closed;
- all entries in a partial ledger are green;
- a generic theorem has no known bad divisor;
- an agent says there are no remaining cases.

A transition away from **UNRESOLVED** requires a dedicated
proof-consolidation audit.

That audit should reconstruct the global DAG from first principles
and adversarially check:

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

Only after no unresolved load-bearing leaf or edge remains should the
repository consider changing global status.

## 9. Future machine-readable obligation graph

After the layout migration is substantially complete, perform a
dedicated proof-DAG inventory.

Only then decide whether to extend the theorem ledger or create a
separate machine-readable graph.

Do not create two overlapping status databases accidentally.

A future schema may need separate fields for:

```text
mathematical_status
scope
dependencies
evidence_mode
certificate
primary_checker
independent_audit
formalization_status
formal_theorem
formal_assumptions
open_boundaries
```

but that design should be driven by real post-migration obligations.
