"""Independent exact audit of the GLD73 contracted edge control.

This file deliberately does not import the primary verifier, SymPy, or any
repository module.  It rebuilds the four-port permanent map, the Gaussian
frames, the raw coefficient lift, the ten-vertex matching contraction, and
the six first-transverse response ranks using only standard-library exact
arithmetic over Q(i).
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import combinations, permutations, product


Gaussian = tuple[Fraction, Fraction]
ZERO: Gaussian = (Fraction(0), Fraction(0))
ONE: Gaussian = (Fraction(1), Fraction(0))
LOCAL_INDICES = tuple(product(range(3), repeat=4))
LOCAL_INDEX = {word: index for index, word in enumerate(LOCAL_INDICES)}
PERMUTATIONS_3 = tuple(permutations(range(3)))
PERMUTATIONS_4 = tuple(permutations(range(4)))
MODES = tuple(range(4))
PAIRS = tuple(combinations(MODES, 2))


def gi(real: int | Fraction, imaginary: int | Fraction = 0) -> Gaussian:
    return Fraction(real), Fraction(imaginary)


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gsub(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] - right[0], left[1] - right[1]


def gneg(value: Gaussian) -> Gaussian:
    return -value[0], -value[1]


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gdiv(left: Gaussian, right: Gaussian) -> Gaussian:
    norm = right[0] * right[0] + right[1] * right[1]
    assert norm
    return (
        (left[0] * right[0] + left[1] * right[1]) / norm,
        (left[1] * right[0] - left[0] * right[1]) / norm,
    )


def gsum(values) -> Gaussian:
    result = ZERO
    for value in values:
        result = gadd(result, value)
    return result


def gprod(values) -> Gaussian:
    result = ONE
    for value in values:
        result = gmul(result, value)
    return result


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def permanent4(columns: list[list[Gaussian]]) -> Gaussian:
    assert len(columns) == 4
    return gsum(
        gprod(columns[mode][permutation[mode]] for mode in range(4))
        for permutation in PERMUTATIONS_4
    )


def rank(matrix: list[list[Gaussian]]) -> int:
    """Exact Gaussian elimination, returning row/column rank."""

    if not matrix:
        return 0
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column] != ZERO),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [gdiv(value, scale) for value in work[pivot_row]]
        for row in range(pivot_row + 1, rows):
            if work[row][column] == ZERO:
                continue
            factor = work[row][column]
            work[row] = [
                gsub(value, gmul(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def solve_columns(
    columns: list[list[Gaussian]], target: list[Gaussian]
) -> tuple[list[Gaussian], tuple[int, ...]]:
    """Solve A*x=target with free variables set to zero."""

    row_count = len(target)
    column_count = len(columns)
    work = [
        [columns[column][row] for column in range(column_count)] + [target[row]]
        for row in range(row_count)
    ]
    pivot_row = 0
    pivot_columns: list[int] = []
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column] != ZERO),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [gdiv(value, scale) for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or work[row][column] == ZERO:
                continue
            factor = work[row][column]
            work[row] = [
                gsub(value, gmul(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    for row in range(pivot_row, row_count):
        assert work[row][-1] == ZERO
    solution = [ZERO] * column_count
    for row, column in enumerate(pivot_columns):
        solution[column] = work[row][-1]
    return solution, tuple(pivot_columns)


def matrix_transpose(matrix: list[list[Gaussian]]) -> list[list[Gaussian]]:
    return [list(column) for column in zip(*matrix)]


def matrix_multiply(
    left: list[list[Gaussian]], right: list[list[Gaussian]]
) -> list[list[Gaussian]]:
    assert left and right and len(left[0]) == len(right)
    return [
        [
            gsum(
                gmul(left[row][inner], right[inner][column])
                for inner in range(len(right))
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def matrix_vector(
    matrix: list[list[Gaussian]], vector: list[Gaussian]
) -> list[Gaussian]:
    return [
        gsum(gmul(value, vector[column]) for column, value in enumerate(row))
        for row in matrix
    ]


def matrix_inverse(matrix: list[list[Gaussian]]) -> list[list[Gaussian]]:
    size = len(matrix)
    work = [
        row_values[:] + [ONE if row_index == column else ZERO for column in range(size)]
        for row_index, row_values in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column] != ZERO),
            None,
        )
        assert pivot is not None
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [gdiv(value, scale) for value in work[column]]
        for row in range(size):
            if row == column or work[row][column] == ZERO:
                continue
            factor = work[row][column]
            work[row] = [
                gsub(value, gmul(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[column], strict=True)
            ]
    return [row[size:] for row in work]


def determinant3(matrix: list[list[Gaussian]]) -> Gaussian:
    return gsum(
        gmul(
            gi(permutation_sign(permutation)),
            gprod(matrix[row][permutation[row]] for row in range(3)),
        )
        for permutation in PERMUTATIONS_3
    )


def linear_combination(
    columns: list[list[Gaussian]], coefficients: list[Gaussian]
) -> list[Gaussian]:
    return [
        gsum(
            gmul(column[row], coefficients[index])
            for index, column in enumerate(columns)
        )
        for row in range(len(columns[0]))
    ]


def vector(*entries: int) -> list[Gaussian]:
    return [gi(entry) for entry in entries]


def canonical_torus_star() -> tuple[
    list[Gaussian], list[Gaussian], list[list[list[Gaussian]]]
]:
    xi = vector(1, 1, 1, -1)
    eta = vector(1, 1, 1, 1)
    radical0 = vector(1, -1, 0, 0)
    radical1 = vector(1, 0, -1, 0)
    centre = vector(1, 0, 0, 1)
    leaf = vector(1, 0, 0, -1)
    ports = [
        [radical0, radical1, centre],
        [radical0, radical1, leaf],
        [radical0, radical1, leaf],
        [radical0, radical1, leaf],
    ]
    return xi, eta, ports


def build_q_layer_columns(
    xi: list[Gaussian],
    eta: list[Gaussian],
    ports: list[list[list[Gaussian]]],
) -> list[list[Gaussian]]:
    columns: list[list[Gaussian]] = []
    columns.append(
        [
            permanent4([ports[mode][word[mode]] for mode in MODES])
            for word in LOCAL_INDICES
        ]
    )
    for residual in (xi, eta):
        for labelled_mode in MODES:
            for labelled_index in range(3):
                column = [ZERO] * len(LOCAL_INDICES)
                for row, word in enumerate(LOCAL_INDICES):
                    if word[labelled_mode] != labelled_index:
                        continue
                    companion = [
                        residual,
                        *[
                            ports[mode][word[mode]]
                            for mode in MODES
                            if mode != labelled_mode
                        ],
                    ]
                    column[row] = permanent4(companion)
                columns.append(column)
    for left_mode, right_mode in PAIRS:
        for left_index, right_index in product(range(3), repeat=2):
            column = [ZERO] * len(LOCAL_INDICES)
            for row, word in enumerate(LOCAL_INDICES):
                if word[left_mode] != left_index or word[right_mode] != right_index:
                    continue
                companions = [
                    xi,
                    eta,
                    *[
                        ports[mode][word[mode]]
                        for mode in MODES
                        if mode not in (left_mode, right_mode)
                    ],
                ]
                column[row] = permanent4(companions)
            columns.append(column)
    assert len(columns) == 79
    return columns


def frame_tensor(
    centre: list[list[Gaussian]], leaf: list[list[Gaussian]]
) -> list[Gaussian]:
    return [
        gsum(
            gprod(
                (
                    centre[word[0]][colour],
                    leaf[word[1]][colour],
                    leaf[word[2]][colour],
                    leaf[word[3]][colour],
                )
            )
            for colour in range(3)
        )
        for word in LOCAL_INDICES
    ]


def act_on_tensor(
    tensor: list[Gaussian], maps: tuple[list[list[Gaussian]], ...]
) -> list[Gaussian]:
    return [
        gsum(
            gprod(
                [maps[mode][output[mode]][source[mode]] for mode in MODES]
                + [tensor[LOCAL_INDEX[source]]]
            )
            for source in LOCAL_INDICES
        )
        for output in LOCAL_INDICES
    ]


def transform_ports(
    ports: list[list[list[Gaussian]]],
    inverse_frames: tuple[list[list[Gaussian]], ...],
) -> list[list[list[Gaussian]]]:
    transformed = []
    for port, inverse in zip(ports, inverse_frames, strict=True):
        matrix = [[port[column][row] for column in range(3)] for row in range(4)]
        new_matrix = matrix_multiply(matrix, matrix_transpose(inverse))
        transformed.append(
            [[new_matrix[row][column] for row in range(4)] for column in range(3)]
        )
    return transformed


def transform_coefficients(
    coefficients: list[Gaussian],
    inverse_frames: tuple[list[list[Gaussian]], ...],
) -> list[Gaussian]:
    output = [coefficients[0]]
    offset = 1
    for _residual in range(2):
        for mode in MODES:
            output.extend(
                matrix_vector(inverse_frames[mode], coefficients[offset : offset + 3])
            )
            offset += 3
    for left_mode, right_mode in PAIRS:
        old = [
            coefficients[offset + 3 * row : offset + 3 * row + 3] for row in range(3)
        ]
        new = matrix_multiply(
            matrix_multiply(inverse_frames[left_mode], old),
            matrix_transpose(inverse_frames[right_mode]),
        )
        output.extend(value for row in new for value in row)
        offset += 9
    assert len(output) == 79
    return output


def target_delta() -> list[Gaussian]:
    return [
        ONE if word[0] == word[1] == word[2] == word[3] else ZERO
        for word in LOCAL_INDICES
    ]


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


def coefficient_hash(coefficients: list[Gaussian]) -> str:
    serial = "\n".join(
        f"{real.numerator}/{real.denominator},{imaginary.numerator}/{imaginary.denominator}"
        for real, imaginary in coefficients
    )
    return hashlib.sha256(serial.encode()).hexdigest()


def check() -> dict[str, object]:
    centre = [
        [gi(-2, -2), gi(-1, 2), gi(3)],
        [gi(0), gi(-3, 3), gi(0)],
        [gi(0), gi(-1, 2), gi(1)],
    ]
    leaf = [
        [gi(1), gi(1), gi(1)],
        [gi(0), gi(0), gi(1, 1)],
        [gi(0), gi(1), gi(1)],
    ]
    assert determinant3(centre) == gi(12)
    assert determinant3(leaf) == gi(-1, -1)
    frames = (centre, leaf, leaf, leaf)
    inverse_frames = tuple(matrix_inverse(frame) for frame in frames)
    survivor = frame_tensor(centre, leaf)
    target = target_delta()
    assert act_on_tensor(survivor, inverse_frames) == target
    assert sum(value != ZERO for value in survivor) == 61

    xi, eta, ports = canonical_torus_star()
    original_columns = build_q_layer_columns(xi, eta, ports)
    assert rank([list(row) for row in zip(*original_columns)]) == 44
    original_coefficients, pivot_columns = solve_columns(original_columns, survivor)
    assert len(pivot_columns) == 44
    assert linear_combination(original_columns, original_coefficients) == survivor
    assert sum(value != ZERO for value in original_coefficients) == 37

    transformed_ports = transform_ports(ports, inverse_frames)
    transformed_columns = build_q_layer_columns(xi, eta, transformed_ports)
    transformed_coefficients = transform_coefficients(
        original_coefficients, inverse_frames
    )
    assert linear_combination(transformed_columns, transformed_coefficients) == target

    q_value = transformed_coefficients[0]
    residual_values = transformed_coefficients[1:25]
    pair_values = transformed_coefficients[25:]
    residual_vectors = {}
    offset = 0
    for residual_name in ("xi", "eta"):
        for mode in MODES:
            residual_vectors[(residual_name, mode)] = residual_values[
                offset : offset + 3
            ]
            offset += 3
    pair_matrices = {}
    offset = 0
    for pair in PAIRS:
        pair_matrices[pair] = [
            pair_values[offset + 3 * row : offset + 3 * row + 3] for row in range(3)
        ]
        offset += 9

    matchings = tuple(perfect_matchings(tuple(range(10))))
    assert len(matchings) == 945
    port_words = tuple(product(range(3), repeat=4))

    def effective_edge(left: int, right: int, word: tuple[int, ...]) -> Gaussian:
        if left > right:
            left, right = right, left
        if right < 4:
            return ZERO
        if left < 4:
            if right == 4:
                return xi[left]
            if right == 5:
                return eta[left]
            return transformed_ports[right - 6][word[right - 6]][left]
        if (left, right) == (4, 5):
            return q_value
        if left in (4, 5):
            port = right - 6
            # q0-port leaves q1 in the companion and uses eta;
            # q1-port leaves q0 and uses xi.
            residual_name = "eta" if left == 4 else "xi"
            assert residual_name == ("eta" if left == 4 else "xi")
            return residual_vectors[(residual_name, port)][word[port]]
        return pair_matrices[(left - 6, right - 6)][word[left - 6]][word[right - 6]]

    contracted = [
        gsum(
            gprod(effective_edge(left, right, word) for left, right in matching)
            for matching in matchings
        )
        for word in port_words
    ]
    assert contracted == target

    # Build an actual edge-block lift with literal all-one contraction vectors.
    # Every root-incident block has root row 1 equal to zero; every q-incident
    # block has q row 1 equal to zero.  This is enough to force the global
    # all-one coefficient to vanish while preserving the displayed fibre.
    blocks: dict[tuple[int, int], list[list[Gaussian]]] = {}
    closed_weights = [ONE, ONE, ONE]
    assert all(weight == ONE for weight in closed_weights)

    def zero_block() -> list[list[Gaussian]]:
        return [[ZERO for _ in range(3)] for _ in range(3)]

    for left, right in combinations(range(10), 2):
        block = zero_block()
        if left < 4 and right < 4:
            pass
        elif left < 4 and right == 4:
            block[0][0] = xi[left]
        elif left < 4 and right == 5:
            block[0][0] = eta[left]
        elif left < 4:
            port = right - 6
            for colour in range(3):
                block[0][colour] = transformed_ports[port][colour][left]
        elif (left, right) == (4, 5):
            block[0][0] = q_value
        elif left in (4, 5):
            port = right - 6
            residual_name = "eta" if left == 4 else "xi"
            assert residual_name == ("eta" if left == 4 else "xi")
            for colour in range(3):
                block[0][colour] = residual_vectors[(residual_name, port)][colour]
        else:
            block = [row[:] for row in pair_matrices[(left - 6, right - 6)]]
        blocks[(left, right)] = block

    # Recheck every effective scalar by contracting the six closed vertices
    # with (1,1,1), rather than trusting the effective-edge definition.
    for left, right in combinations(range(10), 2):
        block = blocks[(left, right)]
        for word in port_words:
            if left < 6 and right < 6:
                value = gsum(
                    gprod(
                        (
                            closed_weights[row],
                            block[row][column],
                            closed_weights[column],
                        )
                    )
                    for row in range(3)
                    for column in range(3)
                )
            elif left < 6:
                value = gsum(
                    gprod((closed_weights[row], block[row][word[right - 6]]))
                    for row in range(3)
                )
            else:
                value = block[word[left - 6]][word[right - 6]]
            assert value == effective_edge(left, right, word)

    all_one_word = (1,) * 10
    global_all_one = gsum(
        gprod(
            blocks[(left, right)][all_one_word[left]][all_one_word[right]]
            for left, right in matching
        )
        for matching in matchings
    )
    assert global_all_one == ZERO

    effective_values = {
        (left, right, word): effective_edge(left, right, word)
        for left, right in combinations(range(10), 2)
        for word in port_words
    }
    mixed_row_indices = [
        index for index, word in enumerate(port_words) if len(set(word)) != 1
    ]
    response_ranks = []
    for varied in range(6):
        edge_sums = {}
        parameter_labels = []
        for neighbor in range(10):
            if neighbor == varied:
                continue
            edge = tuple(sorted((varied, neighbor)))
            containing = [matching for matching in matchings if edge in matching]
            assert len(containing) == 105
            edge_sums[neighbor] = [
                gsum(
                    gprod(
                        effective_values[(left, right, word)]
                        for left, right in matching
                        if (left, right) != edge
                    )
                    for matching in containing
                )
                for word in port_words
            ]
            if neighbor < 6:
                parameter_labels.append((neighbor, None))
            else:
                parameter_labels.extend((neighbor, colour) for colour in range(3))
        assert len(parameter_labels) == 17

        columns = []
        for neighbor, selected_colour in parameter_labels:
            values = edge_sums[neighbor]
            if selected_colour is None:
                columns.append(values)
            else:
                columns.append(
                    [
                        value if word[neighbor - 6] == selected_colour else ZERO
                        for value, word in zip(values, port_words, strict=True)
                    ]
                )
        derivative_rows = [[column[row] for column in columns] for row in range(81)]
        full_rank = rank(derivative_rows)
        mixed_rank = rank([derivative_rows[row] for row in mixed_row_indices])
        base_parameters = []
        for neighbor, selected_colour in parameter_labels:
            if selected_colour is None:
                word = (0, 0, 0, 0)
            else:
                mutable = [0, 0, 0, 0]
                mutable[neighbor - 6] = selected_colour
                word = tuple(mutable)
            base_parameters.append(
                effective_values[tuple(sorted((varied, neighbor))) + (word,)]
            )
        assert linear_combination(columns, base_parameters) == target
        response_ranks.append((full_rank, mixed_rank, full_rank - mixed_rank))

    assert response_ranks == [(17, 16, 1)] * 6
    return {
        "status": "independent_exact_single_fibre_control_and_pointwise_first_transverse_nonextension",
        "global_conjecture": "UNRESOLVED",
        "permanent_map_columns": 79,
        "permanent_map_rank": 44,
        "original_pivot_columns": len(pivot_columns),
        "original_raw_nonzero": sum(value != ZERO for value in original_coefficients),
        "transformed_raw_sha256": coefficient_hash(transformed_coefficients),
        "transformed_raw_nonzero": sum(
            value != ZERO for value in transformed_coefficients
        ),
        "transformed_q_residual_pair_nonzero": (
            int(q_value != ZERO),
            sum(value != ZERO for value in residual_values),
            sum(value != ZERO for value in pair_values),
        ),
        "contraction_vectors": "six literal (1,1,1) vectors",
        "q_edge_convention": "q0-port=eta, q1-port=xi",
        "ten_vertex_perfect_matchings": len(matchings),
        "contracted_target": "literal unweighted Delta_3 on four ports",
        "first_transverse_full_mixed_diagonal_image_ranks": response_ranks,
        "global_all_one_coefficient": "0"
        if global_all_one == ZERO
        else str(global_all_one),
        "root_order_four_maximality_certified": False,
        "fifth_root_excluded": False,
        "full_35d_raw_coefficient_fibre_excluded": False,
        "graph_witness_proved": False,
    }


def main() -> None:
    result = check()
    print("independent GLD73 contracted edge and transverse audit: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
