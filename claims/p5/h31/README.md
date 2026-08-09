# P5 marked-`H31` obstruction packages

Most subdirectories are migrated component-level generic marked-`H31`
claim packages: theorem document + primary verifier + an independent
audit where one exists, moved together with preserved filenames.  There
are seven scoped exceptions.  The `embedded-p3/` package contains the
complete five-triple generic, boundary, and projective component-closure
forest.  The three single-gate directories form one complete
rank-one-gate obstruction forest, not a generic package or complete
component closure.  The `common-active-binary-triangle/` package contains
the complete three-triple diagonal `p+q=0` wall subforest, not the broader
common-active component family.  The `internal-e0-marked-fibre/` package is
one exact divisor-scoped leaf, not a generic theorem or whole-component
package.  The `toric-marked-fibre/` package is the exact complete marked-fibre
obstruction over the 21 genuine toric base-orbit/orientation cases of the
first pure-rank-two compression component, not its projective interior, a
second or further component, or a whole-component theorem.
The `component-chart-boundary/` package is the exact canonical-section
obstruction on one nonzero preferred-chart divisor of that first component;
it is not the later complete marked-fibre strengthening.
The `component-fiber-infinity/` package is the exact canonical marked-row
section obstruction on the first-plane Schubert-infinity divisor where the
other three selected preferred Pluecker coordinates remain nonzero; it is not
the later complete marked-fibre strengthening or a whole-component theorem.
Stage 9 used batch `p5-generic-obstructions-stage9`
(mapping_sha256
`68d20c08b987c2465395ec485647dc37c958d8400a8d05dede37559256a47f23`).
Stage 10 used batch `p5-deferred-generics-stage10` (mapping_sha256
`e39d17c3ed855ef5a1342560ebf61e9b313246142f24af23940bc3ff8af472db`).
Stage 16 used batch `p5-h31-embedded-p3-stage16` (mapping_sha256
`db3bf4cc6309334ffc2a9983456f8674d9df5f22c3f921c969bcc4af414d5fb7`).
Stage 17 used batch `p5-h31-single-gate-stage17` (mapping_sha256
`7525f91818132db42c0104a366f873441118befe50c0ffcf9d676fe1c765c6a0`).
Stage 18 used batch `p5-h31-common-active-p-plus-q-stage18`
(mapping_sha256
`7595460669d3e45b4a5c12924f846d02e3dddf36385822a577b2826aebcb04d9`).
Stage 19 used batch `p5-h31-internal-e0-stage19` (mapping_sha256
`0a345a2e89974d1e7f8b026cd568d1da6ecec62b0337412b9cc9a35c7edecd6a`).
Stage 20 used batch `p5-h31-toric-marked-fibre-stage20` (mapping_sha256
`48c99b929b824d4cf5709406aa846beb4a3f47cf18f570e936910ee9408621a2`).
Stage 22 used batch `p5-h31-component-chart-boundary-stage22`
(mapping_sha256
`7130acd031ab499906c6c463298292de459ce7a60eac566a35986d40d3763837`).
Stage 23 used batch `p5-h31-component-fiber-infinity-stage23`
(mapping_sha256
`3874be216b1210251aea1150fa655e7ea5bde0c035df0d8c9d51d18b0d57a454`).

Except for the `embedded-p3/` component-closure forest, the diagonal `p+q=0`
wall subforest, the single-gate branch forest, and the internal-`E=0` divisor
leaf, toric marked-fibre boundary leaf, and canonical chart-boundary section
leaf and canonical first-plane Schubert-infinity section leaf described below,
every theorem in the generic-package table is a
**generic/function-field** statement: the marked `H31` fibre is empty at the
generic point of the named P4 component (or on a dense open subset).  Those
generic theorems do not close special divisors, projective boundaries, or the
pointwise locus.

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

## Common-active `p+q=0` wall subforest

The three triples in `common-active-binary-triangle/` form the complete
marked-`H31` subforest on the diagonal-source-torus `p+q=0` wall.  The
whole-wall theorem consumes the exceptional-lower-pair and infinity-endpoint
children together
with the separately owned P4 arc exhaustion and the already-migrated
embedded-P3 projective closure.

| scope / role | document | verifier | audit |
|---|---|---|---|
| whole diagonal `p+q=0` wall | `P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md` | `verify_p5_h31_common_active_binary_triangle_p_plus_q_boundary_obstruction.py` | `audit_p5_h31_common_active_binary_triangle_p_plus_q_boundary_obstruction.py` |
| component-15 exceptional `a=0,-1` lower-pair fibres | `P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_LOWER_PAIR_OBSTRUCTION.md` | `verify_p5_h31_common_active_binary_triangle_p_plus_q_exceptional_lower_pair_obstruction.py` | `audit_p5_h31_common_active_binary_triangle_p_plus_q_exceptional_lower_pair_obstruction.py` |
| two component-14 infinity-endpoint faces | `P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_OBSTRUCTION.md` | `verify_p5_h31_common_active_binary_triangle_p_plus_q_infinity_endpoint_obstruction.py` | `audit_p5_h31_common_active_binary_triangle_p_plus_q_infinity_endpoint_obstruction.py` |

All three results retain their exact characteristic-zero `VERIFIED` scopes.
The whole-wall and lower-pair audits are no-primary-import reconstructions.
The endpoint primary and audit share the root marked-basis matrix constructor,
so their independence is only downstream of that shared layer.  None of the
three documents has a curated theorem-ledger entry.

This package does not close weighted `H22`, non-diagonal source changes,
component placement or compactification, local-to-global gluing, or the
global conjecture.  The other 12 common-active generic, normalized,
special-divisor, and intrinsic-boundary files remain at the repository root
as separately owned sibling obligations.

## Internal `E=0` marked-fibre divisor

The triple in `internal-e0-marked-fibre/` is an exact
characteristic-zero obstruction for every marked `H31` fibre on the internal
`E=0` divisor of the first pure-compression component.  It covers both Segre
directions, `q=0,2,3`, both first-plane charts, all shifts, and all genuine
binary extension directions.

| scope | theorem | verifier | audit |
|---|---|---|---|
| complete marked fibre on the internal `E=0` divisor | `P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md` | `verify_p5_h31_internal_e0_marked_fibre.py` | `audit_p5_h31_internal_e0_marked_fibre.py` |

The `F5/F7` audit is independent only downstream of the shared toric-case and
marked-row construction; it is modular QA, not the characteristic-zero
proof.  This is a divisor leaf, not a generic or complete-component package,
and it changes no status elsewhere.  The pre-existing broader-component
status/provenance conflict is recorded without adjudication in the
[Stage 19 dry run](../../../docs/architecture/p5-h31-internal-e0-stage19-dry-run.md).
No selected artifact has a curated theorem-ledger entry.

## First-component toric marked-fibre boundary

The triple in `toric-marked-fibre/` is an exact characteristic-zero
obstruction for the complete marked `H31` fibre over the 21 genuine toric
base-orbit/orientation cases of the first pure-rank-two compression component.
It covers 17 pure-direction types, 39 direction/orientation types, both
first-plane charts, every row shift, and every binary extension direction.

| scope | theorem | verifier | audit |
|---|---|---|---|
| complete marked fibre over the first component's genuine toric base boundary | `P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md` | `verify_p5_h31_toric_marked_fibre_obstruction.py` | `audit_p5_h31_toric_marked_fibre_obstruction.py` |

The audit does not import the primary and independently recomputes modular
kernels, extension directions, and marked-minor tests.  It nevertheless
shares `toric_cases` / `marked_rows`, reused modular marked-basis primitives,
and hard-coded projection/certificate-selection data, so its independence is
only downstream of that shared construction/data layer.  The `F5/F7`
enumeration is modular QA, not the characteristic-zero proof.  This is a
boundary leaf, not a generic or complete-component package.

This leaf does not close the projective base interior, a second or further
component, component exhaustiveness, weighted `H22`, `P5 -> Delta3`, or the
global conjecture.  The pre-existing broader-component status/provenance
conflict is recorded without adjudication in the [Stage 20 dry run](../../../docs/architecture/p5-h31-toric-marked-fibre-stage20-dry-run.md).
The verifier's `additional_components_closed: false` field is scope-local.
No selected artifact has a curated theorem-ledger entry.

## First-component canonical chart-boundary section

The triple in `component-chart-boundary/` gives an exact
characteristic-zero obstruction for the displayed canonical marked-row
normal form on the nonzero all-rank-two preferred-chart divisor of the first
known pure-rank-two component.  Its parameters satisfy `A H N != 0`, with
`R` arbitrary, and it checks all four distinguished-source orientations
`q=0,1,2,3`.

| scope | theorem | verifier | audit |
|---|---|---|---|
| canonical marked sections on the nonzero preferred-chart divisor | `P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md` | `verify_p5_h31_component_chart_boundary.py` | `audit_p5_h31_component_chart_boundary.py` |

The primary is the characteristic-zero replay.  The no-primary-import audit
uses separately implemented dynamic-programming permanents and modular row
reduction over `F5/F7`; it is modular QA, not the characteristic-zero proof.
This leaf does not cover arbitrary kernel-row shifts or the complete
marked-basis fibre.  The later full marked-fibre theorem, primary, audit, and
uniquely owned elimination generator remain together as grandfathered root
debt.  Their proposed Stage 23 batch was deferred because the theorem says
fourteen certificate strata while the primary asserts and reports sixteen;
the [deferred audit](../../../docs/architecture/p5-h31-component-chart-boundary-marked-fibre-stage23-dry-run.md)
preserves that owner-gated contradiction.  This leaf is not generic, a whole-component theorem, or
component-closure evidence, and it changes no status for later components,
weighted `H22`, `P5 -> Delta3`, or the global conjecture.

The pre-existing P4 attribution conflict between internal `E=0` and this
leaf's `D=0, a!=0` chart is recorded without adjudication in the
[Stage 22 dry run](../../../docs/architecture/p5-h31-component-chart-boundary-stage22-dry-run.md).
Retargeting that link does not endorse either attribution.  No selected
artifact has a curated theorem-ledger entry.

## First-plane Schubert-infinity canonical section

The triple in `component-fiber-infinity/` gives an exact
characteristic-zero obstruction for the displayed canonical marked-row normal
form on `Delta_0(01)=0` in the first component, restricted to the locus where
the other three selected preferred Pluecker coordinates remain nonzero.  It
has `H,N != 0`, `E` arbitrary, projective fibre direction
`(A,D)!=(0,0)`, and all four distinguished-source orientations.

| scope | theorem | verifier | audit |
|---|---|---|---|
| canonical marked sections on the first-plane Schubert-infinity locus | `P5_H31_COMPONENT_FIBER_INFINITY_OBSTRUCTION.md` | `verify_p5_h31_component_fiber_infinity.py` | `audit_p5_h31_component_fiber_infinity.py` |

The primary is the characteristic-zero replay.  The audit imports no primary
or scientific/computational repository helper and separately implements a
dynamic-programming permanent, modular row reduction, and exhaustive
projective scans over `F5/F7`; its sole repository import is path-only
bootstrap after migration.  It is modular QA, not the characteristic-zero
proof.

This leaf covers only the displayed canonical marking.  The later
`P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md` family adds all
kernel-row shifts and the complete marked-basis fibre and remains together at
root as grandfathered debt pending a separately reviewed four-file batch.
Internal `E=0` and genuine toric packages separately provide complete
marked-fibre coverage on their own scoped intersections.  This leaf is not an
entire projective-boundary closure, a generic theorem, a whole-component
theorem, or component-exhaustiveness evidence.  It changes no status for a
second component, weighted `H22`, `P5 -> Delta3`, or the global conjecture.
The primary's historical `remaining_known_component_geometry` field does not
reopen the later toric closure.  No selected artifact has a curated
theorem-ledger entry.

## Single-gate obstruction forest

These three sibling packages form one complete **rank-one-gate** obstruction
forest.  They do not close the all-rank-two pure-`P4` locus or all `H31`.

| scope / role | package | document | verifier | audit |
|---|---|---|---|---|
| exact line-arrangement reduction when the other three pairs have rank two on `M` | `single-gate-p3/` | `P5_H31_SINGLE_GATE_P3_REDUCTION.md` | `verify_p5_h31_single_gate_p3_reduction.py` | `audit_p5_h31_single_gate_p3_reduction.py` |
| exact ternary exclusion of that rank-two-`M` branch | `single-gate-rank-two-m-exclusion/` | `P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md` | `verify_p5_h31_single_gate_rank_two_m_exclusion.py` | `audit_p5_h31_single_gate_rank_two_m_exclusion.py` |
| exact exclusion when another pair drops rank on `M` | `secondary-gate-exclusion/` | `P5_H31_SECONDARY_GATE_EXCLUSION.md` | `verify_p5_h31_secondary_gate_exclusion.py` | `audit_p5_h31_secondary_gate_exclusion.py` |

The first document is a reduction, not an exclusion theorem.  The latter two
are complementary characteristic-zero obstructions and together establish
only that every pure/`Delta2` H31 pencil with a rank-one row pair on its pure
hyperplane is impossible.  Their outputs retain all-rank-two H31, all `H31`,
`P5 -> Delta3`, and global resolution as false.

Each F5/F7 audit independently reimplements its corresponding primary's
calculation at the modular arithmetic and row-reduction layer and is not a
characteristic-zero proof.  The rank-two-M and secondary audits reuse helper
functions from the P3 audit, so the three audits are not mutually no-import
independent.  None of the three documents has a curated theorem-ledger entry.

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
- The internal-`E=0` and toric marked-fibre primaries and audits consume the
  shared root `derive_p5_h31_toric_marked_fibre_elimination.py` and separate
  primary/audit marked-basis constructors.  Those helpers serve multiple
  obligations and were not absorbed into either leaf package.
- The canonical chart-boundary primary consumes the separately owned P4
  chart-closure document and root rank-two-orbit theorem.  Its later complete
  marked-fibre strengthening and uniquely owned elimination generator remain
  together as grandfathered root debt pending scientific reconciliation and
  a separate migration review.
- The canonical first-plane Schubert-infinity primary consumes the separately
  owned P4 chart closure and the migrated canonical chart-boundary checkpoint.
  Its complete marked-fibre successor and uniquely consumed generator remain
  together as grandfathered root debt for a later four-file review.
- The single-gate reduction consumes the separately owned root
  `P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md`; the two importing modular
  audits expose `single-gate-p3/` through the shared bootstrap helper.
- The common-active `p+q=0` aggregate consumes the separately owned root
  `P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md` and the migrated
  `embedded-p3/` projective closure; neither dependency was re-moved.
- Already-migrated P4 anchors (components and star/pair-geometry
  classifications under [`../../p4/`](../../p4/)) are referenced by
  link and by `expose_claim_package`; they were not re-moved.
- Bare-name imports of modules inside these hyphenated package
  directories go through the shared
  `krenn_gu.bootstrap.expose_claim_package` helper
  (`src/krenn_gu/bootstrap.py`).

## Not migrated here

The H31 diagonal-quadric **elliptic** documents remain at the repository root
with their boundary forest.  The 12 common-active generic, special-divisor,
normalized-affine, and intrinsic-boundary sibling files outside the migrated
`p+q=0` wall subforest also remain at root; Stage 18 did not claim a complete
common-active component closure.  The
all-rank-two P4/H31 component and boundary forests also remain at root except
for the exact internal-`E=0` divisor, toric marked-fibre boundary, and
canonical chart-boundary and first-plane Schubert-infinity section leaves;
the single-gate forest closes only their rank-one-gate branch.  The
separate weighted-H22 embedded-P3 programme also remains at root; its
projective coverage is still open and it is not part of the closed H31
forest above.  The equal-support-sixfold package is present with its
actual primary-only evidence structure; migration did not create an
audit or promote its status.  Migration status changes no theorem
claim; the global conjecture remains **UNRESOLVED**.
