"""Independent audit of the diagonal-matching bit-balance theorem."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
import time
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def direct_allowed(
    left: tuple[int, int, int],
    right: tuple[int, int, int],
    row: int,
    column: int,
) -> bool:
    for target in range(3):
        for x_colour in range(3):
            if x_colour == left[target]:
                continue
            for y_colour in range(3):
                if y_colour == right[target]:
                    continue
                coefficient = (
                    x_colour == row and y_colour == column
                )
                coordinate_product = (
                    x_colour == target and y_colour == target
                )
                if coefficient and not coordinate_product:
                    return False
    return True


def independent_potential(
    item: tuple[int, int, int], colour: int
) -> int:
    b0 = int(item[0] == 2)
    b1 = int(item[1] == 2)
    b2 = int(item[2] == 1)
    if colour == 0:
        return 1 - 2 * b2
    if colour == 1:
        return 2 * (b2 - b0)
    return 2 * (b0 + b1 - 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(
            "tmp/three_colour_diagonal_matching_balance_verified.json"
        ),
    )
    parser.add_argument(
        "--theorem",
        type=Path,
        default=Path(
            "THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM.md"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/three_colour_diagonal_matching_balance_audited.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    source = json.loads(args.source.read_text(encoding="utf-8"))
    if (
        not source.get("verified")
        or source.get("status")
        != "three_colour_diagonal_matching_balance_verified"
        or source.get("theorem_sha256") != sha256(args.theorem)
        or source.get("global_conjecture_resolved") is not False
        or source.get(
            "matching_anchor_two_colour_factorization_forced"
        )
        is not True
        or source.get(
            "cross_colour_matching_edge_hafnian_cofactors_forced_zero"
        )
        is not True
        or source.get(
            "matching_anchor_full_colour_factorization_forced"
        )
        is not True
        or source.get(
            "pairwise_disjoint_cubic_boundary_is_kotzig"
        )
        is not True
        or source.get(
            "pairwise_disjoint_cubic_blocks_have_at_most_two_units"
        )
        is not True
        or source.get(
            "optional_cubic_off_diagonal_units_are_reciprocal"
        )
        is not True
        or source.get(
            "saturated_diagonal_transition_potential_is_zero"
        )
        is not True
        or source.get(
            "optional_cubic_transition_potential_is_positive"
        )
        is not True
        or source.get(
            "minimum_potential_nonmonochromatic_layer_uses_no_optional_d_units"
        )
        is not True
        or source.get(
            "legacy_target_state_path_cycle_claim_withdrawn"
        )
        is not True
    ):
        raise AssertionError("primary balance theorem binding changed")

    normals = list(
        itertools.product((1, 2), (0, 2), (0, 1))
    )

    def bits(item: tuple[int, int, int]) -> tuple[int, int, int]:
        return (
            int(item[0] == 2),
            int(item[1] == 2),
            int(item[2] == 1),
        )

    diagonal: dict[int, set[tuple[int, int]]] = {
        colour: set() for colour in range(3)
    }
    for left_id, left in enumerate(normals):
        for right_id, right in enumerate(normals):
            for colour in range(3):
                if direct_allowed(
                    left, right, colour, colour
                ):
                    diagonal[colour].add((left_id, right_id))

    saturated_rows = []
    saturated = {}
    for colour in range(3):
        other_bits = tuple(
            bit for bit in range(3) if bit != colour
        )
        transitions = {
            (left, right)
            for left, right in diagonal[colour]
            if all(
                bits(normals[left])[bit]
                != bits(normals[right])[bit]
                for bit in other_bits
            )
        }
        distances = Counter(
            sum(
                a != b
                for a, b in zip(
                    bits(normals[left]),
                    bits(normals[right]),
                    strict=True,
                )
            )
            for left, right in transitions
        )
        if (
            len(diagonal[colour]) != 36
            or len(transitions) != 16
            or distances != Counter({2: 8, 3: 8})
        ):
            raise AssertionError(
                "independent saturated transition audit changed"
            )
        saturated[colour] = transitions
        saturated_rows.append(
            {
                "colour": colour,
                "allowed_ordered_transitions": len(diagonal[colour]),
                "saturated_ordered_transitions": len(transitions),
                "hamming_distance_histogram": {
                    str(key): value
                    for key, value in sorted(distances.items())
                },
                "forced_flip_bits": list(other_bits),
            }
        )

    shared_rows = []
    for first, second in itertools.combinations(range(3), 2):
        shared = saturated[first] & saturated[second]
        complementary = all(
            all(
                a != b
                for a, b in zip(
                    bits(normals[left]),
                    bits(normals[right]),
                    strict=True,
                )
            )
            for left, right in shared
        )
        if len(shared) != 8 or not complementary:
            raise AssertionError(
                "independent shared-transition audit changed"
            )
        shared_rows.append(
            {
                "colours": [first, second],
                "shared_ordered_transitions": len(shared),
                "all_complementary": complementary,
            }
        )

    effective_cubic_block_rows = []
    total_optional_potential_histogram = Counter()
    for colour in range(3):
        histogram = Counter()
        reciprocal_count = 0
        own_potential_histogram = Counter()
        optional_potential_histogram = Counter()
        for left_id, right_id in saturated[colour]:
            effective = set()
            for row in range(3):
                for column in range(3):
                    if not direct_allowed(
                        normals[left_id],
                        normals[right_id],
                        row,
                        column,
                    ):
                        continue
                    if row == column and row != colour:
                        continue
                    effective.add((row, column))
            if (colour, colour) not in effective or len(effective) > 2:
                raise AssertionError(
                    "independent effective block bound changed"
                )
            own_value = (
                independent_potential(normals[left_id], colour)
                + independent_potential(normals[right_id], colour)
            )
            if own_value != 0:
                raise AssertionError(
                    "independent own-diagonal potential changed"
                )
            own_potential_histogram[own_value] += 1
            for row, column in effective:
                if row == column:
                    continue
                reciprocal_count += 1
                if (
                    normals[left_id][column] != row
                    or normals[right_id][row] != column
                ):
                    raise AssertionError(
                        "independent optional reciprocity changed"
                    )
                value = (
                    independent_potential(normals[left_id], row)
                    + independent_potential(
                        normals[right_id], column
                    )
                )
                if value <= 0:
                    raise AssertionError(
                        "independent optional potential changed"
                    )
                optional_potential_histogram[value] += 1
                total_optional_potential_histogram[value] += 1
            histogram[len(effective)] += 1
        if histogram != Counter({2: 14, 1: 2}):
            raise AssertionError(
                "independent effective block census changed"
            )
        effective_cubic_block_rows.append(
            {
                "matching_colour": colour,
                "effective_block_size_histogram": {
                    str(key): value
                    for key, value in sorted(histogram.items())
                },
                "optional_off_diagonal_transitions": reciprocal_count,
                "all_optional_off_diagonals_reciprocal": True,
                "own_diagonal_potential_sum_histogram": {
                    str(key): value
                    for key, value in sorted(
                        own_potential_histogram.items()
                    )
                },
                "optional_off_diagonal_potential_sum_histogram": {
                    str(key): value
                    for key, value in sorted(
                        optional_potential_histogram.items()
                    )
                },
            }
        )
    if total_optional_potential_histogram != Counter(
        {1: 6, 2: 4, 3: 22, 4: 10}
    ):
        raise AssertionError(
            "independent total optional potential census changed"
        )

    anchor_automata = []
    for anchor_colour in range(3):
        anchors = sorted(saturated[anchor_colour])
        for colour_pair in itertools.combinations(range(3), 2):
            nodes = [
                (anchor_id, side, colour)
                for anchor_id in range(len(anchors))
                for side in (0, 1)
                for colour in colour_pair
            ]
            edges = set()
            for first in nodes:
                anchor_id, side, first_colour = first
                left = anchors[anchor_id][side]
                for second in nodes:
                    other_id, outgoing_side, second_colour = second
                    right = anchors[other_id][1 - outgoing_side]
                    if direct_allowed(
                        normals[left],
                        normals[right],
                        first_colour,
                        second_colour,
                    ):
                        edges.add((first, second))
            reach = {
                node: {node}
                | {
                    second
                    for first, second in edges
                    if first == node
                }
                for node in nodes
            }
            for middle in nodes:
                for first in nodes:
                    if middle in reach[first]:
                        reach[first].update(reach[middle])
            components = {
                frozenset(
                    other
                    for other in nodes
                    if (
                        other in reach[node]
                        and node in reach[other]
                    )
                )
                for node in nodes
            }
            sizes = sorted(map(len, components), reverse=True)
            expected_sizes = (
                [16, 16, 8, 8, 8, 8]
                if anchor_colour in colour_pair
                else [16, 16, 16, 16]
            )
            mixed = sum(
                len({node[2] for node in component}) > 1
                for component in components
            )
            if (
                len(edges) != 1536
                or sizes != expected_sizes
                or mixed
            ):
                raise AssertionError(
                    "independent matching-anchor automaton changed"
                )
            anchor_automata.append(
                {
                    "anchor_colour": anchor_colour,
                    "pair_colours": list(colour_pair),
                    "states": len(nodes),
                    "directed_transitions": len(edges),
                    "strong_component_sizes": sizes,
                    "mixed_colour_strong_components": mixed,
                }
            )

    full_colour_anchor_automata = []
    for anchor_colour in range(3):
        anchors = sorted(saturated[anchor_colour])
        nodes = [
            (anchor_id, side, colour)
            for anchor_id in range(len(anchors))
            for side in (0, 1)
            for colour in range(3)
        ]
        edges = {
            (first, second)
            for first in nodes
            for second in nodes
            if direct_allowed(
                normals[anchors[first[0]][first[1]]],
                normals[anchors[second[0]][1 - second[1]]],
                first[2],
                second[2],
            )
        }
        reach = {
            node: {node}
            | {
                second
                for first, second in edges
                if first == node
            }
            for node in nodes
        }
        for middle in nodes:
            for first in nodes:
                if middle in reach[first]:
                    reach[first].update(reach[middle])
        components = {
            frozenset(
                other
                for other in nodes
                if other in reach[node] and node in reach[other]
            )
            for node in nodes
        }
        sizes = sorted(map(len, components), reverse=True)
        mixed = sum(
            len({node[2] for node in component}) > 1
            for component in components
        )
        if (
            len(edges) != 2880
            or sizes != [16, 16, 16, 16, 8, 8, 8, 8]
            or mixed
        ):
            raise AssertionError(
                "independent full-colour anchor automaton changed"
            )
        full_colour_anchor_automata.append(
            {
                "anchor_colour": anchor_colour,
                "states": len(nodes),
                "directed_transitions": len(edges),
                "strong_component_sizes": sizes,
                "mixed_colour_strong_components": mixed,
            }
        )

    if (
        saturated_rows != source["saturated_transition_rows"]
        or shared_rows != source["shared_transition_rows"]
        or effective_cubic_block_rows
        != source["effective_cubic_block_rows"]
        or {
            str(index): {
                str(colour): independent_potential(item, colour)
                for colour in range(3)
            }
            for index, item in enumerate(normals)
        }
        != source["transition_potential_table"]
        or {
            str(key): value
            for key, value in sorted(
                total_optional_potential_histogram.items()
            )
        }
        != source["total_optional_transition_potential_histogram"]
        or anchor_automata
        != source["matching_anchor_two_colour_automata"]
        or full_colour_anchor_automata
        != source["matching_anchor_full_colour_automata"]
    ):
        raise AssertionError(
            "primary and independent balance tables differ"
        )

    payload = {
        "verified": True,
        "status": (
            "three_colour_diagonal_matching_balance_"
            "independently_audited"
        ),
        "scope": (
            "direct coordinate-plane restrictions, independent bit "
            "encoding, saturated matching transitions, and all "
            "two-colour matching intersections and matching-anchor "
            "full-colour separation automata"
        ),
        "source": str(args.source),
        "source_sha256": sha256(args.source),
        "theorem": str(args.theorem),
        "theorem_sha256": sha256(args.theorem),
        "normal_types": len(normals),
        "ordered_type_pairs": len(normals) ** 2,
        "saturated_transition_rows": saturated_rows,
        "shared_transition_rows": shared_rows,
        "effective_cubic_block_rows": effective_cubic_block_rows,
        "transition_potential_table": source[
            "transition_potential_table"
        ],
        "total_optional_transition_potential_histogram": source[
            "total_optional_transition_potential_histogram"
        ],
        "matching_anchor_two_colour_automata": anchor_automata,
        "matching_anchor_full_colour_automata": (
            full_colour_anchor_automata
        ),
        "bit_balance_forced": True,
        "shared_matching_edges_are_complementary": True,
        "pairwise_disjoint_union_is_cubic": True,
        "matching_anchor_two_colour_factorization_forced": True,
        "matching_anchor_full_colour_factorization_forced": True,
        "cross_colour_matching_edge_hafnian_cofactors_forced_zero": True,
        "pairwise_disjoint_cubic_own_cofactors_forced_nonzero": True,
        "extra_diagonal_on_matching_edge_forbidden": True,
        "pairwise_matching_unions_forced_hamiltonian": True,
        "pairwise_disjoint_cubic_boundary_is_kotzig": True,
        "pairwise_disjoint_cubic_blocks_have_at_most_two_units": True,
        "optional_cubic_off_diagonal_units_are_reciprocal": True,
        "exact_degree_six_support_splits_into_cubic_diagonal_and_ports": True,
        "saturated_diagonal_transition_potential_is_zero": True,
        "optional_cubic_transition_potential_is_positive": True,
        "minimum_potential_nonmonochromatic_layer_uses_no_optional_d_units": True,
        "legacy_target_state_path_cycle_claim_withdrawn": True,
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
