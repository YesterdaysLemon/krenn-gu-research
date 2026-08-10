"""Quotient certified orbit-8 mandatory-unit supports by residual symmetry."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Sequence

from analyze_fourteen_vertex_c4_c4_c6_transport_rules import (
    full_automorphisms,
    transform_factor,
)


Edge = tuple[int, int]
Factor = tuple[Edge, ...]
PairKey = tuple[Factor, Factor]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def factor(raw: Sequence[Sequence[int]]) -> Factor:
    return tuple(
        sorted(tuple(sorted(map(int, item))) for item in raw)
    )


def encode_factor(value: Factor) -> list[list[int]]:
    return [list(item) for item in value]


def encode_pair(value: PairKey) -> list[list[list[int]]]:
    return [encode_factor(item) for item in value]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first-support", type=int, default=3)
    parser.add_argument("--last-support", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.first_support < 1:
        raise ValueError("first support must be positive")
    if args.last_support < args.first_support:
        raise ValueError("last support precedes first support")

    records: list[dict[str, object]] = []
    pinned: Factor | None = None
    raw_rows: list[tuple[int, Factor, Factor]] = []
    for support in range(args.first_support, args.last_support + 1):
        prefix = f"fourteen_vertex_c4_c4_c6_orbit8_support{support}"
        partial = Path(
            "tmp",
            "fourteen_vertex_c4_c4_c6_orbit8_"
            f"partial_minimal_circuit_lattice_support{support}.json",
        )
        analysis = Path(
            "tmp", f"{prefix}_mandatory_unit_binomial_closure.json"
        )
        verified = Path(
            "tmp", f"{prefix}_mandatory_unit_binomial_closure_verified.json"
        )
        augmentation = Path(
            "tmp",
            "fourteen_vertex_c4_c4_c6_orbit8_"
            f"binomial{support}_augmentation.json",
        )
        augmentation_audit = Path(
            "tmp",
            "fourteen_vertex_c4_c4_c6_orbit8_"
            f"binomial{support}_augmentation_verified.json",
        )
        for path in (
            partial,
            analysis,
            verified,
            augmentation,
            augmentation_audit,
        ):
            if not path.is_file():
                raise FileNotFoundError(path)

        partial_payload = json.loads(partial.read_text(encoding="utf-8"))
        analysis_payload = json.loads(analysis.read_text(encoding="utf-8"))
        verified_payload = json.loads(verified.read_text(encoding="utf-8"))
        augmentation_payload = json.loads(
            augmentation.read_text(encoding="utf-8")
        )
        audit_payload = json.loads(
            augmentation_audit.read_text(encoding="utf-8")
        )
        if verified_payload.get("verified") is not True:
            raise AssertionError(f"support {support} is not verified")
        if audit_payload.get("verified") is not True:
            raise AssertionError(
                f"support {support} augmentation is not verified"
            )
        if analysis_payload.get("support_closed") is not True:
            raise AssertionError(f"support {support} is not closed")
        if (
            sha256(analysis)
            != verified_payload.get("analysis_sha256")
        ):
            raise AssertionError(
                f"support {support} analysis hash changed"
            )
        factors = tuple(
            factor(item) for item in partial_payload["singleton_factors"]
        )
        if len(factors) != 3:
            raise AssertionError("expected three singleton factors")
        if pinned is None:
            pinned = factors[0]
        elif factors[0] != pinned:
            raise AssertionError("pinned first factor changed")
        raw_rows.append((support, factors[1], factors[2]))
        records.append(
            {
                "support": support,
                "partial_analysis_sha256": sha256(partial),
                "analysis_sha256": sha256(analysis),
                "verified_support_sha256": sha256(verified),
                "augmentation_sha256": sha256(augmentation),
                "augmentation_audit_sha256": sha256(
                    augmentation_audit
                ),
                "relation_clauses": verified_payload[
                    "relation_clauses"
                ],
                "selected_initial_relations": verified_payload[
                    "selected_initial_relations"
                ],
                "derived_relations": verified_payload[
                    "derived_relations_checked"
                ],
                "final_lattice_rank": verified_payload[
                    "final_lattice_rank"
                ],
                "target_active_matchings": verified_payload[
                    "target_active_matchings"
                ],
                "target_colouring": analysis_payload["contradiction"][
                    "target_colouring"
                ],
                "sole_surviving_matching": analysis_payload[
                    "contradiction"
                ]["surviving_group"]["members"][0]["matching_id"],
                "output_cnf_sha256": augmentation_payload[
                    "output_cnf_sha256"
                ],
            }
        )

    if pinned is None:
        raise AssertionError("no supports loaded")
    stabilizer = [
        action
        for action in full_automorphisms()
        if transform_factor(pinned, action) == pinned
    ]
    if not stabilizer:
        raise AssertionError("empty pinned-factor stabilizer")

    def canonical_pair(first: Factor, second: Factor) -> PairKey:
        images: list[PairKey] = []
        for action in stabilizer:
            image_first = transform_factor(first, action)
            image_second = transform_factor(second, action)
            images.append((image_first, image_second))
            images.append((image_second, image_first))
        return min(images)

    keys = {
        support: canonical_pair(first, second)
        for support, first, second in raw_rows
    }
    types = sorted(set(keys.values()))
    type_id = {key: index for index, key in enumerate(types)}
    counts = Counter(type_id[key] for key in keys.values())
    for record in records:
        support = int(record["support"])
        record["residual_symmetry_type"] = type_id[keys[support]]

    payload = {
        "status": "certified_mandatory_unit_support_symmetry_quotient",
        "scope": (
            "certified orbit-8 supports with mandatory-unit closure, "
            "modulo the pinned first-factor stabilizer and colour-1/2 swap"
        ),
        "support_range": [
            args.first_support,
            args.last_support,
        ],
        "certified_supports": len(records),
        "pinned_first_factor": encode_factor(pinned),
        "full_factor_automorphisms": len(full_automorphisms()),
        "pinned_factor_stabilizer": len(stabilizer),
        "residual_symmetry_types": len(types),
        "type_multiplicities": {
            str(key): counts[key] for key in sorted(counts)
        },
        "type_representatives": [
            {
                "type": index,
                "remaining_factors": encode_pair(key),
            }
            for index, key in enumerate(types)
        ],
        "records": records,
        "global_conjecture_resolved": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
