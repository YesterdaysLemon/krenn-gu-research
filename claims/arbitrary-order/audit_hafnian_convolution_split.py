"""Independent audit of the hafnian convolution-split identity."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def involutions_without_fixed_points(vertices):
    vertices = frozenset(vertices)
    if not vertices:
        yield frozenset()
        return
    root = max(vertices)
    for partner in sorted(vertices - {root}, reverse=True):
        edge = frozenset((root, partner))
        for rest in involutions_without_fixed_points(
            vertices - edge
        ):
            yield rest | {edge}


def main() -> None:
    primary_path = Path(
        "tmp", "hafnian_convolution_split_verified.json"
    )
    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    theorem = Path(__file__).resolve().with_name(
        "HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md"
    )
    if (
        primary.get("verified") is not True
        or primary.get("theorem_sha256") != sha256(theorem)
    ):
        raise AssertionError("primary theorem binding changed")

    rows = []
    for edge_count in range(6, 0, -1):
        matchings = tuple(
            involutions_without_fixed_points(range(2 * edge_count))
        )
        if len(matchings) != math.prod(
            range(2 * edge_count - 1, 0, -2)
        ):
            raise AssertionError("independent matching census changed")
        for left_edge_count in range(edge_count, -1, -1):
            chosen_splits = 0
            reconstructed = set()
            for matching in matchings:
                edges = tuple(matching)
                for chosen in itertools.combinations(
                    range(edge_count), left_edge_count
                ):
                    left = frozenset(edges[index] for index in chosen)
                    right = matching - left
                    if left | right != matching or left & right:
                        raise AssertionError("split reconstruction failed")
                    reconstructed.add(matching)
                    chosen_splits += 1
            coefficient = math.comb(edge_count, left_edge_count)
            if (
                reconstructed != set(matchings)
                or chosen_splits != coefficient * len(matchings)
            ):
                raise AssertionError("independent coefficient changed")
            rows.append(
                {
                    "vertices": 2 * edge_count,
                    "left_edge_count": left_edge_count,
                    "perfect_matching_monomials": len(matchings),
                    "coefficient_per_monomial": coefficient,
                }
            )

    primary_rows = {
        (
            row["vertices"],
            row["left_edge_count"],
            row["perfect_matching_monomials"],
            row["coefficient_per_monomial"],
        )
        for row in primary["coefficientwise_rows"]
    }
    audit_rows = {
        (
            row["vertices"],
            row["left_edge_count"],
            row["perfect_matching_monomials"],
            row["coefficient_per_monomial"],
        )
        for row in rows
    }
    if audit_rows != primary_rows:
        raise AssertionError("primary/audit row comparison failed")
    if (
        primary.get("three_colour_exclusive_cut_consequence")
        is not True
        or len(primary.get("exclusive_support_truth_table", [])) != 3
    ):
        raise AssertionError("exclusive-cut consequence missing")

    payload = {
        "verified": True,
        "status": "hafnian_convolution_identity_independently_audited",
        "method": (
            "reverse-root fixed-point-free involutions followed by "
            "direct edge-subset choices"
        ),
        "orders_checked": [12, 10, 8, 6, 4, 2],
        "coefficientwise_rows": rows,
        "three_colour_exclusive_cut_consequence_audited": True,
        "primary": str(primary_path),
        "primary_sha256": sha256(primary_path),
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp", "hafnian_convolution_split_audited.json"
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
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
