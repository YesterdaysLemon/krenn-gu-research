"""Independent replay of the order-twelve residual contradictions.

This audit intentionally does not import the primary residual analyzer.
It rebuilds the six potentials, guaranteed and maximal unit sets, and
matching counters directly from the cell census plus residual TSV.  For
every claimed contradiction it checks:

* the architecture is a reciprocal simple cubic port realization;
* every one of the six ray-minimum layers has no singleton colouring;
* the recorded maximal-support colouring has exactly one compatible
  perfect matching; and
* every unit of that matching is forced.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time

Normal = tuple[int, int, int]
Unit = tuple[int, int, int, int, bool, str]
Port = tuple[int, int, int, int]
EXTREME_RAYS = (
    (-4, 1, 1, 1, 6, -4),
    (-4, 1, 6, 1, 1, -4),
    (1, -4, 1, 1, -4, 6),
    (1, -4, 1, 6, -4, 1),
    (1, 6, -4, -4, 1, 1),
    (6, 1, -4, -4, 1, 1),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def allowed(
    left: Normal, right: Normal, row: int, column: int
) -> bool:
    for target in range(3):
        if (
            (row, column) != (target, target)
            and row != left[target]
            and column != right[target]
        ):
            return False
    return True


def base_potential(normal: Normal) -> tuple[int, int, int]:
    b0 = int(normal[0] == 2)
    b1 = int(normal[1] == 2)
    b2 = int(normal[2] == 1)
    return (
        1 - 2 * b2,
        2 * (b2 - b0),
        2 * (b0 + b1 - 1),
    )


def relabelled_potential(
    normal: Normal, permutation: tuple[int, int, int]
) -> tuple[int, int, int]:
    image = [-1, -1, -1]
    for colour in range(3):
        image[permutation[colour]] = permutation[normal[colour]]
    base = base_potential(tuple(image))
    return tuple(base[permutation[colour]] for colour in range(3))


def enumerate_unit_matchings(
    order: int, units: tuple[Unit, ...]
) -> Counter[tuple[int, ...]]:
    incident: list[list[int]] = [[] for _ in range(order)]
    for unit_id, (left, right, *_rest) in enumerate(units):
        incident[left].append(unit_id)
        incident[right].append(unit_id)
    colours = [-1] * order
    counts: Counter[tuple[int, ...]] = Counter()

    def visit(remaining: int) -> None:
        if remaining == 0:
            row = tuple(colours)
            counts[row] = min(2, counts[row] + 1)
            return
        left = (remaining & -remaining).bit_length() - 1
        for unit_id in incident[left]:
            u, v, cu, cv, _forced, _kind = units[unit_id]
            if v == left:
                u, v = v, u
                cu, cv = cv, cu
            if not remaining & (1 << v):
                continue
            colours[u] = cu
            colours[v] = cv
            visit(remaining ^ (1 << u) ^ (1 << v))
            colours[u] = -1
            colours[v] = -1

    visit((1 << order) - 1)
    return counts


def compatible_matching_count(
    order: int,
    units: tuple[Unit, ...],
    colouring: tuple[int, ...],
) -> tuple[int, tuple[int, ...] | None]:
    compatible = tuple(
        unit_id
        for unit_id, (left, right, cu, cv, _forced, _kind) in enumerate(
            units
        )
        if colouring[left] == cu and colouring[right] == cv
    )
    incident: list[list[int]] = [[] for _ in range(order)]
    for unit_id in compatible:
        left, right, *_rest = units[unit_id]
        incident[left].append(unit_id)
        incident[right].append(unit_id)
    count = 0
    first: tuple[int, ...] | None = None
    chosen: list[int] = []

    def visit(remaining: int) -> None:
        nonlocal count, first
        if count >= 2:
            return
        if remaining == 0:
            count += 1
            if first is None:
                first = tuple(chosen)
            return
        left = (remaining & -remaining).bit_length() - 1
        for unit_id in incident[left]:
            u, v, *_rest = units[unit_id]
            other = v if u == left else u
            if not remaining & (1 << other):
                continue
            chosen.append(unit_id)
            visit(remaining ^ (1 << left) ^ (1 << other))
            chosen.pop()

    visit((1 << order) - 1)
    return count, first


def read_ports(path: Path) -> dict[str, tuple[int, tuple[Port, ...]]]:
    output: dict[str, tuple[int, tuple[Port, ...]]] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        fields = tuple(map(int, raw.split()))
        cell_id = fields[0]
        architecture = str(fields[3])
        ports = tuple(
            tuple(fields[offset : offset + 4])
            for offset in range(4, len(fields), 4)
        )
        if architecture in output:
            raise AssertionError("duplicate residual architecture hash")
        output[architecture] = (cell_id, ports)
    return output


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
        "--residuals",
        type=Path,
        default=Path(
            "tmp", "twelve_vertex_six_potential_orbits_residuals.tsv"
        ),
    )
    parser.add_argument(
        "--primary",
        type=Path,
        default=Path(
            "tmp",
            "twelve_vertex_six_potential_residuals_analyzed.json",
        ),
    )
    parser.add_argument(
        "--full-cone-primary",
        type=Path,
        default=Path(
            "tmp",
            "twelve_vertex_full_potential_cone_analyzed.json",
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp",
            "twelve_vertex_six_potential_residuals_audited.json",
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    cells_payload = json.loads(args.cells.read_text(encoding="utf-8"))
    cells = cells_payload["cell_representatives"]
    primary = json.loads(args.primary.read_text(encoding="utf-8"))
    full_cone_primary = json.loads(
        args.full_cone_primary.read_text(encoding="utf-8")
    )
    ports_by_hash = read_ports(args.residuals)
    records = primary["contradiction_records"]
    if (
        primary.get("verified") is not True
        or primary.get("all_six_potential_residuals") != 395
        or primary.get("survivors") != 0
        or len(records) != 395
        or len(ports_by_hash) != 395
        or full_cone_primary.get("verified") is not True
        or full_cone_primary.get("full_cone_contradictions") != 395
        or full_cone_primary.get("survivors") != 0
    ):
        raise AssertionError("primary residual analysis binding changed")

    permutations = tuple(itertools.permutations(range(3)))
    audited = 0
    ray_minimum_count_histogram: Counter[int] = Counter()
    compatible_unit_histogram: Counter[int] = Counter()
    optional_unit_histogram: Counter[int] = Counter()
    full_cone_success_count_histogram: Counter[int] = Counter()
    for record in records:
        architecture = str(record["architecture_hash"])
        cell_id, ports = ports_by_hash[architecture]
        if cell_id != int(record["cell_id"]):
            raise AssertionError("recorded cell id changed")
        cell = cells[cell_id]
        normals = tuple(
            tuple(map(int, row)) for row in cell["normal_types"]
        )
        potentials = tuple(
            tuple(
                tuple(
                    relabelled_potential(normal, permutation)[colour]
                    for permutation in permutations
                )
                for colour in range(3)
            )
            for normal in normals
        )
        guaranteed: list[Unit] = []
        maximal: list[Unit] = []
        diagonal_pairs: set[tuple[int, int]] = set()
        for colour, matching in enumerate(
            cell["diagonal_matchings"]
        ):
            for raw_pair in matching:
                left, right = sorted(map(int, raw_pair))
                diagonal_pairs.add((left, right))
                own = (left, right, colour, colour, True, "D")
                guaranteed.append(own)
                maximal.append(own)
                options = tuple(
                    (row, column)
                    for row in range(3)
                    for column in range(3)
                    if (
                        row != column
                        and allowed(
                            normals[left],
                            normals[right],
                            row,
                            column,
                        )
                    )
                )
                if len(options) > 1:
                    raise AssertionError("too many optional D units")
                for row, column in options:
                    for ray in range(6):
                        if (
                            potentials[left][row][ray]
                            + potentials[right][column][ray]
                            <= 0
                        ):
                            raise AssertionError(
                                "optional unit is not positive"
                            )
                    maximal.append(
                        (
                            left,
                            right,
                            row,
                            column,
                            False,
                            "D_optional",
                        )
                    )

        used_pairs: set[tuple[int, int]] = set()
        used_stubs: set[tuple[int, int]] = set()
        for left, right, cu, cv in ports:
            if (
                (left, right) in diagonal_pairs
                or (left, right) in used_pairs
                or (left, cu) in used_stubs
                or (right, cv) in used_stubs
                or normals[left][cu] != cv
                or normals[right][cv] != cu
            ):
                raise AssertionError("port reciprocity audit failed")
            used_pairs.add((left, right))
            used_stubs.add((left, cu))
            used_stubs.add((right, cv))
            item = (left, right, cu, cv, True, "K")
            guaranteed.append(item)
            maximal.append(item)
        if len(used_stubs) != 36 or len(guaranteed) != 36:
            raise AssertionError("port cover audit failed")
        optional_unit_histogram[len(maximal) - len(guaranteed)] += 1

        counts = enumerate_unit_matchings(12, tuple(guaranteed))
        mixed_counts = {
            colouring: count
            for colouring, count in counts.items()
            if len(set(colouring)) > 1
        }
        for ray in range(6):
            values = {
                colouring: sum(
                    potentials[vertex][colour][ray]
                    for vertex, colour in enumerate(colouring)
                )
                for colouring in mixed_counts
            }
            minimum = min(values.values())
            rows = tuple(
                colouring
                for colouring, value in values.items()
                if value == minimum
            )
            ray_minimum_count_histogram[len(rows)] += 1
            if any(mixed_counts[colouring] == 1 for colouring in rows):
                raise AssertionError("architecture is not a ray residual")

        signatures = {
            colouring: tuple(
                sum(
                    potentials[vertex][colour][ray]
                    for vertex, colour in enumerate(colouring)
                )
                for ray in range(6)
            )
            for colouring in mixed_counts
        }
        extreme_successes = 0
        for extreme in EXTREME_RAYS:
            keys = {
                colouring: (
                    sum(
                        value[index] * extreme[index]
                        for index in range(6)
                    ),
                    sum(value),
                )
                for colouring, value in signatures.items()
            }
            minimum = min(keys.values())
            extreme_successes += any(
                count == 1 and keys[colouring] == minimum
                for colouring, count in mixed_counts.items()
            )
        if extreme_successes == 0:
            raise AssertionError(
                "full admissible cone left a residual architecture"
            )
        full_cone_success_count_histogram[extreme_successes] += 1

        witness = tuple(map(int, record["maximal_unique_colouring"]))
        count, matching = compatible_matching_count(
            12, tuple(maximal), witness
        )
        compatible_unit_histogram[
            sum(
                witness[left] == cu and witness[right] == cv
                for left, right, cu, cv, _forced, _kind in maximal
            )
        ] += 1
        if count != 1 or matching is None:
            raise AssertionError(
                "maximal-support witness is not a singleton"
            )
        if not all(maximal[unit_id][4] for unit_id in matching):
            raise AssertionError(
                "maximal-support singleton uses an optional unit"
            )
        expected = {
            (
                tuple(map(int, item["edge"])),
                tuple(map(int, item["half_colours"])),
                str(item["kind"]),
            )
            for item in record["maximal_unique_forced_matching"]
        }
        observed = {
            (
                (maximal[unit_id][0], maximal[unit_id][1]),
                (maximal[unit_id][2], maximal[unit_id][3]),
                maximal[unit_id][5],
            )
            for unit_id in matching
        }
        if expected != observed:
            raise AssertionError("recorded singleton matching changed")
        audited += 1

    payload = {
        "verified": audited == 395,
        "status": "independent_order_twelve_residual_replay",
        "scope": (
            "independent reconstruction of all six-ray residuals and "
            "direct replay of each maximal-support forced singleton"
        ),
        "cells": str(args.cells),
        "cells_sha256": sha256(args.cells),
        "residuals": str(args.residuals),
        "residuals_sha256": sha256(args.residuals),
        "primary": str(args.primary),
        "primary_sha256": sha256(args.primary),
        "full_cone_primary": str(args.full_cone_primary),
        "full_cone_primary_sha256": sha256(args.full_cone_primary),
        "residual_architectures": len(ports_by_hash),
        "audited_contradictions": audited,
        "ray_minimum_colouring_count_histogram": {
            str(key): value
            for key, value in sorted(
                ray_minimum_count_histogram.items()
            )
        },
        "optional_unit_count_histogram": {
            str(key): value
            for key, value in sorted(optional_unit_histogram.items())
        },
        "full_cone_success_count_histogram": {
            str(key): value
            for key, value in sorted(
                full_cone_success_count_histogram.items()
            )
        },
        "full_cone_residuals": 0,
        "compatible_maximal_unit_count_histogram": {
            str(key): value
            for key, value in sorted(
                compatible_unit_histogram.items()
            )
        },
        "survivors": 0,
        "order_twelve_residuals_excluded": audited == 395,
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "verified": payload["verified"],
                "audited_contradictions": audited,
                "survivors": 0,
                "elapsed_seconds": payload["elapsed_seconds"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
