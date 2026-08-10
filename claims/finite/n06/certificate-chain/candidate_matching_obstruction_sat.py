"""Tutte-Berge SAT certificates for the global twelve-edge cover bound.

The 18 killer tasks are the pairs ``(vertex, colour)``.  Two tasks are
compatible when they have opposite eligible arcs on the same undirected
edge.  The minimum number of edges needed to cover all tasks is exactly
``18 - nu``, where ``nu`` is the maximum matching size of this compatibility
graph.

By the Tutte-Berge formula, ``nu <= 5`` iff some set ``S`` has at least
``|S| + 8`` odd components after deletion.  It is enough to existentially
encode that many pairwise isolated odd vertex groups; connectivity inside a
group is unnecessary, because an odd union of components contains an odd
component.  Since there are 18 task vertices, only ``|S| = 0..5`` can occur.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

from candidate_killer_cover_sat import candidate_support_problem
from rankone_support_sat import CNF


Task = tuple[int, int]


def odd_group_size_patterns(
    separator_size: int,
    maximum_matching: int = 5,
) -> list[tuple[int, ...]]:
    """List all possible sorted odd sizes for a Tutte obstruction."""
    if not 0 <= maximum_matching <= 9:
        raise ValueError("maximum_matching must lie in 0..9")
    if not 0 <= separator_size <= maximum_matching:
        raise ValueError(
            "separator_size must lie in 0..maximum_matching"
        )
    deficiency = 18 - 2 * maximum_matching
    group_count = separator_size + deficiency
    extra_budget = maximum_matching - separator_size
    patterns = {
        tuple(1 + 2 * extra for extra in extras)
        for extras in itertools.combinations_with_replacement(
            range(extra_budget + 1),
            group_count,
        )
        if sum(extras) <= extra_budget
    }
    return sorted(patterns, key=lambda pattern: (sum(pattern), pattern))


def separator_orbit_representatives(
    size: int,
) -> list[tuple[int, ...]]:
    """Return row-mask representatives modulo S6 vertices and S3 colours."""
    if not 0 <= size <= 18:
        raise ValueError("separator size must lie in 0..18")

    def permute_mask(
        mask: int,
        colour_permutation: tuple[int, ...],
    ) -> int:
        output = 0
        for colour in range(3):
            if mask & (1 << colour):
                output |= 1 << colour_permutation[colour]
        return output

    representatives: set[tuple[int, ...]] = set()
    for row_masks in itertools.combinations_with_replacement(range(8), 6):
        if sum(mask.bit_count() for mask in row_masks) != size:
            continue
        representatives.add(
            min(
                tuple(
                    sorted(
                        permute_mask(mask, colour_permutation)
                        for mask in row_masks
                    )
                )
                for colour_permutation in itertools.permutations(range(3))
            )
        )
    return sorted(representatives)


def fixed_separator_cnf(
    row_masks: tuple[int, ...],
) -> tuple[CNF, dict[str, object]]:
    """Require the fixed task set to cover every compatibility edge."""
    if len(row_masks) != 6 or any(not 0 <= mask < 8 for mask in row_masks):
        raise ValueError("row_masks must contain six three-bit masks")
    cnf, candidates = candidate_support_problem()
    tasks: tuple[Task, ...] = tuple(
        (vertex, colour)
        for vertex in range(6)
        for colour in range(3)
    )
    separator = {
        (vertex, colour)
        for vertex, mask in enumerate(row_masks)
        for colour in range(3)
        if mask & (1 << colour)
    }
    for first_index, (first_vertex, first_colour) in enumerate(tasks):
        if (first_vertex, first_colour) in separator:
            continue
        for second_vertex, second_colour in tasks[first_index + 1 :]:
            if (
                first_vertex == second_vertex
                or (second_vertex, second_colour) in separator
            ):
                continue
            cnf.add(
                -candidates[
                    (first_vertex, first_colour, second_vertex)
                ],
                -candidates[
                    (second_vertex, second_colour, first_vertex)
                ],
            )
    return cnf, {
        "row_masks": list(row_masks),
        "separator_tasks": [
            list(task) for task in sorted(separator)
        ],
        "separator_size": len(separator),
    }


def add_cardinality_equals(
    cnf: CNF,
    literals: list[int],
    bound: int,
) -> None:
    from pysat.card import CardEnc, EncType

    encoded = CardEnc.equals(
        lits=literals,
        bound=bound,
        top_id=cnf.variable_count,
        encoding=EncType.seqcounter,
    )
    cnf.variable_count = max(cnf.variable_count, encoded.nv)
    cnf.clauses.extend(tuple(clause) for clause in encoded.clauses)


def add_xor(
    cnf: CNF,
    first: int,
    second: int,
) -> int:
    """Add ``output <-> first xor second`` and return output."""
    output = cnf.variable()
    cnf.add(-first, -second, -output)
    cnf.add(first, second, -output)
    cnf.add(first, -second, output)
    cnf.add(-first, second, output)
    return output


def require_odd(cnf: CNF, literals: list[int]) -> None:
    parity = literals[0]
    for literal in literals[1:]:
        parity = add_xor(cnf, parity, literal)
    cnf.add(parity)


def add_lex_leq(
    cnf: CNF,
    first: list[int],
    second: list[int],
) -> None:
    """Constrain one equal-length Boolean vector to be lexicographically <=."""
    if len(first) != len(second) or not first:
        raise ValueError("lexicographic vectors must be nonempty and equal")
    prefix_equal: int | None = None
    for index, (left, right) in enumerate(zip(first, second)):
        if prefix_equal is None:
            cnf.add(-left, right)
        else:
            cnf.add(-prefix_equal, -left, right)
        if index == len(first) - 1:
            continue
        next_equal = cnf.variable()
        if prefix_equal is not None:
            cnf.add(-next_equal, prefix_equal)
        cnf.add(-next_equal, -left, right)
        cnf.add(-next_equal, left, -right)
        if prefix_equal is None:
            cnf.add(left, right, next_equal)
            cnf.add(-left, -right, next_equal)
        else:
            cnf.add(-prefix_equal, left, right, next_equal)
            cnf.add(-prefix_equal, -left, -right, next_equal)
        prefix_equal = next_equal


def matching_obstruction_cnf(
    separator_size: int,
    group_sizes: tuple[int, ...] | None = None,
    maximum_matching: int = 5,
) -> tuple[CNF, dict[str, object]]:
    if not 0 <= separator_size <= maximum_matching <= 9:
        raise ValueError(
            "require 0 <= separator_size <= maximum_matching <= 9"
        )
    cnf, candidates = candidate_support_problem()
    tasks: tuple[Task, ...] = tuple(
        (vertex, colour)
        for vertex in range(6)
        for colour in range(3)
    )
    metadata = add_matching_obstruction(
        cnf,
        candidates,
        tasks,
        separator_size,
        group_sizes,
        maximum_matching,
    )
    return cnf, metadata


def add_matching_obstruction(
    cnf: CNF,
    candidates: dict[tuple[int, int, int], int],
    tasks: tuple[Task, ...],
    separator_size: int,
    group_sizes: tuple[int, ...] | None = None,
    maximum_matching: int = 5,
) -> dict[str, object]:
    """Add an exact Tutte-Berge upper-bound witness for matching number."""
    if len(tasks) != 18:
        raise ValueError("the obstruction encoding expects exactly 18 tasks")
    if not 0 <= separator_size <= maximum_matching <= 9:
        raise ValueError(
            "require 0 <= separator_size <= maximum_matching <= 9"
        )
    deficiency = len(tasks) - 2 * maximum_matching
    group_count = separator_size + deficiency
    if group_sizes is not None:
        if len(group_sizes) != group_count:
            raise ValueError(
                f"expected {group_count} group sizes, got {len(group_sizes)}"
            )
        if any(size <= 0 or size % 2 == 0 for size in group_sizes):
            raise ValueError("every fixed group size must be positive and odd")
        if sum(group_sizes) > len(tasks) - separator_size:
            raise ValueError("fixed groups do not fit outside the separator")
        if tuple(sorted(group_sizes)) != group_sizes:
            raise ValueError("fixed group sizes must be nondecreasing")
    separator = [cnf.variable() for _ in tasks]
    add_cardinality_equals(cnf, separator, separator_size)
    non_singleton_sizes = (
        [size for size in group_sizes if size > 1]
        if group_sizes is not None
        else []
    )
    leftover_size = (
        len(tasks) - separator_size - sum(group_sizes)
        if group_sizes is not None
        else -1
    )
    special_size: int | None = None
    special_label: str | None = None
    if group_sizes is not None and not non_singleton_sizes:
        special_size = leftover_size
        special_label = "unselected_remainder"
    elif (
        group_sizes is not None
        and len(non_singleton_sizes) == 1
        and leftover_size == 0
    ):
        special_size = non_singleton_sizes[0]
        special_label = "unique_nonsingleton_group"
    if special_size is not None:
        special = [cnf.variable() for _ in tasks] if special_size else []
        if special:
            add_cardinality_equals(cnf, special, special_size)
            for task_index in range(len(tasks)):
                cnf.add(-separator[task_index], -special[task_index])
            for vertex in range(5):
                first_row = [
                    literal
                    for colour in range(3)
                    for literal in (
                        separator[3 * vertex + colour],
                        special[3 * vertex + colour],
                    )
                ]
                second_row = [
                    literal
                    for colour in range(3)
                    for literal in (
                        separator[3 * (vertex + 1) + colour],
                        special[3 * (vertex + 1) + colour],
                    )
                ]
                add_lex_leq(cnf, first_row, second_row)
            # A lexicographically least matrix in every S6 x S3 orbit has
            # both its category rows and its category columns ordered.
            for colour in range(2):
                first_column = [
                    literal
                    for vertex in range(6)
                    for literal in (
                        separator[3 * vertex + colour],
                        special[3 * vertex + colour],
                    )
                ]
                second_column = [
                    literal
                    for vertex in range(6)
                    for literal in (
                        separator[3 * vertex + colour + 1],
                        special[3 * vertex + colour + 1],
                    )
                ]
                add_lex_leq(cnf, first_column, second_column)
        for first_index, (first_vertex, first_colour) in enumerate(tasks):
            for second_index in range(first_index + 1, len(tasks)):
                second_vertex, second_colour = tasks[second_index]
                if first_vertex == second_vertex:
                    continue
                edge_prefix = (
                    -candidates[
                        (first_vertex, first_colour, second_vertex)
                    ],
                    -candidates[
                        (second_vertex, second_colour, first_vertex)
                    ],
                    separator[first_index],
                    separator[second_index],
                )
                if special:
                    cnf.add(*edge_prefix, special[first_index])
                    cnf.add(*edge_prefix, special[second_index])
                else:
                    cnf.add(*edge_prefix)
        return {
            "separator_size": separator_size,
            "maximum_matching": maximum_matching,
            "odd_groups": group_count,
            "group_sizes": list(group_sizes),
            "tasks": [list(task) for task in tasks],
            "separator_variables": separator,
            "group_variables": [],
            "special_variables": special,
            "simplification": (
                "compatibility_vertex_cover"
                if special_size == 0
                else f"edge_containment_{special_label}"
            ),
        }

    groups = [
        [cnf.variable() for _ in range(group_count)]
        for _ in tasks
    ]

    for task_index in range(len(tasks)):
        for group in range(group_count):
            cnf.add(-separator[task_index], -groups[task_index][group])
            for other_group in range(group):
                cnf.add(
                    -groups[task_index][group],
                    -groups[task_index][other_group],
                )

    for group in range(group_count):
        group_literals = [
            groups[task_index][group]
            for task_index in range(len(tasks))
        ]
        if group_sizes is None:
            require_odd(cnf, group_literals)
        else:
            add_cardinality_equals(
                cnf,
                group_literals,
                group_sizes[group],
            )
        # Restricted-growth labels remove the otherwise dominant group
        # permutation symmetry.
        for task_index in range(len(tasks)):
            if group == 0:
                continue
            if (
                group_sizes is not None
                and group_sizes[group] != group_sizes[group - 1]
            ):
                continue
            cnf.add(
                -groups[task_index][group],
                *(
                    groups[earlier][group - 1]
                    for earlier in range(task_index)
                ),
            )

    for first_index, (first_vertex, first_colour) in enumerate(tasks):
        for second_index in range(first_index + 1, len(tasks)):
            second_vertex, second_colour = tasks[second_index]
            if first_vertex == second_vertex:
                continue
            first_arc = candidates[
                (first_vertex, first_colour, second_vertex)
            ]
            second_arc = candidates[
                (second_vertex, second_colour, first_vertex)
            ]
            for group in range(group_count):
                # A compatibility edge may remain inside a group or cross
                # into S, but it may not reach any other or unassigned task.
                cnf.add(
                    -first_arc,
                    -second_arc,
                    -groups[first_index][group],
                    separator[second_index],
                    groups[second_index][group],
                )
                cnf.add(
                    -first_arc,
                    -second_arc,
                    -groups[second_index][group],
                    separator[first_index],
                    groups[first_index][group],
                )

    metadata: dict[str, object] = {
        "separator_size": separator_size,
        "maximum_matching": maximum_matching,
        "odd_groups": group_count,
        "group_sizes": list(group_sizes) if group_sizes is not None else None,
        "tasks": [list(task) for task in tasks],
        "separator_variables": separator,
        "group_variables": groups,
        "simplification": None,
    }
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--separator-size", type=int, required=True)
    parser.add_argument("--maximum-matching", type=int, default=5)
    parser.add_argument(
        "--group-sizes",
        help="comma-separated fixed odd sizes for the isolated groups",
    )
    parser.add_argument(
        "--solver",
        choices=(
            "cadical195",
            "glucose42",
            "lingeling",
            "maplechrono",
            "mergesat3",
            "minisat22",
        ),
        default="cadical195",
    )
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    from pysat.solvers import Solver

    group_sizes = (
        tuple(int(token) for token in args.group_sizes.split(","))
        if args.group_sizes
        else None
    )
    cnf, metadata = matching_obstruction_cnf(
        args.separator_size,
        group_sizes,
        args.maximum_matching,
    )
    if args.cnf:
        args.cnf.parent.mkdir(parents=True, exist_ok=True)
        cnf.write_dimacs(args.cnf)
    started = time.perf_counter()
    with Solver(
        name=args.solver,
        bootstrap_with=cnf.clauses,
    ) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None
        try:
            statistics = solver.accum_stats()
        except NotImplementedError:
            statistics = None
    elapsed_seconds = time.perf_counter() - started
    result = {
        "status": "SAT" if sat else "UNSAT",
        "solver": args.solver,
        "variables": cnf.variable_count,
        "clauses": len(cnf.clauses),
        "separator_size": args.separator_size,
        "maximum_matching": args.maximum_matching,
        "odd_groups": metadata["odd_groups"],
        "group_sizes": metadata["group_sizes"],
        "model": model,
        "statistics": statistics,
        "elapsed_seconds": elapsed_seconds,
    }
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
        print(
            f"wrote {args.output}: status={result['status']} "
            f"variables={cnf.variable_count} clauses={len(cnf.clauses)}"
        )
    else:
        print(text)


if __name__ == "__main__":
    main()
