"""Independent semantic replay of an all-even factor/pair fork."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

N = 14
Edge = tuple[int, int]
Factor = tuple[Edge, ...]
ALL_GRAPH_EDGES = tuple(itertools.combinations(range(N), 2))
ALL_GRAPH_EDGE_ID = {
    item: position for position, item in enumerate(ALL_GRAPH_EDGES)
}


def edge(first: int, second: int) -> Edge:
    return (
        (first, second) if first < second else (second, first)
    )


def cycle_edges(cycle: Sequence[int]) -> frozenset[Edge]:
    return frozenset(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def contiguous_cycles(lengths: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    output = []
    start = 0
    for length in lengths:
        output.append(tuple(range(start, start + length)))
        start += length
    return tuple(output)


def perfect_matchings(allowed: Iterable[Edge]) -> list[Factor]:
    allowed_set = set(allowed)
    adjacency = {
        vertex: tuple(
            other
            for other in range(N)
            if other != vertex and edge(vertex, other) in allowed_set
        )
        for vertex in range(N)
    }
    output = []

    def visit(remaining: int, chosen: Factor) -> None:
        if remaining == 0:
            output.append(chosen)
            return
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        for second in adjacency[first]:
            second_bit = 1 << second
            if remaining & second_bit:
                visit(
                    remaining ^ first_bit ^ second_bit,
                    (*chosen, edge(first, second)),
                )

    visit((1 << N) - 1, ())
    return sorted(output)


def indexed_colouring(index: int) -> tuple[int, ...]:
    return tuple(
        (index // (3**vertex)) % 3 for vertex in range(N)
    )


def local_code(
    colouring: Sequence[int], cycle: Sequence[int]
) -> int:
    return sum(
        int(colouring[vertex]) * (3**position)
        for position, vertex in enumerate(cycle)
    )


def relation_signature(
    first: Sequence[Edge],
    second: Sequence[Edge],
    colouring: Sequence[int],
    labels: dict[Edge, int],
    full_edges: frozenset[Edge],
) -> tuple[tuple[int, int], ...]:
    def variables(matching: Sequence[Edge]) -> list[int]:
        output = []
        for item in matching:
            if item in full_edges:
                first_colour = int(colouring[item[0]])
                second_colour = int(colouring[item[1]])
            else:
                first_colour = second_colour = labels[item]
            output.append(
                9 * ALL_GRAPH_EDGE_ID[item]
                + 3 * first_colour
                + second_colour
            )
        return output

    vector = Counter(variables(first))
    vector.subtract(variables(second))
    direct = tuple(
        sorted(
            (entry, coefficient)
            for entry, coefficient in vector.items()
            if coefficient
        )
    )
    negative = tuple(
        (entry, -coefficient) for entry, coefficient in direct
    )
    return min(direct, negative)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("analysis", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_even_cycle_double_pair_fork_verified.json"
        ),
    )
    args = parser.parse_args()
    analysis = json.loads(args.analysis.read_text(encoding="utf-8"))
    if analysis.get("status") != "even_cycle_double_pair_fork":
        raise AssertionError("analysis does not contain a contradiction")
    certificate = analysis["certificate"]
    lengths = tuple(map(int, analysis["full_cycle_type"]))
    cycles = contiguous_cycles(lengths)
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    factors = tuple(
        tuple(
            sorted(edge(*map(int, item)) for item in analysis[
                "singleton_matchings"
            ][key])
        )
        for key in ("first", "second", "third")
    )
    labels = {
        item: colour
        for colour, factor in enumerate(factors)
        for item in factor
    }
    if len(labels) != 3 * (N // 2):
        raise AssertionError("singleton factors are not edge-disjoint")
    matchings = perfect_matchings(set(full_edges) | set(labels))
    if len(matchings) != int(analysis["skeleton_perfect_matchings"]):
        raise AssertionError("skeleton matching count changed")
    full_only = frozenset(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(item in full_edges for item in matching)
    )
    baseline = 1 << len(cycles)
    if len(full_only) != baseline:
        raise AssertionError("full-only factorization changed")

    def active_ids(equation: int) -> tuple[int, ...]:
        colouring = indexed_colouring(equation)
        if len(set(colouring)) == 1:
            raise AssertionError("certificate uses a required equation")
        active_edges = set(full_edges)
        active_edges.update(
            item
            for item, colour in labels.items()
            if colouring[item[0]] == colouring[item[1]] == colour
        )
        return tuple(
            matching_id
            for matching_id, matching in enumerate(matchings)
            if all(item in active_edges for item in matching)
        )

    def parse_signature(raw) -> tuple[tuple[int, int], ...]:
        return tuple(tuple(map(int, item)) for item in raw)

    conditional_replays = 0

    def validate_conditional(item: dict[str, object]) -> None:
        nonlocal conditional_replays
        cycle = tuple(map(int, item["cycle"]))
        cycle_id = cycles.index(cycle)
        code = int(item["cycle_local_code"])
        if "pair_equations" in item:
            pair_rows = item["pair_equations"]
        else:
            pair_rows = [
                {
                    "equation_index": item[
                        "first_pair_equation_index"
                    ],
                    "matchings": item["first_pair_matchings"],
                    "relation_signature": item[
                        "first_pair_relation_signature"
                    ],
                },
                {
                    "equation_index": item[
                        "second_pair_equation_index"
                    ],
                    "matchings": item["second_pair_matchings"],
                    "relation_signature": item[
                        "second_pair_relation_signature"
                    ],
                },
            ]
        origins = []
        for row in pair_rows:
            equation = int(row["equation_index"])
            colouring = indexed_colouring(equation)
            if local_code(colouring, cycle) != code:
                raise AssertionError(
                    "conditional pair local code changed"
                )
            activity = active_ids(equation)
            if len(activity) != baseline + 2 or not (
                full_only <= set(activity)
            ):
                raise AssertionError(
                    "conditional pair activity changed"
                )
            pair = tuple(map(int, row["matchings"]))
            extras = tuple(
                matching_id
                for matching_id in activity
                if matching_id not in full_only
            )
            if set(pair) != set(extras):
                raise AssertionError("reported extra pair changed")
            signature = relation_signature(
                matchings[pair[0]],
                matchings[pair[1]],
                colouring,
                labels,
                full_edges,
            )
            if signature != parse_signature(
                row["relation_signature"]
            ):
                raise AssertionError("pair signature changed")
            origins.append(signature)

        rich_equation = int(item["rich_equation_index"])
        rich_colouring = indexed_colouring(rich_equation)
        if local_code(rich_colouring, cycle) != code:
            raise AssertionError("conditional rich local code changed")
        rich_activity = active_ids(rich_equation)
        if tuple(map(int, item["rich_activity"])) != rich_activity:
            raise AssertionError("conditional rich activity changed")
        rich_extras = {
            matching_id
            for matching_id in rich_activity
            if matching_id not in full_only
        }
        survivor = int(item["rich_surviving_matching"])
        used = {survivor}
        rich_pairs = [
            tuple(map(int, pair))
            for pair in item["rich_paired_matchings"]
        ]
        if len(rich_pairs) != len(origins):
            raise AssertionError("conditional rich pair count changed")
        for pair, origin_signature in zip(
            rich_pairs, origins, strict=True
        ):
            pair = set(pair)
            if used & pair:
                raise AssertionError("conditional pairs overlap")
            used.update(pair)
            first, second = tuple(pair)
            if relation_signature(
                matchings[first],
                matchings[second],
                rich_colouring,
                labels,
                full_edges,
            ) != origin_signature:
                raise AssertionError(
                    "conditional pair does not transport"
                )
        if used != rich_extras:
            raise AssertionError(
                "conditional rich target does not leave one survivor"
            )
        conditional_replays += 1

    mode = certificate["certificate_mode"]
    forcing_base_equations = 0
    final_pair_relations = 0
    if mode == "even_cycle_factor_two_pair_survivor_fork":
        base_equation = int(certificate["base_equation_index"])
        if active_ids(base_equation) != tuple(
            map(int, certificate["base_activity"])
        ):
            raise AssertionError("base activity changed")
        if set(active_ids(base_equation)) != full_only:
            raise AssertionError("base is not the full factor")
        alternatives = certificate["alternatives"]
        if {
            tuple(map(int, row["cycle"])) for row in alternatives
        } != set(cycles):
            raise AssertionError("not every factor choice is closed")
        for row in alternatives:
            validate_conditional(row)
    elif mode in {
        "forced_cycle_slice_pair_survivor_fork",
        "forced_cycle_all_codes_two_pair_survivor_fork",
    }:
        forced_cycle = tuple(map(int, certificate["forced_cycle"]))
        forced_cycle_id = cycles.index(forced_cycle)
        forcing_rows = {
            int(row["forced_local_code"]): row
            for row in certificate[
                "forcing_base_equations_by_local_code"
            ]
        }
        conditional_by_cycle_code = {}
        for cycle_row in certificate[
            "conditional_cycle_certificates"
        ]:
            cycle = tuple(map(int, cycle_row["cycle"]))
            for code_raw, row in cycle_row[
                "certificates_by_local_code"
            ].items():
                code = int(code_raw)
                validate_conditional(row)
                conditional_by_cycle_code[(cycle, code)] = row
        for forced_code, row in forcing_rows.items():
            equation = int(row["base_equation_index"])
            colouring = indexed_colouring(equation)
            activity = active_ids(equation)
            if set(activity) != full_only:
                raise AssertionError(
                    "forcing base is not exactly the full factor"
                )
            codes = [
                local_code(colouring, cycle) for cycle in cycles
            ]
            if codes != list(
                map(int, row["base_cycle_local_codes"])
            ):
                raise AssertionError("forcing base codes changed")
            if codes[forced_cycle_id] != forced_code:
                raise AssertionError("forced local code changed")
            for cycle_id, cycle in enumerate(cycles):
                if cycle_id == forced_cycle_id:
                    continue
                if (cycle, codes[cycle_id]) not in (
                    conditional_by_cycle_code
                ):
                    raise AssertionError(
                        "forcing base lacks an excluded alternative"
                    )
            forcing_base_equations += 1

        if "pair_equations" in certificate:
            pair_rows = certificate["pair_equations"]
        else:
            pair_rows = [
                {
                    "equation_index": certificate[
                        "first_pair_equation_index"
                    ],
                    "forced_cycle_local_code": local_code(
                        indexed_colouring(
                            int(
                                certificate[
                                    "first_pair_equation_index"
                                ]
                            )
                        ),
                        forced_cycle,
                    ),
                    "matchings": certificate[
                        "first_pair_matchings"
                    ],
                    "relation_signature": certificate[
                        "first_pair_relation_signature"
                    ],
                },
                {
                    "equation_index": certificate[
                        "second_pair_equation_index"
                    ],
                    "forced_cycle_local_code": local_code(
                        indexed_colouring(
                            int(
                                certificate[
                                    "second_pair_equation_index"
                                ]
                            )
                        ),
                        forced_cycle,
                    ),
                    "matchings": certificate[
                        "second_pair_matchings"
                    ],
                    "relation_signature": certificate[
                        "second_pair_relation_signature"
                    ],
                },
            ]
        origin_signatures = []
        required_codes = set()
        for row in pair_rows:
            equation = int(row["equation_index"])
            colouring = indexed_colouring(equation)
            code = local_code(colouring, forced_cycle)
            if code != int(row["forced_cycle_local_code"]):
                raise AssertionError("pair forced code changed")
            if code not in forcing_rows:
                raise AssertionError("pair code was not forced")
            activity = active_ids(equation)
            if len(activity) != baseline + 2 or not (
                full_only <= set(activity)
            ):
                raise AssertionError("forced pair activity changed")
            extras = tuple(
                matching_id
                for matching_id in activity
                if matching_id not in full_only
            )
            pair = tuple(map(int, row["matchings"]))
            if set(pair) != set(extras):
                raise AssertionError("forced pair IDs changed")
            signature = relation_signature(
                matchings[pair[0]],
                matchings[pair[1]],
                colouring,
                labels,
                full_edges,
            )
            if signature != parse_signature(
                row["relation_signature"]
            ):
                raise AssertionError(
                    "forced pair signature changed"
                )
            rich_pair = tuple(
                map(int, row.get("rich_matchings", pair))
            )
            origin_signatures.append((set(rich_pair), signature))
            required_codes.add(code)
            final_pair_relations += 1

        rich_equation = int(certificate["rich_equation_index"])
        rich_colouring = indexed_colouring(rich_equation)
        rich_code = local_code(rich_colouring, forced_cycle)
        reported_rich_code = int(
            certificate.get(
                "rich_forced_cycle_local_code", rich_code
            )
        )
        if rich_code != reported_rich_code or rich_code not in forcing_rows:
            raise AssertionError("rich forced code was not established")
        rich_activity = active_ids(rich_equation)
        if rich_activity != tuple(
            map(int, certificate["rich_activity"])
        ):
            raise AssertionError("final rich activity changed")
        rich_extras = {
            matching_id
            for matching_id in rich_activity
            if matching_id not in full_only
        }
        survivor = int(certificate["rich_surviving_matching"])
        used = {survivor}
        for pair, origin_signature in origin_signatures:
            if used & pair:
                raise AssertionError("final rich pairs overlap")
            used.update(pair)
            first, second = tuple(pair)
            if relation_signature(
                matchings[first],
                matchings[second],
                rich_colouring,
                labels,
                full_edges,
            ) != origin_signature:
                raise AssertionError(
                    "forced pair does not transport to final target"
                )
        if used != rich_extras:
            raise AssertionError(
                "final target does not leave exactly one survivor"
            )
    else:
        raise AssertionError(f"unsupported certificate mode: {mode}")

    payload = {
        "verified": True,
        "status": "even_cycle_factor_pair_fork_verified",
        "analysis": str(args.analysis),
        "analysis_sha256": sha256(args.analysis),
        "survivor_index": int(analysis["survivor_index"]),
        "full_cycle_type": list(lengths),
        "skeleton_perfect_matchings": len(matchings),
        "full_only_matching_count": baseline,
        "certificate_mode": mode,
        "conditional_factor_forks_replayed": conditional_replays,
        "forcing_base_equations_replayed": forcing_base_equations,
        "final_pair_relations_replayed": final_pair_relations,
        "logical_check": (
            "every factor choice is either conditionally contradicted "
            "or forced by a full-only product equation; the transported "
            "matching pairs cancel in the final forbidden equation, "
            "leaving one supported nonzero monomial"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
