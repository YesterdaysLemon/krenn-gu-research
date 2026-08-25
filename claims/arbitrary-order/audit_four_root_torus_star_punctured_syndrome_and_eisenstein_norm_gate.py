"""Independent no-import audit of the GLD71 punctured-syndrome gate."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product

Q = Fraction
MODES = (0, 1, 2, 3)
LEAVES = (1, 2, 3)
WORDS = tuple(product(range(3), repeat=4))
WORD_OFFSET = {word: offset for offset, word in enumerate(WORDS)}
PUNCTURED = tuple(
    word for word in WORDS if sum(word[leaf] == 2 for leaf in LEAVES) <= 1
)


def vec(*entries: int) -> tuple[Q, ...]:
    return tuple(Q(entry) for entry in entries)


def permanent_dp(columns: tuple[tuple[Q, ...], ...]) -> Q:
    """Evaluate a permanent by subset dynamic programming."""

    states = {0: Q(1)}
    for column in columns:
        following: dict[int, Q] = {}
        for mask, value in states.items():
            for row, entry in enumerate(column):
                if mask & (1 << row):
                    continue
                next_mask = mask | (1 << row)
                following[next_mask] = following.get(next_mask, Q(0)) + value * entry
        states = following
    return states[(1 << len(columns)) - 1]


def rank(rows: list[list[Q]]) -> int:
    matrix = [row[:] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0]) if matrix else 0):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / pivot_value for entry in matrix[pivot_row]]
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
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def span_rank(columns: list[list[Q]], rows: tuple[int, ...] | None = None) -> int:
    selected = rows if rows is not None else tuple(range(81))
    return rank([[column[row] for column in columns] for row in selected])


def determinant(matrix: list[list[Q]]) -> Q:
    size = len(matrix)
    return sum(
        Q(permutation_sign(sigma))
        * product_entries(matrix[row][sigma[row]] for row in range(size))
        for sigma in permutations(range(size))
    )


def product_entries(entries) -> Q:
    answer = Q(1)
    for entry in entries:
        answer *= entry
    return answer


def permutation_sign(sigma: tuple[int, ...]) -> int:
    inversions = sum(
        sigma[left] > sigma[right]
        for left in range(len(sigma))
        for right in range(left + 1, len(sigma))
    )
    return -1 if inversions % 2 else 1


def build_layers() -> tuple[list[list[Q]], list[list[Q]], list[list[Q]]]:
    """Reconstruct the fixed-star columns in a reversed presentation order."""

    xi = vec(1, 1, 1, -1)
    eta = vec(1, 1, 1, 1)
    radical = (vec(1, -1, 0, 0), vec(1, 0, -1, 0))
    centre = radical + (vec(1, 0, 0, 1),)
    leaf = radical + (vec(1, 0, 0, -1),)
    ports = (centre, leaf, leaf, leaf)

    q = [
        [
            permanent_dp(tuple(ports[mode][word[mode]] for mode in MODES))
            for word in WORDS
        ]
    ]

    residual: list[list[Q]] = []
    for residual_vector in (eta, xi):
        for labelled_mode in reversed(MODES):
            others = tuple(mode for mode in MODES if mode != labelled_mode)
            for labelled_index in reversed(range(3)):
                column = []
                for word in WORDS:
                    if word[labelled_mode] != labelled_index:
                        column.append(Q(0))
                    else:
                        column.append(
                            permanent_dp(
                                (residual_vector,)
                                + tuple(ports[mode][word[mode]] for mode in others)
                            )
                        )
                residual.append(column)

    pair: list[list[Q]] = []
    for labelled_modes in reversed(tuple(combinations(MODES, 2))):
        others = tuple(mode for mode in MODES if mode not in labelled_modes)
        for labelled_indices in reversed(tuple(product(range(3), repeat=2))):
            column = []
            for word in WORDS:
                if any(
                    word[mode] != index
                    for mode, index in zip(
                        labelled_modes, labelled_indices, strict=True
                    )
                ):
                    column.append(Q(0))
                else:
                    column.append(
                        permanent_dp(
                            (
                                xi,
                                eta,
                                ports[others[0]][word[others[0]]],
                                ports[others[1]][word[others[1]]],
                            )
                        )
                    )
            pair.append(column)
    assert (len(q), len(residual), len(pair)) == (1, 24, 54)
    return q, residual, pair


def exact_dimension_audit(
    layers: tuple[list[list[Q]], list[list[Q]], list[list[Q]]],
) -> tuple[int, ...]:
    q, residual, pair = layers
    punctured_rows = tuple(WORD_OFFSET[word] for word in PUNCTURED)
    erased_rows = tuple(row for row in range(81) if row not in punctured_rows)
    assert (len(punctured_rows), len(erased_rows)) == (60, 21)
    assert all(column[row] == 0 for column in pair for row in punctured_rows)
    values = (
        span_rank(pair),
        span_rank(pair, erased_rows),
        span_rank(q + residual, punctured_rows),
        span_rank(q + residual + pair),
    )
    assert values == (21, 21, 23, 44)

    slice_codimensions = []
    for root in range(3):
        rows = tuple(WORD_OFFSET[word] for word in PUNCTURED if word[0] == root)
        slice_codimensions.append(len(rows) - span_rank(q + residual + pair, rows))
    assert slice_codimensions == [4, 4, 6]
    return values + tuple(slice_codimensions)


def rref_mod(rows: list[list[int]], prime: int) -> tuple[list[list[int]], list[int]]:
    matrix = [[entry % prime for entry in row] for row in rows]
    pivots: list[int] = []
    pivot_row = 0
    for column in range(len(matrix[0]) if matrix else 0):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [entry * inverse % prime for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                (entry - scale * pivot_entry) % prime
                for entry, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return matrix, pivots


def nullspace_mod(rows: list[list[int]], prime: int) -> list[list[int]]:
    reduced, pivots = rref_mod(rows, prime)
    free = [column for column in range(len(rows[0])) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [0] * len(rows[0])
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column] % prime
        basis.append(vector)
    return basis


def projective_points(prime: int) -> list[tuple[int, int, int]]:
    points = []
    for pivot in range(3):
        for tail in product(range(prime), repeat=2 - pivot):
            point = [0, 0, 0]
            point[pivot] = 1
            point[pivot + 1 :] = tail
            points.append(tuple(point))
    return points


def finite_one_word_audit(
    layers: tuple[list[list[Q]], list[list[Q]], list[list[Q]]],
) -> tuple[int, int, int, int]:
    """Independently exhaust all projective leaf triples over F_5."""

    prime = 5
    q, residual, _pair = layers
    punctured_rows = tuple(WORD_OFFSET[word] for word in PUNCTURED)
    code_transpose = [
        [int(column[row]) % prime for row in punctured_rows] for column in q + residual
    ]
    annihilator = nullspace_mod(code_transpose, prime)
    assert len(annihilator) == 37
    position = {word: offset for offset, word in enumerate(PUNCTURED)}
    points = projective_points(prime)
    e2 = (0, 0, 1)

    partial: dict[tuple[int, int], list[list[list[int]]]] = {}
    for b_index, b in enumerate(points):
        for c_index, c in enumerate(points):
            block = [[[0] * 3 for _root in range(3)] for _relation in annihilator]
            for relation_index, relation in enumerate(annihilator):
                for root in range(3):
                    for k in range(3):
                        total = 0
                        for i, j in product(range(3), repeat=2):
                            word = (root, i, j, k)
                            if word not in position:
                                continue
                            total += relation[position[word]] * b[i] * c[j]
                        block[relation_index][root][k] = total % prime
            partial[(b_index, c_index)] = block

    histogram: dict[tuple[bool, int], int] = {}
    for b_index, b in enumerate(points):
        for c_index, c in enumerate(points):
            block = partial[(b_index, c_index)]
            for d in points:
                syndrome = [
                    [
                        sum(block[relation][root][k] * d[k] for k in range(3)) % prime
                        for root in range(3)
                    ]
                    for relation in range(len(annihilator))
                ]
                syndrome_rank = len(rref_mod(syndrome, prime)[1])
                hidden = sum(factor == e2 for factor in (b, c, d)) >= 2
                key = (hidden, syndrome_rank)
                histogram[key] = histogram.get(key, 0) + 1

    assert histogram == {(True, 0): 91, (False, 3): 29_700}
    return len(points), histogram[(True, 0)], histogram[(False, 3)], len(annihilator)


def binary_tensor(
    gamma: Q,
    x: tuple[Q, ...],
    y: tuple[Q, ...],
) -> dict[tuple[int, int, int, int], Q]:
    xi = vec(1, 1, 1, -1)
    eta = vec(1, 1, 1, 1)
    radical = (vec(1, -1, 0, 0), vec(1, 0, -1, 0))
    ports = (radical + (vec(1, 0, 0, 1),),) + 3 * (radical + (vec(1, 0, 0, -1),),)
    answer = {}
    for word in product(range(2), repeat=4):
        value = gamma * permanent_dp(tuple(ports[mode][word[mode]] for mode in MODES))
        for residual_vector, parameters in ((xi, x), (eta, y)):
            for labelled_mode in MODES:
                companions = tuple(mode for mode in MODES if mode != labelled_mode)
                value += parameters[2 * labelled_mode + word[labelled_mode]] * (
                    permanent_dp(
                        (residual_vector,)
                        + tuple(ports[mode][word[mode]] for mode in companions)
                    )
                )
        answer[word] = value
    return answer


def balanced_binary_determinant(
    tensor: dict[tuple[int, int, int, int], Q], left_modes: tuple[int, int]
) -> Q:
    right_modes = tuple(mode for mode in MODES if mode not in left_modes)
    matrix = []
    for left_indices in product(range(2), repeat=2):
        row = []
        for right_indices in product(range(2), repeat=2):
            word = [0] * 4
            for mode, index in zip(left_modes, left_indices, strict=True):
                word[mode] = index
            for mode, index in zip(right_modes, right_indices, strict=True):
                word[mode] = index
            row.append(tensor[tuple(word)])
        matrix.append(row)
    return determinant(matrix)


def eisenstein_gate_audit() -> tuple[tuple[Q, Q, Q], ...]:
    assignments = (
        (
            Q(7),
            tuple(Q(value) for value in (0, 1, 2, 3, 4, 5, 6, 7)),
            tuple(Q(value) for value in (8, -2, 1, -4, 3, 9, -5, 2)),
        ),
        (
            Q(-3, 2),
            tuple(Q(value) for value in (1, 0, -1, 2, 3, -2, 4, 1)),
            tuple(Q(value) for value in (-2, 3, 5, 0, -1, 6, 2, -4)),
        ),
        (
            Q(0),
            tuple(Q(value) for value in (2, 5, 1, -3, 0, 4, -2, 7)),
            tuple(Q(value) for value in (1, -1, 6, 2, 3, 0, 5, -4)),
        ),
    )
    outputs = []
    for gamma, x, y in assignments:
        tensor = binary_tensor(gamma, x, y)
        alpha = [x[2 * mode] - y[2 * mode] for mode in MODES]
        beta = [x[2 * mode + 1] - y[2 * mode + 1] for mode in MODES]
        norm = [
            alpha[mode] ** 2 - alpha[mode] * beta[mode] + beta[mode] ** 2
            for mode in MODES
        ]
        expected = (
            16 * (norm[0] - norm[1]) * (norm[2] - norm[3]),
            16 * (norm[0] - norm[2]) * (norm[1] - norm[3]),
            16 * (norm[0] - norm[3]) * (norm[1] - norm[2]),
        )
        actual = tuple(
            balanced_binary_determinant(tensor, modes)
            for modes in ((0, 1), (0, 2), (0, 3))
        )
        assert actual == expected
        outputs.append(actual)
    return tuple(outputs)


def tensor_from_frames(centre: list[list[Q]], leaf: list[list[Q]]) -> list[Q]:
    return [
        sum(
            centre[word[0]][component]
            * leaf[word[1]][component]
            * leaf[word[2]][component]
            * leaf[word[3]][component]
            for component in range(3)
        )
        for word in WORDS
    ]


def flattening_rank(tensor: list[Q], left_modes: tuple[int, int]) -> int:
    right_modes = tuple(mode for mode in MODES if mode not in left_modes)
    rows = []
    for left_indices in product(range(3), repeat=2):
        row = []
        for right_indices in product(range(3), repeat=2):
            word = [0] * 4
            for mode, index in zip(left_modes, left_indices, strict=True):
                word[mode] = index
            for mode, index in zip(right_modes, right_indices, strict=True):
                word[mode] = index
            row.append(tensor[WORD_OFFSET[tuple(word)]])
        rows.append(row)
    return rank(rows)


def epsilon_full(tensor: list[Q]) -> Q:
    total = Q(0)
    permutations_3 = tuple(permutations(range(3)))
    for sigmas in product(permutations_3, repeat=4):
        term = Q(product_entries(permutation_sign(sigma) for sigma in sigmas))
        for colour in range(3):
            word = tuple(sigmas[mode][colour] for mode in MODES)
            term *= tensor[WORD_OFFSET[word]]
        total += term
    return total


def secant_two_control_audit(
    layers: tuple[list[list[Q]], list[list[Q]], list[list[Q]]],
) -> tuple[int, int, tuple[int, int, int], Q]:
    q, residual, pair = layers
    nuisance = q + residual + pair
    leaf = [
        [Q(1), Q(1), Q(1)],
        [Q(-1), Q(0), Q(0)],
        [Q(0), Q(-1), Q(0)],
    ]
    centre = [
        [Q(0), Q(1), Q(-1)],
        [Q(0), Q(0), Q(0)],
        [Q(0), Q(0), Q(1)],
    ]
    tensor = tensor_from_frames(centre, leaf)
    nuisance_rank = span_rank(nuisance)
    augmented_rank = span_rank(nuisance + [tensor])
    leaf_det = determinant(leaf)
    centre_rank = rank(centre)
    balanced = tuple(
        flattening_rank(tensor, modes) for modes in ((0, 1), (0, 2), (0, 3))
    )
    epsilon = epsilon_full(tensor)
    assert nuisance_rank == augmented_rank == 44
    assert leaf_det == 1 and centre_rank == 2
    assert balanced == (2, 2, 2) and epsilon == 0
    return leaf_det, centre_rank, balanced, epsilon


def main() -> None:
    layers = build_layers()
    dimensions = exact_dimension_audit(layers)
    finite = finite_one_word_audit(layers)
    norm_values = eisenstein_gate_audit()
    boundary = secant_two_control_audit(layers)
    print("independent GLD71 punctured-syndrome audit: PASS")
    print("  exact dimensions pair/punctured/full/root slices:", dimensions)
    print("  F5 points/hidden/nonhidden/annihilator:", finite)
    print("  direct binary determinant samples:", norm_values)
    print("  exact secant-two control:", boundary)
    print("  determinant-safe three-word statement proved: False")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
