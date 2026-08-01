#!/usr/bin/env python3
"""Independent aggregate audit of weighted H22 on the diagonal p+q DVR wall.

This verifier intentionally does not import the primary aggregate verifier.  It
rebuilds the nine-cell partition, checks the frozen coverage ledger and direct
mask-6 certificate, and replays the mathematical verifiers used by each cell.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from z3 import And, Not, Or, Real, Solver, sat, unsat

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_VERIFICATION.md"
)
THEOREM = (
    ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md"
)
PRIMARY = (
    ROOT / "verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_obstruction.py"
)
LEDGER = ROOT / "p5_h22_p_plus_q_diagonal_dvr_coverage.json"
MASK6_CERTIFICATE = (
    ROOT / "p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_certificate.json"
)

EXPECTED_ROWS = {
    "finite_generic_y0_b_full": {
        "parameter_conditions": "a not in {0,-1,-1/2}; y=0; x0=d",
        "p4_route": "B_full",
        "h22_status": "VERIFIED",
    },
    "finite_generic_y0_b_drop": {
        "parameter_conditions": "a not in {0,-1,-1/2}; y=0; x0>d",
        "p4_route": "B_drop",
        "h22_status": "VERIFIED",
    },
    "finite_generic_negative_y_embedded_p3": {
        "parameter_conditions": (
            "a not in {0,-1,-1/2}; -d<=y<0; x0>=d; all "
            "(eps_x,eps_y) in {0,1}^2 realized subject to "
            "eps_x=[x0=d], eps_y=[y=-d]"
        ),
        "p4_route": "embedded-P3 support-two tangent closure",
        "h22_status": "UNKNOWN",
    },
    "finite_exceptional_a0_a_minus1": {
        "parameter_conditions": (
            "a in {0,-1}; -d<=y<=0; x0>=max(d-R,d+y); every realized "
            "residue law, direct y=0 chart, and lower-pair y<0 baseline/wall"
        ),
        "p4_route": (
            "direct exceptional charts for y=0; component-15 support-one "
            "lower-pair closure for y<0"
        ),
        "h22_status": "VERIFIED",
    },
    "finite_half_centre_y0": {
        "parameter_conditions": (
            "a=-1/2; y=0; x0=d (k!=0 replacement) or x0>d (k=0 degeneration)"
        ),
        "p4_route": "half-centre replacement family",
        "h22_status": "VERIFIED",
    },
    "finite_half_centre_negative_y_embedded_p3": {
        "parameter_conditions": (
            "a=-1/2; -d<=y<0; x0>=d; all four (eps_x,eps_y) boundary flags"
        ),
        "p4_route": "embedded-P3 support-two tangent closure",
        "h22_status": "UNKNOWN",
    },
    "infinity_lower_pair_embedded_p3": {
        "parameter_conditions": (
            "r<0<d; -d<=y<-r; x0>=d-2r; four (eps_x,eps_l) faces "
            "with eps_u=0"
        ),
        "p4_route": "embedded-P3 support-two tangent closure",
        "h22_status": "UNKNOWN",
    },
    "infinity_component14_off_wall": {
        "parameter_conditions": "r<0<d; y=-r; x0>d-2r",
        "p4_route": "component-14 gamma=0 endpoint",
        "h22_status": "VERIFIED",
    },
    "infinity_component14_on_wall": {
        "parameter_conditions": "r<0<d; y=-r; x0=d-2r",
        "p4_route": "component-14 gamma=2 endpoint",
        "h22_status": "VERIFIED",
    },
}

MASK6_IDS = {
    "finite_generic_negative_y_embedded_p3",
    "finite_half_centre_negative_y_embedded_p3",
    "infinity_lower_pair_embedded_p3",
}
FLAG_SQUARE = {(0, 0), (1, 0), (0, 1), (1, 1)}

FILES = {
    "p4_theorem": "P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md",
    "p4_primary": "verify_p4_common_active_binary_triangle_p_plus_q_boundary.py",
    "p4_audit": "audit_p4_common_active_binary_triangle_p_plus_q_boundary.py",
    "partial_report": (
        "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_PARTIAL.md"
    ),
    "partial_audit": (
        "audit_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial.py"
    ),
    "b_full_audit": (
        "audit_p5_h22_common_active_binary_triangle_p_plus_q_"
        "b_full_infinity_finite_pair_verifier.py"
    ),
    "b_drop_audit": (
        "audit_p5_h22_common_active_binary_triangle_p_plus_q_"
        "generic_d01_infinity_b_drop.py"
    ),
    "exceptional_audit": (
        "audit_p5_h22_common_active_binary_triangle_p_plus_q_"
        "exceptional_fibres_independent.py"
    ),
    "endpoint_base_audit": (
        "audit_p5_h22_common_active_binary_triangle_p_plus_q_"
        "infinity_endpoint_candidate_verifier.py"
    ),
    "endpoint_integration_audit": (
        "audit_p5_h22_common_active_binary_triangle_p_plus_q_"
        "infinity_endpoint_integration_verifier.py"
    ),
    "endpoint_compatibility_audit": (
        "audit_p5_h22_common_active_binary_triangle_p_plus_q_"
        "infinity_endpoint_compatibility_obstruction_verifier.py"
    ),
    "r0_primary": "derive_p5_h22_embedded_p3_component_r_zero_boundary_obstruction.py",
    "r0_historical_audit": (
        "audit_p5_h22_embedded_p3_component_r_zero_boundary_independent.py"
    ),
    "r0_endpoint_audit": (
        "audit_p5_h22_embedded_p3_component_r_zero_t_nonzero_"
        "weight_endpoints_verifier.py"
    ),
    "coverage_audit": "audit_p5_h22_p_plus_q_diagonal_dvr_coverage.py",
    "mask6_primary": (
        "derive_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_"
        "obstruction_candidate.py"
    ),
    "mask6_audit": (
        "audit_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_"
        "independent.py"
    ),
    "coverage_ledger": LEDGER.name,
    "mask6_certificate": MASK6_CERTIFICATE.name,
    "aggregate_theorem": THEOREM.name,
    "aggregate_primary": PRIMARY.name,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout.strip()


def run_json(*command: str) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    require(
        completed.returncode == 0,
        f"replay failed ({' '.join(command)}): {completed.stderr[-2000:]}",
    )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"replay did not emit JSON ({' '.join(command)}): "
            f"{completed.stdout[-2000:]}"
        ) from exc
    require(isinstance(result, dict), f"non-object replay: {' '.join(command)}")
    return result


def prove_exact_partition(name: str, constraints: list[Any], branches: list[Any]) -> None:
    """Prove coverage, disjointness, and non-vacuity for a linear branch split."""

    solver = Solver()
    solver.add(*constraints, Not(Or(*branches)))
    require(solver.check() == unsat, f"{name}: uncovered valuation region")
    for index, branch in enumerate(branches):
        solver = Solver()
        solver.add(*constraints, branch)
        require(solver.check() == sat, f"{name}: vacuous branch {index}")
        for other_index in range(index + 1, len(branches)):
            solver = Solver()
            solver.add(*constraints, branch, branches[other_index])
            require(
                solver.check() == unsat,
                f"{name}: overlapping branches {index},{other_index}",
            )


def exact_p4_partition() -> dict[str, list[str]]:
    d, r, y, x0, residue_min = (
        Real("d"),
        Real("r"),
        Real("y"),
        Real("x0"),
        Real("R"),
    )

    generic = [
        And(y == 0, x0 == d),
        And(y == 0, x0 > d),
        y < 0,
    ]
    prove_exact_partition(
        "finite generic",
        [d > 0, y >= -d, y <= 0, x0 >= d],
        generic,
    )

    half = [y == 0, y < 0]
    prove_exact_partition(
        "finite half-centre",
        [d > 0, y >= -d, y <= 0, x0 >= d],
        half,
    )

    infinity = [
        y < -r,
        And(y == -r, x0 > d - 2 * r),
        And(y == -r, x0 == d - 2 * r),
    ]
    prove_exact_partition(
        "infinity",
        [r < 0, d > 0, y >= -d, y <= -r, x0 >= d - 2 * r],
        infinity,
    )

    # The two exceptional centres are aggregated because the exact P4 theorem
    # gives the same valuation schema and one verified H22 route for both.
    exceptional_constraints = [
        d > 0,
        residue_min > 0,
        d >= residue_min,
        y >= -d,
        y <= 0,
        x0 >= d - residue_min,
        x0 >= d + y,
    ]
    exceptional = [And(*exceptional_constraints)]
    prove_exact_partition(
        "finite exceptional aggregate",
        exceptional_constraints,
        exceptional,
    )

    return {
        "finite_generic": [
            "finite_generic_y0_b_full",
            "finite_generic_y0_b_drop",
            "finite_generic_negative_y_embedded_p3",
        ],
        "finite_exceptional": ["finite_exceptional_a0_a_minus1"],
        "finite_half_centre": [
            "finite_half_centre_y0",
            "finite_half_centre_negative_y_embedded_p3",
        ],
        "infinity": [
            "infinity_lower_pair_embedded_p3",
            "infinity_component14_off_wall",
            "infinity_component14_on_wall",
        ],
    }


def audit_ledger() -> tuple[dict[str, dict[str, Any]], set[str]]:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in ledger["strata"]}
    require(set(rows) == set(EXPECTED_ROWS), "ledger does not have exactly nine rows")
    require(len(rows) == 9, "ledger row count is not nine")
    for row_id, expected in EXPECTED_ROWS.items():
        for field, value in expected.items():
            require(rows[row_id].get(field) == value, f"{row_id}: changed {field}")
    old_unknown = {
        row_id for row_id, row in rows.items() if row["h22_status"] == "UNKNOWN"
    }
    require(old_unknown == MASK6_IDS, "historical UNKNOWN set is not exactly mask 6")
    require(
        sum(row["h22_status"] == "VERIFIED" for row in rows.values()) == 6,
        "historical ledger no longer has six verified rows",
    )
    return rows, old_unknown


def audit_mask6(old_unknown: set[str]) -> tuple[dict[str, Any], list[str]]:
    certificate = json.loads(MASK6_CERTIFICATE.read_text(encoding="utf-8"))
    require(certificate["claim_label"] == "VERIFIED", "mask-6 certificate label")
    require(certificate["independent_verifier_complete"] is True, "mask-6 audit flag")
    families = {entry["id"]: entry for entry in certificate["actual_families"]}
    require(set(families) == old_unknown, "mask-6 ids do not exactly equal old UNKNOWN ids")
    actual_flags: list[str] = []
    for family_id, family in families.items():
        flags = {(entry["first"], entry["second"]) for entry in family["flags"]}
        require(flags == FLAG_SQUARE, f"{family_id}: flag square is incomplete")
        require(len(family["flags"]) == 4, f"{family_id}: duplicate flag")
        actual_flags.extend(f"{family_id}:{a}{b}" for a, b in sorted(flags))
    require(len(actual_flags) == 12, "actual mask-6 flag count is not twelve")
    structural = certificate["certificate"]
    require(structural["D01_all_alpha_diagonal"] == "0", "D01 obstruction changed")
    require(structural["D23_all_alpha_diagonal"] == "0", "D23 obstruction changed")
    require(
        structural["homogeneous_weight_coverage"] == ["[0:1]", "[1:0]", "rho*sigma!=0"],
        "homogeneous weight coverage changed",
    )
    return certificate, sorted(actual_flags)


def replay_dependencies() -> dict[str, dict[str, Any]]:
    uv_sympy = ("uv", "run", "--with", "sympy", "python")
    results = {
        "p4_primary": run_json(
            "uv",
            "run",
            "--with",
            "sympy",
            "--with",
            "z3-solver",
            "python",
            FILES["p4_primary"],
        ),
        "p4_audit": run_json(*uv_sympy, FILES["p4_audit"]),
        "partial": run_json(*uv_sympy, FILES["partial_audit"]),
        "b_full": run_json(*uv_sympy, FILES["b_full_audit"]),
        "b_drop": run_json(*uv_sympy, FILES["b_drop_audit"]),
        "exceptional": run_json(*uv_sympy, FILES["exceptional_audit"]),
        "endpoint_base": run_json(*uv_sympy, FILES["endpoint_base_audit"]),
        "endpoint_integration": run_json(
            *uv_sympy, FILES["endpoint_integration_audit"]
        ),
        "endpoint_compatibility": run_json(
            *uv_sympy, FILES["endpoint_compatibility_audit"]
        ),
        "r0_primary": run_json(*uv_sympy, FILES["r0_primary"]),
        "r0_historical": run_json(*uv_sympy, FILES["r0_historical_audit"]),
        "r0_endpoints": run_json(*uv_sympy, FILES["r0_endpoint_audit"]),
        "coverage": run_json("python", FILES["coverage_audit"]),
        "mask6_primary": run_json(*uv_sympy, FILES["mask6_primary"]),
        "mask6_audit": run_json(*uv_sympy, FILES["mask6_audit"]),
    }

    for key in ("p4_primary", "p4_audit"):
        require(results[key]["status"] == "pass", f"{key} did not pass")
        require(results[key]["claim_label"] == "VERIFIED", f"{key} label")
    require(
        results["p4_primary"]["fresh_independent_verifier_complete"] is True,
        "P4 independent replay incomplete",
    )

    partial = results["partial"]
    require(partial["status"] == "pass", "partial verifier failed")
    require(partial["claim_label"] == "UNKNOWN", "historical partial label changed")
    require(partial["overall_weighted_H22_resolved"] is False, "partial overclaim")
    require(
        partial["D01_infinity_closed"] is False,
        "historical partial checkpoint was silently promoted",
    )
    finite_certificates = partial["subclaim_verdicts"][
        "four_generic_finite_D01_certificates"
    ]
    require(len(finite_certificates) == 4, "generic finite certificate count")
    require(
        all(item["verdict"] == "VERIFIED" for item in finite_certificates),
        "generic finite D01 certificate",
    )
    require(
        partial["subclaim_verdicts"]["half_replacement_Hall_obstruction"]["verdict"]
        == "VERIFIED",
        "half-centre Hall obstruction missing",
    )

    b_full = results["b_full"]
    require(b_full["status"] == "pass" and b_full["claim_label"] == "VERIFIED", "B_full")
    require(b_full["generic_B_full_D01_infinity_subclaim"] == "VERIFIED", "B_full infinity")
    require(
        b_full["generic_B_full_infinity_finite_pair_subclaim"] == "VERIFIED",
        "B_full finite pair",
    )
    b_drop = results["b_drop"]
    require(
        b_drop["status"] == "pass"
        and b_drop["claim_label"] == "VERIFIED"
        and b_drop["verdict"] == "VERIFIED",
        "B_drop replay",
    )
    exceptional = results["exceptional"]
    require(
        exceptional["status"] == "pass"
        and exceptional["claim_label"] == "VERIFIED"
        and exceptional["verdict"] == "VERIFIED",
        "exceptional replay",
    )

    # The first endpoint verifier correctly remains REFUTED only for its
    # overstrong exact-rank sentence.  Its survivor cover is unchanged, and
    # the two later no-import verifiers close the required compatibility.
    endpoint_base = results["endpoint_base"]
    require(endpoint_base["claim_label"] == "REFUTED", "endpoint history erased")
    require(endpoint_base["on_wall_weighted_H22_fibre_empty_verified"] is True, "on-wall endpoint")
    require(
        endpoint_base["off_wall_factor_cover_verified_up_to_rank_at_most_three"]
        is True,
        "off-wall factor cover",
    )
    require(endpoint_base["survivor_boundary_changed_by_refutation"] is False, "endpoint survivor change")
    integration = results["endpoint_integration"]
    compatibility = results["endpoint_compatibility"]
    require(
        integration["status"] == "pass"
        and integration["claim_label"] == "VERIFIED"
        and integration["reduction_to_verified_r_zero_compatibility_obstruction"]
        is True,
        "component-14 integration",
    )
    require(
        compatibility["status"] == "pass"
        and compatibility["claim_label"] == "VERIFIED"
        and compatibility["stacked_compatibility_obstruction"] == "VERIFIED",
        "component-14 compatibility",
    )

    # Retain the original r0 transport refutation while checking the repaired
    # combined theorem.  This chart is corroborating evidence, not the route
    # used for the actual mask-6 wall flags.
    r0_primary = results["r0_primary"]
    require(
        r0_primary["status"] == "pass"
        and r0_primary["claim_label"] == "VERIFIED"
        and r0_primary["full_r_zero_divisor_obstruction_proved"] is True
        and r0_primary["original_full_divisor_transport_proof_refuted"] is True,
        "combined r0 divisor status",
    )
    require(
        results["r0_historical"]["claim_label"] == "REFUTED",
        "historical r0 refutation erased",
    )
    require(
        results["r0_endpoints"]["status"] == "pass"
        and results["r0_endpoints"]["claim_label"] == "VERIFIED",
        "r0 endpoint repair",
    )

    coverage = results["coverage"]
    require(
        coverage["status"] == "pass"
        and coverage["claim_label"] == "UNKNOWN"
        and coverage["stratum_count"] == 9
        and coverage["verified_stratum_count"] == 6
        and coverage["unknown_stratum_count"] == 3
        and set(coverage["unknown_strata"]) == MASK6_IDS,
        "historical coverage replay",
    )
    for key in ("mask6_primary", "mask6_audit"):
        require(
            results[key]["status"] == "pass"
            and results[key]["claim_label"] == "VERIFIED",
            f"{key} replay",
        )
    require(results["mask6_audit"]["actual_flag_count"] == 12, "mask-6 audit flag count")
    require(
        results["mask6_audit"]["all_actual_mask6_flags_obstructed"] is True,
        "mask-6 audit conclusion",
    )
    require(
        results["mask6_audit"]["projective_chart_transport_used"] is False,
        "mask-6 audit unexpectedly used projective transport",
    )
    return results


def theorem_scope_audit() -> dict[str, bool]:
    text = THEOREM.read_text(encoding="utf-8")
    markers = {
        "full_projective_excluded": "does not close the\nfull projective embedded-`P3` component" in text,
        "non_diagonal_excluded": "non-diagonal or arbitrary `GL4`\nsource changes" in text,
        "local_to_global_excluded": "arbitrary-order local-to-global reduction" in text,
        "global_excluded": "global\nKrenn--Gu conjecture" in text,
        "finite_field_not_proof": "No finite-field computation" in text,
    }
    require(all(markers.values()), "aggregate theorem lost an evidence boundary")
    return markers


def main() -> None:
    for path_name in FILES.values():
        require((ROOT / path_name).is_file(), f"missing input: {path_name}")
    require(REPORT.is_file(), f"missing run report: {REPORT.name}")

    partition = exact_p4_partition()
    require(sum(len(ids) for ids in partition.values()) == 9, "partition total")
    require(
        {item for ids in partition.values() for item in ids} == set(EXPECTED_ROWS),
        "partition ids differ from ledger ids",
    )
    rows, old_unknown = audit_ledger()
    _certificate, actual_flags = audit_mask6(old_unknown)
    replays = replay_dependencies()
    scope_markers = theorem_scope_audit()

    integrated = {
        row_id: "VERIFIED"
        if row["h22_status"] == "VERIFIED" or row_id in MASK6_IDS
        else row["h22_status"]
        for row_id, row in rows.items()
    }
    require(set(integrated.values()) == {"VERIFIED"}, "actual wall retains a gap")

    inputs = {key: sha256(ROOT / path_name) for key, path_name in FILES.items()}
    result = {
        "status": "pass",
        "claim_label": "VERIFIED",
        "role": "verifier",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "scope": (
            "weighted H22 on the complete nine-stratum diagonal-source-torus "
            "DVR p+q=0 wall of component twenty"
        ),
        "inputs": inputs,
        "method": (
            "fresh Z3 real-linear coverage/disjointness proof for the P4 centre "
            "splits; exact ledger and twelve-flag certificate comparison; direct "
            "subprocess replay of every mathematical dependency; no import of "
            "the primary aggregate verifier"
        ),
        "command": (
            "uv run --with z3-solver python "
            "audit_p5_h22_common_active_binary_triangle_p_plus_q_"
            "boundary_obstruction.py"
        ),
        "outputs": {REPORT.name: sha256(REPORT), SCRIPT.name: sha256(SCRIPT)},
        "limitations": (
            "diagonal source tori only; no full embedded-P3 projective closure, "
            "non-diagonal or arbitrary GL4 source changes, arbitrary-order "
            "local-to-global reduction, component exhaustiveness, prize graph, "
            "or global Krenn-Gu conclusion"
        ),
        "p4_partition": partition,
        "partition_solver_result": "exactly nine nonempty pairwise-disjoint exhaustive strata",
        "historical_verified_stratum_count": 6,
        "historical_unknown_strata": sorted(old_unknown),
        "mask6_actual_flags": actual_flags,
        "mask6_actual_flag_count": len(actual_flags),
        "integrated_strata": integrated,
        "verified_stratum_count": sum(value == "VERIFIED" for value in integrated.values()),
        "remaining_actual_diagonal_DVR_H22_gaps": [],
        "component14_infinity_endpoints_closed": True,
        "standard_chart_r0_divisor_closed": True,
        "standard_chart_r0_divisor_needed_for_mask6_wall_closure": False,
        "full_embedded_P3_projective_H22_closed": False,
        "finite_field_computation_used_as_proof": False,
        "broad_brute_force_used": False,
        "primary_aggregate_verifier_imported": False,
        "dependency_replay_labels": {
            key: value.get("claim_label") for key, value in replays.items()
        },
        "scope_markers": scope_markers,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
