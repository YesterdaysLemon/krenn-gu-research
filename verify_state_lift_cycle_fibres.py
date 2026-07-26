"""Verify the lifted-cycle fibre formula on all hard order-twelve cases."""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

from analyze_ten_vertex_degree_six_kotzig_port_survivors import (
    enumerate_coloured_matchings,
)
from analyze_ten_vertex_permuted_potential_survivors import (
    permuted_potential,
)
from verify_full_admissible_potential_cone import EXTREME_RAYS


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def main() -> None:
    cells_path = Path(
        "tmp", "twelve_vertex_port_cell_orbits_counted.json"
    )
    residuals_path = Path(
        "tmp", "twelve_vertex_six_potential_orbits_residuals.tsv"
    )
    theorem_path = Path("STATE_LIFT_CYCLE_FIBRE_LEMMA.md")
    cells = json.loads(
        cells_path.read_text(encoding="utf-8")
    )["cell_representatives"]
    rows = tuple(
        tuple(map(int, line.split()))
        for line in residuals_path.read_text(
            encoding="utf-8"
        ).splitlines()
    )
    if len(rows) != 395:
        raise AssertionError("order-twelve residual count changed")
    permutations = tuple(itertools.permutations(range(3)))
    lifted_component_count_histogram: Counter[int] = Counter()
    transversal_girth_histogram: Counter[int] = Counter()
    extreme_small_positive_ray_histogram: Counter[int] = Counter()
    architectures_with_girth_singleton_bound = 0
    colourings_checked = 0

    for fields in rows:
        cell = cells[fields[0]]
        normals = tuple(
            tuple(map(int, normal))
            for normal in cell["normal_types"]
        )
        state_adjacency: list[list[tuple[int, str]]] = [
            [] for _ in range(36)
        ]
        matching_edges = []
        for colour, matching in enumerate(
            cell["diagonal_matchings"]
        ):
            for left, right in matching:
                first = 3 * left + colour
                second = 3 * right + colour
                state_adjacency[first].append((second, "D"))
                state_adjacency[second].append((first, "D"))
                matching_edges.append(
                    (
                        left,
                        right,
                        colour,
                        colour,
                        True,
                        "D",
                        0,
                    )
                )
        for offset in range(4, len(fields), 4):
            left, right, cu, cv = fields[offset : offset + 4]
            first = 3 * left + cu
            second = 3 * right + cv
            state_adjacency[first].append((second, "K"))
            state_adjacency[second].append((first, "K"))
            matching_edges.append(
                (left, right, cu, cv, True, "K", 0)
            )
        if any(
            sorted(kind for _other, kind in neighbours) != ["D", "K"]
            for neighbours in state_adjacency
        ):
            raise AssertionError("lifted state graph is not D/K 2-regular")

        components = []
        state_component = [-1] * 36
        for root in range(36):
            if state_component[root] != -1:
                continue
            component_id = len(components)
            component = []
            stack = [root]
            state_component[root] = component_id
            while stack:
                state = stack.pop()
                component.append(state)
                for other, _kind in state_adjacency[state]:
                    if state_component[other] == -1:
                        state_component[other] = component_id
                        stack.append(other)
            if len(component) % 2:
                raise AssertionError("lifted component has odd length")
            components.append(tuple(component))
        lifted_component_count_histogram[len(components)] += 1
        transversal_lengths = tuple(
            len(component)
            for component in components
            if len({state // 3 for state in component})
            == len(component)
        )
        girth = min(transversal_lengths, default=10**9)
        transversal_girth_histogram[girth] += 1

        counts, _first, _forced = enumerate_coloured_matchings(
            12, tuple(matching_edges)
        )
        for colouring, count in counts.items():
            selected = {
                3 * vertex + colour
                for vertex, colour in enumerate(colouring)
            }
            full_components = sum(
                all(state in selected for state in component)
                for component in components
            )
            if count != 2**full_components:
                raise AssertionError("lifted fibre formula failed")
            colourings_checked += 1

        mixed_counts = {
            colouring: count
            for colouring, count in counts.items()
            if len(set(colouring)) > 1
        }
        potentials = tuple(
            tuple(
                tuple(
                    permuted_potential(normal, permutation)[colour]
                    for permutation in permutations
                )
                for colour in range(3)
            )
            for normal in normals
        )
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
        small_rays = 0
        for extreme in EXTREME_RAYS:
            minimum = min(
                dot(value, extreme)
                for value in signatures.values()
            )
            positive_states = (minimum // 5 + 12) // 2
            if positive_states < girth / 2:
                small_rays += 1
        extreme_small_positive_ray_histogram[small_rays] += 1
        architectures_with_girth_singleton_bound += small_rays > 0

    if (
        transversal_girth_histogram != Counter({4: 395})
        or architectures_with_girth_singleton_bound != 7
    ):
        raise AssertionError("order-twelve lifted-girth census changed")
    payload = {
        "verified": True,
        "status": "order_twelve_state_lift_cycle_fibre_verification",
        "scope": (
            "all 395 original-six-ray residual architectures; exact "
            "lifted D/K components, every feasible colouring fibre, and "
            "the Boolean extreme positive-state girth criterion"
        ),
        "cells": str(cells_path),
        "cells_sha256": sha256(cells_path),
        "residuals": str(residuals_path),
        "residuals_sha256": sha256(residuals_path),
        "theorem": str(theorem_path),
        "theorem_sha256": sha256(theorem_path),
        "architectures": len(rows),
        "colouring_fibres_checked": colourings_checked,
        "lifted_component_count_histogram": {
            str(key): value
            for key, value in sorted(
                lifted_component_count_histogram.items()
            )
        },
        "transversal_lifted_girth_histogram": {
            str(key): value
            for key, value in sorted(
                transversal_girth_histogram.items()
            )
        },
        "extreme_girth_bound_success_count_histogram": {
            str(key): value
            for key, value in sorted(
                extreme_small_positive_ray_histogram.items()
            )
        },
        "architectures_excluded_by_girth_bound": (
            architectures_with_girth_singleton_bound
        ),
        "architectures_not_excluded_by_girth_bound": (
            len(rows) - architectures_with_girth_singleton_bound
        ),
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp", "state_lift_cycle_fibres_verified.json"
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "verified": True,
                "architectures": len(rows),
                "colouring_fibres_checked": colourings_checked,
                "transversal_lifted_girth_histogram": {"4": 395},
                "architectures_excluded_by_girth_bound": 7,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
