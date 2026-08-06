# P4 component packages

Each subdirectory is one migrated pure-`P_4` component claim package:
theorem document + primary verifier + independent audit, moved together
as a unit (Stage 3 batch `p4-components-stage3`, mapping_sha256
`17058a8819de…`).  Filenames are preserved; no file was renamed to a
generic name.

## `disjoint-mixed-star/`

- `P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`
- `audit_p4_disjoint_mixed_star_pure_component.py`
- `verify_p4_disjoint_mixed_star_pure_component.py`

## `equal-support-sixfold/`

- `P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md`
- `audit_p4_equal_support_sixfold_pure_component.py`
- `verify_p4_equal_support_sixfold_pure_component.py`

## `split-pair/`

- `P4_SPLIT_PAIR_PURE_COMPONENT.md`
- `audit_p4_split_pair_pure_component.py`
- `verify_p4_split_pair_pure_component.py`

Shared dependencies (e.g. `verify_p4_mixed_orientation_pure_component`,
the global classification documents, and research snapshots) stay at the
repository root or in `research_snapshots/`; cross-family references are
links, not file ownership.  Migration status does not change any theorem
claim, and the global conjecture remains **UNRESOLVED**.
