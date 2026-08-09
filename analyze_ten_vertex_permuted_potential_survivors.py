"""Apply all six colour-permuted potentials to the order-ten residuals."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
import time
from pathlib import Path

from analyze_ten_vertex_degree_six_kotzig_port_survivors import (
    allowed_unit,
    enumerate_coloured_matchings,
)

NormalType = tuple[int, int, int]
Permutation = tuple[int, int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def base_potential(normal: NormalType) -> tuple[int, int, int]:
    b0 = int(normal[0] == 2)
    b1 = int(normal[1] == 2)
    b2 = int(normal[2] == 1)
    return (
        1 - 2 * b2,
        2 * (b2 - b0),
        2 * (b0 + b1 - 1),
    )


def permuted_potential(
    normal: NormalType, permutation: Permutation
) -> tuple[int, int, int]:
    relabelled = [-1] * 3
    for old_colour in range(3):
        relabelled[permutation[old_colour]] = permutation[
            normal[old_colour]
        ]
    relabelled_values = base_potential(
        tuple(relabelled)
    )
    return tuple(
        relabelled_values[permutation[old_colour]]
        for old_colour in range(3)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--primary",
        type=Path,
        default=Path(
            "tmp",
            "ten_vertex_degree_six_kotzig_ports_explored.json",
        ),
    )
    parser.add_argument(
        "--base-theorem",
        type=Path,
        default=Path(
            "claims",
            "arbitrary-order",
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
            "ten_vertex_permuted_potential_survivors_analyzed.json",
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    source = json.loads(args.primary.read_text(encoding="utf-8"))
    records = list(source["survivor_records"])
    if (
        len(records) != 392
        or source.get("survivors") != 392
        or source.get("theorem_sha256")
        != sha256(args.base_theorem)
    ):
        raise AssertionError(
            "identity-potential survivor binding changed"
        )

    permutations = tuple(itertools.permutations(range(3)))
    success_by_permutation: Counter[int] = Counter()
    success_count_histogram: Counter[int] = Counter()
    success_set_histogram: Counter[tuple[int, ...]] = Counter()
    chosen_permutation_histogram: Counter[int] = Counter()
    survivor_records = []
    result_records = []

    for survivor_index, record in enumerate(records):
        normals = tuple(
            tuple(map(int, item)) for item in record["normal_types"]
        )
        guaranteed = []
        diagonal_rows = []
        for colour, matching in enumerate(
            record["diagonal_matchings"]
        ):
            for raw_pair in matching:
                left, right = map(int, raw_pair)
                guaranteed.append(
                    (
                        left,
                        right,
                        colour,
                        colour,
                        True,
                        "D",
                        0,
                    )
                )
                diagonal_rows.append((left, right, colour))
        for port in record["port_edges"]:
            left, right = map(int, port["edge"])
            first, second = map(int, port["half_colours"])
            guaranteed.append(
                (
                    left,
                    right,
                    first,
                    second,
                    True,
                    "K",
                    int(port["potential"]),
                )
            )

        counts, _first, _forced = enumerate_coloured_matchings(
            10, tuple(guaranteed)
        )
        mixed = {
            colouring: count
            for colouring, count in counts.items()
            if len(set(colouring)) > 1
        }
        successes = []
        signatures = []
        for permutation_index, permutation in enumerate(
            permutations
        ):
            potentials = tuple(
                permuted_potential(normal, permutation)
                for normal in normals
            )
            for left, right, colour in diagonal_rows:
                if (
                    potentials[left][colour]
                    + potentials[right][colour]
                    != 0
                ):
                    raise AssertionError(
                        "permuted own-diagonal potential changed"
                    )
                optional = [
                    (row, column)
                    for row in range(3)
                    for column in range(3)
                    if (
                        row != column
                        and allowed_unit(
                            normals[left],
                            normals[right],
                            row,
                            column,
                        )
                    )
                ]
                if any(
                    (
                        potentials[left][row]
                        + potentials[right][column]
                        <= 0
                    )
                    for row, column in optional
                ):
                    raise AssertionError(
                        "permuted optional potential is not positive"
                    )

            minimum = min(
                sum(
                    potentials[vertex][colour]
                    for vertex, colour in enumerate(colouring)
                )
                for colouring in mixed
            )
            minimum_rows = {
                colouring: count
                for colouring, count in mixed.items()
                if sum(
                    potentials[vertex][colour]
                    for vertex, colour in enumerate(colouring)
                )
                == minimum
            }
            multiplicities = tuple(
                sorted(Counter(minimum_rows.values()).items())
            )
            signatures.append(
                {
                    "permutation_index": permutation_index,
                    "minimum_potential": minimum,
                    "minimum_multiplicity_histogram": {
                        str(key): value
                        for key, value in multiplicities
                    },
                }
            )
            if any(count == 1 for count in minimum_rows.values()):
                successes.append(permutation_index)
                success_by_permutation[permutation_index] += 1

        if 0 in successes:
            raise AssertionError(
                "identity potential unexpectedly resolved a source survivor"
            )
        success_count_histogram[len(successes)] += 1
        success_set_histogram[tuple(successes)] += 1
        if not successes:
            survivor_records.append(
                {
                    "survivor_index": survivor_index,
                    "signatures": signatures,
                }
            )
            continue
        chosen_permutation_histogram[successes[0]] += 1
        result_records.append(
            {
                "survivor_index": survivor_index,
                "successful_permutation_indices": successes,
                "chosen_permutation_index": successes[0],
                "signatures": signatures,
            }
        )

    payload = {
        "verified": len(survivor_records) == 0,
        "status": "finite_permuted_potential_analysis",
        "scope": (
            "all six colour-permuted positive potentials on the 392 "
            "identity-potential residuals of the complete order-ten "
            "exact-degree-six Kotzig/port census"
        ),
        "primary": str(args.primary),
        "primary_sha256": sha256(args.primary),
        "base_theorem": str(args.base_theorem),
        "base_theorem_sha256": sha256(args.base_theorem),
        "lemma": str(args.lemma),
        "lemma_sha256": sha256(args.lemma),
        "permutations": [list(item) for item in permutations],
        "identity_residuals": len(records),
        "successes_by_permutation": {
            str(index): success_by_permutation[index]
            for index in range(len(permutations))
        },
        "successful_nonidentity_potential_count_histogram": {
            str(key): value
            for key, value in sorted(
                success_count_histogram.items()
            )
        },
        "successful_permutation_set_histogram": [
            {
                "permutation_indices": list(indices),
                "residuals": count,
            }
            for indices, count in sorted(
                success_set_histogram.items()
            )
        ],
        "first_successful_permutation_histogram": {
            str(key): value
            for key, value in sorted(
                chosen_permutation_histogram.items()
            )
        },
        "result_records": result_records,
        "survivors": len(survivor_records),
        "survivor_records": survivor_records,
        "finite_identity_residuals_excluded": (
            len(survivor_records) == 0
        ),
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
