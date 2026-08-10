"""Replay the order-14 C6+C8 certificate excluding 130 kappa>=3 orbits."""

from __future__ import annotations

import argparse
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from verify_fourteen_vertex_c6_8_kappa3_extension_step import Step, verify_step


STEP = Step(
    excluded_orbits=130,
    new_orbit=16,
    predecessor_script="claims/finite/n14/verify_fourteen_vertex_c6_8_129_orbits_kappa3.py",
    predecessor_status="C6+C8_kappa3_129_first_factor_orbits_excluded",
    predecessor_cnf_sha256=(
        "691b58cf5e7190113938e8f5467619cf"
        "b16b116c93b0848743a125c1f615fb28"
    ),
    certificates=64,
    new_clauses=268,
    base_extension_clauses=4040,
    global_cnf_sha256=(
        "6bef527f14379520ecdfa595d51e0d8ca"
        "d8563014fe9fe09968a5d8901fb1d6a"
    ),
    global_cnf_clauses=130918,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--augmentation",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_"
            "v29_orbit16_targeted_augmentation.json"
        ),
    )
    parser.add_argument(
        "--conditioned-cnf",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_130_orbits_"
            "v29_kappa3_conditioned.cnf"
        ),
    )
    parser.add_argument(
        "--proof",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c6_8_130_orbits_"
            "v29_kappa3_kissat.drat"
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
            "tmp/fourteen_vertex_c6_8_130_orbits_"
            "kappa3_final_verified.json"
        ),
    )
    args = parser.parse_args()
    verify_step(
        STEP,
        augmentation_path=args.augmentation,
        conditioned_cnf=args.conditioned_cnf,
        proof=args.proof,
        drat_trim=args.drat_trim,
        output=args.output,
    )


if __name__ == "__main__":
    main()
