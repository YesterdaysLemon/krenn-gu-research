# Layout migration report — Stage 6 (P4 star / mixed-star classification spine)

Status: **the second P4 classification spine is migrated.**  Seventeen
star / mixed-star classification packages (theorem + primary verifier +
independent audit each) moved from the repository root into the new
nested hierarchy `claims/p4/classifications/star/`.  This is a human
refinement of the flat classifier output, frozen as one exact approved
batch, and replayed end-to-end without losing scientific or provenance
integrity.  Stage 6 is the first stage above 43 moved files and proves
the workflow scales: larger batch, more staying consumers, more
cross-spine dependencies, zero new machinery defects.

> No theorem claim, assumption, scope, provenance status, or
> global-resolution status changed as a result of this migration. The
> global Krenn–Gu conjecture remains **UNRESOLVED**.

## Provenance anchors

- Starting main SHA: `a342d12` (merged main including PR #33 / Stage 5).
  Stage 5 verified present before any Stage 6 work (14 triangle/211
  packages, `p4-triangle-211-stage5.json` batch, dry-run, report,
  rewriter fixed-point CI step).
- Branch: `layout-migration-stage6-p4-star-classifications`.
- Commits: A `50a8eb8` (classification refinement + dry-run),
  B `022865b` (frozen batch), C `11e5d48` (pure git-mv),
  D `0ab4a75` (mechanical repairs), E (navigation, ledger hashes,
  this report).
- Batch: `p4-star-stage6`, artifact
  `catalog/batches/p4-star-stage6.json`:
  - approved_by: "YesterdaysLemon (repository owner), Stage 6 P4
    star/mixed-star classification migration instruction";
  - approved_at: 2026-08-07;
  - base_sha: `50a8eb8` (Stage 6 commit A);
  - informational manifest_sha256
    `8ecfe9506236d4be069cad6feff141e04a7ffbf945b8a0a72dd456927c046de4`;
  - **mandatory** canonical mapping_sha256:
    `25c91c812a1f0138b0a12a477406836d8f0bb97d3cb0caf42d2e6cde4de57fb7`;
  - member_count: **51**.
- Packages (17): all-center-kernel-star-111-obstruction,
  all-double-endpoint-star-111-obstruction, coincident-support-rank-one-star,
  coincident-support-star-reverse, common-center-kernel-star-211,
  disjoint-mixed-star-affine, disjoint-mixed-star-projective,
  equal-endpoint-inward-star-211-obstruction,
  mixed-endpoint-star-111-complete, no-double-endpoint-star-1110-collision,
  one-double-endpoint-star-111, radical-star,
  rank-two-relation-star-obstruction, two-double-endpoint-star-111-complete,
  two-rank-two-spoke-mixed-star-classification,
  two-rank-two-spoke-mixed-star-component, unequal-endpoint-inward-star-211.
- Pure-move commit: `11e5d48`; R100 count: **51 / 51**.

## Confidence composition and classification records refined

- **0 high-confidence members.**  Every selected record was
  `review_required` (17 medium theorem docs, 34 low-confidence
  scripts).  Stage 6's human review resolved *ownership* (package
  membership, nested destination, triple completeness); no confidence
  field was promoted and no status was silently upgraded — the batch
  is an ownership/destination decision, recorded by approval, not a
  confidence promotion.
- **51 selected records** refined in
  `catalog/layout-classification.json` (the durable source), then the
  manifest regenerated through the normal `build_manifest.py`
  machinery.  Verified against the committed manifest: exactly 51
  pending records changed destination/family (`review_required ->
  review_required`), all 114 already-moved records byte-identical
  with `executed_batch` preserved 114/114, counts unchanged, no
  unrelated record touched.
- Of the 51, **12 were originally classified `p4/boundaries`**
  (the four star-cell orientation obstructions:
  all-center-kernel-star-111, all-double-endpoint-star-111,
  equal-endpoint-inward-star-211, rank-two-relation-star, each with
  verify + audit).  Each document states it closes or excludes an
  orientation of the star `(1,1,1)` or `(2,1,1)` cell, so ownership
  is genuinely star-specific; human review reassigned them into the
  star spine.  Accounted separately in the root arithmetic below
  (family reassignment, not a classifications-bucket subtraction).

## Root-count accounting (observed)

| Moment | Root entries |
|---|---|
| 1. original pre-migration root (`pre-layout-migration-v1`) | **2,366** |
| 2. Stage 6 starting `main` (`a342d12`) | **2,258** |
| 3. immediately after pure Stage 6 moves (`11e5d48`) | **2,207** |
| 4. final PR head | **2,207** |

Manifest tallies (observed, produced by the executor itself):

```text
stage6_files_moved                    51
stage6_root_entries_removed           51
cumulative_moved_entries              165
stale_paths_enforced (after)          165   (114 before + 51 = 165 ✓)
remaining_proposed_high_confidence    361   (unchanged; no high members)
remaining_review_required             1489  (1540 - 51)
remaining_unclassified                348
remaining_p4_classifications_proposals 83   (122 - 39; the other 12 members came from p4/boundaries)
```

## Executor acceptance test — real-world scaling at 51 files

Immediately after the executor ran (before any rebuild), the manifest
already carried:

```text
counts.moved                        114 + 51 = 165      ✓
counts.proposed_high_confidence    361 (unchanged)      ✓
counts.review_required             1540 - 51 = 1489     ✓
projected_root_if_moved_only       2258 - 51 = 2207     ✓
```

`finalize_execution` re-derived every summary number from the records
inside the rollback-safe transaction; no manual rebuild was needed at
any point in Stage 6.  All 51 members came from `review_required`, so
the entire decrease lands there (0 from `proposed_high_confidence`);
the two starting-status categories are accounted separately above.

## Dependency chain

Stage 6 exercised a substantially larger dependency surface:

```text
zero intra-batch Python imports (verified by full regex scan)

three moving verifiers reference moving sibling DOCS via root constants:
    mixed-endpoint  -> disjoint-mixed-star-projective doc
    no-double-coll. -> coincident-support-star-reverse + radical-star docs
    two-double-endpoint -> coincident-support-star-reverse doc

one staying P5 consumer imports a moving module:
    verify_p5_h31_two_rank_two_spoke_mixed_star_component_generic_obstruction
        imports verify_p4_two_rank_two_spoke_mixed_star_component
        (repaired via expose_claim_package)

one staying shared script is migration-aware by design:
    verify_p4_common_singleton_component resolves the moved
    two-rank-two-spoke component verifier through
    catalog/moved-paths.json (no repair needed; verified)
```

Clean-subprocess acceptance (fresh interpreter, only the repo root on
`sys.path`): all 10 repaired staying root consumers import cleanly;
all four already-migrated component verifiers replay from their
packages with repointed radical-star constants; the h31 spoke bare
import resolves through `expose_claim_package`.  No one-off
`sys.path` shim was added; the single new bare-name exposure goes
through `expose_claim_package`.

### Already-migrated cross-spine dependencies exercised (stable)

| dependency | migrated in | Stage 6 interaction |
|---|---|---|
| `claims/p4/classifications/triangle-211/mixed-center-star-211-complete` | Stage 5 | navigation cross-link only (not moved again) |
| `claims/p4/classifications/triangle-211/split-center-mixed-star-211` | Stage 5 | navigation cross-link only |
| `claims/p4/classifications/triangle-211/unequal-endpoint-inward-star-211-complete` | Stage 5 | links the moved unequal-endpoint component doc (re-anchored) |
| `claims/p4/classifications/triangle-211/triple-kernel-rank-one-triangle` | Stage 5 | hashed by the moved two-double-endpoint verifier (REPO_ROOT constant) |
| `claims/p4/classifications/triangle-211/cyclic-rank-one-triangle-support` | Stage 5 | links the moved disjoint-mixed-star-projective doc (re-anchored) |
| `claims/p4/components/disjoint-mixed-star` | Stage 3 | linked by both moved disjoint-mixed-star classifications; its verifier hashes the moved radical-star doc |
| `claims/p4/components/{all-rank-one-triangle, mixed-orientation, six-dimensional}` | Stage 3/4 | each hashes the moved radical-star doc (REPO_ROOT constants repointed, all replay rc=0) |

## Link and command rewrites

- Rewriter first pass: **90 links** re-anchored and **58 replay
  commands** repointed (plain `python` and `uv run --with sympy
  python` forms) across 35 files, **0 ambiguities**.  Second pass:
  **0 links, 0 commands, 0 touched files, 0 ambiguities**
  (idempotent fixed point).
- **Zero manual replay-fence repairs.**  The shared replay-command
  grammar handled every command form in this batch, including the
  continuation-line `python \` + filename pair in the radical-star
  doc; no new syntax form was discovered.
- Python path repairs: 5 moved scripts switched from `ROOT=parent` to
  the centralized bootstrap (siblings via `HERE`, root-resident docs
  and `tmp/` via `REPO_ROOT`); 14 staying consumers repointed path
  constants/hash tuples (all-pair-rank reducer ×8 docs, component21
  verify+audit hash tables, h22 coincident-support audit/derive,
  h31 coincident-support, two h22 spoke consumers, high-coordinate
  frontier, four component verifiers); 1 staying P5 consumer gained
  `expose_claim_package` for its bare import.
- No theorem prose changed (verified by diff: only link targets,
  fenced command paths, and path constants).

## Replay results

All 17 packages replayed post-migration from the new locations
(working directory: repository root; outputs in `tmp/`, untracked).
This is a **manual Windows replay** (no GitHub Actions replay of
Singular; CI carries sympy-only checks).

| class | packages | verifier | audit | external binary |
|---|---|---|---|---|
| sympy-only | 15 packages | verified/pass (≤3.4 s each) | audited (≤1.3 s each) | none |
| one-double-endpoint-star-111 | 1 | verified (2.4 s) | audited (0.7 s) | **Singular** via WSL |
| no-double-endpoint-star-1110-collision | 1 | verified (6.3 s) | audited (7.2 s post-move) | **Singular** via WSL |

All 34 replay runs returned rc=0 with positive verdicts.  Singular
4.3.2 executed via WSL (`wsl.exe --exec /usr/bin/Singular -q`);
native Windows `Singular` is not on PATH.  No verifier was claimed
without execution.  No generated solver artifacts committed
(hygiene check [2]).

Preflight note: the same 34 scripts also ran rc=0 from the root
**before** the moves (≤6.3 s each), establishing the pre/post
replayability baseline for this batch.

## Ledger

- **0 entries repointed.**  The theorem ledger is a curated partial
  index centered on the P5 H22/H31 claims; no entry referenced any of
  the 51 moving files.  No ledger entry was fabricated; global ledger
  status remains **UNRESOLVED**.
- **8 committed-blob hash fields refreshed** for docs whose content
  changed during reference rewrites: `README.md` (×3 entries),
  `P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md`,
  `P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`,
  `P5_H31_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`,
  `P5_H31_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`,
  `P4_RANK_TWO_RELATION_STAR_OBSTRUCTION_WITHDRAWN_OVERSTRONG.md`.
  All 85 ledger hashes validate.

## Stale-reference enforcement

Enforced old paths increased from 114 to **165** (114 + 51 = 165 ✓;
3 full-path, 162 root-to-package).  Zero stale references outside
provenance, checked across all supported replay-command forms
(`python`, `python3`, `wsl … python`, `uv run … python`, and
continuation-line `python \` + filename).

## Machinery behavior

- **Executor summary recomputation worked without rebuilding** at 51
  files — the exact acceptance numbers above were produced by
  `finalize_execution` inside the transaction; `check_hygiene.py
  [11]` agrees.
- **Rollback was NOT invoked** — no mid-batch failure.
- **Shared replay-command grammar remained effective** — zero manual
  fence repairs across 58 rewritten commands and all stale scans.
- **No new migration-tool defect** in the executor, contract
  validator, summary recomputation, rewriter, or stale scanner.
- **No migration-tool code change** in this stage: existing machinery
  handled the 51-file batch unmodified.  No new regression tests were
  required; the suite stays at 107.

## Validation floor (Step 33)

On the final head: `check_hygiene.py` all green (1,698 files compile;
all 771 markdown files' local links resolve; ledger 85/85 hashes;
provenance 165/165; stale paths 165 enforced, none present;
portability clean; 5 fast verifiers pass).  107 migration-tool tests
OK.  `test_fourteen_vertex_cycle_cover_lattice.py` OK (14 tests).
Rewriter idempotent (second pass 0/0/0).  No generated solver
artifacts committed.  Root: 2,258 → 2,207.

CI bookkeeping (per the established convention): the substantive-head
workflow dispatch [31210469788](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31210469788)
passed (**success**) on the exact substantive head
`5a3cb2cee8636caebfaec1d8e5f0ef60a7cf4856`; the subsequent report-fill
bookkeeping commit carries its own PR CI run, recorded on the PR.
The final PR-triggered workflow must pass hygiene, migration tests,
cycle-cover tests, and the rewriter fixed-point check on the
resulting PR head.

## Selected / excluded / deferred / shared / already migrated elsewhere

- **Selected:** 17 complete star packages (51 files), listed above.
- **Excluded:** `P4_RANK_TWO_RELATION_STAR_OBSTRUCTION_WITHDRAWN_OVERSTRONG`
  (+ verify/audit) — withdrawn historical artifact; classifier
  proposes `claims/legacy/` (high confidence); belongs to a dedicated
  legacy batch.
- **Deferred:** the remaining 83 `p4/classifications` records, the
  rest of `p4/boundaries`, global classification machinery, atlases,
  working notes — Stage 7+.
- **Shared (staying):** directed-zero-divisor machinery,
  common-singleton component verifier (migration-aware resolver),
  all-pair-rank exceptional-graph reducer.
- **Already migrated elsewhere (not touched):** Stage 5
  triangle-211 star packages (mixed-center, split-center,
  unequal-endpoint-complete); Stage 3/4 component packages.

## Stop condition

This PR does not begin another classification family and does not
move the remaining `p4/classifications` bucket (83 records stay
pending) or P5.  Stage 6 proves that the migration workflow can carry
a substantially larger star-family classification batch (51 files vs
43, 17 packages vs 14, 14 repaired staying consumers, 7 cross-spine
dependencies) without losing ownership boundaries, provenance, or
reproducibility.

> No theorem claim, assumption, scope, provenance status, or
> global-resolution status changed as a result of this migration. The
> global Krenn–Gu conjecture remains **UNRESOLVED**.
