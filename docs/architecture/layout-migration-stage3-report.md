# Layout migration report — Stage 3 (P4 component packages)

Status: **first real mathematical claim-family migration complete.**
Three full P4 pure-component theorem packages (theorem + primary
verifier + independent audit each) moved from the repository root into
`claims/p4/components/`, preserving provenance, replayability, links,
ledger integrity, and Git history.

> No theorem claim, assumption, scope, provenance status, or
> global-resolution status changed as a result of this migration. The
> global Krenn–Gu conjecture remains **UNRESOLVED**.

## Provenance anchors

- Starting main SHA: `295a875` (merged main including PR #30), tagged
  `stage3-start`.
- Branch: `layout-migration-stage3-p4-components`.
- Batch: `p4-components-stage3`, artifact
  `catalog/batches/p4-components-stage3.json`:
  - approved_by: "YesterdaysLemon (repository owner), Stage 3 P4
    component migration instruction";
  - approved_at: 2026-08-06;
  - base_sha: `7fb12b2` (commit A);
  - informational manifest_sha256 recorded;
  - **mandatory** canonical mapping_sha256:
    `17058a8819de3bcf051b81ba441249415493053c546f9a441d604941fa0fa327`;
  - member_count: **9**.
- Packages: disjoint-mixed-star, split-pair, equal-support-sixfold.
- Pure-move commit: `69ed945`; R100 count: **9 / 9** (every moved file
  recorded by Git as a 100%-similarity rename — history preserved, no
  content change).

## Root-count accounting (observed, kept separate)

| Moment | Root entries |
|---|---|
| 1. original pre-migration root (`pre-layout-migration-v1`) | **2,366** |
| 2. Stage 3 starting `main` (`295a875`) | **2,328** |
| 3. immediately after pure Stage 3 moves (`69ed945`) | **2,319** |
| 4. final PR head | **2,319** |

Moments 3 and 4 are equal because the only new files after the pure
move (the two P4 navigation indexes) were nested under
`claims/p4/`, not placed at the root.

Manifest tallies (observed, not projections):

```text
stage3_files_moved                    9
stage3_root_entries_removed           9
cumulative_moved_entries              53
stale_paths_enforced (after)          53   (44 before + 9 = 53 ✓)
remaining_proposed_high_confidence    379
remaining_review_required             1583
remaining_unclassified                348
```

(Unclassified files are never added twice; they are not members of any
move set.)

## Replay results (Step 13)

Every moved verifier and every moved audit was replayed post-migration
from the new locations.  The two verifiers that need Singular
(split-pair and equal-support-sixfold) ran in WSL (Singular 4.3.2);
the disjoint-mixed-star verifier is pure SymPy and needs no external
binary.

| Package | Verifier | Audit |
|---|---|---|
| disjoint-mixed-star | **verified=true** (pure sympy, 4 s) | audited=true, independent=true |
| split-pair | **verified=true** (Singular, 222 s) | audited=true, independent=true |
| equal-support-sixfold | **verified=true** (Singular, 68 s) | audited=true, independent=true |

All six import cleanly; all six compile.  No proof required hours or
unavailable binaries beyond the WSL Singular already established in the
repo.  Nothing was faked; every replay produced a committed-blob output
JSON with `verified`/`audited` true.

## Link and import rewrites

- Rewriter first pass: 34 links re-anchored across 20 files, 4 fenced
  replay commands repointed, 0 ambiguities.  Second pass: **0 links, 0
  commands, 0 ambiguities** (idempotent).
- Python: the six moved scripts switched to the centralized bootstrap
  (siblings via `HERE`, repo-root files via `REPO_ROOT`).  Six
  importers of the moved disjoint-mixed-star verifier (the canonical
  H22 verifier, three H22 boundary scripts, and two root scripts)
  expose the moved package directory before the bare-name import and
  repoint the component-doc/primary-script constants.  All six import
  OK — this exercises the already-migrated-source / later-moved-target
  case.
- No theorem prose changed.

## Ledger (Step 14)

- No theorem-ledger entry referenced the three moved docs (the ledger
  is a curated partial index; P4 component packages were not yet
  mapped), so 0 entries were repointed.  Provenance for the moved files
  lives in the manifest's `executed_batch` record.
- 12 committed-blob hashes were refreshed for docs whose content changed
  during reference rewrites; all 85 ledger hashes validate.

## Stale-reference enforcement (Step 16)

Enforced old paths increased from 44 to **53** (44 + 9 = 53 ✓).  Zero
stale references outside provenance.  Checked root markdown links,
`docs/` links, already-migrated P5 package links, Python subprocess/path
strings, replay commands, the ledger, and workflow comments.

## Shared dependencies deliberately left in place

- `verify_p4_mixed_orientation_pure_component.py` (imported by the
  disjoint-mixed-star verifier and the deferred all-rank-one-triangle
  verifier) stays at root.
- The four root docs referenced by the disjoint-mixed-star verifier,
  and research snapshots, stay where they are.

## Ambiguous files deliberately excluded

- **P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT** package deferred to
  Stage 4: its verifier both imports the moving disjoint-mixed-star
  package and is imported by two root P5 verifiers (ambiguous
  cross-package Python dependency).  Recorded in the dry-run report.

## Validation floor (Step 18)

On the final head: `check_hygiene.py` all green (1,697 files compile;
764 markdown files, all links resolve; ledger 85/85 hashes; provenance
53/53; portability clean; 5 fast verifiers pass).  74 migration-tool
tests OK.  `test_fourteen_vertex_cycle_cover_lattice.py` OK.  Rewriter
idempotent (second pass 0/0/0).  CI run
[31128660002](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31128660002)
passed (**success**) on the pure-migration head `3807a06` (hygiene
all checks, migration tests).  A final bookkeeping commit carries this
report text and the manifest-accounting invariant; its own CI run is
recorded on the PR.

## Stop condition

This PR does not begin another P4 batch.  Stage 3 demonstrates that
multiple complete theorem/verifier/audit claim packages can be moved
together with the Stage 2 machinery while preserving replayability,
provenance, links, ledger integrity, and Git history.

> No theorem claim, assumption, scope, provenance status, or
> global-resolution status changed as a result of this migration. The
> global Krenn–Gu conjecture remains **UNRESOLVED**.
