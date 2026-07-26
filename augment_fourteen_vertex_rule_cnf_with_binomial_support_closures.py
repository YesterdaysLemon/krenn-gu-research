"""Append exact support no-goods from verified binomial-closure chains."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
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
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument(
        "--verified-chain", type=Path, action="append", default=[]
    )
    parser.add_argument(
        "--verified-support", type=Path, action="append", default=[]
    )
    parser.add_argument(
        "--stabilizer-orbit-closure",
        action="store_true",
        help=(
            "also append every support image under full-factor "
            "automorphisms stabilizing colour 0 and colour-1/2 swap"
        ),
    )
    parser.add_argument(
        "--full-support-orbit-closure",
        action="store_true",
        help=(
            "append every support image under all full-factor "
            "automorphisms and all six colour permutations"
        ),
    )
    parser.add_argument("--output-cnf", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--clauses-only",
        action="store_true",
        help=(
            "write an independently auditable symmetry-closed clause set "
            "without parsing or materializing the base DIMACS"
        ),
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help=(
            "omit the potentially large support_no_goods array from stdout; "
            "the complete array remains in --output"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    if not args.verified_chain and not args.verified_support:
        parser.error("provide --verified-chain or --verified-support")
    if (
        args.stabilizer_orbit_closure
        and args.full_support_orbit_closure
    ):
        parser.error(
            "choose at most one support-orbit closure mode"
        )
    if not args.clauses_only and args.output_cnf is None:
        parser.error("--output-cnf is required unless --clauses-only is used")

    partition: tuple[int, ...] | None = None
    records = []
    factors_list = []
    for verified_path in args.verified_chain:
        verified = json.loads(verified_path.read_text(encoding="utf-8"))
        if (
            not verified.get("verified")
            or verified.get("status")
            != "partial_circuit_binomial_selection_chain_verified"
            or not verified.get("support_closed")
            or verified.get("terminal_relation_selection_sat")
        ):
            raise ValueError(f"{verified_path} is not a support closure")
        chain_path = Path(verified["chain"])
        if sha256(chain_path) != verified["chain_sha256"]:
            raise ValueError("verified chain hash changed")
        chain = json.loads(chain_path.read_text(encoding="utf-8"))
        if chain.get("status") != "support_closed":
            raise ValueError("source chain no longer claims support closure")
        partial_path = Path(chain["partial_analysis"])
        if sha256(partial_path) != chain["partial_analysis_sha256"]:
            raise ValueError("partial-analysis hash changed")
        partial = json.loads(partial_path.read_text(encoding="utf-8"))
        local_partition = tuple(map(int, partial["partition"]))
        if partition is None:
            partition = local_partition
        elif partition != local_partition:
            raise ValueError("verified chains use different partitions")
        if Path(partial["cnf"]) != args.base_cnf:
            raise ValueError(
                "partial support was not selected from the base CNF"
            )
        records.append(
            {
                "verified_chain": str(verified_path),
                "verified_chain_sha256": sha256(verified_path),
                "chain": str(chain_path),
                "chain_sha256": sha256(chain_path),
                "partial_analysis": str(partial_path),
                "partial_analysis_sha256": sha256(partial_path),
                "orbit": int(partial["orbit"]),
                "verified_relation_selection_branches": int(
                    verified["records_checked"]
                ),
            }
        )
        factors_list.append(partial["singleton_factors"])
    for verified_path in args.verified_support:
        verified = json.loads(verified_path.read_text(encoding="utf-8"))
        if (
            not verified.get("verified")
            or verified.get("status")
            != "partial_circuit_binomial_support_verified"
            or not verified.get("support_closed")
        ):
            raise ValueError(
                f"{verified_path} is not a verified support closure"
            )
        analysis_path = Path(verified["analysis"])
        if sha256(analysis_path) != verified["analysis_sha256"]:
            raise ValueError("verified support-analysis hash changed")
        analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
        if (
            analysis.get("status") != "contradiction"
            or not analysis.get("support_closed")
            or not analysis.get("selected_mandatory_unit_core")
        ):
            raise ValueError(
                "source analysis no longer claims mandatory-unit closure"
            )
        partial_path = Path(analysis["partial_analysis"])
        partial = json.loads(partial_path.read_text(encoding="utf-8"))
        local_partition = tuple(map(int, partial["partition"]))
        if partition is None:
            partition = local_partition
        elif partition != local_partition:
            raise ValueError(
                "verified supports use different partitions"
            )
        if Path(partial["cnf"]) != args.base_cnf:
            raise ValueError(
                "partial support was not selected from the base CNF"
            )
        records.append(
            {
                "certificate_type": "mandatory_unit_core",
                "verified_support": str(verified_path),
                "verified_support_sha256": sha256(verified_path),
                "analysis": str(analysis_path),
                "analysis_sha256": sha256(analysis_path),
                "partial_analysis": str(partial_path),
                "partial_analysis_sha256": sha256(partial_path),
                "orbit": int(partial["orbit"]),
                "selected_mandatory_relations": int(
                    verified["selected_initial_relations"]
                ),
                "derived_relations": int(
                    verified["derived_relations_checked"]
                ),
            }
        )
        factors_list.append(partial["singleton_factors"])
    if partition is None:
        raise AssertionError("no verified chains loaded")

    cycles = cycles_for(partition)
    full_edges = set().union(*(cycle_edges(cycle) for cycle in cycles))
    eligible = tuple(
        sorted(set(itertools.combinations(range(14), 2)) - full_edges)
    )
    if len(eligible) != 77:
        raise AssertionError("eligible edge count changed")
    edge_index = {item: index for index, item in enumerate(eligible)}
    candidate_clauses = []
    orbit_sizes = []
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
    for factors in factors_list:
        parsed_factors = tuple(
            tuple(sorted(edge(*map(int, item)) for item in factor))
            for factor in factors
        )
        if any(len(factor) != 7 for factor in parsed_factors):
            raise AssertionError("certified role stopped being a factor")
        if args.full_support_orbit_closure:
            local_actions = actions
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
        elif args.stabilizer_orbit_closure:
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
            local_actions = []
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
        candidate_clauses.extend(local_clauses)
        orbit_sizes.append(len(local_clauses))
    candidate_clauses = sorted(set(candidate_clauses))

    if args.clauses_only:
        payload = {
            "status": "verified_binomial_support_no_goods_clause_set",
            "partition": list(partition),
            "base_cnf": str(args.base_cnf),
            "base_cnf_sha256": sha256(args.base_cnf),
            "certificate_records": records,
            "stabilizer_orbit_closure": (
                args.stabilizer_orbit_closure
            ),
            "full_factor_automorphisms": (
                len(actions)
                if (
                    args.stabilizer_orbit_closure
                    or args.full_support_orbit_closure
                )
                else 0
            ),
            "colour_1_2_swap": (
                args.stabilizer_orbit_closure
                or args.full_support_orbit_closure
            ),
            "certificate_symmetry_orbit_sizes": orbit_sizes,
            "candidate_support_no_goods": len(candidate_clauses),
            "support_no_good_widths": sorted(
                {len(clause) for clause in candidate_clauses}
            ),
            "support_no_goods": [
                list(clause) for clause in candidate_clauses
            ],
            "global_conjecture_resolved": False,
            "elapsed_seconds": time.perf_counter() - started,
        }
        if args.full_support_orbit_closure:
            payload["full_support_orbit_closure"] = True
            payload["colour_permutations"] = 6
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8"
        )
        stdout_payload = payload
        if args.summary_only:
            stdout_payload = {
                key: value
                for key, value in payload.items()
                if key != "support_no_goods"
            }
            stdout_payload[
                "support_no_goods_omitted_from_stdout"
            ] = True
        print(json.dumps(stdout_payload, indent=2))
        return

    formula = CNF(from_file=str(args.base_cnf))
    existing = {tuple(map(int, clause)) for clause in formula.clauses}
    new_clauses = [
        clause for clause in candidate_clauses if clause not in existing
    ]
    formula.extend(new_clauses)
    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    formula.to_file(str(args.output_cnf))
    payload = {
        "status": "verified_binomial_support_no_goods_augmented",
        "partition": list(partition),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "base_variables": formula.nv,
        "base_clauses": len(formula.clauses) - len(new_clauses),
        "certificate_records": records,
        "stabilizer_orbit_closure": args.stabilizer_orbit_closure,
        "full_factor_automorphisms": (
            len(actions)
            if (
                args.stabilizer_orbit_closure
                or args.full_support_orbit_closure
            )
            else 0
        ),
        "colour_1_2_swap": (
            args.stabilizer_orbit_closure
            or args.full_support_orbit_closure
        ),
        "certificate_symmetry_orbit_sizes": orbit_sizes,
        "candidate_support_no_goods": len(candidate_clauses),
        "new_support_no_goods": len(new_clauses),
        "support_no_good_widths": sorted(
            {len(clause) for clause in new_clauses}
        ),
        "support_no_goods": [list(clause) for clause in new_clauses],
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "output_variables": formula.nv,
        "output_clauses": len(formula.clauses),
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    if args.full_support_orbit_closure:
        payload["full_support_orbit_closure"] = True
        payload["colour_permutations"] = 6
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    stdout_payload = payload
    if args.summary_only:
        stdout_payload = {
            key: value
            for key, value in payload.items()
            if key != "support_no_goods"
        }
        stdout_payload["support_no_goods_omitted_from_stdout"] = True
    print(json.dumps(stdout_payload, indent=2))


if __name__ == "__main__":
    main()
