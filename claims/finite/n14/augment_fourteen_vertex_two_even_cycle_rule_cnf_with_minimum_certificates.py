"""Augment an even-cycle rule CNF with verified minimum-activity rules."""

from __future__ import annotations

import argparse
import glob
import hashlib
import itertools
import json
import time
from pathlib import Path

from pysat.formula import CNF

from analyze_fourteen_vertex_two_even_cycle_rule_sat import parse_factor
from explore_fourteen_vertex_equality_factor_family import (
    contiguous_cycles,
    full_automorphisms,
)
from explore_random_even_cycle_forks import cycle_edges
from run_fourteen_vertex_two_even_cycle_rule_sat_incremental import (
    minimum_condition_no_goods,
)

N = 14


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def certificate_paths(
    explicit: list[Path],
    patterns: list[str],
    manifests: list[Path],
) -> list[Path]:
    output = {path.resolve(): path for path in explicit}
    for pattern in patterns:
        for raw in glob.glob(pattern):
            path = Path(raw)
            output.setdefault(path.resolve(), path)
    for manifest_path in manifests:
        manifest = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
        if (
            manifest.get("status")
            != "minimum_activity_rules_augmented"
        ):
            raise AssertionError(
                "certificate manifest status changed"
            )
        for row in manifest["minimum_certificates"]:
            path = Path(row["certificate"])
            output.setdefault(path.resolve(), path)
    return sorted(output.values(), key=lambda path: str(path))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--compiled-result", type=Path, required=True)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument(
        "--certificate", type=Path, action="append", default=[]
    )
    parser.add_argument(
        "--certificate-glob", action="append", default=[]
    )
    parser.add_argument(
        "--certificate-manifest",
        type=Path,
        action="append",
        default=[],
        help=(
            "reuse the minimum-certificate path catalogue from an "
            "existing augmentation manifest"
        ),
    )
    parser.add_argument(
        "--three-connectivity-augmentation",
        type=Path,
        help=(
            "required when replaying certificates minimized relative to "
            "vertex connectivity at least 3"
        ),
    )
    parser.add_argument(
        "--three-connectivity-audit",
        type=Path,
        help=(
            "independent reconstruction paired with "
            "--three-connectivity-augmentation"
        ),
    )
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()

    compiled = json.loads(
        args.compiled_result.read_text(encoding="utf-8")
    )
    census = json.loads(args.census.read_text(encoding="utf-8"))
    lengths = tuple(map(int, compiled["partition"]))
    if (
        not lengths
        or sum(lengths) != N
        or any(length % 2 for length in lengths)
        or tuple(map(int, census["partition"])) != lengths
    ):
        raise AssertionError("even-cycle partition changed")
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item
        for cycle in cycles
        for item in cycle_edges(cycle)
    }
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    representatives = [
        parse_factor(row["representative"])
        for row in census["factor_orbits"]
    ]
    if len(representatives) != int(compiled["first_factor_orbits"]):
        raise AssertionError("first-factor orbit census changed")
    representative_id = {
        factor: index for index, factor in enumerate(representatives)
    }
    edge_variables = 3 * len(eligible_edges)
    selector_variables = [
        edge_variables + 1 + index
        for index in range(len(representatives))
    ]
    actions = full_automorphisms(cycles)
    cnf = CNF(from_file=str(args.base_cnf))
    known_clauses = {
        tuple(
            sorted(set(clause), key=lambda item: (abs(item), item))
        )
        for clause in cnf.clauses
    }
    paths = certificate_paths(
        args.certificate,
        args.certificate_glob,
        args.certificate_manifest,
    )
    if not paths:
        raise ValueError("at least one minimum certificate is required")

    three_connectivity_prerequisite = None
    if (
        args.three_connectivity_augmentation is not None
        or args.three_connectivity_audit is not None
    ):
        if (
            args.three_connectivity_augmentation is None
            or args.three_connectivity_audit is None
        ):
            raise ValueError(
                "both three-connectivity prerequisite files are required"
            )
        prerequisite = json.loads(
            args.three_connectivity_augmentation.read_text(
                encoding="utf-8"
            )
        )
        prerequisite_audit = json.loads(
            args.three_connectivity_audit.read_text(encoding="utf-8")
        )
        prerequisite_cnf = Path(prerequisite["output_cnf"])
        prerequisite_formula = CNF(from_file=str(prerequisite_cnf))
        prerequisite_is_prefix = cnf.clauses[
            : len(prerequisite_formula.clauses)
        ] == prerequisite_formula.clauses
        if (
            prerequisite.get("status")
            != "three_vertex_connectivity_condition_augmented"
            or prerequisite["output_cnf_sha256"]
            != sha256(prerequisite_cnf)
            or not prerequisite_is_prefix
            or prerequisite_audit.get("verified") is not True
            or prerequisite_audit.get("status")
            != "three_vertex_connectivity_augmentation_reconstructed"
            or prerequisite_audit.get("augmentation_sha256")
            != sha256(args.three_connectivity_augmentation)
        ):
            raise AssertionError(
                "three-connectivity prerequisite did not verify"
            )
        three_connectivity_prerequisite = {
            "augmentation": str(
                args.three_connectivity_augmentation
            ),
            "augmentation_sha256": sha256(
                args.three_connectivity_augmentation
            ),
            "audit": str(args.three_connectivity_audit),
            "audit_sha256": sha256(args.three_connectivity_audit),
            "base_extension_clauses": (
                len(cnf.clauses)
                - len(prerequisite_formula.clauses)
            ),
        }

    rows: list[dict[str, object]] = []
    all_new: set[tuple[int, ...]] = set()
    for path in paths:
        certificate = json.loads(path.read_text(encoding="utf-8"))
        if certificate.get("status") not in {
            "two_even_cycle_minimum_activity_certificate",
            "fourteen_vertex_minimum_activity_certificate",
        }:
            raise AssertionError("minimum certificate status changed")
        if tuple(map(int, certificate["partition"])) != lengths:
            raise AssertionError("minimum certificate partition changed")
        if (
            certificate.get("activity_scope")
            == "three_connected_perfect_matching_edge_disjoint"
            and three_connectivity_prerequisite is None
        ):
            raise AssertionError(
                "three-connected certificate lacks a verified base "
                "prerequisite"
            )
        audit_path = path.with_name(
            f"{path.stem}_verified{path.suffix}"
        )
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        if (
            audit.get("verified") is not True
            or audit.get("status")
            != "fourteen_vertex_minimum_activity_certificate_verified"
            or audit.get("certificate_sha256") != sha256(path)
        ):
            raise AssertionError(
                "minimum activity audit provenance changed"
            )
        factors = tuple(
            parse_factor(certificate["singleton_matchings"][key])
            for key in ("first", "second", "third")
        )
        generated = minimum_condition_no_goods(
            factors,
            certificate["activation_conditions"],
            representative_id,
            selector_variables,
            actions,
            eligible_edges,
        )
        new_clauses = generated - known_clauses - all_new
        all_new.update(new_clauses)
        rows.append(
            {
                "certificate": str(path),
                "certificate_sha256": sha256(path),
                "audit": str(audit_path),
                "audit_sha256": sha256(audit_path),
                "source_first_factor_orbit": representative_id[
                    factors[0]
                ],
                "activation_constraint_score": int(
                    certificate["activation_constraint_score"]
                ),
                "transport_clauses": len(generated),
                "new_transport_clauses": len(new_clauses),
            }
        )

    for clause in sorted(all_new):
        cnf.append(list(clause))
    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    cnf.to_file(str(args.output_cnf))
    payload = {
        "status": "minimum_activity_rules_augmented",
        "partition": list(lengths),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "compiled_result": str(args.compiled_result),
        "compiled_result_sha256": sha256(args.compiled_result),
        "census": str(args.census),
        "census_sha256": sha256(args.census),
        "minimum_certificates": rows,
        "three_connectivity_prerequisite": (
            three_connectivity_prerequisite
        ),
        "certificates_replayed": len(rows),
        "new_transport_clauses": len(all_new),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "output_cnf_variables": cnf.nv,
        "output_cnf_clauses": len(cnf.clauses),
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_until_independently_reconstructed": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
