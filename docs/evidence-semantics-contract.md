# Evidence semantics and root-exit contract

## Status and authority

This is the repository's durable contract for scientific metadata,
proof-obligation relationships, and the root-layout end state.

It defines what metadata means.  It does not assert that the metadata is
complete or mathematically correct merely because it conforms to this
contract.  The owning theorem document, its exact scope, and its evidence
still require scientific review.

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Metadata is multi-axis

Do not compress the following into one rank or one word:

1. **mathematical state** -- whether the stated proposition is proved,
   partial, open, or refuted;
2. **scope** -- global, generic/function-field, divisor-specific,
   boundary-specific, pointwise, finite, characteristic-specific, or other
   stated restrictions;
3. **evidence mode and assessment** -- written proof, exact replay,
   exhaustive computation, checkable certificate, formal proof,
   experiment, or unreviewed evidence;
4. **lifecycle** -- live, candidate, superseded, withdrawn, or historical;
5. **execution outcome** -- pass, fail, timeout, or inconclusive;
6. **independent-audit status** -- absent, not mapped, shared-construction
   audit, or independent at a stated layer; and
7. **formalization status** -- statement encoding, correspondence,
   formalized reductions, certificate bridge, closed obligations, or final
   theorem as defined in `docs/formalization-interface.md`.

A theorem can be proved without an independent audit or formalization.  A
program can pass while supporting only an experiment.  A timeout can occur
while the target theorem is true, false, or unresolved.  A withdrawn route
can retain correct identities.  Every consumer must preserve those
distinctions.

## 2. Vocabulary

These terms occupy different axes even when older repository metadata uses a
compact composite token.

### Mathematical and evidence terms

| Term | Exact meaning |
|---|---|
| `proved` | A mathematical argument establishes the proposition at exactly its stated scope.  This says nothing by itself about replay, independent audit, or formalization. |
| `verified` | The stated proof, certificate, or exact evidence has passed the recorded verification procedure.  Verification cannot enlarge the proposition's scope. |
| `verified_generic` | Legacy ledger shorthand for a proved and verified claim over the stated generic point or function field.  It does not include excluded divisors, special fibres, projective boundaries, or pointwise closure. |
| `verified_finite` | Legacy ledger shorthand for an exact accepted finite result.  The finite-to-mathematical bridge and any case-exhaustion theorem remain separate obligations. |
| `partial` | One or more exact subclaims are closed, but the stated parent obligation, case cover, divisor tree, or boundary family remains incomplete. |
| `candidate` | A proposed claim or route that has not passed the review required for live use.  A candidate name does not taint neutral imported code, and a candidate can later become proved, refuted, withdrawn, or superseded. |
| `experimental` | Evidence from search, sampling, numerical/modular probes, heuristic solvers, or other discovery work.  It is not a proof. |
| `exploratory` | An artifact or ledger entry whose role is reconnaissance, translation, or programme tracking rather than a proof-active conclusion. |

### Lifecycle and outcome terms

| Term | Exact meaning |
|---|---|
| `superseded` | A later artifact replaces this artifact for live use.  The older artifact is historical unless an explicit surviving subclaim is identified. |
| `withdrawn` | The formerly claimed conclusion or argument is explicitly non-live and cannot be used as a proof premise.  Correct identities may survive only at their separately stated narrower scope. |
| `partially_withdrawn` | A specifically identified part is withdrawn; only separately identified surviving subclaims remain live. |
| `failed` | An attempt, route, checker invocation, or run did not achieve its acceptance condition.  Failure does not prove the target proposition false. |
| `timeout` | Execution exceeded its declared limit.  It is neither a pass nor mathematical evidence of emptiness, satisfiability, or impossibility. |
| `inconclusive` | The available method or run did not decide its stated question.  It must not be normalized to pass, fail, open, or refuted without further evidence. |
| `refuted argument` | An argument or inference is invalidated.  The target proposition may remain open or may be proved later by a different route. |
| `refuted claim` | An exact counterexample or contradiction disproves the proposition at the stated scope.  A claimed global counterexample requires the dedicated validation route in `docs/proof-obligation-architecture.md`. |

`failed`, `timeout`, and `inconclusive` are normally execution or attempt
outcomes, not values of a mathematical claim-status field.

## 3. Typed relationship contract

Relationship type, source status, target status, and scope are independent.
An edge is never inferred solely from a filename, directory, import,
subprocess, hash, or shared data constructor.

The relationship roles below are authoritative; there is no generic
untyped-arrow convention.  A future schema must either use the named roles
shown here or declare an equivalent direction for each type.  Consumers must
not reverse an edge, treat every edge as `premise -> conclusion`, or traverse
heterogeneous relationships as though they had one common direction.

### Proof-active mathematical relationships

| Relationship | Named roles and meaning | Minimum acceptance condition |
|---|---|---|
| `mathematical_dependency` | `dependent_claim` uses `premise_claim`; the dependency direction is dependent to prerequisite, while proof flow runs from the premise to the dependent conclusion | the owning mathematical prose states the implication and preserves all hypotheses and scope |
| `reduction_dependency` | `original_obligation` is reduced to `reduced_target`; closing the target closes the original only through the recorded soundness implication | a proved soundness implication in the direction needed by the original obligation |
| `case_coverage` | `parent_claim` is exhausted jointly by one named `case_group` containing the children | an explicit cover theorem; isolated child edges or a directory listing are insufficient |
| `specialization` | `generic_source` is transported to a `specialized_target` locus | a proved specialization argument with legality, denominators, and hypotheses stated |
| `boundary_obligation` | analysis of `parent_scope` leaves a named `residual_boundary` such as a divisor, exceptional fibre, endpoint, or projective chart | the residual scope is stated; the parent is not closed until the required boundary route is closed |
| `residual_refinement` | an `exact_partial_result` narrows an `original_obligation` to a stated `remaining_residual` | the surviving residual and any lost cases are explicit |
| `symmetry_transfer` | a proved map transports a conclusion from `source_chart` to `target_chart` | the map, preserved hypotheses, and coverage of the target chart are proved |

`case_coverage` is set-valued: no single child proves the parent merely because
all children have ordinary dependency edges.  `specialization` and
`boundary_obligation` are not interchangeable: a generic result can create a
boundary obligation without proving any specialization to it.

### Evidence, implementation, and history relationships

| Relationship | Named roles and meaning | Proof-active? |
|---|---|---|
| `primary_evidence` | `claim` is supported by an `evidence_carrier`, such as a verifier, checker, certificate, or in-document proof | evidence for the node, not an extra theorem premise |
| `implementation_dependency` | `consumer_implementation` imports, calls, or subprocesses `used_implementation` | no |
| `shared_implementation` | named `claims` reuse one `shared_component` | no |
| `provenance_dependency` | `record` pins a `lineage_or_replay_artifact` by hash or immutable identifier | no, unless a separate mathematical edge is proved |
| `independent_audit` | an `audit_carrier` checks a `claim_or_evidence_carrier` at a stated layer | no; it raises confidence but is not a mathematical hypothesis |
| `corroboration` | `corroborating_evidence` supports a `claim` without forming the proof route | no |
| `historical_evidence` | a `current_record` retains a superseded, withdrawn, failed, or earlier `historical_artifact` for lineage | no |
| `frontier_consumer` | a broader `synthesis_consumer` records a `local_result` inside an open programme | no implication that the broader frontier is closed |
| `refutation_of_argument` | an `audit_or_countercheck` invalidates an `argument_or_inference` | no implication that the target proposition is false |

An audit's independence is scoped.  A no-import rederivation may be independent
at the implementation and algebraic-derivation layers.  An audit that shares
model construction or row generators can still be useful, but must not be
described as independent of the shared layer.

## 4. Current theorem-ledger contract

`catalog/theorem-ledger.json` is a **partial curated claim index**.  It is not
the proof DAG, a complete inventory of claims, or the authority for theorem
scope when it conflicts with the owning document.

The current `status` field is a legacy composite summary at the entry's
granularity.  Its permitted values and meanings are declared in the ledger.
Consumers must still read the entry's assumptions, owning document, evidence
mapping, and lifecycle.

The following rules are machine-checked:

- `completeness` remains `partial_curated` until a dedicated coverage audit
  changes the ledger's role;
- every status value used by an entry is declared and defined;
- `assumptions_and_excluded_divisors` and `external_binaries` remain arrays;
- verified entries have evidence provenance that explains mapped and null
  carriers; and
- every current `dependencies` value is `[]` under the state
  `reserved_unpopulated`.

For `dependencies`, an empty array means exactly:

```text
not recorded in this ledger
```

It does **not** mean:

```text
no mathematical dependencies
complete dependency inventory
independent theorem
no implementation, provenance, audit, or historical relationships
```

Do not populate this field mechanically.  A future machine-readable
proof-obligation graph must be a separately reviewed structure with typed
relationships, explicit scope, group semantics for case covers, lifecycle,
and provenance.  It must not be synthesized from imports, hashes, subprocess
lists, filenames, or the current empty arrays.

`primary_verifier` and `independent_audit` are evidence carriers, not proof
premises.  Their provenance labels describe the mapped carrier only; they do
not certify full methodological independence.  A null field paired with
`none_exists` is an explicit absence.  `not_yet_mapped` is an indexing gap.
Neither is a passing audit.

Ledger entries identify claims at the entry's granularity; `document` is not a
unique claim identifier.  One document can own several claims with different
statuses and scopes.  Consumers must retain all entries for a document and
must never use last-write-wins `document -> status` lookup.  Aggregate and
frontier entries are collections for navigation, not sources of inheritable
status for every artifact they mention.

When ledger metadata conflicts with the owning theorem or replay semantics:

1. stop any status-consuming migration or proof-graph work;
2. inspect provenance and the exact evidence output;
3. correct the index without changing the theorem's mathematical content;
4. add a regression check for a consequential contradiction; and
5. record any still-open target as an explicit obligation.

## 5. Root-exit policy

The end state is intentionally strict:

> Ordinary research documents, verifier scripts, audit scripts,
> experimental scripts, generators, result data, and similar loose scientific
> artifacts must eventually leave repository root.

The permanent root is limited to top-level navigation, repository
configuration, licenses/citation/contribution metadata, and explicitly
justified repository-wide entrypoints.  `check_hygiene.py` contains the exact
path allowlist and a justification for every permitted file and directory.

Root location is an operational state, not scientific metadata.  Moving a
file cannot prove, verify, promote, withdraw, or supersede a claim.

### Phase R1 -- no new root debt (active)

The pre-migration classifier and unclassified-file catalogs freeze the
grandfathered root-path universe.  Hygiene pins both its 2,363-path count and
the SHA-256 of its canonical sorted path set, so editing a catalog cannot
silently expand the baseline.  `check_hygiene.py` fails if:

- a new non-allowlisted root file appears outside that frozen universe; or
- an executed old path reappears after retirement from active debt; or
- a grandfathered path disappears without a manifest-recorded migration
  retirement; or
- an unapproved top-level directory appears.

Grandfathering means only that an existing path may remain while ownership is
reviewed.  It is not a classification, destination, status, approval, or
waiver.  A same-count rename does not evade the ratchet, and direct deletion
is not a legal debt-reduction transaction that can reserve a path for later
recreation.

The frozen catalogs contribute only their root-path set to this ratchet.
Their classification and status-evidence strings are snapshot provenance,
not current scientific metadata or migration authority.

An allowed top-level directory is likewise not a dumping ground.  Its
allowance covers only the ownership class named by its justification; placing
an artifact under `tools/`, `docs/`, or another allowed directory still
requires that directory to be its real owner.

### Phase R2 -- reviewed debt reduction (active migration workflow)

Grandfathered debt can leave root only through the normal migration contract:

1. reconstruct filesystem/classification, executable/provenance, and
   mathematical proof-obligation topology separately;
2. resolve ownership and evidence boundaries;
3. perform a documented dry run;
4. obtain an exact frozen batch reviewed by an authorized reviewer;
5. use `git mv` through the transaction-aware workflow; and
6. validate paths, blobs, provenance, replays, and root arithmetic.

Authorized review follows
`docs/architecture/layout-migration-runbook.md`.  Under the repository
owner's standing delegation dated 2026-08-08, Codex may act as the actual
reviewer for routine, non-ambiguous, evidence-backed exact layout mappings;
the batch must identify Codex and the delegation basis.  Scientific status or
scope, genuinely ambiguous proof-boundary ownership, and architectural choices
requiring owner preference remain owner-gated.

Root-exit pressure never resolves ambiguous ownership.  When a family is
mathematically entangled, it remains grandfathered debt until its boundary is
understood.

Lifecycle metadata is likewise not a destination rule.  In particular,
`partially_withdrawn` requires the surviving and withdrawn subclaims to be
separated before ownership review; it must not automatically route the whole
document to a legacy package.  Only an unambiguous all-withdrawn document can
use withdrawn status as supporting evidence for a legacy proposal, and even
then classifier output is not move approval.

### Phase R3 -- exact end-state enforcement (not yet active)

The current hygiene report compares the tree to the exact allowlist but keeps
pre-existing debt warning-only.  Activate strict end-state enforcement only
after a dedicated review confirms that grandfathered debt is zero and all
remaining exceptions are intentional.  At that point CI must reject every
nonallowlisted root path; the numeric root target is only a diagnostic, not a
substitute for exact path policy.

At the Stage 11.5 baseline there are 2,023 tracked root entries: 2,014 files
and 9 directories.  Seven present files have permanent justifications, so
2,007 files are grandfathered root-exit debt.  This count is layout debt, not
a claim count or migration priority.

## 6. Decision rules for future stages

Before a proof-forest migration, reviewers must be able to state:

- the exact claim and scope owned by every live document;
- whether each verifier/audit is primary evidence, independent at a stated
  layer, corroboration, implementation, provenance, or history;
- all same-obligation case-cover, specialization, boundary, residual, and
  symmetry relationships;
- which candidate, partial, withdrawn, superseded, failed, timeout, or
  inconclusive artifacts must remain visibly non-live; and
- why every proposed destination owns the artifact independently of the desire
  to clean root.

Stop rather than migrate when any answer is unknown.  The artifact still must
eventually leave root, but only after the uncertainty is resolved and an exact
batch is approved.
