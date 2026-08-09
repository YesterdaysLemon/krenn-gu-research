"""Iterate independently checked mandatory-unit binomial support exclusions.

This is an orchestrator, not a verifier.  Each accepted support is checked by
the standalone branch verifier, and each DIMACS extension is reconstructed by
the standalone augmentation verifier before the next support is queried.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


PREFIX = "fourteen_vertex_c4_c4_c6"
CNF_STEM = (
    f"{PREFIX}_rule_sat_late_combined_v7_orbit8_partial2_"
    "minimal_circuits_kappa3"
)


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    print(f"[run] {' '.join(command)}", flush=True)
    result = subprocess.run(
        command,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.stdout:
        print(result.stdout.rstrip(), flush=True)
    return result


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-support", type=int, required=True)
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--maximum-support", type=int, default=40)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.start_support < 1:
        raise ValueError("start support must be positive")
    if args.maximum_support < args.start_support:
        raise ValueError("maximum support precedes start support")
    if not args.base_cnf.is_file():
        raise FileNotFoundError(args.base_cnf)

    started = time.perf_counter()
    current_cnf = args.base_cnf
    records: list[dict[str, object]] = []
    terminal: dict[str, object] = {
        "mode": "maximum_support_reached",
        "support": args.maximum_support + 1,
    }

    for support in range(args.start_support, args.maximum_support + 1):
        tag = f"{PREFIX}_orbit8_support{support}"
        partial = Path(
            "tmp",
            f"{PREFIX}_orbit8_partial_minimal_circuit_lattice_"
            f"support{support}.json",
        )
        analysis = Path(
            "tmp", f"{tag}_mandatory_unit_binomial_closure.json"
        )
        verified_support = Path(
            "tmp", f"{tag}_mandatory_unit_binomial_closure_verified.json"
        )
        output_cnf = Path("tmp", f"{CNF_STEM}_binomial{support}.cnf")
        augmentation = Path(
            "tmp", f"{PREFIX}_orbit8_binomial{support}_augmentation.json"
        )
        verified_augmentation = Path(
            "tmp",
            f"{PREFIX}_orbit8_binomial{support}_augmentation_verified.json",
        )

        analysis_result = run(
            [
                sys.executable,
                "analyze_fourteen_vertex_partial_minimal_circuit_lattice.py",
                "--cnf",
                str(current_cnf),
                "--partition",
                "4,4,6",
                "--orbit",
                "8",
                "--output",
                str(partial),
            ]
        )
        if analysis_result.returncode != 0:
            if "requested selector is UNSAT" in analysis_result.stdout:
                terminal = {
                    "mode": "selector_unsat",
                    "support": support,
                    "cnf": str(current_cnf),
                }
                break
            raise RuntimeError(
                f"support {support} analysis failed with "
                f"exit code {analysis_result.returncode}"
            )

        closure_result = run(
            [
                sys.executable,
                "analyze_fourteen_vertex_partial_circuit_binomial_closure.py",
                str(partial),
                "--select-mandatory-unit-core",
                "--output",
                str(analysis),
            ]
        )
        if closure_result.returncode != 0:
            raise RuntimeError(
                f"support {support} closure failed with "
                f"exit code {closure_result.returncode}"
            )
        closure = read_json(analysis)
        if (
            closure.get("status") != "contradiction"
            or closure.get("support_closed") is not True
            or closure.get("selected_mandatory_unit_core") is not True
        ):
            terminal = {
                "mode": "mandatory_unit_core_open",
                "support": support,
                "cnf": str(current_cnf),
                "partial_analysis": str(partial),
                "analysis": str(analysis),
                "analysis_status": closure.get("status"),
            }
            break

        verify_result = run(
            [
                sys.executable,
                "verify_fourteen_vertex_partial_circuit_binomial_branch.py",
                str(analysis),
                "--output",
                str(verified_support),
            ]
        )
        if verify_result.returncode != 0:
            raise RuntimeError(
                f"support {support} verification failed with "
                f"exit code {verify_result.returncode}"
            )
        verified = read_json(verified_support)
        if verified.get("verified") is not True:
            raise RuntimeError(f"support {support} verifier did not certify")

        augment_result = run(
            [
                sys.executable,
                "tools/generate/augment_fourteen_vertex_rule_cnf_with_binomial_support_closures.py",
                "--base-cnf",
                str(current_cnf),
                "--verified-support",
                str(verified_support),
                "--output-cnf",
                str(output_cnf),
                "--output",
                str(augmentation),
            ]
        )
        if augment_result.returncode != 0:
            raise RuntimeError(
                f"support {support} augmentation failed with "
                f"exit code {augment_result.returncode}"
            )

        audit_result = run(
            [
                sys.executable,
                "verify_fourteen_vertex_binomial_support_closure_augmentation.py",
                str(augmentation),
                "--output",
                str(verified_augmentation),
            ]
        )
        if audit_result.returncode != 0:
            raise RuntimeError(
                f"support {support} augmentation audit failed with "
                f"exit code {audit_result.returncode}"
            )
        audit = read_json(verified_augmentation)
        if audit.get("verified") is not True:
            raise RuntimeError(
                f"support {support} augmentation auditor did not certify"
            )

        augmentation_payload = read_json(augmentation)
        records.append(
            {
                "support": support,
                "partial_analysis": str(partial),
                "analysis": str(analysis),
                "verified_support": str(verified_support),
                "augmentation": str(augmentation),
                "verified_augmentation": str(verified_augmentation),
                "output_cnf": str(output_cnf),
                "output_cnf_sha256": augmentation_payload[
                    "output_cnf_sha256"
                ],
                "output_clauses": augmentation_payload["output_clauses"],
                "selected_initial_relations": verified[
                    "selected_initial_relations"
                ],
                "derived_relations": verified["derived_relations_checked"],
                "target_active_matchings": verified[
                    "target_active_matchings"
                ],
            }
        )
        current_cnf = output_cnf
        print(f"[certified] support {support}", flush=True)

    payload = {
        "status": "mandatory_unit_binomial_cegar_stopped",
        "scope": (
            "bounded C4+C4+C6 orbit-8 support iteration with independent "
            "support and DIMACS-extension audits"
        ),
        "start_support": args.start_support,
        "maximum_support": args.maximum_support,
        "initial_cnf": str(args.base_cnf),
        "certified_supports": len(records),
        "records": records,
        "terminal": terminal,
        "final_cnf": str(current_cnf),
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2), flush=True)


if __name__ == "__main__":
    main()
