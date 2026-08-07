# P4 star / mixed-star classification packages

Migrated P4 star / mixed-star classification packages — the second P4
classification spine, moved as Stage 6 batch `p4-star-stage6`
(mapping_sha256 `25c91c812a1f…`).  These are the migrated
classification packages of the star family; this table does not claim
the family (or the P4 classification) is exhaustive — where a
package's own theorem states completeness it is noted in its status
column.

Filenames are preserved; no file was renamed to a generic name.

| package | claim document | verifier | audit | status/provenance source | batch |
|---|---|---|---|---|---|
| `all-center-kernel-star-111-obstruction/` | `P4_ALL_CENTER_KERNEL_STAR_111_OBSTRUCTION.md` | `verify_p4_all_center_kernel_star_111_obstruction.py` | `audit_p4_all_center_kernel_star_111_obstruction.py` | classifier review_required (p4/boundaries); Stage 6 review: star-cell-specific orientation obstruction | stage6 |
| `all-double-endpoint-star-111-obstruction/` | `P4_ALL_DOUBLE_ENDPOINT_STAR_111_OBSTRUCTION.md` | `verify_p4_all_double_endpoint_star_111_obstruction.py` | `audit_p4_all_double_endpoint_star_111_obstruction.py` | classifier review_required (p4/boundaries); Stage 6 review: star-cell-specific orientation obstruction | stage6 |
| `coincident-support-rank-one-star/` | `P4_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT.md` | `verify_p4_coincident_support_rank_one_star_component.py` | `audit_p4_coincident_support_rank_one_star_component.py` | classifier review_required; Stage 6 review | stage6 |
| `coincident-support-star-reverse/` | `P4_COINCIDENT_SUPPORT_STAR_REVERSE_CLASSIFICATION.md` | `verify_p4_coincident_support_star_reverse_classification.py` | `audit_p4_coincident_support_star_reverse_classification.py` | classifier review_required; Stage 6 review | stage6 |
| `common-center-kernel-star-211/` | `P4_COMMON_CENTER_KERNEL_STAR_211_COMPONENT.md` | `verify_p4_common_center_kernel_star_211_component.py` | `audit_p4_common_center_kernel_star_211_component.py` | classifier review_required; Stage 6 review | stage6 |
| `disjoint-mixed-star-affine/` | `P4_DISJOINT_MIXED_STAR_AFFINE_CLASSIFICATION.md` | `verify_p4_disjoint_mixed_star_affine_classification.py` | `audit_p4_disjoint_mixed_star_affine_classification.py` | classifier review_required; Stage 6 review | stage6 |
| `disjoint-mixed-star-projective/` | `P4_DISJOINT_MIXED_STAR_PROJECTIVE_CLASSIFICATION.md` | `verify_p4_disjoint_mixed_star_projective_classification.py` | `audit_p4_disjoint_mixed_star_projective_classification.py` | classifier review_required; Stage 6 review | stage6 |
| `equal-endpoint-inward-star-211-obstruction/` | `P4_EQUAL_ENDPOINT_INWARD_STAR_211_OBSTRUCTION.md` | `verify_p4_equal_endpoint_inward_star_211_obstruction.py` | `audit_p4_equal_endpoint_inward_star_211_obstruction.py` | classifier review_required (p4/boundaries); Stage 6 review: closes the two-inward frontier of the star (2,1,1) cell | stage6 |
| `mixed-endpoint-star-111-complete/` | `P4_MIXED_ENDPOINT_STAR_111_COMPLETE_CLASSIFICATION.md` | `verify_p4_mixed_endpoint_star_111_complete_classification.py` | `audit_p4_mixed_endpoint_star_111_complete_classification.py` | classifier review_required; Stage 6 review | stage6 |
| `no-double-endpoint-star-1110-collision/` | `P4_NO_DOUBLE_ENDPOINT_STAR_1110_COLLISION_CLASSIFICATION.md` | `verify_p4_no_double_endpoint_star_1110_collision_classification.py` | `audit_p4_no_double_endpoint_star_1110_collision_classification.py` | classifier review_required; Stage 6 review; Singular required (exact radical replay, WSL fallback) | stage6 |
| `one-double-endpoint-star-111/` | `P4_ONE_DOUBLE_ENDPOINT_STAR_111_CLASSIFICATION.md` | `verify_p4_one_double_endpoint_star_111_classification.py` | `audit_p4_one_double_endpoint_star_111_classification.py` | classifier review_required; Stage 6 review; Singular required (exact radical replay, WSL fallback) | stage6 |
| `radical-star/` | `P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md` | `verify_p4_radical_star_component_classification.py` | `audit_p4_radical_star_component_classification.py` | classifier review_required; Stage 6 review | stage6 |
| `rank-two-relation-star-obstruction/` | `P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md` | `verify_p4_rank_two_relation_star_obstruction.py` | `audit_p4_rank_two_relation_star_obstruction.py` | classifier review_required (p4/boundaries); Stage 6 review: repaired rank-two-relation star obstruction | stage6 |
| `two-double-endpoint-star-111-complete/` | `P4_TWO_DOUBLE_ENDPOINT_STAR_111_COMPLETE_CLASSIFICATION.md` | `verify_p4_two_double_endpoint_star_111_complete_classification.py` | `audit_p4_two_double_endpoint_star_111_complete_classification.py` | classifier review_required; Stage 6 review | stage6 |
| `two-rank-two-spoke-mixed-star-classification/` | `P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_CLASSIFICATION.md` | `verify_p4_two_rank_two_spoke_mixed_star_classification.py` | `audit_p4_two_rank_two_spoke_mixed_star_classification.py` | classifier review_required; Stage 6 review; slug keeps `-classification` to avoid collision with the component package | stage6 |
| `two-rank-two-spoke-mixed-star-component/` | `P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md` | `verify_p4_two_rank_two_spoke_mixed_star_component.py` | `audit_p4_two_rank_two_spoke_mixed_star_component.py` | classifier review_required; Stage 6 review | stage6 |
| `unequal-endpoint-inward-star-211/` | `P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPONENT.md` | `verify_p4_unequal_endpoint_inward_star_211_component.py` | `audit_p4_unequal_endpoint_inward_star_211_component.py` | classifier review_required; Stage 6 review | stage6 |

## Already-migrated cross-spine dependencies

These star-related packages migrated earlier and are **not** Stage 6
members; they remain stable dependencies:

- [`../triangle-211/mixed-center-star-211-complete/`](../triangle-211/mixed-center-star-211-complete/)
  (Stage 5, `p4-triangle-211-stage5`)
- [`../triangle-211/split-center-mixed-star-211/`](../triangle-211/split-center-mixed-star-211/)
  (Stage 5)
- [`../triangle-211/unequal-endpoint-inward-star-211-complete/`](../triangle-211/unequal-endpoint-inward-star-211-complete/)
  (Stage 5)
- [`../../components/disjoint-mixed-star/`](../../components/disjoint-mixed-star/)
  (Stage 3, pure component)

## Deliberately not in this spine

- `P4_RANK_TWO_RELATION_STAR_OBSTRUCTION_WITHDRAWN_OVERSTRONG` —
  withdrawn historical artifact; the classifier proposes
  `claims/legacy/` (high confidence); belongs to a dedicated legacy
  batch, not the star classification spine.
- Shared machinery (`verify_p4_directed_zero_divisor_triangle_components`,
  `verify_p4_common_singleton_component`,
  `verify_p4_all_pair_rank_exceptional_graph_reduction`) — cross-family
  use is dependency, not ownership.
- P5 H22/H31 star-consumer population — downstream consumers; P5
  migration is a later stage.
- Other boundary theorems, global exhaustion machinery, atlases, and
  working notes — separate ownership; cross-links only.

Migration provenance: `catalog/batches/p4-star-stage6.json`,
`docs/architecture/p4-star-stage6-dry-run.md`, and
`docs/architecture/layout-migration-stage6-report.md`.  No theorem
claim changed; the global conjecture remains **UNRESOLVED**.
