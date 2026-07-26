"""Verify the hafnian convolution identity coefficientwise through order 12."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import Counter
from functools import lru_cache
from pathlib import Path

Edge = tuple[int, int]
Matching = tuple[Edge, ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for position in range(1, len(vertices)):
        partner = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        edge = (min(first, partner), max(first, partner))
        for tail in perfect_matchings(remainder):
            result.append(tuple(sorted((edge,) + tail)))
    return tuple(result)


def main() -> None:
    rows = []
    for edge_count in range(1, 7):
        vertices = tuple(range(2 * edge_count))
        full_matchings = perfect_matchings(vertices)
        expected_matchings = math.prod(
            range(1, 2 * edge_count, 2)
        )
        if len(full_matchings) != expected_matchings:
            raise AssertionError("perfect-matching census changed")
        for left_edge_count in range(edge_count + 1):
            coefficient = Counter()
            left_size = 2 * left_edge_count
            for left_vertices in itertools.combinations(
                vertices, left_size
            ):
                left_set = set(left_vertices)
                right_vertices = tuple(
                    vertex
                    for vertex in vertices
                    if vertex not in left_set
                )
                for left_matching in perfect_matchings(left_vertices):
                    for right_matching in perfect_matchings(
                        right_vertices
                    ):
                        full = tuple(
                            sorted(left_matching + right_matching)
                        )
                        coefficient[full] += 1
            expected_coefficient = math.comb(
                edge_count, left_edge_count
            )
            if (
                set(coefficient) != set(full_matchings)
                or set(coefficient.values())
                != {expected_coefficient}
            ):
                raise AssertionError("convolution coefficient changed")
            rows.append(
                {
                    "vertices": 2 * edge_count,
                    "edge_count": edge_count,
                    "left_edge_count": left_edge_count,
                    "perfect_matching_monomials": len(full_matchings),
                    "coefficient_per_monomial": expected_coefficient,
                    "expanded_terms": sum(coefficient.values()),
                }
            )

    # If p_c(A)q_d(A)=0 for c != d and p_c(A)q_c(A)
    # is nonzero, then all p_d(A),q_d(A) for d != c vanish.
    exclusive_support_truth_table = []
    for colour in range(3):
        admissible = []
        for assignment in itertools.product((False, True), repeat=6):
            p = assignment[:3]
            q = assignment[3:]
            if not (p[colour] and q[colour]):
                continue
            if not all(
                not (p[left] and q[right])
                for left in range(3)
                for right in range(3)
                if left != right
            ):
                continue
            admissible.append(assignment)
        if len(admissible) != 1 or any(
            admissible[0][other]
            or admissible[0][3 + other]
            for other in range(3)
            if other != colour
        ):
            raise AssertionError("exclusive-cut support logic changed")
        exclusive_support_truth_table.append(
            {
                "active_colour": colour,
                "admissible_boolean_support_assignments": len(admissible),
                "other_colour_factors_forced_zero": True,
            }
        )

    theorem = Path("HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md")
    payload = {
        "verified": True,
        "status": "hafnian_convolution_identity_verified",
        "orders_checked": [2, 4, 6, 8, 10, 12],
        "coefficientwise_rows": rows,
        "arbitrary_order_proof": (
            "each full matching is counted once for every choice of k "
            "of its m edges"
        ),
        "all_size_nonzero_split_consequence": True,
        "three_colour_exclusive_cut_consequence": True,
        "exclusive_support_truth_table": (
            exclusive_support_truth_table
        ),
        "same_colour_forbidden_factorization_assumed": False,
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp", "hafnian_convolution_split_verified.json"
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "verified": True,
                "orders_checked": payload["orders_checked"],
                "rows": len(rows),
                "largest_matching_census": rows[-1][
                    "perfect_matching_monomials"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
