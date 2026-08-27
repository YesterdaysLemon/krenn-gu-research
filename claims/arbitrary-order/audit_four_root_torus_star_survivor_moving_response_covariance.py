#!/usr/bin/env python3
"""Exact symbolic covariance audit for the equal-leaf moving interface.

This is deliberately independent of the GLD82 verifier.  It works in the
polynomial ring Z[p] on the entries of two formal port matrices:

    p[0,c,r] = (P_0 adj(F_0)^T)[r,c] / det(F_0),
    p[1,c,r] = (P_l adj(F_l)^T)[r,c] / det(F_l).

The three leaf ports all use the second family.  Thus identities proved in
Z[p] remain identities after the 15-variable equal-leaf frame substitution
of GLD75 (and after clearing the displayed frame determinants).  Keeping the
port entries formal avoids a large rational expansion while retaining an
exact polynomial identity check: no numerical frame is sampled here.

The audit checks, for every leaf permutation and every root response index,

    b P_raw = P_tensor b,
    H_r P_raw = P_tensor H_r,       r=0,1,2,3,
    C P_const = P_tensor C,

where C is the Q plus twelve eta-residual constant block.  It also checks
the corresponding Reynolds-summed identities and invariance of Delta_4.
Consequently an affine full raw preimage averages to an invariant affine
preimage, and a common linear quotient action preserves the rank-one
necessary condition.  This is an affine necessary-condition compression,
not a claim that the full bilinear legal lift equation is Reynolds-equivalent
and not a projective-boundary classification.
"""

from __future__ import annotations

import json
from itertools import combinations, permutations, product


MODES = tuple(range(4))
COLOURS = tuple(range(3))
WORDS = tuple(product(COLOURS, repeat=4))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}
PAIRS = tuple(combinations(MODES, 2))
PERMUTATIONS_3 = tuple(permutations((1, 2, 3)))
PERMUTATIONS_4 = tuple(permutations(MODES))
XI = (1, 1, 1, -1)
ETA = (1, 1, 1, 1)


# A sparse integer polynomial is a dict monomial -> coefficient.  The
# monomial is a sorted tuple of formal port-entry atoms.  This is enough for
# the multilinear permanent/cofactor identities and keeps the audit in the
# standard library.
Poly = dict[tuple[str, ...], int]
ZERO: Poly = {}
ONE: Poly = {(): 1}


def const(value: int) -> Poly:
    return {} if value == 0 else {(): value}


def atom(name: str) -> Poly:
    return {(name,): 1}


def add(left: Poly, right: Poly) -> Poly:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def scale(value: Poly, coefficient: int) -> Poly:
    if coefficient == 0 or not value:
        return {}
    return {monomial: coefficient * value0 for monomial, value0 in value.items()}


def multiply(left: Poly, right: Poly) -> Poly:
    if not left or not right:
        return {}
    result: Poly = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] = result.get(monomial, 0) + (
                left_coefficient * right_coefficient
            )
    return {monomial: value for monomial, value in result.items() if value}


def sum_polys(values) -> Poly:
    result: Poly = {}
    for value in values:
        result = add(result, value)
    return result


def product_polys(values) -> Poly:
    result = ONE
    for value in values:
        result = multiply(result, value)
    return result


def permanent(columns: list[list[Poly]]) -> Poly:
    assert len(columns) == 4 and all(len(column) == 4 for column in columns)
    return sum_polys(
        product_polys(columns[column][sigma[column]] for column in MODES)
        for sigma in PERMUTATIONS_4
    )


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for offset in range(1, len(vertices)):
        second = vertices[offset]
        remainder = vertices[1:offset] + vertices[offset + 1 :]
        for matching in perfect_matchings(remainder):
            yield ((first, second),) + matching


MATCHINGS = tuple(perfect_matchings(tuple(range(10))))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}


def raw_descriptors():
    descriptors = [("q",)]
    descriptors.extend(
        ("residual", residual, mode, colour)
        for residual in range(2)
        for mode in MODES
        for colour in COLOURS
    )
    descriptors.extend(
        ("pair", modes, colours)
        for modes in PAIRS
        for colours in product(COLOURS, repeat=2)
    )
    assert len(descriptors) == 79
    return tuple(descriptors)


RAW_DESCRIPTORS = raw_descriptors()
RAW_INDEX = {descriptor: index for index, descriptor in enumerate(RAW_DESCRIPTORS)}


def port_vector(mode: int, colour: int) -> list[Poly]:
    # Class zero is the centre frame; class one is the common leaf frame.
    frame_class = 0 if mode == 0 else 1
    return [atom(f"p{frame_class}_{colour}_{row}") for row in range(4)]


def constant_vector(values: tuple[int, ...]) -> list[Poly]:
    return [const(value) for value in values]


def nuisance_columns() -> list[list[Poly]]:
    columns: list[list[Poly]] = []

    q_column = [
        permanent([port_vector(mode, word[mode]) for mode in MODES]) for word in WORDS
    ]
    columns.append(q_column)

    for residual_values in (XI, ETA):
        residual = constant_vector(residual_values)
        for labelled_mode in MODES:
            companion_modes = tuple(mode for mode in MODES if mode != labelled_mode)
            for labelled_colour in COLOURS:
                column = []
                for word in WORDS:
                    if word[labelled_mode] != labelled_colour:
                        column.append({})
                        continue
                    column.append(
                        permanent(
                            [
                                residual,
                                *[
                                    port_vector(mode, word[mode])
                                    for mode in companion_modes
                                ],
                            ]
                        )
                    )
                columns.append(column)

    for labelled_modes in PAIRS:
        companion_modes = tuple(mode for mode in MODES if mode not in labelled_modes)
        for labelled_colours in product(COLOURS, repeat=2):
            column = []
            for word in WORDS:
                if any(
                    word[mode] != colour
                    for mode, colour in zip(
                        labelled_modes, labelled_colours, strict=True
                    )
                ):
                    column.append({})
                    continue
                column.append(
                    permanent(
                        [
                            constant_vector(XI),
                            constant_vector(ETA),
                            port_vector(companion_modes[0], word[companion_modes[0]]),
                            port_vector(companion_modes[1], word[companion_modes[1]]),
                        ]
                    )
                )
            columns.append(column)

    assert len(columns) == 79 and all(len(column) == 81 for column in columns)
    return columns


def columns_to_rows(columns: list[list[Poly]]) -> list[list[Poly]]:
    return [[column[row] for column in columns] for row in range(81)]


def raw_index_for_matching(raw_edge: tuple[int, int], word: tuple[int, ...]) -> int:
    left, right = raw_edge
    if left == 5:
        port = right - 6
        return 1 + 3 * port + word[port]
    left_port = left - 6
    right_port = right - 6
    return (
        25
        + 9 * PAIR_INDEX[(left_port, right_port)]
        + 3 * word[left_port]
        + word[right_port]
    )


def response_maps() -> list[list[list[Poly]]]:
    maps = []
    for root in MODES:
        varied_edge = (root, 4)
        root_matchings = tuple(
            matching for matching in MATCHINGS if varied_edge in matching
        )
        assert len(root_matchings) == 105
        rows = []
        for word in WORDS:
            row = [{} for _ in range(79)]
            for matching in root_matchings:
                complement = tuple(edge for edge in matching if edge != varied_edge)
                if any(right < 4 for _left, right in complement):
                    continue
                raw_edges = [edge for edge in complement if edge[0] >= 5]
                assert len(raw_edges) == 1
                raw_index = raw_index_for_matching(raw_edges[0], word)
                fixed_weight = product_polys(
                    (
                        const(ETA[left_root])
                        if right_vertex == 5
                        else port_vector(right_vertex - 6, word[right_vertex - 6])[
                            left_root
                        ]
                    )
                    for left_root, right_vertex in complement
                    if left_root < 4
                )
                row[raw_index] = add(row[raw_index], fixed_weight)
            rows.append(row)
        assert len(rows) == 81 and all(len(row) == 79 for row in rows)
        maps.append(rows)
    return maps


def permute_raw_descriptor(descriptor, mode_permutation: tuple[int, ...]):
    if descriptor[0] == "q":
        return descriptor
    if descriptor[0] == "residual":
        _tag, residual, mode, colour = descriptor
        return ("residual", residual, mode_permutation[mode], colour)
    _tag, modes, colours = descriptor
    transported = sorted(
        zip(
            (mode_permutation[modes[0]], mode_permutation[modes[1]]),
            colours,
            strict=True,
        )
    )
    return (
        "pair",
        tuple(mode for mode, _colour in transported),
        tuple(colour for _mode, colour in transported),
    )


def permute_word_source_to_output(
    word: tuple[int, ...], mode_permutation: tuple[int, ...]
) -> tuple[int, ...]:
    # This is the source-to-output action corresponding to GLD75's
    # permute_tensor_modes implementation (which evaluates sources at the
    # inverse-permuted output indices).
    return tuple(word[mode_permutation[position]] for position in MODES)


def raw_action_rows(mode_permutation: tuple[int, ...]) -> tuple[int, ...]:
    # GLD76/S3 use P_raw=M.T, where M[target,source]=1.  Thus a source
    # coordinate is sent to the inverse-permuted row.
    target_of_source = [
        RAW_INDEX[permute_raw_descriptor(descriptor, mode_permutation)]
        for descriptor in RAW_DESCRIPTORS
    ]
    source_of_target = [0] * len(target_of_source)
    for source, target in enumerate(target_of_source):
        source_of_target[target] = source
    return tuple(source_of_target)


def tensor_action_rows(mode_permutation: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        WORD_INDEX[permute_word_source_to_output(word, mode_permutation)]
        for word in WORDS
    )


def right_action(matrix: list[list[Poly]], column_rows: tuple[int, ...]):
    return [
        [matrix[row][column_rows[column]] for column in range(len(column_rows))]
        for row in range(len(matrix))
    ]


def left_action(matrix: list[list[Poly]], row_targets: tuple[int, ...]):
    output = [[{} for _ in matrix[0]] for _ in matrix]
    for source, target in enumerate(row_targets):
        for column, value in enumerate(matrix[source]):
            output[target][column] = add(output[target][column], value)
    return output


def matrix_equal(left: list[list[Poly]], right: list[list[Poly]]) -> bool:
    return left == right


def matrix_sum(matrices: list[list[list[Poly]]]) -> list[list[Poly]]:
    assert matrices
    rows = len(matrices[0])
    columns = len(matrices[0][0])
    output = [[{} for _ in range(columns)] for _ in range(rows)]
    for matrix in matrices:
        assert len(matrix) == rows and len(matrix[0]) == columns
        for row in range(rows):
            for column in range(columns):
                output[row][column] = add(output[row][column], matrix[row][column])
    return output


def select_columns(matrix: list[list[Poly]], indices: tuple[int, ...]):
    return [[matrix[row][column] for column in indices] for row in range(len(matrix))]


def frame_specification() -> dict[str, object]:
    variables = tuple(f"x{index}" for index in range(15))
    centre_base = (
        ("-2-2i", "-1+2i", "3"),
        ("0", "-3+3i", "0"),
        ("0", "-1+2i", "1"),
    )
    leaf_base = (
        ("1", "1", "1"),
        ("0", "0", "1+i"),
        ("0", "1", "1"),
    )
    centre = tuple(
        tuple(
            f"{centre_base[row][column]}+{variables[3 * row + column]}"
            for column in range(3)
        )
        for row in range(3)
    )
    leaf_entries = list(leaf_base[0])
    leaf_entries.extend(
        variables[9 + 3 * (row - 1) + column] for row in (1, 2) for column in range(3)
    )
    leaf = (
        tuple(leaf_entries[:3]),
        tuple(leaf_entries[3:6]),
        tuple(leaf_entries[6:9]),
    )
    assert len(variables) == 15
    assert centre[0][0].endswith("+x0") and leaf[1][0] == "x9"
    # The equal-leaf frame tuple is the exact GLD75 chart F=(A,G,G,G).
    frames = (centre, leaf, leaf, leaf)
    assert frames[1] == frames[2] == frames[3]
    return {
        "variables": variables,
        "frame_shape": [3, 3],
        "equal_leaf_tuple": True,
        "frame_tuple": "(A,G,G,G)",
        "port_columns": {
            "centre": [[1, -1, 0, 0], [1, 0, -1, 0], [1, 0, 0, 1]],
            "leaf": [[1, -1, 0, 0], [1, 0, -1, 0], [1, 0, 0, -1]],
        },
        "adjugate_substitution": (
            "p[class,c,r]=(P_class*adj(F_class)^T)[r,c]/det(F_class)"
        ),
        "denominator_classes": ["det(A)", "det(G)", "det(G)", "det(G)"],
    }


def check() -> dict[str, object]:
    frame_data = frame_specification()
    columns = nuisance_columns()
    nuisance = columns_to_rows(columns)
    responses = response_maps()
    raw_indices = RAW_INDEX
    constant_indices = (0,) + tuple(
        raw_indices[("residual", 1, mode, colour)]
        for mode in MODES
        for colour in COLOURS
    )
    constant = select_columns(nuisance, constant_indices)

    covariance_records = []
    reynolds_records = []
    for sigma in PERMUTATIONS_3:
        mode_permutation = (0, *sigma)
        raw_rows = raw_action_rows(mode_permutation)
        tensor_rows = tensor_action_rows(mode_permutation)
        assert matrix_equal(
            right_action(nuisance, raw_rows), left_action(nuisance, tensor_rows)
        )
        for root, response in enumerate(responses):
            assert matrix_equal(
                right_action(response, raw_rows), left_action(response, tensor_rows)
            )

        constant_positions = {
            global_index: position
            for position, global_index in enumerate(constant_indices)
        }
        constant_rows = []
        for global_index in constant_indices:
            target = raw_rows[global_index]
            assert target in constant_positions
            constant_rows.append(constant_positions[target])
        assert matrix_equal(
            right_action(constant, tuple(constant_rows)),
            left_action(constant, tensor_rows),
        )

        reynolds_records.append(
            {
                "mode_permutation": mode_permutation,
                "raw_action_is_permutation": len(set(raw_rows)) == 79,
                "tensor_action_is_permutation": len(set(tensor_rows)) == 81,
            }
        )
        covariance_records.append(
            {
                "mode_permutation": mode_permutation,
                "nuisance_covariance": True,
                "individual_root_response_covariance": [True, True, True, True],
                "constant_Q_eta_submodule_preserved": True,
            }
        )

    average_nuisance_left = matrix_sum(
        [
            left_action(nuisance, tensor_action_rows((0, *sigma)))
            for sigma in PERMUTATIONS_3
        ]
    )
    average_nuisance_right = matrix_sum(
        [
            right_action(nuisance, raw_action_rows((0, *sigma)))
            for sigma in PERMUTATIONS_3
        ]
    )
    assert matrix_equal(average_nuisance_left, average_nuisance_right)

    average_response = []
    for response in responses:
        left = matrix_sum(
            [
                left_action(response, tensor_action_rows((0, *sigma)))
                for sigma in PERMUTATIONS_3
            ]
        )
        right = matrix_sum(
            [
                right_action(response, raw_action_rows((0, *sigma)))
                for sigma in PERMUTATIONS_3
            ]
        )
        assert matrix_equal(left, right)
        average_response.append(True)

    diagonal = [
        {(): 1} if word[0] == word[1] == word[2] == word[3] else {} for word in WORDS
    ]
    for sigma in PERMUTATIONS_3:
        assert left_action(
            [[entry] for entry in diagonal], tensor_action_rows((0, *sigma))
        ) == [[entry] for entry in diagonal]

    return {
        "status": "exact_symbolic_moving_response_covariance_reduction",
        "field": "Z_then_Q(i)_then_C",
        "formal_ring": "Z[p_class_colour_row]",
        "frame_setup": frame_data,
        "leaf_permutation_count": len(PERMUTATIONS_3),
        "nuisance_shape": [81, 79],
        "response_shapes": [[81, 79] for _ in responses],
        "constant_block_shape": [81, 13],
        "constant_block": "Q plus twelve eta-residual columns",
        "covariance": covariance_records,
        "reynolds_sum_nuisance_identity": True,
        "reynolds_sum_response_identities": average_response,
        "delta4_invariant": True,
        "root_index_fixed_under_leaf_action": True,
        "quotient_constant_submodule_preserved": True,
        "affine_full_to_invariant_preimage": True,
        "affine_rank_one_necessary_condition_preserved": True,
        "full_bilinear_legal_lift_reynolds_equivalence": False,
        "projective_boundary_claim": False,
        "separate_scope": [
            "This audit does not expand the universal moving 45x45 determinant.",
            "The adjugate substitution is exact on det(A)det(G)!=0; divisor closure is separate.",
            "The GLD82 builder separately constructs and validates the quotient pivot and determinant circuit.",
        ],
    }


def main() -> None:
    result = check()
    print("moving equal-leaf response covariance audit: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
