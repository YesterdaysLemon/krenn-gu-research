"""Replay the certificate excluding C4+C4+C6 first-factor orbit 8."""

from __future__ import annotations

import argparse
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

from verify_fourteen_vertex_c4_c4_c6_orbit6 import read_json, sha256


BASE_CNF = Path(
    "tmp/fourteen_vertex_c4_c4_c6_rule_sat_late_combined_v7_"
    "orbit8_partial2_minimal_circuits_kappa3.cnf"
)
FRONTIER_AUDIT = Path(
    "tmp/fourteen_vertex_minimal_circuit_frontiers_verified.json"
)
CHAIN_CERTIFICATES = (
    (
        Path(
            "tmp/fourteen_vertex_c4_c4_c6_orbit8_"
            "partial_binomial_selection_cegar_minimal_v5.json"
        ),
        128,
    ),
    (
        Path(
            "tmp/fourteen_vertex_c4_c4_c6_orbit8_"
            "support2_partial_binomial_selection_cegar.json"
        ),
        32,
    ),
)
MANDATORY_CERTIFICATES = (
    Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit8_"
        "support3_mandatory_unit_binomial_closure.json"
    ),
    Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit8_"
        "symmetry_support2_mandatory_unit_binomial_closure.json"
    ),
    Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit8_"
        "symmetry_support3_mandatory_unit_binomial_closure.json"
    ),
)
AUGMENTATIONS = (
    (
        Path(
            "tmp/fourteen_vertex_c4_c4_c6_orbit8_"
            "binomial1_augmentation.json"
        ),
        False,
        1,
    ),
    (
        Path(
            "tmp/fourteen_vertex_c4_c4_c6_orbit8_"
            "binomial2_augmentation.json"
        ),
        False,
        1,
    ),
    (
        Path(
            "tmp/fourteen_vertex_c4_c4_c6_orbit8_"
            "support3_symmetry_augmentation.json"
        ),
        True,
        16,
    ),
    (
        Path(
            "tmp/fourteen_vertex_c4_c4_c6_orbit8_"
            "symmetry_support2_augmentation.json"
        ),
        True,
        15,
    ),
    (
        Path(
            "tmp/fourteen_vertex_c4_c4_c6_orbit8_"
            "symmetry_support3_augmentation.json"
        ),
        True,
        15,
    ),
)


def run_quiet(command: list[str]) -> None:
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--conditioned-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_"
            "orbit8_symbinomial3_conditioned.cnf"
        ),
    )
    parser.add_argument(
        "--proof",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_"
            "orbit8_symbinomial3_kissat.drat"
        ),
    )
    parser.add_argument(
        "--kissat-record",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_"
            "orbit8_symbinomial3_kissat.json"
        ),
    )
    parser.add_argument(
        "--drat-trim",
        type=Path,
        default=Path("tmp/drat-trim/drat-trim"),
    )
    parser.add_argument(
        "--full-support-replay",
        action="store_true",
        help=(
            "freshly replay both selection chains and all three "
            "mandatory-unit closures before the augmentation audits"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_"
            "orbit8_final_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    frontier = read_json(FRONTIER_AUDIT)
    frontier_row = frontier.get("C4+C4+C6")
    if (
        frontier.get("verified") is not True
        or frontier.get("status")
        != "fourteen_vertex_minimal_circuit_frontiers_verified"
        or not isinstance(frontier_row, dict)
        or frontier_row.get("global_cnf_sha256") != sha256(BASE_CNF)
        or frontier_row.get("remaining_orbits") is None
        or 8 not in frontier_row["remaining_orbits"]
    ):
        raise AssertionError("minimal-circuit frontier binding changed")

    chain_branches = 0
    mandatory_replays = 0
    if args.full_support_replay:
        for index, (chain_path, expected_branches) in enumerate(
            CHAIN_CERTIFICATES, start=1
        ):
            recheck = Path(
                "tmp",
                f"fourteen_vertex_c4_c4_c6_orbit8_"
                f"final_chain{index}_recheck.json",
            )
            run_quiet(
                [
                    sys.executable,
                    str(HERE / "verify_fourteen_vertex_partial_circuit_binomial_selection_chain.py"),
                    str(chain_path),
                    "--output",
                    str(recheck),
                ]
            )
            replay = read_json(recheck)
            if (
                replay.get("verified") is not True
                or replay.get("status")
                != "partial_circuit_binomial_selection_chain_verified"
                or replay.get("support_closed") is not True
                or replay.get("terminal_relation_selection_sat") is not False
                or int(replay["records_checked"]) != expected_branches
            ):
                raise AssertionError(
                    f"selection chain {index} replay changed"
                )
            chain_branches += expected_branches

        for index, analysis_path in enumerate(
            MANDATORY_CERTIFICATES, start=1
        ):
            recheck = Path(
                "tmp",
                f"fourteen_vertex_c4_c4_c6_orbit8_"
                f"final_mandatory{index}_recheck.json",
            )
            run_quiet(
                [
                    sys.executable,
                    str(HERE / "verify_fourteen_vertex_partial_circuit_binomial_branch.py"),
                    str(analysis_path),
                    "--output",
                    str(recheck),
                ]
            )
            replay = read_json(recheck)
            if (
                replay.get("verified") is not True
                or replay.get("status")
                != "partial_circuit_binomial_support_verified"
                or replay.get("support_closed") is not True
                or int(replay["selected_initial_relations"]) != 4
                or int(replay["derived_relations_checked"]) != 4
                or int(replay["final_lattice_rank"]) != 8
            ):
                raise AssertionError(
                    f"mandatory-unit support {index} replay changed"
                )
            mandatory_replays += 1

    predecessor = BASE_CNF
    total_new_no_goods = 0
    symmetry_no_goods = 0
    for index, (
        augmentation_path,
        expected_symmetry,
        expected_new,
    ) in enumerate(AUGMENTATIONS, start=1):
        augmentation = read_json(augmentation_path)
        output_cnf = Path(str(augmentation["output_cnf"]))
        if (
            augmentation.get("status")
            != "verified_binomial_support_no_goods_augmented"
            or Path(str(augmentation["base_cnf"])).resolve()
            != predecessor.resolve()
            or augmentation.get("base_cnf_sha256")
            != sha256(predecessor)
            or augmentation.get("output_cnf_sha256")
            != sha256(output_cnf)
            or int(augmentation["output_variables"]) != 324
            or bool(
                augmentation.get("stabilizer_orbit_closure", False)
            )
            != expected_symmetry
            or int(augmentation["new_support_no_goods"])
            != expected_new
        ):
            raise AssertionError(f"augmentation {index} binding changed")
        recheck = Path(
            "tmp",
            f"fourteen_vertex_c4_c4_c6_orbit8_"
            f"final_augmentation{index}_recheck.json",
        )
        run_quiet(
            [
                sys.executable,
                str(HERE / "verify_fourteen_vertex_binomial_support_closure_augmentation.py"),
                str(augmentation_path),
                "--output",
                str(recheck),
            ]
        )
        replay = read_json(recheck)
        if (
            replay.get("verified") is not True
            or replay.get("status")
            != "binomial_support_closure_augmentation_verified"
            or int(replay["new_support_no_goods"]) != expected_new
            or bool(replay["stabilizer_orbit_closure"])
            != expected_symmetry
            or replay.get("output_cnf_sha256") != sha256(output_cnf)
        ):
            raise AssertionError(
                f"augmentation {index} reconstruction changed"
            )
        total_new_no_goods += expected_new
        if expected_symmetry:
            symmetry_no_goods += expected_new
        predecessor = output_cnf

    final_cnf = predecessor
    final_formula = CNF(from_file=str(final_cnf))
    conditioned_formula = CNF(from_file=str(args.conditioned_cnf))
    selector_clause = [240]
    if conditioned_formula.clauses != [
        *final_formula.clauses,
        selector_clause,
    ]:
        raise AssertionError(
            "conditioned CNF is not the final CNF plus selector 240"
        )

    kissat = read_json(args.kissat_record)
    if (
        kissat.get("status") != "UNSAT"
        or int(kissat["returncode"]) != 20
        or Path(str(kissat["cnf"])).resolve()
        != args.conditioned_cnf.resolve()
        or kissat.get("cnf_sha256") != sha256(args.conditioned_cnf)
        or Path(str(kissat["proof"])).resolve() != args.proof.resolve()
        or kissat.get("proof_sha256") != sha256(args.proof)
        or int(kissat["proof_bytes"]) != args.proof.stat().st_size
    ):
        raise AssertionError("Kissat proof record changed")

    drat_path = Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit8_"
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
            "tmp/fourteen_vertex_c4_c4_c6_orbit8_"
            "final_drat_trim_recheck.stdout.log",
            "--stderr",
            "tmp/fourteen_vertex_c4_c4_c6_orbit8_"
            "final_drat_trim_recheck.stderr.log",
            "--output",
            str(drat_path),
            "--forward",
        ]
    )
    drat = read_json(drat_path)
    if (
        drat.get("verified") is not True
        or drat.get("cnf_sha256") != sha256(args.conditioned_cnf)
        or drat.get("proof_sha256") != sha256(args.proof)
    ):
        raise AssertionError("orbit-8 DRAT replay changed")

    payload = {
        "verified": True,
        "status": "C4+C4+C6_first_factor_orbit_8_excluded",
        "scope": (
            "order-14 equality architecture with full factor C4+C4+C6, "
            "skeleton vertex connectivity at least 3, and pinned first "
            "singleton factor orbit 8"
        ),
        "minimal_counterexample_relevance": (
            "a minimal Krenn-Gu counterexample must be 4-connected "
            "(Chandran-Gajjala-Illickan, arXiv:2407.00303)"
        ),
        "predecessor_minimal_circuit_frontier_bound": True,
        "full_support_replay": args.full_support_replay,
        "selection_branches_replayed": chain_branches,
        "mandatory_unit_supports_replayed": mandatory_replays,
        "augmentations_reconstructed": len(AUGMENTATIONS),
        "new_support_no_goods": total_new_no_goods,
        "symmetry_closed_new_support_no_goods": symmetry_no_goods,
        "global_cnf": str(final_cnf),
        "global_cnf_sha256": sha256(final_cnf),
        "global_cnf_variables": final_formula.nv,
        "global_cnf_clauses": len(final_formula.clauses),
        "excluded_first_factor_orbit": 8,
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
