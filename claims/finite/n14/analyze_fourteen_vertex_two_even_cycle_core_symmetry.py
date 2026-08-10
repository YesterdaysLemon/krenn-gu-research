"""Quotient a decoded two-even-cycle extension core by target symmetry."""

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

from analyze_fourteen_vertex_two_even_cycle_rule_sat import parse_factor
from explore_fourteen_vertex_equality_factor_family import (
    contiguous_cycles,
    full_automorphisms,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decoded-core", type=Path, required=True)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--orbit", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    decoded = json.loads(args.decoded_core.read_text(encoding="utf-8"))
    census = json.loads(args.census.read_text(encoding="utf-8"))
    partition = tuple(map(int, census["partition"]))
    cycles = contiguous_cycles(partition)
    target = parse_factor(
        census["factor_orbits"][args.orbit]["representative"]
    )
    stabilizer = [
        action
        for action in full_automorphisms(cycles)
        if tuple(
            sorted(
                tuple(sorted((action[u], action[v]))) for u, v in target
            )
        )
        == target
    ]

    def image_key(
        forbidden: list[dict[str, object]],
        action: dict[int, int],
        swap: bool,
    ) -> tuple[tuple[int, int, int, bool], ...]:
        result = []
        for item in forbidden:
            role = int(item["role"])
            if swap and role in (1, 2):
                role = 3 - role
            u, v = map(int, item["edge"])
            a, b = sorted((action[u], action[v]))
            result.append((role, a, b, bool(item["value"])))
        return tuple(sorted(result))

    rows: list[dict[str, object]] = []
    counts: Counter[tuple[tuple[int, int, int, bool], ...]] = Counter()
    for clause in decoded["decoded_clauses"]:
        forbidden = clause["forbidden_assignment"]
        canonical = min(
            image_key(forbidden, action, swap)
            for action in stabilizer
            for swap in (False, True)
        )
        counts[canonical] += 1
        rows.append(
            {
                "source_extension_clause_index": clause[
                    "source_extension_clause_index"
                ],
                "canonical_type": [list(item) for item in canonical],
            }
        )

    types = [
        {
            "multiplicity_in_irredundant_core": count,
            "reduced_width": len(key),
            "forbidden_assignment": [
                {
                    "role": role,
                    "edge": [u, v],
                    "value": value,
                }
                for role, u, v, value in key
            ],
        }
        for key, count in sorted(
            counts.items(), key=lambda item: (len(item[0]), item[0])
        )
    ]
    payload = {
        "status": "two_even_cycle_core_symmetry_quotient",
        "decoded_core": str(args.decoded_core),
        "census": str(args.census),
        "target_orbit": args.orbit,
        "target_representative": [list(edge) for edge in target],
        "target_stabilizer_size": len(stabilizer),
        "remaining_role_swap": True,
        "core_clauses": len(rows),
        "canonical_clause_types": len(types),
        "type_widths": dict(
            sorted(Counter(row["reduced_width"] for row in types).items())
        ),
        "types": types,
        "rows": rows,
        "exploratory_only": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
