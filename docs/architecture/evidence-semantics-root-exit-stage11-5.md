# Stage 11.5 report -- evidence semantics and root-exit policy

Status: **contract and safeguards implemented; no scientific file moved and
no global-status change**

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Verified baseline

The live repository state was reconstructed before this pass:

- PR #39, Stage 10, is merged at
  `920c79621d1901ae41d5fc91e46ae0ed1c7ce44a`;
- local `main` and `origin/main` both resolve to that merge commit;
- Stage 11 exists as the pushed docs-only commit
  `5e46a0d9b35426f217a79b339d5fc8c12d588bc4` on
  `codex/stage11-p5-topology`;
- Stage 11 is the head of open draft PR #40 and has not reached `main`;
- the Stage 11 worktree was clean before Stage 11.5 changes; and
- `origin/main...5e46a0d` changes only `AGENTS.md`, the migration runbook,
  the proof-obligation architecture, and the Stage 11 topology report.

No intervening scientific commit changed the Stage 10 baseline or invalidated
the Stage 11 reconnaissance.  Stage 11.5 therefore extends the existing draft
review path rather than recreating or merging Stage 11 policy independently.

## 2. Decision

Stage 11's central finding is accepted:

```text
filesystem / classification
executable / provenance
mathematical proof obligations
```

are distinct graphs.  Stage 11.5 adds the missing semantic contract before
any proof-DAG schema or further proof-forest migration.

The durable contract is
[`docs/evidence-semantics-contract.md`](../evidence-semantics-contract.md).
Its operative decisions are:

1. scientific metadata is multi-axis rather than one verification ladder;
2. proof-active mathematical relationships are typed separately from
   evidence, implementation, provenance, audit, corroboration, frontier, and
   historical relationships;
3. the theorem ledger remains a partial claim index, not a proof graph;
4. every current `dependencies: []` means `not recorded`, never `none`;
5. root evacuation is mandatory as an end state, while current ambiguous
   artifacts remain grandfathered debt pending ownership review; and
6. no classifier confidence, root-debt pressure, import, hash, filename, or
   ledger lifecycle value authorizes a move.

No proof-DAG file or migration batch is created by this pass.

## 3. Ledger audit and contract

At the inspected baseline the ledger had 85 entries but only 82 distinct
documents.  All 85 entries had `dependencies: []`; there was no scope,
evidence-mode, execution-outcome, audit-independence, or formalization field.
The old `status` field therefore combined several axes.  Its baseline counts
were:

| status | count |
|---|---:|
| `verified_generic` | 50 |
| `verified` | 11 |
| `verified_finite` | 5 |
| `withdrawn` | 6 |
| `partially_withdrawn` | 4 |
| `partial` | 3 |
| `exploratory` | 2 |
| `candidate` | 1 |
| `framework` | 1 |
| `open` | 1 |
| `superseded` | 1 |

The ledger is now schema version 3.  It links to the permanent contract,
declares itself `partial_claim_index_not_proof_graph`, defines every allowed
legacy status, marks assumptions as a non-exhaustive navigation summary, and
declares evidence paths to be carrier mappings rather than theorem premises.

The old `independent_modular_audit` token is explicitly retained as a legacy
broad mapping label, not a literal assertion about method or complete
independence.  At baseline it labeled 51 entries although some mapped audits
are exact-rational and some share construction machinery.  A new narrow
`independent_exact_identity_audit` label is used for the repaired identity-only
case below.

Ledger documents are not unique claim identifiers.  Consumers must treat
`document -> entries` as a multimap.  The migration inventory now does so and
will auto-propose a legacy destination only when every indexed claim on that
document is unambiguously `withdrawn`.  It no longer treats
`partially_withdrawn` as automatic legacy ownership.

The component census remains a curated navigation snapshot.  Hygiene no
longer derives scientific counts from display-name prefixes; it validates the
snapshot's declared semantics and shape only.

## 4. Confirmed contradiction repaired

The baseline ledger entry for
`P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_FINITE_D01_BRANCH_B_GENERIC_OBSTRUCTION.md`
said `verified_generic`, mapped no primary or audit, and asserted generic
emptiness.  The pinned document instead says:

```text
WITHDRAWN AS A GENERIC OBSTRUCTION; VERIFIED IDENTITIES ONLY
```

It identifies an invalid coefficient split over `K`-valued free extensions,
leaves the complete Branch B obligation unknown, and names exact primary and
audit scripts.  Both scripts explicitly report that generic Branch B
emptiness is false as an output claim and that they verify identities only.

One composite entry could not preserve all three facts.  It is split into:

- an `open` entry for the complete finite-`D01` Branch B obligation, with no
  proof carrier and an explicit note that the old route is withdrawn; and
- a `verified` entry for the narrower characteristic-zero descent identities,
  with the exact primary and exact independent identity audit mapped.

The baseline also used one `candidate` entry as an aggregate for 23 boundary
documents while pinning a representative document whose own frozen
certificate is explicitly `REFUTED`.  That heterogeneous collection is now
`exploratory`, with explicit no-inheritance and non-proof-active semantics;
each underlying document still controls its own status.

The result is 86 entries: `verified_generic` decreases from 50 to 49,
`verified` increases from 11 to 12, `open` increases from 1 to 2,
`exploratory` increases from 2 to 3, and the unsafe aggregate `candidate`
entry is removed.  The `candidate` vocabulary remains available for granular
future entries.  No mathematical document, theorem, verifier, audit, or
global status changed.  The changes correct the index to match existing
committed evidence.

## 5. Root-exit baseline and active policy

Current Git state has:

```text
2,023 tracked root entries
2,014 root files
9 top-level directories
1,372 root .py files
615 root .md files
19 root .json files
4 root .cpp files
```

The seven present permanently justified files are:

```text
.gitignore
AGENTS.md
Containerfile
README.md
check_hygiene.py
requirements.lock.txt
requirements.txt
```

The other 2,007 root files are grandfathered root-exit debt.  This is a layout
count, not a count of claims, proof obligations, priorities, or safe batches.

`check_hygiene.py` now applies two different controls:

1. **active fail-closed ratchet** -- the frozen pre-migration classified and
   unclassified catalogs define the only grandfathered debt paths; their
   canonical 2,363-path set is pinned by SHA-256
   `2f4f1af23a89fa3ca56fe2114676c6324385aa1dbd7e5b6ddf35863511edd76c`;
   every manifest `moved` old path is retired from active debt; new or
   retired nonallowlisted root files and unknown top-level directories fail
   hygiene;
2. **end-state exact allowlist report** -- all 2,007 existing debt files are
   reported as warnings until ordinary migration has reduced them to zero.

The old regex families remain diagnostics only.  They are not the allowlist:
an unmatched `analyze_*.py`, a same-count rename, or a new arbitrary root file
cannot evade the active ratchet.

Strict exact-allowlist CI is deliberately not activated yet.  It requires a
dedicated end-state review after grandfathered debt reaches zero.  The numeric
target of 30 root entries remains a diagnostic and cannot replace exact path
justification.

## 6. Why this does not authorize migration

The frozen root universe permits a path to remain; it does not say where the
path belongs.  The pre-migration classifier is likewise operational evidence,
not ownership truth.  It currently proposes the repository-wide
`check_hygiene.py` entrypoint as an exploration tool solely because its name
starts with `check_`, demonstrating why prefix rules cannot decide ownership.

Future debt reduction still requires the full runbook:

- exact owner and live scientific surface;
- same-theorem case covers and residual chains;
- separation of proof edges from code/provenance/audit edges;
- candidate, partial, withdrawn, superseded, failed, timeout, and
  inconclusive lineage preserved;
- staying consumers and shared implementation known;
- exact human-reviewed batch; and
- pure move, mechanical repair, replay, and candidate-tree validation.

Ambiguity is a reason to defer, not a reason to keep a file at root forever
or to move it for structural symmetry.

## 7. Durable checks added

The migration test suite now covers:

- schema/contract linkage and declared status vocabulary;
- the reserved `dependencies` field and the exact meaning of `[]`;
- rejection of undeclared statuses;
- separate Branch B open-target and verified-identity entries;
- non-proof-active handling for the heterogeneous boundary-candidate
  collection;
- multimap lifecycle handling in the classifier;
- no automatic legacy route for `partially_withdrawn` or mixed-status docs;
- grandfathered root debt versus new root debt;
- same-count root renames;
- reappearance of an already retired old path;
- unknown top-level directories; and
- end-state allowlist reporting for prefix-unmatched files.

These tests validate metadata representation and migration safety.  They do
not prove that a mathematical status or scope is true.

## 8. Bounded read-only delegation

Three workers performed bounded read-only audits; the lead remained the sole
writer and status authority.

| audit | bounded surface | consequential result | lead action |
|---|---|---|---|
| ledger contract | all ledger entries, consumers, Branch B evidence | all dependencies empty; composite axes; duplicate documents; stale Branch B; partially-withdrawn routing risk | contract, split correction, semantic checks, multimap classifier |
| root exit | Git root, catalogs, inventory/hygiene tooling, CI | 2,007 debt files; regex policy incomplete; no-new-debt ratchet feasible | exact justified allowlist plus active ratchet |
| semantics adversary | operating/proof/formalization docs and representative evidence | proved/verified/lifecycle/outcome conflations; typed-edge and audit-independence requirements | permanent multi-axis and edge contract |

Every consequential policy decision was checked against the owning repository
files before integration.

## 9. Stop boundary and follow-up

Stage 11.5 stops before:

- moving or renaming scientific artifacts;
- editing layout-classification or moved-path records;
- freezing a migration batch;
- implementing a proof-obligation graph;
- mechanically normalizing all 86 ledger entries;
- extracting candidate-housed shared helpers; or
- beginning new proof work.

The next safe architectural task remains a bounded candidate-helper ownership
audit, followed by a whole-family dry run only after owner review.  Any future
proof graph must implement this contract explicitly rather than importing the
legacy ledger's composite status or empty dependency arrays.
