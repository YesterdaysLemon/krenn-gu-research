"""Append activation-transport no-goods from verified one-extra cores."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from pysat.formula import CNF

from analyze_fourteen_vertex_two_even_cycle_rule_sat import (
    parse_factor,
)
from explore_fourteen_vertex_equality_factor_family import (
    N,
    contiguous_cycles,
    full_automorphisms,
)
from explore_random_even_cycle_forks import cycle_edges
from run_fourteen_vertex_two_even_cycle_rule_sat_incremental import (
    certificate_no_goods,
    minimum_condition_no_goods,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--compiled-result", type=Path, required=True)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument(
        "--one-extra-core",
        type=Path,
        action="append",
        default=[],
    )
    parser.add_argument(
        "--core-chain",
        type=Path,
        action="append",
        default=[],
        help=(
            "reuse every independently audited core recorded by an "
            "incremental direct-core chain"
        ),
    )
    parser.add_argument(
        "--minimum-activation",
        action="store_true",
        help=(
            "use each core's independently verified three-connected "
            "minimum-activity companion certificate"
        ),
    )
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    core_paths = list(args.one_extra_core)
    for chain_path in args.core_chain:
        chain = json.loads(chain_path.read_text(encoding="utf-8"))
        for row in chain["iterations"]:
            if row.get("core_candidates"):
                core_paths.extend(
                    Path(candidate["core"])
                    for candidate in row["core_candidates"]
                    if candidate.get("audit")
                )
            elif row.get("audit"):
                core_paths.append(Path(row["core"]))
    core_paths = sorted(
        {path.resolve(): path for path in core_paths}.values(),
        key=lambda path: str(path),
    )
    if not core_paths:
        raise ValueError("at least one one-extra core is required")

    compiled = json.loads(
        args.compiled_result.read_text(encoding="utf-8")
    )
    census = json.loads(args.census.read_text(encoding="utf-8"))
    lengths = tuple(map(int, compiled["partition"]))
    if (
        tuple(map(int, census["partition"])) != lengths
        or sum(lengths) != N
        or any(length % 2 for length in lengths)
    ):
        raise AssertionError("all-even partition changed")
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
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
    actions = full_automorphisms(cycles)
    if len(actions) != int(census["full_automorphisms"]):
        raise AssertionError("automorphism count changed")

    cnf = CNF(from_file=str(args.base_cnf))
    known = {
        tuple(
            sorted(
                set(map(int, clause)),
                key=lambda item: (abs(item), item),
            )
        )
        for clause in cnf.clauses
    }
    added: set[tuple[int, ...]] = set()
    records = []
    for core_path in core_paths:
        audit_path = core_path.with_name(
            f"{core_path.stem}_verified.json"
        )
        proof = json.loads(core_path.read_text(encoding="utf-8"))
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        if (
            proof.get("status") != "one_extra_cycle_core"
            or tuple(map(int, proof["full_cycle_type"])) != lengths
            or audit.get("verified") is not True
            or audit.get("status") != "one_extra_cycle_core_verified"
            or audit.get("certificate_sha256") != sha256(core_path)
        ):
            raise AssertionError(f"one-extra core changed: {core_path}")
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
        colourings = tuple(
            tuple(
                (equation // (3**vertex)) % 3
                for vertex in range(N)
            )
            for equation in equations
        )
        minimum_path = None
        minimum_audit_path = None
        minimum_score = None
        if args.minimum_activation:
            minimum_path = core_path.with_name(
                f"{core_path.stem}_minimum_activity.json"
            )
            minimum_audit_path = core_path.with_name(
                f"{core_path.stem}_minimum_activity_verified.json"
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
                or minimum.get("analysis_sha256") != sha256(core_path)
                or minimum_factors != factors
                or list(map(int, minimum["equations"])) != equations
                or minimum.get("activity_scope")
                != "three_connected_perfect_matching_edge_disjoint"
                or minimum_audit.get("verified") is not True
                or minimum_audit.get("status")
                != "fourteen_vertex_minimum_activity_"
                "certificate_verified"
                or minimum_audit.get("certificate_sha256")
                != sha256(minimum_path)
            ):
                raise AssertionError(
                    f"minimum activation changed: {minimum_path}"
                )
            minimum_score = int(
                minimum["activation_constraint_score"]
            )
            clauses = minimum_condition_no_goods(
                factors,
                minimum["activation_conditions"],
                representative_id,
                selectors,
                actions,
                eligible_edges,
            )
        else:
            clauses = certificate_no_goods(
                factors,
                colourings,
                representative_id,
                selectors,
                actions,
                eligible_edges,
            )
        new = clauses - known - added
        added.update(new)
        records.append(
            {
                "mode": "verified_one_extra_cycle_activation_core",
                "certificate": str(core_path),
                "certificate_sha256": sha256(core_path),
                "audit": str(audit_path),
                "audit_sha256": sha256(audit_path),
                "first_factor_orbit": representative_id[factors[0]],
                "activation_equations": equations,
                "activation_mode": (
                    "three_connected_minimum_activity"
                    if minimum_path
                    else "exact_activity_mask"
                ),
                "minimum_activity": (
                    str(minimum_path) if minimum_path else None
                ),
                "minimum_activity_sha256": (
                    sha256(minimum_path) if minimum_path else None
                ),
                "minimum_activity_audit": (
                    str(minimum_audit_path)
                    if minimum_audit_path
                    else None
                ),
                "minimum_activity_audit_sha256": (
                    sha256(minimum_audit_path)
                    if minimum_audit_path
                    else None
                ),
                "minimum_activity_score": minimum_score,
                "transport_clauses": len(clauses),
                "transport_clause_widths": sorted(
                    {len(clause) for clause in clauses}
                ),
                "new_no_goods": len(new),
            }
        )

    for clause in sorted(added):
        cnf.append(list(clause))
    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    cnf.to_file(str(args.output_cnf))
    payload = {
        "status": "verified_one_extra_cycle_rules_augmented",
        "partition": list(lengths),
        "compiled_result": str(args.compiled_result),
        "compiled_result_sha256": sha256(args.compiled_result),
        "census": str(args.census),
        "census_sha256": sha256(args.census),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "base_clauses": len(cnf.clauses) - len(added),
        "certificate_records": records,
        "new_no_goods": len(added),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "output_clauses": len(cnf.clauses),
        "exploratory_until_independently_reconstructed": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
