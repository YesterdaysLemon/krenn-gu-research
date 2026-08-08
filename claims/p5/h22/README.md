# P5 generic weighted-`H22` obstruction packages

Each subdirectory is one migrated component-level generic
weighted-`H22` claim package: theorem document + primary verifier + an
independent audit where one exists, moved together with preserved
filenames.  Stage 9 used batch `p5-generic-obstructions-stage9`
(mapping_sha256
`68d20c08b987c2465395ec485647dc37c958d8400a8d05dede37559256a47f23`).
Stage 10 used batch `p5-deferred-generics-stage10` (mapping_sha256
`e39d17c3ed855ef5a1342560ebf61e9b313246142f24af23940bc3ff8af472db`).

Every theorem here is a **generic/function-field** statement: the
weighted `H22` incidence is empty at the generic point of the named
P4 component (or on a dense open subset).  None closes special
divisors, slope/projective boundaries, or the pointwise locus.

| package | theorem | verifier | audit |
|---|---|---|---|
| `all-rank-one-triangle/` | `P5_H22_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_all_rank_one_triangle_component_generic_obstruction.py` | `audit_p5_h22_all_rank_one_triangle_component_generic_obstruction.py` |
| `coincident-support/` | `P5_H22_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_coincident_support_component_generic_obstruction.py` | `audit_p5_h22_coincident_support_component_generic_obstruction.py` |
| `common-singleton/` | `P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_common_singleton_component_generic_obstruction.py` | `audit_p5_h22_common_singleton_component_generic_obstruction.py` |
| `diagonal-quadric/` | `P5_H22_DIAGONAL_QUADRIC_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_diagonal_quadric_component_generic_obstruction.py` | `audit_p5_h22_diagonal_quadric_component_generic_obstruction.py` |
| `directed-zero-divisor-triangle-components/` | `P5_H22_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_directed_zero_divisor_triangle_components_generic_obstruction.py` | `audit_p5_h22_directed_zero_divisor_triangle_components_generic_obstruction.py` |
| `disjoint-secant/` | `P5_H22_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_disjoint_secant_component_generic_obstruction.py` | `audit_p5_h22_disjoint_secant_component_generic_obstruction.py` |
| `eisenstein-norm/` | `P5_H22_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_eisenstein_norm_component_generic_obstruction.py` | `audit_p5_h22_eisenstein_norm_component_generic_obstruction.py` |
| `equal-support-common-factor/` | `P5_H22_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_equal_support_common_factor_component_generic_obstruction.py` | `audit_p5_h22_equal_support_common_factor_component_generic_obstruction.py` |
| `equal-support-sixfold/` | `P5_H22_EQUAL_SUPPORT_SIXFOLD_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_equal_support_sixfold_component_generic_obstruction.py` | — (no P5 independent audit exists) |
| `first-rank-two/` | `P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_first_rank_two_component_generic_obstruction.py` | `audit_p5_h22_first_rank_two_component_generic_obstruction.py` |
| `full-support-tangent/` | `P5_H22_FULL_SUPPORT_TANGENT_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_full_support_tangent_component_generic_obstruction.py` | `audit_p5_h22_full_support_tangent_component_generic_obstruction.py` |
| `mixed-orientation/` | `P5_H22_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_mixed_orientation_component_generic_obstruction.py` | `audit_p5_h22_mixed_orientation_component_generic_obstruction.py` |
| `one-three-components/` | `P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_one_three_components_generic_obstruction.py` | `audit_p5_h22_one_three_components_generic_obstruction.py` |
| `six-dimensional/` | `P5_H22_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_six_dimensional_component_generic_obstruction.py` | `audit_p5_h22_six_dimensional_component_generic_obstruction.py` |
| `transverse-common-factor/` | `P5_H22_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_transverse_common_factor_component_generic_obstruction.py` | `audit_p5_h22_transverse_common_factor_component_generic_obstruction.py` |
| `two-rank-two-spoke-mixed-star/` | `P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_two_rank_two_spoke_mixed_star_component_generic_obstruction.py` | `audit_p5_h22_two_rank_two_spoke_mixed_star_component_generic_obstruction.py` |

The **disjoint-mixed-star** H22 package was migrated in the layout
migration pilot (batch `p5-h22-disjoint-mixed-star-pilot`) and lives
at [`disjoint-mixed-star/`](disjoint-mixed-star/) with its boundary
subpackages and working note.  It is the structural template for this
side and is not part of the Stage 9 batch.

## Extras

`diagonal-quadric/` also carries
`P5_H22_DIAGONAL_QUADRIC_WORKING_NOTE.md`, a **superseded exploratory**
frontier note.  It is explicitly historical (not a theorem or a
certificate) and moved only because it is owned by this package,
mirroring the pilot's treatment of its working note.

## Shared and cross-package dependencies

- Root shared utilities consumed by these verifiers:
  `p5_high_coordinate_tree_chart_cegar.py` (Singular timeout helper)
  and `verify_p5_h31_marked_basis_open_branch.py` remain at the
  repository root.
- Intra-batch sibling edges: `disjoint-secant` imports its H31 sibling
  and the `full-support-tangent` H22 verifier; `full-support-tangent`
  imports its H31 sibling.  These resolve through
  `expose_claim_package` (see `src/krenn_gu/bootstrap.py`).
- Already-migrated P4 anchors under [`../../p4/`](../../p4/) are
  referenced by link and exposure helper; they were not re-moved.

## Not migrated here

The H22 common-center-kernel-star partial theorem, unequal-complement
and unequal-endpoint recursion, split-center theorem with its
candidate-derived dependency, and embedded-p3 / common-active-binary-
triangle documents remain at the repository root with their boundary
forests or open recursion.  The equal-support-sixfold package is
present with its actual primary-only evidence structure; migration did
not create an audit or promote its status.  Migration status changes no
theorem claim; the global conjecture remains **UNRESOLVED**.
