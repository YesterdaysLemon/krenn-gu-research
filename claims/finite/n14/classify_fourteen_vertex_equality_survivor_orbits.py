"""Quotient saved order-14 equality survivors by exact symmetries."""

from __future__ import annotations
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])


import argparse
import json
from collections import Counter
from pathlib import Path

from explore_fourteen_vertex_equality_factor_family import (
    Edge,
    contiguous_cycles,
    full_automorphisms,
    transform,
)


Factor = tuple[Edge, ...]
Support = tuple[Factor, Factor, Factor]


def decode_factor(items: list[list[int]]) -> Factor:
    return tuple(
        sorted(tuple(sorted(map(int, item))) for item in items)
    )


def decode_support(item: dict[str, object]) -> Support:
    return tuple(
        decode_factor(item[key])  # type: ignore[arg-type]
        for key in ("first", "second", "third")
    )  # type: ignore[return-value]


def encode_support(support: Support) -> dict[str, list[list[int]]]:
    return {
        key: [list(item) for item in factor]
        for key, factor in zip(
            ("first", "second", "third"), support, strict=True
        )
    }


def transformed_support(
    support: Support, action: dict[int, int]
) -> Support:
    return tuple(
        sorted(transform(factor, action) for factor in support)
    )  # type: ignore[return-value]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_equality_survivor_orbits.json"
        ),
    )
    args = parser.parse_args()
    exploration = json.loads(
        args.exploration.read_text(encoding="utf-8")
    )
    lengths = tuple(map(int, exploration["partition"]))
    actions = full_automorphisms(contiguous_cycles(lengths))
    raw_supports = [
        decode_support(item) for item in exploration["survivors"]
    ]
    canonical_to_representative: dict[Support, Support] = {}
    multiplicities: Counter[Support] = Counter()
    for support in raw_supports:
        canonical = min(
            transformed_support(support, action)
            for action in actions
        )
        canonical_to_representative.setdefault(canonical, support)
        multiplicities[canonical] += 1
    rows = []
    representatives = []
    for orbit_id, canonical in enumerate(
        sorted(canonical_to_representative)
    ):
        representative = canonical_to_representative[canonical]
        full_orbit = {
            transformed_support(representative, action)
            for action in actions
        }
        encoded = encode_support(representative)
        representatives.append(encoded)
        rows.append(
            {
                "orbit_id": orbit_id,
                "saved_manifest_multiplicity": multiplicities[canonical],
                "full_unlabelled_orbit_size": len(full_orbit),
                "representative": encoded,
                "canonical_support": encode_support(canonical),
            }
        )
    if sum(row["saved_manifest_multiplicity"] for row in rows) != len(
        raw_supports
    ):
        raise AssertionError("orbit multiplicities do not cover survivors")
    payload = {
        "status": "complete_saved_survivor_orbit_quotient",
        "exploration": str(args.exploration),
        "partition": list(lengths),
        "full_automorphisms": len(actions),
        "saved_ordered_survivors": len(raw_supports),
        "distinct_saved_unlabelled_supports": len(set(
            tuple(sorted(support)) for support in raw_supports
        )),
        "survivor_orbits": len(rows),
        "survivors": representatives,
        "orbit_rows": rows,
        "exploratory_until_independently_replayed": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                key: value
                for key, value in payload.items()
                if key not in {"survivors", "orbit_rows"}
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
