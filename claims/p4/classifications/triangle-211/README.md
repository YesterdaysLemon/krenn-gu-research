# Triangle / 211 classification packages

Migrated triangle / 211 classification packages — the first P4
classification spine, moved as Stage 5 batch
`p4-triangle-211-stage5` (mapping_sha256 `2838344305e6…`).  These are
the migrated classification packages of the 211/triangle family; this
table does not claim the family (or the P4 classification) is
exhaustive — where a package's own theorem states completeness it is
noted in its status column.

Filenames are preserved; no file was renamed to a generic name.

| package | claim document | verifier | audit | status/provenance source | batch |
|---|---|---|---|---|---|
| `211-triangle-complete/` | `P4_211_TRIANGLE_COMPLETE_CLASSIFICATION.md` | `verify_p4_211_triangle_complete_classification.py` | `audit_p4_211_triangle_complete_classification.py` | classifier review_required (medium doc / low scripts); Stage 5 human review confirmed the triple | stage5 |
| `all-rank-two-relation-triangle-inclusion/` | `P4_ALL_RANK_TWO_RELATION_TRIANGLE_COMPONENT_INCLUSION.md` | `verify_p4_all_rank_two_relation_triangle_component_inclusion.py` | `audit_p4_all_rank_two_relation_triangle_component_inclusion.py` | classifier review_required; Stage 5 review | stage5 |
| `common-active-211-triangle-projective-boundary/` | `P4_COMMON_ACTIVE_211_TRIANGLE_PROJECTIVE_BOUNDARY_CLASSIFICATION.md` | `verify_p4_common_active_211_triangle_projective_boundary_classification.py` | `audit_p4_common_active_211_triangle_projective_boundary_classification.py` | classifier review_required; Stage 5 review | stage5 |
| `common-active-binary-triangle/` | `P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md` | `verify_p4_common_active_binary_triangle_component.py` | `audit_p4_common_active_binary_triangle_component.py` | classifier review_required; Stage 5 review; includes owned support `analyze_p4_common_active_binary_triangle_local_dimension.py` | stage5 |
| `common-kernel-yy-211-triangle-projective/` | `P4_COMMON_KERNEL_YY_211_TRIANGLE_PROJECTIVE_CLASSIFICATION.md` | `verify_p4_common_kernel_yy_211_triangle_projective_classification.py` | `audit_p4_common_kernel_yy_211_triangle_projective_classification.py` | classifier review_required; Stage 5 review | stage5 |
| `crossed-211-triangle-support/` | `P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md` | `verify_p4_crossed_211_triangle_support_classification.py` | `audit_p4_crossed_211_triangle_support_classification.py` | classifier review_required; Stage 5 review | stage5 |
| `cyclic-rank-one-triangle-support/` | `P4_CYCLIC_RANK_ONE_TRIANGLE_SUPPORT_CLASSIFICATION.md` | `verify_p4_cyclic_rank_one_triangle_support_classification.py` | `audit_p4_cyclic_rank_one_triangle_support_classification.py` | classifier review_required; Stage 5 review | stage5 |
| `mixed-center-star-211-complete/` | `P4_MIXED_CENTER_STAR_211_COMPLETE_CLASSIFICATION.md` | `verify_p4_mixed_center_star_211_complete_classification.py` | `audit_p4_mixed_center_star_211_complete_classification.py` | classifier review_required; Stage 5 review | stage5 |
| `rank-two-relation-triangle-corrected/` | `P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md` | `verify_p4_rank_two_relation_triangle_corrected_classification.py` | `audit_p4_rank_two_relation_triangle_corrected_classification.py` | classifier review_required; Stage 5 review | stage5 |
| `split-center-mixed-star-211/` | `P4_SPLIT_CENTER_MIXED_STAR_211_COMPONENT.md` | `verify_p4_split_center_mixed_star_211_component.py` | `audit_p4_split_center_mixed_star_211_component.py` | classifier review_required; included because the selected mixed-center verifier imports it unconditionally | stage5 |
| `transitive-rank-one-triangle/` | `P4_TRANSITIVE_RANK_ONE_TRIANGLE_CLASSIFICATION.md` | `verify_p4_transitive_rank_one_triangle_classification.py` | `audit_p4_transitive_rank_one_triangle_classification.py` | classifier review_required; Stage 5 review | stage5 |
| `triple-kernel-rank-one-triangle/` | `P4_TRIPLE_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md` | `verify_p4_triple_kernel_rank_one_triangle_classification.py` | `audit_p4_triple_kernel_rank_one_triangle_classification.py` | classifier review_required; Stage 5 review | stage5 |
| `two-kernel-rank-one-triangle/` | `P4_TWO_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md` | `verify_p4_two_kernel_rank_one_triangle_classification.py` | `audit_p4_two_kernel_rank_one_triangle_classification.py` | classifier review_required; Stage 5 review | stage5 |
| `unequal-endpoint-inward-star-211-complete/` | `P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPLETE_CLASSIFICATION.md` | `verify_p4_unequal_endpoint_inward_star_211_complete_classification.py` | `audit_p4_unequal_endpoint_inward_star_211_complete_classification.py` | classifier review_required; Stage 5 review | stage5 |

## Deliberately not in this spine

- [`../P4_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS.md`](../P4_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS.md)
  — shared machinery: its verifier is imported by six downstream scripts
  spanning four component
  families; cross-family use is dependency, not ownership.
- `P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION` — no independent
  audit exists; its documented replay depends on three unselected
  boundary pairs.
- Boundary theorems, global exhaustion machinery, atlases, working
  notes, and P5 consumers — separate ownership; cross-links only.

Migration provenance: `catalog/batches/p4-triangle-211-stage5.json`,
`docs/architecture/p4-triangle-211-stage5-dry-run.md`, and
`docs/architecture/layout-migration-stage5-report.md`.  No theorem
claim changed; the global conjecture remains **UNRESOLVED**.
