"""Independently reconstruct a binomial-support CNF augmentation."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import tempfile
import time
from pathlib import Path

from pysat.formula import CNF


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def edge(first: int, second: int) -> tuple[int, int]:
    return tuple(sorted((int(first), int(second))))


def cycles_for(lengths: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    output = []
    start = 0
    for length in lengths:
        output.append(tuple(range(start, start + length)))
        start += length
    if start != 14:
        raise ValueError("partition does not sum to 14")
    return tuple(output)


def cycle_edges(cycle: tuple[int, ...]) -> set[tuple[int, int]]:
    return {
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    }


def full_factor_automorphisms(
    cycles: tuple[tuple[int, ...], ...],
) -> list[tuple[int, ...]]:
    component_maps = [
        permutation
        for permutation in itertools.permutations(range(len(cycles)))
        if all(
            len(cycles[source]) == len(cycles[target])
            for source, target in enumerate(permutation)
        )
    ]
    local_choices = list(
        itertools.product(
            *[
                [
                    (direction, rotation)
                    for direction in (1, -1)
                    for rotation in range(len(cycle))
                ]
                for cycle in cycles
            ]
        )
    )
    output = []
    for component_map in component_maps:
        for choices in local_choices:
            action = [0] * 14
            for source_id, source in enumerate(cycles):
                target = cycles[component_map[source_id]]
                direction, rotation = choices[source_id]
                for position, vertex in enumerate(source):
                    action[vertex] = target[
                        (rotation + direction * position) % len(target)
                    ]
            output.append(tuple(action))
    return output


def transform_factor(
    factor: tuple[tuple[int, int], ...],
    action: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    return tuple(
        sorted(edge(action[first], action[second]) for first, second in factor)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("augmentation", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()

    augmentation = json.loads(
        args.augmentation.read_text(encoding="utf-8")
    )
    clause_set_only = (
        augmentation.get("status")
        == "verified_binomial_support_no_goods_clause_set"
    )
    if not clause_set_only and (
        augmentation.get("status")
        != "verified_binomial_support_no_goods_augmented"
    ):
        raise AssertionError("unexpected augmentation status")
    base_path = Path(augmentation["base_cnf"])
    if sha256(base_path) != augmentation["base_cnf_sha256"]:
        raise AssertionError("base CNF hash changed")
    output_path = None
    if not clause_set_only:
        output_path = Path(augmentation["output_cnf"])
        if sha256(output_path) != augmentation["output_cnf_sha256"]:
            raise AssertionError("output CNF hash changed")

    partition = tuple(map(int, augmentation["partition"]))
    cycles = cycles_for(partition)
    full_edges = set().union(*(cycle_edges(cycle) for cycle in cycles))
    eligible = tuple(
        sorted(set(itertools.combinations(range(14), 2)) - full_edges)
    )
    if len(eligible) != 77:
        raise AssertionError("eligible edge count changed")
    edge_index = {item: index for index, item in enumerate(eligible)}
    clauses = []
    orbit_sizes = []
    symmetry_orbit_closure = bool(
        augmentation.get("stabilizer_orbit_closure", False)
    )
    full_support_orbit_closure = bool(
        augmentation.get("full_support_orbit_closure", False)
    )
    if symmetry_orbit_closure and full_support_orbit_closure:
        raise AssertionError("conflicting support-orbit closure modes")
    actions = full_factor_automorphisms(cycles)
    if any(tuple(sorted(action)) != tuple(range(14)) for action in actions):
        raise AssertionError("full-factor action stopped being a permutation")
    if any(
        {
            edge(action[first], action[second])
            for first, second in full_edges
        }
        != full_edges
        for action in actions
    ):
        raise AssertionError("full-factor action changed the cycle skeleton")
    records_checked = 0
    branches_bound = 0
    for record in augmentation["certificate_records"]:
        partial_path = Path(record["partial_analysis"])
        if sha256(partial_path) != record["partial_analysis_sha256"]:
            raise AssertionError("partial-analysis hash changed")
        partial = json.loads(partial_path.read_text(encoding="utf-8"))
        if record.get("certificate_type") == "mandatory_unit_core":
            verified_path = Path(record["verified_support"])
            analysis_path = Path(record["analysis"])
            if (
                sha256(verified_path)
                != record["verified_support_sha256"]
            ):
                raise AssertionError("verified-support hash changed")
            if sha256(analysis_path) != record["analysis_sha256"]:
                raise AssertionError("support-analysis hash changed")
            verified = json.loads(
                verified_path.read_text(encoding="utf-8")
            )
            analysis = json.loads(
                analysis_path.read_text(encoding="utf-8")
            )
            if (
                not verified.get("verified")
                or verified.get("status")
                != "partial_circuit_binomial_support_verified"
                or not verified.get("support_closed")
                or Path(verified["analysis"]) != analysis_path
                or verified["analysis_sha256"]
                != sha256(analysis_path)
                or analysis.get("status") != "contradiction"
                or not analysis.get("support_closed")
                or not analysis.get("selected_mandatory_unit_core")
                or Path(analysis["partial_analysis"]) != partial_path
                or int(record["selected_mandatory_relations"])
                != int(verified["selected_initial_relations"])
                or int(record["derived_relations"])
                != int(verified["derived_relations_checked"])
            ):
                raise AssertionError(
                    "mandatory-unit certificate binding changed"
                )
        else:
            verified_path = Path(record["verified_chain"])
            chain_path = Path(record["chain"])
            if (
                sha256(verified_path)
                != record["verified_chain_sha256"]
            ):
                raise AssertionError("verified-chain hash changed")
            if sha256(chain_path) != record["chain_sha256"]:
                raise AssertionError("chain hash changed")
            verified = json.loads(
                verified_path.read_text(encoding="utf-8")
            )
            chain = json.loads(
                chain_path.read_text(encoding="utf-8")
            )
            if (
                not verified.get("verified")
                or not verified.get("support_closed")
                or verified.get("terminal_relation_selection_sat")
                or Path(verified["chain"]) != chain_path
                or verified["chain_sha256"] != sha256(chain_path)
                or chain.get("status") != "support_closed"
                or Path(chain["partial_analysis"]) != partial_path
                or chain["partial_analysis_sha256"]
                != sha256(partial_path)
            ):
                raise AssertionError("chain certificate binding changed")
            branch_count = int(verified["records_checked"])
            if (
                branch_count
                != int(record["verified_relation_selection_branches"])
                or branch_count != len(chain["records"])
            ):
                raise AssertionError("branch count changed")
            branches_bound += branch_count
        if (
            tuple(map(int, partial["partition"])) != partition
            or Path(partial["cnf"]) != base_path
        ):
            raise AssertionError("partial-support binding changed")
        if int(record["orbit"]) != int(partial["orbit"]):
            raise AssertionError("orbit binding changed")
        parsed_factors = tuple(
            tuple(
                sorted(edge(*map(int, item)) for item in factor)
            )
            for factor in partial["singleton_factors"]
        )
        if any(len(factor) != 7 for factor in parsed_factors):
            raise AssertionError("certified role stopped being a factor")
        if full_support_orbit_closure:
            image_factors = {
                tuple(
                    transform_factor(
                        parsed_factors[source_colour], action
                    )
                    for source_colour in colour_permutation
                )
                for action in actions
                for colour_permutation in itertools.permutations(range(3))
            }
        elif symmetry_orbit_closure:
            local_actions = [
                action
                for action in actions
                if transform_factor(parsed_factors[0], action)
                == parsed_factors[0]
            ]
            if not local_actions:
                raise AssertionError("pinned-factor stabilizer is empty")
            image_factors = {
                (
                    transform_factor(parsed_factors[0], action),
                    transform_factor(
                        parsed_factors[2 if swap else 1], action
                    ),
                    transform_factor(
                        parsed_factors[1 if swap else 2], action
                    ),
                )
                for action in local_actions
                for swap in (False, True)
            }
        else:
            image_factors = {parsed_factors}
        local_clauses = []
        for image in image_factors:
            clause = tuple(
                sorted(
                    -(
                        colour * len(eligible)
                        + edge_index[item]
                        + 1
                    )
                    for colour, factor in enumerate(image)
                    for item in factor
                )
            )
            if len(clause) != 21:
                raise AssertionError("support no-good width changed")
            local_clauses.append(clause)
        local_clauses = sorted(set(local_clauses))
        clauses.extend(local_clauses)
        orbit_sizes.append(len(local_clauses))
        records_checked += 1
    clauses = sorted(set(clauses))

    if "certificate_symmetry_orbit_sizes" in augmentation and [
        int(item) for item in augmentation["certificate_symmetry_orbit_sizes"]
    ] != orbit_sizes:
        raise AssertionError("certificate symmetry-orbit sizes changed")
    expected_action_count = (
        len(actions)
        if symmetry_orbit_closure or full_support_orbit_closure
        else 0
    )
    if (
        "full_factor_automorphisms" in augmentation
        and int(augmentation["full_factor_automorphisms"])
        != expected_action_count
    ):
        raise AssertionError("full-factor automorphism count changed")
    if bool(augmentation.get("colour_1_2_swap", False)) != (
        symmetry_orbit_closure or full_support_orbit_closure
    ):
        raise AssertionError("colour-swap metadata changed")
    expected_colour_permutations = (
        6
        if full_support_orbit_closure
        else (2 if symmetry_orbit_closure else 1)
    )
    if (
        "colour_permutations" in augmentation
        and int(augmentation["colour_permutations"])
        != expected_colour_permutations
    ):
        raise AssertionError("colour-permutation count changed")

    if clause_set_only:
        if [list(clause) for clause in clauses] != augmentation[
            "support_no_goods"
        ]:
            raise AssertionError(
                "reconstructed support clause set changed"
            )
        if len(clauses) != int(
            augmentation["candidate_support_no_goods"]
        ):
            raise AssertionError("candidate support count changed")
        payload = {
            "verified": True,
            "status": "binomial_support_no_good_clause_set_verified",
            "scope": (
                "verified-certificate hash binding, terminal support "
                "closure, partial-support reconstruction, and exact "
                + (
                    "full-colour-orbit-closed"
                    if full_support_orbit_closure
                    else (
                        "stabilizer-orbit-closed"
                        if symmetry_orbit_closure
                        else "unclosed"
                    )
                )
                + " width-21 no-good clause set without DIMACS "
                "materialization"
            ),
            "augmentation": str(args.augmentation),
            "augmentation_sha256": sha256(args.augmentation),
            "certificate_records_checked": records_checked,
            "relation_selection_branches_bound": branches_bound,
            "stabilizer_orbit_closure": symmetry_orbit_closure,
            "certificate_symmetry_orbit_sizes": orbit_sizes,
            "support_no_goods": len(clauses),
            "base_cnf": str(base_path),
            "base_cnf_sha256": sha256(base_path),
            "global_conjecture_resolved": False,
            "elapsed_seconds": time.perf_counter() - started,
        }
        if full_support_orbit_closure:
            payload["full_support_orbit_closure"] = True
            payload["colour_permutations"] = expected_colour_permutations
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(payload, indent=2))
        return

    base = CNF(from_file=str(base_path))
    if (
        base.nv != int(augmentation["base_variables"])
        or len(base.clauses) != int(augmentation["base_clauses"])
    ):
        raise AssertionError("base CNF counts changed")
    existing = {tuple(map(int, clause)) for clause in base.clauses}
    new_clauses = [clause for clause in clauses if clause not in existing]
    if [list(clause) for clause in new_clauses] != augmentation[
        "support_no_goods"
    ]:
        raise AssertionError("reconstructed support no-goods changed")
    if len(clauses) != int(augmentation["candidate_support_no_goods"]):
        raise AssertionError("candidate support count changed")
    if len(new_clauses) != int(augmentation["new_support_no_goods"]):
        raise AssertionError("new support count changed")

    reconstructed = CNF(from_clauses=base.clauses)
    reconstructed.extend(new_clauses)
    with tempfile.TemporaryDirectory(
        prefix="binomial-support-augmentation-audit-"
    ) as raw_directory:
        rebuilt_path = Path(raw_directory) / "rebuilt.cnf"
        reconstructed.to_file(str(rebuilt_path))
        if output_path is None:
            raise AssertionError("output path unexpectedly absent")
        if sha256(rebuilt_path) != sha256(output_path):
            raise AssertionError("canonical augmented CNF bytes changed")
    if (
        reconstructed.nv != int(augmentation["output_variables"])
        or len(reconstructed.clauses)
        != int(augmentation["output_clauses"])
    ):
        raise AssertionError("output CNF counts changed")

    payload = {
        "verified": True,
        "status": "binomial_support_closure_augmentation_verified",
        "scope": (
            "verified-certificate hash binding, terminal support closure, "
            "partial-support reconstruction, exact"
            + (
                " full-colour-orbit-closed"
                if full_support_orbit_closure
                else (
                    " stabilizer-orbit-closed"
                    if symmetry_orbit_closure
                    else ""
                )
            )
            + " width-21 no-goods, "
            "and byte-identical augmented DIMACS"
        ),
        "augmentation": str(args.augmentation),
        "augmentation_sha256": sha256(args.augmentation),
        "certificate_records_checked": records_checked,
        "relation_selection_branches_bound": branches_bound,
        "stabilizer_orbit_closure": symmetry_orbit_closure,
        "certificate_symmetry_orbit_sizes": orbit_sizes,
        "new_support_no_goods": len(new_clauses),
        "output_cnf": str(output_path),
        "output_cnf_sha256": sha256(output_path),
        "output_variables": reconstructed.nv,
        "output_clauses": len(reconstructed.clauses),
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    if full_support_orbit_closure:
        payload["full_support_orbit_closure"] = True
        payload["colour_permutations"] = expected_colour_permutations
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
