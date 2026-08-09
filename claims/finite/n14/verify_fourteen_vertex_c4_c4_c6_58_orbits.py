"""Replay the C4+C4+C6 certificate excluding 58 first-factor orbits."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from pysat.formula import CNF

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)



EXCLUDED_ORBITS = [
    0,
    1,
    2,
    3,
    4,
    12,
    17,
    18,
    19,
    20,
    21,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    52,
    53,
    58,
    59,
    60,
    61,
    62,
    64,
    65,
    66,
    69,
    70,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    82,
    83,
    84,
    85,
    86,
    87,
    88,
    89,
    90,
    91,
    92,
]

SURVIVING_ORBITS = [
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    13,
    14,
    15,
    16,
    22,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    54,
    55,
    56,
    57,
    63,
    67,
    68,
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_quiet(arguments: list[str]) -> None:
    subprocess.run(arguments, check=True, stdout=subprocess.DEVNULL)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--simple-result",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_late_simple_v1.json"
        ),
    )
    parser.add_argument(
        "--hard-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "late_combined_v1_hard_augmentation.json"
        ),
    )
    parser.add_argument(
        "--core12-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "late_combined_v1_hard_core12_augmentation.json"
        ),
    )
    parser.add_argument(
        "--rich-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "late_combined_v1_rich_augmentation.json"
        ),
    )
    parser.add_argument(
        "--minimum-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "late_combined_v2_min_augmentation.json"
        ),
    )
    parser.add_argument(
        "--orbit2-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "late_combined_v2_min_plus_orbit2_augmentation.json"
        ),
    )
    parser.add_argument(
        "--connectivity-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "late_combined_v2_min_plus_orbit2_kappa3_augmentation.json"
        ),
    )
    parser.add_argument(
        "--orbit3-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "late_combined_v3_orbit3_augmentation.json"
        ),
    )
    parser.add_argument(
        "--orbit-audit",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "late_combined_v3_orbit_audit.json"
        ),
    )
    parser.add_argument(
        "--conditioned-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_"
            "late_combined_v3_58_orbits_conditioned.cnf"
        ),
    )
    parser.add_argument(
        "--proof",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_"
            "late_combined_v3_58_orbits_kissat.drat"
        ),
    )
    parser.add_argument(
        "--drat-trim",
        type=Path,
        default=Path("tmp/drat-trim/drat-trim"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_"
            "late_combined_v3_58_orbits_final_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    hard = read_json(args.hard_augmentation)
    core12 = read_json(args.core12_augmentation)
    rich = read_json(args.rich_augmentation)
    minimum = read_json(args.minimum_augmentation)
    orbit2 = read_json(args.orbit2_augmentation)
    connectivity = read_json(args.connectivity_augmentation)
    orbit3 = read_json(args.orbit3_augmentation)
    chain = [
        (hard, args.hard_augmentation, 8, 64),
        (core12, args.core12_augmentation, 12, 152),
        (rich, args.rich_augmentation, 17, 136),
    ]
    expected_base = Path(
        read_json(args.simple_result)["cnf"]
    ).resolve()
    for manifest, path, certificate_count, new_no_goods in chain:
        if (
            manifest.get("status")
            != "verified_hard_certificate_no_goods_appended"
            or Path(manifest["base_cnf"]).resolve() != expected_base
            or len(manifest["certificate_records"]) != certificate_count
            or manifest["new_no_goods"] != new_no_goods
        ):
            raise AssertionError(f"hard augmentation changed: {path}")
        expected_base = Path(manifest["output_cnf"]).resolve()
    if (
        minimum.get("status")
        != "minimum_activity_rules_augmented"
        or Path(minimum["base_cnf"]).resolve() != expected_base
        or orbit2.get("status")
        != "minimum_activity_rules_augmented"
        or Path(orbit2["base_cnf"]).resolve()
        != Path(minimum["output_cnf"]).resolve()
        or connectivity.get("status")
        != "three_vertex_connectivity_condition_augmented"
        or Path(connectivity["base_cnf"]).resolve()
        != Path(orbit2["output_cnf"]).resolve()
        or orbit3.get("status")
        != "minimum_activity_rules_augmented"
        or Path(orbit3["base_cnf"]).resolve()
        != Path(connectivity["output_cnf"]).resolve()
    ):
        raise AssertionError("minimum/connectivity augmentation chain changed")

    rich_recheck = Path(
        "tmp/fourteen_vertex_c4_c4_c6_58_orbits_"
        "rich_reconstruction_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            str(REPO_ROOT / "verify_fourteen_vertex_c4_c4_c6_rule_cnf.py"),
            str(args.simple_result),
            "--augmentation",
            str(args.hard_augmentation),
            "--augmentation",
            str(args.core12_augmentation),
            "--augmentation",
            str(args.rich_augmentation),
            "--output",
            str(rich_recheck),
        ]
    )
    rich_audit = read_json(rich_recheck)
    if (
        rich_audit.get("verified") is not True
        or Path(rich_audit["final_cnf"]).resolve()
        != Path(rich["output_cnf"]).resolve()
        or rich_audit["final_cnf_sha256"]
        != rich["output_cnf_sha256"]
        or rich_audit["simple_sources_replayed"] != 5800
        or rich_audit["simple_transport_no_goods"] != 982563
    ):
        raise AssertionError("rich reconstruction changed")

    augmentation_specs = [
        (
            "minimum",
            args.minimum_augmentation,
            2357,
            92386,
        ),
        (
            "orbit2",
            args.orbit2_augmentation,
            168,
            3712,
        ),
        (
            "orbit3",
            args.orbit3_augmentation,
            272,
            5856,
        ),
    ]
    augmentation_audits: dict[str, dict] = {}
    for name, manifest_path, certificates, new_clauses in augmentation_specs:
        recheck = Path(
            "tmp/fourteen_vertex_c4_c4_c6_58_orbits_"
            f"{name}_augmentation_recheck.json"
        )
        run_quiet(
            [
                sys.executable,
                str(HERE / "verify_fourteen_vertex_two_even_cycle_minimum_activity_augmentation.py"),
                str(manifest_path),
                "--output",
                str(recheck),
            ]
        )
        audit = read_json(recheck)
        if (
            audit.get("verified") is not True
            or audit.get("certificates_replayed") != certificates
            or audit.get("new_transport_clauses") != new_clauses
            or audit.get("sat") is not True
        ):
            raise AssertionError(f"{name} augmentation changed")
        augmentation_audits[name] = audit

    connectivity_recheck = Path(
        "tmp/fourteen_vertex_c4_c4_c6_58_orbits_"
        "connectivity_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            str(REPO_ROOT / "verify_fourteen_vertex_two_even_cycle_three_connectivity_augmentation.py"),
            str(args.connectivity_augmentation),
            "--output",
            str(connectivity_recheck),
        ]
    )
    connectivity_audit = read_json(connectivity_recheck)
    if (
        connectivity_audit.get("verified") is not True
        or connectivity_audit.get("partition") != [4, 4, 6]
        or connectivity_audit.get("first_factor_orbits") != 93
        or connectivity_audit.get("new_quotient_cut_clauses") != 2576
        or connectivity_audit.get("sat") is not True
    ):
        raise AssertionError("connectivity reconstruction changed")

    global_cnf = Path(orbit3["output_cnf"])
    global_formula = CNF(from_file=str(global_cnf))
    conditioned_formula = CNF(from_file=str(args.conditioned_cnf))
    selector_clause = [232 + orbit for orbit in EXCLUDED_ORBITS]
    if conditioned_formula.clauses != [
        *global_formula.clauses,
        selector_clause,
    ]:
        raise AssertionError(
            "conditioned CNF is not the global CNF plus 58 selectors"
        )

    orbit_audit = read_json(args.orbit_audit)
    if (
        orbit_audit.get("status") != "per_orbit_rule_sat_frontier"
        or orbit_audit.get("cnf_sha256") != sha256(global_cnf)
        or orbit_audit.get("unsat_orbits") != EXCLUDED_ORBITS
        or orbit_audit.get("sat_orbits") != SURVIVING_ORBITS
    ):
        raise AssertionError("stored per-orbit frontier changed")

    drat_output = Path(
        "tmp/fourteen_vertex_c4_c4_c6_58_orbits_"
        "final_drat_trim_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            str(REPO_ROOT / "tools" / "generate" / "run_drat_trim.py"),
            "--drat-trim",
            str(args.drat_trim),
            "--cnf",
            str(args.conditioned_cnf),
            "--proof",
            str(args.proof),
            "--stdout",
            "tmp/fourteen_vertex_c4_c4_c6_58_orbits_"
            "final_drat_trim_recheck.stdout.log",
            "--stderr",
            "tmp/fourteen_vertex_c4_c4_c6_58_orbits_"
            "final_drat_trim_recheck.stderr.log",
            "--output",
            str(drat_output),
            "--forward",
        ]
    )
    drat = read_json(drat_output)
    if drat.get("verified") is not True:
        raise AssertionError("58-orbit DRAT replay changed")

    payload = {
        "verified": True,
        "status": "C4+C4+C6_58_first_factor_orbits_excluded",
        "scope": (
            "order-14 equality architecture with full factor C4+C4+C6, "
            "skeleton vertex connectivity at least 3, and a pinned first "
            "singleton factor in one of 58 orbits"
        ),
        "minimal_counterexample_relevance": (
            "a minimal Krenn-Gu counterexample must be 4-connected "
            "(Chandran-Gajjala-Illickan, arXiv:2407.00303)"
        ),
        "simple_sources_replayed": 5800,
        "simple_transport_no_goods": 982563,
        "hard_certificates_replayed": 37,
        "hard_new_no_goods": 352,
        "minimum_certificates_replayed": 2357,
        "minimum_new_transport_clauses": 92386,
        "orbit2_certificates_replayed": 168,
        "orbit2_new_transport_clauses": 3712,
        "connectivity_quotient_cut_clauses": 2576,
        "orbit3_certificates_replayed": 272,
        "orbit3_new_transport_clauses": 5856,
        "global_cnf": str(global_cnf),
        "global_cnf_sha256": sha256(global_cnf),
        "global_cnf_variables": global_formula.nv,
        "global_cnf_clauses": len(global_formula.clauses),
        "excluded_first_factor_orbits": EXCLUDED_ORBITS,
        "surviving_first_factor_orbits": SURVIVING_ORBITS,
        "selector_clause": selector_clause,
        "conditioned_cnf": str(args.conditioned_cnf),
        "conditioned_cnf_sha256": sha256(args.conditioned_cnf),
        "conditioned_cnf_clauses": len(conditioned_formula.clauses),
        "proof": str(args.proof),
        "proof_sha256": sha256(args.proof),
        "proof_bytes": args.proof.stat().st_size,
        "drat_trim_verified": True,
        "elapsed_seconds": time.perf_counter() - started,
        "global_conjecture_resolved": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
