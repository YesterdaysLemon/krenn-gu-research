"""Replay the order-14 C6+C8 certificate excluding 118 first orbits.

The verifier rebuilds the certified 117-orbit predecessor, independently
reconstructs every later minimum-activity and one-extra-cycle augmentation,
audits all 328 selectors, checks the exact conditioned DIMACS formula, and
finally replays the raw Kissat DRAT proof.
"""

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



PREDECESSOR_UNSAT_ORBITS = [
    *range(0, 5),
    *range(100, 144),
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
UNSAT_ORBITS = sorted([*PREDECESSOR_UNSAT_ORBITS, 5])

MINIMUM_LAYERS = [
    "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_v9_"
    "reoriented_augmentation.json",
    "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_v10_"
    "augmentation.json",
    "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_v11_"
    "reoriented_augmentation.json",
]
ONE_EXTRA_LAYERS = [
    "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_v12_"
    "one_extra_transport_augmentation.json",
    "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_v13_"
    "minimum_one_extra_transport_augmentation.json",
    "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_v14_"
    "minimum_one_extra_multicore_augmentation.json",
    "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_v15_"
    "minimum_one_extra_multicore_augmentation.json",
    "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_v16_"
    "minimum_one_extra_multicore_augmentation.json",
    "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_v17_"
    "orbit5_one_extra_augmentation.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_quiet(arguments: list[str]) -> None:
    subprocess.run(arguments, check=True, stdout=subprocess.DEVNULL)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--conditioned-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_118_orbits_v17_conditioned.cnf"
        ),
    )
    parser.add_argument(
        "--proof",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_118_orbits_v17_kissat.drat"
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
            "tmp/fourteen_vertex_c6_8_118_orbits_final_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    predecessor_output = Path(
        "tmp/fourteen_vertex_c6_8_118_orbits_"
        "predecessor_117_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            str(HERE / "verify_fourteen_vertex_c6_8_117_orbits.py"),
            "--output",
            str(predecessor_output),
        ]
    )
    predecessor = json.loads(
        predecessor_output.read_text(encoding="utf-8")
    )
    if (
        predecessor.get("verified") is not True
        or predecessor.get("unsat_first_factor_orbits")
        != PREDECESSOR_UNSAT_ORBITS
    ):
        raise AssertionError("117-orbit predecessor certificate changed")
    previous_cnf = Path(predecessor["global_cnf"])

    layer_records: list[dict[str, object]] = []
    layer_specs = [
        *[
            (
                Path(path),
                str(HERE / "verify_fourteen_vertex_two_even_cycle_minimum_activity_augmentation.py"),
                "minimum_activity_augmentation_reconstructed",
                "new_transport_clauses",
            )
            for path in MINIMUM_LAYERS
        ],
        *[
            (
                Path(path),
                str(HERE / "verify_fourteen_vertex_two_even_cycle_one_extra_cycle_augmentation.py"),
                "one_extra_cycle_augmentation_reconstructed",
                "new_transport_no_goods",
            )
            for path in ONE_EXTRA_LAYERS
        ],
    ]
    for layer_id, (
        manifest_path,
        verifier,
        expected_status,
        clause_key,
    ) in enumerate(layer_specs):
        manifest = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
        base_cnf = Path(manifest["base_cnf"])
        output_cnf = Path(manifest["output_cnf"])
        if (
            base_cnf.resolve() != previous_cnf.resolve()
            or manifest["base_cnf_sha256"] != sha256(base_cnf)
            or manifest["output_cnf_sha256"] != sha256(output_cnf)
        ):
            raise AssertionError(
                f"augmentation chain changed at layer {layer_id}"
            )
        recheck_path = Path(
            "tmp/fourteen_vertex_c6_8_118_orbits_"
            f"layer_{layer_id}_recheck.json"
        )
        run_quiet(
            [
                sys.executable,
                verifier,
                str(manifest_path),
                "--output",
                str(recheck_path),
            ]
        )
        recheck = json.loads(
            recheck_path.read_text(encoding="utf-8")
        )
        if (
            recheck.get("verified") is not True
            or recheck.get("status") != expected_status
            or recheck.get("sat") is not True
        ):
            raise AssertionError(
                f"independent augmentation replay failed at layer {layer_id}"
            )
        layer_records.append(
            {
                "manifest": str(manifest_path),
                "manifest_sha256": sha256(manifest_path),
                "recheck": str(recheck_path),
                "recheck_sha256": sha256(recheck_path),
                "certificates_replayed": int(
                    recheck["certificates_replayed"]
                ),
                "new_clauses": int(recheck[clause_key]),
                "output_cnf_sha256": sha256(output_cnf),
            }
        )
        previous_cnf = output_cnf

    global_cnf = previous_cnf
    orbit_output = Path(
        "tmp/fourteen_vertex_c6_8_118_orbits_"
        "final_orbit_audit_recheck.json"
    )
    run_quiet(
        [
            sys.executable,
            str(HERE / "audit_fourteen_vertex_c4_c4_c6_rule_sat_orbits.py"),
            "--cnf",
            str(global_cnf),
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
    orbit_audit = json.loads(
        orbit_output.read_text(encoding="utf-8")
    )
    expected_sat = [
        orbit for orbit in range(328) if orbit not in UNSAT_ORBITS
    ]
    if (
        orbit_audit["unsat_orbits"] != UNSAT_ORBITS
        or orbit_audit["sat_orbits"] != expected_sat
    ):
        raise AssertionError("fresh 118-orbit frontier changed")

    global_formula = CNF(from_file=str(global_cnf))
    conditioned_formula = CNF(from_file=str(args.conditioned_cnf))
    selector_clause = [232 + orbit for orbit in UNSAT_ORBITS]
    if conditioned_formula.clauses != [
        *global_formula.clauses,
        selector_clause,
    ]:
        raise AssertionError(
            "conditioned CNF is not global CNF plus the 118 selectors"
        )

    drat_output = Path(
        "tmp/fourteen_vertex_c6_8_118_orbits_"
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
            "tmp/fourteen_vertex_c6_8_118_orbits_"
            "final_drat_trim_recheck.stdout.log",
            "--stderr",
            "tmp/fourteen_vertex_c6_8_118_orbits_"
            "final_drat_trim_recheck.stderr.log",
            "--output",
            str(drat_output),
            "--forward",
        ]
    )
    drat = json.loads(drat_output.read_text(encoding="utf-8"))
    if drat.get("verified") is not True:
        raise AssertionError("118-orbit DRAT replay changed")

    payload = {
        "verified": True,
        "status": "C6+C8_118_first_factor_orbits_excluded",
        "scope": (
            "order-14 equality architecture with full factor C6+C8 "
            "and a pinned first singleton factor in the listed 118 orbits"
        ),
        "predecessor_117_verified": True,
        "augmentation_layers_replayed": layer_records,
        "later_certificates_replayed": sum(
            int(row["certificates_replayed"])
            for row in layer_records
        ),
        "later_new_transport_clauses": sum(
            int(row["new_clauses"]) for row in layer_records
        ),
        "global_cnf": str(global_cnf),
        "global_cnf_sha256": sha256(global_cnf),
        "global_cnf_variables": global_formula.nv,
        "global_cnf_clauses": len(global_formula.clauses),
        "sat_first_factor_orbits": len(expected_sat),
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
