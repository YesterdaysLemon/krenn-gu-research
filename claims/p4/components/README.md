# P4 component packages

Each subdirectory is one migrated pure-`P_4` component claim package:
theorem document + primary verifier + independent audit, moved together
as a unit with preserved filenames (no file was renamed to a generic
name).  Batches:

- `p4-components-stage3` (mapping_sha256 `17058a8819de…`):
  disjoint-mixed-star, equal-support-sixfold, split-pair;
- `p4-components-stage4` (mapping_sha256 `5833e9f2e17f…`):
  all-rank-one-triangle, diagonal-quadric, embedded-p3,
  mixed-orientation, single-word-quadrilateral, six-dimensional.

These nine directories are the migrated standalone pure-component
packages; they are not claimed here to exhaust the P4 component
classification.

| package | theorem | verifier | audit | batch |
|---|---|---|---|---|
| `all-rank-one-triangle/` | `P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md` | `verify_p4_all_rank_one_triangle_pure_component.py` | `audit_p4_all_rank_one_triangle_pure_component.py` | stage4 |
| `diagonal-quadric/` | `P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md` | `verify_p4_diagonal_quadric_pure_component.py` | `audit_p4_diagonal_quadric_pure_component.py` | stage4 |
| `disjoint-mixed-star/` | `P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md` | `verify_p4_disjoint_mixed_star_pure_component.py` | `audit_p4_disjoint_mixed_star_pure_component.py` | stage3 |
| `embedded-p3/` | `P4_EMBEDDED_P3_PURE_COMPONENT.md` | `verify_p4_embedded_p3_pure_component.py` | `audit_p4_embedded_p3_pure_component.py` | stage4 |
| `equal-support-sixfold/` | `P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md` | `verify_p4_equal_support_sixfold_pure_component.py` | `audit_p4_equal_support_sixfold_pure_component.py` | stage3 |
| `mixed-orientation/` | `P4_MIXED_ORIENTATION_PURE_COMPONENT.md` | `verify_p4_mixed_orientation_pure_component.py` | `audit_p4_mixed_orientation_pure_component.py` | stage4 |
| `single-word-quadrilateral/` | `P4_SINGLE_WORD_QUADRILATERAL_PURE_COMPONENT.md` | `verify_p4_single_word_quadrilateral_pure_component.py` | `audit_p4_single_word_quadrilateral_pure_component.py` | stage4 |
| `six-dimensional/` | `P4_SIX_DIMENSIONAL_PURE_COMPONENT.md` | `verify_p4_six_dimensional_pure_component.py` | `audit_p4_six_dimensional_pure_component.py` | stage4 |
| `split-pair/` | `P4_SPLIT_PAIR_PURE_COMPONENT.md` | `verify_p4_split_pair_pure_component.py` | `audit_p4_split_pair_pure_component.py` | stage3 |

## Cross-package imports

The Stage 4 batch deliberately kept the dependency chain

```text
mixed-orientation  <-  disjoint-mixed-star (moved Stage 3)
                     <-  all-rank-one-triangle
                          <-  root P5 H22/H31 AROT verifiers (guarded)
```

usable after multiple package relocations.  Bare-name imports of
modules inside these hyphenated package directories go through the
single shared helper `krenn_gu.bootstrap.expose_claim_package`
(see `src/krenn_gu/bootstrap.py`); no per-importer `sys.path` shims
remain for these packages.

## Shared dependencies

The global classification documents, research snapshots, and the P5
H22/H31 consumer scripts stay at the repository root or in
`research_snapshots/`; cross-family references are links, not file
ownership.  Migration status does not change any theorem claim, and the
global conjecture remains **UNRESOLVED**.
