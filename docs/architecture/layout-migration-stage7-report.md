# Layout migration report — Stage 7 (P4 pair-geometry classification/boundary spine)

Status: **the third P4 classification spine is migrated, and the
classification/boundary distinction survived its first cross-category
batch.**  Twelve pair-geometry packages — ten classification packages
(including the four-document pure-rank-two cluster and the
document-only lower-pair exhaustion corollary) plus two genuine
boundary-inclusion packages — moved from the repository root into
`claims/p4/classifications/pair-geometry/` and
`claims/p4/boundaries/pair-geometry/`.  Stage 7 tested dependency and
ownership complexity rather than raw file count, and the existing
machinery carried it with one narrow grammar fix.

> No theorem claim, assumption, scope, proof status, provenance
> status, or global-resolution status changed as a result of this
> migration. The global Krenn–Gu conjecture remains **UNRESOLVED**.

## Provenance anchors

- Starting main SHA: `22b674e` (merged main including PR #34 / Stage 6).
  Stage 6 verified present before any Stage 7 work (17 star packages,
  `p4-star-stage6.json` batch, dry-run, report, rewriter fixed-point
  CI step).
- Branch: `layout-migration-stage7-p4-pair-geometry`.
- Machinery fix: `8e36cc5` — shared replay grammar gained the
  uv-wrapper continuation form (`uv run --with sympy \` + next-line
  `python script.py`); 5 regression tests; suite 107 → 112.  This is
  the only migration-tool change in the stage.
- Commits: A `51fbc33` (classification refinement + dry-run),
  B `fd7e2fa` (frozen batch), C `8033c0f` (pure git-mv),
  D `ac27029` (mechanical repairs), E (navigation, ledger hashes,
  this report).
- Batch: `p4-pair-geometry-stage7`, artifact
  `catalog/batches/p4-pair-geometry-stage7.json`:
  - approved_by: "YesterdaysLemon (repository owner), Stage 7 P4
    pair-geometry classification/boundary migration instruction";
  - approved_at: 2026-08-07;
  - base_sha: `51fbc33` (Stage 7 commit A);
  - informational manifest_sha256
    `39ebb68f0b52d6501447e2fe06f0348f54fda656c217d161226a7818c3c32e85`;
  - **mandatory** canonical mapping_sha256:
    `dbe3558f58f446fd6f6f6acb2a6d623219c351071bdac1b802aeb0f40d499ead`;
  - member_count: **42**.
- Packages (12): decomposable-rank-two-family,
  decomposable-restriction-rank-drop, disjoint-secant-lower-pair,
  full-support-tangent-pair, lower-pair-rank-exhaustion,
  overlapping-secant-lower-pair, pure-rank-two,
  rank-one-pair-obstruction, rank-two-pair-kernel-geometry,
  tangent-rank-two-pair-purity (classifications); support-one-secant,
  support-two-tangent-flag (boundaries).
- Pure-move commit: `8033c0f`; R100 count: **42 / 42**.

## Classification/boundary composition and records refined

- **0 high-confidence members.**  Every selected record was
  `review_required` (30 medium docs/scripts, 12 low-confidence
  scripts).  No confidence field was promoted and no status was
  silently upgraded — the batch is an ownership/destination decision,
  recorded by approval.
- **42 selected records** refined in
  `catalog/layout-classification.json` (the durable source), then the
  manifest regenerated through the normal `build_manifest.py`
  machinery.  Verified against the committed manifest: exactly 42
  pending records changed destination/family, all 165 already-moved
  records byte-identical with `executed_batch` preserved 165/165,
  counts unchanged before execution, no unrelated record touched.
- **Cross-category reassignments (11 records, evidence-recorded):**
  the three records each of rank-one-pair-obstruction,
  decomposable-rank-two-family, and decomposable-restriction-rank-drop,
  plus the two rank-two-pair-kernel-geometry records, moved from the
  classifier's `p4/boundaries` bucket to pair-geometry
  classifications.  Each document's status section states it is a
  structural component/rank theorem (closing pair-image ranks,
  constructing the rank-two family, proving the rank-drop bound), not
  a boundary inclusion; the reassignment marker in each record's
  evidence records the decision.  Conversely the two genuine boundary
  inclusions (support-one-secant, support-two-tangent-flag) **stayed
  boundary-owned** under `claims/p4/boundaries/pair-geometry/` — the
  distinction is preserved by directory, not filename.

## Root-count accounting (observed)

| Moment | Root entries |
|---|---|
| 1. original pre-migration root (`pre-layout-migration-v1`) | **2,366** |
| 2. Stage 7 starting `main` (`22b674e`) | **2,207** |
| 3. immediately after pure Stage 7 moves (`8033c0f`) | **2,165** |
| 4. final PR head | **2,165** |

Manifest tallies (observed, produced by the executor itself):

```text
stage7_files_moved                    42
stage7_root_entries_removed           42
cumulative_moved_entries              207
stale_paths_enforced (after)          207   (165 before + 42 = 207 ✓)
remaining_proposed_high_confidence    361   (unchanged; no high members)
remaining_review_required             1447  (1489 - 42)
remaining_unclassified                348
remaining_p4_classifications_proposals 60   (83 - 23 classifications-source members)
remaining_p4_boundaries_proposals      54   (73 - 19 boundaries-source members)
```

The per-source-family arithmetic is reported honestly: 19 members
originated in `p4/boundaries` and 23 in `p4/classifications`; naive
total subtraction against either bucket would be wrong.

## Executor acceptance test — mixed source categories

Immediately after the executor ran (before any rebuild), the manifest
already carried:

```text
counts.moved                        165 + 42 = 207      ✓
counts.proposed_high_confidence    361 (unchanged)      ✓
counts.review_required             1489 - 42 = 1447     ✓
projected_root_if_moved_only       2207 - 42 = 2165     ✓
```

All 42 members started `review_required`, so the entire decrease lands
there; the breakdown by starting status and by original classifier
family was recorded immediately after execution (19 boundaries / 23
classifications).  No manual rebuild was needed at any point.

## Pure-rank-two cluster — final ownership resolution

Outcome A: **one mathematical package**.  The four documents form one
connected component narrative (canonical theorem → chart closure →
toric boundary fan → Segre slice reduction of the boundary orbits).
Each subclaim keeps its own verifier + audit with independent
implementations, so provenance stays per-executable.  The toric
boundary is boundary-flavored but is owned by this component's
geometry, so it sits in the package's `boundaries/` subpackage
following the Stage 1 pilot precedent.  The existing metadata model
(`claim_package` / `proof_variant: canonical` / `subpackage:
boundaries`) expressed everything; **no metadata-model extension was
needed and no regression test was required for it**.

The lower-pair exhaustion corollary is a **document-only package**:
its stated replay is the union of the eight sibling pair-geometry
scripts (all in this batch), and no dedicated verifier/audit exists.
The rank-two-pair-kernel-geometry package likewise has no independent
audit — its document states the verifier is a tiny exact replay of the
completed symbolic proof.  Both are intentional documented states,
not oversights.

## Dependency chain

- **Intra-batch Python imports: none** (verified by full regex scan
  of all 27 scripts).
- Intra-batch doc cross-references (path constants, all repaired):
  pure-rank-two verifier → decomposable-family doc; chart-closure
  verifier → component theorem doc (sibling); Segre verifier → toric
  boundary doc (subpackage).
- **Cross-spine P4 dependencies (stable):**
  `claims/p4/components/six-dimensional` (identification target of
  overlapping secant + support-two flag), `claims/p4/components/
  diagonal-quadric` (linked by the pure-rank-two theorem and toric
  boundary docs), `claims/p4/classifications/star/no-double-endpoint-
  star-1110-collision` (hashes the moved lower-pair exhaustion doc —
  repointed, package untouched).
- **Shared root dependencies (stay):** the global pair-rank reduction
  (`verify_p4_all_pair_rank_exceptional_graph_reduction`, its
  `RESOLUTION_PACKAGES` list repointed), `verify_p4_common_singleton_
  component` (migration-aware resolver found the moved
  disjoint-secant/full-support-tangent verifiers with **no repair** —
  verified), `verify_p4_directed_zero_divisor_triangle_components`.
- **P5 downstream consumers repaired (staying):** 15 H22/H31/q5_311
  frontier scripts repointed doc path constants;
  `derive_p5_h31_toric_marked_fibre_elimination` gained
  `expose_claim_package` for its bare import of the moved Segre
  verifier; `verify_p4_common_active_binary_triangle_p_plus_q_
  boundary`'s `CLASSIFICATION_VERIFIERS` subprocess dispatch
  repointed to the six moved verifiers.

## Link and command rewrites

- Rewriter first pass: **103 links** re-anchored and **48 replay
  commands** repointed across 39 files, **0 ambiguities** — including
  the first-ever uv-continuation form, handled by the Stage 7 grammar
  fix without manual fence repair.  Second pass: **0 links, 0
  commands, 0 touched files, 0 ambiguities** (idempotent fixed
  point).
- Python path repairs: 12 moved scripts switched from `ROOT=parent`
  to the centralized bootstrap (`HERE` for package-local
  docs/verifiers, `REPO_ROOT` for root-resident docs and `tmp/`);
  25 staying consumers repointed path constants or dispatch tuples.
- No theorem prose changed (verified by diff: only link targets,
  fenced command paths, and path constants).

## Replay results

All 27 moved scripts replayed post-migration from the new locations
(working directory: repository root; outputs in `tmp/`, untracked).
This is a **native Windows replay** (no external solvers required by
any selected package; no GitHub Actions replay of anything — CI is
sympy-only checks).

| class | scripts | result | runtime |
|---|---|---|---|
| sympy-only verifiers | 13 | all rc=0 | ≤2.5 s each |
| sympy-only audits | 14 | all rc=0 | ≤3.9 s each |

Preflight note: the same 27 scripts ran rc=0 from the root before the
moves (≤3.8 s each), establishing the pre/post replayability
baseline.  No verifier or audit was claimed without execution.

**Honest limitation (pre-existing, not caused by Stage 7):** four
staying consumers — `verify_p4_common_active_binary_triangle_p_plus_q_
boundary` and three component20 candidates — `import z3`, which is not
installed in this environment (they fail identically on the
pre-Stage-7 tree).  For them the strongest available checks were
performed: all four compile, all repaired pair-geometry path
constants resolve to existing files, and the six moved-verifier
dispatch targets of `p_plus_q` exist.  Their z3-dependent runtime was
**not replayed**.

## Ledger

- **0 entries repointed.**  The theorem ledger is a curated partial
  index; no entry referenced any of the 42 moving files.  No ledger
  entry was fabricated; global ledger status remains **UNRESOLVED**.
- **8 committed-blob hash fields refreshed** for docs whose content
  changed during reference rewrites: `README.md` (×3 entries),
  `P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md`,
  `P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`,
  `P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md`,
  `P5_H31_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md`,
  `P5_H31_FULL_SUPPORT_TANGENT_COMPONENT_GENERIC_OBSTRUCTION.md`.
  All 85 ledger hashes validate.

## Stale-reference enforcement

Enforced old paths increased from 165 to **207** (165 + 42 = 207 ✓;
3 full-path, 204 root-to-package).  Zero stale references outside
provenance, checked across all supported replay-command forms
(`python`, `python3`, `wsl … python`, `uv run … python`,
continuation-line `python \` + filename, and the new uv-continuation
form).

## Machinery behavior

- **One genuine defect found and fixed** (commit `8e36cc5`): the
  shared replay grammar did not recognize the uv-wrapper continuation
  form (`uv run --with sympy \` + next-line `python script.py`), used
  by the kernel-geometry doc.  Stages 3–6 never hit it because no
  migrated doc used that form.  Fixed narrowly via
  `LAUNCHER_UV_CONTINUATION` in `replay_command.py` (shared by
  rewriter and stale scanner through `match_replay`), with 5
  regression tests; suite 107 → 112; full floor re-run green.
- Executor summary recomputation worked without rebuilding at mixed
  source categories; rollback was NOT invoked; no other migration-
  tool change.

## Validation floor (Step 31)

On the final head: `check_hygiene.py` all green (1,698 files compile;
all markdown local links resolve; ledger 85/85 hashes; provenance
207/207; stale paths 207 enforced, none present; portability clean;
5 fast verifiers pass).  112 migration-tool tests OK.
`test_fourteen_vertex_cycle_cover_lattice.py` OK (14 tests).
Rewriter idempotent (second pass 0/0/0).  No generated solver
artifacts committed.  Root: 2,207 → 2,165.

CI bookkeeping (per the established convention): the substantive-head
workflow dispatch [31215243165](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31215243165)
passed (**success**) on the exact substantive head
`79b89f0e43ca70db5f1e2eefa5cee60e91d031b7`; the subsequent report-fill
bookkeeping commit carries its own PR CI run, recorded on the PR.
The final PR-triggered workflow must pass hygiene, migration tests,
14-vertex tests, and the rewriter fixed-point check on the resulting
PR head.

## Selected / excluded / deferred / shared / already migrated elsewhere

- **Selected:** 12 pair-geometry packages (42 files), listed above.
- **Excluded:** global pair-rank machinery
  (`P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION`), shared machinery
  (directed-zero-divisor, common-singleton), P5 consumers, legacy
  artifacts.
- **Deferred:** `P4_MARKED_DELTA2_SLICE_CLASSIFICATION` and
  `P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION` (q4_211 marked
  boundary population), `P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION`
  (mixed-orientation family ownership).
- **Shared (staying):** the three machinery scripts above; root
  component docs referenced by moving verifiers.
- **Already migrated elsewhere (not touched):** Stages 3–6 component
  packages, triangle-211 and star classification spines.

## Stop condition

This PR does not begin another P4 family and does not move the
remaining `p4/classifications` (60 records) or `p4/boundaries` (54
records) populations, nor P5.  Stage 7 proves that the migration
workflow can represent and relocate a cross-category,
dependency-rich mathematical family with nontrivial internal
structure (multi-document cluster, document-only corollary,
audit-less structural theorem, boundary/classification split) without
losing ownership boundaries, provenance, or reproducibility.

> No theorem claim, assumption, scope, provenance status, or
> global-resolution status changed as a result of this migration. The
> global Krenn–Gu conjecture remains **UNRESOLVED**.
