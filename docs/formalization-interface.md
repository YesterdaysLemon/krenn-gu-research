# Formalization interface

## Purpose

This repository contains exploratory computation, mathematical proofs,
proof replays, certificates, and provenance for work on the Krenn–Gu
conjecture.

A separate Lean development appears to formalize the same mathematical
problem or substantial parts of it.

The goal of this interface is to make the two efforts composable
without overstating their current relationship.

The global conjecture in this repository remains **UNRESOLVED**.

## 1. External Lean development

```text
repository:       KitaKen1/monochromatic-quantum-graphs-lean
inspected commit: d3ed1892ef181f5f5f5d61d9b5817f05b53a6675
Lean version:     v4.27.0 (lean/ edition); v4.33.0-rc1 (lean4web/ edition)
mathlib version:  mathlib4 a3a10db0e9d66acbebf76c5e6a135066525ac900
FC dependency:    google-deepmind/formal-conjectures
                  f7349f32ba6df6e7b7baf77467a3c6c7777a634d (pinned)
inspection date:  2026-08-07
```

Candidate identified during the documentation pass:

```text
KitaKen1/monochromatic-quantum-graphs-lean
```

Status until correspondence is explicitly audited:

```text
candidate external formalization;
relationship to this repository not yet assumed definitionally exact
```

### Facts established by inspection at the pinned commit

Read-only inspection (no build run) established the following:

- The project states a central theorem
  `QuantumLean.eqSystem_no_solution_ge6_ge3_int`:
  `∀ N D : Nat, N ≥ 6 → Even N → D ≥ 3 → ¬ ∃ W : WeightsN N D ℤ,
  EqSystemN N D W` — the **integer-weight** no-solution obstruction.
- It depends on the Google DeepMind Formal Conjectures catalogue at
  the pinned commit above; the statement types (`WeightsN`,
  `EqSystemN`) are imported from that pinned package, not redefined.
- `QuantumLean/FormalConjecturesWrappers.lean` proves twelve exact
  `answer(True) ↔ ...` wrapper propositions for the catalogue's
  integer targets (six arbitrary-integer, six `{-1,0,1}`-restricted);
  `lean/TwelveTheoremsAudit.lean` applies `#check` and
  `#print axioms` to each.
- No `sorry` and no project-specific `axiom` declarations appear in
  the Lean sources; the README records the expected final axiom
  closure as `propext`, `Classical.choice`, `Quot.sound` (ordinary
  foundational/classical assumptions) and explicitly excludes
  `sorryAx`, `Lean.ofReduceBool`, and `Lean.trustCompiler`.  This
  record is the project's own claim; a fresh `lake build` + audit
  run is the decisive confirmation.
- The `N = 4` base case uses four committed CNF/LRAT certificate
  pairs checked by mathlib's `lrat_proof` elaborator, so the external
  SAT producer is not trusted by the kernel.  A Python program is
  described as an independent regression check only, not part of the
  trusted theorem.
- The proof is explicitly described as an integer/characteristic-two
  contraction-iteration obstruction, not a conceptual solver-free
  proof.

These facts are about the external project alone.  They do not
establish that its statement matches the formulation used in this
repository; correspondence is still **pending audit** (section 2).

## 2. "Formalized in Lean" has several meanings

Use these conceptual milestones.

### L0 — statement encoded

A Lean proposition corresponding to the intended conjecture exists.

This is not a proof.

### L1 — statement correspondence audited

The Lean proposition has been compared carefully with the
mathematical problem used in this repository.

Audit at least:

- vertex/index conventions;
- graph/multigraph conventions;
- edge weights;
- color definitions;
- perfect matching definitions;
- monochromaticity condition;
- allowed coefficient domain;
- real/complex/integer assumptions;
- characteristic assumptions;
- nonzero hypotheses;
- normalization/equivalence conventions;
- quantifier order;
- exceptional small cases;
- dimension/local-dimension conventions;
- exact conjecture variant.

Only after this audit should this repository call the Lean statement
an authoritative formal counterpart.

Particular open question for this pair of projects: this repository's
frontier work is largely over complex/projective coefficient domains,
while the inspected Lean theorem is an integer-weight obstruction.
Whether the integer result closes, partially closes, or merely
interacts with the obligations tracked here is precisely what the
correspondence audit must decide — do not assume it.

### L2 — reductions formalized

Load-bearing reductions from the global conjecture to smaller
obligations are Lean theorems.

### L3 — certificate bridge formalized

Certificate semantics or the checker are connected to Lean strongly
enough that certificate acceptance yields the corresponding Lean
proposition.

Possible architectures include:

- a small checker implemented and verified in Lean;
- reflection where certificate data are evaluated inside Lean;
- an external checker plus a separately formalized soundness theorem
  and carefully delimited trust boundary.

Do not say an external Python/SAT/CAS run is Lean-verified merely
because Lean formalizes the surrounding mathematics.

(The external project's LRAT usage is an example of the third
pattern: an untrusted SAT producer, a kernel-checked proof trace.)

### L4 — obligations close formally

Every load-bearing leaf required by the master reduction has a Lean
proof, directly or through a formally justified certificate bridge.

### L5 — final theorem

The formal conjecture is proved from an understood and audited axiom
footprint.

## 3. Axiom and admission audit

When evaluating a Lean proof, inspect the actual dependency
footprint.

Specifically look for:

- `sorry`;
- `sorryAx`;
- project-specific `axiom` declarations;
- theorem wrappers that take the desired result as an assumption;
- admitted conjectures;
- imported files containing such assumptions.

Do not automatically treat foundational/classical axioms reported by
Lean as defects.

Record the distinction between:

```text
Lean/foundational assumptions
project-specific mathematical assumptions
temporary admissions
```

A project-specific axiom can be useful scaffolding, but a theorem
depending on it is conditional on that axiom.

## 4. Correspondence is a theorem-sized obligation

Two definitions that look similar in prose may differ formally.

Therefore the bridge:

```text
informal repository formulation
          <=>
Lean formulation
```

must itself be treated as a load-bearing obligation.

Prefer proving explicit equivalence/implication lemmas in Lean where
practical rather than relying forever on prose correspondence.

## 5. Certificate integration strategy

Do not formalize every search program.

Prefer:

```text
large untrusted producer
        |
        v
small certificate
        |
        v
small checker / formal semantics
        |
        v
Lean theorem
```

The expensive solver is allowed to be complicated if its answer is
not trusted.

High-value certificate formats are those whose correctness can be
checked with small exact kernels.

For each certificate family eventually record:

```text
mathematical obligation
instance encoding
producer
certificate format
checker
checker soundness status
Lean bridge status
hash/provenance
```

## 6. Synchronization policy

This repository and the Lean formalization should not silently drift.

When a load-bearing definition or theorem statement changes in either
project:

1. identify the corresponding artifact in the other project;
2. determine whether the correspondence remains valid;
3. update the recorded external commit;
4. rerun any formalization/correspondence checks;
5. do not claim formal coverage until the mismatch is resolved.

Avoid copying whole source trees merely to synchronize them.

Pin exact external commits when making claims about formal coverage.

## 7. What agents should do today

For ordinary mathematical work:

- use the Lean development as a source of definitions and already
  formalized lemmas when correspondence has been established;
- do not force every exploratory result into Lean immediately;
- flag especially load-bearing reductions as candidates for
  formalization;
- prefer certificate formats that admit a small formal checker;
- record when a new theorem would close a formal proof-DAG leaf.

For formalization work:

- start from a clearly named proof obligation;
- state the exact informal theorem being formalized;
- identify dependencies and assumptions;
- inspect axiom/admission status after the theorem checks;
- report whether the result proves a statement, a reduction, a
  checker-soundness lemma, or the final theorem.

## 8. Near-term formalization audit

A future dedicated pass should produce a correspondence report
between this repository and the external Lean project.

That pass should answer:

1. What exact Krenn–Gu proposition does Lean define?
2. Is it equivalent to the formulation used here?
3. Which finite results are already formally proved?
4. Which structural reductions are already formally proved?
5. Does any certificate checker already execute or verify inside
   Lean?
6. What project-specific axioms or `sorry` dependencies remain?
7. What theorem in the Lean project is closest to the global target?
8. Which open obligations in this repository correspond naturally to
   holes in the Lean proof?
9. What is the smallest next interface theorem worth formalizing?

Do not answer these questions by filename inference alone.
