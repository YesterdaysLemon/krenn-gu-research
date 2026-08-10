# P4 pair-geometry classification packages

Migrated P4 pair-geometry classification packages — the third P4
classification spine, moved as Stage 7 batch `p4-pair-geometry-stage7`
(mapping_sha256 `dbe3558f58f4…`).  These are the migrated
classification packages of the pair-geometry family; this table does
not claim the family (or the P4 classification) is exhaustive — where
a package's own theorem states completeness it is noted in its status
column.

The family covers: the rank-one/rank-two pair-image structure
(rank-one obstruction, rank-two kernel geometry), the secant and
tangent lower-pair component strata (components fifteen and fourteen,
the overlapping secant sixfold identification), the decomposable
rank-two family and rank-drop reduction feeding the pure-rank-two
component geometry, the lower-pair exhaustion corollary, and the
pure-rank-two component cluster (canonical theorem, chart closure,
toric boundary, Segre slice reduction).

Filenames are preserved; no file was renamed to a generic name.

| package | claim document | verifier | audit | status/provenance source | batch |
|---|---|---|---|---|---|
| `rank-one-pair-obstruction/` | `P4_RANK_ONE_PAIR_OBSTRUCTION.md` | `verify_p4_rank_one_pair_obstruction.py` | `audit_p4_rank_one_pair_obstruction.py` | classifier review_required (p4/boundaries); Stage 7 review: structural theorem, not a boundary inclusion | stage7 |
| `rank-two-pair-kernel-geometry/` | `P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md` | `verify_p4_rank_two_pair_kernel_geometry.py` | **none** — the document states the verifier is a tiny exact replay of the completed symbolic proof; intentional documented state | classifier review_required (p4/boundaries); Stage 7 review: structural theorem | stage7 |
| `disjoint-secant-lower-pair/` | `P4_DISJOINT_SECANT_LOWER_PAIR_COMPONENT.md` | `verify_p4_disjoint_secant_lower_pair_component.py` | `audit_p4_disjoint_secant_lower_pair_component.py` | classifier review_required; Stage 7 review | stage7 |
| `overlapping-secant-lower-pair/` | `P4_OVERLAPPING_SECANT_LOWER_PAIR_CLASSIFICATION.md` | `verify_p4_overlapping_secant_lower_pair_classification.py` | `audit_p4_overlapping_secant_lower_pair_classification.py` | classifier review_required; Stage 7 review; identification target is the migrated six-dimensional component | stage7 |
| `full-support-tangent-pair/` | `P4_FULL_SUPPORT_TANGENT_PAIR_COMPONENT.md` | `verify_p4_full_support_tangent_pair_component.py` | `audit_p4_full_support_tangent_pair_component.py` | classifier review_required; Stage 7 review | stage7 |
| `tangent-rank-two-pair-purity/` | `P4_TANGENT_RANK_TWO_PAIR_PURITY_CLASSIFICATION.md` | `verify_p4_tangent_rank_two_pair_purity_classification.py` | `audit_p4_tangent_rank_two_pair_purity_classification.py` | classifier review_required; Stage 7 review | stage7 |
| `decomposable-rank-two-family/` | `P4_DECOMPOSABLE_RANK_TWO_FAMILY.md` | `verify_p4_decomposable_rank_two_family.py` | `audit_p4_decomposable_rank_two_family.py` | classifier review_required (p4/boundaries); Stage 7 review: construction theorem feeding the pure-rank-two component | stage7 |
| `decomposable-restriction-rank-drop/` | `P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md` | `verify_p4_decomposable_restriction_rank_drop.py` | `audit_p4_decomposable_restriction_rank_drop.py` | classifier review_required (p4/boundaries); Stage 7 review: tensor rank-drop theorem | stage7 |
| `lower-pair-rank-exhaustion/` | `P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md` | **corollary document only** — its stated replay is the union of the eight sibling pair-geometry verifier/audit scripts | classifier review_required; Stage 7 review; intentional documented state | stage7 |
| `pure-rank-two/` | `P4_PURE_RANK_TWO_COMPONENT_THEOREM.md` (canonical) | `verify_p4_pure_rank_two_component.py` | `audit_p4_pure_rank_two_component.py` | classifier review_required; Stage 7 review; multi-document cluster | stage7 |

## The pure-rank-two cluster

One mathematical package with four connected subclaims; each carries
its own verifier + audit (provenance stays per-executable):

| document | role | verifier | audit |
|---|---|---|---|
| `P4_PURE_RANK_TWO_COMPONENT_THEOREM.md` | canonical component theorem | `verify_p4_pure_rank_two_component.py` | `audit_p4_pure_rank_two_component.py` |
| `P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md` | closure certificate of the component chart | `verify_p4_pure_rank_two_component_chart_closure.py` | `audit_p4_pure_rank_two_component_chart_closure.py` |
| `P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md` | reduction closing the toric divisor orientations | `verify_p4_pure_rank_two_toric_slice_segre.py` | `audit_p4_pure_rank_two_toric_slice_segre.py` |
| `boundaries/P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md` | toric boundary fan subclaim (`boundaries/` subpackage) | `boundaries/verify_p4_pure_rank_two_component_toric_boundary.py` | `boundaries/audit_p4_pure_rank_two_component_toric_boundary.py` |

## Already-migrated cross-spine dependencies

These packages migrated earlier and are **not** Stage 7 members; they
remain stable dependencies:

- [`../../components/six-dimensional/`](../../components/six-dimensional/)
  (Stage 3/4) — identification target of the overlapping secant and
  support-two tangent flag results
- [`../../components/diagonal-quadric/`](../../components/diagonal-quadric/)
  (Stage 4) — second pure-rank-two-era component referenced by the
  pure-rank-two theorem and toric boundary docs
- [`../triangle-211/`](../triangle-211/) and [`../star/`](../star/)
  (Stages 5–6) — sibling classification spines
- the migrated star package
  [`../star/no-double-endpoint-star-1110-collision/`](../star/no-double-endpoint-star-1110-collision/)
  hashes the lower-pair exhaustion doc

Genuine boundary inclusions of this family live under
[`../../boundaries/pair-geometry/`](../../boundaries/pair-geometry/).

## Deliberately not in this spine

- [`P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md`](../P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md)
  — shared/global pair-rank machinery spanning stars, triangles, and pair
  geometry; it remains parent-classification-owned.
- [`verify_p4_directed_zero_divisor_triangle_components.py`](../verify_p4_directed_zero_divisor_triangle_components.py)
  and [`verify_p4_common_singleton_component.py`](../verify_p4_common_singleton_component.py)
  — shared parent-owned machinery; cross-family use is dependency, not
  ownership.
- [`P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md`](../P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md),
  [`P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md`](../P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md),
  (the `q4_211` marked boundary population), and
  [`P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md`](../P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md)
  (the mixed-orientation family) remain separately parent-owned.
- P5 H22/H31 pair-geometry consumers are downstream under the P5 tree;
  cross-family use is dependency, not ownership.

Migration provenance: `catalog/batches/p4-pair-geometry-stage7.json`,
`docs/architecture/p4-pair-geometry-stage7-dry-run.md`, and
`docs/architecture/layout-migration-stage7-report.md`.  No theorem
claim changed; the global conjecture remains **UNRESOLVED**.
