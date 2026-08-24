"""Exact replay for the GLD70 complete-Q-layer secant reduction."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product

Q = Fraction
MODES = tuple(range(4))
LOCAL_INDICES = tuple(product(range(3), repeat=4))
LOCAL_INDEX = {indices: offset for offset, indices in enumerate(LOCAL_INDICES)}
PERMUTATIONS_3 = tuple(permutations(range(3)))
PERMUTATIONS_4 = tuple(permutations(range(4)))
PAIRS = tuple(combinations(MODES, 2))

STAR_PIVOT_COLUMNS = (
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    37,
    38,
    40,
    41,
    43,
    44,
    46,
    47,
    49,
)
STAR_PIVOT_ROWS = (
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    17,
    18,
    19,
    20,
    23,
    24,
    25,
    26,
    28,
    29,
    35,
    41,
    44,
    47,
    50,
    51,
    52,
    53,
    55,
    56,
    60,
    62,
    71,
    72,
    74,
    77,
    78,
    79,
    80,
)
STAR_MINOR_CONSTANT = 510015580149921683079168


def vector(*entries: int) -> list[Q]:
    return [Q(entry) for entry in entries]


def permutation_sign(sigma: tuple[int, ...]) -> int:
    inversions = sum(
        sigma[left] > sigma[right]
        for left in range(len(sigma))
        for right in range(left + 1, len(sigma))
    )
    return -1 if inversions % 2 else 1


def permanent(columns: list[list[Q]]) -> Q:
    assert len(columns) == 4
    return sum(
        (
            columns[0][sigma[0]]
            * columns[1][sigma[1]]
            * columns[2][sigma[2]]
            * columns[3][sigma[3]]
        )
        for sigma in PERMUTATIONS_4
    )


def matrix_rank(rows: list[list[Q]]) -> int:
    matrix = [row[:] for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(pivot_row + 1, len(matrix)):
            if not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def pivot_columns(rows: list[list[Q]]) -> tuple[int, ...]:
    matrix = [row[:] for row in rows]
    if not matrix:
        return ()
    pivots: list[int] = []
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return tuple(pivots)


def column_rows(columns: list[list[Q]]) -> list[list[Q]]:
    return [[column[row] for column in columns] for row in range(len(LOCAL_INDICES))]


def column_rank(columns: list[list[Q]]) -> int:
    return matrix_rank(column_rows(columns))


def flatten_layers(
    layers: tuple[list[list[Q]], list[list[Q]], list[list[Q]]],
) -> list[list[Q]]:
    return [column for layer in layers for column in layer]


def determinant_bareiss(rows: list[list[int]]) -> int:
    matrix = [row[:] for row in rows]
    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    if size == 0:
        return 1
    sign = 1
    previous = 1
    for column in range(size - 1):
        pivot = next((row for row in range(column, size) if matrix[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            sign *= -1
        pivot_value = matrix[column][column]
        for row in range(column + 1, size):
            for offset in range(column + 1, size):
                numerator = (
                    matrix[row][offset] * pivot_value
                    - matrix[row][column] * matrix[column][offset]
                )
                assert numerator % previous == 0
                matrix[row][offset] = numerator // previous
            matrix[row][column] = 0
        previous = pivot_value
    return sign * matrix[-1][-1]


def full_q_layer_columns(
    xi: list[Q], eta: list[Q], ports: list[list[list[Q]]]
) -> tuple[list[list[Q]], list[list[Q]], list[list[Q]]]:
    """Return the Q, residual-port, and port-pair raw column families."""

    q_column = [
        permanent([ports[mode][indices[mode]] for mode in MODES])
        for indices in LOCAL_INDICES
    ]

    residual_columns: list[list[Q]] = []
    for residual in (xi, eta):
        for labelled_mode in MODES:
            companion_modes = tuple(mode for mode in MODES if mode != labelled_mode)
            for labelled_index in range(3):
                column = [Q(0)] * len(LOCAL_INDICES)
                for companion_indices in product(range(3), repeat=3):
                    indices = [0] * 4
                    indices[labelled_mode] = labelled_index
                    for mode, index in zip(
                        companion_modes, companion_indices, strict=True
                    ):
                        indices[mode] = index
                    column[LOCAL_INDEX[tuple(indices)]] = permanent(
                        [residual]
                        + [ports[mode][indices[mode]] for mode in companion_modes]
                    )
                residual_columns.append(column)

    pair_columns: list[list[Q]] = []
    for labelled_modes in PAIRS:
        companion_modes = tuple(mode for mode in MODES if mode not in labelled_modes)
        for labelled_indices in product(range(3), repeat=2):
            column = [Q(0)] * len(LOCAL_INDICES)
            for companion_indices in product(range(3), repeat=2):
                indices = [0] * 4
                for mode, index in zip(labelled_modes, labelled_indices, strict=True):
                    indices[mode] = index
                for mode, index in zip(companion_modes, companion_indices, strict=True):
                    indices[mode] = index
                column[LOCAL_INDEX[tuple(indices)]] = permanent(
                    [
                        xi,
                        eta,
                        ports[companion_modes[0]][companion_indices[0]],
                        ports[companion_modes[1]][companion_indices[1]],
                    ]
                )
            pair_columns.append(column)

    assert (len([q_column]), len(residual_columns), len(pair_columns)) == (1, 24, 54)
    return [q_column], residual_columns, pair_columns


def diagonal_columns() -> list[list[Q]]:
    return [
        [Q(all(index == colour for index in indices)) for indices in LOCAL_INDICES]
        for colour in range(3)
    ]


def weighted_diagonal(weights: tuple[int, int, int]) -> list[Q]:
    diagonal = diagonal_columns()
    return [
        sum(Q(weights[colour]) * diagonal[colour][row] for colour in range(3))
        for row in range(len(LOCAL_INDICES))
    ]


def tensor_from_terms(
    terms: list[tuple[Q, tuple[list[Q], list[Q], list[Q], list[Q]]]],
) -> list[Q]:
    return [
        sum(
            coefficient
            * factors[0][indices[0]]
            * factors[1][indices[1]]
            * factors[2][indices[2]]
            * factors[3][indices[3]]
            for coefficient, factors in terms
        )
        for indices in LOCAL_INDICES
    ]


def epsilon(tensor: list[Q]) -> Q:
    """Degree-three four-qutrit epsilon contraction, fixing mode zero."""

    total = Q(0)
    for sigma_1, sigma_2, sigma_3 in product(PERMUTATIONS_3, repeat=3):
        term = Q(
            permutation_sign(sigma_1)
            * permutation_sign(sigma_2)
            * permutation_sign(sigma_3)
        )
        for colour in range(3):
            term *= tensor[
                LOCAL_INDEX[
                    (
                        colour,
                        sigma_1[colour],
                        sigma_2[colour],
                        sigma_3[colour],
                    )
                ]
            ]
        total += term
    return 6 * total


def determinant_3(matrix: list[list[Q]]) -> Q:
    return sum(
        Q(permutation_sign(sigma))
        * matrix[0][sigma[0]]
        * matrix[1][sigma[1]]
        * matrix[2][sigma[2]]
        for sigma in PERMUTATIONS_3
    )


def balanced_flattening_rank(tensor: list[Q], left_modes: tuple[int, int]) -> int:
    right_modes = tuple(mode for mode in MODES if mode not in left_modes)
    rows: list[list[Q]] = []
    for left_indices in product(range(3), repeat=2):
        row: list[Q] = []
        for right_indices in product(range(3), repeat=2):
            indices = [0] * 4
            for mode, index in zip(left_modes, left_indices, strict=True):
                indices[mode] = index
            for mode, index in zip(right_modes, right_indices, strict=True):
                indices[mode] = index
            row.append(tensor[LOCAL_INDEX[tuple(indices)]])
        rows.append(row)
    return matrix_rank(rows)


def canonical_torus_star(
    slope: int,
) -> tuple[list[Q], list[Q], list[list[list[Q]]]]:
    xi = vector(1, 1, 1, -1)
    eta = vector(1, 1, 1, 1)
    radical_0 = vector(1, -1, 0, 0)
    radical_1 = vector(1, 0, -1, 0)
    centre = vector(1, 0, 0, slope)
    leaf = vector(1, 0, 0, -slope)
    ports = [
        [radical_0, radical_1, centre],
        [radical_0, radical_1, leaf],
        [radical_0, radical_1, leaf],
        [radical_0, radical_1, leaf],
    ]
    return xi, eta, ports


def scalar_zero_star() -> tuple[list[Q], list[Q], list[list[list[Q]]]]:
    xi = vector(0, 0, 0, 1)
    eta = vector(0, 0, 1, 0)
    radical_0 = vector(0, 0, 1, 0)
    radical_1 = vector(0, 0, 0, 1)
    centre = vector(1, 1, 0, 0)
    leaf = vector(1, -1, 0, 0)
    ports = [
        [radical_0, radical_1, centre],
        [radical_0, radical_1, leaf],
        [leaf, radical_0, radical_1],
        [radical_0, leaf, radical_1],
    ]
    return xi, eta, ports


def projection_full_triangle() -> tuple[list[Q], list[Q], list[list[list[Q]]]]:
    xi = vector(0, 0, 1, 1)
    eta = vector(1, 1, 0, 0)
    radical = vector(1, -1, 0, 0)
    siblings = [radical, vector(0, 0, 1, 0), vector(0, 0, 0, 1)]
    centre = [
        vector(1, 0, 1, 0),
        vector(0, 1, 0, 0),
        vector(0, 0, 0, 1),
    ]
    return xi, eta, [centre, siblings, siblings, siblings]


def check_epsilon_open_orbit() -> tuple[Q, Q, tuple[Q, Q, Q, Q]]:
    basis = [vector(1, 0, 0), vector(0, 1, 0), vector(0, 0, 1)]
    matrices = [
        [vector(1, 0, 0), vector(1, 1, 0), vector(0, 1, 1)],
        [vector(1, 1, 0), vector(0, 1, 1), vector(1, 0, 1)],
        [vector(2, 0, 1), vector(1, 1, 0), vector(0, 1, 1)],
        [vector(1, 0, 1), vector(0, 2, 1), vector(1, 1, 0)],
    ]
    weights = (Q(2), Q(-3), Q(5))
    honest = tensor_from_terms(
        [
            (
                weights[colour],
                tuple(matrices[mode][colour] for mode in MODES),
            )
            for colour in range(3)
        ]
    )
    expected = 6 * weights[0] * weights[1] * weights[2]
    for matrix in matrices:
        # Stored vectors are columns; transpose for determinant_3.
        expected *= determinant_3(
            [[matrix[column][row] for column in range(3)] for row in range(3)]
        )
    assert epsilon(honest) == expected

    delta = tensor_from_terms([(Q(1), (basis[colour],) * 4) for colour in range(3)])
    sigma_2 = tensor_from_terms([(Q(1), (basis[colour],) * 4) for colour in range(2)])

    type_ii_terms = []
    for mode in MODES:
        factors = [basis[0]] * 4
        factors[mode] = basis[1]
        type_ii_terms.append((Q(1), tuple(factors)))
    type_ii_terms.append((Q(1), (basis[2],) * 4))

    type_iii_terms = []
    for left, right in PAIRS:
        factors = [basis[0]] * 4
        factors[left] = basis[1]
        factors[right] = basis[1]
        type_iii_terms.append((Q(1), tuple(factors)))
    for mode in MODES:
        factors = [basis[0]] * 4
        factors[mode] = basis[2]
        type_iii_terms.append((Q(1), tuple(factors)))

    type_iv_terms = []
    for mode in (1, 2, 3):
        factors = [basis[0]] * 4
        factors[0] = basis[1]
        factors[mode] = basis[1]
        type_iv_terms.append((Q(1), tuple(factors)))
    for mode in MODES:
        factors = [basis[0]] * 4
        factors[mode] = basis[2]
        type_iv_terms.append((Q(1), tuple(factors)))

    boundary_values = (
        epsilon(sigma_2),
        epsilon(tensor_from_terms(type_ii_terms)),
        epsilon(tensor_from_terms(type_iii_terms)),
        epsilon(tensor_from_terms(type_iv_terms)),
    )
    assert epsilon(delta) == 6
    assert boundary_values == (Q(0), Q(0), Q(0), Q(0))
    return epsilon(delta), expected, boundary_values


def check_complete_layer_controls() -> dict[str, tuple[int, ...]]:
    controls = {
        "scalar_zero_star": scalar_zero_star(),
        "torus_star": canonical_torus_star(1),
        "projection_full_triangle": projection_full_triangle(),
    }
    expected = {
        "scalar_zero_star": (16, 21, 21, 24, 22, 22, 22, 22),
        "torus_star": (24, 21, 44, 46, 45, 45, 44, 45),
        "projection_full_triangle": (22, 19, 35, 38, 36, 36, 36, 36),
    }
    diagonal = diagonal_columns()
    target = weighted_diagonal((1, 2, 3))
    results: dict[str, tuple[int, ...]] = {}
    for name, data in controls.items():
        q_columns, residual_columns, pair_columns = full_q_layer_columns(*data)
        nuisance = q_columns + residual_columns + pair_columns
        result = (
            column_rank(q_columns + residual_columns),
            column_rank(pair_columns),
            column_rank(nuisance),
            column_rank(nuisance + diagonal),
            *(column_rank(nuisance + [column]) for column in diagonal),
            column_rank(nuisance + [target]),
        )
        assert result == expected[name]
        results[name] = result
    return results


def check_torus_star_compression() -> tuple[int, int, int]:
    columns_at_one = flatten_layers(full_q_layer_columns(*canonical_torus_star(1)))
    columns_at_zero = flatten_layers(full_q_layer_columns(*canonical_torus_star(0)))
    columns_at_two = flatten_layers(full_q_layer_columns(*canonical_torus_star(2)))
    assert len(columns_at_one) == 79

    rows_at_one = column_rows(columns_at_one)
    pivots = pivot_columns(rows_at_one)
    assert pivots == STAR_PIVOT_COLUMNS
    basis = [columns_at_one[index] for index in pivots]
    pivot_rows = pivot_columns(
        [[basis[column][row] for row in range(81)] for column in range(44)]
    )
    assert pivot_rows == STAR_PIVOT_ROWS
    assert column_rank(basis) == 44

    # Each raw column is affine in h.  The h=0 coefficients already lie in
    # N(1), hence every N(h) is contained in that fixed 44-space.
    assert all(
        twice == 2 * at_one - at_zero
        for column_zero, column_one, column_two in zip(
            columns_at_zero, columns_at_one, columns_at_two, strict=True
        )
        for at_zero, at_one, twice in zip(
            column_zero, column_one, column_two, strict=True
        )
    )
    assert column_rank(basis + columns_at_zero) == 44

    # Every entry of the pinned 44-square minor is affine in h, so its
    # determinant has degree at most 44.  Agreement at 45 integer values
    # certifies det=C*h^33 as a polynomial identity over characteristic zero.
    evaluations = 0
    for slope in range(45):
        columns = flatten_layers(full_q_layer_columns(*canonical_torus_star(slope)))
        square = [
            [int(columns[column][row]) for column in STAR_PIVOT_COLUMNS]
            for row in STAR_PIVOT_ROWS
        ]
        value = determinant_bareiss(square)
        assert value == STAR_MINOR_CONSTANT * slope**33
        evaluations += 1
    assert evaluations == 45
    return len(pivots), evaluations, STAR_MINOR_CONSTANT


def check_q_generator_boundary() -> tuple[Q, tuple[int, int, int]]:
    q_columns, _residual_columns, _pair_columns = full_q_layer_columns(
        *canonical_torus_star(1)
    )
    q_tensor = q_columns[0]
    value = epsilon(q_tensor)
    flattening_ranks = tuple(
        balanced_flattening_rank(q_tensor, modes) for modes in ((0, 1), (0, 2), (0, 3))
    )
    assert value == -288
    assert flattening_ranks == (5, 5, 5)
    return value, flattening_ranks


def main() -> None:
    epsilon_checks = check_epsilon_open_orbit()
    controls = check_complete_layer_controls()
    compression = check_torus_star_compression()
    q_boundary = check_q_generator_boundary()
    print("four-root complete-Q-layer secant reduction: PASS")
    print("  epsilon target / honest / boundary:", epsilon_checks)
    print("  exact layer ranks:", controls)
    print("  torus-star rank / determinant samples / constant:", compression)
    print("  Q-only epsilon / balanced ranks:", q_boundary)


if __name__ == "__main__":
    main()
