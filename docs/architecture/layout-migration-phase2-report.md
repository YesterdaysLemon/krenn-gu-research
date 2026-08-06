# Layout migration report — Phase 2 (navigation-docs batch + hardened contracts)

Status: **first real bulk batch executed; tooling contracts hardened.**
The global Krenn–Gu conjecture remains **UNRESOLVED**.  No theorem
claim was added, removed, promoted, or reworded in this phase; no
theorem status, assumption, scope, or meaning changed.

## Provenance anchors

- Starting state: `main` at `ba91ea0` (the merge of PR #29), tagged
  `phase2-start` locally.  All inventories in this phase are built
  from `pre-layout-migration-v1` (`f6d2cc4`), the true pre-migration
  base carried over from the pilot.
- Branch: `layout-migration-phase2`.
- Batch: `navigation-docs-phase2`, approval artifact
  `catalog/batches/navigation-docs-phase2.json`:
  - approved_by: "YesterdaysLemon (repository owner), Phase 2
    migration instruction";
  - approved_at: 2026-08-06;
  - base_sha: `081c54b` (contract-hardening head);
  - member_count: **8**;
  - mapping_sha256:
    `b981092ec090fca61c7c81d763bb81ab8903a271809a7c85d8291500b58db8a0`;
  - approval applies only to this exact mapping; it does not extend
    to later batches.

## Step 1 — tooling contracts hardened

### 1A. Frozen batch approval

`tools/migration/batch_contract.py` freezes the exact migration a
batch approves: `moves` (full old→new pairs), `member_count`,
canonical `mapping_sha256` (sorted-key, whitespace-free JSON of the
sorted mappings), `base_sha`, and `manifest_sha256`.
`execute_moves.py` now verifies before the **first** `git mv`:

- `approved_at` present;
- `base_sha` resolves in this repository;
- `member_count` equals the recorded mappings;
- no duplicate sources or destinations;
- the batch's own `mapping_sha256` matches its `moves` (batch
  unaltered after approval);
- every batch mapping equals the CURRENT manifest mapping (manifest
  has not drifted after approval).

Any violation refuses execution outright.

### 1B. Structural package metadata

`tools/migration/package_metadata.py` derives `claim_package`,
`proof_variant`, and `subpackage` from the manifest `claim_family` or
the well-defined `claims/<family>[/(alternate|boundaries)]` structure
— never from arbitrary path depth or manual patching.
`update_ledger()` uses the resolver; alternate proofs keep their own
package root and are distinguished only by `proof_variant`.

### 1C. Executed-batch provenance invariant

- The 36 PR-29 moves were backfilled with
  `executed_batch = p5-h22-disjoint-mixed-star-pilot` (paths and
  statuses untouched); the pilot batch was upgraded to the frozen
  schema.
- `build_manifest.py` now carries `executed_batch` forward across
  manifest rebuilds (a rebuild previously dropped provenance).
- `check_hygiene.py` enforces durably: every `status: moved` entry
  names a batch file that exists and freezes its exact mapping.

## Step 2 — test suite expanded

67 tests (was 39), all in CI.  New coverage:

- **Batch integrity**: valid frozen batch accepted; altered
  destination / member count / mapping hash refused; missing
  `approved_at`, duplicate source/destination, unresolvable base SHA,
  manifest drift, stale source, already-moved member — all refused;
  hash determinism and order-independence.
- **Provenance**: valid provenance passes; missing
  `executed_batch`, missing batch file, and mapping mismatch fail.
- **Ledger metadata**: canonical/alternate/boundary resolution,
  verifier-under-alternate, audit-under-boundaries, working note not
  canonical, non-claim `None`, manifest-family authority, structural
  derivation in `update_ledger`, hash recomputation, idempotent
  second pass, foreign-CWD operation, injected hash function.

## Step 3–5 — batch selection, approval, execution

Re-inventory of current `main` (`tracked=2516, root_files=2327`):
8 of the 10 candidate navigation docs are present, classified
high-confidence, with fixed destinations; the two attack-plan docs
(`SPARSE_RESULTANT_CORES_ATTACK_PLAN.md`,
`GRASSMANNIAN_PLUECKER_ATTACK_PLAN.md`) no longer exist on `main`
(stale classification entries) and were excluded rather than guessed.

Dry-run report:
[`navigation-docs-phase2-dry-run.md`](navigation-docs-phase2-dry-run.md)
(mappings, inbound/outbound link counts, replay commands, ledger
entries, the two derive scripts reading the handoff doc as INPUTS,
zero collisions).

Execution (pure `git mv`, commit `d833b22`): 8 files, all recorded as
`R100` renames, zero content changes in the move commit, no rollback
or recovery events.

| old path | new path |
|---|---|
| ASTRA_MATHEMATICS_TRANSFER_STRATEGY.md | docs/ASTRA_MATHEMATICS_TRANSFER_STRATEGY.md |
| CURRENT_FRONTIER.md | docs/current-frontier.md |
| LITERATURE_REVIEW_2026-07-30.md | docs/LITERATURE_REVIEW_2026-07-30.md |
| MERGE_AUDIT_REPORT.md | docs/audits/MERGE_AUDIT_REPORT.md |
| NEXT_INSTANCE_HANDOFF_2026-07-31.md | docs/NEXT_INSTANCE_HANDOFF_2026-07-31.md |
| RESEARCH_NOTES.md | docs/research-notes.md |
| STABILIZATION_AUDIT_REPORT.md | docs/audits/STABILIZATION_AUDIT_REPORT.md |
| SYMBOLIC_TRANSLATION_LITERATURE_FRONTIER_2026-08-02.md | docs/SYMBOLIC_TRANSLATION_LITERATURE_FRONTIER_2026-08-02.md |

## Step 6 — reference rewrites

`tools/migration/rewrite_links.py`:

- first pass: 349 links re-anchored, 0 ambiguities, 2 ledger entries
  repointed with recomputed committed-blob hashes;
- second pass: **0 links, 0 commands, 0 ambiguities** — idempotent;
- repairs: an already-re-anchored link whose target moved again is now
  remapped (alternate-proof link to the merge audit report); the stale
  checker masks display labels of links targeting a renamed file's new
  location; four certificate prose references and one workflow comment
  repaired to the new paths; the two derive scripts' `INPUTS`
  constants updated to the handoff doc's docs/ location (the file
  content hash recorded by those scripts is unchanged).

## Step 7 — stale-reference enforcement

Executed enforceable old paths: **44** (36 pilot + 8 this batch:
3 full-path including the two renamed docs and the ledger relocation,
41 root-to-package context-aware).  Zero stale references remain
outside provenance.  The count increased by exactly 8, the batch
size; no basename special case was needed.

## Step 8 — validation

Run on the final working tree:

- `python check_hygiene.py`: all checks passed — 1,697 Python files
  compile; no generated artifacts tracked; 759 markdown files, all
  local links resolve; ledger 85 entries, hashes recomputed 85/85,
  provenance and census consistent; portability clean; stale paths 44
  enforced, none present; provenance invariant 44/44; five fast
  verifiers pass.
- `python -m unittest tests.test_migration_tools`: 67 tests, OK.
- `python -m unittest test_fourteen_vertex_cycle_cover_lattice.py`:
  OK.

**Not run (stated explicitly, not implied):** no Singular replays, no
SAT/DRAT certificate replays.  This batch moved no executable proof
scripts, so none were required; none were claimed.

## Step 9 — root-count accounting

Observed counts, kept strictly separate:

1. original pre-migration root (`pre-layout-migration-v1`):
   2,363 files + 3 dirs = **2,366**;
2. post-PR-29 head before this batch (`ba91ea0`):
   2,327 files + 9 dirs = **2,336**;
3. root immediately after this phase's pure moves (`d833b22`):
   2,319 files + 9 dirs = **2,328**;
4. final PR head: **2,328** (reference rewrites changed no root
   entries).

Net change this phase: **−8 root entries**.  Net since the
pre-migration base: −38.

Projections (from the manifest, never adding the unclassified count
twice): moved-only 2,336; high-confidence batches executed 1,967; all
classified executed 357 (= 348 unclassified + retained files/dirs).

## Step 10 — ledger entries changed

Two entries repointed (status, assumptions, provenance untouched):

- "Transfer track: root-of-unity selector, hafnian lift, quotient
  catalogue" → docs/ASTRA_MATHEMATICS_TRANSFER_STRATEGY.md;
- "P6/P7 symbolic reductions (ARBITRARY_PERMANENT_* family)" →
  docs/SYMBOLIC_TRANSLATION_LITERATURE_FRONTIER_2026-08-02.md.

## Unresolved / unclassified

348 root files remain unclassified
(`catalog/unclassified-files.json`); 1,610 classified entries remain
`review_required`; 369 remain `proposed_high_confidence`.  None may
execute without an explicit, separately approved batch file.

## Explicit statement

No theorem claim changed.  No expensive proof was replayed or claimed
replayed.  The global conjecture remains **UNRESOLVED**.
