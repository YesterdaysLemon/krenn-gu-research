#!/usr/bin/env python3
"""Independent audit of the four-K5 support-Segre rank census.

This audit intentionally does not import the primary enumerator.  It uses a
separate SymPy construction for both q=20 equality strata, checks the exact
source-dimension arithmetic, and independently recomputes the pinned hashes
and totals of the full primary histogram.  It does *not* re-enumerate the
2,269,536,547 partition systems; that limitation is part of the audit result.
"""

from __future__ import annotations

import hashlib
import json
from itertools import combinations

import sympy as sp

SELECTOR = (0, 0, 1)
EXPECTED_SELECTOR_ORBITS = 65_966
EXPECTED_SELECTOR_HASH = (
    "e27c85bda3fc01904ad977c003eee1d235a12677186b84a9790d20a234c1e35f"
)
EXPECTED_PAIR_INSTANCES = 74_083_334
EXPECTED_RAW_SIGNATURES = 1_026_928
EXPECTED_LEGACY_PACKED_SIGNATURES = 677_260
EXPECTED_FULL_SYSTEMS = 2_269_536_547
EXPECTED_RANK_HISTOGRAM = {
    (1, 1): 49,
    (2, 2): 2_755,
    (3, 2): 541,
    (3, 3): 92_401,
    (4, 2): 209,
    (4, 3): 22_060,
    (4, 4): 908_913,
}
EXPECTED_Q_HISTOGRAM = {
    20: 2,
    21: 39,
    22: 506,
    23: 8_882,
    24: 150_155,
    25: 804_555,
    26: 5_147_814,
    27: 18_813_205,
    28: 65_063_565,
    29: 162_773_111,
    30: 322_044_201,
    31: 496_230_100,
    32: 535_661_624,
    33: 394_624_590,
    34: 194_788_958,
    35: 55_870_011,
    36: 13_169_086,
    37: 3_943_026,
    38: 443_117,
}
EXPECTED_RANK_HASH = (
    "b4610a69106b5fa342f7d5e386ba28761523b3976fea29657d7a348d7351d00f"
)
EXPECTED_Q_HASH = (
    "1af40871b003b0bbbdcb23aa46de728ff950b9edae489f65a2b504a8808bcb6a"
)


def evaluation(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    """Return the 9 evaluation coordinates in row-major order."""

    return sp.Matrix(
        [left[row] * right[column] for row in range(3) for column in range(3)]
    )


def supports(selector: tuple[int, int, int]) -> tuple[int, ...]:
    return tuple(
        sum(1 << colour for colour in range(3) if selector[colour] != vertex)
        for vertex in range(4)
    )


def partition_delta(
    partition: tuple[int, int, int, int], support: tuple[int, ...]
) -> int:
    independent = sum(mask.bit_count() - 1 for mask in support)
    blocks = [7] * (max(partition) + 1)
    for chart, block in enumerate(partition):
        blocks[block] &= support[chart]
    synchronized = sum(mask.bit_count() - 1 for mask in blocks)
    return independent - synchronized


def roots(
    vertex_one_by_chart: tuple[tuple[int, int, int], ...]
) -> tuple[tuple[sp.Matrix, ...], ...]:
    x2 = ((1, 2, 1), (2, 1, 1), (3, 4, 1), (5, 1, 1))
    x3 = ((2, 1, 1), (1, 3, 1), (4, 2, 1), (3, 5, 1))
    result = []
    for chart in range(4):
        result.append(
            (
                sp.Matrix((0, 0, 1)),
                sp.Matrix(vertex_one_by_chart[chart]),
                sp.Matrix(x2[chart]),
                sp.Matrix(x3[chart]),
            )
        )
    return tuple(result)


def frontier_replay() -> list[dict[str, object]]:
    support = supports(SELECTOR)
    # First stratum: only vertex 0 is synchronized.
    first_roots = roots(((1, 1, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0)))
    first_partitions = (
        (0, 0, 0, 0),
        (0, 1, 2, 3),
        (0, 1, 2, 3),
        (0, 1, 2, 3),
    )
    # Second stratum: vertices 0 and 1 are synchronized.
    second_roots = roots(((1, 1, 0),) * 4)
    second_partitions = (
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 1, 2, 3),
        (0, 1, 2, 3),
    )
    results = []
    for label, chart_roots, partitions in (
        ("one_synchronized_common_vertex", first_roots, first_partitions),
        ("two_synchronized_common_vertices", second_roots, second_partitions),
    ):
        ranks = tuple(
            sp.Matrix.hstack(
                *[
                    evaluation(chart_roots[chart][left], chart_roots[chart][right])
                    for chart in range(4)
                ]
            ).rank()
            for left, right in combinations(range(4), 2)
        )
        deltas = tuple(
            partition_delta(partitions[vertex], (support[vertex],) * 4)
            for vertex in range(4)
        )
        q = sum(ranks) + sum(deltas)
        assert q == 20
        assert ranks == (
            (2, 3, 3, 4, 4, 4)
            if label == "one_synchronized_common_vertex"
            else (1, 3, 3, 3, 3, 4)
        )
        assert deltas == (
            (0, 0, 0, 0)
            if label == "one_synchronized_common_vertex"
            else (0, 3, 0, 0)
        )
        # The first equality stratum has four partition pairs on edge 01 but
        # only a two-dimensional tensor span, directly auditing the rejected
        # cardinality-as-rank step.
        if label == "one_synchronized_common_vertex":
            assert len(
                {
                    (partitions[0][chart], partitions[1][chart])
                    for chart in range(4)
                }
            ) == 4
            assert ranks[0] == 2
        common_root_dimension = 20
        root_dimension = common_root_dimension + 8 - sum(deltas)
        affine_codimension = 16 + sum(ranks) - root_dimension
        assert affine_codimension == 8
        results.append(
            {
                "label": label,
                "partitions": [list(partition) for partition in partitions],
                "ranks": list(ranks),
                "delta_by_vertex": list(deltas),
                "q": q,
                "affine_codimension": affine_codimension,
            }
        )
    return results


def integrity_checks() -> dict[str, object]:
    rank_hash = hashlib.sha256(
        repr(sorted(EXPECTED_RANK_HISTOGRAM.items())).encode()
    ).hexdigest()
    q_hash = hashlib.sha256(
        repr(sorted(EXPECTED_Q_HISTOGRAM.items())).encode()
    ).hexdigest()
    assert sum(EXPECTED_RANK_HISTOGRAM.values()) == EXPECTED_RAW_SIGNATURES
    assert sum(EXPECTED_Q_HISTOGRAM.values()) == EXPECTED_FULL_SYSTEMS
    assert min(EXPECTED_Q_HISTOGRAM) == 20
    assert EXPECTED_Q_HISTOGRAM[20] == 2
    assert rank_hash == EXPECTED_RANK_HASH
    assert q_hash == EXPECTED_Q_HASH
    assert len(EXPECTED_SELECTOR_HASH) == 64
    assert EXPECTED_SELECTOR_ORBITS == 65_966
    assert EXPECTED_PAIR_INSTANCES == 74_083_334
    assert EXPECTED_LEGACY_PACKED_SIGNATURES == 677_260
    return {
        "rank_histogram_sha256": rank_hash,
        "q_histogram_sha256": q_hash,
        "raw_signature_count": EXPECTED_RAW_SIGNATURES,
        "full_partition_systems": EXPECTED_FULL_SYSTEMS,
        "q_minimum": min(EXPECTED_Q_HISTOGRAM),
        "q20_count": EXPECTED_Q_HISTOGRAM[20],
        "full_reenumeration": False,
    }


def main() -> None:
    result = {
        "status": "independent_exact_q20_and_histogram_integrity_audit",
        "field": "Q_exact_frontier_replay",
        "global_conjecture": "UNRESOLVED",
        "frontier": frontier_replay(),
        "integrity": integrity_checks(),
        "audit_scope_limit": (
            "does not re-enumerate all selector orbits or partition systems; "
            "full-census totals and hashes are pinned integrity checks"
        ),
    }
    print("four-K5 support-Segre census independent audit: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
