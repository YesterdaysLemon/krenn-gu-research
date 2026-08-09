"""Aggregate all five n=10 five-regular equality-family audits."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def partitions(
    total: int,
    minimum: int = 3,
) -> list[tuple[int, ...]]:
    output: list[tuple[int, ...]] = []

    def visit(remaining: int, least: int, chosen: tuple[int, ...]) -> None:
        if remaining == 0:
            output.append(chosen)
            return
        for part in range(least, remaining + 1):
            if remaining - part not in {0} and remaining - part < part:
                continue
            visit(remaining - part, part, (*chosen, part))

    visit(total, minimum, ())
    return output


def load_verified(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("verified") is not True:
        raise AssertionError(f"family audit is not verified: {path}")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--c10",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c10_equality_family_verified.json"
        ),
    )
    parser.add_argument(
        "--c4-c6",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_family_verified.json"
        ),
    )
    parser.add_argument(
        "--c5-c5",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c5_c5_equality_family_verified.json"
        ),
    )
    parser.add_argument(
        "--c3-c7",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c3_c7_equality_family_verified.json"
        ),
    )
    parser.add_argument(
        "--c3-c3-c4",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c3_c3_c4_equality_family_verified.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/ten_vertex_five_regular_equality_boundary_verified.json"
        ),
    )
    parser.add_argument(
        "--entry-boundary",
        type=Path,
        default=Path("tmp/eight_vertex_entry84_boundary_verified.json"),
    )
    args = parser.parse_args()
    structural_audit = load_verified(args.entry_boundary)
    if (
        structural_audit.get("general_three_colour_bound")
        != "entries <= 9m - 12n"
    ):
        raise AssertionError("general three-colour entry bound changed")
    if structural_audit.get(
        "local_assignments_with_all_required_backups", {}
    ).get("2") != [[0, 1, 2]]:
        raise AssertionError(
            "diagonal-singleton backup audit changed at full degree two"
        )

    entry_rows: list[dict[str, int]] = []
    for reciprocal in range(16):
        one_way = 30 - 2 * reciprocal
        unused = 25 - reciprocal - one_way
        if one_way < 0 or unused < 0:
            continue
        entry_rows.append(
            {
                "reciprocal_selected_edges": reciprocal,
                "one_way_selected_edges": one_way,
                "unused_edges": unused,
                "entry_upper_bound": (
                    reciprocal + 3 * one_way + 9 * unused
                ),
            }
        )
    equality_rows = [
        row for row in entry_rows if row["entry_upper_bound"] == 105
    ]
    if max(row["entry_upper_bound"] for row in entry_rows) != 105:
        raise AssertionError("n=10 entry maximum changed")
    if equality_rows != [
        {
            "reciprocal_selected_edges": 15,
            "one_way_selected_edges": 0,
            "unused_edges": 10,
            "entry_upper_bound": 105,
        }
    ]:
        raise AssertionError("n=10 equality entry structure changed")

    paths = [
        args.c10,
        args.c4_c6,
        args.c5_c5,
        args.c3_c7,
        args.c3_c3_c4,
    ]
    audits = [load_verified(path) for path in paths]
    expected_types = {
        (10,),
        (4, 6),
        (5, 5),
        (3, 7),
        (3, 3, 4),
    }
    actual_types = {
        tuple(map(int, audit.get("full_cycle_type", [])))
        for audit in audits
        if audit.get("full_cycle_type")
    }
    # The older C4+C6 audit predates the explicit cycle-type field.
    if (4, 6) not in actual_types and "C4+C6" in str(audits[1]["scope"]):
        actual_types.add((4, 6))
    if actual_types != expected_types:
        raise AssertionError(
            f"full-factor coverage changed: {actual_types}"
        )
    if set(partitions(10)) != expected_types:
        raise AssertionError("ten-vertex 2-factor partitions changed")
    expected_orbits = {
        (10,): 23_204,
        (4, 6): 4_903,
        (5, 5): 2_536,
        (3, 7): 5_558,
        (3, 3, 4): 906,
    }
    expected_labelled = {
        (10,): 491_794_208_640,
        (4, 6): 101_287_065_600,
        (5, 5): 50_152_556_160,
        (3, 7): 118_737_964_800,
        (3, 3, 4): 17_325_705_600,
    }
    rows: list[dict[str, object]] = []
    for cycle_type, path, audit in zip(
        ((10,), (4, 6), (5, 5), (3, 7), (3, 3, 4)),
        paths,
        audits,
        strict=True,
    ):
        if int(audit["support_orbits"]) != expected_orbits[cycle_type]:
            raise AssertionError(f"orbit count changed for {cycle_type}")
        if (
            int(audit["labelled_coloured_supports"])
            != expected_labelled[cycle_type]
        ):
            raise AssertionError(
                f"labelled support count changed for {cycle_type}"
            )
        rows.append(
            {
                "full_cycle_type": list(cycle_type),
                "audit": str(path),
                "audit_sha256": sha256(path),
                "support_orbits": int(audit["support_orbits"]),
                "labelled_coloured_supports": int(
                    audit["labelled_coloured_supports"]
                ),
            }
        )
    payload = {
        "verified": True,
        "scope": (
            "all n=10,d=3 105-entry five-regular equality supports "
            "with ten full blocks forming a spanning 2-factor and "
            "fifteen diagonal singleton blocks forming three perfect "
            "matchings"
        ),
        "claim_scope": (
            "excludes this complete five-regular equality boundary only; "
            "does not exclude supports below 105 entries, non-5-regular "
            "exact-25 supports, or prove the global conjecture"
        ),
        "full_factor_types": [
            list(cycle_type) for cycle_type in sorted(expected_types)
        ],
        "entry_upper_bound": 105,
        "equality_rows": equality_rows,
        "structural_audit": str(args.entry_boundary),
        "structural_audit_sha256": sha256(args.entry_boundary),
        "support_orbits": sum(
            int(row["support_orbits"]) for row in rows
        ),
        "labelled_coloured_supports": sum(
            int(row["labelled_coloured_supports"]) for row in rows
        ),
        "families": rows,
    }
    if payload["support_orbits"] != 37_107:
        raise AssertionError("aggregate orbit count changed")
    if payload["labelled_coloured_supports"] != 779_297_500_800:
        raise AssertionError("aggregate labelled support count changed")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
