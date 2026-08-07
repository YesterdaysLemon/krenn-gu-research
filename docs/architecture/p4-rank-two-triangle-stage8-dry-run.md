# Stage 8 dry-run: P4 resonant / nonresonant rank-two-triangle live spine

Generated before execution, from the tree at the Stage 8 starting
SHA `3f093da` (merged `main` including PR #35 / Stage 7) plus the
Stage 7 report erratum commit `eeb2025` (bookkeeping only), branch
`layout-migration-stage8-p4-rank-two-triangle`.

Approval artifact: `catalog/batches/p4-rank-two-triangle-stage8.json`
(produced after this report).  Approval:

```text
YesterdaysLemon (repository owner), Stage 8 P4 resonant/nonresonant rank-two triangle migration instruction
```

applies only to the exact reviewed **live** mapping recorded in that
batch file.  It does not authorize withdrawn legacy claims, all
remaining triangle claims, all P4 boundaries, all P4 classifications,
P5, arbitrary-order claims, or future batches.

Stage 8's strategic purpose is not throughput: it tests whether the
research-library architecture can preserve a **live theorem chain**
while keeping nearby withdrawn / superseded historical attempts
visibly distinct without Git archaeology.

## Baseline (measured at `eeb2025`, before any Stage 8 change)

```text
starting main SHA (merged Stage 7)   3f093da (PR #35 merge commit)
stage-7 erratum commit               eeb2025
root entries                         2165
manifest moved                       207
proposed_high_confidence             361
review_required                      1447
unclassified                         348
remaining p4/classifications         60
remaining p4/boundaries              54
stale enforced                       207 (3 full-path, 204 root-to-package)
migration-tool tests                 112
ledger entries                       85
markdown files                       778
python files compiled                1698
```

## Scope and stop-condition verdict

**Batch: 11 live packages / 32 files** (4 classification packages =
11 files, 7 boundary packages = 21 files; preferred range 8–12
packages, 24–40 files — hit on both; hard maximum 50 not approached).

The family is the complete live resonant / nonresonant
rank-two-relation triangle chain.  Two explicit withdrawn neighbors
were inspected and are **deliberately left unmoved** at root with
their existing `claims/legacy/` proposals.

## Candidate review

### Nonresonant branch

| seed | classifier family | decision | rationale |
|---|---|---|---|
| P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION | p4/classifications | **include** | the root reduction of the whole chain; verifier present; **no independent audit** — the doc states the verifier is a tiny exact replay of the displayed symbolic proof, not a substitute; intentional documented state |
| P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION | p4/boundaries | **include** (stays boundary) | exact boundary theorem closing every proper bridge-support boundary of the cut reduction; complete triple; its status states the boundary role explicitly |
| P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION | p4/boundaries | **include** (stays boundary) | full-support `1+3` obstruction on the unresolved cut triangle; complete triple |
| P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION | p4/boundaries | **include** (stays boundary) | full-support `2+2` bridge obstruction; complete triple; combined with one-three it proves the nonresonant all-rank-two-relation triangle is empty |

### Resonant branch

| seed | classifier family | decision | rationale |
|---|---|---|---|
| P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION | p4/classifications | **include** | reduction of the sole stratum left after the nonresonant branch; splits into nonzero-holonomy and flat binary-cubic shapes; complete triple under the shortened stem `verify_p4_resonant_rank_two_triangle_affine_holonomy.py` |
| P4_RESONANT_NONZERO_ADDITIVE_HOLONOMY_OBSTRUCTION | p4/boundaries | **include** (stays boundary) | obstruction of the `delta != 0` branch; confines the frontier to the flat divisor; complete triple |
| P4_RESONANT_FLAT_FULL_KERNEL_COLLISION_CLASSIFICATION | p4/classifications | **include** | classification of every affine-ratio collision in the full-kernel-support flat triangle; complete triple under shortened stem |
| P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION | p4/classifications | **include** | projective partner-sheet classification over the genuine Borel-generic flat center; complete triple under shortened stem |
| P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION | p4/boundaries | **include** (stays boundary) | corrected-scope obstruction on the genuine Borel-generic chart; complete triple under shortened stem |
| P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION | p4/boundaries | **include** (stays boundary) | valid one-kernel-zero boundary theorem (its earlier overstrong "complete flat branch" scope is what was withdrawn); complete triple under shortened stem |

### Mixed bridge

| seed | classifier family | decision | rationale |
|---|---|---|---|
| P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION | p4/boundaries | **include** (stays boundary) | **corrected** exact theorem (status section says so explicitly); keeps kernel rows Borel-marked; complete triple |

### Historical / withdrawn neighbors (inspected, NOT migrated)

| artifact | classifier state | decision |
|---|---|---|
| P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION_WITHDRAWN_OVERSTRONG (+ verify/audit) | proposed_high_confidence → `claims/legacy/` | **historical-withdrawn**, stays at root pending a dedicated legacy stage |
| P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION_WITHDRAWN_PENDING_BOREL_AUDIT (+ verify/audit) | proposed_high_confidence → `claims/legacy/` | **historical-withdrawn**, stays at root pending a dedicated legacy stage |

Both withdrawn records are untouched by the refinement (verified).

### Default exclusions honored

- `claims/p4/classifications/triangle-211/` — separate support/211
  classification spine (Stage 5); the corrected Borel classification
  `rank-two-relation-triangle-corrected` stays put as a cross-spine
  dependency.
- P5 consumers (`P5_ALTERNATIVE_STRATEGY_MAP` and the H22/H31
  frontier docs) — downstream; links re-anchored only.
- `verify_p4_all_pair_rank_exceptional_graph_reduction` — shared
  global machinery; its `RESOLUTION_PACKAGES` entry is repointed in
  Commit D.
- Other P4 triangle material (common-kernel/common-factor,
  marked-Delta2) — out of scope; Stage 8 approves none of it.

## Live versus withdrawn lineage (Stage 8 integrity deliverable)

| current live claim | lineage relationship | historical artifact |
|---|---|---|
| mixed/two-rank-two (live, corrected) | **supersedes** (`withdrawn_pending_audit`) | `P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION_WITHDRAWN_PENDING_BOREL_AUDIT` — withdrew the unmarked `GL_2` row change; the live theorem keeps kernel rows Borel-marked; the withdrawn doc names the live doc as its replacement |
| resonant/flat-generic-binary-cubic (live) | **corrected successor** (`withdrawn_overstrong` scope) | `P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION_WITHDRAWN_OVERSTRONG` — the withdrawn doc names this live theorem as the true full-support Borel chart |
| resonant/flat-kernel-zero-binary-cubic (live) | **valid scope preserved** (`withdrawn_overstrong` neighbor) | same withdrawn doc names this live theorem as the valid one-kernel-zero theorem; the live doc records that its earlier "complete flat branch" claim was overstrong |
| nonresonant/cut-reduction + one-three + two-two + degenerate-cut | **no predecessor** | none — first-generation exact claims |
| resonant/affine-holonomy-reduction + nonzero-additive-holonomy | **no predecessor** | none — first-generation exact claims |
| resonant/flat-full-kernel-collision + flat-projective-partner | **no predecessor** | none — first-generation exact claims |

Additional cross-spine lineage: the withdrawn-overstrong doc states
the complete Borel classification was recovered by
[`claims/p4/classifications/triangle-211/rank-two-relation-triangle-corrected/`](../../claims/p4/classifications/triangle-211/rank-two-relation-triangle-corrected/)
(Stage 5 package — stable, not moved).  Navigation in Commit E will
expose the whole lineage table without requiring Git archaeology.

## Dependency graph (reconstructed from theorem text)

```text
nonresonant/cut-reduction (reduction, audit-less)
    |
    +-- nonresonant/one-three (boundary, full-support 1+3)
    +-- nonresonant/two-two   (boundary, full-support 2+2)
    +-- nonresonant/degenerate-cut (boundary, proper supports)
    |       [the three together: complete nonresonant triangle empty]
    |
    v  (frontier confined to the resonant divisor)
resonant/affine-holonomy-reduction (reduction)
    |
    +-- resonant/nonzero-additive-holonomy (boundary, delta != 0)
    |       [frontier confined to Omega=0, delta=0]
    |
    v  (flat branch: compressed binary cubic)
    +-- resonant/flat-generic-binary-cubic (boundary, Borel-generic chart)
    +-- resonant/flat-projective-partner   (classification, partner sheets)
    +-- resonant/flat-kernel-zero-binary-cubic (boundary, one-kernel-zero)
    +-- resonant/flat-full-kernel-collision (classification, affine-ratio collisions)

mixed/two-rank-two (boundary; corrected; independent stratum of the
                    rank-two-relation triangle family)
```

Edge types: `reduction_to_case` (cut-reduction → its three boundary
cases; affine-holonomy → nonzero-holonomy and the flat subcases),
`boundary_case` (each obstruction closes one divisor/cut type),
`theorem_dependency` (docs cite upstream reductions by link),
`supersedes` / `withdrawn_predecessor` (the two lineage rows above),
`shared_utility` (all-pair-rank global reducer, staying),
`downstream_consumer` (P5 strategy map and H22/H31 docs, staying),
`already_migrated_dependency` (triangle-211 corrected classification,
Stage 5; radical-star star package, Stage 6).

**Intra-batch Python imports: none** (full regex scan of all 21
scripts).  **Member scripts carry zero path constants** (no `ROOT=`,
no doc references, no `tmp/` writes) — Commit D needs no bootstrap
repair inside the moved packages, a first for the migration.

## Shared and cross-spine dependencies (stay; repaired in Commit D)

```text
verify_p4_all_pair_rank_exceptional_graph_reduction.py
    (RESOLUTION_PACKAGES names the mixed obstacle doc — repoint)
claims/p4/classifications/star/radical-star/
    (inbound links to the flat binary-cubic docs — re-anchored)
claims/p4/classifications/triangle-211/rank-two-relation-triangle-corrected/
    (Stage 5; inbound from live+withdrawn docs — re-anchored)
claims/p4/components/embedded-p3/  (inbound links — re-anchored)
README.md, docs/LITERATURE_REVIEW_2026-07-30.md,
docs/research-notes.md, P5_ALTERNATIVE_STRATEGY_MAP.md,
P4_BOREL_GAUGE_CORRECTION.md, P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md
    (inbound links — re-anchored)
```

Inbound link census: **56 links across 12 staying files**.

## Mapping (exact, 32 moves)

| old path | new path |
|---|---|
| P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md | claims/p4/classifications/rank-two-triangle/nonresonant/cut-reduction/P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md |
| verify_p4_nonresonant_rank_two_triangle_cut_reduction.py | claims/p4/classifications/rank-two-triangle/nonresonant/cut-reduction/verify_p4_nonresonant_rank_two_triangle_cut_reduction.py |
| P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md | claims/p4/classifications/rank-two-triangle/resonant/affine-holonomy-reduction/P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md |
| verify_p4_resonant_rank_two_triangle_affine_holonomy.py | claims/p4/classifications/rank-two-triangle/resonant/affine-holonomy-reduction/verify_p4_resonant_rank_two_triangle_affine_holonomy.py |
| audit_p4_resonant_rank_two_triangle_affine_holonomy.py | claims/p4/classifications/rank-two-triangle/resonant/affine-holonomy-reduction/audit_p4_resonant_rank_two_triangle_affine_holonomy.py |
| P4_RESONANT_FLAT_FULL_KERNEL_COLLISION_CLASSIFICATION.md | claims/p4/classifications/rank-two-triangle/resonant/flat-full-kernel-collision/P4_RESONANT_FLAT_FULL_KERNEL_COLLISION_CLASSIFICATION.md |
| verify_p4_resonant_flat_full_kernel_collision.py | claims/p4/classifications/rank-two-triangle/resonant/flat-full-kernel-collision/verify_p4_resonant_flat_full_kernel_collision.py |
| audit_p4_resonant_flat_full_kernel_collision.py | claims/p4/classifications/rank-two-triangle/resonant/flat-full-kernel-collision/audit_p4_resonant_flat_full_kernel_collision.py |
| P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md | claims/p4/classifications/rank-two-triangle/resonant/flat-projective-partner/P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md |
| verify_p4_resonant_flat_projective_partner.py | claims/p4/classifications/rank-two-triangle/resonant/flat-projective-partner/verify_p4_resonant_flat_projective_partner.py |
| audit_p4_resonant_flat_projective_partner.py | claims/p4/classifications/rank-two-triangle/resonant/flat-projective-partner/audit_p4_resonant_flat_projective_partner.py |
| P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md | claims/p4/boundaries/rank-two-triangle/nonresonant/degenerate-cut/P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md |
| verify_p4_nonresonant_degenerate_cut_triangle_obstruction.py | claims/p4/boundaries/rank-two-triangle/nonresonant/degenerate-cut/verify_p4_nonresonant_degenerate_cut_triangle_obstruction.py |
| audit_p4_nonresonant_degenerate_cut_triangle_obstruction.py | claims/p4/boundaries/rank-two-triangle/nonresonant/degenerate-cut/audit_p4_nonresonant_degenerate_cut_triangle_obstruction.py |
| P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md | claims/p4/boundaries/rank-two-triangle/nonresonant/one-three/P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md |
| verify_p4_nonresonant_one_three_triangle_obstruction.py | claims/p4/boundaries/rank-two-triangle/nonresonant/one-three/verify_p4_nonresonant_one_three_triangle_obstruction.py |
| audit_p4_nonresonant_one_three_triangle_obstruction.py | claims/p4/boundaries/rank-two-triangle/nonresonant/one-three/audit_p4_nonresonant_one_three_triangle_obstruction.py |
| P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md | claims/p4/boundaries/rank-two-triangle/nonresonant/two-two/P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md |
| verify_p4_nonresonant_two_two_triangle_obstruction.py | claims/p4/boundaries/rank-two-triangle/nonresonant/two-two/verify_p4_nonresonant_two_two_triangle_obstruction.py |
| audit_p4_nonresonant_two_two_triangle_obstruction.py | claims/p4/boundaries/rank-two-triangle/nonresonant/two-two/audit_p4_nonresonant_two_two_triangle_obstruction.py |
| P4_RESONANT_NONZERO_ADDITIVE_HOLONOMY_OBSTRUCTION.md | claims/p4/boundaries/rank-two-triangle/resonant/nonzero-additive-holonomy/P4_RESONANT_NONZERO_ADDITIVE_HOLONOMY_OBSTRUCTION.md |
| verify_p4_resonant_nonzero_additive_holonomy_obstruction.py | claims/p4/boundaries/rank-two-triangle/resonant/nonzero-additive-holonomy/verify_p4_resonant_nonzero_additive_holonomy_obstruction.py |
| audit_p4_resonant_nonzero_additive_holonomy_obstruction.py | claims/p4/boundaries/rank-two-triangle/resonant/nonzero-additive-holonomy/audit_p4_resonant_nonzero_additive_holonomy_obstruction.py |
| P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md | claims/p4/boundaries/rank-two-triangle/resonant/flat-generic-binary-cubic/P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md |
| verify_p4_resonant_flat_generic_binary_cubic.py | claims/p4/boundaries/rank-two-triangle/resonant/flat-generic-binary-cubic/verify_p4_resonant_flat_generic_binary_cubic.py |
| audit_p4_resonant_flat_generic_binary_cubic.py | claims/p4/boundaries/rank-two-triangle/resonant/flat-generic-binary-cubic/audit_p4_resonant_flat_generic_binary_cubic.py |
| P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md | claims/p4/boundaries/rank-two-triangle/resonant/flat-kernel-zero-binary-cubic/P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md |
| verify_p4_resonant_flat_kernel_zero_binary_cubic.py | claims/p4/boundaries/rank-two-triangle/resonant/flat-kernel-zero-binary-cubic/verify_p4_resonant_flat_kernel_zero_binary_cubic.py |
| audit_p4_resonant_flat_kernel_zero_binary_cubic.py | claims/p4/boundaries/rank-two-triangle/resonant/flat-kernel-zero-binary-cubic/audit_p4_resonant_flat_kernel_zero_binary_cubic.py |
| P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md | claims/p4/boundaries/rank-two-triangle/mixed/two-rank-two/P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md |
| verify_p4_mixed_two_rank_two_triangle_obstruction.py | claims/p4/boundaries/rank-two-triangle/mixed/two-rank-two/verify_p4_mixed_two_rank_two_triangle_obstruction.py |
| audit_p4_mixed_two_rank_two_triangle_obstruction.py | claims/p4/boundaries/rank-two-triangle/mixed/two-rank-two/audit_p4_mixed_two_rank_two_triangle_obstruction.py |

## Classification refinement (durable, rebuild-safe)

For the 32 selected records, `catalog/layout-classification.json` —
the durable source — was edited:

```text
claim_family:  p4/boundaries (27 records) | p4/classifications (5)
           ->  p4/classifications/rank-two-triangle/<branch>/<slug>  (11 records)
               p4/boundaries/rank-two-triangle/<branch>/<slug>       (21 records)
proposed_path: -> matching nested claims/... destinations
evidence:      + "stage8_human_review: P4 rank-two-triangle live spine package"
```

**Stage 8 is the first stage with zero classifier-category
reassignments**: for all 11 packages, the flat classifier's
`p4/classifications` vs `p4/boundaries` bucketing agreed with the
human ownership review of each document's mathematical role
(reductions/classifications vs obstructions/boundary theorems).

`build_manifest.py` was then run normally.  Verified against the
committed manifest:

- **32 records changed**, all `review_required -> review_required`
  (no status promotion; confidence untouched);
- all **207 already-moved records byte-identical**, `executed_batch`
  preserved 207/207;
- counts unchanged (moved 207, proposed 361, review 1447,
  projected_root_if_moved_only 2165);
- no record outside the selection changed;
- **both withdrawn legacy records untouched**;
- **cross-category arithmetic**: 27 members originate in
  `p4/boundaries` and 5 in `p4/classifications`; the post-move
  family populations are therefore 60 − 5 = 55 remaining
  `p4/classifications` proposals and 54 − 27 = 27 remaining
  `p4/boundaries` proposals.

## Projections (expected, measured after execution)

| measure | projection |
|---|---|
| package count | 11 (4 classifications + 7 boundaries) |
| member count | 32 (11 + 21) |
| starting-status composition | 32 review_required; 0 high-confidence |
| source-family composition | 27 p4/boundaries + 5 p4/classifications |
| destination collisions | none |
| source/destination cycles | none |
| expected root-entry decrease | −32 (2,165 → 2,133; all sources are root files) |
| expected stale-path increase | +32 (207 → 239; all basename-preserving root→package) |
| manifest-state transitions | moved 207 → 239; review_required 1447 → 1415; proposed 361 unchanged; projected_root_if_moved_only 2165 → 2133 |
| ledger entries affected | 0 repointed (the one near-matching entry points at the withdrawn doc, which stays); hash refresh only for touched ledger docs |
| links/commands likely affected | inbound links ≈ 56 across 12 staying docs; 27 replay commands inside moving docs (incl. 7 in the cut reduction); plus README/handoff fences |

## Preflight replayability (all performed pre-freeze, rc=0, from repo root)

| script class | result |
|---|---|
| 11 verifiers (all sympy-only; no external solvers) | all rc=0; 10 of 11 ≤4.4 s; flat-generic-binary-cubic verifier 90.7 s (accepted; exact symbolic census) |
| 10 audits (all sympy-only) | all rc=0, ≤5.7 s each |

No Singular / msolve / SAT / z3 required by any selected package.
Manual Windows replay; outputs in `tmp/` (gitignored).  No generated
solver artifacts will be committed.

## Machinery note

Stage 8 requires **no machinery change**.  All replay forms in the
moving docs (single-line `uv run --with sympy python`, single-line
`python`, and the uv-continuation form in the cut-reduction doc) are
covered by the shared grammar as fixed in Stage 7.
