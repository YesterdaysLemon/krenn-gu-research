"""Independently audit colour transport of certified factor-orbit exclusions."""

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

REPO_ROOT, HERE = _bootstrap_repository(__file__)


import argparse
import hashlib
import itertools
import json
import tempfile
import time
from pathlib import Path
from typing import Iterable, Sequence

from pysat.formula import CNF


N = 14
Edge = tuple[int, int]
Factor = tuple[Edge, ...]
CYCLES = (
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (8, 9, 10, 11, 12, 13),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def edge(first: int, second: int) -> Edge:
    return (
        (first, second) if first < second else (second, first)
    )


def parse_factor(raw: Sequence[Sequence[int] | str]) -> Factor:
    output = []
    for item in raw:
        if isinstance(item, str):
            first, second = map(int, item.split())
        else:
            first, second = map(int, item)
        output.append(edge(first, second))
    return tuple(sorted(output))


def cycle_edges(cycle: Sequence[int]) -> set[Edge]:
    return {
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    }


def full_automorphisms() -> list[tuple[int, ...]]:
    component_maps = ((0, 1, 2), (1, 0, 2))
    local_choices = itertools.product(
        *[
            [
                (direction, rotation)
                for direction in (1, -1)
                for rotation in range(len(cycle))
            ]
            for cycle in CYCLES
        ]
    )
    choices = list(local_choices)
    output = []
    for component_map in component_maps:
        for local in choices:
            action = [0] * N
            for source_id, source in enumerate(CYCLES):
                target = CYCLES[component_map[source_id]]
                direction, rotation = local[source_id]
                for position, vertex in enumerate(source):
                    action[vertex] = target[
                        (rotation + direction * position) % len(target)
                    ]
            output.append(tuple(action))
    return output


def transform_factor(
    factor: Factor, action: Sequence[int]
) -> Factor:
    return tuple(
        sorted(
            edge(action[first], action[second])
            for first, second in factor
        )
    )


def perfect_matchings(allowed: Iterable[Edge]) -> set[Factor]:
    adjacency = [0] * N
    for first, second in allowed:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first
    output = set()

    def visit(remaining: int, chosen: Factor) -> None:
        if not remaining:
            output.add(tuple(sorted(chosen)))
            return
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        candidates = adjacency[first] & remaining
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            visit(
                remaining ^ first_bit ^ second_bit,
                (*chosen, edge(first, second)),
            )

    visit((1 << N) - 1, ())
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("augmentation", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    augmentation = json.loads(
        args.augmentation.read_text(encoding="utf-8")
    )
    if (
        augmentation.get("status")
        != "colour_symmetric_factor_orbit_exclusions_augmented"
    ):
        raise AssertionError("unexpected augmentation status")

    frontier_path = Path(augmentation["frontier_audit"])
    orbit8_path = Path(augmentation["orbit8_audit"])
    census_path = Path(augmentation["factor_census"])
    base_path = Path(augmentation["base_cnf"])
    output_path = Path(augmentation["output_cnf"])
    for path, field in (
        (frontier_path, "frontier_audit_sha256"),
        (orbit8_path, "orbit8_audit_sha256"),
        (census_path, "factor_census_sha256"),
        (base_path, "base_cnf_sha256"),
        (output_path, "output_cnf_sha256"),
    ):
        if sha256(path) != augmentation[field]:
            raise AssertionError(f"{field} binding changed")

    frontier = json.loads(frontier_path.read_text(encoding="utf-8"))
    orbit8 = json.loads(orbit8_path.read_text(encoding="utf-8"))
    census = json.loads(census_path.read_text(encoding="utf-8"))
    if (
        frontier.get("verified") is not True
        or frontier.get("status")
        != "fourteen_vertex_minimal_circuit_frontiers_verified"
        or orbit8.get("verified") is not True
        or orbit8.get("status")
        != "C4+C4+C6_first_factor_orbit_8_excluded"
        or Path(orbit8["global_cnf"]) != base_path
        or orbit8["global_cnf_sha256"] != sha256(base_path)
    ):
        raise AssertionError("theorem-level predecessor gate changed")

    frontier_remaining = sorted(
        map(int, frontier["C4+C4+C6"]["remaining_orbits"])
    )
    if 8 not in frontier_remaining:
        raise AssertionError("predecessor frontier no longer contains 8")
    remaining = [item for item in frontier_remaining if item != 8]
    excluded = [item for item in range(93) if item not in remaining]
    if (
        excluded != list(map(int, augmentation["excluded_factor_orbits"]))
        or remaining
        != list(map(int, augmentation["remaining_factor_orbits"]))
        or len(excluded) != 66
        or len(remaining) != 27
    ):
        raise AssertionError("certified orbit partition changed")

    full_edges = set().union(
        *(cycle_edges(cycle) for cycle in CYCLES)
    )
    eligible = tuple(
        sorted(
            set(itertools.combinations(range(N), 2)) - full_edges
        )
    )
    edge_index = {item: index for index, item in enumerate(eligible)}
    all_factors = perfect_matchings(eligible)
    if (
        len(eligible) != 77
        or len(all_factors)
        != int(census["eligible_singleton_factors"])
        or len(census["factor_orbits"]) != 93
    ):
        raise AssertionError("factor universe changed")

    actions = full_automorphisms()
    if (
        len(actions) != int(census["full_automorphisms"])
        or any(tuple(sorted(action)) != tuple(range(N)) for action in actions)
        or any(
            {
                edge(action[first], action[second])
                for first, second in full_edges
            }
            != full_edges
            for action in actions
        )
    ):
        raise AssertionError("full-factor automorphism audit failed")

    independently_partitioned = set()
    excluded_factors = set()
    for orbit, row in enumerate(census["factor_orbits"]):
        representative = parse_factor(row["representative"])
        images = {
            transform_factor(representative, action)
            for action in actions
        }
        if (
            representative != min(images)
            or len(images) != int(row["orbit_size"])
            or independently_partitioned & images
        ):
            raise AssertionError(f"factor orbit {orbit} changed")
        independently_partitioned.update(images)
        if orbit in excluded:
            excluded_factors.update(images)
    if independently_partitioned != all_factors:
        raise AssertionError("factor orbits do not partition the universe")
    if (
        len(excluded_factors) != int(augmentation["excluded_factors"])
        or len(all_factors - excluded_factors)
        != int(augmentation["remaining_factors"])
    ):
        raise AssertionError("factor frontier counts changed")

    clauses = sorted(
        {
            tuple(
                sorted(
                    -(
                        colour * len(eligible)
                        + edge_index[item]
                        + 1
                    )
                    for item in factor
                )
            )
            for colour in range(3)
            for factor in excluded_factors
        }
    )
    if (
        len(clauses)
        != int(augmentation["candidate_factor_no_goods"])
        or any(len(clause) != 7 for clause in clauses)
    ):
        raise AssertionError("factor no-good reconstruction changed")

    base = CNF(from_file=str(base_path))
    existing = {tuple(map(int, clause)) for clause in base.clauses}
    new_clauses = [
        clause for clause in clauses if clause not in existing
    ]
    if (
        base.nv != int(augmentation["base_variables"])
        or len(base.clauses) != int(augmentation["base_clauses"])
        or len(new_clauses) != int(augmentation["new_factor_no_goods"])
    ):
        raise AssertionError("base or extension count changed")
    reconstructed = CNF(from_clauses=base.clauses)
    reconstructed.extend(new_clauses)
    with tempfile.TemporaryDirectory(
        prefix="colour-symmetric-orbit-audit-"
    ) as raw_directory:
        rebuilt = Path(raw_directory) / "rebuilt.cnf"
        reconstructed.to_file(str(rebuilt))
        if sha256(rebuilt) != sha256(output_path):
            raise AssertionError("augmented DIMACS bytes changed")
    if (
        reconstructed.nv != int(augmentation["output_variables"])
        or len(reconstructed.clauses)
        != int(augmentation["output_clauses"])
    ):
        raise AssertionError("output DIMACS count changed")

    payload = {
        "verified": True,
        "status": "colour_symmetric_factor_orbit_exclusions_verified",
        "scope": (
            "theorem-audit hash gates, fresh 44,196-factor orbit "
            "partition, three colour roles, exact width-seven clauses, "
            "and byte-identical DIMACS reconstruction"
        ),
        "augmentation": str(args.augmentation),
        "augmentation_sha256": sha256(args.augmentation),
        "excluded_factor_orbits": len(excluded),
        "remaining_factor_orbits": len(remaining),
        "excluded_factors": len(excluded_factors),
        "remaining_factors": len(all_factors - excluded_factors),
        "candidate_factor_no_goods": len(clauses),
        "new_factor_no_goods": len(new_clauses),
        "output_cnf": str(output_path),
        "output_cnf_sha256": sha256(output_path),
        "output_variables": reconstructed.nv,
        "output_clauses": len(reconstructed.clauses),
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
