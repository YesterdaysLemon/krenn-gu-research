"""Independently reconstruct one-extra cycle-core activation rules."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Solver

from verify_fourteen_vertex_two_even_cycle_rule_cnf import (
    N,
    automorphisms,
    certificate_no_goods,
    cycle_edge_set,
    cycles_for,
    indexed_colouring,
    parse_factor,
)
from verify_fourteen_vertex_two_even_cycle_minimum_activity_augmentation import (
    independently_transport,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("augmentation", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    manifest = json.loads(
        args.augmentation.read_text(encoding="utf-8")
    )
    if (
        manifest.get("status")
        != "verified_one_extra_cycle_rules_augmented"
    ):
        raise AssertionError("augmentation status changed")
    compiled_path = Path(manifest["compiled_result"])
    census_path = Path(manifest["census"])
    base_path = Path(manifest["base_cnf"])
    output_path = Path(manifest["output_cnf"])
    for path, key in (
        (compiled_path, "compiled_result_sha256"),
        (census_path, "census_sha256"),
        (base_path, "base_cnf_sha256"),
        (output_path, "output_cnf_sha256"),
    ):
        if sha256(path) != manifest[key]:
            raise AssertionError(f"source hash changed: {path}")
    compiled = json.loads(compiled_path.read_text(encoding="utf-8"))
    census = json.loads(census_path.read_text(encoding="utf-8"))
    lengths = tuple(map(int, compiled["partition"]))
    if (
        list(lengths) != manifest["partition"]
        or tuple(map(int, census["partition"])) != lengths
        or sum(lengths) != N
        or any(length % 2 for length in lengths)
    ):
        raise AssertionError("partition changed")
    cycles = cycles_for(lengths)
    full_edges = cycle_edge_set(cycles)
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    representatives = tuple(
        parse_factor(row["representative"])
        for row in census["factor_orbits"]
    )
    representative_id = {
        factor: index for index, factor in enumerate(representatives)
    }
    selectors = tuple(
        3 * len(eligible_edges) + 1 + index
        for index in range(len(representatives))
    )
    actions = automorphisms(cycles)
    if len(actions) != int(census["full_automorphisms"]):
        raise AssertionError("automorphism count changed")

    base = CNF(from_file=str(base_path))
    known = {
        tuple(
            sorted(
                set(map(int, clause)),
                key=lambda item: (abs(item), item),
            )
        )
        for clause in base.clauses
    }
    reconstructed: set[tuple[int, ...]] = set()
    for record in manifest["certificate_records"]:
        certificate_path = Path(record["certificate"])
        audit_path = Path(record["audit"])
        if (
            record.get("mode")
            != "verified_one_extra_cycle_activation_core"
            or sha256(certificate_path)
            != record["certificate_sha256"]
            or sha256(audit_path) != record["audit_sha256"]
        ):
            raise AssertionError("certificate record changed")
        proof = json.loads(
            certificate_path.read_text(encoding="utf-8")
        )
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        if (
            proof.get("status") != "one_extra_cycle_core"
            or tuple(map(int, proof["full_cycle_type"])) != lengths
            or audit.get("verified") is not True
            or audit.get("status") != "one_extra_cycle_core_verified"
            or audit.get("certificate_sha256")
            != sha256(certificate_path)
        ):
            raise AssertionError("one-extra certificate changed")
        factors = tuple(
            parse_factor(proof["singleton_matchings"][key])
            for key in ("first", "second", "third")
        )
        certificate = proof["certificate"]
        equations = [
            int(certificate["full_only_equation_index"]),
            *[
                int(row["one_extra_equation_index"])
                for row in certificate["cycle_rows"]
            ],
        ]
        equations = list(dict.fromkeys(equations))
        if equations != list(
            map(int, record["activation_equations"])
        ):
            raise AssertionError("activation equation list changed")
        activation_mode = record.get(
            "activation_mode", "exact_activity_mask"
        )
        if activation_mode == "three_connected_minimum_activity":
            minimum_path = Path(record["minimum_activity"])
            minimum_audit_path = Path(
                record["minimum_activity_audit"]
            )
            if (
                sha256(minimum_path)
                != record["minimum_activity_sha256"]
                or sha256(minimum_audit_path)
                != record["minimum_activity_audit_sha256"]
            ):
                raise AssertionError(
                    "minimum activation source hash changed"
                )
            minimum = json.loads(
                minimum_path.read_text(encoding="utf-8")
            )
            minimum_audit = json.loads(
                minimum_audit_path.read_text(encoding="utf-8")
            )
            minimum_factors = tuple(
                parse_factor(minimum["singleton_matchings"][key])
                for key in ("first", "second", "third")
            )
            if (
                minimum.get("status")
                != "fourteen_vertex_minimum_activity_certificate"
                or minimum.get("analysis_sha256")
                != sha256(certificate_path)
                or minimum_factors != factors
                or list(map(int, minimum["equations"])) != equations
                or minimum.get("activity_scope")
                != "three_connected_perfect_matching_edge_disjoint"
                or int(minimum["activation_constraint_score"])
                != int(record["minimum_activity_score"])
                or minimum_audit.get("verified") is not True
                or minimum_audit.get("status")
                != "fourteen_vertex_minimum_activity_"
                "certificate_verified"
                or minimum_audit.get("certificate_sha256")
                != sha256(minimum_path)
            ):
                raise AssertionError(
                    "minimum activation certificate changed"
                )
            clauses = independently_transport(
                factors,
                minimum["activation_conditions"],
                representative_id,
                selectors,
                actions,
                eligible_edges,
            )
        elif activation_mode == "exact_activity_mask":
            clauses = certificate_no_goods(
                factors,
                tuple(
                    indexed_colouring(value) for value in equations
                ),
                representative_id,
                selectors,
                actions,
                eligible_edges,
            )
        else:
            raise AssertionError("activation mode changed")
        if (
            representative_id[factors[0]]
            != int(record["first_factor_orbit"])
            or len(clauses) != int(record["transport_clauses"])
            or sorted({len(clause) for clause in clauses})
            != list(map(int, record["transport_clause_widths"]))
        ):
            raise AssertionError("transport metadata changed")
        new = clauses - known - reconstructed
        if len(new) != int(record["new_no_goods"]):
            raise AssertionError("transport deduplication changed")
        reconstructed.update(new)

    observed = CNF(from_file=str(output_path))
    expected = [
        *base.clauses,
        *[list(clause) for clause in sorted(reconstructed)],
    ]
    if (
        observed.clauses != expected
        or len(base.clauses) != int(manifest["base_clauses"])
        or len(reconstructed) != int(manifest["new_no_goods"])
        or len(observed.clauses) != int(manifest["output_clauses"])
    ):
        raise AssertionError("output CNF reconstruction changed")
    with Solver(
        name="cadical195", bootstrap_with=observed.clauses
    ) as solver:
        sat = solver.solve()
    output = {
        "verified": True,
        "status": "one_extra_cycle_augmentation_reconstructed",
        "scope": (
            "all source hashes, activation-mask symmetry transport, "
            "deduplication, exact clauses, and independent SAT status"
        ),
        "augmentation": str(args.augmentation),
        "augmentation_sha256": sha256(args.augmentation),
        "partition": list(lengths),
        "certificates_replayed": len(
            manifest["certificate_records"]
        ),
        "new_transport_no_goods": len(reconstructed),
        "output_cnf_variables": observed.nv,
        "output_cnf_clauses": len(observed.clauses),
        "independent_solver": "cadical195",
        "sat": sat,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
