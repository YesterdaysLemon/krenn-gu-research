# Layout migration report — Stage 5 (P4 triangle / 211 classification spine)

Status: **the first P4 classification spine is migrated.**  Fourteen
triangle / 211 classification packages (theorem + primary verifier +
independent audit each, plus one owned support script) moved from the
repository root into the new nested hierarchy
`claims/p4/classifications/triangle-211/`.  This is a human refinement
of the flat classifier output, frozen as one exact approved batch, and
replayed end-to-end without losing scientific or provenance integrity.

> No theorem claim, assumption, scope, provenance status, or
> global-resolution status changed as a result of this migration. The
> global Krenn–Gu conjecture remains **UNRESOLVED**.

## Provenance anchors

- Starting main SHA: `6d4b43f` (merged main including PR #32), tagged
  `stage5-start`.  Stage 4 verified present before any Stage 5 work
  (six component packages, `replay_command.py`, shared grammar in both
  rewriter and stale scanner, `expose_claim_package`, executor
  in-transaction summary recomputation, Stage 4 report + frozen batch).
- Branch: `layout-migration-stage5-p4-triangle-211`.
- Stage 4 leftover debt landed first (commit `532d424`): the 20
  replay-command rewrites the Stage 4 shared grammar produced but the
  merged Stage 4 tip did not stage, plus the 4 ledger hash fields they
  invalidated.  This is Stage 4 bookkeeping, not Stage 5 scope, and is
  recorded here for honesty.
- Batch: `p4-triangle-211-stage5`, artifact
  `catalog/batches/p4-triangle-211-stage5.json`:
  - approved_by: "YesterdaysLemon (repository owner), Stage 5 P4
    triangle/211 classification migration instruction";
  - approved_at: 2026-08-06;
  - base_sha: `f77994d` (Stage 5 commit A1);
  - informational manifest_sha256 recorded;
  - **mandatory** canonical mapping_sha256:
    `2838344305e6432707e98d1fa68f5865ae17c6029805204087198fb208ee37fd`;
  - member_count: **43**.
- Packages (14): 211-triangle-complete,
  common-active-211-triangle-projective-boundary,
  common-active-binary-triangle, common-kernel-yy-211-triangle-projective,
  crossed-211-triangle-support, cyclic-rank-one-triangle-support,
  rank-two-relation-triangle-corrected, transitive-rank-one-triangle,
  triple-kernel-rank-one-triangle, two-kernel-rank-one-triangle,
  all-rank-two-relation-triangle-inclusion,
  mixed-center-star-211-complete, unequal-endpoint-inward-star-211-complete,
  split-center-mixed-star-211.
- Pure-move commit: `efc20e4`; R100 count: **43 / 43**.

## Confidence composition and classification records refined

- **0 high-confidence members.**  Every selected record was
  `review_required` (medium theorem docs, low-confidence scripts, one
  medium tool_script).  Stage 5's human review resolved *ownership*
  (package membership, nested destination, triple completeness); no
  confidence field was promoted and no status was silently upgraded —
  the batch is an ownership/destination decision, recorded by approval,
  not a confidence promotion.
- **43 classification records refined** in
  `catalog/layout-classification.json` (the durable source), then the
  manifest regenerated through the normal `build_manifest.py`
  machinery.  Verified against the committed manifest: exactly 43
  pending records changed destination/family (`review_required ->
  review_required`), all 71 already-moved records byte-identical with
  `executed_batch` preserved 71/71, counts unchanged, no unrelated
  record touched.

## Root-count accounting (observed)

| Moment | Root entries |
|---|---|
| 1. original pre-migration root (`pre-layout-migration-v1`) | **2,366** |
| 2. Stage 5 starting `main` (`6d4b43f`) | **2,301** |
| 3. immediately after pure Stage 5 moves (`efc20e4`) | **2,258** |
| 4. final PR head | **2,258** |

Manifest tallies (observed, produced by the executor itself):

```text
stage5_files_moved                    43
stage5_root_entries_removed           43
cumulative_moved_entries              114
stale_paths_enforced (after)          114   (71 before + 43 = 114 ✓)
remaining_proposed_high_confidence    361   (unchanged; no high members)
remaining_review_required             1540  (1583 - 43)
remaining_unclassified                348
remaining_p4_classifications_proposals 122  (164 - 43, per classification summary)
```

## Executor acceptance test — real-world scaling

Immediately after the executor ran (before any rebuild), the manifest
already carried:

```text
counts.moved                        71 + 43 = 114       ✓
counts.proposed_high_confidence    361 (unchanged)      ✓
counts.review_required             1583 - 43 = 1540     ✓
projected_root_if_moved_only       2301 - 43 = 2258     ✓
```

`finalize_execution` re-derived every summary number from the records
inside the rollback-safe transaction; no manual rebuild was needed at
any point in Stage 5.  This is the first time the summary recomputation
scaled to a 43-file batch where **no member was high-confidence** (the
decrease lands entirely in `review_required`, not `proposed`).

## Dependency chain

Stage 5 exercised three relocation-sensitive chains:

```text
verify_p4_mixed_center_star_211_complete_classification
        imports (unconditional)
verify_p4_split_center_mixed_star_211_component      (both move)

verify_p4_common_active_binary_triangle_component
        imports (unconditional)
analyze_p4_common_active_binary_triangle_local_dimension   (moves, owned)
        imports (unconditional)
verify_p4_directed_zero_divisor_triangle_components        (STAYS: shared)

verify_p4_211_triangle_complete_classification
        reads 9 source docs (6 stay at root, 3 in sibling spine packages)
```

Clean-subprocess acceptance (fresh interpreter, only the repo root on
`sys.path`): mixed-center → split-center, CAB → analyze, analyze →
root directed-zero-divisor machinery, and the 211-complete SOURCES
resolution all pass.  No one-off `sys.path` shim was added; every new
bare-name import goes through `expose_claim_package`.

## Link and command rewrites

- Rewriter first pass: **82 links** re-anchored and **50 replay
  commands** repointed (plain `python`, `python3`, and `uv run --with
  sympy python` forms) across 34 files, **0 ambiguities**.  Second
  pass: **0 links, 0 commands, 0 ambiguities** (idempotent).
- **Zero manual replay-fence repairs.**  The Stage 4 shared
  replay-command grammar handled every command form in this batch,
  including the `uv run` wrappers; no new syntax form was discovered.
- Python path repairs: 7 moved scripts switched from `ROOT=parent` to
  the centralized bootstrap (siblings via `HERE`, root-resident docs
  and `tmp/` via `REPO_ROOT`); 16 staying consumers repointed their
  path constants/tuples (all-pair-rank reducer, two-double-endpoint
  classifier, four P5 H31 common-active-binary consumers, two
  candidate derives, two p+q boundary scripts, six component20
  derive/audit candidates).
- No theorem prose changed (verified by diff: only link targets,
  fenced command paths, and path constants).

## Replay results

All 14 packages replayed post-migration from the new locations
(working directory: repository root; outputs in `tmp/`, untracked).

| class | packages | verifier | audit | external binary |
|---|---|---|---|---|
| sympy-only | 12 packages | verified/pass (≤1 s each) | audited (≤1 s each) | none |
| split-center | 1 | verified (~3 s) | audited (~1 s) | none |
| common-active-binary | 1 | verified (~11 s) | audited (~1 s) | **Singular** via WSL (native `Singular` not on the Windows PATH) |

All 28 replay logs carry a positive verdict (`verified: true`,
`status: verified/audited/pass`, or `claim_label: VERIFIED`); the
independence marker is present in the 11 audits that emit it.  No
verifier was claimed without execution.

## Ledger

- **0 entries repointed.**  The theorem ledger is a curated partial
  index centered on the P5 H22/H31 generic-fibre claims; no entry
  referenced any of the 43 moving files.  No ledger entry was
  fabricated.
- **7 committed-blob hash fields refreshed** for docs whose content
  changed during reference rewrites: `README.md` (×3 entries),
  `P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md`,
  `P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION_WITHDRAWN_OVERSTRONG.md`,
  `P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md`,
  `P5_H31_SPLIT_CENTER_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`.
  All 85 ledger hashes validate.

## Stale-reference enforcement

Enforced old paths increased from 71 to **114** (71 + 43 = 114 ✓; 3
full-path, 111 root-to-package).  Zero stale references outside
provenance, checked across all supported replay-command forms
(`python`, `python3`, `wsl … python`, `uv run … python`, and
continuation-line `python \` + filename).

## Machinery behavior

- **Executor summary recomputation worked without rebuilding** — the
  exact acceptance numbers above were produced by `finalize_execution`
  inside the transaction; `check_hygiene.py [11]` agrees.
- **Rollback was NOT invoked** — no mid-batch failure.
- **Shared replay-command grammar remained effective** — zero manual
  fence repairs across 50 rewritten commands and all stale scans.
- **One pre-existing defect discovered and fixed before Stage 5 scope:**
  the merged Stage 4 tip had not staged the 20 replay-command rewrites
  its own shared grammar generated (nor the 4 ledger hashes they
  invalidated).  Landed as commit `532d424`.  Not a grammar defect.
- **No new migration-tool bug** in the executor, contract validator,
  summary recomputation, or rewriter.  The only new code is the nested
  metadata support + tests below.

## New tooling and regression tests

- Nested classification-spine package metadata resolves correctly
  through `package_metadata.resolve_claim_package_metadata` (manifest
  `claim_family` authoritative; canonical/verifier/audit share the
  package root; working notes are never canonical).  5 new regression
  tests (`NestedClassificationMetadataTests`); migration suite
  **98 → 103**.

## Validation floor (Step 25)

On the final head: `check_hygiene.py` all green (1,698 files compile;
all markdown links resolve; ledger 85/85 hashes; provenance 114/114;
stale paths 114 enforced, none present; portability clean; 5 fast
verifiers pass).  103 migration-tool tests OK.
`test_fourteen_vertex_cycle_cover_lattice.py` OK (14 tests).  Rewriter
idempotent (second pass 0/0/0).  No generated solver artifacts
committed.  CI: substantive-head workflow dispatch
[31159062067](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31159062067) passed (**success**) on the exact substantive head `478cef66dca1baced15790512e4b5da4baf6e287`; the subsequent report-fill
bookkeeping commit carries its own PR CI run, recorded on the PR.

## Stop condition

This PR does not begin another classification family and does not move
the remaining `p4/classifications` bucket (122 records stay pending).
Stage 5 proves that a rough classifier proposal can be human-refined
into a nested mathematical package hierarchy, frozen as an exact
approved batch, migrated at roughly twice Stage 4 scale (43 files vs
18), and replayed without losing scientific or provenance integrity.
Stage 6 may choose the next coherent family (likely mixed-star / star
classifications, or rank-two / tangent / lower-pair classifications).

> No theorem claim, assumption, scope, provenance status, or
> global-resolution status changed as a result of this migration. The
> global Krenn–Gu conjecture remains **UNRESOLVED**.
