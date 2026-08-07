# P4 pair-geometry boundary packages

Migrated P4 pair-geometry boundary packages — genuine boundary
inclusions of the pair-geometry family, moved as Stage 7 batch
`p4-pair-geometry-stage7` (mapping_sha256 `dbe3558f58f4…`).  These
claims are boundary-owned: each proves that a degenerate pair
configuration lies in the closure of an already-certified component
and therefore creates no new component.

Filenames are preserved; no file was renamed to a generic name.

| package | claim document | verifier | audit | status/provenance source | batch |
|---|---|---|---|---|---|
| `support-one-secant/` | `P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md` | `verify_p4_support_one_secant_boundary_inclusion.py` | `audit_p4_support_one_secant_boundary_inclusion.py` | classifier review_required (p4/boundaries); Stage 7 review confirmed the boundary category | stage7 |
| `support-two-tangent-flag/` | `P4_SUPPORT_TWO_TANGENT_FLAG_BOUNDARY_INCLUSION.md` | `verify_p4_support_two_tangent_flag_boundary_inclusion.py` | `audit_p4_support_two_tangent_flag_boundary_inclusion.py` | classifier review_required (p4/boundaries); Stage 7 review confirmed the boundary category | stage7 |

## Relationship to the classification spine

Both inclusions bound strata classified in
[`../../classifications/pair-geometry/`](../../classifications/pair-geometry/):
support-one secants lie in the closure of the disjoint-secant
component (fifteen), and support-two tangent flags lie on the known
six-dimensional lower-pair component.  The classification/boundary
distinction is preserved by directory, not merely by filename.

Migration provenance: `catalog/batches/p4-pair-geometry-stage7.json`
and `docs/architecture/layout-migration-stage7-report.md`.  No
theorem claim changed; the global conjecture remains **UNRESOLVED**.
