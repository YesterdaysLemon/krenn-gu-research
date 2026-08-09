"""Independent perfect-matching audit of the balanced-bridge obstruction.

This program deliberately does not import the primary verifier.  It builds
the physical endpoint graph for every contracted order-six port system and
directly counts compatible perfect matchings for all single-pair colour
perturbations.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time


COLOURS = (0, 1, 2)
NormalType = tuple[int, int, int]
Edge = tuple[int, int, int, int, str]


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def endpoint_types() -> tuple[NormalType, ...]:
    # Build the eight types as three binary choices, independently of the
    # Cartesian-product filter used by the primary verifier.
    return tuple(
        tuple(
            (colour + 1 + bit) % 3
            for colour, bit in enumerate(bits)
        )
        for bits in itertools.product((0, 1), repeat=3)
    )


def complementary(item: NormalType) -> NormalType:
    output = []
    for colour, normal in enumerate(item):
        candidates = [
            value
            for value in COLOURS
            if value != colour and value != normal
        ]
        if len(candidates) != 1:
            raise AssertionError("complement is not unique")
        output.append(candidates[0])
    return tuple(output)


def port_sides(item: NormalType) -> dict[tuple[int, int], int]:
    output = {}
    for side, vertex_type in enumerate((item, complementary(item))):
        for target in COLOURS:
            local = vertex_type[target]
            output[(local, target)] = side
    if len(output) != 6:
        raise AssertionError("directed port labels are not unique")
    return output


def no_fixed_points(size: int) -> tuple[tuple[int, ...], ...]:
    output = []
    for candidate in itertools.permutations(range(size)):
        if all(candidate[index] != index for index in range(size)):
            output.append(candidate)
    return tuple(output)


def physical_edges(
    types: tuple[NormalType, ...],
    matchings: tuple[tuple[int, ...], ...],
) -> list[Edge]:
    edges = []
    for pair in range(len(types)):
        edges.append(
            (2 * pair, 2 * pair + 1, -1, -1, "anchor")
        )
    colour_pairs = ((0, 1), (0, 2), (1, 2))
    sides = [port_sides(item) for item in types]
    for matching, (left, right) in zip(
        matchings, colour_pairs, strict=True
    ):
        for pair, partner in enumerate(matching):
            first = 2 * pair + sides[pair][(left, right)]
            second = 2 * partner + sides[partner][(right, left)]
            edges.append(
                (
                    first,
                    second,
                    left,
                    right,
                    f"singleton_{left}{right}_{pair}",
                )
            )
    return edges


def compatible_matchings(
    vertices: int,
    edges: list[Edge],
    colours: tuple[int, ...],
    cap: int = 2,
) -> int:
    compatible = []
    for edge in edges:
        left, right, left_colour, right_colour, kind = edge
        if kind == "anchor":
            if colours[left] == colours[right]:
                compatible.append(edge)
        elif (
            colours[left] == left_colour
            and colours[right] == right_colour
        ):
            compatible.append(edge)

    incidence: list[list[Edge]] = [[] for _ in range(vertices)]
    for edge in compatible:
        incidence[edge[0]].append(edge)
        incidence[edge[1]].append(edge)

    full_mask = (1 << vertices) - 1

    def visit(mask: int) -> int:
        if mask == full_mask:
            return 1
        first = next(
            vertex
            for vertex in range(vertices)
            if not (mask >> vertex) & 1
        )
        total = 0
        for edge in incidence[first]:
            other = edge[1] if edge[0] == first else edge[0]
            if (mask >> other) & 1:
                continue
            total += visit(mask | (1 << first) | (1 << other))
            if total >= cap:
                return cap
        return total

    return visit(0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--analysis",
        type=Path,
        default=Path(
            "tmp/four_regular_balanced_bridge_obstruction_verified.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/four_regular_balanced_bridge_obstruction_audited.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    started = time.perf_counter()
    source = json.loads(args.analysis.read_text(encoding="utf-8"))
    if (
        source.get("verified") is not True
        or source.get("status")
        != "four_regular_balanced_bridge_obstruction_verified"
    ):
        raise AssertionError("primary analysis is not verified")

    types = endpoint_types()
    if len(types) != 8 or len(set(types)) != 8:
        raise AssertionError("independent normal-type census changed")
    usable_distribution = Counter()
    independent_records = []
    for item in types:
        sides = port_sides(item)
        usable = []
        for local in COLOURS:
            targets = [
                target for target in COLOURS if target != local
            ]
            if (
                sides[(local, targets[0])]
                != sides[(local, targets[1])]
            ):
                usable.append(local)
        usable_distribution[len(usable)] += 1
        independent_records.append(
            {
                "normals": list(item),
                "complement": list(complementary(item)),
                "usable_pair_constant_colours": usable,
            }
        )
    if usable_distribution != {1: 6, 3: 2}:
        raise AssertionError("independent transition census changed")

    size = 3
    derangements = no_fixed_points(size)
    configurations = 0
    colourings = 0
    matching_calls = 0
    minimum_unique = 2 * size
    matching_count_distribution = Counter()
    for chosen_types in itertools.product(types, repeat=size):
        for chosen_matchings in itertools.product(
            derangements, repeat=3
        ):
            edges = physical_edges(chosen_types, chosen_matchings)
            configurations += 1
            for background in COLOURS:
                unique = 0
                for pair in range(size):
                    for colour in COLOURS:
                        if colour == background:
                            continue
                        pair_colours = [background] * size
                        pair_colours[pair] = colour
                        vertex_colours = tuple(
                            pair_colours[vertex // 2]
                            for vertex in range(2 * size)
                        )
                        count = compatible_matchings(
                            2 * size, edges, vertex_colours
                        )
                        matching_count_distribution[count] += 1
                        if count == 1:
                            unique += 1
                        elif count < 1:
                            raise AssertionError(
                                "anchor matching disappeared"
                            )
                        colourings += 1
                        matching_calls += 1
                if unique < size:
                    raise AssertionError(
                        "fewer than m unique-anchor perturbations"
                    )
                minimum_unique = min(minimum_unique, unique)

    if (
        configurations != 4_096
        or colourings != 73_728
        or matching_calls != colourings
        or minimum_unique < size
    ):
        raise AssertionError("independent order-six totals changed")
    if source.get("order_six_contracted_configurations") != configurations:
        raise AssertionError("primary configuration count disagrees")
    if (
        source.get("order_six_perturbations_checked")
        != colourings
    ):
        raise AssertionError("primary perturbation count disagrees")

    payload = {
        "verified": True,
        "status": (
            "four_regular_balanced_bridge_obstruction_"
            "independently_audited"
        ),
        "scope": (
            "independent type and transition reconstruction plus direct "
            "perfect-matching enumeration for all contracted order-six "
            "configurations and one-pair colour perturbations"
        ),
        "analysis": str(args.analysis),
        "analysis_sha256": file_hash(args.analysis),
        "normal_types": len(types),
        "independent_local_records": independent_records,
        "usable_colour_count_distribution": {
            str(key): value
            for key, value in sorted(usable_distribution.items())
        },
        "order_six_configurations": configurations,
        "order_six_colourings": colourings,
        "direct_matching_enumerations": matching_calls,
        "matching_count_capped_distribution": {
            str(key): value
            for key, value in sorted(
                matching_count_distribution.items()
            )
        },
        "minimum_unique_anchor_perturbations_per_background": (
            minimum_unique
        ),
        "anchor_matching_unique_bound_verified": True,
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
