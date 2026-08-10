"""Find exact one-vertex cancellation-transport certificates at order 14.

The input is a JSON support manifest with ``best_singleton_matchings`` and
the fixed full factor ``C3 + C4 + C7`` used by the order-14 experiments.
Unlike the Laurent-signature scanner, this program records every active
perfect matching as an exact bit set.  It therefore tests the elementary
cancellation-transport lemma directly, without probabilistic hashing.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Sequence

import numpy as np

from analyze_fourteen_vertex_full_direct_motifs import (
    EQUATIONS,
    FULL_EDGES,
    N,
    edge,
    extension_offsets,
    indexed_colouring,
    perfect_matchings,
)

Edge = tuple[int, int]


def active_bitsets(
    matchings: Sequence[Sequence[Edge]],
    labels: dict[Edge, int],
) -> tuple[np.ndarray, np.ndarray, int]:
    words = (len(matchings) + 63) // 64
    bitsets = np.zeros((EQUATIONS, words), dtype=np.uint64)
    counts = np.zeros(EQUATIONS, dtype=np.int16)
    offset_cache: dict[tuple[int, ...], np.ndarray] = {}
    total_extensions = 0
    for matching_id, matching in enumerate(matchings):
        requirements = {
            vertex: labels[item]
            for item in matching
            if item in labels
            for vertex in item
        }
        base = sum(
            colour * (3**vertex)
            for vertex, colour in requirements.items()
        )
        free = tuple(
            vertex for vertex in range(N) if vertex not in requirements
        )
        indices = base + extension_offsets(free, offset_cache)
        word, position = divmod(matching_id, 64)
        bitsets[indices, word] |= np.uint64(1) << np.uint64(position)
        counts[indices] += 1
        total_extensions += len(indices)
    return bitsets, counts, total_extensions


def active_ids(row: np.ndarray, matching_count: int) -> list[int]:
    output: list[int] = []
    for matching_id in range(matching_count):
        word, position = divmod(matching_id, 64)
        if int(row[word]) & (1 << position):
            output.append(matching_id)
    return output


def extra_id(
    large: np.ndarray,
    small: np.ndarray,
    matching_count: int,
) -> int:
    difference = np.bitwise_and(large, np.bitwise_not(small))
    ids = active_ids(difference, matching_count)
    if len(ids) != 1:
        raise AssertionError("set difference is not a singleton")
    return ids[0]


def partner_at(matching: Sequence[Edge], vertex: int) -> int:
    incident = [item for item in matching if vertex in item]
    if len(incident) != 1:
        raise AssertionError("not a perfect matching at the changed vertex")
    first, second = incident[0]
    return second if first == vertex else first


def find_transport(
    bitsets: np.ndarray,
    counts: np.ndarray,
    matchings: Sequence[Sequence[Edge]],
) -> dict[str, object] | None:
    indices = np.arange(EQUATIONS, dtype=np.int64)
    monochromatic = {
        sum(colour * (3**vertex) for vertex in range(N))
        for colour in range(3)
    }
    for vertex in range(N):
        weight = 3**vertex
        zero = indices[((indices // weight) % 3) == 0]
        colour_rows = (zero, zero + weight, zero + 2 * weight)
        for first_colour, second_colour in ((0, 1), (0, 2), (1, 2)):
            first_rows = colour_rows[first_colour]
            second_rows = colour_rows[second_colour]
            for rich_rows, sparse_rows in (
                (first_rows, second_rows),
                (second_rows, first_rows),
            ):
                eligible = (
                    (counts[sparse_rows] >= 1)
                    & (counts[rich_rows] == counts[sparse_rows] + 1)
                )
                for word in range(bitsets.shape[1]):
                    sparse_word = bitsets[sparse_rows, word]
                    eligible &= (
                        np.bitwise_and(
                            sparse_word, bitsets[rich_rows, word]
                        )
                        == sparse_word
                    )
                for position in np.flatnonzero(eligible):
                    rich_index = int(rich_rows[position])
                    sparse_index = int(sparse_rows[position])
                    if (
                        rich_index in monochromatic
                        or sparse_index in monochromatic
                    ):
                        continue
                    sparse_ids = active_ids(
                        bitsets[sparse_index], len(matchings)
                    )
                    partners = {
                        partner_at(matchings[item], vertex)
                        for item in sparse_ids
                    }
                    if len(partners) != 1:
                        continue
                    partner = next(iter(partners))
                    common_edge = edge(vertex, partner)
                    if common_edge not in FULL_EDGES:
                        raise AssertionError(
                            "a singleton edge cannot remain active when "
                            "one endpoint changes colour"
                        )
                    rich_ids = active_ids(
                        bitsets[rich_index], len(matchings)
                    )
                    return {
                        "changed_vertex": vertex,
                        "common_partner": partner,
                        "common_full_edge": list(common_edge),
                        "sparse_equation_index": sparse_index,
                        "sparse_colouring": list(
                            indexed_colouring(sparse_index)
                        ),
                        "sparse_activity": sparse_ids,
                        "rich_equation_index": rich_index,
                        "rich_colouring": list(
                            indexed_colouring(rich_index)
                        ),
                        "rich_activity": rich_ids,
                        "extra_matching": extra_id(
                            bitsets[rich_index],
                            bitsets[sparse_index],
                            len(matchings),
                        ),
                    }
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_cancellation_transport.json"
        ),
    )
    args = parser.parse_args()
    candidate = json.loads(
        args.candidate.read_text(encoding="utf-8")
    )
    singleton_matchings = [
        tuple(edge(*map(int, item)) for item in matching)
        for matching in candidate["best_singleton_matchings"]
    ]
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    skeleton = set(FULL_EDGES) | set(labels)
    matchings = perfect_matchings(skeleton)
    started = time.perf_counter()
    bitsets, counts, total_extensions = active_bitsets(matchings, labels)
    certificate = find_transport(bitsets, counts, matchings)
    payload = {
        "status": (
            "cancellation_transport_contradiction"
            if certificate is not None
            else "cancellation_transport_absent"
        ),
        "necessary_conditions_only": certificate is None,
        "candidate": str(args.candidate),
        "full_cycle_type": [3, 4, 7],
        "skeleton_perfect_matchings": len(matchings),
        "colourings_scanned": EQUATIONS,
        "matching_extensions_accumulated": total_extensions,
        "zero_term_forbidden_colourings": int(
            np.count_nonzero(counts == 0)
        ),
        "one_term_forbidden_colourings": int(
            np.count_nonzero(counts == 1)
        ),
        "certificate": certificate,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
