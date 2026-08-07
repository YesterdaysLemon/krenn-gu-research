# Layout migration report — Stage 8 (P4 resonant / nonresonant rank-two-triangle live spine)

Status: **the live resonant / nonresonant rank-two-relation triangle
chain is migrated, and the live-versus-withdrawn lineage survived the
move.**  Eleven live packages — four classification packages (the two
reductions and the two flat classifications) plus seven boundary
obstruction packages across the nonresonant, resonant, and mixed
branches — moved from the repository root into
`claims/p4/classifications/rank-two-triangle/` and
`claims/p4/boundaries/rank-two-triangle/`.  Stage 8's strategic
purpose was not throughput: it tested whether the research-library
architecture can preserve a live theorem chain while keeping nearby
withdrawn / superseded historical attempts visibly distinct without
Git archaeology.  The answer is yes.

> No theorem claim, assumption, scope, proof status, provenance
> status, or global-resolution status changed as a result of this
> migration. Withdrawn and superseded artifacts remain explicitly
> historical. The global Krenn–Gu conjecture remains UNRESOLVED.

## Provenance anchors

- Starting merged main SHA: `3f093da` (PR #35 / Stage 7 merge
  commit).  Stage 7 verified present before any Stage 8 work (12
  pair-geometry packages, `p4-pair-geometry-stage7.json`, dry-run,
  report, uv-continuation grammar, fixed-point CI step).
- Stage 7 report erratum commit: `eeb2025` (documentation only;
  corrects the transposed verifier/audit replay counts and the
  exhaustion replay wording; the frozen batch and dry-run are left
  immutable and the erratum supersedes the older wording).
- Branch: `layout-migration-stage8-p4-rank-two-triangle`.
- Commits: A `3e5119e` (classification refinement + dry-run),
  B `341d457` (frozen batch), C `855e392` (pure git-mv),
  D `362f5e0` (mechanical repairs), E (navigation, ledger hashes,
  this report).
- Batch: `p4-rank-two-triangle-stage8`, artifact
  `catalog/batches/p4-rank-two-triangle-stage8.json`:
  - approved_by: "YesterdaysLemon (repository owner), Stage 8 P4
    resonant/nonresonant rank-two triangle migration instruction";
  - approved_at: 2026-08-07;
  - base_sha: `3e5119e` (Stage 8 commit A);
  - informational manifest_sha256
    `98fbe027c39ed85805e97ebacb1854bec075f7f31837388d6fa4c2b0fbf2d78b`;
  - **mandatory** canonical mapping_sha256:
    `e628b126377820690f9c6fc46197b1f52798b302c4146a6676f3e5bf185c7762`;
  - member_count: **32**.
- Packages (11): classifications — nonresonant/cut-reduction,
  resonant/affine-holonomy-reduction,
  resonant/flat-full-kernel-collision,
  resonant/flat-projective-partner; boundaries —
  nonresonant/degenerate-cut, nonresonant/one-three,
  nonresonant/two-two, resonant/nonzero-additive-holonomy,
  resonant/flat-generic-binary-cubic,
  resonant/flat-kernel-zero-binary-cubic, mixed/two-rank-two.
- Pure-move commit: `855e392`; R100 count: **32 / 32** (measured
  against the direct parent).

## Live versus withdrawn lineage

This is Stage 8's headline deliverable.  Every selected live claim's
lineage was determined from the documents' own status sections:

| current live claim | lineage relationship | historical artifact |
|---|---|---|
| `boundaries/rank-two-triangle/mixed/two-rank-two` | **supersedes** (`withdrawn_pending_audit`) | `P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION_WITHDRAWN_PENDING_BOREL_AUDIT` (+ verify/audit) — withdrew the unmarked `GL_2` row change; the live theorem keeps kernel rows Borel-marked; the withdrawn doc names the live doc as its replacement |
| `boundaries/rank-two-triangle/resonant/flat-generic-binary-cubic` | **corrected successor** (`withdrawn_overstrong` scope) | `P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION_WITHDRAWN_OVERSTRONG` (+ verify/audit) — the withdrawn doc names this live theorem as the true full-support Borel chart |
| `boundaries/rank-two-triangle/resonant/flat-kernel-zero-binary-cubic` | **valid scope preserved** (`withdrawn_overstrong` neighbor) | same withdrawn doc names this live theorem as the valid one-kernel-zero theorem; the live doc records that its earlier "complete flat branch" scope was overstrong |
| all other Stage 8 packages | **no predecessor** | none — first-generation exact claims |

Cross-spine lineage: the withdrawn-overstrong doc states the complete
Borel classification was recovered by the Stage 5 package
`claims/p4/classifications/triangle-211/rank-two-relation-triangle-corrected/`
(stable; not moved).

**Both withdrawn artifacts were deliberately left unmoved** at the
repository root with their existing high-confidence `claims/legacy/`
proposals (classifier state `proposed_high_confidence` / family
`legacy`), untouched by the classification refinement (verified
record-for-record).  They were not deleted, not moved into the live
packages, not silently replaced, and not rehabilitated.  The
navigation READMEs expose the full lineage table so a reader can
distinguish live results from historical failed variants without Git
archaeology.  Withdrawn evidence was never substituted for live
verification: all 21 live scripts were replayed independently.

## Classification/boundary composition and records refined

- **0 high-confidence members.**  Every selected record was
  `review_required` (21 medium docs/scripts, 11 low-confidence
  scripts).  No confidence field was promoted and no status was
  silently upgraded.
- **32 selected records** refined in
  `catalog/layout-classification.json` (the durable source), then the
  manifest regenerated through the normal `build_manifest.py`
  machinery.  Verified against the committed manifest: exactly 32
  pending records changed destination/family, all 207 already-moved
  records byte-identical with `executed_batch` preserved 207/207,
  counts unchanged before execution, no unrelated record touched,
  both withdrawn legacy records untouched.
- **Stage 8 is the first stage with zero claim-document /
  package-category reassignments.**  At the claim-document level, the
  flat classifier's `p4/classifications` vs `p4/boundaries`
  bucketing agreed with the human ownership review for every package:
  the four classification claim documents were already
  coarse-classified `p4/classifications`, and the seven obstruction
  claim documents were already coarse-classified `p4/boundaries`.
  Six `claim_script` records were refined from the rough
  `p4/boundaries` bucket into the classification packages owned by
  their classification documents (the affine-holonomy,
  full-kernel-collision, and projective-partner verify/audit pairs);
  this is consistent with the recorded source-family arithmetic:
  27 boundaries-source records = 21 boundary-triple records + 6
  script records refined into classification packages, and 5
  classifications-source records = 4 classification documents + the
  nonresonant cut-reduction verifier.  No theorem was moved into
  `boundaries` merely because the old classifier put it there, and no
  true obstruction was moved into `classifications` for symmetry.
  The frozen batch rationale's "zero reassignments" wording is
  package-level shorthand for this claim-document statement; the
  frozen batch artifact itself is unchanged.

## Root-count accounting (observed)

| Moment | Root entries |
|---|---|
| 1. original pre-migration root (`pre-layout-migration-v1`) | **2,366** |
| 2. Stage 8 starting `main` (`3f093da`) | **2,165** |
| 3. immediately after pure Stage 8 moves (`855e392`) | **2,133** |
| 4. final PR head | **2,133** |

Manifest tallies (observed, produced by the executor itself):

```text
stage8_files_moved                    32
stage8_root_entries_removed           32
cumulative_moved_entries              239
stale_paths_enforced (after)          239   (207 before + 32 = 239 ✓)
remaining_proposed_high_confidence    361   (unchanged; no high members)
remaining_review_required             1415  (1447 - 32)
remaining_unclassified                348
remaining_p4_classifications_proposals 55   (60 - 5 classifications-source members)
remaining_p4_boundaries_proposals      27   (54 - 27 boundaries-source members)
```

The per-source-family arithmetic is reported honestly: 27 members
originated in `p4/boundaries` and 5 in `p4/classifications`; naive
total subtraction against one bucket would be wrong.  Every selected
member started at root, so the root decrease equals the member count
(32) — verified.

## Executor acceptance test — mixed source categories

Immediately after the executor ran (before any rebuild), the manifest
already carried:

```text
counts.moved                        207 + 32 = 239      ✓
counts.proposed_high_confidence    361 (unchanged)      ✓
counts.review_required             1447 - 32 = 1415     ✓
projected_root_if_moved_only       2165 - 32 = 2133     ✓
```

All 32 members started `review_required`, so the entire decrease
lands there; the breakdown by starting status (32 review_required)
and by original classifier family (27 boundaries / 5 classifications)
was recorded immediately after execution.  No manual rebuild was
needed at any point.

## Dependency graph

Reconstructed from theorem text, verifiers, and references:

```text
nonresonant/cut-reduction (reduction; audit-less by documented design)
    |
    +-- boundaries: one-three, two-two, degenerate-cut
    |       [the three together: complete nonresonant triangle empty]
    v  (frontier confined to the resonant divisor)
resonant/affine-holonomy-reduction (reduction)
    |
    +-- boundaries: nonzero-additive-holonomy (delta != 0 branch)
    |       [frontier confined to Omega=0, delta=0]
    v  (flat branch: compressed binary cubic)
    +-- classifications: flat-full-kernel-collision,
    |                    flat-projective-partner
    +-- boundaries: flat-generic-binary-cubic,
                    flat-kernel-zero-binary-cubic

mixed/two-rank-two (corrected; independent (2,2,1) stratum)
```

Edge types: `reduction_to_case` (cut-reduction → its three boundary
cases; affine-holonomy → the nonzero-holonomy and flat subcases),
`boundary_case` (each obstruction closes one divisor/cut type),
`theorem_dependency` (docs cite upstream reductions by link),
`supersedes` / `withdrawn_predecessor` (the lineage table above),
`shared_utility` (all-pair-rank global reducer, staying),
`downstream_consumer` (P5 strategy map, staying),
`already_migrated_dependency` (triangle-211 corrected classification
Stage 5; radical-star Stage 6; embedded-p3 and crossed-211 support
packages).

- **Intra-batch Python imports: none** (full regex scan of all 21
  scripts).
- **Member scripts carry zero path constants** (no `ROOT=`, no doc
  references, no `tmp/` writes) — Commit D needed no bootstrap repair
  inside the moved packages, a first for the migration.
- **Cross-spine P4 dependencies (stable):** triangle-211 corrected
  classification (inbound links re-anchored), radical-star (inbound
  links), embedded-p3 (inbound links); none moved.
- **Shared root (stay):** `verify_p4_all_pair_rank_exceptional_graph_
  reduction` — its `RESOLUTION_PACKAGES` entry for the mixed obstacle
  doc repointed; import verified.  No P5 consumer imports a moved
  module by bare name (no `expose_claim_package` needed this stage).

## Link and command rewrites

- Rewriter first pass: **106 links** re-anchored and **27 replay
  commands** repointed across 23 files, **0 ambiguities** (including
  the uv-continuation form in the cut-reduction doc, handled by the
  Stage 7 grammar fix).  Second pass: **0 links, 0 commands, 0
  touched files, 0 ambiguities** (idempotent fixed point).
- Python path repairs: exactly **1** staying consumer
  (`verify_p4_all_pair_rank_exceptional_graph_reduction`).
- No theorem prose changed (verified by diff: only link targets,
  fenced command paths, and the one path constant).  The withdrawn
  documents' only changes were link re-anchoring to their live
  successors — their withdrawn status text is untouched.

## Replay results

All 21 live scripts replayed post-migration from the new locations
(working directory: repository root; outputs in `tmp/`, untracked).
This is a **native Windows replay** (no external solvers required by
any selected package; no GitHub Actions replay of anything — CI is
sympy-only checks).

| class | scripts | result | runtime |
|---|---|---|---|
| sympy-only verifiers | 11 | all rc=0 | 10 of 11 ≤4.5 s; flat-generic-binary-cubic 95.0 s (exact symbolic census; accepted) |
| sympy-only audits | 10 | all rc=0 | ≤5.7 s each |

Preflight note: the same 21 scripts ran rc=0 from the root before the
moves (≤4.4 s except flat-generic 90.7 s), establishing the pre/post
replayability baseline.  No verifier or audit was claimed without
execution; no generated solver artifacts were committed.

## Ledger

- **0 entries repointed.**  The theorem ledger is a curated partial
  index; the only near-matching entry points at the withdrawn mixed
  triangle doc (which stays at root), and per policy a withdrawn
  ledger entry is not silently redirected to a corrected live
  theorem.  No ledger entry was fabricated; global ledger status
  remains **UNRESOLVED**.
- **6 committed-blob hash fields refreshed** for docs whose content
  changed during reference rewrites: `README.md` (×3 entries),
  `P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md`, and the two
  withdrawn docs (`P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION_WITHDRAWN_
  OVERSTRONG.md`, `P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION_
  WITHDRAWN_PENDING_BOREL_AUDIT.md`) whose successor links were
  re-anchored.  All 85 ledger hashes validate.

## Stale-reference enforcement

Enforced old paths increased from 207 to **239** (207 + 32 = 239 ✓;
3 full-path, 236 root-to-package).  Zero stale references outside
provenance, checked across all supported replay-command forms
(`python`, `python3`, `wsl … python`, `uv run … python`,
continuation-line `python \` + filename, and the uv-continuation
form).  Final CI proves committed-tree rewriter closure.

## Machinery behavior

Stage 8 required **no migration-machinery change** — the preferred
outcome for the executor, rewriter, and grammar.  All replay forms in
the moving docs were covered by the shared grammar as fixed in
Stage 7.

The first substantive-head dispatch did, however, expose one genuine
**validation-workflow** defect: the local floor can appear green
while a newly created, nonignored, not-yet-staged file is completely
outside every tracked-file check (Markdown links, stale references,
rewriter coverage), because `check_hygiene.py` and the rewriter
enumerate through plain `git ls-files`.  Fixed narrowly by a
candidate-index completeness precondition: authoritative local
validation now requires an index-complete candidate tree (no
nonignored untracked files, no unstaged tracked changes; staged
changes allowed).  The intended workflow is `git add -A` before the
floor; CI's clean checkout satisfies the invariant automatically.
Five focused regression tests in a synthetic Git repository cover
the precondition; migration-tool suite 112 → 117.  No replay-command
grammar, executor, or batch-contract change was made.

## Validation floor (Step 34)

On the final head: `check_hygiene.py` all green (1,698 files compile;
all markdown local links resolve; ledger 85/85 hashes; provenance
239/239; stale paths 239 enforced, none present; portability clean;
5 fast verifiers pass; candidate-index completeness precondition
green).  117 migration-tool tests OK.
`test_fourteen_vertex_cycle_cover_lattice.py` OK (14 tests).
Rewriter idempotent (second pass 0/0/0).  No generated solver
artifacts committed.  Root: 2,165 → 2,133.

The 21 scientific verifier/audit replays are **not repeated** for the
validation-workflow hardening: no claim document, verifier, audit, or
path content changed in the final integrity pass (only
`check_hygiene.py`, the migration-tool tests, and report prose), so
the existing replay evidence above remains valid and is preserved.

CI bookkeeping (per the established convention): the substantive-head
`workflow_dispatch` run ID and the exact substantive-head SHA are
recorded here, and the final PR-triggered workflow must pass hygiene,
migration tests, 14-vertex tests, and the rewriter fixed-point check
on the resulting PR head.

- First dispatch [31219014091](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31219014091)
  on `011db9f999cf74904e22c7d22992db7914321707` **failed**: the
  classifications README's companion link used one too many parent
  segments and resolved to a nonexistent path.  The local floor had
  passed because the link check counts HEAD-tracked markdown and the
  new READMEs were not yet committed at that moment.
- Navigation fix commit `3fa86eb` corrected the link depth; the
  re-run [31219192731](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31219192731)
  passed (**success**) on the corrected substantive head
  `3fa86ebb251a76be67b039144a4456437e92d3ac`, which is the true
  substantive head.  No migration machinery, theorem claim, or batch
  mapping changed as a result.

## Selected / excluded / deferred / shared / historical

- **Selected:** 11 live rank-two-triangle packages (32 files), listed
  above.
- **Historical-withdrawn (inspected, left unmoved):** the overstrong
  resonant flat classification and the mixed triangle pending Borel
  audit, each with verify/audit companions; both retain their
  `claims/legacy/` proposals.
- **Excluded:** global pair-rank machinery, shared machinery
  (directed-zero-divisor, common-singleton), P5 consumers, legacy
  artifacts, arbitrary-order claims.
- **Deferred:** common-kernel/common-factor geometry, marked-Delta2 /
  q4_211 boundary interface, remaining P4 boundaries, legacy
  evacuation — Stage 8 approves none of them.
- **Already migrated elsewhere (not touched):** Stages 3–7 component
  packages and the triangle-211 / star / pair-geometry spines.

## Stop condition

This PR does not begin the common-kernel/common-factor population,
does not migrate marked-Delta2, does not evacuate legacy, and does
not start P5.  Stage 8 proves that the migration system can preserve
not only where mathematical claims live, but also which claims
survived scrutiny and which did not.

> No theorem claim, assumption, scope, proof status, provenance
> status, or global-resolution status changed as a result of this
> migration. Withdrawn and superseded artifacts remain explicitly
> historical. The global Krenn–Gu conjecture remains UNRESOLVED.
