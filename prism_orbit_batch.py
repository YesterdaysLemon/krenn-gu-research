"""Generate exact generic and exceptional jobs for prism half-edge orbits."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from enumerate_cubic_rankone import (
    graph_automorphisms,
    graph_edges,
    transform_pattern,
)
from prism_orbit_screen import (
    Polynomial,
    core_rank_one_audit,
    minimal_monomial_zero_covers,
    orbit_equations,
    prism_orbit_representatives,
    singular_program,
)
from search_prism_stratum import PRISM_MATCHINGS
from search_witness import EquationSystem


def complement_edge_blocks() -> tuple[list[tuple[int, int]], dict[tuple[int, int], int]]:
    prism_edges = graph_edges(PRISM_MATCHINGS)
    free_edges = sorted(
        set(itertools.combinations(range(6), 2)) - set(prism_edges)
    )
    return free_edges, {edge: index for index, edge in enumerate(free_edges)}


def stabilizer_block_representatives(
    pattern: tuple[int, ...],
) -> list[int]:
    prism_edges = graph_edges(PRISM_MATCHINGS)
    automorphisms = graph_automorphisms(prism_edges)
    stabilizer = [
        (vertex_permutation, colour_permutation)
        for vertex_permutation in automorphisms
        for colour_permutation in itertools.permutations(range(3))
        if transform_pattern(
            pattern, vertex_permutation, colour_permutation
        )
        == pattern
    ]
    free_edges, block_by_edge = complement_edge_blocks()
    unseen = set(free_edges)
    representatives: list[int] = []
    while unseen:
        edge = min(unseen)
        orbit = {
            tuple(
                sorted(
                    (
                        vertex_permutation[edge[0]],
                        vertex_permutation[edge[1]],
                    )
                )
            )
            for vertex_permutation, _ in stabilizer
        }
        representatives.append(block_by_edge[edge])
        unseen -= orbit
    return representatives


def variable_zero_equation(variable: str) -> Polynomial:
    equation: Polynomial = Counter()
    equation[(variable,)] = 1
    return equation


def write_jobs(
    output_directory: Path,
    orbit_index: int,
    characteristic: int,
    algorithm: str,
    system: EquationSystem,
    pattern: tuple[int, ...],
    generic_only: bool = False,
) -> dict[str, object]:
    names, equations = orbit_equations(system, pattern)
    audit = core_rank_one_audit(system, pattern)
    if not audit["passes"]:
        raise ValueError(f"orbit {orbit_index} does not pass the core audit")
    lambdas = audit["lambdas"]
    matrices = audit["remainder_matrices"]
    assert isinstance(lambdas, list)
    assert isinstance(matrices, list)

    suffix = "q" if characteristic == 0 else str(characteristic)
    output_directory.mkdir(parents=True, exist_ok=True)
    generic_name = f"prism_orbit_{orbit_index}_generic_{suffix}.sing"
    (output_directory / generic_name).write_text(
        singular_program(
            orbit_index,
            names,
            equations,
            characteristic,
            "full",
            algorithm,
            add_rank_one_minors=True,
        ),
        encoding="utf-8",
    )

    branches: list[dict[str, object]] = []
    for block_index in (
        [] if generic_only else stabilizer_block_representatives(pattern)
    ):
        covers = minimal_monomial_zero_covers(matrices[block_index])
        for cover_index, cover in enumerate(covers):
            name = (
                f"prism_orbit_{orbit_index}_b{block_index}_"
                f"cover{cover_index}_{suffix}.sing"
            )
            extra = [lambdas[block_index]]
            extra.extend(variable_zero_equation(variable) for variable in cover)
            (output_directory / name).write_text(
                singular_program(
                    orbit_index,
                    names,
                    equations,
                    characteristic,
                    "full",
                    algorithm,
                    extra_equations=extra,
                ),
                encoding="utf-8",
            )
            branches.append(
                {
                    "block": block_index,
                    "cover": list(cover),
                    "file": name,
                }
            )
    return {
        "orbit": orbit_index,
        "generic": generic_name,
        "branches": branches,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--indices", type=int, nargs="+", required=True)
    parser.add_argument("--output-directory", type=Path, default=Path("."))
    parser.add_argument("--characteristic", type=int, default=0)
    parser.add_argument("--algorithm", choices=("std", "slimgb"), default="slimgb")
    parser.add_argument("--generic-only", action="store_true")
    args = parser.parse_args()

    representatives = prism_orbit_representatives()
    system = EquationSystem(6, 3)
    rows = []
    for orbit_index in args.indices:
        if not 0 <= orbit_index < len(representatives):
            raise ValueError(
                f"orbit index {orbit_index} must lie in 0..{len(representatives) - 1}"
            )
        rows.append(
            write_jobs(
                args.output_directory,
                orbit_index,
                args.characteristic,
                args.algorithm,
                system,
                representatives[orbit_index],
                args.generic_only,
            )
        )
    manifest = args.output_directory / "prism_orbit_batch_manifest.json"
    manifest.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(
        f"wrote {sum(1 + len(row['branches']) for row in rows)} jobs "
        f"for {len(rows)} orbits and {manifest}"
    )


if __name__ == "__main__":
    main()
