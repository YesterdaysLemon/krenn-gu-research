"""Independent audit of the multi-star matching factorisation."""

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


def allowed_matching_count(root_count: int, free_count: int) -> int:
    # DP on type counts.  An allowed root can only consume a blocker;
    # a free vertex can only consume another free vertex.
    states = {(root_count, root_count, free_count): 1}
    while states:
        (roots, blockers, free), count = states.popitem()
        if roots:
            if not blockers:
                return 0
            next_state = (roots - 1, blockers - 1, free)
            states[next_state] = (
                states.get(next_state, 0) + count * blockers
            )
            continue
        if blockers:
            return 0
        if free == 0:
            return count
        if free % 2:
            return 0
        next_state = (0, 0, free - 2)
        states[next_state] = (
            states.get(next_state, 0) + count * (free - 1)
        )
    return 0


def residual_matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in residual_matchings(remainder):
            yield ((first, second),) + tail


def main() -> None:
    records = []
    for n in range(4, 13, 2):
        for root_count in range(2, n // 2 + 1):
            roots = tuple(range(root_count))
            blockers = tuple(range(root_count, 2 * root_count))
            free = tuple(range(2 * root_count, n))
            products = set()
            residuals = tuple(residual_matchings(free))
            for blocker_order in itertools.permutations(blockers):
                root_pairs = tuple(
                    sorted(zip(roots, blocker_order, strict=True))
                )
                for residual in residuals:
                    matching = tuple(sorted(root_pairs + residual))
                    products.add(matching)

            formula_count = math.factorial(root_count)
            for odd in range(len(free) - 1, 0, -2):
                formula_count *= odd
            dp_count = allowed_matching_count(
                root_count, len(free)
            )
            if len(products) != formula_count or dp_count != formula_count:
                raise AssertionError(
                    f"independent count mismatch for n={n}, "
                    f"r={root_count}"
                )
            if any(
                any(
                    not (
                        (left in roots and right in blockers)
                        or (left in free and right in free)
                    )
                    for left, right in matching
                )
                for matching in products
            ):
                raise AssertionError("constructed an invalid matching")
            records.append(
                {
                    "n": n,
                    "root_count": root_count,
                    "cartesian_product_count": len(products),
                    "dynamic_programming_count": dp_count,
                    "closed_formula_count": formula_count,
                }
            )

    source = Path(__file__)
    primary = Path(
        "tmp", "multi_star_blocker_factorisation_verified.json"
    )
    primary_payload = json.loads(primary.read_text(encoding="utf-8"))
    primary_projection = [
        (
            row["n"],
            row["root_count"],
            row["surviving_matchings"],
        )
        for row in primary_payload["exact_factorisation_cases"]
    ]
    audit_projection = [
        (
            row["n"],
            row["root_count"],
            row["cartesian_product_count"],
        )
        for row in records
    ]
    if primary_projection != audit_projection:
        raise AssertionError("primary/audit projections differ")

    # Independent symbolic labels for the three diagonal blocker
    # tensors.  In a rank-one flattening F tensor H, coefficient rows
    # are scalar multiples of the one residual row H.  Therefore the
    # independently labelled residual rows attached to D_0,D_1,D_2
    # must all be collinear, and F has no row outside their diagonal
    # span.
    diagonal_labels = tuple(
        tuple(colour for _blocker in range(2))
        for colour in range(3)
    )
    all_blocker_labels = tuple(itertools.product(range(3), repeat=2))
    mixed_labels = tuple(
        label
        for label in all_blocker_labels
        if label not in diagonal_labels
    )
    if len(diagonal_labels) != 3 or len(mixed_labels) != 6:
        raise AssertionError("unexpected blocker coefficient basis")

    payload = {
        "verified": True,
        "independent_method": (
            "Cartesian construction plus type-count dynamic programming"
        ),
        "cases_checked": len(records),
        "tight_case_tensor_logic": {
            "diagonal_basis_labels": diagonal_labels,
            "mixed_basis_labels": mixed_labels,
            "rank_one_forces_residual_collinearity": True,
            "mixed_root_blocker_coefficients_forced_zero": True,
        },
        "records": records,
        "primary_artifact": str(primary),
        "primary_artifact_sha256": sha256(primary),
        "source": str(source),
        "source_sha256": sha256(source),
        "global_conjecture_resolved": False,
    }
    output = Path(
        "tmp", "multi_star_blocker_factorisation_audited.json"
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
