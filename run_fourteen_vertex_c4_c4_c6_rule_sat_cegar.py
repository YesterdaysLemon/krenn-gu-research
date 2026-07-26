"""Iteratively harvest simple C4+C4+C6 fork certificates with SAT.

The rule SAT compiler returns a support outside all supplied simple
transport certificates.  This driver analyzes that support, appends a new
simple certificate, and asks again.  It stops on UNSAT or on a residual
requiring a richer certificate.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--extra-samples",
        type=Path,
        action="append",
        default=[],
    )
    parser.add_argument(
        "--extra-analysis-pattern",
        action="append",
        default=[],
    )
    parser.add_argument("--rounds", type=int, default=50)
    parser.add_argument(
        "--prefix",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_cegar"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_cegar_chain.json"
        ),
    )
    args = parser.parse_args()
    if len(args.extra_samples) != len(
        args.extra_analysis_pattern
    ):
        raise ValueError(
            "each --extra-samples needs one --extra-analysis-pattern"
        )
    if args.rounds < 1:
        raise ValueError("--rounds must be positive")

    started = time.perf_counter()
    samples_path = Path(f"{args.prefix}_samples.json")
    analysis_pattern = f"{args.prefix}_{{index}}_factor_fork.json"
    sat_output = Path(f"{args.prefix}_current_sat.json")
    sat_sample = Path(f"{args.prefix}_current_sample.json")
    cnf_path = Path(f"{args.prefix}_current.cnf")
    survivors: list[dict[str, object]] = []
    iterations: list[dict[str, object]] = []
    terminal_status = "round_limit"

    for iteration in range(args.rounds):
        command = [
            sys.executable,
            "analyze_fourteen_vertex_c4_c4_c6_rule_sat.py",
        ]
        for samples, pattern in zip(
            args.extra_samples,
            args.extra_analysis_pattern,
            strict=True,
        ):
            command.extend(
                [
                    "--extra-samples",
                    str(samples),
                    "--extra-analysis-pattern",
                    pattern,
                ]
            )
        if survivors:
            command.extend(
                [
                    "--extra-samples",
                    str(samples_path),
                    "--extra-analysis-pattern",
                    analysis_pattern,
                ]
            )
        command.extend(
            [
                "--cnf",
                str(cnf_path),
                "--sample-output",
                str(sat_sample),
                "--output",
                str(sat_output),
            ]
        )
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        sat_result = json.loads(
            sat_output.read_text(encoding="utf-8")
        )
        if not sat_result["sat"]:
            iterations.append(
                {
                    "iteration": iteration,
                    "sat": False,
                    "transport_no_goods": sat_result[
                        "deduplicated_transport_no_goods"
                    ],
                    "cnf_clauses": sat_result["cnf_clauses"],
                }
            )
            terminal_status = "UNSAT"
            break

        sample_manifest = json.loads(
            sat_sample.read_text(encoding="utf-8")
        )
        survivor = sample_manifest["survivors"][0]
        survivors.append(survivor)
        samples_payload = {
            "status": "simple_rule_sat_cegar_samples",
            "partition": [4, 4, 6],
            "survivors": survivors,
            "exploratory_only": True,
        }
        samples_path.parent.mkdir(parents=True, exist_ok=True)
        samples_path.write_text(
            json.dumps(samples_payload, indent=2) + "\n",
            encoding="utf-8",
        )
        analysis_path = Path(
            analysis_pattern.format(index=len(survivors) - 1)
        )
        subprocess.run(
            [
                sys.executable,
                "analyze_fourteen_vertex_even_cycle_factor_fork.py",
                str(samples_path),
                "--survivor-index",
                str(len(survivors) - 1),
                "--output",
                str(analysis_path),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        analysis = json.loads(
            analysis_path.read_text(encoding="utf-8")
        )
        status = str(analysis["status"])
        row = {
            "iteration": iteration,
            "sat": True,
            "orbit_id": survivor["orbit_id"],
            "analysis_status": status,
            "transport_no_goods": sat_result[
                "deduplicated_transport_no_goods"
            ],
            "cnf_clauses": sat_result["cnf_clauses"],
        }
        iterations.append(row)
        print(json.dumps(row), flush=True)
        if status != "even_cycle_factor_fork":
            terminal_status = status
            break

    payload = {
        "status": terminal_status,
        "partition": [4, 4, 6],
        "iterations": iterations,
        "new_samples": len(survivors),
        "samples": str(samples_path),
        "analysis_pattern": analysis_pattern,
        "current_cnf": str(cnf_path),
        "current_sat_result": str(sat_output),
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_only": terminal_status != "UNSAT",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
