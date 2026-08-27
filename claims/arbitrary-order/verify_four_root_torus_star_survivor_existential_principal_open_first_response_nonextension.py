#!/usr/bin/env python3
"""Replay the exact computational premises of the GLD80 open theorem.

The new implication from these premises to an existential principal open is
the algebraic properness/trait argument in the theorem document.  This script
checks the pinned exact fibre, boundary, and entrance certificates; it does
not present a CAS properness status as a substitute for that proof.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GLD74 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_gaussian_survivor_full_coefficient_"
    "fibre_first_response_nonextension.py"
)
GLD78 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_survivor_response_sign_boundary_"
    "invariant_open_obstruction.py"
)
GLD76 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_survivor_response_universal_module_reduction.py"
)
GLD79 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_gaussian_survivor_full_projective_"
    "response_boundary_classification.py"
)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check() -> dict[str, object]:
    gld76 = load("gld76_gld80_replay", GLD76).check()
    assert gld76["gld74_gaussian_intertwining_verified"] is True
    assert gld76["gaussian_full_response_intertwining_verified"] is True
    assert gld76[
        "matching_partition_identity_verified_in_both_presentations"
    ] is True
    assert gld76["equivalent_lift_matrix_shape"] == [4, 3]

    gld74 = load("gld74_gld80_replay", GLD74).check()
    assert gld74[
        "full_raw_coefficient_fibre_excluded_at_q0_first_response"
    ] is True
    assert gld74["affine_fibre_dimension"] == 35

    gld78 = load("gld78_gld80_replay", GLD78).check()
    assert gld78[
        "sign_plane_boundary_branches_excluded_on_named_principal_opens"
    ] is True
    assert len(gld78["points"]) == 3
    assert all(
        point["operator_augmented_ranks"] == [8, 9]
        for point in gld78["points"]
    )

    gld79 = load("gld79_gld80_replay", GLD79).check()
    assert gld79[
        "full_projective_boundary_is_exactly_gld77_sign_points"
    ] is True
    assert gld79["full_projective_boundary_point_count"] == 3
    assert gld79["other_projective_charts_empty"] is True
    assert gld79["transformed_gld74_quotient_covariance_verified"] is True

    return {
        "status": "exact_existential_principal_open_first_response_nonextension",
        "global_conjecture": "UNRESOLVED",
        "field": "Q(i)_then_geometric_over_characteristic_zero",
        "gld76_complete_gaussian_interface_transport_verified": True,
        "gld76_matching_partition_identity_verified": True,
        "fixed_coordinate_universal_lift_matrix_shape": [4, 3],
        "gld74_affine_gaussian_fibre_empty": True,
        "gld78_all_three_boundary_entrances_excluded": True,
        "gld79_complete_gaussian_projective_boundary_point_count": 3,
        "strict_closure": "s_saturation_of_intrinsic_rank_one_incidence",
        "properness_trait_bridge": "proved_in_theorem_not_a_CAS_status",
        "survivor_principal_open_exists": True,
        "explicit_survivor_exceptional_polynomial_computed": False,
        "other_survivor_components_covered": False,
        "source_interface_globalization_proved": False,
        "graph_witness_proved": False,
    }


def main() -> None:
    result = check()
    print("four-root survivor existential principal-open nonextension: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
