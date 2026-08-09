# P5 marked-`H31` obstruction packages

Most subdirectories are migrated component-level generic marked-`H31`
claim packages: theorem document + primary verifier + an independent
audit where one exists, moved together with preserved filenames.  The
`embedded-p3/` package is the one exception: it contains the complete
five-triple generic, boundary, and projective closure forest.  Stage 9
used batch `p5-generic-obstructions-stage9`
(mapping_sha256
`68d20c08b987c2465395ec485647dc37c958d8400a8d05dede37559256a47f23`).
Stage 10 used batch `p5-deferred-generics-stage10` (mapping_sha256
`e39d17c3ed855ef5a1342560ebf61e9b313246142f24af23940bc3ff8af472db`).
Stage 16 used batch `p5-h31-embedded-p3-stage16` (mapping_sha256
`db3bf4cc6309334ffc2a9983456f8674d9df5f22c3f921c969bcc4af414d5fb7`).

Except for the `embedded-p3/` closure forest described below, every
theorem in the generic-package table is a **generic/function-field**
statement: the marked `H31` fibre is empty at the generic point of the
named P4 component (or on a dense open subset).  Those generic theorems
do not close special divisors, projective boundaries, or the pointwise
locus.

| package | theorem | verifier | audit |
|---|---|---|---|
| `all-rank-one-triangle/` | `P5_H31_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_all_rank_one_triangle_component_generic_obstruction.py` | `audit_p5_h31_all_rank_one_triangle_component_generic_obstruction.py` |
| `coincident-support/` | `P5_H31_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_coincident_support_component_generic_obstruction.py` | `audit_p5_h31_coincident_support_component_generic_obstruction.py` |
| `coincident-support-rank-one-star/` | `P5_H31_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_coincident_support_rank_one_star_component_generic_obstruction.py` | `audit_p5_h31_coincident_support_rank_one_star_component_generic_obstruction.py` |
| `common-center-kernel-star/` | `P5_H31_COMMON_CENTER_KERNEL_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_common_center_kernel_star_component_generic_obstruction.py` | `audit_p5_h31_common_center_kernel_star_component_generic_obstruction.py` |
| `common-kernel-vertical-triangle/` | `P5_H31_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_common_kernel_vertical_triangle_component_generic_obstruction.py` | `audit_p5_h31_common_kernel_vertical_triangle_component_generic_obstruction.py` |
| `common-singleton/` | `P5_H31_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_common_singleton_component_generic_obstruction.py` | `audit_p5_h31_common_singleton_component_generic_obstruction.py` |
| `directed-zero-divisor-triangle-components/` | `P5_H31_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_directed_zero_divisor_triangle_components_generic_obstruction.py` | `audit_p5_h31_directed_zero_divisor_triangle_components_generic_obstruction.py` |
| `disjoint-mixed-star/` | `P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_disjoint_mixed_star_component_generic_obstruction.py` | `audit_p5_h31_disjoint_mixed_star_component_generic_obstruction.py` |
| `disjoint-secant/` | `P5_H31_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_disjoint_secant_component_generic_obstruction.py` | `audit_p5_h31_disjoint_secant_component_generic_obstruction.py` |
| `eisenstein-norm/` | `P5_H31_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_eisenstein_norm_component_generic_obstruction.py` | `audit_p5_h31_eisenstein_norm_component_generic_obstruction.py` |
| `equal-support-common-factor/` | `P5_H31_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_equal_support_common_factor_component_generic_obstruction.py` | `audit_p5_h31_equal_support_common_factor_component_generic_obstruction.py` |
| `equal-support-sixfold/` | `P5_H31_EQUAL_SUPPORT_SIXFOLD_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_equal_support_sixfold_component_generic_obstruction.py` | — (no P5 independent audit exists) |
| `full-support-tangent/` | `P5_H31_FULL_SUPPORT_TANGENT_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_full_support_tangent_component_generic_obstruction.py` | `audit_p5_h31_full_support_tangent_component_generic_obstruction.py` |
| `mixed-orientation/` | `P5_H31_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_mixed_orientation_component_generic_obstruction.py` | `audit_p5_h31_mixed_orientation_component_generic_obstruction.py` |
| `one-three/` | `P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_one_three_component_generic_obstruction.py` | `audit_p5_h31_one_three_component_generic_obstruction.py` |
| `six-dimensional/` | `P5_H31_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_six_dimensional_component_generic_obstruction.py` | `audit_p5_h31_six_dimensional_component_generic_obstruction.py` |
| `split-center-mixed-star/` | `P5_H31_SPLIT_CENTER_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_split_center_mixed_star_component_generic_obstruction.py` | `audit_p5_h31_split_center_mixed_star_component_generic_obstruction.py` |
| `transverse-common-factor/` | `P5_H31_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_transverse_common_factor_component_generic_obstruction.py` | `audit_p5_h31_transverse_common_factor_component_generic_obstruction.py` |
| `two-rank-two-spoke-mixed-star/` | `P5_H31_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_two_rank_two_spoke_mixed_star_component_generic_obstruction.py` | `audit_p5_h31_two_rank_two_spoke_mixed_star_component_generic_obstruction.py` |
| `unequal-complement-common-kernel/` | `P5_H31_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction.py` | `audit_p5_h31_unequal_complement_common_kernel_component_generic_obstruction.py` |
| `unequal-endpoint-inward-star/` | `P5_H31_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction.py` | `audit_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction.py` |

## Embedded-P3 closure forest

The five triples in `embedded-p3/` are one proof-obligation forest.  The
normalized, support-two, and `r=0` theorems close the affine charts used
by the projective case-union theorem.

| scope | theorem | verifier | audit |
|---|---|---|---|
| dense generic point | `P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h31_embedded_p3_component_generic_obstruction.py` | `audit_p5_h31_embedded_p3_component_generic_obstruction.py` |
| normalized `A B r != 0` chart | `P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md` | `verify_p5_h31_embedded_p3_component_normalized_boundary.py` | `audit_p5_h31_embedded_p3_component_normalized_boundary.py` |
| support-two `A=0, B!=0` divisor | `P5_H31_EMBEDDED_P3_COMPONENT_SUPPORT_TWO_BOUNDARY_OBSTRUCTION.md` | `verify_p5_h31_embedded_p3_component_support_two_boundary.py` | `audit_p5_h31_embedded_p3_component_support_two_boundary.py` |
| `r=0, A B!=0` divisor | `P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md` | `verify_p5_h31_embedded_p3_component_r_zero_boundary.py` | `audit_p5_h31_embedded_p3_component_r_zero_boundary.py` |
| full projective ninth component | `P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md` | `verify_p5_h31_embedded_p3_component_projective_closure.py` | `audit_p5_h31_embedded_p3_component_projective_closure.py` |

Only the generic triple has a curated theorem-ledger entry, whose status
remains `verified_generic`.  Each audit is modular corroboration and does
not replace its theorem's characteristic-zero proof.

## Extras

`all-rank-one-triangle/` also carries
`explore_p5_h31_all_rank_one_triangle_modular.py`, a finite-field
**exploration** script.  It is evidence only, not a theorem replay,
and is not part of the characteristic-zero verification.

## Shared and cross-package dependencies

- Root shared utilities consumed by these verifiers:
  `verify_p5_h31_marked_basis_open_branch.py`,
  `p5_high_coordinate_tree_chart_cegar.py`, and
  `verify_p4_directed_zero_divisor_triangle_components.py` remain at
  the repository root.
- Already-migrated P4 anchors (components and star/pair-geometry
  classifications under [`../../p4/`](../../p4/)) are referenced by
  link and by `expose_claim_package`; they were not re-moved.
- Bare-name imports of modules inside these hyphenated package
  directories go through the shared
  `krenn_gu.bootstrap.expose_claim_package` helper
  (`src/krenn_gu/bootstrap.py`).

## Not migrated here

The H31 diagonal-quadric **elliptic** and
common-active-binary-triangle generic documents remain at the
repository root with their boundary forests: their generic cores are
not separable from descendant evidence at this granularity.  The
separate weighted-H22 embedded-P3 programme also remains at root; its
projective coverage is still open and it is not part of the closed H31
forest above.  The equal-support-sixfold package is present with its
actual primary-only evidence structure; migration did not create an
audit or promote its status.  Migration status changes no theorem
claim; the global conjecture remains **UNRESOLVED**.
