"""Independent no-project-import audit for GLS58.

This script imports neither the primary verifier nor repository code.  It uses
finite-field subspace sets, bit-mask perfect matchings, and coefficient tables
for bilinear cross-product polynomials.  The written proof carries the
characteristic-zero and complete-witness quantifiers.
"""

from __future__ import annotations

from collections import Counter
from functools import cache
from itertools import product

PRIME = 5


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(x * y for x, y in zip(left, right, strict=True)) % PRIME


def audit_covector_kernel_census() -> dict[str, int]:
    vectors = tuple(product(range(PRIME), repeat=3))
    cases = 0
    pure_axes = 0
    witness_triples = 0
    support_counts: Counter[int] = Counter()

    for vector in vectors:
        support_counts[sum(bool(value) for value in vector)] += 1

    for colour in range(3):
        for covector in vectors:
            cases += 1
            witnesses = [
                vector
                for vector in vectors
                if dot(covector, vector) == 0 and vector[colour]
            ]
            pure = (
                covector[colour] != 0
                and all(
                    covector[index] == 0
                    for index in range(3)
                    if index != colour
                )
            )
            assert bool(witnesses) != pure
            pure_axes += int(pure)
            witness_triples += len(witnesses)

    assert cases == 375
    assert pure_axes == 12
    assert witness_triples == 7500
    assert support_counts == Counter({0: 1, 1: 12, 2: 48, 3: 64})
    return {
        "independent_covector_colour_cases": cases,
        "independent_pure_axis_obstructions": pure_axes,
        "independent_kernel_coordinate_witnesses": witness_triples,
        "F5_support_one_vectors": support_counts[1],
        "F5_support_two_vectors": support_counts[2],
        "F5_support_three_vectors": support_counts[3],
    }


@cache
def matching_masks(vertices_mask: int) -> tuple[tuple[int, ...], ...]:
    if vertices_mask == 0:
        return ((),)
    first_bit = vertices_mask & -vertices_mask
    first = first_bit.bit_length() - 1
    rest = vertices_mask ^ first_bit
    result: list[tuple[int, ...]] = []
    partner_mask = rest
    while partner_mask:
        partner_bit = partner_mask & -partner_mask
        edge_mask = (1 << first) | partner_bit
        for tail in matching_masks(rest ^ partner_bit):
            result.append((edge_mask,) + tail)
        partner_mask ^= partner_bit
    return tuple(result)


def edge_in_matching(matching: tuple[int, ...], left: int, right: int) -> bool:
    return ((1 << left) | (1 << right)) in matching


def partner(matching: tuple[int, ...], vertex: int) -> int:
    vertex_bit = 1 << vertex
    edge = next(edge for edge in matching if edge & vertex_bit)
    return (edge ^ vertex_bit).bit_length() - 1


def normalized_matching(edges: list[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(tuple(sorted(edge)) for edge in edges))


def audit_reverse_matching_partitions() -> dict[str, int]:
    matchings = matching_masks((1 << 8) - 1)
    one_counts: Counter[str] = Counter()
    two_counts: Counter[str] = Counter()
    one_signatures: set[
        tuple[int, int, tuple[tuple[int, int], ...]]
    ] = set()
    one_pair_counts: Counter[frozenset[int]] = Counter()
    two_signatures: set[tuple[tuple[tuple[int, int], ...], str]] = set()
    retained = {0, 1, 4, 5, 6, 7}
    auxiliary = {2, 3, 4, 5, 6, 7}

    for matching in matchings:
        if edge_in_matching(matching, 0, 1):
            one_counts["anchor"] += 1
            two_counts["anchor"] += 1
            continue

        probe_pair = {partner(matching, 0), partner(matching, 1)}
        if 2 in probe_pair:
            one_counts["kernel_killed"] += 1
        else:
            one_counts["retained"] += 1
            probe_zero_partner = partner(matching, 0)
            probe_one_partner = partner(matching, 1)
            deck_edges = normalized_matching(
                [
                    tuple(index for index in range(8) if edge & (1 << index))
                    for edge in matching
                    if not edge & ((1 << 0) | (1 << 1))
                ]
            )
            deck_vertices = {
                vertex for edge in deck_edges for vertex in edge
            }
            assert deck_vertices == auxiliary - {
                probe_zero_partner,
                probe_one_partner,
            }
            one_signatures.add(
                (probe_zero_partner, probe_one_partner, deck_edges)
            )
            one_pair_counts[
                frozenset({probe_zero_partner, probe_one_partner})
            ] += 1

        if probe_pair & {2, 3}:
            two_counts["kernel_killed"] += 1
            continue
        two_counts["retained"] += 1

        if edge_in_matching(matching, 2, 3):
            port_edge = next(
                edge
                for edge in matching
                if not edge & ((1 << 0) | (1 << 1) | (1 << 2) | (1 << 3))
            )
            u, v = tuple(index for index in range(8) if port_edge & (1 << index))
            branch = "h"
        else:
            u = partner(matching, 2)
            v = partner(matching, 3)
            branch = "ab" if u < v else "ba"

        new_edges: list[tuple[int, int]] = [(min(u, v), max(u, v))]
        for edge in matching:
            endpoints = tuple(index for index in range(8) if edge & (1 << index))
            if set(endpoints) <= retained:
                new_edges.append((endpoints[0], endpoints[1]))
        signature = (normalized_matching(new_edges), branch)
        two_signatures.add(signature)

    assert len(matchings) == 105
    assert one_counts == Counter(anchor=15, kernel_killed=30, retained=60)
    assert len(one_signatures) == 60
    assert len(one_pair_counts) == 10
    assert set(one_pair_counts.values()) == {6}
    assert two_counts == Counter(anchor=15, kernel_killed=54, retained=36)
    assert len(two_signatures) == 36

    six_matchings = matching_masks(sum(1 << vertex for vertex in retained))
    live_six = [matching for matching in six_matchings if not edge_in_matching(matching, 0, 1)]
    assert len(six_matchings) == 15
    assert len(live_six) == 12
    assert len(two_signatures) == len(live_six) * 3
    return {
        "bitmask_eight_vertex_matchings": len(matchings),
        "one_kernel_anchor_matchings": one_counts["anchor"],
        "one_kernel_killed_matchings": one_counts["kernel_killed"],
        "one_kernel_not_forced_zero_matching_slots": one_counts["retained"],
        "one_kernel_ten_deck_signatures": len(one_signatures),
        "two_kernel_killed_matchings": two_counts["kernel_killed"],
        "two_kernel_not_forced_zero_matching_slots": two_counts["retained"],
        "two_kernel_descent_signatures": len(two_signatures),
    }


Cell = tuple[int, int, int]


def sparse_tensor_from_cells(
    vertices: tuple[int, ...],
    open_vertices: tuple[int, ...],
    edge_cells: dict[tuple[int, int], tuple[Cell, ...]],
    fixed_vectors: dict[int, tuple[int, int, int]] | None = None,
) -> tuple[Counter[tuple[int, ...]], int]:
    fixed = fixed_vectors or {}
    position = {vertex: index for index, vertex in enumerate(open_vertices)}
    coefficients: Counter[tuple[int, ...]] = Counter()
    coloured_terms = 0
    for matching in matching_masks(sum(1 << vertex for vertex in vertices)):
        choices: list[tuple[Cell, ...]] = []
        ordered_edges: list[tuple[int, int]] = []
        for edge_mask in matching:
            endpoints = tuple(
                index for index in vertices if edge_mask & (1 << index)
            )
            edge = (endpoints[0], endpoints[1])
            cells = edge_cells.get(edge, ())
            if not cells:
                break
            ordered_edges.append(edge)
            choices.append(cells)
        else:
            for selected in product(*choices):
                word = [-1] * len(open_vertices)
                value = 1
                for (left, right), (left_colour, right_colour, entry) in zip(
                    ordered_edges, selected, strict=True
                ):
                    value *= entry
                    if left in fixed:
                        value *= fixed[left][left_colour]
                    else:
                        word[position[left]] = left_colour
                    if right in fixed:
                        value *= fixed[right][right_colour]
                    else:
                        word[position[right]] = right_colour
                if value:
                    coloured_terms += 1
                    coefficients[tuple(word)] += value
    return Counter(
        {word: coefficient for word, coefficient in coefficients.items() if coefficient}
    ), coloured_terms


def rank_mod(rows: tuple[tuple[int, ...], ...]) -> int:
    matrix = [list(entry % PRIME for entry in row) for row in rows]
    if not matrix:
        return 0
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, PRIME)
        matrix[rank] = [entry * inverse % PRIME for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                (entry - scale * pivot_entry) % PRIME
                for entry, pivot_entry in zip(
                    matrix[row], matrix[rank], strict=True
                )
            ]
        rank += 1
    return rank


def joint_rows_from_cells(
    label: int, edge_cells: dict[tuple[int, int], tuple[Cell, ...]]
) -> tuple[tuple[int, int, int], ...]:
    rows = [[0, 0, 0] for _ in range(6)]
    for probe in (0, 1):
        for probe_colour, label_colour, value in edge_cells.get(
            (probe, label), ()
        ):
            rows[3 * probe + probe_colour][label_colour] += value
    return tuple(tuple(row) for row in rows)  # type: ignore[return-value]


def audit_h_zero_binary_control() -> dict[str, int]:
    # Full eight-vertex sparse lift: probes 0,1; deficient labels 2,3;
    # retained ports 4,5,6,7.  Cells are (left colour, right colour, value).
    full_vertices = tuple(range(8))
    retained = (0, 1, 4, 5, 6, 7)
    full_cells: dict[tuple[int, int], tuple[Cell, ...]] = {
        (0, 2): ((0, 0, 1), (0, 1, -1), (1, 2, 1)),
        (0, 3): ((0, 0, 1), (0, 1, -1), (1, 2, 1)),
        (0, 4): ((0, 0, 1),),
        (1, 5): ((0, 0, 1),),
        (1, 6): ((1, 1, 1),),
        (0, 7): ((1, 1, 1),),
        (2, 4): ((0, 1, 1),),
        (2, 6): ((0, 0, 1),),
        (3, 5): ((0, 1, 1),),
        (3, 7): ((0, 0, 1),),
    }
    kernel = (1, 1, 0)
    full_coefficients, full_terms = sparse_tensor_from_cells(
        full_vertices,
        retained,
        full_cells,
        {2: kernel, 3: kernel},
    )

    effective_cells: dict[tuple[int, int], tuple[Cell, ...]] = {
        (0, 4): ((0, 0, 1),),
        (1, 5): ((0, 0, 1),),
        (1, 6): ((1, 1, 1),),
        (0, 7): ((1, 1, 1),),
        (4, 5): ((1, 1, 1),),
        (6, 7): ((0, 0, 1),),
        (4, 7): ((1, 0, 1),),
        (5, 6): ((1, 0, 1),),
    }
    effective_coefficients, effective_terms = sparse_tensor_from_cells(
        retained,
        retained,
        effective_cells,
    )
    expected = Counter({(0,) * 6: 1, (1,) * 6: 1})
    assert full_coefficients == effective_coefficients == expected
    assert full_terms == effective_terms == 2

    expected_ranks = {2: 2, 3: 2, 4: 1, 5: 1, 6: 1, 7: 1}
    rigid_colours = {2: 2, 3: 2, 4: 0, 5: 0, 6: 1, 7: 1}
    for label in range(2, 8):
        rows = joint_rows_from_cells(label, full_cells)
        rank = rank_mod(rows)
        assert rank == expected_ranks[label]
        coordinate_row = tuple(int(index == rigid_colours[label]) for index in range(3))
        assert rank_mod(rows + (coordinate_row,)) == rank
    assert all(
        sum(
            kernel[label_colour] * value
            for left_colour, label_colour, value in full_cells.get(
                (probe, label), ()
            )
            if left_colour == probe_colour
        )
        == 0
        for label in (2, 3)
        for probe in (0, 1)
        for probe_colour in range(3)
    )
    return {
        "independent_binary_full_lift_edges": len(full_cells),
        "independent_binary_coloured_terms": full_terms,
        "independent_binary_nonzero_words": len(full_coefficients),
        "independent_binary_rigid_labels": len(expected_ranks),
    }


def normalize_projective(vector: tuple[int, int, int]) -> tuple[int, int, int]:
    first = next(value for value in vector if value)
    inverse = pow(first, -1, PRIME)
    return tuple(value * inverse % PRIME for value in vector)  # type: ignore[return-value]


def all_subspaces() -> tuple[frozenset[tuple[int, int, int]], ...]:
    vectors = tuple(product(range(PRIME), repeat=3))
    zero = (0, 0, 0)
    projective = sorted(
        {
            normalize_projective(vector)
            for vector in vectors
            if vector != zero
        }
    )
    spaces: set[frozenset[tuple[int, int, int]]] = {frozenset({zero}), frozenset(vectors)}
    for generator in projective:
        spaces.add(
            frozenset(
                tuple(scale * entry % PRIME for entry in generator)
                for scale in range(PRIME)
            )
        )
        spaces.add(frozenset(vector for vector in vectors if dot(generator, vector) == 0))
    assert len(spaces) == 64
    return tuple(spaces)


def span_sum(
    left: frozenset[tuple[int, int, int]],
    right: frozenset[tuple[int, int, int]],
) -> frozenset[tuple[int, int, int]]:
    return frozenset(
        tuple((x + y) % PRIME for x, y in zip(u, v, strict=True))
        for u in left
        for v in right
    )


def projected_determinant(
    left: tuple[int, int, int], right: tuple[int, int, int], colour: int
) -> int:
    other = tuple(index for index in range(3) if index != colour)
    return (
        left[other[0]] * right[other[1]]
        - left[other[1]] * right[other[0]]
    ) % PRIME


def audit_injective_projection_classification() -> dict[str, int]:
    spaces = all_subspaces()
    full = frozenset(product(range(PRIME), repeat=3))
    injective_pairs = 0
    coordinate_cases = 0
    whole_cross_zero_pairs = 0
    no_zero_coordinate_pairs = 0

    for left in spaces:
        for right in spaces:
            if span_sum(left, right) != full:
                continue
            injective_pairs += 1
            zero_coordinates = 0
            for colour in range(3):
                cross_zero = all(
                    projected_determinant(u, v, colour) == 0
                    for u in left
                    for v in right
                )
                left_projection_zero = all(
                    all(vector[index] == 0 for index in range(3) if index != colour)
                    for vector in left
                )
                right_projection_zero = all(
                    all(vector[index] == 0 for index in range(3) if index != colour)
                    for vector in right
                )
                assert cross_zero == (left_projection_zero or right_projection_zero)
                coordinate_cases += 1
                zero_coordinates += int(cross_zero)
            whole_cross_zero_pairs += int(zero_coordinates == 3)
            no_zero_coordinate_pairs += int(zero_coordinates == 0)

    assert injective_pairs == 2607
    assert coordinate_cases == 2607 * 3
    assert whole_cross_zero_pairs == 2
    assert no_zero_coordinate_pairs == 2449
    return {
        "F5_subspaces": len(spaces),
        "F5_injective_rowspace_pairs": injective_pairs,
        "F5_injective_coordinate_cases": coordinate_cases,
        "F5_pure_probe_axis_pairs": whole_cross_zero_pairs,
        "F5_no_zero_cross_coordinate_pairs": no_zero_coordinate_pairs,
    }


def cross_mod(
    left: tuple[int, int, int], right: tuple[int, int, int]
) -> tuple[int, int, int]:
    return (
        (left[1] * right[2] - left[2] * right[1]) % PRIME,
        (left[2] * right[0] - left[0] * right[2]) % PRIME,
        (left[0] * right[1] - left[1] * right[0]) % PRIME,
    )


def audit_transverse_rank_two_factor_and_cover() -> dict[str, int]:
    spaces = all_subspaces()
    vectors = tuple(product(range(PRIME), repeat=3))
    zero = (0, 0, 0)
    planes = tuple(space for space in spaces if len(space) == PRIME**2)
    pair_count = 0
    nonzero_crosses = 0

    assert len(planes) == 31
    for plane in planes:
        normal_set = {
            normalize_projective(vector)
            for vector in vectors
            if vector != zero and all(dot(row, vector) == 0 for row in plane)
        }
        assert len(normal_set) == 1
        normal = next(iter(normal_set))
        nonzero_subspaces = tuple(
            space for space in spaces if len(space) > 1 and space <= plane
        )
        assert len(nonzero_subspaces) == 7
        local_pairs = 0
        for left in nonzero_subspaces:
            for right in nonzero_subspaces:
                if span_sum(left, right) != plane:
                    continue
                local_pairs += 1
                pair_count += 1
                crosses = {
                    cross_mod(u, v)
                    for u in left
                    for v in right
                    if cross_mod(u, v) != zero
                }
                assert crosses
                assert {
                    normalize_projective(vector) for vector in crosses
                } == {normal}
                nonzero_crosses += len(crosses)
        assert local_pairs == 43

    assert pair_count == 31 * 43 == 1333

    # The cancelled coefficient scalars vanish exactly when the six kernel
    # zero sets cover all three coordinates.  Seven masks exhaust the possible
    # zero-coordinate patterns of a nonzero vector in dimension three.
    zero_masks = tuple(range(7))
    mask_profiles = 0
    covering_profiles = 0
    for profile in product(zero_masks, repeat=6):
        coefficient_zero = all(
            any(mask & (1 << colour) for mask in profile)
            for colour in range(3)
        )
        covers = bool(profile[0] | profile[1] | profile[2] | profile[3] | profile[4] | profile[5] == 7)
        assert coefficient_zero == covers
        mask_profiles += 1
        covering_profiles += int(covers)
    assert mask_profiles == 7**6
    return {
        "F5_transverse_rank_two_rowspace_pairs": pair_count,
        "F5_rank_two_nonzero_cross_vectors": nonzero_crosses,
        "rank_two_kernel_zero_mask_profiles": mask_profiles,
        "rank_two_covering_zero_mask_profiles": covering_profiles,
    }


def matrix_add_mod(
    left: tuple[tuple[int, ...], ...], right: tuple[tuple[int, ...], ...]
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple((x + y) % PRIME for x, y in zip(lrow, rrow, strict=True))
        for lrow, rrow in zip(left, right, strict=True)
    )


def cross_coordinate_coefficients(
    x_matrix: tuple[tuple[int, ...], ...],
    y_matrix: tuple[tuple[int, ...], ...],
    colour: int,
) -> tuple[tuple[int, ...], ...]:
    other = tuple(index for index in range(3) if index != colour)
    return tuple(
        tuple(
            (
                x_matrix[left_root][other[0]] * y_matrix[right_root][other[1]]
                - x_matrix[left_root][other[1]] * y_matrix[right_root][other[0]]
            )
            % PRIME
            for right_root in range(3)
        )
        for left_root in range(3)
    )


def audit_termwise_injective_control() -> dict[str, int]:
    permutation = ((0, 0, 1), (1, 0, 0), (0, 1, 0))
    addition_cells = ((0, 0), (1, 1), None, (2, 2), None, None)
    y_cells = ((2, 2), (0, 1), (0, 0), (0, 2), (1, 1), (0, 1))
    selected_zero = (2, None, 0, None, 1, None)
    zero_matrix = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
    crosses: list[tuple[tuple[tuple[int, ...], ...], ...]] = []

    for addition_cell, y_cell, vanished in zip(
        addition_cells, y_cells, selected_zero, strict=True
    ):
        addition = [list(row) for row in zero_matrix]
        if addition_cell is not None:
            addition[addition_cell[0]][addition_cell[1]] = 1
        x_matrix = matrix_add_mod(permutation, tuple(tuple(row) for row in addition))
        y_matrix = [list(row) for row in zero_matrix]
        y_matrix[y_cell[0]][y_cell[1]] = 1
        y_tuple = tuple(tuple(row) for row in y_matrix)
        coordinate_tables = tuple(
            cross_coordinate_coefficients(x_matrix, y_tuple, colour)
            for colour in range(3)
        )
        assert any(any(any(row) for row in table) for table in coordinate_tables)
        if vanished is not None:
            assert not any(any(row) for row in coordinate_tables[vanished])
        crosses.append(coordinate_tables)

    for colour in range(3):
        assert any(
            not any(any(row) for row in crosses[label][colour])
            for label in range(6)
        )
    return {
        "independent_injective_control_labels": len(crosses),
        "independent_termwise_zero_products": 3,
    }


def audit_injective_physical_control() -> dict[str, int]:
    labels = (2, 3, 4, 5, 6, 7)
    base_cells = ((0, 2, 1), (1, 0, 1), (2, 1, 1))
    additions = ((0, 0), (1, 1), None, (2, 2), None, None)
    y_cells = ((2, 2), (0, 1), (0, 0), (0, 2), (1, 1), (0, 1))
    edge_cells: dict[tuple[int, int], tuple[Cell, ...]] = {}
    for label, addition, y_cell in zip(
        labels, additions, y_cells, strict=True
    ):
        x_cells = list(base_cells)
        if addition is not None:
            x_cells.append((addition[0], addition[1], 1))
        edge_cells[(0, label)] = tuple(x_cells)
        edge_cells[(1, label)] = ((y_cell[0], y_cell[1], 1),)

    edge_cells[(3, 7)] = ((0, 0, 1), (2, 2, 1))
    edge_cells[(5, 6)] = ((0, 0, 1),)
    edge_cells[(2, 7)] = ((1, 1, 1),)
    edge_cells[(4, 5)] = ((1, 1, 1),)
    edge_cells[(4, 6)] = ((2, 2, 1),)

    coefficients, coloured_terms = sparse_tensor_from_cells(
        tuple(range(8)), tuple(range(8)), edge_cells
    )
    pure = tuple(coefficients[(colour,) * 8] for colour in range(3))
    mixed = {
        word: coefficient
        for word, coefficient in coefficients.items()
        if len(set(word)) > 1
    }
    assert pure == (1, 1, 1)
    assert len(coefficients) == 64
    assert len(mixed) == 61
    assert max(coefficients.values()) == 2
    assert coloured_terms == 66
    assert (2, 3) not in edge_cells  # H_Q=0 for Q={q_0,q_1}.
    assert all(rank_mod(joint_rows_from_cells(label, edge_cells)) == 3 for label in labels)
    return {
        "independent_physical_control_supported_words": len(coefficients),
        "independent_physical_control_mixed_words": len(mixed),
        "independent_physical_control_coloured_terms": coloured_terms,
        "independent_physical_control_injective_maps": len(labels),
        "independent_physical_control_H_Q_zero": 1,
    }


def main() -> None:
    summary: dict[str, int] = {}
    summary.update(audit_covector_kernel_census())
    summary.update(audit_reverse_matching_partitions())
    summary.update(audit_h_zero_binary_control())
    summary.update(audit_injective_projection_classification())
    summary.update(audit_transverse_rank_two_factor_and_cover())
    summary.update(audit_termwise_injective_control())
    summary.update(audit_injective_physical_control())
    for key, value in summary.items():
        print(f"{key}: {value}")
    print("GLS58 independent no-import audit: PASS")


if __name__ == "__main__":
    main()
