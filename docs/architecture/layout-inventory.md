# Layout inventory (pre-migration)

Starting commit: `f6d2cc426c05d99fcff08ddb1c95f3f1481a373a` (tag `pre-layout-migration-v1`).

## Headline counts

- total tracked entries: **2500**
- root-level files: **2363** (+ 3 directories = 2366 entries, GitHub truncates at 1,000)
- classified by rules: **2015** ({'medium': 1188, 'low': 444, 'high': 383})
- unclassified (need human decision): **348**

## Root files by extension

- `.py`: 1597
- `.md`: 738
- `.json`: 20
- `.cpp`: 4
- `(none)`: 2
- `.txt`: 2

## Top-level directories

- `.github/`
- `research_figures/`
- `research_snapshots/`

## Classification by destination family (top 30)

- `arbitrary-order`: 323
- `p5/frontier`: 227
- `p7`: 183
- `p4/components`: 103
- `p4/classifications`: 88
- `p4/boundaries`: 85
- `p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-b`: 43
- `p6`: 39
- `p5/h22/disjoint-mixed-star`: 35
- `finite/fourteen-vertex`: 31
- `p5/boundaries`: 31
- `p5/coordinate-cegar`: 24
- `p5/h31/common-active-binary-triangle`: 21
- `p5/h22/embedded-p3`: 20
- `p5/h31/embedded-p3`: 15
- `p5/h31/common-center-kernel-star`: 12
- `finite/eight-vertex`: 11
- `legacy`: 10
- `p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-a-exceptional-divisor`: 9
- `p5/h22/common-active-binary-triangle-p-plus-q-boundary`: 7
- `finite/ten-vertex`: 7
- `p5/h22/coincident-support`: 6
- `p5/h22/six-dimensional`: 6
- `p5/h22/two-rank-two-spoke-mixed-star`: 6
- `p5/h22/diagonal-quadric`: 4
- `p5/h31/all-rank-one-triangle`: 4
- `p5/h22/all-rank-one-triangle`: 3
- `p5/h22/common-active-binary-triangle-component-generic`: 3
- `p5/h22/common-active-binary-triangle-intrinsic-boundary`: 3
- `p5/h22/common-active-binary-triangle-p-plus-q-exceptional-fibres`: 3

## Classification by category

- `claim_script`: 1071
- `claim_document`: 679
- `tool_script`: 211
- `shared_library`: 35
- `navigation`: 6
- `withdrawn_document`: 5
- `legacy_document`: 5
- `audit_report`: 2
- `catalog`: 1

## Shared-library candidates (imported by >=3 root scripts)

- `search_witness.py`: 96 importers
- `verify_p5_h31_marked_basis_open_branch.py`: 81 importers
- `explore_random_even_cycle_forks.py`: 48 importers
- `p5_high_coordinate_tree_chart_cegar.py`: 44 importers
- `derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py`: 39 importers
- `eight_vertex_sparse_exact.py`: 33 importers
- `explore_fourteen_vertex_equality_factor_family.py`: 22 importers
- `analyze_fourteen_vertex_full_direct_motifs.py`: 21 importers
- `prism_orbit_screen.py`: 20 importers
- `rankone_support_sat.py`: 18 importers
- `explore_random_minimal_singleton_sets.py`: 17 importers
- `p5_pair_support_semantics.py`: 17 importers
- `eight_vertex_degree4_cegar.py`: 17 importers
- `verify_p5_h22_common_center_kernel_star_component_partial.py`: 17 importers
- `prism_laurent_reduction.py`: 15 importers
- `generate_p5_one_partial_support_system.py`: 14 importers
- `search_killer_patterns.py`: 13 importers
- `signed_binomial_lattice.py`: 12 importers
- `analyze_fourteen_vertex_two_even_cycle_rule_sat.py`: 12 importers
- `verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction.py`: 12 importers
- `eight_vertex_skeleton_batch.py`: 12 importers
- `search_prism_stratum.py`: 12 importers
- `eight_vertex_skeleton_laurent_batch.py`: 11 importers
- `verify_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction.py`: 11 importers
- `analyze_fourteen_vertex_c4_c4_c6_transport_rules.py`: 10 importers
- `killer_union_stratum.py`: 10 importers
- `cancellation_transport.py`: 10 importers
- `enumerate_cubic_rankone.py`: 10 importers
- `verify_p5_h22_unequal_complement_common_kernel_component_d23_pair_orbit_partial_obstruction.py`: 10 importers
- `verify_p5_pair_signature_catalogue_coverage.py`: 9 importers
- `audit_p5_h31_disjoint_mixed_star_component_generic_obstruction.py`: 9 importers
- `generate_p5_exact_three_partial_support_system.py`: 9 importers
- `verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py`: 9 importers
- `verify_p5_h22_unequal_endpoint_inward_star_component_partial.py`: 9 importers
- `analyze_fourteen_vertex_portal_determinant_lattice.py`: 8 importers
- `analyze_ten_vertex_degree_six_kotzig_port_survivors.py`: 8 importers
- `explore_p5_h22_disjoint_mixed_star_modular.py`: 8 importers
- `global_candidate_laurent_cegar.py`: 8 importers
- `minimize_p5_high_coordinate_gauge_forest.py`: 8 importers
- `verify_p5_h22_disjoint_mixed_star_component_generic_obstruction.py`: 8 importers
- `verify_p4_directed_zero_divisor_triangle_components.py`: 7 importers
- `analyze_ten_vertex_permuted_potential_survivors.py`: 7 importers
- `generate_p5_split_saturation_system.py`: 7 importers
- `candidate_matching_obstruction_sat.py`: 7 importers
- `verify_p5_component21_finite_base_extension_infinity_partial_closure.py`: 7 importers
- `verify_p5_h31_common_center_kernel_star_component_generic_obstruction.py`: 7 importers
- `audit_p5_exact_two_partial_boundary.py`: 6 importers
- `verify_laurent_batch_manifest.py`: 6 importers
- `explore_eight_vertex_degree_six_kotzig_ports.py`: 6 importers
- `enumerate_double_c4_singleton_family.py`: 6 importers
- `augment_no_binomial_amplitudes.py`: 6 importers
- `verify_p4_disjoint_mixed_star_pure_component.py`: 6 importers
- `verify_root_m7_one_edge_a10_shared_pure_mixed_factor_obstruction.py`: 6 importers
- `integer_signed_lattice.py`: 5 importers
- `odd_binomial_cycle.py`: 5 importers
- `verify_full_admissible_potential_cone.py`: 5 importers
- `audit_p5_all_full_boundary_obstruction.py`: 5 importers
- `audit_p5_h31_marked_basis_open_branch.py`: 5 importers
- `audit_p5_h31_marked_basis_fibre_classification.py`: 5 importers
- `candidate_killer_cover_sat.py`: 5 importers
- `probe_p5_q5_311_rare_slice_core.py`: 5 importers
- `generate_prism_singular.py`: 5 importers
- `eight_vertex_degree4_support.py`: 5 importers
- `verify_prism_certificates.py`: 5 importers
- `prism_orbit_batch.py`: 5 importers
- `verify_p5_high_coordinate_chart_ledgers.py`: 5 importers
- `verify_p5_h22_common_center_kernel_star_component_finite_all_marking_dense_open_supplement.py`: 5 importers
- `analyze_fourteen_vertex_even_cycle_double_pair_fork.py`: 4 importers
- `verify_fourteen_vertex_no_one_term_support.py`: 4 importers
- `analyze_fourteen_vertex_partial_circuit_factor_cegar.py`: 4 importers
- `analyze_fourteen_vertex_full_only_cycle_cover_cegar.py`: 4 importers
- `factor_lattice_cegar.py`: 4 importers
- `support_toric_degeneration.py`: 4 importers
- `audit_p5_h31_diagonal_quadric_component_point.py`: 4 importers
- `audit_p5_h31_elliptic_end_genus_two_exception.py`: 4 importers
- `derive_p5_h31_toric_marked_fibre_elimination.py`: 4 importers
- `killer_pattern_certificates.py`: 4 importers
- `verify_double_c4_singleton_family.py`: 4 importers
- `audit_p5_exact_three_partial_boundary.py`: 4 importers
- `verify_p5_c10_binary_fork_obstruction.py`: 4 importers
- `verify_p5_h22_common_center_kernel_star_component_s_zero_k_infinity_coordinate_survivor.py`: 4 importers
- `verify_p7_221_common_terminal_block_scalar_hafnian_realizability.py`: 4 importers
- `verify_p7_221_degree5_incidence_quotient_rectangle_flattening.py`: 4 importers
- `analyze_fourteen_vertex_even_cycle_factor_fork.py`: 3 importers
- `analyze_fourteen_vertex_partial_circuit_amplitude_lattice.py`: 3 importers
- `integer_constant_lattice.py`: 3 importers
- `analyze_fourteen_vertex_forced_slice_factor_cegar.py`: 3 importers
- `verify_p5_h31_elliptic_end_t2_divisor.py`: 3 importers
- `verify_p5_h31_elliptic_end_t3_divisor.py`: 3 importers
- `run_fourteen_vertex_two_even_cycle_rule_sat_incremental.py`: 3 importers
- `enumerate_killer_union_orbits.py`: 3 importers
- `verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial.py`: 3 importers
- `eight_vertex_native_kissat_laurent_batch.py`: 3 importers
- `enumerate_five_regular_double_c4_singleton_family.py`: 3 importers
- `learn_singular_fallback_clauses.py`: 3 importers
- `cover_p5_q5_311_rare_slice_supports.py`: 3 importers
- `prism_rankone_parameterization.py`: 3 importers
- `prism_support_sat.py`: 3 importers
- `search_minimal_singleton_counterexample.py`: 3 importers
- `eight_vertex_no_binomial_cegar.py`: 3 importers
- `verify_p5_c10_triangle_obstruction.py`: 3 importers
- `derive_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate.py`: 3 importers
- `verify_p5_h22_mixed_orientation_component_generic_obstruction.py`: 3 importers
- `verify_root_m7_endpoint_legal_certificate_hitting_minimum_two_exclusion.py`: 3 importers

## Markdown link health

- resolved local links: 2005
- broken local links: 0

## verify/audit triples inferred from naming: 448

## Unclassified root files: 348

See `catalog/unclassified-files.json` for the complete list.

