# Agent operating contract

This repository contains computational and analytic research on the
Krenn–Gu monochromatic quantum graph prize conjecture.

The global conjecture is **UNRESOLVED**.

This file is the durable operating contract for automated agents and
human contributors working with agent assistance.  Detailed procedures
live in linked runbooks; this file contains the invariants that should
remain valid when the current layout migration is over.

## 1. Reconstruct context from committed evidence

Before asking the repository owner to restate prior work, inspect the
current tree and the relevant committed documentation.

Use focused retrieval rather than reading every historical file.

For operational/layout questions, current Git state is authoritative.

For scientific questions, do not confuse committed state with
mathematical truth.  Read the claim's status, assumptions, provenance,
dependencies, verifier/audit evidence, and any formal counterpart.

If documentation conflicts with actual paths or tooling, investigate
the discrepancy.

If two scientific artifacts make conflicting claims, do not decide
that the newer file is automatically correct.  Establish provenance
and report the conflict.

## 2. Preserve scientific status

The following distinctions are mandatory:

- conjecture vs theorem;
- theorem vs reduction;
- reduction vs obstruction;
- proof vs experiment;
- exhaustive computation vs sampling;
- computational certificate vs an unconnected computational result;
- generic/function-field statement vs pointwise statement;
- live vs candidate vs exploratory;
- live vs withdrawn vs superseded;
- exact result vs numerical/modular evidence.

Never strengthen a quantifier, assumption, divisor scope, field,
characteristic, support condition, or genericity statement silently.

A file move or documentation cleanup never changes mathematical
status.

The global Krenn–Gu status remains **UNRESOLVED** until a dedicated
resolution audit validates either:

- a complete proof route, for which every edge and leaf load-bearing
  **for that claimed proof** is closed (not every open research
  obligation in the repository; unrelated, abandoned, or superseded
  branches need not be closed merely because they exist); or
- an exact counterexample/refutation satisfying the original
  definitions and quantifiers and independently validated.

## 3. Evidence is multi-axis

Do not compress all evidence into one notion of "verified."

A claim can independently have:

- a mathematical status;
- a scope (generic, divisor-specific, pointwise, finite, etc.);
- a computational evidence mode;
- an independent-audit status;
- a formalization status.

For example, a theorem can be mathematically proved but not
formalized, or a conjecture can be formalized as a Lean proposition
but remain unproved.

Preserve all of these distinctions.

`proved`, `verified`, `verified_generic`, `partial`, `candidate`,
`experimental`, `superseded`, `withdrawn`, `failed`, `timeout`, and
`inconclusive` do not form one ladder.  In particular, failure,
timeout, and inconclusive are attempt/run outcomes; withdrawn and
superseded are lifecycle states; and genericity is scope.  Use the
authoritative vocabulary and typed-relationship rules in:

`docs/evidence-semantics-contract.md`.

## 4. Computational certificates and proof obligations

A certificate is not automatically a proof of the global theorem.

A computational certificate may rigorously discharge a mathematical
proof obligation when the repository also supplies the required
mathematical bridge.

The ideal pattern is:

1. a proved reduction maps the mathematical obligation to a precise
   computational instance or finite family of instances;
2. any claimed case cover is itself proved exhaustive;
3. certificate semantics are specified;
4. a sound checker verifies the certificate using exact computation;
5. instance generation/canonicalization is reproducible;
6. hashes or other immutable identifiers pin the checked objects;
7. the accepted certificate implies the mathematical obligation.

When these conditions hold, the certificate is a proof leaf inside a
larger mathematical proof.

A thousand correct certificates do not prove a global theorem if the
repository has not proved that the certified cases exhaust all
possibilities.

See:

`docs/proof-obligation-architecture.md`.

## 5. Independent verification

A primary verifier and an independent audit have different purposes.

Do not call two scripts independent merely because they have different
filenames or random seeds.

Independent evidence should, where practical, differ in derivation,
implementation route, representation, algorithm, or checker.

If no independent audit exists, record that absence explicitly rather
than inventing one.

If a verifier replays only displayed identities and is not the proof
itself, say so.

## 6. Formal methods and Lean

An existing Lean formalization is a valuable semantic anchor, but
"formalized in Lean" is not one binary state.

Distinguish:

- the target statement is encoded;
- correspondence with the intended informal statement is audited;
- reductions are formalized;
- certificate semantics/checkers are formalized;
- the final theorem is kernel-checked from understood assumptions.

Do not claim that an informal theorem is formally proved solely
because a similarly named Lean theorem exists.

Audit quantifiers, definitions, graph conventions, coefficient
domains, field/characteristic assumptions, nonzero hypotheses,
equivalence relations, indexing, and imported assumptions.

Project-specific `axiom` declarations, `sorry`/`sorryAx`, admitted
conjectures, or wrapper assumptions must be surfaced explicitly.
Do not conflate these with ordinary foundational/classical
assumptions.

See:

`docs/formalization-interface.md`.

## 7. Mathematical research mode

When doing mathematical research:

- state the exact obligation being attacked;
- state its assumptions and scope;
- identify upstream dependencies;
- identify what would count as success;
- separate experimental evidence from proof-producing work;
- keep failed approaches when they are scientifically informative;
- preserve withdrawn/superseded lineage;
- prefer exact arithmetic for proof claims;
- record external solver/tool requirements honestly;
- never promote a timeout, failed search, modular experiment, or
  numerical observation into a proof.

If work appears to close a major frontier, do not immediately rewrite
the global status:

- a candidate proof triggers an adversarial proof-consolidation
  audit;
- a candidate counterexample triggers an adversarial
  counterexample-validation audit (escalate an apparent exact
  counterexample rather than casually promoting or dismissing it);
- neither changes global status merely because one agent reports
  success.

## 8. Software and verifier mode

Prefer reproducible, portable tooling.

Do not add machine-specific checkout paths.

Do not rely on `.git` discovery when repository helpers already exist
(`src/krenn_gu/bootstrap.py` provides the shared path machinery).

Use shared bootstrap/path machinery rather than proliferating one-off
`sys.path` hacks.

Generated solver outputs should remain untracked unless the repository
explicitly treats a particular artifact as durable certificate data.

Large search programs should ideally produce smaller independently
checkable witnesses.

## 9. Layout-migration mode

The active layout-migration procedure is documented separately:

`docs/architecture/layout-migration-runbook.md`.

Do not infer migration approval from classifier confidence.

Only exact, frozen, human-approved batches are executable.

Use `git mv`; preserve history and scientific content.

Do not opportunistically edit mathematics during migration.

### Root-exit invariant

Ordinary research documents, verifiers, audits, experiments,
generators, and similar executable artifacts must eventually leave
repository root.  Existing root debt may remain only while ownership
and evidence boundaries are investigated.  It is not permanently
root-owned merely because a safe batch is not yet known.

The no-new-debt ratchet and exact end-state allowlist are defined in
`docs/evidence-semantics-contract.md` and enforced by
`check_hygiene.py`.  Root-exit pressure never authorizes a move,
resolves ambiguous ownership, or changes scientific status.

### Proof-boundary ownership

- Reconstruct filesystem/classification, executable/provenance, and
  mathematical proof-obligation topology separately; they may
  legitimately disagree.
- Do not infer mathematical ownership or logical dependence from a
  filename, import, subprocess call, or hash alone.
- Move a generic core separately only after demonstrating that its
  specialization, boundary, exceptional-fibre, and case-coverage
  descendants are not pieces of the same obligation.
- Preserve the actual, potentially asymmetric theorem/verifier/audit
  surface.  Candidate, partial, historical, or refuted artifacts must
  not become verified proof evidence merely through code reuse or
  proximity.
- When proof-boundary ownership remains ambiguous, investigate before
  migrating.

## 10. Candidate-tree validation

Authoritative local validation uses an index-complete candidate tree.

Before the final validation floor:

```bash
git add -A
python check_hygiene.py
python -m unittest -v tests.test_migration_tools
python -m unittest -v test_fourteen_vertex_cycle_cover_lattice.py
python tools/migration/rewrite_links.py
git diff --exit-code
```

If current repository tooling changes this contract, follow the
committed runbook/tool documentation rather than stale prose here and
update this file in the same change.

## 11. Where to look

Current filesystem and code:
Git.

Proposed layout ownership:
`catalog/layout-classification.json`.

Executed layout migration:
`catalog/moved-paths.json`.

Frozen migration approvals:
`catalog/batches/`.

Curated theorem/provenance index:
`catalog/theorem-ledger.json`.

Evidence vocabulary, relationship types, ledger semantics, and root
end state:
`docs/evidence-semantics-contract.md`.

Proof-obligation philosophy:
`docs/proof-obligation-architecture.md`.

Formalization/Lean correspondence:
`docs/formalization-interface.md`.

Migration procedure:
`docs/architecture/layout-migration-runbook.md`.

Per-family mathematics:
the relevant claim package and its own README/status documents.

## 12. Stop conditions

Stop and report rather than silently repairing when:

- a claimed proof contradicts its verifier;
- an apparent exact counterexample appears anywhere in the work —
  escalate it for dedicated validation before any status claim;
- a supposedly independent audit is not independent;
- a live theorem appears to rely on a withdrawn step;
- an exhaustive case split is not actually exhaustive;
- a generic result is being used pointwise without a specialization
  argument;
- a computational instance is not proved equivalent/sufficient for
  the mathematical obligation;
- a Lean proposition appears not to match the intended informal
  statement;
- a proof depends on an unexplained project-specific axiom or
  admission;
- migration ownership is ambiguous;
- completing the requested task would require changing mathematical
  meaning outside its scope.

Uncertainty should become an explicit open obligation, not an
unrecorded assumption.
