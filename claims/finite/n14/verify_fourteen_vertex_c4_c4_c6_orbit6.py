"""Replay the C4+C4+C6 certificate excluding first-factor orbit 6."""

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



BASE_KAPPA3_SHA256 = (
    "e2d315a63071a22fc4ef148871a1dc52"
    "ae879c290f6e004c0b4a203c2e4aea07"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "late_combined_v3_orbit6_targeted_kappa3_augmentation.json"
        ),
    )
    parser.add_argument(
        "--augmentation-audit",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_"
            "late_combined_v3_orbit6_targeted_"
            "kappa3_augmentation_verified.json"
        ),
    )
    parser.add_argument(
        "--conditioned-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_"
            "orbit6_targeted_kappa3_conditioned.cnf"
        ),
    )
    parser.add_argument(
        "--proof",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_"
            "orbit6_targeted_kappa3_kissat.drat"
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
            "orbit6_final_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    augmentation = read_json(args.augmentation)
    stored_audit = read_json(args.augmentation_audit)
    base_cnf = Path(str(augmentation["base_cnf"]))
    global_cnf = Path(str(augmentation["output_cnf"]))
    prerequisite = augmentation.get("three_connectivity_prerequisite")
    if not isinstance(prerequisite, dict):
        raise AssertionError("orbit-6 connectivity prerequisite missing")
    prerequisite_manifest = Path(str(prerequisite["augmentation"]))
    prerequisite_audit = Path(str(prerequisite["audit"]))
    if (
        augmentation.get("status")
        != "minimum_activity_rules_augmented"
        or augmentation.get("partition") != [4, 4, 6]
        or augmentation.get("certificates_replayed") != 400
        or augmentation.get("new_transport_clauses") != 5824
        or sha256(base_cnf) != BASE_KAPPA3_SHA256
        or augmentation.get("base_cnf_sha256") != BASE_KAPPA3_SHA256
        or augmentation.get("output_cnf_sha256") != sha256(global_cnf)
        or augmentation.get("output_cnf_variables") != 324
        or augmentation.get("output_cnf_clauses") != 1094929
        or stored_audit.get("verified") is not True
        or stored_audit.get("augmentation_sha256")
        != sha256(args.augmentation)
        or prerequisite.get("base_extension_clauses") != 0
        or sha256(prerequisite_manifest)
        != prerequisite["augmentation_sha256"]
        or sha256(prerequisite_audit)
        != prerequisite["audit_sha256"]
    ):
        raise AssertionError("orbit-6 augmentation chain changed")

    recheck_path = Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit6_"
        "augmentation_recheck.json"
    )
    subprocess.run(
        [
            sys.executable,
            str(HERE / "verify_fourteen_vertex_two_even_cycle_minimum_activity_augmentation.py"),
            str(args.augmentation),
            "--output",
            str(recheck_path),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    recheck = read_json(recheck_path)
    if (
        recheck.get("verified") is not True
        or recheck.get("certificates_replayed") != 400
        or recheck.get("new_transport_clauses") != 5824
        or recheck.get("output_cnf_variables") != 324
        or recheck.get("output_cnf_clauses") != 1094929
        or recheck.get("sat") is not True
    ):
        raise AssertionError("orbit-6 augmentation replay changed")

    global_formula = CNF(from_file=str(global_cnf))
    conditioned_formula = CNF(from_file=str(args.conditioned_cnf))
    selector_clause = [238]
    if conditioned_formula.clauses != [
        *global_formula.clauses,
        selector_clause,
    ]:
        raise AssertionError(
            "conditioned CNF is not the global CNF plus selector 238"
        )

    drat_path = Path(
        "tmp/fourteen_vertex_c4_c4_c6_orbit6_"
        "final_drat_trim_recheck.json"
    )
    subprocess.run(
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
            "tmp/fourteen_vertex_c4_c4_c6_orbit6_"
            "final_drat_trim_recheck.stdout.log",
            "--stderr",
            "tmp/fourteen_vertex_c4_c4_c6_orbit6_"
            "final_drat_trim_recheck.stderr.log",
            "--output",
            str(drat_path),
            "--forward",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    if read_json(drat_path).get("verified") is not True:
        raise AssertionError("orbit-6 DRAT replay changed")

    payload = {
        "verified": True,
        "status": "C4+C4+C6_first_factor_orbit_6_excluded",
        "scope": (
            "order-14 equality architecture with full factor C4+C4+C6, "
            "skeleton vertex connectivity at least 3, and pinned first "
            "singleton factor orbit 6"
        ),
        "minimal_counterexample_relevance": (
            "a minimal Krenn-Gu counterexample must be 4-connected "
            "(Chandran-Gajjala-Illickan, arXiv:2407.00303)"
        ),
        "base_kappa3_cnf": str(base_cnf),
        "base_kappa3_cnf_sha256": sha256(base_cnf),
        "orbit6_certificates_replayed": 400,
        "orbit6_new_transport_clauses": 5824,
        "global_cnf": str(global_cnf),
        "global_cnf_sha256": sha256(global_cnf),
        "global_cnf_variables": global_formula.nv,
        "global_cnf_clauses": len(global_formula.clauses),
        "excluded_first_factor_orbit": 6,
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
