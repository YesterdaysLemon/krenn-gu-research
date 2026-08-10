"""Independently reconstruct an even-cycle minimum-activity augmentation."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path
from typing import Sequence

from pysat.formula import CNF
from pysat.solvers import Solver

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from analyze_fourteen_vertex_two_even_cycle_rule_sat import (
    Factor,
    edge_variable,
    parse_factor,
    transform_factor,
)
from explore_fourteen_vertex_equality_factor_family import (
    N,
    contiguous_cycles,
    full_automorphisms,
)
from krenn_gu.explore_random_even_cycle_forks import cycle_edges

Edge = tuple[int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def independently_transport(
    factors: Sequence[Factor],
    raw_conditions: Sequence[Sequence[object]],
    representative_id: dict[Factor, int],
    selector_variables: Sequence[int],
    actions: Sequence[dict[int, int]],
    eligible_edges: Sequence[Edge],
) -> set[tuple[int, ...]]:
    first_orbit = representative_id.get(factors[0])
    if first_orbit is None:
        raise AssertionError("source first factor is not representative")
    selector = selector_variables[first_orbit]
    edge_id = {
        item: index for index, item in enumerate(eligible_edges)
    }
    decoded: list[tuple[int, Edge, bool]] = []
    for raw_variable, raw_value in raw_conditions:
        zero = int(raw_variable) - 1
        role, item_id = divmod(zero, len(eligible_edges))
        if role not in (1, 2) or item_id >= len(eligible_edges):
            raise AssertionError("minimum condition variable changed")
        decoded.append(
            (role, eligible_edges[item_id], bool(raw_value))
        )
    output: set[tuple[int, ...]] = set()
    for action in actions:
        if transform_factor(factors[0], action) != factors[0]:
            continue
        for role_swap in (False, True):
            moved: dict[int, bool] = {}
            for role, item, value in decoded:
                moved_role = 3 - role if role_swap else role
                moved_item = tuple(
                    sorted((action[item[0]], action[item[1]]))
                )
                variable = edge_variable(
                    moved_role,
                    edge_id[moved_item],
                    len(eligible_edges),
                )
                previous = moved.get(variable)
                if previous is not None and previous != value:
                    raise AssertionError(
                        "transported minimum conditions conflict"
                    )
                moved[variable] = value
            clause = {
                -selector,
                *(
                    -variable if value else variable
                    for variable, value in moved.items()
                ),
            }
            if any(-literal in clause for literal in clause):
                raise AssertionError("transport clause is tautological")
            output.add(
                tuple(
                    sorted(
                        clause, key=lambda item: (abs(item), item)
                    )
                )
            )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("augmentation", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    manifest = json.loads(
        args.augmentation.read_text(encoding="utf-8")
    )
    if manifest.get("status") != "minimum_activity_rules_augmented":
        raise AssertionError("augmentation status changed")

    base_path = Path(manifest["base_cnf"])
    compiled_path = Path(manifest["compiled_result"])
    census_path = Path(manifest["census"])
    output_cnf_path = Path(manifest["output_cnf"])
    for path, key in (
        (base_path, "base_cnf_sha256"),
        (compiled_path, "compiled_result_sha256"),
        (census_path, "census_sha256"),
        (output_cnf_path, "output_cnf_sha256"),
    ):
        if sha256(path) != manifest[key]:
            raise AssertionError(f"augmentation input changed: {path}")

    compiled = json.loads(compiled_path.read_text(encoding="utf-8"))
    census = json.loads(census_path.read_text(encoding="utf-8"))
    lengths = tuple(map(int, manifest["partition"]))
    if (
        tuple(map(int, compiled["partition"])) != lengths
        or tuple(map(int, census["partition"])) != lengths
        or not lengths
        or sum(lengths) != N
        or any(length % 2 for length in lengths)
    ):
        raise AssertionError("augmentation partition changed")
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
    representative_id = {
        factor: index for index, factor in enumerate(representatives)
    }
    selector_variables = [
        3 * len(eligible_edges) + 1 + index
        for index in range(len(representatives))
    ]
    actions = full_automorphisms(cycles)
    base = CNF(from_file=str(base_path))
    expected = [list(clause) for clause in base.clauses]
    known = {
        tuple(
            sorted(set(clause), key=lambda item: (abs(item), item))
        )
        for clause in base.clauses
    }
    all_new: set[tuple[int, ...]] = set()
    reconstructed_rows = []
    used_three_connected_scope = False
    for row in manifest["minimum_certificates"]:
        certificate_path = Path(row["certificate"])
        audit_path = Path(row["audit"])
        if (
            sha256(certificate_path) != row["certificate_sha256"]
            or sha256(audit_path) != row["audit_sha256"]
        ):
            raise AssertionError("certificate provenance changed")
        certificate = json.loads(
            certificate_path.read_text(encoding="utf-8")
        )
        if (
            certificate.get("activity_scope")
            == "three_connected_perfect_matching_edge_disjoint"
        ):
            used_three_connected_scope = True
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        if (
            audit.get("verified") is not True
            or audit.get("status")
            != "fourteen_vertex_minimum_activity_certificate_verified"
            or audit.get("certificate_sha256")
            != row["certificate_sha256"]
        ):
            raise AssertionError("minimum audit no longer verifies")
        factors = tuple(
            parse_factor(certificate["singleton_matchings"][key])
            for key in ("first", "second", "third")
        )
        generated = independently_transport(
            factors,
            certificate["activation_conditions"],
            representative_id,
            selector_variables,
            actions,
            eligible_edges,
        )
        new_clauses = generated - known - all_new
        if (
            int(row["source_first_factor_orbit"])
            != representative_id[factors[0]]
            or int(row["transport_clauses"]) != len(generated)
            or int(row["new_transport_clauses"])
            != len(new_clauses)
        ):
            raise AssertionError(
                "recorded minimum transport counts changed"
            )
        all_new.update(new_clauses)
        reconstructed_rows.append(
            {
                "certificate": str(certificate_path),
                "transport_clauses": len(generated),
                "new_transport_clauses": len(new_clauses),
            }
        )
    prerequisite = manifest.get("three_connectivity_prerequisite")
    if used_three_connected_scope:
        if not prerequisite:
            raise AssertionError(
                "three-connected certificates lack a base prerequisite"
            )
        prerequisite_path = Path(prerequisite["augmentation"])
        prerequisite_audit_path = Path(prerequisite["audit"])
        if (
            sha256(prerequisite_path)
            != prerequisite["augmentation_sha256"]
            or sha256(prerequisite_audit_path)
            != prerequisite["audit_sha256"]
        ):
            raise AssertionError(
                "three-connectivity prerequisite hash changed"
            )
        prerequisite_data = json.loads(
            prerequisite_path.read_text(encoding="utf-8")
        )
        prerequisite_audit = json.loads(
            prerequisite_audit_path.read_text(encoding="utf-8")
        )
        prerequisite_cnf_path = Path(
            prerequisite_data["output_cnf"]
        )
        prerequisite_formula = CNF(
            from_file=str(prerequisite_cnf_path)
        )
        prerequisite_is_prefix = base.clauses[
            : len(prerequisite_formula.clauses)
        ] == prerequisite_formula.clauses
        base_extension_clauses = (
            len(base.clauses) - len(prerequisite_formula.clauses)
        )
        if (
            prerequisite_data.get("status")
            != "three_vertex_connectivity_condition_augmented"
            or prerequisite_data["output_cnf_sha256"]
            != sha256(prerequisite_cnf_path)
            or not prerequisite_is_prefix
            or int(
                prerequisite.get(
                    "base_extension_clauses",
                    base_extension_clauses,
                )
            )
            != base_extension_clauses
            or prerequisite_audit.get("verified") is not True
            or prerequisite_audit.get("status")
            != "three_vertex_connectivity_augmentation_reconstructed"
            or prerequisite_audit.get("augmentation_sha256")
            != prerequisite["augmentation_sha256"]
        ):
            raise AssertionError(
                "three-connectivity prerequisite no longer verifies"
            )
    elif prerequisite is not None:
        raise AssertionError(
            "unused three-connectivity prerequisite was recorded"
        )
    expected.extend(map(list, sorted(all_new)))
    observed = CNF(from_file=str(output_cnf_path))
    if observed.clauses != expected:
        raise AssertionError(
            "augmented CNF differs from independent reconstruction"
        )
    with Solver(
        name="cadical195", bootstrap_with=observed.clauses
    ) as solver:
        sat = solver.solve()
    payload = {
        "verified": True,
        "status": "minimum_activity_augmentation_reconstructed",
        "scope": (
            "all source and audit hashes, independent symmetry transport, "
            "deduplication, exact clause sequence, and independent SAT solve"
        ),
        "augmentation": str(args.augmentation),
        "augmentation_sha256": sha256(args.augmentation),
        "partition": list(lengths),
        "certificates_replayed": len(reconstructed_rows),
        "new_transport_clauses": len(all_new),
        "output_cnf_variables": observed.nv,
        "output_cnf_clauses": len(observed.clauses),
        "independent_solver": "cadical195",
        "sat": bool(sat),
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
