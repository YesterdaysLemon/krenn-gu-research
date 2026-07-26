"""Independent audit of the six-potential order-ten residual exclusion."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
import time
from pathlib import Path

NormalType = tuple[int, int, int]
Permutation = tuple[int, int, int]
ColouredEdge = tuple[int, int, int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def direct_base_values(normal: NormalType) -> tuple[int, int, int]:
    first_bit = 1 if normal[0] == 2 else 0
    second_bit = 1 if normal[1] == 2 else 0
    third_bit = 1 if normal[2] == 1 else 0
    return (
        1 - 2 * third_bit,
        2 * third_bit - 2 * first_bit,
        2 * first_bit + 2 * second_bit - 2,
    )


def independently_relabelled_values(
    normal: NormalType, permutation: Permutation
) -> tuple[int, int, int]:
    inverse = [0] * 3
    for old, new in enumerate(permutation):
        inverse[new] = old
    renamed = tuple(
        permutation[normal[inverse[new]]]
        for new in range(3)
    )
    renamed_values = direct_base_values(renamed)
    return tuple(
        renamed_values[permutation[old]]
        for old in range(3)
    )


def direct_allowed(
    left: NormalType,
    right: NormalType,
    row: int,
    column: int,
) -> bool:
    for target in range(3):
        if (row, column) == (target, target):
            continue
        if row == left[target] or column == right[target]:
            continue
        return False
    return True


def colouring_multiplicities(
    order: int, edges: tuple[ColouredEdge, ...]
) -> Counter[tuple[int, ...]]:
    incident: list[list[int]] = [[] for _ in range(order)]
    for edge_id, item in enumerate(edges):
        incident[item[0]].append(edge_id)
        incident[item[1]].append(edge_id)
    counts: Counter[tuple[int, ...]] = Counter()
    colours = [-1] * order

    def search(unused: frozenset[int]) -> None:
        if not unused:
            counts[tuple(colours)] += 1
            return
        root = min(unused)
        for edge_id in incident[root]:
            left, right, first_colour, second_colour = edges[edge_id]
            if right == root:
                left, right = right, left
                first_colour, second_colour = (
                    second_colour,
                    first_colour,
                )
            if right not in unused:
                continue
            colours[left] = first_colour
            colours[right] = second_colour
            search(unused - {left, right})
            colours[left] = -1
            colours[right] = -1

    search(frozenset(range(order)))
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--identity-census",
        type=Path,
        default=Path(
            "tmp",
            "ten_vertex_degree_six_kotzig_ports_explored.json",
        ),
    )
    parser.add_argument(
        "--primary",
        type=Path,
        default=Path(
            "tmp",
            "ten_vertex_permuted_potential_survivors_analyzed.json",
        ),
    )
    parser.add_argument(
        "--base-theorem",
        type=Path,
        default=Path(
            "THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM.md"
        ),
    )
    parser.add_argument(
        "--lemma",
        type=Path,
        default=Path("SIX_PERMUTED_POTENTIALS_LEMMA.md"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp",
            "ten_vertex_permuted_potential_survivors_audited.json",
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    census = json.loads(
        args.identity_census.read_text(encoding="utf-8")
    )
    records = list(census["survivor_records"])
    if (
        len(records) != 392
        or census.get("survivors") != 392
        or census.get("theorem_sha256")
        != sha256(args.base_theorem)
    ):
        raise AssertionError(
            "independent identity-residual binding changed"
        )

    permutations = tuple(itertools.permutations(range(3)))
    success_by_permutation: Counter[int] = Counter()
    success_counts: Counter[int] = Counter()
    success_sets: Counter[tuple[int, ...]] = Counter()
    first_successes: Counter[int] = Counter()
    survivors = []
    local_diagonal_checks = 0
    local_optional_checks = 0

    for survivor_index, record in enumerate(records):
        normals = tuple(
            tuple(map(int, item)) for item in record["normal_types"]
        )
        edges = []
        diagonal_rows = []
        for colour, matching in enumerate(
            record["diagonal_matchings"]
        ):
            for raw_pair in matching:
                left, right = map(int, raw_pair)
                edges.append(
                    (left, right, colour, colour)
                )
                diagonal_rows.append((left, right, colour))
        for port in record["port_edges"]:
            left, right = map(int, port["edge"])
            first, second = map(int, port["half_colours"])
            edges.append((left, right, first, second))

        all_counts = colouring_multiplicities(
            10, tuple(edges)
        )
        mixed = {
            colouring: count
            for colouring, count in all_counts.items()
            if len(set(colouring)) > 1
        }
        successful = []
        for permutation_index, permutation in enumerate(
            permutations
        ):
            potentials = tuple(
                independently_relabelled_values(
                    normal, permutation
                )
                for normal in normals
            )
            for left, right, colour in diagonal_rows:
                if (
                    potentials[left][colour]
                    + potentials[right][colour]
                    != 0
                ):
                    raise AssertionError(
                        "independent permuted diagonal check changed"
                    )
                local_diagonal_checks += 1
                for row in range(3):
                    for column in range(3):
                        if (
                            row == column
                            or not direct_allowed(
                                normals[left],
                                normals[right],
                                row,
                                column,
                            )
                        ):
                            continue
                        if (
                            potentials[left][row]
                            + potentials[right][column]
                            <= 0
                        ):
                            raise AssertionError(
                                "independent permuted optional check changed"
                            )
                        local_optional_checks += 1

            minimum = min(
                sum(
                    potentials[vertex][colour]
                    for vertex, colour in enumerate(colouring)
                )
                for colouring in mixed
            )
            minimum_counts = [
                count
                for colouring, count in mixed.items()
                if sum(
                    potentials[vertex][colour]
                    for vertex, colour in enumerate(colouring)
                )
                == minimum
            ]
            if 1 in minimum_counts:
                successful.append(permutation_index)
                success_by_permutation[permutation_index] += 1

        if 0 in successful:
            raise AssertionError(
                "independent identity residual was not residual"
            )
        success_counts[len(successful)] += 1
        success_sets[tuple(successful)] += 1
        if successful:
            first_successes[successful[0]] += 1
        else:
            survivors.append(survivor_index)

    observed = {
        "identity_residuals": len(records),
        "successes_by_permutation": {
            str(index): success_by_permutation[index]
            for index in range(len(permutations))
        },
        "successful_nonidentity_potential_count_histogram": {
            str(key): value
            for key, value in sorted(success_counts.items())
        },
        "successful_permutation_set_histogram": [
            {
                "permutation_indices": list(indices),
                "residuals": count,
            }
            for indices, count in sorted(success_sets.items())
        ],
        "first_successful_permutation_histogram": {
            str(key): value
            for key, value in sorted(first_successes.items())
        },
        "survivors": len(survivors),
    }
    primary = json.loads(args.primary.read_text(encoding="utf-8"))
    if (
        primary.get("primary_sha256")
        != sha256(args.identity_census)
        or primary.get("base_theorem_sha256")
        != sha256(args.base_theorem)
        or primary.get("lemma_sha256")
        != sha256(args.lemma)
        or any(
            primary.get(key) != value
            for key, value in observed.items()
        )
    ):
        raise AssertionError(
            "primary and independent permuted-potential analyses disagree"
        )
    if survivors:
        raise AssertionError(
            "a residual survived all six potentials"
        )

    payload = {
        "verified": True,
        "status": "independent_finite_permuted_potential_audit",
        "scope": (
            "separate colour relabelling, local diagonal/optional "
            "potential checks, guaranteed matching enumeration, and "
            "six minimum-layer multiplicity tests on all 392 "
            "order-ten identity residuals"
        ),
        "identity_census": str(args.identity_census),
        "identity_census_sha256": sha256(args.identity_census),
        "primary": str(args.primary),
        "primary_sha256": sha256(args.primary),
        "base_theorem": str(args.base_theorem),
        "base_theorem_sha256": sha256(args.base_theorem),
        "lemma": str(args.lemma),
        "lemma_sha256": sha256(args.lemma),
        "permutations": [list(item) for item in permutations],
        **observed,
        "local_diagonal_checks": local_diagonal_checks,
        "local_optional_checks": local_optional_checks,
        "finite_identity_residuals_excluded": True,
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
