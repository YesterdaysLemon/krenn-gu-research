"""Replay the three-amplitude contradiction for the explicit n=10 support."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Sequence

from verify_ten_vertex_equality_factor_lattice import (
    canonical,
    monomial_vector,
    reconstruct,
)


BASE_EQUATION = 2359
BASE_ACTIVITY = (8, 11, 49, 50)
FIRST_RELATION_ID = 25
FIRST_TARGET_EQUATION = 205
FIRST_TARGET_ACTIVITY = (3, 8, 11, 38, 41, 49, 50)
FIRST_TARGET_PAIRS = ((8, 11), (38, 41), (49, 50))
FIRST_SURVIVOR = 3
SECOND_RELATION_ID = 5
SECOND_TARGET_EQUATION = 2188
SECOND_TARGET_ACTIVITY = (2, 8, 11, 49, 50)
SECOND_TARGET_PAIRS = ((8, 49), (11, 50))
SECOND_SURVIVOR = 2


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def difference(
    first: Sequence[int], second: Sequence[int]
) -> tuple[int, ...]:
    return tuple(
        int(left - right)
        for left, right in zip(first, second, strict=True)
    )


def vector(data: dict[str, object], equation: int, matching: int) -> tuple[int, ...]:
    return monomial_vector(
        data["matchings"][matching],
        data["colourings"][equation],
        data["singleton"],
        data["positions"],
    )


def verify_pair_partition(
    data: dict[str, object],
    equation: int,
    expected_activity: Sequence[int],
    relation_id: int,
    pairs: Sequence[tuple[int, int]],
    survivor: int,
) -> dict[str, object]:
    activity = tuple(map(int, data["activities"][equation]))
    if activity != tuple(expected_activity):
        raise AssertionError("target amplitude activity changed")
    if len(set(data["colourings"][equation])) == 1:
        raise AssertionError("target amplitude is not forbidden")
    partition = {survivor}
    relation = data["relations"][relation_id]
    checked_pairs: list[dict[str, object]] = []
    for first, second in pairs:
        if first in partition or second in partition:
            raise AssertionError("pair partition repeats a monomial")
        partition.update((first, second))
        raw = difference(
            vector(data, equation, first),
            vector(data, equation, second),
        )
        if canonical(raw) != relation:
            raise AssertionError("target pair has the wrong Laurent ratio")
        checked_pairs.append(
            {
                "matching_indices": [first, second],
                "canonical_difference_relation_id": relation_id,
            }
        )
    if partition != set(activity):
        raise AssertionError("pairs plus survivor do not partition amplitude")
    # Every selected entry is constrained nonzero on this fixed support, so
    # the surviving perfect-matching monomial is nonzero.
    return {
        "equation_index": equation,
        "colouring": list(map(int, data["colourings"][equation])),
        "activity": list(activity),
        "relation_id": relation_id,
        "cancelling_pairs": checked_pairs,
        "surviving_matching_index": survivor,
        "surviving_matching_edges": [
            list(item) for item in data["matchings"][survivor]
        ],
        "contradiction": (
            "if the relation has value -1, every pair cancels and the "
            "single nonzero monomial survives in a forbidden amplitude"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--factor-manifest",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_factor_lattice_"
            "final_verified.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_three_amplitude_verified.json"
        ),
    )
    args = parser.parse_args()
    factor_manifest = json.loads(
        args.factor_manifest.read_text(encoding="utf-8")
    )
    if factor_manifest.get("verified") is not True:
        raise AssertionError("factor proof chain is not verified")
    data = reconstruct()

    if tuple(map(int, data["activities"][BASE_EQUATION])) != BASE_ACTIVITY:
        raise AssertionError("base amplitude activity changed")
    base_colouring = data["colourings"][BASE_EQUATION]
    if len(set(base_colouring)) == 1:
        raise AssertionError("base amplitude is not forbidden")
    base_vectors = {
        matching: vector(data, BASE_EQUATION, matching)
        for matching in BASE_ACTIVITY
    }
    if tuple(
        left + right
        for left, right in zip(
            base_vectors[8], base_vectors[50], strict=True
        )
    ) != tuple(
        left + right
        for left, right in zip(
            base_vectors[11], base_vectors[49], strict=True
        )
    ):
        raise AssertionError("base exponents are not a parallelogram")
    first_direction = canonical(
        difference(base_vectors[8], base_vectors[11])
    )
    second_direction = canonical(
        difference(base_vectors[8], base_vectors[49])
    )
    if first_direction != data["relations"][FIRST_RELATION_ID]:
        raise AssertionError("base C4 direction changed")
    if second_direction != data["relations"][SECOND_RELATION_ID]:
        raise AssertionError("base C6 direction changed")

    first = verify_pair_partition(
        data,
        FIRST_TARGET_EQUATION,
        FIRST_TARGET_ACTIVITY,
        FIRST_RELATION_ID,
        FIRST_TARGET_PAIRS,
        FIRST_SURVIVOR,
    )
    second = verify_pair_partition(
        data,
        SECOND_TARGET_EQUATION,
        SECOND_TARGET_ACTIVITY,
        SECOND_RELATION_ID,
        SECOND_TARGET_PAIRS,
        SECOND_SURVIVOR,
    )
    sparse_relations = []
    for relation_id in (FIRST_RELATION_ID, SECOND_RELATION_ID):
        sparse_relations.append(
            {
                "relation_id": relation_id,
                "terms": [
                    {
                        "entry": [
                            list(data["entries"][coordinate][0]),
                            int(data["entries"][coordinate][1]),
                            int(data["entries"][coordinate][2]),
                        ],
                        "exponent": int(value),
                    }
                    for coordinate, value in enumerate(
                        data["relations"][relation_id]
                    )
                    if value
                ],
            }
        )
    payload = {
        "verified": True,
        "scope": (
            "direct three-amplitude contradiction for the explicit "
            "n=10 C4+C6 equality support"
        ),
        "claim_scope": (
            "this fixed 105-entry support only; not all n=10 supports "
            "and not the global conjecture"
        ),
        "factor_manifest": str(args.factor_manifest),
        "factor_manifest_sha256": sha256(args.factor_manifest),
        "base_factor_amplitude": {
            "equation_index": BASE_EQUATION,
            "colouring": list(map(int, base_colouring)),
            "activity": list(BASE_ACTIVITY),
            "parallelogram_identity": "v8 + v50 = v11 + v49",
            "first_relation_id": FIRST_RELATION_ID,
            "second_relation_id": SECOND_RELATION_ID,
            "consequence": (
                "the forbidden four-term amplitude factors, so relation "
                "25 or relation 5 must have Laurent value -1"
            ),
        },
        "sparse_relations": sparse_relations,
        "first_relation_contradiction": first,
        "second_relation_contradiction": second,
        "conclusion": (
            "the base amplitude forces one of two signed relations and "
            "the other two amplitudes rule out each alternative"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
