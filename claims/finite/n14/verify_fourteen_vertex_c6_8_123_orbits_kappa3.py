"""Replay the order-14 C6+C8 certificate excluding 123 kappa>=3 orbits."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from pysat.formula import CNF


UNSAT_ORBITS = [
    *range(0, 10),
    *range(100, 145),
    *range(171, 174),
    179,
    182,
    185,
    *range(187, 190),
    *range(200, 219),
    *range(220, 226),
    227,
    232,
    233,
    238,
    247,
    269,
    *range(300, 328),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_quiet(arguments: list[str]) -> None:
    subprocess.run(arguments, check=True, stdout=subprocess.DEVNULL)


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_augmentation(
    path: Path,
    output: Path,
    expected_certificates: int,
    expected_clauses: int,
) -> dict[str, object]:
    run_quiet(
        [
            sys.executable,
            "verify_fourteen_vertex_two_even_cycle_"
            "minimum_activity_augmentation.py",
            str(path),
            "--output",
            str(output),
        ]
    )
    audit = read_json(output)
    if (
        audit.get("verified") is not True
        or audit.get("status")
        != "minimum_activity_augmentation_reconstructed"
        or audit.get("certificates_replayed") != expected_certificates
        or audit.get("new_transport_clauses") != expected_clauses
        or audit.get("sat") is not True
    ):
        raise AssertionError(f"augmentation replay changed: {path}")
    return audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--orbit9-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_"
            "v22_orbit9_targeted_augmentation.json"
        ),
    )
    parser.add_argument(
        "--orbit9-direct-augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_"
            "v22_orbit9_direct_kappa3_augmentation.json"
        ),
    )
    parser.add_argument(
        "--conditioned-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_123_orbits_"
            "v22_kappa3_conditioned.cnf"
        ),
    )
    parser.add_argument(
        "--proof",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_123_orbits_"
            "v22_kappa3_kissat.drat"
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
            "tmp/fourteen_vertex_c6_8_123_orbits_"
            "kappa3_final_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    predecessor_output = Path(
        "tmp/fourteen_vertex_c6_8_123_orbits_"
        "predecessor_122_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            "verify_fourteen_vertex_c6_8_122_orbits_kappa3.py",
            "--output",
            str(predecessor_output),
        ]
    )
    predecessor = read_json(predecessor_output)
    predecessor_cnf = Path(str(predecessor["global_cnf"]))
    if (
        predecessor.get("verified") is not True
        or predecessor.get("status")
        != "C6+C8_kappa3_122_first_factor_orbits_excluded"
        or predecessor_cnf
        != Path(
            "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_"
            "v21_orbit8_targeted.cnf"
        )
        or predecessor.get("global_cnf_sha256")
        != "8a03d170099f2dea4fe8fd8457dbbad4f"
        "85fdc1fc2811bb6559a1d01c0a9822d"
    ):
        raise AssertionError("122-orbit predecessor reconstruction changed")

    targeted = read_json(args.orbit9_augmentation)
    global_cnf = Path(str(targeted["output_cnf"]))
    prerequisite = targeted.get("three_connectivity_prerequisite")
    if not isinstance(prerequisite, dict):
        raise AssertionError("targeted orbit-9 prerequisite missing")
    connectivity = Path(str(prerequisite["augmentation"]))
    if (
        targeted.get("status") != "minimum_activity_rules_augmented"
        or targeted.get("partition") != [6, 8]
        or Path(str(targeted["base_cnf"])).resolve()
        != predecessor_cnf.resolve()
        or targeted.get("base_cnf_sha256") != sha256(predecessor_cnf)
        or prerequisite.get("augmentation_sha256")
        != sha256(connectivity)
        or prerequisite.get("base_extension_clauses") != 530
        or targeted.get("certificates_replayed") != 136
        or targeted.get("new_transport_clauses") != 360
        or targeted.get("output_cnf_sha256") != sha256(global_cnf)
        or targeted.get("output_cnf_variables") != 559
        or targeted.get("output_cnf_clauses") != 127500
    ):
        raise AssertionError("targeted orbit-9 augmentation changed")

    verify_augmentation(
        args.orbit9_augmentation,
        Path(
            "tmp/fourteen_vertex_c6_8_123_orbits_"
            "orbit9_targeted_augmentation_recheck.json"
        ),
        136,
        360,
    )

    direct = read_json(args.orbit9_direct_augmentation)
    direct_cnf = Path(str(direct["output_cnf"]))
    direct_prerequisite = direct.get("three_connectivity_prerequisite")
    if not isinstance(direct_prerequisite, dict):
        raise AssertionError("direct orbit-9 prerequisite missing")
    if (
        direct.get("status") != "minimum_activity_rules_augmented"
        or direct.get("partition") != [6, 8]
        or Path(str(direct["base_cnf"])).resolve()
        != predecessor_cnf.resolve()
        or direct.get("base_cnf_sha256") != sha256(predecessor_cnf)
        or direct_prerequisite.get("augmentation_sha256")
        != sha256(connectivity)
        or direct_prerequisite.get("base_extension_clauses") != 530
        or direct.get("certificates_replayed") != 61
        or direct.get("new_transport_clauses") != 244
        or direct.get("output_cnf_sha256") != sha256(direct_cnf)
        or direct.get("output_cnf_variables") != 559
        or direct.get("output_cnf_clauses") != 127384
    ):
        raise AssertionError("direct orbit-9 augmentation changed")

    verify_augmentation(
        args.orbit9_direct_augmentation,
        Path(
            "tmp/fourteen_vertex_c6_8_123_orbits_"
            "orbit9_direct_augmentation_recheck.json"
        ),
        61,
        244,
    )

    for name, cnf_path in (
        ("targeted", global_cnf),
        ("direct", direct_cnf),
    ):
        orbit_output = Path(
            f"tmp/fourteen_vertex_c6_8_123_orbits_"
            f"{name}_orbit_audit_recheck.json"
        )
        run_quiet(
            [
                sys.executable,
                "audit_fourteen_vertex_c4_c4_c6_rule_sat_orbits.py",
                "--cnf",
                str(cnf_path),
                "--selector-zero",
                "232",
                "--orbit-offset",
                "0",
                "--orbits",
                "328",
                "--output",
                str(orbit_output),
            ]
        )
        orbit_audit = read_json(orbit_output)
        expected_sat = [
            orbit for orbit in range(328) if orbit not in UNSAT_ORBITS
        ]
        if (
            orbit_audit["unsat_orbits"] != UNSAT_ORBITS
            or orbit_audit["sat_orbits"] != expected_sat
        ):
            raise AssertionError(f"fresh {name} orbit frontier changed")

    global_formula = CNF(from_file=str(global_cnf))
    conditioned_formula = CNF(from_file=str(args.conditioned_cnf))
    selector_clause = [232 + orbit for orbit in UNSAT_ORBITS]
    if conditioned_formula.clauses != [
        *global_formula.clauses,
        selector_clause,
    ]:
        raise AssertionError(
            "conditioned CNF is not global CNF plus the 123 selectors"
        )

    drat_output = Path(
        "tmp/fourteen_vertex_c6_8_123_orbits_"
        "final_drat_trim_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            "run_drat_trim.py",
            "--drat-trim",
            str(args.drat_trim),
            "--cnf",
            str(args.conditioned_cnf),
            "--proof",
            str(args.proof),
            "--stdout",
            "tmp/fourteen_vertex_c6_8_123_orbits_"
            "final_drat_trim_recheck.stdout.log",
            "--stderr",
            "tmp/fourteen_vertex_c6_8_123_orbits_"
            "final_drat_trim_recheck.stderr.log",
            "--output",
            str(drat_output),
            "--forward",
        ]
    )
    if read_json(drat_output).get("verified") is not True:
        raise AssertionError("123-orbit DRAT replay changed")

    payload = {
        "verified": True,
        "status": "C6+C8_kappa3_123_first_factor_orbits_excluded",
        "scope": (
            "order-14 equality architecture with full factor C6+C8, "
            "skeleton vertex connectivity at least 3, and a pinned "
            "first singleton factor in the listed 123 orbits"
        ),
        "minimal_counterexample_relevance": (
            "a minimal Krenn-Gu counterexample must be 4-connected "
            "(Chandran-Gajjala-Illickan, arXiv:2407.00303)"
        ),
        "predecessor_122_replayed": True,
        "orbit9_targeted_certificates_replayed": 136,
        "orbit9_targeted_new_transport_clauses": 360,
        "orbit9_direct_certificates_replayed": 61,
        "orbit9_direct_new_transport_clauses": 244,
        "independent_orbit9_frontiers_agree": True,
        "global_cnf": str(global_cnf),
        "global_cnf_sha256": sha256(global_cnf),
        "global_cnf_variables": global_formula.nv,
        "global_cnf_clauses": len(global_formula.clauses),
        "sat_first_factor_orbits": 328 - len(UNSAT_ORBITS),
        "unsat_first_factor_orbits": UNSAT_ORBITS,
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
