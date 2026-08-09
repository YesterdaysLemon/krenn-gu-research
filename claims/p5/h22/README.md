# P5 weighted-`H22` obstruction packages

Most subdirectories are migrated component-level generic weighted-`H22`
claim packages: theorem document + primary verifier + an independent audit
where one exists, moved together with preserved filenames. Scoped boundary
leaves are labelled separately below. Stage 9 used batch
`p5-generic-obstructions-stage9`
(mapping_sha256
`68d20c08b987c2465395ec485647dc37c958d8400a8d05dede37559256a47f23`).
Stage 10 used batch `p5-deferred-generics-stage10` (mapping_sha256
`e39d17c3ed855ef5a1342560ebf61e9b313246142f24af23940bc3ff8af472db`).
Stage 13 used batch `p5-h22-split-center-stage13` (mapping_sha256
`fd1d3e4163068b2e0e16f6e6161a52f822a4d02acd74bdd5e80e5bc6ba341154`).
Stage 21 used batch `p5-h22-six-dimensional-equal-weight-stage21`
(mapping_sha256
`f7427206126ecc290b0a926c1731eb5eb557aca7d784547d4c64df2dc2b41cf0`).
Stage 25 used batch `p5-h22-finite-lambda-one-all-marking-stage25`
(mapping_sha256
`611abb78c553a124a4cf02308950ec5ace6c9f5f1e2e727ece7f043f3b1f59ba`).
Stage 26 used batch `p5-h22-finite-lambda-zero-all-marking-stage26`
(mapping_sha256
`06622ad9c8ab149021fd4d3a5c412327db4a28cd2f210d339418d118a7e85131`).

Every theorem in the generic table is a **generic/function-field** statement:
the
weighted `H22` incidence is empty at the generic point of the named
P4 component (or on a dense open subset).  None closes every special
component-parameter divisor or the global pointwise locus.  Weight
scope is package-specific: the split-center package covers every finite
`[lambda:1]` weight and `[1:0]`, while other packages may leave
slope/projective boundaries open.

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
| `split-center-mixed-star/` | `P5_H22_SPLIT_CENTER_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_split_center_mixed_star_component_generic_obstruction.py` | `audit_p5_h22_split_center_mixed_star_component_generic_obstruction.py` |
| `transverse-common-factor/` | `P5_H22_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_transverse_common_factor_component_generic_obstruction.py` | `audit_p5_h22_transverse_common_factor_component_generic_obstruction.py` |
| `two-rank-two-spoke-mixed-star/` | `P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` | `verify_p5_h22_two_rank_two_spoke_mixed_star_component_generic_obstruction.py` | `audit_p5_h22_two_rank_two_spoke_mixed_star_component_generic_obstruction.py` |

## Component-23 finite lambda-zero all-marking leaf

The
[`common-center-kernel-star-component-finite-lambda-zero-all-marking/`](common-center-kernel-star-component-finite-lambda-zero-all-marking/)
package is the exact characteristic-zero obstruction over `Q(r,t)` for the
finite `lambda=0` slice and every affine marking at the generic point of the
common-center-kernel-star component. It depends load-bearingly on the prior
dense-open supplement's factor cover `h2*h3*H0=0`; its primary closes only
the three residual branches `h2=0`, `h3=0`, and `H0=0`. It does not itself
prove that factor cover or the whole generic finite theorem.

The no-repository-import audit is exact-`Q` branch-module QA at
`(r,t)=(2,4)`, where it uses the `H0=0` solution `h3=3/8`. It does not audit
the factor cover and is not an independent generic `Q(r,t)` proof. The later
ordinary-residual theorem consumes the complete `lambda=0,1,-1` slices and
the ordinary residual branches to close the generic finite case union. The
leaf's chronological `generic_finite_all_markings_closed: false` and
residual-`UNKNOWN` fields remain leaf-local and unchanged.

This leaf does not close special or projective component fibres, the whole
common-center-kernel-star component, component exhaustiveness, any separate
H31 certificate-stratum conflict, or the global conjecture.

## Component-23 finite lambda-one all-marking leaf

The
[`common-center-kernel-star-component-finite-lambda-one-all-marking/`](common-center-kernel-star-component-finite-lambda-one-all-marking/)
package is the exact characteristic-zero obstruction over `Q(r,t)` for the
finite `lambda=1` slice and every affine marking at the generic point of the
common-center-kernel-star component. It is one complete case-coverage leaf,
not a pointwise theorem for special component fibres and not by itself the
whole generic finite fibre. The later ordinary-residual theorem at repository
root combines this leaf with the complete `lambda=0,-1` slices and the
ordinary residual branches to close the generic finite case union. The
leaf's chronological `generic_finite_all_markings_closed: false` and
residual-`UNKNOWN` fields remain unchanged.

The primary's candidate-named model builder and migrated H31 row provider are
shared implementation, not promoted theorem premises. The no-repository-import
audit independently reconstructs exact `Q` at `(r,t)=(2,4)` but shares
Singular standard-basis/reduction machinery; it is exact QA, not an
independent generic `Q(r,t)` proof. Special/projective component fibres,
wider source-torus or ambient degenerations, `P5 -> Delta3`, arbitrary-order
gluing, and the global conjecture remain outside this leaf.

## Six-dimensional equal-weight normal-form point

The `six-dimensional/` package also contains the Stage 21 equal-weight
triple:

| scope | theorem | verifier | audit |
|---|---|---|---|
| binary `H22` incidence at the equal-weight `r=1` generic component function-field normal-form point | `P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md` | `verify_p5_h22_six_dimensional_equal_weight_binary_obstruction.py` | `audit_p5_h22_six_dimensional_equal_weight_binary_obstruction.py` |

This is an exact characteristic-zero obstruction over `K=C(s,d,u,v)` for
every marked basis and fifth-coordinate extension at that generic point. It
is **not** a pointwise theorem for the full geometric `r=1` divisor and is not
another generic whole-component theorem. Opposite weight `r=-1`, coupled
slope divisors, slope/parameter intersections, component-parameter and
projective boundaries, other components, all weighted `H22`, `P5 -> Delta3`,
and the global conjecture remain outside this leaf.

The audit imports no primary implementation and separately recomputes the
permanent and modular nullspaces. It nevertheless duplicates the same
theorem-specified normal form and tests one fixed admissible component sample
over each of `F5` and `F7`; its exhaustive marking censuses are modular QA,
not the characteristic-zero proof.

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
- The split-center verifier specifically imports `build_model` and
  `project` from
  `derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py`,
  and `one_marked_map` from
  `verify_p5_h31_marked_basis_open_branch.py`.  Both shared providers
  remain at the repository root pending their own ownership decisions.
- Intra-batch sibling edges: `disjoint-secant` imports its H31 sibling
  and the `full-support-tangent` H22 verifier; `full-support-tangent`
  imports its H31 sibling.  These resolve through
  `expose_claim_package` (see `src/krenn_gu/bootstrap.py`).
- Already-migrated P4 anchors under [`../../p4/`](../../p4/) are
  referenced by link and exposure helper; they were not re-moved.

## Not migrated here

Except for the scoped component-23 `lambda=0` and `lambda=1` leaves described
above, the H22 common-center-kernel-star partial theorem, its generic
case-union core and shared providers, and its special/projective/source-torus
boundary forest remain at the repository root. Their chronological and
terminal statuses are unchanged.
Unequal-complement and unequal-endpoint recursion, and embedded-p3 /
common-active-binary-triangle documents remain at the repository root with
their boundary forests or open recursion.  The split-center theorem package
is present, but its candidate-housed shared construction remains at root
pending a separate ownership decision.  The equal-support-sixfold package is present
with its actual primary-only evidence structure; migration did not create
an audit or promote its status.  Migration status changes no theorem claim;
the global conjecture remains **UNRESOLVED**.
