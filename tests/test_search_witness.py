from __future__ import annotations

import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import (  # noqa: E402
    bootstrap as _bootstrap_repository,
    expose_claim_package,
)

REPO_ROOT, HERE = _bootstrap_repository(__file__)
expose_claim_package(REPO_ROOT, "claims/finite/n06/certificate-chain")
expose_claim_package(REPO_ROOT, "claims/finite/n08")
expose_claim_package(REPO_ROOT, "claims/finite/n14")
expose_claim_package(REPO_ROOT, "tools/explore")

import itertools
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

import numpy as np

from classify_killer_union_support import (
    CASES,
    component_signature,
    parse_edges,
)
from factor_lattice_cegar import (
    eight_term_cube_factors,
    exact_lattice_conflict,
    factor_relations,
)
from enumerate_five_regular_double_c4_singleton_family import (
    enumerate_patterns as enumerate_five_regular_patterns,
    five_regular_skeletons,
)
from verify_double_c4_singleton_family import (
    canonical as canonical_double_c4_pattern,
    double_c4_factors as independent_double_c4_factors,
    one_factorizations,
    skeleton_automorphisms as double_c4_skeleton_automorphisms,
)
from eight_vertex_no_binomial_cegar import (
    first_skeleton_isomorphism,
    is_monomial_parallelogram,
    transported_family_supports,
)
from candidate_matching_obstruction_sat import (
    add_lex_leq,
    add_matching_obstruction,
    odd_group_size_patterns,
    separator_orbit_representatives,
)
from augment_forbid_mixed_singleton_matching import (
    mixed_singleton_clauses,
)
from augment_no_binomial_amplitudes import no_binomial_extension
from krenn_gu.cancellation_transport import (
    cancellation_transport_certificates,
    cube_cancellation_transport_certificates,
    cube_two_monomial_rectangle_certificates,
    support_cancellation_transport_conflict,
    support_two_monomial_rectangle_conflict,
)

from eight_vertex_degree4_support import (
    complement_edges,
    decode_graph6,
    is_four_connected,
    skeleton_matchings,
)
from krenn_gu.eight_vertex_degree4_cegar import (
    local_variable_map,
    stabilizer as degree_center_stabilizer,
    transform_flat,
)
from eight_vertex_no_binomial_cegar import (
    indicator_layout,
    indicator_variable,
    violated_no_binomial_clauses,
)
from krenn_gu.eight_vertex_sparse_exact import positive_model_literals
from global_candidate_laurent_cegar import (
    add_entry_support_symmetry_breaking,
    candidate_variable_map,
    minimum_candidate_pattern,
    symmetry_blocking_clauses,
    symmetry_transforms,
    transform_flat_entry,
)
from verify_eight_vertex_entry84_boundary import (
    audit as audit_entry84_boundary,
)
from certify_fourteen_vertex_matching_fork import (
    active_singletons as matching_fork_active_singletons,
    find_fork as find_matching_fork,
)
from analyze_fourteen_vertex_full_direct_motifs import (
    FULL_EDGES as FOURTEEN_FULL_EDGES,
    edge as fourteen_edge,
    perfect_matchings as fourteen_perfect_matchings,
)
from verify_fourteen_vertex_equality_survivor_signed_lattice import (
    active_ids as signed_lattice_active_ids,
    canonical_relation as signed_lattice_relation,
    contiguous_cycles as signed_lattice_cycles,
    cycle_edges as signed_lattice_cycle_edges,
    decode_colouring as signed_lattice_colouring,
    edge as signed_lattice_edge,
    perfect_matchings as signed_lattice_matchings,
)
from k33_support_analysis import build_problem
from krenn_gu.killer_pattern_certificates import audit_pattern
from killer_union_stratum import mutual_gauge_rank
from krenn_gu.odd_binomial_cycle import (
    cube_odd_binomial_triangle_certificates,
    matching_ratio_vector,
    odd_binomial_triangle_certificates,
)
from prism_matrix_core import (
    normalized_prism_automorphisms,
    prism_matrix_identities,
)
from krenn_gu.prism_laurent_reduction import primitive_binomial_reduction
from krenn_gu.prism_orbit_screen import (
    canonical_matching_pattern,
    clean_polynomial,
    core_rank_one_audit,
    minimal_monomial_zero_covers,
    normalized_pattern_stratum,
    prism_orbit_representatives,
)
from krenn_gu.prism_rankone_parameterization import (
    parameterize_polynomial,
    parameterized_orbit_equations,
)
from krenn_gu.rankone_support_sat import CNF
from krenn_gu.search_witness import (
    EquationSystem,
    balance_vertex_gauge,
    gradient_check,
)
from singleton_slice_minors import (
    support_singleton_slice_minor_certificate,
)
from krenn_gu.signed_binomial_lattice import (
    cube_verify_signed_binomial_lattice_certificate,
    signed_binomial_lattice_certificates,
    signed_lattice_used_equations,
    support_signed_binomial_lattice_conflict,
    verify_signed_binomial_lattice_certificate,
)
from support_toric_degeneration import (
    verify_balanced_certificate,
    verify_degeneration_certificate,
)
from krenn_gu.search_killer_patterns import active_mask_for_pattern
from krenn_gu.search_prism_stratum import (
    K33_MATCHINGS,
    PRISM_MATCHINGS,
    normalized_stratum,
)
from solve_prism_core import linear_core
from two_vertex_divisibility import all_pair_remainders
from two_vertex_quotient import audit_pair
from verify_prism_certificates import is_exact_unit_log


def factorization_weights(n: int, d: int, matchings: list[int]) -> tuple[EquationSystem, np.ndarray]:
    system = EquationSystem(n, d)
    weights = np.zeros(system.variable_count, dtype=np.complex128)
    edge_weights = system.edge_array(weights)
    for colour, matching_index in enumerate(matchings):
        for edge in system.matchings[matching_index]:
            edge_weights[system.edge_index[edge], colour, colour] = 1
    return system, weights


class EquationSystemTests(unittest.TestCase):
    def test_mixed_singleton_matching_clauses(self) -> None:
        clauses = mixed_singleton_clauses(821)
        self.assertEqual(len(clauses), 8_190)
        self.assertEqual(len(set(clauses)), len(clauses))
        system = EquationSystem(8, 3)
        first_matching = system.matchings[0]
        first_variables = {
            821 + system.edge_index[edge] * 3 + colour
            for edge in first_matching
            for colour in range(3)
        }
        first_clauses = [
            clause
            for clause in clauses
            if {abs(literal) for literal in clause}
            <= first_variables
        ]
        self.assertEqual(len(first_clauses), 3**4 - 3)
        self.assertNotIn(
            tuple(
                -(
                    821
                    + system.edge_index[edge] * 3
                    + 1
                )
                for edge in first_matching
            ),
            first_clauses,
        )

    def test_singleton_slice_minor_certificate(self) -> None:
        system = EquationSystem(4, 3)

        def entry(
            edge: tuple[int, int],
            row: int,
            column: int,
        ) -> int:
            return (
                system.edge_index[edge] * 9
                + row * 3
                + column
            )

        selected = {
            entry((0, 1), 0, 0),
            entry((0, 2), 0, 0),
            entry((1, 3), 0, 1),
            entry((0, 3), 1, 1),
            entry((1, 2), 1, 0),
        }
        certificate = support_singleton_slice_minor_certificate(
            system,
            selected,
        )
        self.assertIsNotNone(certificate)
        assert certificate is not None
        self.assertEqual(certificate["singleton_edge"], [0, 1])
        self.assertEqual(certificate["rest_colouring"], [0, 1])
        self.assertEqual(certificate["rows"], [0, 1])
        self.assertEqual(certificate["columns"], [0, 1])
        self.assertEqual(
            abs(int(certificate["surviving_coefficient"])),
            1,
        )

    def test_cancellation_transport_certificate(self) -> None:
        matchings = (
            ((0, 1), (2, 3), (4, 5)),
            ((0, 1), (2, 4), (3, 5)),
            ((0, 2), (1, 3), (4, 5)),
        )
        colourings = (
            (0, 1, 0, 1, 2, 0),
            (2, 1, 0, 1, 2, 0),
        )
        certificates = cancellation_transport_certificates(
            colourings,
            [{0, 1, 2}, {0, 1}],
            matchings,
        )
        self.assertEqual(len(certificates), 1)
        self.assertEqual(certificates[0]["changed_vertex"], 0)
        self.assertEqual(certificates[0]["common_neighbour"], 1)
        self.assertEqual(
            certificates[0]["shared_matching_indices"], [0, 1]
        )
        self.assertEqual(certificates[0]["isolated_matching_index"], 2)

        # The common-ratio argument is unavailable when the transported
        # matchings pair the changed vertex with different neighbours.
        self.assertEqual(
            cancellation_transport_certificates(
                colourings,
                [{0, 1, 2}, {0, 2}],
                matchings,
            ),
            [],
        )

    def test_support_cancellation_transport_conflict(self) -> None:
        system = EquationSystem(6, 3)
        selected = {0, 3, 9, 54, 81, 90, 118, 127}
        result = support_cancellation_transport_conflict(
            system, selected, set()
        )
        self.assertIsNotNone(result)
        assert result is not None
        positive, negative, certificate = result
        self.assertEqual(
            certificate["source_colouring"], [0, 0, 0, 0, 0, 1]
        )
        self.assertEqual(
            certificate["transport_colouring"], [1, 0, 0, 0, 0, 1]
        )
        self.assertEqual(
            certificate["shared_matching_indices"], [0, 1]
        )
        self.assertEqual(certificate["isolated_matching_index"], 3)
        replay = cube_cancellation_transport_certificates(
            system,
            [
                int(certificate["source_equation_index"]),
                int(certificate["transport_equation_index"]),
            ],
            positive,
            negative,
        )
        self.assertIn(certificate, replay)

    def test_odd_binomial_triangle_certificate(self) -> None:
        system = EquationSystem(6, 3)
        colourings = (
            (0, 0, 2, 1, 0, 0),
            (0, 1, 2, 2, 0, 0),
            (0, 2, 1, 1, 0, 0),
        )
        activity = ({1, 2}, {10, 13}, {9, 12})
        position = {
            tuple(map(int, colouring)): index
            for index, colouring in enumerate(system.colourings)
        }
        equations = [position[colouring] for colouring in colourings]
        vectors = [
            matching_ratio_vector(
                system,
                equation,
                *sorted(active),
            )
            for equation, active in zip(
                equations,
                activity,
                strict=True,
            )
        ]
        vector_sum = Counter(dict(vectors[0]))
        vector_sum.update(dict(vectors[1]))
        self.assertEqual(
            tuple(
                sorted(
                    (entry, coefficient)
                    for entry, coefficient in vector_sum.items()
                    if coefficient
                )
            ),
            vectors[2],
        )
        certificates = odd_binomial_triangle_certificates(
            system,
            equations,
            list(activity),
        )
        self.assertEqual(len(certificates), 1)
        self.assertEqual(
            set(certificates[0]["equation_indices"]),
            set(equations),
        )

        positive: set[int] = set()
        for equation, active in zip(
            equations,
            activity,
            strict=True,
        ):
            for matching in active:
                positive.update(
                    map(
                        int,
                        system.variable_ids[matching, equation, :],
                    )
                )
        zero = set(range(system.variable_count)) - positive
        replay = cube_odd_binomial_triangle_certificates(
            system,
            equations,
            positive,
            zero,
        )
        self.assertEqual(len(replay), 1)
        self.assertEqual(
            set(replay[0]["equation_indices"]),
            set(equations),
        )

    def test_signed_binomial_lattice_isolates_monomial(self) -> None:
        system = EquationSystem(6, 3)
        activity = {
            2: {0, 11, 14},
            65: {1, 2},
            146: {10, 13},
            281: {4, 5},
        }
        certificates = signed_binomial_lattice_certificates(
            system,
            sorted(activity),
            [activity[index] for index in sorted(activity)],
            maximum_certificates=1,
        )
        self.assertEqual(len(certificates), 1)
        certificate = certificates[0]
        self.assertEqual(
            certificate["certificate_mode"],
            "isolated_signed_monomial_class",
        )
        self.assertEqual(certificate["target_equation_index"], 2)
        self.assertEqual(certificate["surviving_coefficient"], 1)
        self.assertEqual(len(certificate["basis_relations"]), 3)
        verify_signed_binomial_lattice_certificate(
            system,
            activity,
            certificate,
        )
        selected: set[int] = set()
        for equation, matchings in activity.items():
            for matching in matchings:
                selected.update(
                    map(
                        int,
                        system.variable_ids[matching, equation, :],
                    )
                )
        structural_zero = set(range(system.variable_count)) - selected
        support_result = support_signed_binomial_lattice_conflict(
            system,
            selected,
            structural_zero,
        )
        self.assertIsNotNone(support_result)
        assert support_result is not None
        positive, negative, support_certificate = support_result
        cube_verify_signed_binomial_lattice_certificate(
            system,
            signed_lattice_used_equations(support_certificate),
            positive,
            negative | structural_zero,
            support_certificate,
        )

    def test_two_monomial_rectangle_conflict(self) -> None:
        system = EquationSystem(4, 3)
        first_matching = system.matchings.index(
            ((0, 1), (2, 3))
        )
        second_matching = system.matchings.index(
            ((0, 2), (1, 3))
        )
        selected: set[int] = set()
        for colouring in (
            (0, 0, 0, 0),
            (1, 0, 0, 0),
            (0, 0, 0, 2),
            (1, 0, 0, 2),
        ):
            equation_index = next(
                index
                for index, row in enumerate(system.colourings)
                if tuple(map(int, row)) == colouring
            )
            for matching_index in (
                first_matching,
                second_matching,
            ):
                selected.update(
                    map(
                        int,
                        system.variable_ids[
                            matching_index, equation_index, :
                        ],
                    )
                )
        result = support_two_monomial_rectangle_conflict(
            system,
            selected,
            set(),
        )
        self.assertIsNotNone(result)
        assert result is not None
        positive, negative, certificate = result
        self.assertEqual(certificate["changed_vertices"], [0, 3])
        self.assertEqual(certificate["alternative_colours"], [1, 2])
        self.assertEqual(
            certificate["matching_indices"],
            sorted((first_matching, second_matching)),
        )
        replay = cube_two_monomial_rectangle_certificates(
            system,
            certificate["corner_equation_indices"],
            positive,
            negative,
        )
        self.assertIn(certificate, replay)
        lattice_result = support_signed_binomial_lattice_conflict(
            system,
            selected,
            set(),
        )
        self.assertIsNotNone(lattice_result)
        assert lattice_result is not None
        lattice_positive, lattice_negative, lattice_certificate = (
            lattice_result
        )
        self.assertEqual(
            lattice_certificate["certificate_mode"],
            "annihilated_nonzero_target",
        )
        cube_verify_signed_binomial_lattice_certificate(
            system,
            signed_lattice_used_equations(lattice_certificate),
            lattice_positive,
            lattice_negative,
            lattice_certificate,
        )

    def test_isolated_rectangle_transport_conflict(self) -> None:
        system = EquationSystem(4, 3)
        first_matching = system.matchings.index(
            ((0, 1), (2, 3))
        )
        second_matching = system.matchings.index(
            ((0, 2), (1, 3))
        )
        isolated_matching = system.matchings.index(
            ((0, 3), (1, 2))
        )
        colourings = (
            (0, 0, 0, 1),
            (2, 0, 0, 1),
            (0, 0, 0, 2),
            (2, 0, 0, 2),
        )
        selected: set[int] = set()
        equation_indices = []
        for colouring in colourings:
            equation_index = next(
                index
                for index, row in enumerate(system.colourings)
                if tuple(map(int, row)) == colouring
            )
            equation_indices.append(equation_index)
            for matching_index in (
                first_matching,
                second_matching,
            ):
                selected.update(
                    map(
                        int,
                        system.variable_ids[
                            matching_index, equation_index, :
                        ],
                    )
                )
        selected.update(
            map(
                int,
                system.variable_ids[
                    isolated_matching, equation_indices[0], :
                ],
            )
        )
        result = support_two_monomial_rectangle_conflict(
            system,
            selected,
            set(),
        )
        self.assertIsNotNone(result)
        assert result is not None
        positive, negative, certificate = result
        self.assertEqual(
            certificate["certificate_mode"],
            "isolated_forbidden",
        )
        self.assertEqual(
            certificate["isolated_matching_index"],
            isolated_matching,
        )
        replay = cube_two_monomial_rectangle_certificates(
            system,
            certificate["corner_equation_indices"],
            positive,
            negative,
        )
        self.assertIn(certificate, replay)

    def test_rank_zero_laurent_reduction(self) -> None:
        _, _, unit_metadata = primitive_binomial_reduction(
            [Counter({(): 1})], ["x", "y"]
        )
        self.assertEqual(unit_metadata["binomial_rank"], 0)
        self.assertEqual(unit_metadata["unit_equation_indices"], [0])

        _, _, polynomial_metadata = primitive_binomial_reduction(
            [
                Counter(
                    {
                        (): 1,
                        ("x",): 1,
                        ("y",): 1,
                    }
                )
            ],
            ["x", "y"],
        )
        self.assertEqual(polynomial_metadata["binomial_rank"], 0)
        self.assertEqual(
            polynomial_metadata["unit_equation_indices"], []
        )
        self.assertEqual(
            polynomial_metadata["linear_monomial_unit_relations"], []
        )

        _, _, linear_metadata = primitive_binomial_reduction(
            [
                Counter(
                    {
                        ("x",): 1,
                        ("y",): 1,
                        ("z",): -1,
                        ("w",): 1,
                    }
                ),
                Counter(
                    {
                        ("x",): 1,
                        ("z",): -1,
                        ("w",): 1,
                    }
                ),
            ],
            ["w", "x", "y", "z"],
        )
        self.assertEqual(linear_metadata["unit_equation_indices"], [])
        relations = linear_metadata["linear_monomial_unit_relations"]
        self.assertTrue(relations)
        self.assertEqual(relations[0]["monomial"], ["z2"])
        self.assertEqual(
            relations[0]["output_equation_indices"], [0, 1]
        )

    def test_degree_three_center_stabilizer(self) -> None:
        system = EquationSystem(8, 3)
        fixed = {
            9 * system.edge_index[(0, neighbour)]
            + 3 * colour
            + colour
            for neighbour, colour in ((1, 0), (2, 1), (3, 2))
        }
        transforms = degree_center_stabilizer(3)
        self.assertEqual(len(transforms), 144)
        for vertices, colours in transforms:
            image = {
                transform_flat(
                    system, flat, vertices, colours
                )
                for flat in fixed
            }
            self.assertEqual(image, fixed)
        self.assertEqual(len(local_variable_map(system, 3)), 216)
        self.assertEqual(len(degree_center_stabilizer(0)), 6)
        self.assertEqual(len(local_variable_map(system, 0)), 252)
        self.assertEqual(len(degree_center_stabilizer(1)), 144)
        self.assertEqual(len(local_variable_map(system, 1)), 252)

    def test_native_kissat_model_parser(self) -> None:
        text = (
            "c solver statistics 123 456\n"
            "s SATISFIABLE\n"
            "v 1 -2 3 0\n"
            "c exit 10\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "kissat.log"
            path.write_text(text, encoding="ascii")
            self.assertEqual(
                positive_model_literals(path), {1, 3}
            )

    def test_perfect_matching_counts(self) -> None:
        self.assertEqual(len(EquationSystem(4, 2).matchings), 3)
        self.assertEqual(len(EquationSystem(6, 2).matchings), 15)

    def test_eight_vertex_cubic_complements(self) -> None:
        graph6_rows = (
            "G}GOW[",
            "G{S_g[",
            "G{O_ww",
            "GsXP_[",
            "GsXPGs",
        )
        connectivity = []
        matching_counts = []
        for row in graph6_rows:
            cubic = decode_graph6(row)
            self.assertEqual(len(cubic), 12)
            skeleton = complement_edges(8, cubic)
            self.assertEqual(len(skeleton), 16)
            self.assertEqual(
                Counter(vertex for edge in skeleton for vertex in edge),
                Counter({vertex: 4 for vertex in range(8)}),
            )
            connectivity.append(is_four_connected(8, skeleton))
            matching_counts.append(len(skeleton_matchings(8, skeleton)))
        self.assertEqual(connectivity, [True, True, False, True, True])
        self.assertEqual(matching_counts, [16, 14, 14, 16, 14])

    def test_k4_three_colour_witness(self) -> None:
        system, weights = factorization_weights(4, 3, [0, 1, 2])
        diagnostic = system.diagnostics(system.amplitudes(weights))
        self.assertEqual(diagnostic["max_abs_residual"], 0)

    def test_c6_two_colour_witness(self) -> None:
        system = EquationSystem(6, 2)
        weights = np.zeros(system.variable_count, dtype=np.complex128)
        edge_weights = system.edge_array(weights)
        cycle_matchings = (
            ((0, 1), (2, 3), (4, 5)),
            ((0, 5), (1, 2), (3, 4)),
        )
        for colour, matching in enumerate(cycle_matchings):
            for edge in matching:
                edge_weights[system.edge_index[edge], colour, colour] = 1
        diagnostic = system.diagnostics(system.amplitudes(weights))
        self.assertEqual(diagnostic["max_abs_residual"], 0)

    def test_complex_gradient(self) -> None:
        gradient_check(EquationSystem(4, 3), seed=17)

    def test_vertex_gauge_preserves_amplitudes(self) -> None:
        system = EquationSystem(6, 3)
        rng = np.random.default_rng(23)
        weights = rng.standard_normal(system.variable_count) + 1j * rng.standard_normal(
            system.variable_count
        )
        balanced = balance_vertex_gauge(system, weights)
        np.testing.assert_allclose(
            system.amplitudes(weights),
            system.amplitudes(balanced),
            rtol=1e-12,
            atol=1e-12,
        )
        self.assertLessEqual(np.linalg.norm(balanced), np.linalg.norm(weights) + 1e-12)

    def test_two_vertex_divisibility_on_k4_witness(self) -> None:
        system, weights = factorization_weights(4, 3, [0, 1, 2])
        results = all_pair_remainders(system, weights)
        self.assertLess(
            max(float(result["remainder_norm"]) for result in results),
            1e-12,
        )

    def test_two_vertex_quotient_on_k4_witness(self) -> None:
        system, weights = factorization_weights(4, 3, [0, 1, 2])
        rng = np.random.default_rng(19)
        for p in range(system.n):
            for q in range(p + 1, system.n):
                result = audit_pair(system, weights, p, q, 10, rng)
                self.assertLess(
                    float(result["max_quotient_residual"]), 1e-10
                )

    def test_killer_pattern_mask_orientation(self) -> None:
        system = EquationSystem(6, 3)
        pattern = [
            [1, 2, 3],
            [0, 2, 3],
            [0, 1, 3],
            [0, 1, 2],
            [0, 1, 2],
            [0, 1, 2],
        ]
        mask = active_mask_for_pattern(system, pattern)
        blocks = system.edge_array(mask)
        # 0 -> 1 with colour 0: canonical columns 1 and 2 are forbidden.
        self.assertTrue(np.all(blocks[system.edge_index[(0, 1)]][:, 1:] == 0))
        # 1 -> 0 with colour 0: canonical rows 1 and 2 are forbidden.
        self.assertTrue(np.all(blocks[system.edge_index[(0, 1)]][1:, :] == 0))

    def test_normalized_prism_stratum(self) -> None:
        system = EquationSystem(6, 3)
        fixed, active = normalized_stratum(system)
        self.assertEqual(int(np.sum(active)), 54)

        # Every fixed singleton must be structurally allowed by the same
        # directed killer pattern.  This catches row/column reversal.
        for flat_pattern in prism_orbit_representatives()[::100]:
            orbit_fixed, _ = normalized_pattern_stratum(
                system,
                flat_pattern,
            )
            orbit_active = active_mask_for_pattern(
                system,
                [
                    list(
                        flat_pattern[
                            3 * vertex : 3 * vertex + 3
                        ]
                    )
                    for vertex in range(6)
                ],
            )
            self.assertTrue(
                all(
                    orbit_active[int(index)]
                    for index in np.flatnonzero(orbit_fixed)
                )
            )
        self.assertEqual(int(np.count_nonzero(fixed)), 9)
        amplitudes = system.amplitudes(fixed)
        monochromatic = system.target.astype(bool)
        np.testing.assert_array_equal(
            amplitudes[monochromatic], np.ones(3)
        )
        self.assertEqual(
            int(np.count_nonzero(amplitudes[~monochromatic])), 1
        )
        rows, indices = linear_core(system, fixed, active)
        self.assertEqual(len(rows), 54)
        self.assertEqual(len(indices), 54)

        k33_fixed, k33_active = normalized_stratum(
            system, K33_MATCHINGS
        )
        self.assertEqual(int(np.sum(k33_active)), 54)
        k33_amplitudes = system.amplitudes(k33_fixed)
        self.assertEqual(
            int(np.count_nonzero(k33_amplitudes[~monochromatic])), 3
        )

    def test_prism_matrix_core_identities(self) -> None:
        system = EquationSystem(6, 3)
        fixed, active = normalized_stratum(system)
        rng = np.random.default_rng(41)
        weights = fixed.copy()
        weights[active] = rng.standard_normal(int(np.sum(active))) + 1j * rng.standard_normal(
            int(np.sum(active))
        )

        expected = np.zeros(system.variable_count, dtype=np.complex128)
        for identity in prism_matrix_identities(system, weights):
            edge_index = system.edge_index[identity.edge]
            expected[edge_index * 9 : (edge_index + 1) * 9] = (
                identity.residual.ravel()
            )

        rows, indices = linear_core(system, fixed, active)
        _, jacobian_at_zero = system.residual_and_jacobian(fixed)
        linear_jacobian = jacobian_at_zero[np.ix_(rows, indices)]
        row_variables = np.argmax(np.abs(linear_jacobian), axis=1)
        amplitudes = system.amplitudes(weights)
        np.testing.assert_allclose(
            amplitudes[rows],
            expected[indices[row_variables]],
            rtol=1e-12,
            atol=1e-12,
        )

        automorphisms = normalized_prism_automorphisms(system, fixed)
        self.assertEqual(len(automorphisms), 12)
        complement_edge_orbit = {
            tuple(sorted((vertices[0], vertices[4])))
            for vertices, _ in automorphisms
        }
        self.assertEqual(
            complement_edge_orbit,
            {(0, 4), (0, 5), (1, 2), (1, 3), (2, 5), (3, 4)},
        )

    def test_prism_half_edge_orbits(self) -> None:
        representatives = prism_orbit_representatives()
        self.assertEqual(len(representatives), 718)
        canonical = canonical_matching_pattern()
        self.assertEqual(representatives.index(canonical), 268)

        system = EquationSystem(6, 3)
        expected_fixed, expected_active = normalized_stratum(system)
        fixed, active = normalized_pattern_stratum(system, canonical)
        np.testing.assert_array_equal(fixed, expected_fixed)
        np.testing.assert_array_equal(active, expected_active)
        audit = core_rank_one_audit(system, canonical)
        self.assertTrue(audit["passes"])
        self.assertEqual(len(audit["lambdas"]), 6)
        self.assertEqual(
            [len(minimal_monomial_zero_covers(matrix)) for matrix in audit["remainder_matrices"]],
            [3] * 6,
        )

    def test_rank_one_parameterization(self) -> None:
        polynomial = Counter(
            {
                ("x0", "x17"): 2,
                ("x53",): -1,
                (): 3,
            }
        )
        self.assertEqual(
            parameterize_polynomial(polynomial),
            Counter(
                {
                    ("u0", "u5", "v0", "v5"): 2,
                    ("u17", "v17"): -1,
                    (): 3,
                }
            ),
        )
        names, equations = parameterized_orbit_equations(
            EquationSystem(6, 3), canonical_matching_pattern()
        )
        self.assertEqual(len(names), 36)
        self.assertEqual(len(equations), 726)

    def test_clean_polynomial_preserves_signed_coefficients(self) -> None:
        polynomial = Counter(
            {
                ("x0",): 2,
                ("x1",): -3,
                ("cancelled",): 0,
            }
        )
        self.assertEqual(
            clean_polynomial(polynomial),
            Counter({("x0",): 2, ("x1",): -3}),
        )

    def test_candidate_cover_matching_identity(self) -> None:
        candidates = candidate_variable_map()
        flat_pattern = canonical_matching_pattern()
        pattern = [
            list(flat_pattern[3 * vertex : 3 * vertex + 3])
            for vertex in range(6)
        ]
        model = {
            candidates[(vertex, colour, neighbour)]
            for vertex, row in enumerate(pattern)
            for colour, neighbour in enumerate(row)
        }
        selected, cover = minimum_candidate_pattern(model, candidates)
        self.assertEqual(selected, pattern)
        self.assertEqual(len(cover), 9)

        mutual_edges, gauge_rank = mutual_gauge_rank(
            EquationSystem(6, 3),
            pattern,
        )
        self.assertEqual(mutual_edges, 9)
        self.assertEqual(gauge_rank, 9)

    def test_global_symmetry_entry_and_clause_images(self) -> None:
        system = EquationSystem(6, 3)
        candidates = candidate_variable_map()
        vertex_permutation = (5, 3, 1, 4, 2, 0)
        colour_permutation = (2, 0, 1)
        inverse_vertices = tuple(
            vertex_permutation.index(vertex) for vertex in range(6)
        )
        inverse_colours = tuple(
            colour_permutation.index(colour) for colour in range(3)
        )
        for flat_index in range(system.variable_count):
            transformed = transform_flat_entry(
                system,
                flat_index,
                vertex_permutation,
                colour_permutation,
            )
            restored = transform_flat_entry(
                system,
                transformed,
                inverse_vertices,
                inverse_colours,
            )
            self.assertEqual(restored, flat_index)

        weights = (
            np.arange(system.variable_count, dtype=np.float64)
            + 1j * np.arange(
                system.variable_count,
                2 * system.variable_count,
                dtype=np.float64,
            )
        )
        transformed_weights = np.zeros_like(weights)
        for flat_index, value in enumerate(weights):
            transformed_weights[
                transform_flat_entry(
                    system,
                    flat_index,
                    vertex_permutation,
                    colour_permutation,
                )
            ] = value
        colouring = (0, 2, 1, 1, 0, 2)
        transformed_colouring = [0] * 6
        for vertex, colour in enumerate(colouring):
            transformed_colouring[vertex_permutation[vertex]] = (
                colour_permutation[colour]
            )
        original_index = next(
            index
            for index, item in enumerate(system.colourings)
            if tuple(int(value) for value in item) == colouring
        )
        transformed_index = next(
            index
            for index, item in enumerate(system.colourings)
            if tuple(int(value) for value in item)
            == tuple(transformed_colouring)
        )
        np.testing.assert_allclose(
            system.amplitudes(weights)[original_index],
            system.amplitudes(transformed_weights)[transformed_index],
        )

        clauses = symmetry_blocking_clauses(
            system,
            candidates,
            {(0, 0, 1), (1, 1, 0)},
            {0, 17},
            {53},
            symmetry_transforms("full"),
        )
        self.assertIn(
            (
                -candidates[(0, 0, 1)],
                -candidates[(1, 1, 0)],
                -1,
                -18,
                54,
            ),
            clauses,
        )
        self.assertLessEqual(len(clauses), 4_320)

        cnf = CNF()
        for _ in range(system.variable_count):
            cnf.variable()
        added = add_entry_support_symmetry_breaking(
            cnf,
            system,
            symmetry_transforms("generators"),
        )
        self.assertGreater(added, 0)
        globally_least = min(
            tuple(
                flat_index in {
                    transform_flat_entry(
                        system,
                        original,
                        vertices,
                        colours,
                    )
                    for original in {0, 7, 22, 61, 134}
                }
                for flat_index in range(system.variable_count)
            )
            for vertices, colours in symmetry_transforms("full")
        )
        from pysat.solvers import Cadical195

        assumptions = [
            flat_index + 1 if value else -(flat_index + 1)
            for flat_index, value in enumerate(globally_least)
        ]
        with Cadical195(bootstrap_with=cnf.clauses) as solver:
            self.assertTrue(solver.solve(assumptions=assumptions))

    def test_tutte_obstruction_encoding(self) -> None:
        from pysat.solvers import Cadical195

        tasks = tuple(
            (vertex, colour)
            for vertex in range(6)
            for colour in range(3)
        )

        def fixed_candidate_cnf(
            selected_arcs: set[tuple[int, int, int]],
            separator_size: int,
            group_sizes: tuple[int, ...] | None = None,
            maximum_matching: int = 5,
        ) -> CNF:
            cnf = CNF()
            candidates = {
                (vertex, colour, neighbour): cnf.variable()
                for vertex, colour in tasks
                for neighbour in range(6)
                if neighbour != vertex
            }
            for arc, variable in candidates.items():
                cnf.add(variable if arc in selected_arcs else -variable)
            add_matching_obstruction(
                cnf,
                candidates,
                tasks,
                separator_size,
                group_sizes,
                maximum_matching,
            )
            return cnf

        empty = fixed_candidate_cnf(set(), 0)
        with Cadical195(bootstrap_with=empty.clauses) as solver:
            self.assertTrue(solver.solve())

        flat_pattern = canonical_matching_pattern()
        perfect_matching_arcs = {
            (
                vertex,
                colour,
                flat_pattern[3 * vertex + colour],
            )
            for vertex, colour in tasks
        }
        for separator_size in range(6):
            cnf = fixed_candidate_cnf(
                perfect_matching_arcs,
                separator_size,
            )
            with Cadical195(bootstrap_with=cnf.clauses) as solver:
                self.assertFalse(solver.solve())

        for group_sizes in odd_group_size_patterns(4):
            empty = fixed_candidate_cnf(set(), 4, group_sizes)
            with Cadical195(bootstrap_with=empty.clauses) as solver:
                self.assertTrue(solver.solve())
            perfect = fixed_candidate_cnf(
                perfect_matching_arcs,
                4,
                group_sizes,
            )
            with Cadical195(bootstrap_with=perfect.clauses) as solver:
                self.assertFalse(solver.solve())

        matching_seven_sizes = odd_group_size_patterns(7, 7)[0]
        empty = fixed_candidate_cnf(
            set(),
            7,
            matching_seven_sizes,
            7,
        )
        with Cadical195(bootstrap_with=empty.clauses) as solver:
            self.assertTrue(solver.solve())
        perfect = fixed_candidate_cnf(
            perfect_matching_arcs,
            7,
            matching_seven_sizes,
            7,
        )
        with Cadical195(bootstrap_with=perfect.clauses) as solver:
            self.assertFalse(solver.solve())

        self.assertEqual(
            [
                len(odd_group_size_patterns(separator_size))
                for separator_size in range(6)
            ],
            [19, 12, 7, 4, 2, 1],
        )
        self.assertEqual(len(separator_orbit_representatives(5)), 18)

    def test_boolean_lex_encoding(self) -> None:
        from pysat.solvers import Cadical195

        cnf = CNF()
        first = [cnf.variable() for _ in range(3)]
        second = [cnf.variable() for _ in range(3)]
        add_lex_leq(cnf, first, second)
        with Cadical195(bootstrap_with=cnf.clauses) as solver:
            for first_values in itertools.product((False, True), repeat=3):
                for second_values in itertools.product(
                    (False, True),
                    repeat=3,
                ):
                    assumptions = [
                        variable if value else -variable
                        for variable, value in zip(
                            [*first, *second],
                            [*first_values, *second_values],
                        )
                    ]
                    self.assertEqual(
                        solver.solve(assumptions=assumptions),
                        first_values <= second_values,
                    )

    def test_sequential_at_most_encoding(self) -> None:
        from pysat.solvers import Cadical195

        from eight_vertex_local_degree4_support import add_at_most

        for variable_count in range(1, 7):
            for bound in range(variable_count + 1):
                cnf = CNF()
                variables = [
                    cnf.variable() for _ in range(variable_count)
                ]
                add_at_most(cnf, variables, bound)
                with Cadical195(
                    bootstrap_with=cnf.clauses
                ) as solver:
                    for values in itertools.product(
                        (False, True), repeat=variable_count
                    ):
                        assumptions = [
                            variable if value else -variable
                            for variable, value in zip(
                                variables, values
                            )
                        ]
                        self.assertEqual(
                            solver.solve(assumptions=assumptions),
                            sum(values) <= bound,
                        )

    def test_no_binomial_cegar_clause(self) -> None:
        system = EquationSystem(4, 3)
        indicator_count = (
            len(system.colourings) * len(system.matchings)
        )
        indicator_first, observed_count = indicator_layout(
            system, 99 + indicator_count
        )
        self.assertEqual(indicator_first, 100)
        self.assertEqual(observed_count, indicator_count)

        colouring_index = next(
            index
            for index, target in enumerate(system.target)
            if not target
        )
        variables = [
            indicator_variable(
                indicator_first,
                len(system.matchings),
                colouring_index,
                matching_index,
            )
            for matching_index in range(len(system.matchings))
        ]
        positive = {variables[0], variables[2]}
        clauses, records = violated_no_binomial_clauses(
            system, positive, indicator_first
        )
        self.assertEqual(len(clauses), 1)
        self.assertEqual(records[0]["matching_indices"], [0, 2])
        clause = clauses[0]

        def satisfied(selected: set[int]) -> bool:
            return any(
                literal > 0 and literal in selected
                or literal < 0 and -literal not in selected
                for literal in clause
            )

        self.assertFalse(satisfied({variables[0], variables[2]}))
        self.assertTrue(satisfied(set()))
        self.assertTrue(satisfied({variables[0]}))
        self.assertTrue(satisfied(set(variables)))

    def test_static_no_binomial_counter(self) -> None:
        from pysat.solvers import Cadical195

        indicators = [1, 2, 3, 4]
        clauses, _top_id, _selector = no_binomial_extension(
            indicators, top_id=4
        )
        with Cadical195(bootstrap_with=clauses) as solver:
            for values in itertools.product(
                (False, True), repeat=len(indicators)
            ):
                assumptions = [
                    variable if value else -variable
                    for variable, value in zip(
                        indicators, values, strict=True
                    )
                ]
                self.assertEqual(
                    solver.solve(assumptions=assumptions),
                    sum(values) == 0 or sum(values) >= 3,
                )

    def test_support_toric_certificates(self) -> None:
        system = EquationSystem(2, 3)
        balanced = {
            "mode": "balanced_support",
            "entry_weights": [1, 1, 1],
            "colour_degrees": [1, 1, 1],
        }
        result = verify_balanced_certificate(
            system, [0, 4, 8], balanced
        )
        self.assertTrue(result["verified"])

        degeneration = {
            "mode": "support_degeneration",
            "potentials": [[1, 0, 0], [-1, 0, 0]],
            "deleted_entries": [1],
        }
        result = verify_degeneration_certificate(
            system, [1], degeneration
        )
        self.assertTrue(result["verified"])
        self.assertEqual(result["deleted_entries"], 1)

    def test_eight_vertex_exact_equations_keep_required_sign(self) -> None:
        from krenn_gu.eight_vertex_sparse_exact import exact_equations

        system = EquationSystem(4, 3)
        variable_names = {
            index: f"x{index}"
            for index in range(system.variable_count)
        }
        equations = exact_equations(system, variable_names)
        required = [
            polynomial
            for polynomial in equations
            if () in polynomial
        ]
        self.assertEqual(len(required), 3)
        self.assertTrue(
            all(polynomial[()] == -1 for polynomial in required)
        )

    def test_minisat_model_parser_accepts_sat_header(self) -> None:
        from krenn_gu.eight_vertex_sparse_exact import positive_model_literals

        with tempfile.TemporaryDirectory() as directory:
            model = Path(directory) / "model.txt"
            model.write_text("SAT\n1 -2 3 0\n", encoding="ascii")
            self.assertEqual(positive_model_literals(model), {1, 3})

    def test_unique_mixed_matching_certificate(self) -> None:
        system = EquationSystem(6, 3)
        eliminated_pattern = [
            [4, 3, 1],
            [5, 2, 3],
            [1, 0, 5],
            [2, 5, 1],
            [0, 1, 2],
            [2, 3, 0],
        ]
        result = audit_pattern(system, eliminated_pattern)
        self.assertEqual(result["status"], "combinatorially_eliminated")

        prism_pattern = [[-1, -1, -1] for _ in range(6)]
        for colour, matching in enumerate(PRISM_MATCHINGS):
            for first, second in matching:
                prism_pattern[first][colour] = second
                prism_pattern[second][colour] = first
        result = audit_pattern(system, prism_pattern)
        self.assertEqual(result["status"], "requires_algebraic_analysis")

    def test_k33_support_certificate(self) -> None:
        groups, constant_equations = build_problem()
        self.assertEqual(len(constant_equations), 3)
        self.assertEqual(
            constant_equations[0].terms,
            ((44, 51), (2, 29), (12, 21)),
        )
        self.assertEqual(
            constant_equations[1].terms,
            ((34, 52), (26, 6), (13, 40)),
        )

        forbidden_pairs = {
            tuple(sorted(abs(literal) for literal in group.clauses[0]))
            for group in groups
            if len(group.clauses) == 1
        }
        for first_term in constant_equations[0].terms:
            for second_term in constant_equations[1].terms:
                self.assertTrue(
                    any(
                        tuple(sorted((first, second))) in forbidden_pairs
                        for first in first_term
                        for second in second_term
                    )
                )

    def test_killer_union_complement_classification(self) -> None:
        all_edges = tuple(itertools.combinations(range(6), 2))
        expected_by_missing_count: dict[
            int, set[tuple[tuple[str, int], ...]]
        ] = {}
        for edge_text in CASES.values():
            missing = parse_edges(edge_text)
            expected_by_missing_count.setdefault(len(missing), set()).add(
                component_signature(missing)
            )

        self.assertEqual(
            {count: len(signatures) for count, signatures in expected_by_missing_count.items()},
            {3: 4, 4: 5, 5: 4, 6: 2},
        )
        for missing_count, expected in expected_by_missing_count.items():
            observed = set()
            for raw_edges in itertools.combinations(all_edges, missing_count):
                degrees = [0] * 6
                for first, second in raw_edges:
                    degrees[first] += 1
                    degrees[second] += 1
                if max(degrees) <= 2:
                    observed.add(component_signature(frozenset(raw_edges)))
            self.assertEqual(observed, expected)

    def test_exact_unit_log_parser(self) -> None:
        valid = "GB_SIZE\n1\nREDUCE_ONE\nr\n0\nAuf Wiedersehen.\n"
        self.assertTrue(is_exact_unit_log(valid))
        self.assertFalse(is_exact_unit_log(valid.replace("\n0\n", "\nx1\n")))

    def test_four_term_factor_lattice_isolation(self) -> None:
        class DummySystem:
            target = [False, False]

        rectangle = [
            (1, 0, 1, 0),
            (1, 0, 0, 1),
            (0, 1, 1, 0),
            (0, 1, 0, 1),
        ]
        activities = [
            [0, 1, 2, 3],
            [0, 1, 2, 3, 4],
        ]
        monomials = [
            rectangle,
            [*rectangle, (0, 0, 0, 0)],
        ]
        clauses, relations, origins = factor_relations(
            DummySystem(),  # type: ignore[arg-type]
            activities,
            monomials,
        )
        self.assertEqual(clauses, [(1, 2)])
        self.assertEqual(len(relations), 2)
        self.assertEqual(len(origins), 2)
        conflict = exact_lattice_conflict(
            DummySystem(),  # type: ignore[arg-type]
            [0, 1],
            relations,
            activities,
            monomials,
        )
        self.assertIsNotNone(conflict)
        assert conflict is not None
        self.assertEqual(
            conflict["certificate_mode"],
            "isolated_factor_lattice_class",
        )
        self.assertEqual(conflict["target_equation_index"], 1)

    def test_eight_term_laurent_cube_clause(self) -> None:
        class DummySystem:
            target = [False]

        cube = [
            tuple((mask >> axis) & 1 for axis in range(3))
            for mask in range(8)
        ]
        factors = eight_term_cube_factors(cube)
        self.assertIsNotNone(factors)
        assert factors is not None
        self.assertEqual(len(factors), 3)
        clauses, relations, origins = factor_relations(
            DummySystem(),  # type: ignore[arg-type]
            [list(range(8))],
            [cube],
            include_eight_term_cubes=True,
        )
        self.assertEqual(len(clauses), 1)
        self.assertEqual(len(clauses[0]), 3)
        self.assertEqual(len(relations), 3)
        self.assertTrue(
            all(
                origin["certificate_mode"]
                == "eight_term_laurent_cube"
                for origin in origins
            )
        )

    def test_monomial_parallelogram_detection(self) -> None:
        class DummySystem:
            variable_ids = np.asarray(
                [
                    [[0, 2]],
                    [[0, 3]],
                    [[1, 2]],
                    [[1, 3]],
                ],
                dtype=int,
            )

        self.assertTrue(
            is_monomial_parallelogram(
                DummySystem(),  # type: ignore[arg-type]
                0,
                [0, 1, 2, 3],
            )
        )
        DummySystem.variable_ids[3, 0, 1] = 4
        self.assertFalse(
            is_monomial_parallelogram(
                DummySystem(),  # type: ignore[arg-type]
                0,
                [0, 1, 2, 3],
            )
        )

    def test_double_c4_singleton_family_enumeration(self) -> None:
        skeleton = frozenset(
            {
                (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                (1, 2), (1, 3), (1, 4), (1, 5),
                (2, 3), (2, 6), (2, 7),
                (3, 6), (3, 7),
                (4, 5), (4, 6), (4, 7),
                (5, 6), (5, 7),
                (6, 7),
            }
        )
        edges = sorted(skeleton)
        factors = independent_double_c4_factors(skeleton, 8)
        automorphisms = double_c4_skeleton_automorphisms(skeleton, 8)
        patterns: set[tuple[int, ...]] = set()
        for factor in factors:
            for factorization in one_factorizations(
                skeleton - factor,
                8,
            ):
                labels = {edge: 3 for edge in factor}
                for colour, matching in enumerate(factorization):
                    for edge in matching:
                        labels[edge] = colour
                patterns.add(tuple(labels[edge] for edge in edges))
        representatives = {
            canonical_double_c4_pattern(
                pattern,
                edges,
                automorphisms,
            )
            for pattern in patterns
        }
        self.assertEqual(len(factors), 34)
        self.assertEqual(len(automorphisms), 128)
        self.assertEqual(len(patterns), 108)
        self.assertEqual(len(representatives), 10)

    def test_all_five_regular_double_c4_families(self) -> None:
        reference = frozenset(
            {
                (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                (1, 2), (1, 3), (1, 4), (1, 5),
                (2, 3), (2, 6), (2, 7),
                (3, 6), (3, 7),
                (4, 5), (4, 6), (4, 7),
                (5, 6), (5, 7),
                (6, 7),
            }
        )
        system = EquationSystem(8, 3)
        observed: dict[str, tuple[int, int, int]] = {}
        for type_name, skeleton in five_regular_skeletons(reference):
            factors, patterns = enumerate_five_regular_patterns(
                system,
                skeleton,
            )
            edges = sorted(skeleton)
            automorphisms = double_c4_skeleton_automorphisms(
                skeleton,
                8,
            )
            representatives = {
                canonical_double_c4_pattern(
                    pattern,
                    edges,
                    automorphisms,
                )
                for pattern in patterns
            }
            observed[type_name] = (
                len(factors),
                len(patterns),
                len(representatives),
            )
        self.assertEqual(
            observed,
            {
                "c8": (23, 43, 12),
                "c5_c3": (15, 30, 1),
                "c4_c4": (34, 108, 10),
            },
        )

    def test_family_supports_transport_to_relabelled_role(self) -> None:
        reference = frozenset(
            {
                (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                (1, 2), (1, 3), (1, 4), (1, 5),
                (2, 3), (2, 6), (2, 7),
                (3, 6), (3, 7),
                (4, 5), (4, 6), (4, 7),
                (5, 6), (5, 7),
                (6, 7),
            }
        )
        system = EquationSystem(8, 3)
        _factors, unlabelled = enumerate_five_regular_patterns(
            system,
            reference,
        )
        labelled = {
            tuple(
                3 if label == 3 else permutation[label]
                for label in pattern
            )
            for pattern in unlabelled
            for permutation in itertools.permutations(range(3))
        }
        permutation = (6, 2, 5, 0, 7, 3, 1, 4)
        target = frozenset(
            tuple(sorted((permutation[first], permutation[second])))
            for first, second in reference
        )
        self.assertIsNotNone(
            first_skeleton_isomorphism(reference, target, 8)
        )
        supports = transported_family_supports(
            [(reference, tuple(sorted(labelled)))],
            target,
            system,
        )
        self.assertEqual(len(labelled), 648)
        self.assertEqual(len(supports), 648)
        self.assertEqual({len(support) for support in supports}, {84})

    def test_exact20_entry84_boundary(self) -> None:
        payload = audit_entry84_boundary()
        self.assertTrue(payload["verified"])
        self.assertEqual(payload["maximum_entries"], 84)
        self.assertEqual(
            payload["local_assignments_with_all_required_backups"],
            {
                str(full_degree): [[0, 1, 2]]
                for full_degree in range(5)
            },
        )

    def test_fourteen_vertex_matching_fork_activation(self) -> None:
        path = (
            REPO_ROOT
            / "tmp"
            / "fourteen_vertex_direct_free_search_p500000_multiswitch.json"
        )
        candidate = json.loads(path.read_text(encoding="utf-8"))
        singleton_matchings = [
            tuple(
                fourteen_edge(*map(int, item))
                for item in matching
            )
            for matching in candidate["best_singleton_matchings"]
        ]
        labels = {
            item: colour
            for colour, matching in enumerate(singleton_matchings)
            for item in matching
        }
        matchings = fourteen_perfect_matchings(
            set(FOURTEEN_FULL_EDGES) | set(labels)
        )
        certificate = find_matching_fork(
            matchings,
            set(FOURTEEN_FULL_EDGES),
            labels,
            singleton_matchings,
        )
        self.assertIsNotNone(certificate)
        assert certificate is not None
        sparse = tuple(certificate["sparse_colouring"])
        rich = tuple(certificate["rich_colouring"])
        target = {
            tuple(item) for item in certificate["singleton_target"]
        }
        removed = tuple(certificate["removed_singleton_edge"])
        self.assertEqual(
            matching_fork_active_singletons(sparse, labels),
            frozenset(target - {removed}),
        )
        self.assertEqual(
            matching_fork_active_singletons(rich, labels),
            frozenset(target),
        )
        self.assertEqual(
            sum(left != right for left, right in zip(sparse, rich)),
            1,
        )
        self.assertEqual(len(certificate["sparse_activity"]), 2)
        self.assertEqual(len(certificate["rich_activity"]), 3)

    def test_fourteen_vertex_signed_lattice_reconstruction(self) -> None:
        root = REPO_ROOT
        orbit_manifest = json.loads(
            (
                root
                / "tmp"
                / "fourteen_vertex_c3_c5_c6_fork5_survivor_orbits.json"
            ).read_text(encoding="utf-8")
        )
        analysis = json.loads(
            (
                root
                / "tmp"
                / "fourteen_vertex_c3_c5_c6_fork5_orbit0_signed_lattice.json"
            ).read_text(encoding="utf-8")
        )
        survivor = orbit_manifest["survivors"][0]
        cycles = signed_lattice_cycles(orbit_manifest["partition"])
        full_edges = set().union(
            *(
                signed_lattice_cycle_edges(cycle)
                for cycle in cycles
            )
        )
        singleton_matchings = [
            tuple(
                signed_lattice_edge(*map(int, item))
                for item in survivor[key]
            )
            for key in ("first", "second", "third")
        ]
        labels = {
            item: colour
            for colour, matching in enumerate(singleton_matchings)
            for item in matching
        }
        matchings = signed_lattice_matchings(
            full_edges | set(labels)
        )
        certificate = analysis["certificate"]
        reconstructed: Counter[int] = Counter()
        coordinate_sum = 0
        for position, coefficient in certificate[
            "basis_coordinates"
        ]:
            record = analysis["basis_relations"][int(position)]
            colouring = signed_lattice_colouring(
                int(record["origin_equation_index"])
            )
            activity = signed_lattice_active_ids(
                matchings, colouring, full_edges, labels
            )
            self.assertEqual(len(activity), 2)
            signature = signed_lattice_relation(
                matchings[activity[0]],
                matchings[activity[1]],
                colouring,
                full_edges,
                labels,
            )
            self.assertEqual(
                signature,
                tuple(
                    tuple(map(int, item))
                    for item in record["signature"]
                ),
            )
            for variable, value in signature:
                reconstructed[variable] += int(coefficient) * value
            coordinate_sum += int(coefficient)
        reconstructed = Counter(
            {
                variable: value
                for variable, value in reconstructed.items()
                if value
            }
        )
        target = Counter(
            {
                int(variable): int(value)
                for variable, value in certificate[
                    "target_relation_signature"
                ]
            }
        )
        self.assertEqual(reconstructed, target)
        self.assertEqual(coordinate_sum % 2, 1)

    def test_fourteen_vertex_c14_rectangle_audit(self) -> None:
        payload = json.loads(
            (
                REPO_ROOT
                / "tmp"
                / "fourteen_vertex_c14_rectangle_theorem_verified.json"
            ).read_text(encoding="utf-8")
        )
        self.assertTrue(payload["verified"])
        self.assertEqual(payload["eligible_c14_singleton_factors"], 44189)
        self.assertEqual(payload["minimum_crossing_chords"], 1)
        self.assertEqual(
            payload["crossing_chord_histogram"],
            {"1": 7875, "3": 24885, "5": 10850, "7": 579},
        )
        self.assertEqual(len(payload["sample_rectangle_replays"]), 3)

    def test_fourteen_vertex_c3_c3_c8_family_audit(self) -> None:
        payload = json.loads(
            (
                REPO_ROOT
                / "tmp"
                / "fourteen_vertex_c3_c3_c8_family_verified.json"
            ).read_text(encoding="utf-8")
        )
        self.assertTrue(payload["verified"])
        self.assertEqual(
            payload["status"],
            "all_c3_c3_c8_equality_supports_closed",
        )
        self.assertEqual(payload["eligible_singleton_factors"], 44_250)
        self.assertEqual(
            payload["one_term_unsafe_singleton_factors"], 44_064
        )
        self.assertEqual(payload["one_term_free_singleton_factors"], 186)
        self.assertEqual(payload["triangle_bijection_factors"], 6)
        self.assertEqual(payload["c8_internal_factors"], 31)
        self.assertEqual(payload["safe_factor_cartesian_product"], 186)

    def test_fourteen_vertex_c3_c3_c4_c4_family_audit(self) -> None:
        payload = json.loads(
            (
                REPO_ROOT
                / "tmp"
                / "fourteen_vertex_c3_c3_c4_c4_family_verified.json"
            ).read_text(encoding="utf-8")
        )
        self.assertTrue(payload["verified"])
        self.assertEqual(
            payload["status"],
            "all_c3_c3_c4_c4_equality_supports_closed",
        )
        self.assertEqual(payload["eligible_singleton_factors"], 44_262)
        self.assertEqual(payload["one_term_free_singleton_factors"], 7_974)
        self.assertEqual(payload["safe_factor_orbits"], 14)
        self.assertEqual(payload["connected_thirds"], 2_862_996)
        self.assertEqual(
            payload["stable_fork_certificates_replayed"], 394_068
        )
        self.assertEqual(payload["residual_supports"], 0)

    def test_fourteen_vertex_c4_c4_c6_hard_sample_audit(self) -> None:
        payload = json.loads(
            (
                REPO_ROOT
                / "tmp"
                / (
                    "fourteen_vertex_c4_4_6_sample93_15_"
                    "forced_slice_factor_cegar_verified.json"
                )
            ).read_text(encoding="utf-8")
        )
        self.assertTrue(payload["verified"])
        self.assertEqual(
            payload["status"],
            "forced_slice_factor_choice_unsat_verified",
        )
        self.assertEqual(payload["survivor_index"], 15)
        self.assertEqual(
            payload["conditional_factor_forks_replayed"], 80
        )
        self.assertEqual(payload["unit_factor_clauses_replayed"], 522)
        self.assertEqual(
            payload["binary_factor_clauses_replayed"], 52_059
        )
        self.assertEqual(payload["lattice_conflicts_replayed"], 3)
        self.assertTrue(payload["independent_unsat"])

    def test_fourteen_vertex_c4_c5_c5_family_audit(self) -> None:
        payload = json.loads(
            (
                REPO_ROOT
                / "tmp"
                / "fourteen_vertex_c4_c5_c5_family_verified.json"
            ).read_text(encoding="utf-8")
        )
        self.assertTrue(payload["verified"])
        self.assertEqual(
            payload["status"],
            "all_c4_c5_c5_equality_supports_closed",
        )
        self.assertEqual(payload["eligible_singleton_factors"], 44_195)
        self.assertEqual(
            payload["individually_one_term_free_factors"], 4_495
        )
        self.assertEqual(payload["fork_free_safe_factors"], 3_295)
        self.assertEqual(payload["fork_free_safe_factor_orbits"], 13)
        self.assertEqual(payload["compatible_seconds_across_orbits"], 4)
        self.assertEqual(
            payload["compatible_ordered_thirds_across_orbits"], 0
        )


if __name__ == "__main__":
    unittest.main()
