"""Universal n=8 support screen for a vertex of skeleton degree four.

By vertex and colour symmetry, a hypothetical witness with a degree-four
vertex can be labelled so that vertex 0 has neighbours 1,2,3,4 and the
degree-four singleton theorem supplies

    W_01 = alpha * e_0 outer(e_0),  alpha != 0.

All blocks among vertices 1..7 remain optional and unrestricted.  An
optional minimum-degree restriction can be added as a separate, explicitly
labelled hypothesis.  The amplitude clauses are support-level necessary
conditions only.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.rankone_support_sat import (
    CNF,
    matching_indicator,
    solve_with_cadical,
)
from krenn_gu.search_witness import perfect_matchings

Edge = tuple[int, int]


def add_at_most(cnf: CNF, literals: list[int], bound: int) -> None:
    """Add the Sinz sequential-counter encoding of ``sum(literals) <= bound``."""

    count = len(literals)
    if bound < 0:
        cnf.add()
        return
    if bound >= count:
        return
    if bound == 0:
        for literal in literals:
            cnf.add(-literal)
        return

    sequential = [
        [cnf.variable() for _ in range(bound)]
        for _ in range(count - 1)
    ]
    cnf.add(-literals[0], sequential[0][0])
    for threshold in range(1, bound):
        cnf.add(-sequential[0][threshold])
    for index in range(1, count):
        cnf.add(
            -literals[index],
            -sequential[index - 1][bound - 1],
        )
        if index == count - 1:
            continue
        cnf.add(-literals[index], sequential[index][0])
        cnf.add(-sequential[index - 1][0], sequential[index][0])
        for threshold in range(1, bound):
            cnf.add(
                -literals[index],
                -sequential[index - 1][threshold - 1],
                sequential[index][threshold],
            )
            cnf.add(
                -sequential[index - 1][threshold],
                sequential[index][threshold],
            )


def local_degree_four_cnf(
    n: int = 8,
    d: int = 3,
    minimum_degree: int = 0,
    maximum_edges: int | None = None,
    center_degree: int = 4,
    degree_five_plane: bool = False,
) -> tuple[CNF, dict[str, int]]:
    if (n, d) != (8, 3):
        raise ValueError("this screen is fixed at n=8, d=3")
    if not 0 <= minimum_degree <= 7:
        raise ValueError("minimum_degree must be between zero and seven")
    if center_degree not in (0, 1, 3, 4):
        raise ValueError(
            "center_degree must be zero, one, three, or four"
        )
    neighbours_of_zero = (
        set(range(1, n))
        if center_degree in (0, 1)
        else set(range(1, center_degree + 1))
    )
    allowed_edges = tuple(
        edge
        for edge in itertools.combinations(range(n), 2)
        if edge[0] != 0 or edge[1] in neighbours_of_zero
    )
    cnf = CNF()
    entries = {
        (first, second, row, column): cnf.variable()
        for first, second in allowed_edges
        for row in range(d)
        for column in range(d)
    }

    def entry(
        first: int,
        second: int,
        first_colour: int,
        second_colour: int,
    ) -> int:
        if first < second:
            key = (first, second, first_colour, second_colour)
        else:
            key = (second, first, second_colour, first_colour)
        return entries[key]

    neighbours = {vertex: [] for vertex in range(n)}
    for first, second in allowed_edges:
        neighbours[first].append(second)
        neighbours[second].append(first)

    blocks: dict[Edge, int] = {}
    for first, second in allowed_edges:
        block = cnf.variable()
        blocks[first, second] = block
        block_entries = [
            entries[first, second, row, column]
            for row in range(d)
            for column in range(d)
        ]
        cnf.add(-block, *block_entries)
        for literal in block_entries:
            cnf.add(-literal, block)

    if maximum_edges is not None:
        if maximum_edges < 0:
            raise ValueError("maximum_edges must be nonnegative")
        add_at_most(cnf, list(blocks.values()), maximum_edges)

    # The prescribed incident skeleton blocks are nonzero; the other pairs
    # at vertex 0 are absent because no variables were created for them.
    if center_degree in (3, 4):
        for neighbour in sorted(neighbours_of_zero):
            cnf.add(blocks[0, neighbour])

    # At degree three the singleton-star theorem fixes all three incident
    # blocks.  At degree four, use vertex and global-colour symmetry to fix
    # the guaranteed singleton and select the other two generic killers.
    fixed_killers = {
        0: (),
        1: (),
        3: ((1, 0), (2, 1), (3, 2)),
        4: ((1, 0),),
    }[center_degree]
    for neighbour, colour in fixed_killers:
        for row in range(d):
            for column in range(d):
                if (row, column) == (colour, colour):
                    cnf.add(entry(0, neighbour, row, column))
                else:
                    cnf.add(-entry(0, neighbour, row, column))

    if center_degree == 4:
        # The singleton is an eligible colour-0 killer.  The other two
        # killer neighbours are distinct, so neighbour symmetry among
        # 2,3,4 lets us select 2 for colour 1 and 3 for colour 2.
        for neighbour, colour in ((2, 1), (3, 2)):
            cnf.add(
                *(
                    entry(0, neighbour, row, colour)
                    for row in range(d)
                )
            )
            for row in range(d):
                for column in range(d):
                    if column != colour:
                        cnf.add(
                            -entry(
                                0, neighbour, row, column
                            )
                        )

        # Degree-four relation (4) from the analytic proof.  If the v-side
        # vector a_c of a selected killer a_c outer(e_c) is non-coordinate,
        # then every spare-block column j != c is proportional to a_c.  At
        # support level, a nonzero proportional column has exactly the
        # support of a_c (a zero column is also allowed).
        for killer_neighbour, colour in ((2, 1), (3, 2)):
            off_coordinate = [
                entry(0, killer_neighbour, row, colour)
                for row in range(d)
                if row != colour
            ]
            non_coordinate = cnf.variable()
            cnf.add(-non_coordinate, *off_coordinate)
            for literal in off_coordinate:
                cnf.add(-literal, non_coordinate)
            killer_vector = [
                entry(0, killer_neighbour, row, colour)
                for row in range(d)
            ]
            for spare_colour in range(d):
                if spare_colour == colour:
                    continue
                spare_column = [
                    entry(0, 4, row, spare_colour)
                    for row in range(d)
                ]
                for witness in spare_column:
                    for killer_entry, spare_entry in zip(
                        killer_vector, spare_column, strict=True
                    ):
                        cnf.add(
                            -non_coordinate,
                            -witness,
                            -killer_entry,
                            spare_entry,
                        )
                        cnf.add(
                            -non_coordinate,
                            -witness,
                            -spare_entry,
                            killer_entry,
                        )

    # Apply the degree-four singleton theorem conditionally at every vertex,
    # including vertices whose other incident blocks are optional.  For each
    # possible exact four-edge neighbourhood A, the clause is activated only
    # when precisely the blocks in A are nonzero.
    singleton_indicators: dict[tuple[Edge, int], int] = {}
    for edge in allowed_edges:
        first, second = edge
        for colour in range(d):
            singleton = cnf.variable()
            singleton_indicators[edge, colour] = singleton
            diagonal = entry(first, second, colour, colour)
            other_entries = [
                entries[first, second, row, column]
                for row in range(d)
                for column in range(d)
                if (row, column) != (colour, colour)
            ]
            cnf.add(-singleton, diagonal)
            for literal in other_entries:
                cnf.add(-singleton, -literal)
            cnf.add(-diagonal, *other_entries, singleton)

    for vertex in range(n):
        incident_edges = [
            tuple(sorted((vertex, neighbour)))
            for neighbour in neighbours[vertex]
        ]
        incident_singletons = [
            singleton_indicators[edge, colour]
            for edge in incident_edges
            for colour in range(d)
        ]
        for exact_neighbourhood in itertools.combinations(
            incident_edges, 4
        ):
            exact = set(exact_neighbourhood)
            cnf.add(
                *(-blocks[edge] for edge in exact_neighbourhood),
                *(blocks[edge] for edge in incident_edges if edge not in exact),
                *incident_singletons,
            )

        # At degree three, the three generic killers exhaust the
        # neighbourhood.  Isolating each channel with a colouring that is
        # monochromatic away from the centre forces all three v-side vectors
        # to be coordinate too.  Hence the incident blocks are three
        # monochromatic singletons, one of each colour.
        for exact_neighbourhood in itertools.combinations(
            incident_edges, 3
        ):
            exact = set(exact_neighbourhood)
            activation = [
                *(-blocks[edge] for edge in exact_neighbourhood),
                *(
                    blocks[edge]
                    for edge in incident_edges
                    if edge not in exact
                ),
            ]
            for edge in exact_neighbourhood:
                cnf.add(
                    *activation,
                    *(
                        singleton_indicators[edge, colour]
                        for colour in range(d)
                    ),
                )
            for colour in range(d):
                cnf.add(
                    *activation,
                    *(
                        singleton_indicators[edge, colour]
                        for edge in exact_neighbourhood
                    ),
                )

    # At-least-k among m block indicators is the conjunction saying every
    # subset of m-k+1 indicators contains a true one.  This is optional:
    # leaving k=0 makes the theorem independent of connectivity reductions.
    if minimum_degree:
        for vertex in range(n):
            incident = [
                blocks[tuple(sorted((vertex, neighbour)))]
                for neighbour in neighbours[vertex]
            ]
            subset_size = len(incident) - minimum_degree + 1
            for subset in itertools.combinations(incident, subset_size):
                cnf.add(*subset)

    candidates: dict[tuple[int, int, int], int] = {}
    anchors: dict[tuple[int, int, int], int] = {}
    non_coordinate_flags: dict[tuple[int, int, int], int] = {}
    for vertex in range(n):
        for colour in range(d):
            for neighbour in neighbours[vertex]:
                candidate = cnf.variable()
                candidates[vertex, colour, neighbour] = candidate
                inside = [
                    entry(vertex, neighbour, row, colour)
                    for row in range(d)
                ]
                outside = [
                    entry(vertex, neighbour, row, column)
                    for row in range(d)
                    for column in range(d)
                    if column != colour
                ]
                for literal in outside:
                    cnf.add(-candidate, -literal)
                cnf.add(-candidate, *inside)
                for literal in inside:
                    cnf.add(*outside, -literal, candidate)

                off_coordinate = [
                    entry(vertex, neighbour, row, colour)
                    for row in range(d)
                    if row != colour
                ]
                non_coordinate = cnf.variable()
                non_coordinate_flags[
                    vertex, colour, neighbour
                ] = non_coordinate
                cnf.add(-non_coordinate, *off_coordinate)
                for literal in off_coordinate:
                    cnf.add(-literal, non_coordinate)

                # Diagonal-anchor lemma: row ``colour`` at the centre is a
                # nonzero multiple of the same coordinate covector.
                anchor = cnf.variable()
                anchors[vertex, colour, neighbour] = anchor
                diagonal = entry(
                    vertex, neighbour, colour, colour
                )
                row_outside = [
                    entry(vertex, neighbour, colour, other)
                    for other in range(d)
                    if other != colour
                ]
                cnf.add(-anchor, diagonal)
                for literal in row_outside:
                    cnf.add(-anchor, -literal)
                cnf.add(
                    -diagonal,
                    *row_outside,
                    anchor,
                )
            cnf.add(
                *(
                    candidates[vertex, colour, neighbour]
                    for neighbour in neighbours[vertex]
                )
            )
            cnf.add(
                *(
                    anchors[vertex, colour, neighbour]
                    for neighbour in neighbours[vertex]
                )
            )

    if center_degree == 1:
        # Complete-ambient normalized-killer mode.  The generic killer
        # theorem supplies three distinct neighbours at every vertex.
        # Vertex and global-colour relabelling lets a catalogue role fix
        # them to neighbours 1,2,3 for colours 0,1,2.
        for colour, neighbour in enumerate((1, 2, 3)):
            cnf.add(candidates[0, colour, neighbour])

    # Failure-hyperplane backup theorem.  Let a selected c-killer be
    # ``a_c outer(e_c)``.  If ``a_c`` is non-coordinate, restrict the
    # local annihilator identity to generic points of ``a_c-perp``.  The
    # c-term remains nonzero while the other two terms are killed by their
    # primary killers.  Hence some other incident block B is a backup
    # c-killer throughout that hyperplane:
    #
    #   B[:,j] is proportional to a_c for every j != c,
    #   B[:,c] is nonzero (indeed, it is not proportional to a_c).
    #
    # At support level, each nonzero proportional column has exactly the
    # support of a_c.  A finite-union/Zariski-density argument makes one
    # fixed backup edge work on a dense subset of the hyperplane.
    support_product_indicators: dict[tuple[int, ...], int] = {}

    def support_product(*factors: int) -> int:
        key = tuple(sorted(factors))
        if key not in support_product_indicators:
            support_product_indicators[key] = matching_indicator(
                cnf, key
            )
        return support_product_indicators[key]

    def rank_two_support_products(
        first_vector: list[int],
        second_vector: list[int],
    ) -> list[int]:
        return [
            support_product(first_vector[first], second_vector[second])
            for first, second in itertools.permutations(range(d), 2)
        ]

    backup_indicators: dict[tuple[int, int, int, int], int] = {}
    for vertex in range(n):
        for colour in range(d):
            for killer_neighbour in neighbours[vertex]:
                killer_vector = [
                    entry(
                        vertex,
                        killer_neighbour,
                        row,
                        colour,
                    )
                    for row in range(d)
                ]
                backups: list[int] = []
                for backup_neighbour in neighbours[vertex]:
                    if backup_neighbour == killer_neighbour:
                        continue
                    backup = cnf.variable()
                    backup_indicators[
                        vertex,
                        colour,
                        killer_neighbour,
                        backup_neighbour,
                    ] = backup
                    backups.append(backup)
                    cnf.add(
                        -backup,
                        candidates[
                            vertex, colour, killer_neighbour
                        ],
                    )
                    cnf.add(
                        -backup,
                        non_coordinate_flags[
                            vertex, colour, killer_neighbour
                        ],
                    )
                    backup_colour_column = [
                        entry(
                            vertex,
                            backup_neighbour,
                            row,
                            colour,
                        )
                        for row in range(d)
                    ]
                    cnf.add(-backup, *backup_colour_column)
                    # The backup c-column is not proportional to the first
                    # killer vector, so the two vectors have rank two.
                    cnf.add(
                        -backup,
                        *rank_two_support_products(
                            killer_vector,
                            backup_colour_column,
                        ),
                    )
                    for other_colour in range(d):
                        if other_colour == colour:
                            continue
                        backup_column = [
                            entry(
                                vertex,
                                backup_neighbour,
                                row,
                                other_colour,
                            )
                            for row in range(d)
                        ]
                        for witness in backup_column:
                            for killer_entry, backup_entry in zip(
                                killer_vector,
                                backup_column,
                                strict=True,
                            ):
                                cnf.add(
                                    -backup,
                                    -witness,
                                    -killer_entry,
                                    backup_entry,
                                )
                                cnf.add(
                                    -backup,
                                    -witness,
                                    -backup_entry,
                                    killer_entry,
                                )
                cnf.add(
                    -candidates[
                        vertex, colour, killer_neighbour
                    ],
                    -non_coordinate_flags[
                        vertex, colour, killer_neighbour
                    ],
                    *backups,
                )

    # If one block backs up two different primary colours c,d, its remaining
    # colour-e column is exactly zero.  Indeed, the backup conditions put
    # that column in both span(a_c) and span(a_d), while their c/d columns
    # show that the two primary lines are distinct.  This is an exact
    # consequence even when the two primary vectors have the same support.
    shared_backup_zero_clauses = 0
    for vertex in range(n):
        for first_colour, second_colour in itertools.combinations(
            range(d), 2
        ):
            remaining_colour = next(
                colour
                for colour in range(d)
                if colour not in {first_colour, second_colour}
            )
            for first_neighbour in neighbours[vertex]:
                for second_neighbour in neighbours[vertex]:
                    if second_neighbour == first_neighbour:
                        continue
                    for backup_neighbour in neighbours[vertex]:
                        if backup_neighbour in {
                            first_neighbour,
                            second_neighbour,
                        }:
                            continue
                        first_backup = backup_indicators[
                            vertex,
                            first_colour,
                            first_neighbour,
                            backup_neighbour,
                        ]
                        second_backup = backup_indicators[
                            vertex,
                            second_colour,
                            second_neighbour,
                            backup_neighbour,
                        ]
                        for row in range(d):
                            cnf.add(
                                -first_backup,
                                -second_backup,
                                -entry(
                                    vertex,
                                    backup_neighbour,
                                    row,
                                    remaining_colour,
                                ),
                            )
                            shared_backup_zero_clauses += 1

    # Degree-five plane alternative.  Suppose an exact degree-five
    # neighbourhood has no monochromatic singleton and one spare block B
    # backs up two primary colours c,d.  The three non-coordinate primary
    # killers use three distinct edges, so B is one of only two spare
    # edges.  If neither e_c nor e_d belonged to
    # span(a_c,a_d), both local flags would require the other spare edge as
    # their third step.  Its c/d column-containment requirements are
    # opposite, a contradiction.  Hence
    #
    #   det(a_c,a_d,e_c) = 0  or  det(a_c,a_d,e_d) = 0.
    #
    # Each determinant has two monomials.  At support level, a determinant
    # can vanish only if it does not have exactly one supported monomial.
    # The clauses below forbid both determinants from being structurally
    # unbalanced.  They use only existing entry/support variables, so the
    # optional strengthening is a clause-only extension.
    degree_five_plane_clauses = 0
    if degree_five_plane:
        for vertex in range(n):
            incident_edges = [
                tuple(sorted((vertex, neighbour)))
                for neighbour in neighbours[vertex]
            ]
            for exact_neighbourhood in itertools.combinations(
                incident_edges, 5
            ):
                exact = set(exact_neighbourhood)
                exact_activation = [
                    *(
                        -blocks[edge]
                        for edge in exact_neighbourhood
                    ),
                    *(
                        blocks[edge]
                        for edge in incident_edges
                        if edge not in exact
                    ),
                    *(
                        singleton_indicators[edge, colour]
                        for edge in exact_neighbourhood
                        for colour in range(d)
                    ),
                ]
                exact_neighbours = [
                    edge[1] if edge[0] == vertex else edge[0]
                    for edge in exact_neighbourhood
                ]
                for first_colour, second_colour in itertools.combinations(
                    range(d), 2
                ):
                    coordinate_rows = {}
                    for coordinate in (
                        first_colour,
                        second_colour,
                    ):
                        coordinate_rows[coordinate] = [
                            row
                            for row in range(d)
                            if row != coordinate
                        ]
                    for first_neighbour in exact_neighbours:
                        first_vector = [
                            entry(
                                vertex,
                                first_neighbour,
                                row,
                                first_colour,
                            )
                            for row in range(d)
                        ]
                        for second_neighbour in exact_neighbours:
                            if second_neighbour == first_neighbour:
                                continue
                            second_vector = [
                                entry(
                                    vertex,
                                    second_neighbour,
                                    row,
                                    second_colour,
                                )
                                for row in range(d)
                            ]
                            for backup_neighbour in exact_neighbours:
                                if backup_neighbour in {
                                    first_neighbour,
                                    second_neighbour,
                                }:
                                    continue
                                shared = [
                                    backup_indicators[
                                        vertex,
                                        first_colour,
                                        first_neighbour,
                                        backup_neighbour,
                                    ],
                                    backup_indicators[
                                        vertex,
                                        second_colour,
                                        second_neighbour,
                                        backup_neighbour,
                                    ],
                                ]
                                determinant_terms = {}
                                for coordinate in (
                                    first_colour,
                                    second_colour,
                                ):
                                    first_row, second_row = (
                                        coordinate_rows[coordinate]
                                    )
                                    determinant_terms[coordinate] = (
                                        (
                                            first_vector[first_row],
                                            second_vector[second_row],
                                        ),
                                        (
                                            first_vector[second_row],
                                            second_vector[first_row],
                                        ),
                                    )
                                first_terms = determinant_terms[
                                    first_colour
                                ]
                                second_terms = determinant_terms[
                                    second_colour
                                ]
                                # Choose which term is the unique supported
                                # term in each determinant.  Distribute the
                                # assertion that the opposite term is
                                # unsupported over its two possible missing
                                # factors.
                                for first_active in range(2):
                                    first_on = first_terms[first_active]
                                    first_off = first_terms[
                                        1 - first_active
                                    ]
                                    for second_active in range(2):
                                        second_on = second_terms[
                                            second_active
                                        ]
                                        second_off = second_terms[
                                            1 - second_active
                                        ]
                                        for first_missing in first_off:
                                            for second_missing in second_off:
                                                cnf.add(
                                                    *exact_activation,
                                                    *(
                                                        -indicator
                                                        for indicator in shared
                                                    ),
                                                    *(
                                                        -factor
                                                        for factor in first_on
                                                    ),
                                                    first_missing,
                                                    *(
                                                        -factor
                                                        for factor in second_on
                                                    ),
                                                    second_missing,
                                                )
                                                degree_five_plane_clauses += 1

    # Complete local killer flags.  Continuing the failure-hyperplane
    # argument gives a flag of length at most three.  Its c-columns
    # b_1,...,b_k grow a strict span A_i, every non-c column of the i-th
    # edge lies in A_(i-1), and e_c lies in A_k.
    #
    # The Boolean encoding keeps only necessary support consequences:
    # * length two: rank(b1,b2)=2 and det(b1,b2,e_c)=0;
    # * length three: det(b1,b2,e_c) != 0,
    #   det(b1,b2,b3) != 0, and every non-c column z of edge three obeys
    #   det(b1,b2,z)=0.
    killer_flag_indicators: dict[tuple[int, ...], int] = {}
    for vertex in range(n):
        for colour in range(d):
            task_flags: list[int] = [
                singleton_indicators[
                    tuple(sorted((vertex, neighbour))), colour
                ]
                for neighbour in neighbours[vertex]
            ]
            flags_by_first: dict[int, list[int]] = {
                neighbour: [] for neighbour in neighbours[vertex]
            }
            other_rows = [
                row for row in range(d) if row != colour
            ]
            first_other, second_other = other_rows
            for first_neighbour in neighbours[vertex]:
                first_vector = [
                    entry(
                        vertex,
                        first_neighbour,
                        row,
                        colour,
                    )
                    for row in range(d)
                ]
                for second_neighbour in neighbours[vertex]:
                    if second_neighbour == first_neighbour:
                        continue
                    second_vector = [
                        entry(
                            vertex,
                            second_neighbour,
                            row,
                            colour,
                        )
                        for row in range(d)
                    ]
                    pair = backup_indicators[
                        vertex,
                        colour,
                        first_neighbour,
                        second_neighbour,
                    ]
                    determinant_with_coordinate = [
                        support_product(
                            first_vector[first_other],
                            second_vector[second_other],
                        ),
                        support_product(
                            first_vector[second_other],
                            second_vector[first_other],
                        ),
                    ]

                    length_two = cnf.variable()
                    killer_flag_indicators[
                        (
                            vertex,
                            colour,
                            first_neighbour,
                            second_neighbour,
                        )
                    ] = length_two
                    task_flags.append(length_two)
                    flags_by_first[first_neighbour].append(length_two)
                    cnf.add(-length_two, pair)
                    # det(b1,b2,e_c)=0: its two supported monomials are
                    # either both present or both absent.
                    first_term, second_term = (
                        determinant_with_coordinate
                    )
                    cnf.add(
                        -length_two,
                        -first_term,
                        second_term,
                    )
                    cnf.add(
                        -length_two,
                        -second_term,
                        first_term,
                    )

                    for third_neighbour in neighbours[vertex]:
                        if third_neighbour in {
                            first_neighbour,
                            second_neighbour,
                        }:
                            continue
                        third_vector = [
                            entry(
                                vertex,
                                third_neighbour,
                                row,
                                colour,
                            )
                            for row in range(d)
                        ]
                        length_three = cnf.variable()
                        killer_flag_indicators[
                            (
                                vertex,
                                colour,
                                first_neighbour,
                                second_neighbour,
                                third_neighbour,
                            )
                        ] = length_three
                        task_flags.append(length_three)
                        flags_by_first[first_neighbour].append(
                            length_three
                        )
                        cnf.add(-length_three, pair)
                        # A minimal length-three flag has
                        # det(b1,b2,e_c) != 0.
                        cnf.add(
                            -length_three,
                            *determinant_with_coordinate,
                        )
                        determinant_terms = [
                            support_product(
                                first_vector[permutation[0]],
                                second_vector[permutation[1]],
                                third_vector[permutation[2]],
                            )
                            for permutation in itertools.permutations(
                                range(d)
                            )
                        ]
                        cnf.add(
                            -length_three,
                            *determinant_terms,
                        )
                        for other_colour in range(d):
                            if other_colour == colour:
                                continue
                            third_column = [
                                entry(
                                    vertex,
                                    third_neighbour,
                                    row,
                                    other_colour,
                                )
                                for row in range(d)
                            ]
                            # Membership in span(b1,b2) first forces
                            # coordinate support containment.
                            for row, third_entry in enumerate(
                                third_column
                            ):
                                cnf.add(
                                    -length_three,
                                    -third_entry,
                                    first_vector[row],
                                    second_vector[row],
                                )
                            # It also forces det(b1,b2,z)=0.  A determinant
                            # with exactly one supported monomial cannot
                            # vanish over any field.
                            membership_terms = [
                                support_product(
                                    first_vector[
                                        permutation[0]
                                    ],
                                    second_vector[
                                        permutation[1]
                                    ],
                                    third_column[
                                        permutation[2]
                                    ],
                                )
                                for permutation in itertools.permutations(
                                    range(d)
                                )
                            ]
                            for term in membership_terms:
                                cnf.add(
                                    -length_three,
                                    -term,
                                    *(
                                        other
                                        for other in membership_terms
                                        if other != term
                                    ),
                                )

            # Every non-coordinate c-killer can be extended to such a
            # length-two or length-three flag.  A coordinate candidate is
            # already one of the singleton indicators above.
            for first_neighbour in neighbours[vertex]:
                cnf.add(
                    -candidates[
                        vertex, colour, first_neighbour
                    ],
                    -non_coordinate_flags[
                        vertex, colour, first_neighbour
                    ],
                    *flags_by_first[first_neighbour],
                )
            cnf.add(*task_flags)

    # Conditional form of the degree-four proportionality relation at every
    # vertex.  Each exact four-edge neighbourhood and each possible choice
    # of its three distinct killer edges is covered.  If the chosen
    # c-killer is non-coordinate, every nonzero non-c spare column has
    # exactly the same support as its v-side vector.
    degree_four_relation_cases = 0
    for vertex in range(n):
        incident_edges = [
            tuple(sorted((vertex, neighbour)))
            for neighbour in neighbours[vertex]
        ]
        for exact_neighbourhood in itertools.combinations(
            incident_edges, 4
        ):
            exact = set(exact_neighbourhood)
            exact_activation = [
                *(-blocks[edge] for edge in exact_neighbourhood),
                *(
                    blocks[edge]
                    for edge in incident_edges
                    if edge not in exact
                ),
            ]
            for killer_neighbours in itertools.permutations(
                (
                    edge[1] if edge[0] == vertex else edge[0]
                    for edge in exact_neighbourhood
                ),
                d,
            ):
                killer_edges = {
                    tuple(sorted((vertex, neighbour)))
                    for neighbour in killer_neighbours
                }
                spare_edge = next(iter(exact - killer_edges))
                spare_neighbour = (
                    spare_edge[1]
                    if spare_edge[0] == vertex
                    else spare_edge[0]
                )
                selected = [
                    candidates[vertex, colour, neighbour]
                    for colour, neighbour in enumerate(
                        killer_neighbours
                    )
                ]
                degree_four_relation_cases += 1
                for colour, killer_neighbour in enumerate(
                    killer_neighbours
                ):
                    base = [
                        *exact_activation,
                        *(-literal for literal in selected),
                        -non_coordinate_flags[
                            vertex, colour, killer_neighbour
                        ],
                    ]
                    killer_vector = [
                        entry(
                            vertex,
                            killer_neighbour,
                            row,
                            colour,
                        )
                        for row in range(d)
                    ]
                    for spare_colour in range(d):
                        if spare_colour == colour:
                            continue
                        spare_column = [
                            entry(
                                vertex,
                                spare_neighbour,
                                row,
                                spare_colour,
                            )
                            for row in range(d)
                        ]
                        for witness in spare_column:
                            for killer_entry, spare_entry in zip(
                                killer_vector,
                                spare_column,
                                strict=True,
                            ):
                                cnf.add(
                                    *base,
                                    -witness,
                                    -killer_entry,
                                    spare_entry,
                                )
                                cnf.add(
                                    *base,
                                    -witness,
                                    -spare_entry,
                                    killer_entry,
                                )

    allowed = set(allowed_edges)
    matchings = tuple(
        matching
        for matching in perfect_matchings(tuple(range(n)))
        if all(edge in allowed for edge in matching)
    )
    for colouring in itertools.product(range(d), repeat=n):
        indicators = [
            matching_indicator(
                cnf,
                tuple(
                    entry(
                        first,
                        second,
                        colouring[first],
                        colouring[second],
                    )
                    for first, second in matching
                ),
            )
            for matching in matchings
        ]
        if all(value == colouring[0] for value in colouring):
            cnf.add(*indicators)
        else:
            for indicator in indicators:
                cnf.add(
                    -indicator,
                    *(
                        other
                        for other in indicators
                        if other != indicator
                    ),
                )

    return cnf, {
        "allowed_edges": len(allowed_edges),
        "entry_variables": len(entries),
        "block_indicators": len(blocks),
        "killer_candidates": len(candidates),
        "anchor_candidates": len(anchors),
        "non_coordinate_flags": len(non_coordinate_flags),
        "failure_backup_indicators": len(backup_indicators),
        "shared_backup_zero_clauses": shared_backup_zero_clauses,
        "degree_five_plane_clauses": degree_five_plane_clauses,
        "killer_flag_indicators": len(killer_flag_indicators),
        "killer_flag_support_products": len(
            support_product_indicators
        ),
        "degree_four_relation_flags": 2,
        "degree_four_relation_cases": degree_four_relation_cases,
        "singleton_indicators": len(singleton_indicators),
        "perfect_matchings": len(matchings),
        "colourings": d**n,
        "minimum_degree": minimum_degree,
        "maximum_edges": maximum_edges,
        "center_degree": center_degree,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cnf",
        type=Path,
        default=Path("tmp/eight_vertex_local_degree4.cnf"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tmp/eight_vertex_local_degree4.json"),
    )
    parser.add_argument(
        "--minimum-degree",
        type=int,
        default=0,
        help="optional lower bound on every skeleton degree",
    )
    parser.add_argument(
        "--maximum-edges",
        type=int,
        help="optional upper bound on the number of nonzero blocks",
    )
    parser.add_argument(
        "--center-degree",
        type=int,
        choices=(0, 1, 3, 4),
        default=4,
        help=(
            "degree fixed at normalized vertex zero; "
            "zero keeps the complete unnormalized edge set and "
            "one keeps it complete while normalizing three killers"
        ),
    )
    parser.add_argument(
        "--write-only",
        action="store_true",
        help="materialize the CNF without invoking a solver",
    )
    parser.add_argument(
        "--degree-five-plane",
        action="store_true",
        help=(
            "add the exact-degree-five shared-primary-plane "
            "support consequence"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    cnf, metadata = local_degree_four_cnf(
        minimum_degree=args.minimum_degree,
        maximum_edges=args.maximum_edges,
        center_degree=args.center_degree,
        degree_five_plane=args.degree_five_plane,
    )
    build_seconds = time.perf_counter() - started
    if args.write_only:
        write_started = time.perf_counter()
        cnf.write_dimacs(args.cnf)
        status = "NOT_SOLVED"
        solve_seconds = time.perf_counter() - write_started
    else:
        solve_started = time.perf_counter()
        status = solve_with_cadical(cnf, args.cnf)
        solve_seconds = time.perf_counter() - solve_started
    payload = {
        "scope": (
            "n=8, one degree-four vertex, support relaxation"
            if args.center_degree == 4
            else (
                "n=8, one degree-three vertex, support relaxation"
                if args.center_degree == 3
                else (
                    "n=8, normalized generic-killer support relaxation"
                    if args.center_degree == 1
                    else "n=8, global support relaxation"
                )
            )
        )
        + (
            f", minimum degree {args.minimum_degree}"
            f", maximum edges {args.maximum_edges}"
        ),
        "necessary_conditions_only": True,
        **metadata,
        "variables": cnf.variable_count,
        "clauses": len(cnf.clauses),
        "cnf": str(args.cnf),
        "status": status,
        "build_seconds": build_seconds,
        "solve_seconds": solve_seconds,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
