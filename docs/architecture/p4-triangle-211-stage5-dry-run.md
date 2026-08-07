# Stage 5 dry-run: P4 triangle / 211 classification spine

Generated before execution, from the tree at the Stage 5 starting
SHA `6d4b43f` (merged `main` including PR #32), tagged
`stage5-start`, plus the Stage 4 leftover-debt commit `532d424`
(20 replay-command rewrites that the merged Stage 4 tip omitted, and
the 4 ledger hash fields they invalidated).

Approval artifact: `catalog/batches/p4-triangle-211-stage5.json`
(produced with this report).  Approval:

```text
YesterdaysLemon (repository owner), Stage 5 P4 triangle/211 classification migration instruction
```

applies only to the exact generated mappings recorded in that batch
file.  It does not approve the rest of `p4/classifications`,
low-confidence proposals generally, boundary files, global
classification files, or future batches.

## Scope and stop-condition verdict

All fifteen prompt candidates were verified against current `main`.
Thirteen are selected; one more complete triple from the same 211
spine (`split-center-mixed-star-211`) is included because the selected
`mixed-center-star-211` verifier imports it unconditionally and the
inseparable-dependency rule requires moving them together.  One
directly owned support script moves with its package.

**Batch: 14 packages / 43 files** (14 triples = 42 files + 1 owned
support script; preferred range 13–15 packages, 39–54 files — hit on
both).

## Selection decisions

| package (slug) | confidence | decision | rationale |
|---|---|---|---|
| 211-triangle-complete | doc medium / scripts low | **include** | standalone classification; complete triple; no imports; replay <2 s |
| common-active-211-triangle-projective-boundary | medium/low | **include** | complete triple; hashes two root component docs (shared_dependency, stay); replay ~1 s |
| common-active-binary-triangle | medium/low | **include** (+1 owned support) | complete triple; verifier imports its own `analyze_…_local_dimension.py` (sole importer → owned_by_package); Singular ds slice, replayed 9 s |
| common-kernel-yy-211-triangle-projective | medium/low | **include** | complete triple; hashes one root component doc; replay ~1 s |
| crossed-211-triangle-support | medium/low | **include** | complete triple; links two `research_figures/` images (historical, stay); replay ~1 s |
| cyclic-rank-one-triangle-support | medium/low | **include** | complete triple; replay ~1 s |
| rank-two-relation-triangle-corrected | medium/low | **include** | complete triple; most-linked classification (14 inbound); replay ~1 s |
| transitive-rank-one-triangle | medium/low | **include** | complete triple; replay ~1 s |
| triple-kernel-rank-one-triangle | medium/low | **include** | complete triple; replay ~1 s |
| two-kernel-rank-one-triangle | medium/low | **include** | complete triple; replay ~1 s |
| all-rank-two-relation-triangle-inclusion | medium/low | **include** | complete triple (inclusion theorem of the corrected classification — same spine); replay ~1 s |
| mixed-center-star-211-complete | medium/low | **include** | complete triple; imports split-center verifier (included below); replay <1 s |
| unequal-endpoint-inward-star-211-complete | medium/low | **include** | complete triple; replay ~1 s |
| split-center-mixed-star-211 | medium/low | **include** | not in the prompt seed list, but inseparable: selected mixed-center verifier imports it unconditionally; same 211 family; complete triple; replay ~3 s |
| directed-zero-divisor-triangle | medium/low | **EXCLUDE** | its verifier is **shared machinery**: imported at top level by 6 root scripts spanning 4 different component families (common-singleton analyzer + verify_p4_common_singleton's inventory chain, disjoint-secant, full-support-tangent, plus its own H22/H31 consumers). Cross-family use is dependency, not ownership. |
| nonresonant-rank-two-triangle-cut | medium | **EXCLUDE** | incomplete package: no independent audit exists (the classifier triple is 2 files), and its documented next-step replay depends on three unselected nonresonant boundary pairs (related_but_separate). |

The medium/low classifier confidence is retained as-is; Stage 5's
human review resolved *ownership* (package membership, destination,
completeness), which is what the batch approval records.  No
confidence field is promoted.

## Classification refinement (durable, rebuild-safe)

For the 43 selected classification records (plus the 1 support
script), `catalog/layout-classification.json` — the durable source —
was edited:

```text
claim_family:  p4/classifications
           ->  p4/classifications/triangle-211/<package-slug>
proposed_path: claims/p4/classifications/<file>
           ->  claims/p4/classifications/triangle-211/<package-slug>/<file>
evidence:      + "stage5_human_review: triangle/211 classification spine package"
```

`build_manifest.py` was then run normally.  Verified against the
committed manifest:

- **43 records changed**, all `review_required -> review_required`
  (no status promotion);
- all **71 already-moved records byte-identical**, `executed_batch`
  preserved 71/71;
- counts unchanged (moved 71, proposed 361, review 1583,
  projected_root_if_moved_only 2301);
- no record outside the selection changed;
- `package_metadata.resolve_claim_package_metadata` resolves the
  nested family correctly (manifest `claim_family` authoritative;
  canonical/verifier/audit share the package root; working notes are
  never canonical) — 5 new regression tests
  (`NestedClassificationMetadataTests`), suite 98 -> 103.

## File mapping (exact, 43 moves)

| old path | new path |
|---|---|
| P4_211_TRIANGLE_COMPLETE_CLASSIFICATION.md | claims/p4/classifications/triangle-211/211-triangle-complete/P4_211_TRIANGLE_COMPLETE_CLASSIFICATION.md |
| verify_p4_211_triangle_complete_classification.py | claims/p4/classifications/triangle-211/211-triangle-complete/verify_p4_211_triangle_complete_classification.py |
| audit_p4_211_triangle_complete_classification.py | claims/p4/classifications/triangle-211/211-triangle-complete/audit_p4_211_triangle_complete_classification.py |
| P4_COMMON_ACTIVE_211_TRIANGLE_PROJECTIVE_BOUNDARY_CLASSIFICATION.md | claims/p4/classifications/triangle-211/common-active-211-triangle-projective-boundary/P4_COMMON_ACTIVE_211_TRIANGLE_PROJECTIVE_BOUNDARY_CLASSIFICATION.md |
| verify_p4_common_active_211_triangle_projective_boundary_classification.py | claims/p4/classifications/triangle-211/common-active-211-triangle-projective-boundary/verify_p4_common_active_211_triangle_projective_boundary_classification.py |
| audit_p4_common_active_211_triangle_projective_boundary_classification.py | claims/p4/classifications/triangle-211/common-active-211-triangle-projective-boundary/audit_p4_common_active_211_triangle_projective_boundary_classification.py |
| P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md | claims/p4/classifications/triangle-211/common-active-binary-triangle/P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md |
| verify_p4_common_active_binary_triangle_component.py | claims/p4/classifications/triangle-211/common-active-binary-triangle/verify_p4_common_active_binary_triangle_component.py |
| audit_p4_common_active_binary_triangle_component.py | claims/p4/classifications/triangle-211/common-active-binary-triangle/audit_p4_common_active_binary_triangle_component.py |
| analyze_p4_common_active_binary_triangle_local_dimension.py | claims/p4/classifications/triangle-211/common-active-binary-triangle/analyze_p4_common_active_binary_triangle_local_dimension.py |
| P4_COMMON_KERNEL_YY_211_TRIANGLE_PROJECTIVE_CLASSIFICATION.md | claims/p4/classifications/triangle-211/common-kernel-yy-211-triangle-projective/P4_COMMON_KERNEL_YY_211_TRIANGLE_PROJECTIVE_CLASSIFICATION.md |
| verify_p4_common_kernel_yy_211_triangle_projective_classification.py | claims/p4/classifications/triangle-211/common-kernel-yy-211-triangle-projective/verify_p4_common_kernel_yy_211_triangle_projective_classification.py |
| audit_p4_common_kernel_yy_211_triangle_projective_classification.py | claims/p4/classifications/triangle-211/common-kernel-yy-211-triangle-projective/audit_p4_common_kernel_yy_211_triangle_projective_classification.py |
| P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md | claims/p4/classifications/triangle-211/crossed-211-triangle-support/P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md |
| verify_p4_crossed_211_triangle_support_classification.py | claims/p4/classifications/triangle-211/crossed-211-triangle-support/verify_p4_crossed_211_triangle_support_classification.py |
| audit_p4_crossed_211_triangle_support_classification.py | claims/p4/classifications/triangle-211/crossed-211-triangle-support/audit_p4_crossed_211_triangle_support_classification.py |
| P4_CYCLIC_RANK_ONE_TRIANGLE_SUPPORT_CLASSIFICATION.md | claims/p4/classifications/triangle-211/cyclic-rank-one-triangle-support/P4_CYCLIC_RANK_ONE_TRIANGLE_SUPPORT_CLASSIFICATION.md |
| verify_p4_cyclic_rank_one_triangle_support_classification.py | claims/p4/classifications/triangle-211/cyclic-rank-one-triangle-support/verify_p4_cyclic_rank_one_triangle_support_classification.py |
| audit_p4_cyclic_rank_one_triangle_support_classification.py | claims/p4/classifications/triangle-211/cyclic-rank-one-triangle-support/audit_p4_cyclic_rank_one_triangle_support_classification.py |
| P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md | claims/p4/classifications/triangle-211/rank-two-relation-triangle-corrected/P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md |
| verify_p4_rank_two_relation_triangle_corrected_classification.py | claims/p4/classifications/triangle-211/rank-two-relation-triangle-corrected/verify_p4_rank_two_relation_triangle_corrected_classification.py |
| audit_p4_rank_two_relation_triangle_corrected_classification.py | claims/p4/classifications/triangle-211/rank-two-relation-triangle-corrected/audit_p4_rank_two_relation_triangle_corrected_classification.py |
| P4_TRANSITIVE_RANK_ONE_TRIANGLE_CLASSIFICATION.md | claims/p4/classifications/triangle-211/transitive-rank-one-triangle/P4_TRANSITIVE_RANK_ONE_TRIANGLE_CLASSIFICATION.md |
| verify_p4_transitive_rank_one_triangle_classification.py | claims/p4/classifications/triangle-211/transitive-rank-one-triangle/verify_p4_transitive_rank_one_triangle_classification.py |
| audit_p4_transitive_rank_one_triangle_classification.py | claims/p4/classifications/triangle-211/transitive-rank-one-triangle/audit_p4_transitive_rank_one_triangle_classification.py |
| P4_TRIPLE_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md | claims/p4/classifications/triangle-211/triple-kernel-rank-one-triangle/P4_TRIPLE_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md |
| verify_p4_triple_kernel_rank_one_triangle_classification.py | claims/p4/classifications/triangle-211/triple-kernel-rank-one-triangle/verify_p4_triple_kernel_rank_one_triangle_classification.py |
| audit_p4_triple_kernel_rank_one_triangle_classification.py | claims/p4/classifications/triangle-211/triple-kernel-rank-one-triangle/audit_p4_triple_kernel_rank_one_triangle_classification.py |
| P4_TWO_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md | claims/p4/classifications/triangle-211/two-kernel-rank-one-triangle/P4_TWO_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md |
| verify_p4_two_kernel_rank_one_triangle_classification.py | claims/p4/classifications/triangle-211/two-kernel-rank-one-triangle/verify_p4_two_kernel_rank_one_triangle_classification.py |
| audit_p4_two_kernel_rank_one_triangle_classification.py | claims/p4/classifications/triangle-211/two-kernel-rank-one-triangle/audit_p4_two_kernel_rank_one_triangle_classification.py |
| P4_ALL_RANK_TWO_RELATION_TRIANGLE_COMPONENT_INCLUSION.md | claims/p4/classifications/triangle-211/all-rank-two-relation-triangle-inclusion/P4_ALL_RANK_TWO_RELATION_TRIANGLE_COMPONENT_INCLUSION.md |
| verify_p4_all_rank_two_relation_triangle_component_inclusion.py | claims/p4/classifications/triangle-211/all-rank-two-relation-triangle-inclusion/verify_p4_all_rank_two_relation_triangle_component_inclusion.py |
| audit_p4_all_rank_two_relation_triangle_component_inclusion.py | claims/p4/classifications/triangle-211/all-rank-two-relation-triangle-inclusion/audit_p4_all_rank_two_relation_triangle_component_inclusion.py |
| P4_MIXED_CENTER_STAR_211_COMPLETE_CLASSIFICATION.md | claims/p4/classifications/triangle-211/mixed-center-star-211-complete/P4_MIXED_CENTER_STAR_211_COMPLETE_CLASSIFICATION.md |
| verify_p4_mixed_center_star_211_complete_classification.py | claims/p4/classifications/triangle-211/mixed-center-star-211-complete/verify_p4_mixed_center_star_211_complete_classification.py |
| audit_p4_mixed_center_star_211_complete_classification.py | claims/p4/classifications/triangle-211/mixed-center-star-211-complete/audit_p4_mixed_center_star_211_complete_classification.py |
| P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPLETE_CLASSIFICATION.md | claims/p4/classifications/triangle-211/unequal-endpoint-inward-star-211-complete/P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPLETE_CLASSIFICATION.md |
| verify_p4_unequal_endpoint_inward_star_211_complete_classification.py | claims/p4/classifications/triangle-211/unequal-endpoint-inward-star-211-complete/verify_p4_unequal_endpoint_inward_star_211_complete_classification.py |
| audit_p4_unequal_endpoint_inward_star_211_complete_classification.py | claims/p4/classifications/triangle-211/unequal-endpoint-inward-star-211-complete/audit_p4_unequal_endpoint_inward_star_211_complete_classification.py |
| P4_SPLIT_CENTER_MIXED_STAR_211_COMPONENT.md | claims/p4/classifications/triangle-211/split-center-mixed-star-211/P4_SPLIT_CENTER_MIXED_STAR_211_COMPONENT.md |
| verify_p4_split_center_mixed_star_211_component.py | claims/p4/classifications/triangle-211/split-center-mixed-star-211/verify_p4_split_center_mixed_star_211_component.py |
| audit_p4_split_center_mixed_star_211_component.py | claims/p4/classifications/triangle-211/split-center-mixed-star-211/audit_p4_split_center_mixed_star_211_component.py |

## Dependency summary

### Intra-batch chain (moves together)

```text
verify_p4_mixed_center_star_211_complete_classification
        imports (unconditional)
verify_p4_split_center_mixed_star_211_component
```

Both packages are in this batch; post-move the importer exposes the
split-center package via `expose_claim_package`.

### Package-support chain (one support file moves)

```text
verify_p4_common_active_binary_triangle_component
        imports (unconditional)
analyze_p4_common_active_binary_triangle_local_dimension   (moves as owned support)
        imports (unconditional)
verify_p4_directed_zero_divisor_triangle_components        (STAYS at root: shared machinery)
```

The moved verifier exposes its own package directory for the sibling
analyze module; the analyze module's root import keeps resolving via
REPO_ROOT.  The analyze module writes only to `tmp/`
(REPO_ROOT-relative after the move).

### Python importers of selected modules (outside the batch)

None except the two intra-batch arrows above.  A repo-wide importer
scan confirms no other script imports any of the 14 selected
verifiers/audits/analyze modules.

### Shared dependencies that stay at root

- `P4_PURE_RANK_TWO_COMPONENT_THEOREM.md`,
  `P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md`,
  `P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md`,
  `P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT.md` etc. — component
  docs hashed/linked by selected verifiers/docs (links re-anchored;
  hash constants keep resolving via REPO_ROOT);
- `verify_p4_directed_zero_divisor_triangle_components.py` — shared
  machinery (excluded, see above);
- `research_figures/P4_CROSSED_211_TRIANGLE_SUPPORT_OCTAHEDRON.{png,svg}`
  — historical figures, linked from the crossed package doc (links
  re-anchored).

### Downstream consumers repaired in Commit C (staying files)

Path/string constants pointing at moved files:

```text
verify_p4_all_pair_rank_exceptional_graph_reduction.py
    (hashes: 211-complete doc, unequal-endpoint doc,
     all-rank-two-relation doc)
verify_p4_two_double_endpoint_star_111_complete_classification.py
    (triple-kernel doc)
verify_p5_h31_common_active_binary_triangle_component_generic_obstruction.py
verify_p5_h31_common_active_binary_triangle_component_special_divisor_obstruction.py
verify_p5_h31_common_active_binary_triangle_intrinsic_boundary_obstruction.py
verify_p5_h31_common_active_binary_triangle_normalized_affine_obstruction.py
audit_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py
derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py
verify_p4_common_active_binary_triangle_p_plus_q_boundary.py
audit_p4_common_active_binary_triangle_p_plus_q_boundary.py
audit_component20_intrinsic_wall_exceptional_fibres_candidate.py
audit_component20_intrinsic_zero_diagonal_dvr_atlas_candidate.py
derive_component20_intrinsic_wall_exceptional_fibres_candidate.py
derive_component20_intrinsic_zero_diagonal_dvr_atlas_candidate.py
derive_p4_component20_intrinsic_exceptional_base_geometry_proof_b.py
derive_p4_component20_transverse_base_diagonal_fan_proof_b.py
```

### Markdown inbound links

| theorem doc | inbound files / links |
|---|---|
| P4_211_TRIANGLE_COMPLETE_CLASSIFICATION.md | 3 / 3 (README, ALL_PAIR_RANK reduction, handoff doc) |
| P4_COMMON_ACTIVE_211_..._BOUNDARY_CLASSIFICATION.md | 1 / 1 (211-complete doc, moves) |
| P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md | 11 files / 4 links (+ 7 bare prose mentions) |
| P4_COMMON_KERNEL_YY_..._PROJECTIVE_CLASSIFICATION.md | 1 / 1 (211-complete doc, moves) |
| P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md | 9 / 8 |
| P4_CYCLIC_RANK_ONE_TRIANGLE_SUPPORT_CLASSIFICATION.md | 1 / 1 (README) |
| P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md | 13 / 14 |
| P4_TRANSITIVE_RANK_ONE_TRIANGLE_CLASSIFICATION.md | 2 / 2 |
| P4_TRIPLE_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md | 3 files / 1 link (+2 prose) |
| P4_TWO_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md | 2 / 2 |
| P4_ALL_RANK_TWO_RELATION_TRIANGLE_COMPONENT_INCLUSION.md | 6 / 5 |
| P4_MIXED_CENTER_STAR_211_COMPLETE_CLASSIFICATION.md | 3 / 3 |
| P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPLETE_CLASSIFICATION.md | 4 / 4 |
| P4_SPLIT_CENTER_MIXED_STAR_211_COMPONENT.md | 5 / 5 |

### Replay commands affected

28 replay fences inside the 14 moving docs (14 verifiers + 14 audits;
mixed `python` / `uv run --with sympy python` single-line forms — all
covered by the Stage 4 shared grammar), plus 8 fences outside the
batch (README ×4, docs/NEXT_INSTANCE_HANDOFF ×4 — `uv run` and plain
forms, also covered by the shared grammar).

### Preflight replayability (all performed pre-freeze, rc=0)

| script class | result |
|---|---|
| 12 sympy-only packages (24 scripts) | all rc=0, ≤1 s each |
| common-active-binary verifier (Singular ds, WSL fallback) | rc=0, 9 s |
| common-active-binary audit (Singular, WSL) | rc=0, 1 s |
| split-center verifier/audit | rc=0, 3 s / 1 s |

No extreme runtimes; all replays practical for this PR.  Outputs land
in `tmp/` (gitignored).

### Ledger references

Zero ledger entries reference any of the 43 moving files (the ledger
is a curated partial index; the entries whose names mention these
components point at the P5 H22/H31 consumer docs, which stay).  No
repoints; hash refresh only for ledger docs whose content changes
during rewrites (README.md).  No entries fabricated.

## Integrity summary

| measure | value |
|---|---|
| member count | 43 |
| package count | 14 (one of them +1 owned support file) |
| confidence composition | 43 review_required (medium doc / low script) + 1 tool_script medium; 0 high-confidence; no promotions |
| destination collisions | none (14 new package directories) |
| source/destination cycles | none |
| expected stale-path count increase | +43 (all root→package basename-preserving; 71 → 114) |
| expected root-entry decrease | −43 (2,301 → 2,258; all 43 sources are root files) |
| ledger entries affected | 0 repointed; hash refresh only for touched ledger docs |
| manifest summary expectations | moved 71 → 114; review_required 1583 → 1540; proposed_high_confidence 361 (unchanged); projected_root_if_moved_only 2301 → 2258 (executor recomputes, no rebuild) |

## Exclusions

| candidate | decision | reason |
|---|---|---|
| P4_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS | exclude | shared machinery: 6 root importers across 4 component families |
| P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION | exclude | no independent audit; documented replay depends on 3 unselected boundary pairs |
| all other `claims/p4/classifications` records (121 after refinement) | out of scope | other families / unreviewed; Stage 6+ |
| P4 boundary population, global exhaustiveness, atlases, P5 claims, snapshots | out of scope | §11 categories; not inseparable from any selected package |

## Cross-package acceptance note

This batch moves a package whose verifier imports another moving
package (mixed-center → split-center), a package with an owned
analyze-support module whose own import targets shared root machinery
(directed-zero-divisor), and 14 docs whose replay fences use both the
plain and the `uv run` grammar forms.  The rewriter's second pass must
report 0/0/0, and both intra-batch chains must import from a clean
checkout.
