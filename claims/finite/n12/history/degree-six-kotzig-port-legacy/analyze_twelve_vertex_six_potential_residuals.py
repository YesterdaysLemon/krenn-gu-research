"""Analyze every order-twelve all-six-potential residual.

The compiled exhaustive pass leaves a small residual set of reciprocal
port architectures for which none of the six displayed potential rays
has a unique minimum guaranteed matching.  This program independently
reconstructs those residual architectures from the TSV stream, verifies
their hashes and six-ray status, restores every optional diagonal unit
allowed by the balanced bridge table, and searches the resulting maximal
support for a mixed colouring with exactly one perfect matching made only
from forced units.

Such a maximal-support singleton is a contradiction for every actual
optional-unit subset: the forced monomial is always present, while
removing optional units cannot create a second monomial.
"""

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
from krenn_gu.bootstrap import expose_claim_package  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)
expose_claim_package(REPO_ROOT, "claims/finite/n10/degree-six-kotzig-port")


import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time

from analyze_ten_vertex_degree_six_kotzig_port_survivors import (
    EntryEdge,
    allowed_unit,
    enumerate_coloured_matchings,
)
from analyze_ten_vertex_permuted_potential_survivors import (
    permuted_potential,
)

NormalType = tuple[int, int, int]
Port = tuple[int, int, int, int]
MASK64 = (1 << 64) - 1
FNV_OFFSET = 1_469_598_103_934_665_603
FNV_PRIME = 1_099_511_628_211


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fnv_mix(value: int, item: int) -> int:
    for byte in range(8):
        value ^= (item >> (8 * byte)) & 0xFF
        value = (value * FNV_PRIME) & MASK64
    return value


def architecture_hash(cell_id: int, ports: tuple[Port, ...]) -> int:
    value = fnv_mix(FNV_OFFSET, cell_id)
    for port in sorted(ports):
        for item in port:
            value = fnv_mix(value, item)
    return value


def mixed(row: tuple[int, ...]) -> bool:
    return len(set(row)) > 1


def signature(
    colouring: tuple[int, ...],
    potentials: tuple[tuple[tuple[int, ...], ...], ...],
) -> tuple[int, ...]:
    return tuple(
        sum(
            potentials[vertex][colour][ray]
            for vertex, colour in enumerate(colouring)
        )
        for ray in range(6)
    )


def parse_residuals(path: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for line_number, raw in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        fields = tuple(map(int, raw.split()))
        if len(fields) != 4 + 18 * 4:
            raise AssertionError(
                f"residual line {line_number} has {len(fields)} fields"
            )
        cell_id, graph_index, cell_index, recorded_hash = fields[:4]
        ports = tuple(
            tuple(fields[offset : offset + 4])
            for offset in range(4, len(fields), 4)
        )
        if architecture_hash(cell_id, ports) != recorded_hash:
            raise AssertionError(
                f"residual line {line_number} architecture hash changed"
            )
        records.append(
            {
                "line_number": line_number,
                "cell_id": cell_id,
                "graph_index": graph_index,
                "cell_index": cell_index,
                "architecture_hash": recorded_hash,
                "ports": ports,
            }
        )
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cells",
        type=Path,
        default=Path(
            "tmp", "twelve_vertex_port_cell_orbits_counted.json"
        ),
    )
    parser.add_argument(
        "--exhaustion",
        type=Path,
        default=Path(
            "tmp", "twelve_vertex_six_potential_orbits_exhausted.json"
        ),
    )
    parser.add_argument(
        "--residuals",
        type=Path,
        default=Path(
            "tmp", "twelve_vertex_six_potential_orbits_residuals.tsv"
        ),
    )
    parser.add_argument(
        "--compiled-source",
        type=Path,
        default=REPO_ROOT / "claims/finite/n12/exhaust_twelve_vertex_six_potential_orbits.cpp",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp",
            "twelve_vertex_six_potential_residuals_analyzed.json",
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    cells_payload = json.loads(args.cells.read_text(encoding="utf-8"))
    exhaustion = json.loads(
        args.exhaustion.read_text(encoding="utf-8")
    )
    cells = tuple(cells_payload["cell_representatives"])
    residuals = parse_residuals(args.residuals)
    if (
        cells_payload.get("verified") is not True
        or cells_payload.get("cell_orbits") != 154
        or exhaustion.get("verified") is not True
        or exhaustion.get("cell_orbits") != len(cells)
        or exhaustion.get("representative_port_realizations")
        != 15_478_610
        or exhaustion.get("all_six_potential_survivors")
        != len(residuals)
        or len(residuals) != 395
    ):
        raise AssertionError("order-twelve input binding changed")

    residual_count_by_cell = Counter(
        int(record["cell_id"]) for record in residuals
    )
    for result in exhaustion["cell_results"]:
        if residual_count_by_cell[int(result["cell_id"])] != int(
            result["survivors"]
        ):
            raise AssertionError(
                "residual TSV disagrees with compiled cell summary"
            )

    permutations = tuple(itertools.permutations(range(3)))
    six_ray_reconstructions = 0
    maximal_contradictions = 0
    maximal_survivors: list[dict[str, object]] = []
    contradiction_records: list[dict[str, object]] = []
    guaranteed_matching_histogram: Counter[int] = Counter()
    maximal_matching_histogram: Counter[int] = Counter()
    maximal_unit_histogram: Counter[int] = Counter()
    ray_minimum_colouring_histogram: Counter[int] = Counter()
    pareto_signature_histogram: Counter[int] = Counter()
    lexicographic_cone_contradictions = 0

    for residual_index, residual in enumerate(residuals):
        cell_id = int(residual["cell_id"])
        cell = cells[cell_id]
        if (
            int(cell["graph_index"]) != int(residual["graph_index"])
            or int(cell["cell_index"]) != int(residual["cell_index"])
        ):
            raise AssertionError("residual cell metadata changed")
        normals: tuple[NormalType, ...] = tuple(
            tuple(map(int, row)) for row in cell["normal_types"]
        )
        diagonal_matchings = tuple(
            tuple(tuple(map(int, edge)) for edge in matching)
            for matching in cell["diagonal_matchings"]
        )
        potentials = tuple(
            tuple(
                permuted_potential(normal, permutation)
                for permutation in permutations
            )
            for normal in normals
        )
        # Reindex to potentials[vertex][colour][ray].
        potentials_by_colour = tuple(
            tuple(
                tuple(
                    potentials[vertex][ray][colour]
                    for ray in range(6)
                )
                for colour in range(3)
            )
            for vertex in range(12)
        )

        guaranteed: list[EntryEdge] = []
        maximal: list[EntryEdge] = []
        diagonal_pairs: set[tuple[int, int]] = set()
        for colour, matching in enumerate(diagonal_matchings):
            for left, right in matching:
                pair = (min(left, right), max(left, right))
                if pair in diagonal_pairs:
                    raise AssertionError(
                        "diagonal matchings ceased to be disjoint"
                    )
                diagonal_pairs.add(pair)
                own: EntryEdge = (
                    pair[0],
                    pair[1],
                    colour,
                    colour,
                    True,
                    "D",
                    0,
                )
                guaranteed.append(own)
                maximal.append(own)
                optional = tuple(
                    (row, column)
                    for row in range(3)
                    for column in range(3)
                    if (
                        row != column
                        and allowed_unit(
                            normals[pair[0]],
                            normals[pair[1]],
                            row,
                            column,
                        )
                    )
                )
                if len(optional) > 1:
                    raise AssertionError(
                        "D block lost its at-most-one optional unit"
                    )
                for row, column in optional:
                    weights = tuple(
                        potentials_by_colour[pair[0]][row][ray]
                        + potentials_by_colour[pair[1]][column][ray]
                        for ray in range(6)
                    )
                    if any(weight <= 0 for weight in weights):
                        raise AssertionError(
                            "optional D unit lost positivity"
                        )
                    maximal.append(
                        (
                            pair[0],
                            pair[1],
                            row,
                            column,
                            False,
                            "D_optional",
                            weights[0],
                        )
                    )

        ports: tuple[Port, ...] = residual["ports"]  # type: ignore[assignment]
        used_stubs: set[tuple[int, int]] = set()
        used_pairs: set[tuple[int, int]] = set()
        for left, right, left_colour, right_colour in ports:
            pair = (left, right)
            if (
                not 0 <= left < right < 12
                or pair in diagonal_pairs
                or pair in used_pairs
                or (left, left_colour) in used_stubs
                or (right, right_colour) in used_stubs
                or normals[left][left_colour] != right_colour
                or normals[right][right_colour] != left_colour
            ):
                raise AssertionError("invalid reciprocal port residual")
            used_pairs.add(pair)
            used_stubs.add((left, left_colour))
            used_stubs.add((right, right_colour))
            weights = tuple(
                potentials_by_colour[left][left_colour][ray]
                + potentials_by_colour[right][right_colour][ray]
                for ray in range(6)
            )
            item: EntryEdge = (
                left,
                right,
                left_colour,
                right_colour,
                True,
                "K",
                weights[0],
            )
            guaranteed.append(item)
            maximal.append(item)
        if used_stubs != {
            (vertex, colour)
            for vertex in range(12)
            for colour in range(3)
        }:
            raise AssertionError("port graph did not cover every stub")
        if len(guaranteed) != 36:
            raise AssertionError("guaranteed unit count changed")
        maximal_unit_histogram[len(maximal)] += 1

        guaranteed_counts, _, _ = enumerate_coloured_matchings(
            12, tuple(guaranteed)
        )
        guaranteed_matching_histogram[
            sum(guaranteed_counts.values())
        ] += 1
        mixed_counts = {
            colouring: count
            for colouring, count in guaranteed_counts.items()
            if mixed(colouring)
        }
        if not mixed_counts:
            raise AssertionError("residual has no mixed colouring")

        signatures = {
            colouring: signature(colouring, potentials_by_colour)
            for colouring in mixed_counts
        }
        for ray in range(6):
            minimum = min(
                value[ray] for value in signatures.values()
            )
            minimum_rows = tuple(
                colouring
                for colouring, value in signatures.items()
                if value[ray] == minimum
            )
            ray_minimum_colouring_histogram[len(minimum_rows)] += 1
            if any(mixed_counts[colouring] == 1 for colouring in minimum_rows):
                raise AssertionError(
                    "compiled all-six residual is exposed by a ray"
                )
        six_ray_reconstructions += 1

        signature_values = set(signatures.values())
        pareto = {
            value
            for value in signature_values
            if not any(
                other != value
                and all(
                    left <= right
                    for left, right in zip(
                        other, value, strict=True
                    )
                )
                for other in signature_values
            )
        }
        pareto_signature_histogram[len(pareto)] += 1

        lex_exposed_singleton = False
        for coordinate_order in permutations_of_six():
            best_signature = min(
                signature_values,
                key=lambda value: tuple(
                    value[index] for index in coordinate_order
                ),
            )
            if any(
                count == 1
                and signatures[colouring] == best_signature
                for colouring, count in mixed_counts.items()
            ):
                lex_exposed_singleton = True
                break
        lexicographic_cone_contradictions += int(
            lex_exposed_singleton
        )

        maximal_counts, maximal_first, maximal_forced = (
            enumerate_coloured_matchings(12, tuple(maximal))
        )
        maximal_matching_histogram[sum(maximal_counts.values())] += 1
        witness = next(
            (
                colouring
                for colouring, count in sorted(maximal_counts.items())
                if (
                    count == 1
                    and mixed(colouring)
                    and maximal_forced[colouring]
                )
            ),
            None,
        )
        if witness is None:
            maximal_survivors.append(
                {
                    "residual_index": residual_index,
                    "cell_id": cell_id,
                    "architecture_hash": str(
                        residual["architecture_hash"]
                    ),
                    "guaranteed_matching_monomials": sum(
                        guaranteed_counts.values()
                    ),
                    "maximal_matching_monomials": sum(
                        maximal_counts.values()
                    ),
                    "pareto_signatures": len(pareto),
                }
            )
            continue

        maximal_contradictions += 1
        matching_ids = maximal_first[witness]
        contradiction_records.append(
            {
                "residual_index": residual_index,
                "cell_id": cell_id,
                "architecture_hash": str(
                    residual["architecture_hash"]
                ),
                "maximal_units": len(maximal),
                "maximal_unique_colouring": list(witness),
                "maximal_unique_forced_matching": [
                    {
                        "edge": [
                            maximal[edge_id][0],
                            maximal[edge_id][1],
                        ],
                        "half_colours": [
                            maximal[edge_id][2],
                            maximal[edge_id][3],
                        ],
                        "kind": maximal[edge_id][5],
                    }
                    for edge_id in matching_ids
                ],
            }
        )

    payload = {
        "verified": not maximal_survivors,
        "status": "finite_order_twelve_residual_analysis",
        "scope": (
            "all-six-potential residuals of the complete order-twelve "
            "pairwise-disjoint exact-degree-six Kotzig/port cell-orbit "
            "census, followed by maximal balanced optional-D support"
        ),
        "cells": str(args.cells),
        "cells_sha256": sha256(args.cells),
        "exhaustion": str(args.exhaustion),
        "exhaustion_sha256": sha256(args.exhaustion),
        "residuals": str(args.residuals),
        "residuals_sha256": sha256(args.residuals),
        "compiled_source": str(args.compiled_source),
        "compiled_source_sha256": sha256(args.compiled_source),
        "cell_orbits": len(cells),
        "representative_port_realizations": exhaustion[
            "representative_port_realizations"
        ],
        "labelled_cell_port_realizations": exhaustion[
            "labelled_cell_port_realizations"
        ],
        "all_six_potential_residuals": len(residuals),
        "six_ray_reconstructions": six_ray_reconstructions,
        "lexicographic_cone_contradictions": (
            lexicographic_cone_contradictions
        ),
        "pareto_signature_count_histogram": {
            str(key): value
            for key, value in sorted(pareto_signature_histogram.items())
        },
        "ray_minimum_colouring_count_histogram": {
            str(key): value
            for key, value in sorted(
                ray_minimum_colouring_histogram.items()
            )
        },
        "guaranteed_matching_monomial_count_histogram": {
            str(key): value
            for key, value in sorted(
                guaranteed_matching_histogram.items()
            )
        },
        "maximal_unit_count_histogram": {
            str(key): value
            for key, value in sorted(maximal_unit_histogram.items())
        },
        "maximal_matching_monomial_count_histogram": {
            str(key): value
            for key, value in sorted(maximal_matching_histogram.items())
        },
        "maximal_support_unique_forced_contradictions": (
            maximal_contradictions
        ),
        "contradiction_records": contradiction_records,
        "survivors": len(maximal_survivors),
        "survivor_records": maximal_survivors,
        "order_twelve_pairwise_disjoint_exact_degree_six_excluded": (
            not maximal_survivors
        ),
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
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
                if key
                in {
                    "verified",
                    "all_six_potential_residuals",
                    "lexicographic_cone_contradictions",
                    "pareto_signature_count_histogram",
                    "maximal_support_unique_forced_contradictions",
                    "survivors",
                    "order_twelve_pairwise_disjoint_exact_degree_six_excluded",
                    "elapsed_seconds",
                }
            },
            indent=2,
        )
    )


def permutations_of_six() -> tuple[tuple[int, ...], ...]:
    return tuple(itertools.permutations(range(6)))


if __name__ == "__main__":
    main()
