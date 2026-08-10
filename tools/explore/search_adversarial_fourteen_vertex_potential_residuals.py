"""Hill-climb reciprocal port graphs toward potential-ray residuals."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import time

from analyze_ten_vertex_degree_six_kotzig_port_survivors import (
    enumerate_coloured_matchings,
)
from analyze_ten_vertex_permuted_potential_survivors import (
    permuted_potential,
)
from explore_eight_vertex_degree_six_kotzig_ports import (
    balanced_allowed_entries,
    decode_graph6,
    kotzig_colourings,
    normal_types,
)
from scout_kotzig_full_cone_cells import catalogue
from search_random_fourteen_vertex_potential_residuals import (
    randomized_port,
)
from verify_full_admissible_potential_cone import EXTREME_RAYS

Normal = tuple[int, int, int]
PortKey = tuple[int, int, int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def physical(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def port_from_stubs(first: int, second: int) -> PortKey:
    left, left_target = divmod(first, 3)
    right, right_target = divmod(second, 3)
    if left < right:
        return (left, right, right_target, left_target)
    return (right, left, left_target, right_target)


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def evaluate(
    order: int,
    colouring,
    normals: tuple[Normal, ...],
    ports: tuple[PortKey, ...],
    potentials: tuple[tuple[tuple[int, ...], ...], ...],
) -> tuple[int, int]:
    edges = [
        (left, right, cu, cv, True, "K", 0)
        for left, right, cu, cv in ports
    ]
    for colour, matching in enumerate(colouring):
        edges.extend(
            (
                left,
                right,
                colour,
                colour,
                True,
                "D",
                0,
            )
            for left, right in matching
        )
    counts, _first, _forced = enumerate_coloured_matchings(
        order, tuple(edges)
    )
    mixed_counts = {
        row: count
        for row, count in counts.items()
        if len(set(row)) > 1
    }
    signatures = {
        row: tuple(
            sum(
                potentials[vertex][colour][ray]
                for vertex, colour in enumerate(row)
            )
            for ray in range(6)
        )
        for row in mixed_counts
    }
    old_successes = 0
    for ray in range(6):
        minimum = min(value[ray] for value in signatures.values())
        old_successes += any(
            mixed_counts[row] == 1
            and signatures[row][ray] == minimum
            for row in mixed_counts
        )
    interior = (1, 1, 1, 1, 1, 1)
    extreme_successes = 0
    for extreme in EXTREME_RAYS:
        keys = {
            row: (
                dot(value, extreme),
                dot(value, interior),
            )
            for row, value in signatures.items()
        }
        minimum = min(keys.values())
        extreme_successes += any(
            mixed_counts[row] == 1 and keys[row] == minimum
            for row in mixed_counts
        )
    return old_successes, extreme_successes


def switch_options(
    order: int,
    colouring,
    normals: tuple[Normal, ...],
) -> tuple[set[int], ...]:
    diagonal = set().union(
        *(set(matching) for matching in colouring)
    )
    output = []
    for vertex in range(order):
        for colour in range(3):
            partner_colour = normals[vertex][colour]
            output.append(
                {
                    3 * other + partner_colour
                    for other in range(order)
                    if (
                        other != vertex
                        and physical(vertex, other) not in diagonal
                        and normals[other][partner_colour] == colour
                        and (
                            (
                                partner_colour,
                                colour,
                            )
                            if vertex < other
                            else (
                                colour,
                                partner_colour,
                            )
                        )
                        in balanced_allowed_entries(
                            normals[min(vertex, other)],
                            normals[max(vertex, other)],
                        )
                    )
                }
            )
    return tuple(output)


def propose_switch(
    ports: tuple[PortKey, ...],
    options: tuple[set[int], ...],
    generator: random.Random,
) -> tuple[PortKey, ...] | None:
    stub_pairs = tuple(
        (3 * left + cv, 3 * right + cu)
        for left, right, cu, cv in ports
    )
    used_physical = {
        physical(left, right)
        for left, right, _cu, _cv in ports
    }
    for _attempt in range(100):
        first_index, second_index = generator.sample(
            range(len(stub_pairs)), 2
        )
        a, b = stub_pairs[first_index]
        c, d = stub_pairs[second_index]
        alternatives = [
            ((a, c), (b, d)),
            ((a, d), (b, c)),
        ]
        generator.shuffle(alternatives)
        old_pairs = {
            physical(a // 3, b // 3),
            physical(c // 3, d // 3),
        }
        other_pairs = used_physical - old_pairs
        for first_pair, second_pair in alternatives:
            if (
                first_pair[1] not in options[first_pair[0]]
                or second_pair[1] not in options[second_pair[0]]
            ):
                continue
            first_physical = physical(
                first_pair[0] // 3, first_pair[1] // 3
            )
            second_physical = physical(
                second_pair[0] // 3, second_pair[1] // 3
            )
            if (
                first_physical == second_physical
                or first_physical in other_pairs
                or second_physical in other_pairs
            ):
                continue
            candidate = list(ports)
            candidate[first_index] = port_from_stubs(*first_pair)
            candidate[second_index] = port_from_stubs(*second_pair)
            return tuple(sorted(candidate))
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--restarts", type=int, default=100)
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--seed", type=int, default=914_202_607)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp",
            "fourteen_vertex_adversarial_potential_search.json",
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    generator = random.Random(args.seed)
    order = 14
    rows = catalogue(order)
    permutations = tuple(itertools.permutations(range(3)))
    cells = []
    for graph_index, graph6 in enumerate(rows):
        graph_edges = set(decode_graph6(graph6))
        for colouring_index, colouring in enumerate(
            kotzig_colourings(range(order), graph_edges)
        ):
            for type_index, normals in enumerate(
                normal_types(range(order), colouring)
            ):
                potentials = tuple(
                    tuple(
                        tuple(
                            permuted_potential(normal, permutation)[
                                colour
                            ]
                            for permutation in permutations
                        )
                        for colour in range(3)
                    )
                    for normal in normals
                )
                cells.append(
                    (
                        graph_index,
                        graph6,
                        colouring_index,
                        type_index,
                        colouring,
                        normals,
                        potentials,
                        switch_options(order, colouring, normals),
                    )
                )
    if len(cells) != 19_680:
        raise AssertionError("order-fourteen cell domain changed")

    evaluations = 0
    accepted = 0
    best_score = 13
    best_old = 7
    best_extreme = 7
    best_records = []

    def save(status: str) -> None:
        payload = {
            "verified": True,
            "status": status,
            "scope": (
                "random restarts and valid reciprocal two-edge port "
                "switches; exploratory, not exhaustive"
            ),
            "order": order,
            "seed": args.seed,
            "requested_restarts": args.restarts,
            "steps_per_restart": args.steps,
            "evaluations": evaluations,
            "accepted_switches": accepted,
            "best_combined_successes": best_score,
            "best_original_successes": best_old,
            "best_extreme_successes": best_extreme,
            "best_records": best_records,
            "combined_residual_found": best_score == 0,
            "sampling_complete_for_port_graphs": False,
            "order_fourteen_branch_excluded": False,
            "global_conjecture_resolved": False,
            "source": str(Path(__file__)),
            "source_sha256": sha256(Path(__file__)),
            "elapsed_seconds": time.perf_counter() - started,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8"
        )

    for restart in range(args.restarts):
        cell_id = generator.randrange(len(cells))
        (
            graph_index,
            graph6,
            colouring_index,
            type_index,
            colouring,
            normals,
            potentials,
            options,
        ) = cells[cell_id]
        raw_ports = randomized_port(
            order, colouring, normals, generator
        )
        if raw_ports is None:
            continue
        current = tuple(
            sorted(
                (port[0], port[1], port[2], port[3])
                for port in raw_ports
            )
        )
        current_old, current_extreme = evaluate(
            order, colouring, normals, current, potentials
        )
        evaluations += 1
        temperature = 1.0
        for step in range(args.steps):
            candidate = propose_switch(current, options, generator)
            if candidate is None:
                break
            candidate_old, candidate_extreme = evaluate(
                order, colouring, normals, candidate, potentials
            )
            evaluations += 1
            current_score = current_old + current_extreme
            candidate_score = candidate_old + candidate_extreme
            delta = candidate_score - current_score
            accept = (
                delta < 0
                or (
                    delta == 0
                    and generator.random() < 0.5
                )
                or generator.random()
                < math.exp(-max(0, delta) / max(0.05, temperature))
                * 0.05
            )
            if accept:
                current = candidate
                current_old = candidate_old
                current_extreme = candidate_extreme
                accepted += 1
            temperature *= 0.99
            score = candidate_old + candidate_extreme
            if (
                score < best_score
                or (
                    score == best_score
                    and (candidate_old, candidate_extreme)
                    < (best_old, best_extreme)
                )
            ):
                best_score = score
                best_old = candidate_old
                best_extreme = candidate_extreme
                best_records = [
                    {
                        "restart": restart,
                        "step": step,
                        "cell_id": cell_id,
                        "graph_index": graph_index,
                        "graph6": graph6,
                        "colouring_index": colouring_index,
                        "type_index": type_index,
                        "original_successes": candidate_old,
                        "extreme_successes": candidate_extreme,
                        "normal_types": [
                            list(normal) for normal in normals
                        ],
                        "diagonal_matchings": [
                            [list(edge) for edge in matching]
                            for matching in colouring
                        ],
                        "port_edges": [
                            {
                                "edge": [port[0], port[1]],
                                "half_colours": [port[2], port[3]],
                            }
                            for port in candidate
                        ],
                    }
                ]
                save("exploratory_adversarial_search_checkpoint")
                print(
                    "new best",
                    best_score,
                    "old",
                    best_old,
                    "extreme",
                    best_extreme,
                    "restart",
                    restart,
                    "step",
                    step,
                    "evaluations",
                    evaluations,
                    flush=True,
                )
                if best_score == 0:
                    save("exploratory_combined_residual_found")
                    return
        if (restart + 1) % 10 == 0:
            save("exploratory_adversarial_search_checkpoint")
            print(
                "restarts",
                restart + 1,
                "evaluations",
                evaluations,
                "best",
                best_score,
                "elapsed",
                round(time.perf_counter() - started, 1),
                flush=True,
            )

    save("exploratory_adversarial_search_complete")


if __name__ == "__main__":
    main()
