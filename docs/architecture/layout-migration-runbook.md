# Layout migration runbook

## Scope

This is the operating procedure for the repository's claim-centered
layout migration.

It governs file movement and migration provenance only.

It does not authorize mathematical changes.

The global Krenn–Gu conjecture remains **UNRESOLVED**.

## 1. Core migration invariant

The normal unit is a scientifically coherent claim package:

```text
claim/theorem document
primary verifier
independent audit when one exists
directly owned support material
```

Cross-links and imports do not establish ownership.

Shared dependencies remain shared.

Withdrawn/superseded work remains explicitly historical.

## 2. Authoritative migration artifacts

Human-reviewed source classification:

`catalog/layout-classification.json`.

Generated/executed manifest:

`catalog/moved-paths.json`.

Exact frozen approvals:

`catalog/batches/*.json`.

Migration reports:

`docs/architecture/layout-migration-*-report.md`.

## 3. Approval model

Classifier confidence is not approval.

No proposed move is executable merely because it is high-confidence.

Execution requires an exact named frozen batch containing the approved
old-path to new-path mapping and its mapping hash.

Every executed manifest entry records `executed_batch`.

## 4. Stage workflow

### A. Establish baseline

Start from merged `main`.

Record exact SHA.

Run the existing validation floor.

### B. Inventory a coherent mathematical family

Inspect claim documents, verifiers, audits, imports, inbound/outbound
links, replay commands, downstream consumers, snapshots, ledger
references, and external tools.

Classify related files by ownership rather than filename similarity.

### C. Human ownership review

Resolve the exact package boundary.

Update the durable source classification.

Do not silently promote classifier confidence.

### D. Dry-run

Record:

- selected members;
- excluded/deferred members;
- exact mappings;
- source status/family composition;
- dependency topology;
- expected replay requirements;
- projected manifest/root/stale transitions.

### E. Freeze exact batch

Create a committed batch artifact.

Validate its exact mapping and mandatory mapping hash.

Approval applies only to that mapping.

### F. Pure execution commit

Execute moves with the transaction-aware executor.

Do not repair links or imports in the pure move commit.

Immediately verify:

- source paths gone;
- destinations present;
- blobs byte-identical;
- eligible moves R100;
- `executed_batch` populated;
- manifest summary correct before any rebuild;
- root arithmetic correct.

### G. Mechanical repair

Run migration-aware rewriting.

Repair:

- Markdown links;
- fenced replay commands;
- Python imports/path constants;
- subprocess paths;
- shared-package exposure;
- ledger paths when applicable.

Do not edit mathematical prose.

Run the rewriter twice.

Second pass must be a fixed point.

### H. Scientific replay

Replay every practical moved verifier and independent audit.

Record environment, command, result, runtime, external binaries, and
generated-output location.

Do not claim a solver/backend ran in CI when it ran only manually.

Do not substitute withdrawn evidence for a live theorem.

### I. Navigation and report

Create/update family navigation.

Keep migration completeness separate from mathematical
exhaustiveness.

Update ledger paths/hashes only when existing curated entries require
it.

Do not fabricate ledger coverage merely because a theorem moved.

### J. Candidate-tree validation

Stage the complete candidate tree:

```bash
git add -A
```

Then run:

```bash
python check_hygiene.py
python -m unittest -v tests.test_migration_tools
python -m unittest -v test_fourteen_vertex_cycle_cover_lattice.py
python tools/migration/rewrite_links.py
git diff --exit-code
```

Current committed tooling is authoritative if commands change.

### K. CI bookkeeping

Finish substantive content.

Run `workflow_dispatch` on the substantive head.

Record exact run ID, SHA, and conclusion.

Make at most one report-only bookkeeping commit.

Require normal PR CI on the final head.

Do not create an infinite run-ID/commit loop.

## 5. Python portability

Use shared repository bootstrap/path machinery.

Prefer package-local `HERE` for owned sibling resources.

Prefer repository-root helpers for global resources.

Do not introduce absolute checkout paths.

Do not discover the repository by walking for `.git`.

Do not copy shared modules into a package merely to avoid dependency
analysis.

## 6. Replay commands

Fenced replay commands are canonical repository-root commands.

After a script moves, replay commands should use the root-relative
new path even when the document itself lives in the same package.

Ordinary non-command sibling links may remain package-relative.

The rewriter and stale scanner share replay-command grammar.

Do not manually work around a grammar defect; reproduce and fix the
shared parser with tests.

## 7. Manifest invariants

The executor is responsible for leaving summary counts internally
consistent inside its transaction.

Do not hide a stale summary by immediately rebuilding the manifest.

Record transitions immediately after execution.

If a batch spans several original classifier families/statuses,
account for each separately.

## 8. Scientific non-interference

A layout migration must not:

- strengthen a theorem;
- change assumptions;
- close a divisor;
- promote a candidate;
- reinterpret generic evidence as pointwise;
- repair a withdrawn proof;
- alter global conjecture status.

If replay exposes a mathematical inconsistency, stop migration of the
affected package and report the scientific issue separately.

### Replay and repository-state hygiene

Post-move scientific replay must not silently dirty tracked repository
state.

- After each replay tier, check `git status` / the tracked diff for
  unintended changes to result, certificate, or snapshot artifacts.
- Output-writing research/snapshot scripts must be run in a sandbox or
  copy, or not used as migration smoke tests at all, unless their
  tracked-output behavior is explicitly intended for this migration.
- `rc=0` alone is not a semantic success criterion for optional
  exploration/support scripts.  A script can exit 0 while encoding an
  inconclusive result (for example a `timeout_null`) in its output.
  Read the output before calling a replay green.

### Stale optional-dependency audit

Replay success does not prove that optional provenance dependencies
still resolve.  After a batch moves files, scan executable path
constants, not just imports:

- every root-relative `Path` construction;
- every optional dependency guarded by `.exists()` (these fail open and
  can silently drop a hash/provenance entry while still returning
  `rc=0`);
- hash and provenance inventories;
- subprocess targets;
- sibling theorem/verifier/audit constants.

Classify each occurrence rather than blindly replacing filenames:
same-package `HERE / basename` uses and historical prose strings are
legitimate; only executable root-relative references to moved paths
must be repaired.  An import probe is not sufficient for this audit
because fail-open `.exists()` paths are never exercised at import time.

## 9. End of migration

When the root migration is substantially complete, preserve this
document as migration history or move it into an explicitly
historical architecture area.

Do not keep obsolete migration procedure inside `AGENTS.md`.

The permanent scientific operating contract remains `AGENTS.md`.
