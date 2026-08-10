"""Scout the first reciprocal port graph in each Kotzig/type cell.

This is an explicitly exploratory arbitrary-order driver.  It enumerates
the complete connected cubic catalogue at the requested even order,
every distinguished Kotzig colouring, all eight propagated normal-type
assignments, and the first deterministic reciprocal port realization in
each feasible cell.  It tests both the original six potentials and the
six extreme-ray/interior lexicographic directions of the full admissible
cone.  It does not enumerate all port realizations.
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

from krenn_gu.bootstrap import (  # noqa: E402
    bootstrap as _bootstrap_repository,
    expose_claim_package,
)

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])
expose_claim_package(REPO_ROOT, "claims/finite/n10/degree-six-kotzig-port")
expose_claim_package(REPO_ROOT, "claims/finite/n08/degree-six-kotzig-port")

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

from analyze_ten_vertex_degree_six_kotzig_port_survivors import (
    enumerate_coloured_matchings,
)
from analyze_ten_vertex_permuted_potential_survivors import (
    permuted_potential,
)
from explore_eight_vertex_degree_six_kotzig_ports import (
    decode_graph6,
    kotzig_colourings,
    normal_types,
)

from scout_twelve_vertex_six_potential_cells import (
    first_port_realization,
)
from krenn_gu.admissible_potential_cone import EXTREME_RAYS


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def catalogue(order: int) -> tuple[str, ...]:
    resolved = Path.cwd().resolve().as_posix()
    if len(resolved) < 3 or resolved[1:3] != ":/":
        raise AssertionError("expected a Windows drive workspace")
    workspace = f"/mnt/{resolved[0].lower()}/{resolved[3:]}"
    command = (
        f'cd "{workspace}" && '
        f"./tmp/nauty2_9_3/geng -cq -d3 -D3 {order}"
    )
    result = subprocess.run(
        ["wsl", "bash", "-lc", command],
        check=True,
        capture_output=True,
        text=True,
    )
    return tuple(
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    )


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=14)
    parser.add_argument(
        "--examples",
        type=int,
        default=20,
        help="maximum full-cone residual examples retained",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp", "fourteen_vertex_full_cone_cells_scouted.json"
        ),
    )
    args = parser.parse_args()
    if args.order < 8 or args.order % 2:
        raise ValueError("--order must be even and at least eight")
    started = time.perf_counter()
    rows = catalogue(args.order)
    permutations = tuple(itertools.permutations(range(3)))
    interior = (1, 1, 1, 1, 1, 1)
    labelled_kotzig = 0
    cells = 0
    feasible = 0
    old_residuals = 0
    full_residuals = 0
    old_success_histogram: Counter[int] = Counter()
    full_success_histogram: Counter[int] = Counter()
    examples = []
    graph_records = []

    for graph_index, graph6 in enumerate(rows):
        vertices = range(args.order)
        graph_edges = set(decode_graph6(graph6))
        colourings = kotzig_colourings(vertices, graph_edges)
        labelled_kotzig += len(colourings)
        graph_cells = 0
        graph_feasible = 0
        graph_old_residuals = 0
        graph_full_residuals = 0
        for colouring_index, colouring in enumerate(colourings):
            assignments = normal_types(vertices, colouring)
            for type_index, normals in enumerate(assignments):
                cells += 1
                graph_cells += 1
                ports = first_port_realization(
                    args.order, colouring, normals
                )
                if ports is None:
                    continue
                feasible += 1
                graph_feasible += 1
                edges = list(ports)
                for colour, matching in enumerate(colouring):
                    edges.extend(
                        (
                            left,
                            right,
                            colour,
                            colour,
                            True,
                            "D",
                            0,
                        )
                        for left, right in matching
                    )
                counts, _first, _forced = (
                    enumerate_coloured_matchings(
                        args.order, tuple(edges)
                    )
                )
                mixed_counts = {
                    row: count
                    for row, count in counts.items()
                    if len(set(row)) > 1
                }
                potentials = tuple(
                    tuple(
                        tuple(
                            permuted_potential(normal, permutation)[
                                colour
                            ]
                            for permutation in permutations
                        )
                        for colour in range(3)
                    )
                    for normal in normals
                )
                signatures = {
                    row: tuple(
                        sum(
                            potentials[vertex][colour][ray]
                            for vertex, colour in enumerate(row)
                        )
                        for ray in range(6)
                    )
                    for row in mixed_counts
                }

                old_successes = 0
                for ray in range(6):
                    minimum = min(
                        value[ray] for value in signatures.values()
                    )
                    old_successes += any(
                        mixed_counts[row] == 1
                        and signatures[row][ray] == minimum
                        for row in mixed_counts
                    )
                old_success_histogram[old_successes] += 1
                if old_successes == 0:
                    old_residuals += 1
                    graph_old_residuals += 1

                full_successes = 0
                for extreme in EXTREME_RAYS:
                    keys = {
                        row: (
                            dot(value, extreme),
                            dot(value, interior),
                        )
                        for row, value in signatures.items()
                    }
                    minimum = min(keys.values())
                    full_successes += any(
                        mixed_counts[row] == 1
                        and keys[row] == minimum
                        for row in mixed_counts
                    )
                full_success_histogram[full_successes] += 1
                if full_successes == 0:
                    full_residuals += 1
                    graph_full_residuals += 1
                    if len(examples) < args.examples:
                        examples.append(
                            {
                                "graph_index": graph_index,
                                "graph6": graph6,
                                "colouring_index": colouring_index,
                                "type_index": type_index,
                                "normal_types": [
                                    list(normal) for normal in normals
                                ],
                                "diagonal_matchings": [
                                    [list(pair) for pair in matching]
                                    for matching in colouring
                                ],
                                "port_edges": [
                                    {
                                        "edge": [edge[0], edge[1]],
                                        "half_colours": [
                                            edge[2],
                                            edge[3],
                                        ],
                                    }
                                    for edge in ports
                                ],
                            }
                        )
        graph_records.append(
            {
                "graph_index": graph_index,
                "graph6": graph6,
                "kotzig_colourings": len(colourings),
                "type_cells": graph_cells,
                "feasible_first_ports": graph_feasible,
                "original_six_ray_residuals": graph_old_residuals,
                "full_cone_residuals": graph_full_residuals,
            }
        )
        print(
            "graph",
            graph_index + 1,
            "/",
            len(rows),
            "kotzig",
            len(colourings),
            "cells",
            cells,
            "feasible",
            feasible,
            "full residuals",
            full_residuals,
            "elapsed",
            round(time.perf_counter() - started, 1),
            flush=True,
        )

    payload = {
        "verified": True,
        "status": "exploratory_first_port_full_cone_scout",
        "scope": (
            "complete connected cubic/Kotzig/type cell domain at the "
            "requested order, but only the first deterministic reciprocal "
            "port realization in each feasible cell"
        ),
        "order": args.order,
        "connected_cubic_classes": len(rows),
        "catalogue_graph6": list(rows),
        "labelled_kotzig_colourings": labelled_kotzig,
        "normal_type_cells": cells,
        "feasible_first_port_cells": feasible,
        "original_six_success_count_histogram": {
            str(key): value
            for key, value in sorted(old_success_histogram.items())
        },
        "full_cone_success_count_histogram": {
            str(key): value
            for key, value in sorted(full_success_histogram.items())
        },
        "original_six_ray_residuals": old_residuals,
        "full_cone_residuals": full_residuals,
        "full_cone_residual_examples": examples,
        "graph_records": graph_records,
        "sampling_complete_for_port_graphs": False,
        "finite_order_branch_excluded": False,
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
                "order": args.order,
                "connected_cubic_classes": len(rows),
                "normal_type_cells": cells,
                "feasible_first_port_cells": feasible,
                "original_six_ray_residuals": old_residuals,
                "full_cone_residuals": full_residuals,
                "sampling_complete_for_port_graphs": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
