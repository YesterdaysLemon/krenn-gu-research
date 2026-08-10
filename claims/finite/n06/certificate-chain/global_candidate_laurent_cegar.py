"""Global support-to-Laurent CEGAR for the remaining 11/12-edge cases."""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
from collections import Counter
from functools import lru_cache
from pathlib import Path

from candidate_killer_cover_sat import candidate_cover_cnf
from candidate_matching_obstruction_sat import add_lex_leq
from killer_union_stratum import (
    normalized_union_stratum,
    union_orbit_equations_with_colourings,
)
from prism_laurent_reduction import primitive_binomial_reduction
from prism_orbit_screen import clean_polynomial, singular_program
from rankone_support_sat import windows_to_wsl
from search_witness import EquationSystem
from verify_prism_certificates import is_exact_unit_log


def candidate_variable_map() -> dict[tuple[int, int, int], int]:
    variable = EquationSystem(6, 3).variable_count
    result = {}
    for vertex in range(6):
        for colour in range(3):
            for neighbour in range(6):
                if neighbour == vertex:
                    continue
                variable += 1
                result[(vertex, colour, neighbour)] = variable
    return result


def transform_flat_entry(
    system: EquationSystem,
    flat_index: int,
    vertex_permutation: tuple[int, ...],
    colour_permutation: tuple[int, ...],
) -> int:
    """Relabel one oriented matrix entry under vertices and global colours."""
    edge_position, entry_position = divmod(flat_index, 9)
    first_colour, second_colour = divmod(entry_position, 3)
    first, second = system.edges[edge_position]
    new_first = vertex_permutation[first]
    new_second = vertex_permutation[second]
    new_first_colour = colour_permutation[first_colour]
    new_second_colour = colour_permutation[second_colour]
    if new_first < new_second:
        edge = (new_first, new_second)
        row_colour = new_first_colour
        column_colour = new_second_colour
    else:
        edge = (new_second, new_first)
        row_colour = new_second_colour
        column_colour = new_first_colour
    return (
        system.edge_index[edge] * 9
        + 3 * row_colour
        + column_colour
    )


def symmetry_transforms(
    mode: str,
) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    identity_vertices = tuple(range(6))
    identity_colours = tuple(range(3))
    if mode == "none":
        return [(identity_vertices, identity_colours)]
    if mode == "generators":
        transforms = [(identity_vertices, identity_colours)]
        for index in range(5):
            permutation = list(identity_vertices)
            permutation[index], permutation[index + 1] = (
                permutation[index + 1],
                permutation[index],
            )
            transforms.append((tuple(permutation), identity_colours))
        for index in range(2):
            permutation = list(identity_colours)
            permutation[index], permutation[index + 1] = (
                permutation[index + 1],
                permutation[index],
            )
            transforms.append((identity_vertices, tuple(permutation)))
        return transforms
    if mode == "full":
        return [
            (vertex_permutation, colour_permutation)
            for vertex_permutation in itertools.permutations(range(6))
            for colour_permutation in itertools.permutations(range(3))
        ]
    raise ValueError(f"unknown symmetry mode: {mode}")


def add_entry_support_symmetry_breaking(
    cnf,
    system: EquationSystem,
    transforms: list[
        tuple[tuple[int, ...], tuple[int, ...]]
    ],
) -> int:
    """Keep supports lexicographically minimal under the given relabelings.

    Entry-support variables are the first ``system.variable_count`` variables
    of every global support encoding.  Requiring ``x <=lex g(x)`` for a set
    of group elements is sound: the globally least support in every full
    symmetry orbit satisfies every such comparison.  Generator comparisons
    are deliberately used as a compact, safe symmetry breaker; they need not
    define a unique representative.
    """
    identity = (tuple(range(6)), tuple(range(3)))
    before = len(cnf.clauses)
    entries = list(range(1, system.variable_count + 1))
    for vertex_permutation, colour_permutation in transforms:
        if (vertex_permutation, colour_permutation) == identity:
            continue
        transformed = [
            transform_flat_entry(
                system,
                flat_index,
                vertex_permutation,
                colour_permutation,
            )
            + 1
            for flat_index in range(system.variable_count)
        ]
        add_lex_leq(cnf, entries, transformed)
    return len(cnf.clauses) - before


def symmetry_blocking_clauses(
    system: EquationSystem,
    candidates: dict[tuple[int, int, int], int],
    candidate_arcs: set[tuple[int, int, int]],
    positive: set[int],
    negative: set[int],
    transforms: list[
        tuple[tuple[int, ...], tuple[int, ...]]
    ],
) -> set[tuple[int, ...]]:
    """Return every requested symmetry image of a learned conflict clause."""
    clauses: set[tuple[int, ...]] = set()
    for vertex_permutation, colour_permutation in transforms:
        transformed_arcs = sorted(
            (
                vertex_permutation[vertex],
                colour_permutation[colour],
                vertex_permutation[neighbour],
            )
            for vertex, colour, neighbour in candidate_arcs
        )
        transformed_positive = sorted(
            transform_flat_entry(
                system,
                flat_index,
                vertex_permutation,
                colour_permutation,
            )
            for flat_index in positive
        )
        transformed_negative = sorted(
            transform_flat_entry(
                system,
                flat_index,
                vertex_permutation,
                colour_permutation,
            )
            for flat_index in negative
        )
        clauses.add(
            tuple(
                [
                    *(-candidates[arc] for arc in transformed_arcs),
                    *(-(flat_index + 1) for flat_index in transformed_positive),
                    *((flat_index + 1) for flat_index in transformed_negative),
                ]
            )
        )
    return clauses


def minimum_candidate_pattern(
    model: set[int],
    candidates: dict[tuple[int, int, int], int],
) -> tuple[list[list[int]], set[tuple[int, int]]]:
    """Choose a minimum-edge arc cover via task compatibility matching.

    Two selected arcs share an undirected edge exactly when they are
    oppositely directed candidates for two distinct tasks.  Such shared
    pairs form a matching on the 18 ``(vertex, colour)`` tasks.  Conversely,
    every compatibility matching can be selected simultaneously, after
    which each unmatched task chooses an arbitrary candidate.  Hence the
    minimum cover size is ``18 - maximum_matching_size``.
    """
    tasks = tuple(
        (vertex, colour)
        for vertex in range(6)
        for colour in range(3)
    )
    choices = {
        task: tuple(
            neighbour
            for neighbour in range(6)
            if neighbour != task[0]
            and candidates[(task[0], task[1], neighbour)] in model
        )
        for task in tasks
    }
    if any(not neighbours for neighbours in choices.values()):
        raise ValueError("candidate model leaves a killer task uncovered")
    task_index = {task: index for index, task in enumerate(tasks)}
    compatibility: list[set[int]] = [set() for _ in tasks]
    for first_index, (vertex, colour) in enumerate(tasks):
        for neighbour in choices[(vertex, colour)]:
            for neighbour_colour in range(3):
                second = (neighbour, neighbour_colour)
                if vertex not in choices[second]:
                    continue
                second_index = task_index[second]
                compatibility[first_index].add(second_index)
                compatibility[second_index].add(first_index)

    @lru_cache(maxsize=None)
    def maximum_matching(mask: int) -> tuple[tuple[int, int], ...]:
        if not mask:
            return ()
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        without_first = mask ^ first_bit
        best = maximum_matching(without_first)
        for second in sorted(compatibility[first]):
            second_bit = 1 << second
            if not without_first & second_bit:
                continue
            rest = maximum_matching(without_first ^ second_bit)
            candidate = ((first, second), *rest)
            if len(candidate) > len(best):
                best = candidate
        return best

    matching = maximum_matching((1 << len(tasks)) - 1)
    selected: dict[tuple[int, int], int] = {}
    for first_index, second_index in matching:
        first_vertex, first_colour = tasks[first_index]
        second_vertex, second_colour = tasks[second_index]
        selected[(first_vertex, first_colour)] = second_vertex
        selected[(second_vertex, second_colour)] = first_vertex
    for task in tasks:
        if task not in selected:
            selected[task] = min(choices[task])

    pattern: list[list[int]] = []
    for vertex in range(6):
        row = [selected[(vertex, colour)] for colour in range(3)]
        if len(set(row)) != 3:
            raise AssertionError(
                "distinct killer colours selected the same neighbour"
            )
        pattern.append(row)
    cover = {
        tuple(sorted((vertex, pattern[vertex][colour])))
        for vertex in range(6)
        for colour in range(3)
    }
    expected_size = len(tasks) - len(matching)
    if len(cover) != expected_size:
        raise AssertionError(
            "matching/cover identity failed: "
            f"matching={len(matching)}, cover={len(cover)}"
        )
    return pattern, cover


def laurent_conflict_cube(
    system: EquationSystem,
    pattern: list[list[int]],
    nonzero_flat_entries: set[int],
) -> tuple[
    set[int],
    set[int],
    dict[str, object],
    list[str],
    list[Counter],
    list,
    list[tuple[int, ...]],
    dict[str, int],
    set[str],
    set[int],
]:
    (
        names,
        equations,
        variable_names,
        equation_colourings,
    ) = union_orbit_equations_with_colourings(system, pattern)
    nonzero_names = {
        name
        for flat_index, name in variable_names.items()
        if flat_index in nonzero_flat_entries
    }
    restricted = []
    sources = []
    for equation_index, equation in enumerate(equations):
        surviving = type(equation)(
            {
                monomial: coefficient
                for monomial, coefficient in equation.items()
                if all(variable in nonzero_names for variable in monomial)
            }
        )
        surviving = clean_polynomial(surviving)
        if surviving:
            restricted.append(surviving)
            sources.append(equation_index)
    active_names = [name for name in names if name in nonzero_names]
    reduced_names, reduced, metadata = primitive_binomial_reduction(
        restricted, active_names
    )
    unit_indices = metadata["unit_equation_indices"]
    if not unit_indices:
        return (
            set(),
            set(),
            metadata,
            reduced_names,
            reduced,
            equations,
            equation_colourings,
            {
                name: flat_index
                for flat_index, name in variable_names.items()
            },
            nonzero_names,
            set(),
        )
    used_equations = {
        sources[index]
        for index in [
            *metadata["unit_basis_equation_indices"][
                str(unit_indices[0])
            ],
            unit_indices[0],
        ]
    }
    name_to_flat = {
        name: flat_index
        for flat_index, name in variable_names.items()
    }
    positive: set[int] = set()
    negative: set[int] = set()
    for equation_index in used_equations:
        for monomial, coefficient in equations[equation_index].items():
            if not coefficient:
                continue
            zero_factors = [
                variable
                for variable in monomial
                if variable not in nonzero_names
            ]
            if zero_factors:
                negative.add(name_to_flat[zero_factors[0]])
            else:
                positive.update(
                    name_to_flat[variable] for variable in monomial
                )

    if positive & negative:
        raise AssertionError("global conflict cube is inconsistent")
    return (
        positive,
        negative,
        metadata,
        reduced_names,
        reduced,
        equations,
        equation_colourings,
        name_to_flat,
        nonzero_names,
        used_equations,
    )


def required_candidate_arcs(
    system: EquationSystem,
    pattern: list[list[int]],
    equation_colourings: list[tuple[int, ...]],
    used_equations: set[int],
) -> set[tuple[int, int, int]]:
    fixed, active = normalized_union_stratum(system, pattern)
    mandatory: set[tuple[int, int, int]] = set()
    killing_requirements: list[set[tuple[int, int, int]]] = []
    for equation_index in used_equations:
        colouring = equation_colourings[equation_index]
        for matching in system.matchings:
            flat_indices = [
                system.edge_index[edge] * 9
                + 3 * colouring[edge[0]]
                + colouring[edge[1]]
                for edge in matching
            ]
            if all(
                active[flat_index] or fixed[flat_index] != 0
                for flat_index in flat_indices
            ):
                for edge, flat_index in zip(matching, flat_indices):
                    if fixed[flat_index] == 0:
                        continue
                    first, second = edge
                    first_colours = [
                        colour
                        for colour, neighbour in enumerate(pattern[first])
                        if neighbour == second
                    ]
                    second_colours = [
                        colour
                        for colour, neighbour in enumerate(pattern[second])
                        if neighbour == first
                    ]
                    mandatory.add(
                        (first, first_colours[0], second)
                    )
                    mandatory.add(
                        (second, second_colours[0], first)
                    )
                continue
            killing_arcs: list[tuple[int, int, int]] = []
            for edge, flat_index in zip(matching, flat_indices):
                if active[flat_index] or fixed[flat_index] != 0:
                    continue
                first, second = edge
                for colour, neighbour in enumerate(pattern[first]):
                    if (
                        neighbour == second
                        and colouring[second] != colour
                    ):
                        killing_arcs.append((first, colour, second))
                for colour, neighbour in enumerate(pattern[second]):
                    if (
                        neighbour == first
                        and colouring[first] != colour
                    ):
                        killing_arcs.append((second, colour, first))
            if not killing_arcs:
                raise AssertionError(
                    "structurally absent matching has no killing arc"
                )
            killing_requirements.append(set(killing_arcs))

    required = set(mandatory)
    remaining = [
        requirement
        for requirement in killing_requirements
        if not requirement & required
    ]
    while remaining:
        candidates = set().union(*remaining)
        best = min(
            candidates,
            key=lambda arc: (
                -sum(arc in requirement for requirement in remaining),
                arc,
            ),
        )
        required.add(best)
        remaining = [
            requirement
            for requirement in remaining
            if best not in requirement
        ]
    # Delete any non-mandatory arc that became redundant after greedy choices.
    for arc in sorted(required - mandatory, reverse=True):
        trial = required - {arc}
        if all(requirement & trial for requirement in killing_requirements):
            required = trial
    return required


def exact_torus_unit(
    reduced_names: list[str],
    reduced: list[Counter],
    directory: Path,
    iteration: int,
) -> bool:
    directory.mkdir(parents=True, exist_ok=True)
    program = exact_torus_program(reduced_names, reduced)
    singular_path = directory / f"fallback_{iteration}_q.sing"
    log_path = directory / f"fallback_{iteration}_q.log"
    error_path = directory / f"fallback_{iteration}_q.err.log"
    singular_path.write_text(program, encoding="utf-8")
    completed = subprocess.run(
        [
            "wsl",
            "-d",
            "Ubuntu",
            "--",
            "Singular",
            windows_to_wsl(singular_path),
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    log_path.write_text(completed.stdout, encoding="utf-8")
    error_path.write_text(completed.stderr, encoding="utf-8")
    return (
        completed.returncode == 0
        and is_exact_unit_log(completed.stdout)
    )


def exact_torus_program(
    reduced_names: list[str],
    reduced: list[Counter],
) -> str:
    """Return the characteristic-zero torus-saturation program."""
    saturation_variable = "sat"
    saturation_equation = Counter(
        {
            tuple(sorted([*reduced_names, saturation_variable])): 1,
            (): -1,
        }
    )
    names = [*reduced_names, saturation_variable]
    equations = [*reduced, saturation_equation]
    return singular_program(
        -1,
        names,
        equations,
        0,
        "full",
        "slimgb",
    )


def full_equation_support_cube(
    equations,
    name_to_flat: dict[str, int],
    nonzero_names: set[str],
) -> tuple[set[int], set[int]]:
    positive: set[int] = set()
    negative: set[int] = set()
    for equation in equations:
        for monomial, coefficient in equation.items():
            if not coefficient:
                continue
            zero_factors = [
                variable
                for variable in monomial
                if variable not in nonzero_names
            ]
            if zero_factors:
                negative.add(name_to_flat[zero_factors[0]])
            else:
                positive.update(
                    name_to_flat[variable] for variable in monomial
                )
    if positive & negative:
        raise AssertionError("full support cube is inconsistent")
    return positive, negative


def result_payload(
    status: str,
    rows: list[dict[str, object]],
    symmetry_images: str,
) -> dict[str, object]:
    cover_sizes = sorted(
        {
            int(row["cover_size"])
            for row in rows
            if "cover_size" in row
        }
    )
    return {
        "status": status,
        "iterations": len(rows),
        "symmetry_images": symmetry_images,
        "cover_size_counts": {
            str(size): sum(
                row.get("cover_size") == size for row in rows
            )
            for size in cover_sizes
        },
        "rows": rows,
    }


def write_result(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-iterations", type=int, default=10_000)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--fallback-directory",
        type=Path,
        default=Path("tmp/global_candidate_fallback"),
    )
    parser.add_argument("--resume", type=Path)
    parser.add_argument(
        "--symmetry-images",
        choices=("none", "generators", "full"),
        default="none",
    )
    parser.add_argument(
        "--solver",
        choices=(
            "cadical195",
            "glucose42",
            "maplechrono",
            "mergesat3",
            "minisat22",
        ),
        default="cadical195",
    )
    parser.add_argument("--checkpoint-every", type=int, default=25)
    args = parser.parse_args()

    from pysat.solvers import Solver

    system = EquationSystem(6, 3)
    cnf = candidate_cover_cnf(10)
    candidates = candidate_variable_map()
    transforms = symmetry_transforms(args.symmetry_images)
    rows = []
    if args.resume:
        previous = json.loads(args.resume.read_text(encoding="utf-8"))
        previous_symmetry = str(
            previous.get("symmetry_images", "none")
        )
        if previous_symmetry != args.symmetry_images:
            raise ValueError(
                "resume symmetry mode differs from the manifest: "
                f"{previous_symmetry} != {args.symmetry_images}"
            )
        rows = [
            row
            for row in previous["rows"]
            if "cover_size" in row
        ]
    final_status = "limit"
    with Solver(
        name=args.solver,
        bootstrap_with=cnf.clauses,
    ) as solver:
        for row in rows:
            if "candidate_arcs" in row:
                replay_arcs = [
                    tuple(int(value) for value in arc)
                    for arc in row["candidate_arcs"]
                ]
            else:
                replay_arcs = [
                    (vertex, colour, neighbour)
                    for vertex, pattern_row in enumerate(row["pattern"])
                    for colour, neighbour in enumerate(pattern_row)
                ]
            replay_clauses = symmetry_blocking_clauses(
                system,
                candidates,
                set(replay_arcs),
                {
                    int(flat_index)
                    for flat_index in row["positive_entries"]
                },
                {
                    int(flat_index)
                    for flat_index in row["negative_entries"]
                },
                transforms,
            )
            for replay_clause in replay_clauses:
                solver.add_clause(replay_clause)
        for iteration in range(len(rows), args.max_iterations):
            if not solver.solve():
                final_status = "certified"
                break
            model = set(solver.get_model() or ())
            nonzero_flat_entries = {
                flat_index
                for flat_index in range(system.variable_count)
                if flat_index + 1 in model
            }
            pattern, cover = minimum_candidate_pattern(
                model, candidates
            )
            (
                positive,
                negative,
                metadata,
                reduced_names,
                reduced,
                equations,
                equation_colourings,
                name_to_flat,
                nonzero_names,
                used_equations,
            ) = laurent_conflict_cube(
                system, pattern, nonzero_flat_entries
            )
            used_fallback = False
            if not metadata["unit_equation_indices"]:
                used_fallback = True
                if not exact_torus_unit(
                    reduced_names,
                    reduced,
                    args.fallback_directory,
                    iteration,
                ):
                    final_status = "algebraic_survivor"
                    rows.append(
                        {
                            "iteration": iteration,
                            "pattern": pattern,
                            "nonzero_flat_entries": sorted(
                                nonzero_flat_entries
                            ),
                            "metadata": metadata,
                        }
                    )
                    break
                positive, negative = full_equation_support_cube(
                    equations, name_to_flat, nonzero_names
                )
                used_equations = set(range(len(equations)))
            candidate_arcs = required_candidate_arcs(
                system,
                pattern,
                equation_colourings,
                used_equations,
            )
            blocking_clauses = symmetry_blocking_clauses(
                system,
                candidates,
                candidate_arcs,
                positive,
                negative,
                transforms,
            )
            for blocking_clause in blocking_clauses:
                solver.add_clause(blocking_clause)
            rows.append(
                {
                    "iteration": iteration,
                    "cover_size": len(cover),
                    "cover_complement": [
                        list(edge)
                        for edge in system.edges
                        if edge not in cover
                    ],
                    "positive_cube_size": len(positive),
                    "negative_cube_size": len(negative),
                    "positive_entries": sorted(positive),
                    "negative_entries": sorted(negative),
                    "pattern": pattern,
                    "candidate_arcs": [
                        list(arc) for arc in sorted(candidate_arcs)
                    ],
                    "candidate_arc_count": len(candidate_arcs),
                    "symmetry_clause_count": len(blocking_clauses),
                    "binomial_rank": metadata["binomial_rank"],
                    "unit_equations": len(
                        metadata["unit_equation_indices"]
                    ),
                    "used_grobner_fallback": used_fallback,
                }
            )
            if (
                args.output
                and args.checkpoint_every > 0
                and len(rows) % args.checkpoint_every == 0
            ):
                write_result(
                    args.output,
                    result_payload(
                        "running",
                        rows,
                        args.symmetry_images,
                    ),
                )
                print(
                    f"checkpoint {args.output}: "
                    f"iterations={len(rows)}",
                    flush=True,
                )
    result = result_payload(
        final_status,
        rows,
        args.symmetry_images,
    )
    text = json.dumps(result, indent=2)
    if args.output:
        write_result(args.output, result)
        print(
            f"wrote {args.output}: status={final_status} "
            f"iterations={len(rows)}"
        )
    else:
        print(text)
    if final_status != "certified":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
