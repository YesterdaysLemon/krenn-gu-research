"""Standalone exact audit of the GLD72 fixed-star GHZ survivor.

This file intentionally imports no repository module.  It reconstructs the
complete 79-column permanent map, derives its left annihilator, and checks the
displayed Gaussian-rational survivor using only standard-library arithmetic.

The result is deliberately scoped: it refutes the fixed-star determinant-safe
route, not graph/source integrability and not the global Krenn--Gu conjecture.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations, product


@dataclass(frozen=True, slots=True)
class Gaussian:
    """An exact element of Q(i), represented as re + im*i."""

    re: Fraction
    im: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        object.__setattr__(self, "re", Fraction(self.re))
        object.__setattr__(self, "im", Fraction(self.im))

    @staticmethod
    def coerce(value: int | Fraction | Gaussian) -> Gaussian:
        if isinstance(value, Gaussian):
            return value
        return Gaussian(Fraction(value))

    @property
    def is_zero(self) -> bool:
        return self.re == 0 and self.im == 0

    def __add__(self, other: int | Fraction | Gaussian) -> Gaussian:
        value = Gaussian.coerce(other)
        return Gaussian(self.re + value.re, self.im + value.im)

    def __radd__(self, other: int | Fraction | Gaussian) -> Gaussian:
        return self + other

    def __sub__(self, other: int | Fraction | Gaussian) -> Gaussian:
        value = Gaussian.coerce(other)
        return Gaussian(self.re - value.re, self.im - value.im)

    def __rsub__(self, other: int | Fraction | Gaussian) -> Gaussian:
        return Gaussian.coerce(other) - self

    def __neg__(self) -> Gaussian:
        return Gaussian(-self.re, -self.im)

    def __mul__(self, other: int | Fraction | Gaussian) -> Gaussian:
        value = Gaussian.coerce(other)
        return Gaussian(
            self.re * value.re - self.im * value.im,
            self.re * value.im + self.im * value.re,
        )

    def __rmul__(self, other: int | Fraction | Gaussian) -> Gaussian:
        return self * other

    def reciprocal(self) -> Gaussian:
        norm = self.re * self.re + self.im * self.im
        if norm == 0:
            raise ZeroDivisionError("zero has no Gaussian reciprocal")
        return Gaussian(self.re / norm, -self.im / norm)

    def __truediv__(self, other: int | Fraction | Gaussian) -> Gaussian:
        return self * Gaussian.coerce(other).reciprocal()

    def __rtruediv__(self, other: int | Fraction | Gaussian) -> Gaussian:
        return Gaussian.coerce(other) / self

    def __pow__(self, exponent: int) -> Gaussian:
        if exponent < 0:
            return (ONE / self) ** (-exponent)
        result = ONE
        factor = self
        remaining = exponent
        while remaining:
            if remaining & 1:
                result *= factor
            factor *= factor
            remaining >>= 1
        return result

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (Gaussian, int, Fraction)):
            return NotImplemented
        value = Gaussian.coerce(other)
        return self.re == value.re and self.im == value.im


ZERO = Gaussian(Fraction(0))
ONE = Gaussian(Fraction(1))

Vector = list[Gaussian]
Matrix = list[list[Gaussian]]

MODES = tuple(range(4))
ROOTS = tuple(range(3))
LOCAL_INDICES = tuple(product(range(3), repeat=4))
LOCAL_INDEX = {indices: offset for offset, indices in enumerate(LOCAL_INDICES)}
PAIRS = tuple(combinations(MODES, 2))
PERMUTATIONS_3 = tuple(permutations(range(3)))
PERMUTATIONS_4 = tuple(permutations(range(4)))


def rational_vector(*entries: int) -> Vector:
    return [Gaussian(Fraction(entry)) for entry in entries]


def gaussian(re: int, im: int = 0) -> Gaussian:
    return Gaussian(Fraction(re), Fraction(im))


def permutation_sign(sigma: Sequence[int]) -> int:
    inversions = sum(
        sigma[left] > sigma[right]
        for left in range(len(sigma))
        for right in range(left + 1, len(sigma))
    )
    return -1 if inversions % 2 else 1


def permanent(columns: Sequence[Vector]) -> Gaussian:
    """Evaluate the symmetric four-linear permanent in reversed order."""

    assert len(columns) == 4
    total = ZERO
    for sigma in reversed(PERMUTATIONS_4):
        term = ONE
        for mode in reversed(MODES):
            term *= columns[mode][sigma[mode]]
        total += term
    return total


def zero_vector(length: int) -> Vector:
    return [ZERO for _ in range(length)]


def matrix_from_columns(columns: Sequence[Vector]) -> Matrix:
    if not columns:
        return []
    return [[column[row] for column in columns] for row in range(len(columns[0]))]


def transpose(matrix: Matrix) -> Matrix:
    if not matrix:
        return []
    return [list(column) for column in zip(*matrix, strict=True)]


def rref(matrix: Matrix) -> tuple[Matrix, tuple[int, ...]]:
    work = [[entry for entry in row] for row in matrix]
    if not work:
        return work, ()
    row_count = len(work)
    column_count = len(work[0])
    pivots: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if not work[row][column].is_zero
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or work[row][column].is_zero:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return work, tuple(pivots)


def rank(matrix: Matrix) -> int:
    return len(rref(matrix)[1])


def nullspace(matrix: Matrix) -> list[Vector]:
    reduced, pivots = rref(matrix)
    if not reduced:
        return []
    column_count = len(reduced[0])
    pivot_set = set(pivots)
    free_columns = [column for column in range(column_count) if column not in pivot_set]
    basis: list[Vector] = []
    for free in free_columns:
        vector = [ZERO for _ in range(column_count)]
        vector[free] = ONE
        for pivot_row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -reduced[pivot_row][free]
        basis.append(vector)
    return basis


def matrix_vector(matrix: Matrix, vector: Vector) -> Vector:
    return [
        sum((entry * value for entry, value in zip(row, vector, strict=True)), ZERO)
        for row in matrix
    ]


def dot(left: Vector, right: Vector) -> Gaussian:
    return sum((a * b for a, b in zip(left, right, strict=True)), ZERO)


def determinant_3(matrix: Matrix) -> Gaussian:
    assert len(matrix) == 3 and all(len(row) == 3 for row in matrix)
    return sum(
        (
            Gaussian(permutation_sign(sigma))
            * matrix[0][sigma[0]]
            * matrix[1][sigma[1]]
            * matrix[2][sigma[2]]
            for sigma in PERMUTATIONS_3
        ),
        ZERO,
    )


def build_nuisance_columns() -> tuple[list[Vector], list[Vector], list[Vector]]:
    """Rebuild Q, residual-port, and pair columns with reversed traversal."""

    xi = rational_vector(1, 1, 1, -1)
    eta = rational_vector(1, 1, 1, 1)
    radical_0 = rational_vector(1, -1, 0, 0)
    radical_1 = rational_vector(1, 0, -1, 0)
    centre = rational_vector(1, 0, 0, 1)
    leaf = rational_vector(1, 0, 0, -1)
    ports = [
        [radical_0, radical_1, centre],
        [radical_0, radical_1, leaf],
        [radical_0, radical_1, leaf],
        [radical_0, radical_1, leaf],
    ]

    q_columns: list[Vector] = []
    q_column = zero_vector(len(LOCAL_INDICES))
    for indices in reversed(LOCAL_INDICES):
        q_column[LOCAL_INDEX[indices]] = permanent(
            [ports[mode][indices[mode]] for mode in reversed(MODES)]
        )
    q_columns.append(q_column)

    residual_columns: list[Vector] = []
    for residual in reversed((xi, eta)):
        for labelled_mode in reversed(MODES):
            companion_modes = tuple(
                mode for mode in reversed(MODES) if mode != labelled_mode
            )
            for labelled_index in reversed(range(3)):
                column = zero_vector(len(LOCAL_INDICES))
                for companion_indices in reversed(tuple(product(range(3), repeat=3))):
                    indices = [0] * 4
                    indices[labelled_mode] = labelled_index
                    for mode, index in zip(
                        companion_modes, companion_indices, strict=True
                    ):
                        indices[mode] = index
                    column[LOCAL_INDEX[tuple(indices)]] = permanent(
                        [
                            residual,
                            *[ports[mode][indices[mode]] for mode in companion_modes],
                        ]
                    )
                residual_columns.append(column)

    pair_columns: list[Vector] = []
    for labelled_modes in reversed(PAIRS):
        companion_modes = tuple(
            mode for mode in reversed(MODES) if mode not in labelled_modes
        )
        labelled_indices = tuple(product(range(3), repeat=2))
        for fixed_indices in reversed(labelled_indices):
            column = zero_vector(len(LOCAL_INDICES))
            for companion_indices in reversed(tuple(product(range(3), repeat=2))):
                indices = [0] * 4
                for mode, index in zip(labelled_modes, fixed_indices, strict=True):
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
    return q_columns, residual_columns, pair_columns


def candidate_tensor() -> tuple[Matrix, Matrix, Vector]:
    """Return the proposed leaf frame, centre frame, and 81-entry tensor."""

    leaf_frame = [
        [ONE, ONE, ONE],
        [ZERO, ZERO, gaussian(1, 1)],
        [ZERO, ONE, ONE],
    ]
    centre_frame = [
        [gaussian(-2, -2), gaussian(-1, 2), gaussian(3)],
        [ZERO, gaussian(-3, 3), ZERO],
        [ZERO, gaussian(-1, 2), ONE],
    ]
    tensor = zero_vector(len(LOCAL_INDICES))
    for indices in reversed(LOCAL_INDICES):
        root, first, second, third = indices
        tensor[LOCAL_INDEX[indices]] = sum(
            (
                centre_frame[root][colour]
                * leaf_frame[first][colour]
                * leaf_frame[second][colour]
                * leaf_frame[third][colour]
                for colour in ROOTS
            ),
            ZERO,
        )
    return leaf_frame, centre_frame, tensor


def syndrome_matrix(annihilator: Sequence[Vector], leaf_frame: Matrix) -> Matrix:
    rows: Matrix = []
    for relation in annihilator:
        row: list[Gaussian] = []
        for root in ROOTS:
            for colour in ROOTS:
                value = ZERO
                for first, second, third in product(range(3), repeat=3):
                    value += (
                        relation[LOCAL_INDEX[(root, first, second, third)]]
                        * leaf_frame[first][colour]
                        * leaf_frame[second][colour]
                        * leaf_frame[third][colour]
                    )
                row.append(value)
        rows.append(row)
    return rows


def balanced_flattening(tensor: Vector, left_modes: tuple[int, int]) -> Matrix:
    right_modes = tuple(mode for mode in MODES if mode not in left_modes)
    rows: Matrix = []
    for left_indices in product(range(3), repeat=2):
        row: list[Gaussian] = []
        for right_indices in product(range(3), repeat=2):
            indices = [0] * 4
            for mode, index in zip(left_modes, left_indices, strict=True):
                indices[mode] = index
            for mode, index in zip(right_modes, right_indices, strict=True):
                indices[mode] = index
            row.append(tensor[LOCAL_INDEX[tuple(indices)]])
        rows.append(row)
    return rows


def one_mode_flattening(tensor: Vector, mode: int) -> Matrix:
    other_modes = tuple(other for other in MODES if other != mode)
    rows: Matrix = []
    for local_index in range(3):
        row: list[Gaussian] = []
        for other_indices in product(range(3), repeat=3):
            indices = [0] * 4
            indices[mode] = local_index
            for other, index in zip(other_modes, other_indices, strict=True):
                indices[other] = index
            row.append(tensor[LOCAL_INDEX[tuple(indices)]])
        rows.append(row)
    return rows


def epsilon(tensor: Vector) -> Gaussian:
    total = ZERO
    for sigma_1, sigma_2, sigma_3 in product(PERMUTATIONS_3, repeat=3):
        term = Gaussian(
            Fraction(
                permutation_sign(sigma_1)
                * permutation_sign(sigma_2)
                * permutation_sign(sigma_3)
            )
        )
        for colour in ROOTS:
            term *= tensor[
                LOCAL_INDEX[(colour, sigma_1[colour], sigma_2[colour], sigma_3[colour])]
            ]
        total += term
    return 6 * total


def format_gaussian(value: Gaussian) -> str:
    if value.im == 0:
        return str(value.re)
    if value.re == 0:
        return f"{value.im}i"
    sign = "+" if value.im > 0 else "-"
    magnitude = abs(value.im)
    return f"{value.re}{sign}{magnitude}i"


def assert_zero_vector(values: Iterable[Gaussian]) -> None:
    assert all(value.is_zero for value in values)


def main() -> None:
    q_columns, residual_columns, pair_columns = build_nuisance_columns()
    assert (len(q_columns), len(residual_columns), len(pair_columns)) == (1, 24, 54)
    nuisance_columns = q_columns + residual_columns + pair_columns
    nuisance_matrix = matrix_from_columns(nuisance_columns)
    nuisance_rank = rank(nuisance_matrix)
    assert nuisance_rank == 44

    leaf_frame, centre_frame, tensor = candidate_tensor()
    augmented_rank = rank(
        [row + [tensor[row_index]] for row_index, row in enumerate(nuisance_matrix)]
    )
    assert augmented_rank == 44

    annihilator = nullspace(transpose(nuisance_matrix))
    assert len(annihilator) == 37
    assert all(
        dot(relation, column).is_zero
        for relation in annihilator
        for column in nuisance_columns
    )
    assert all(dot(relation, tensor).is_zero for relation in annihilator)

    syndrome = syndrome_matrix(annihilator, leaf_frame)
    syndrome_rank = rank(syndrome)
    assert syndrome_rank == 7
    centre_vector = [centre_frame[root][colour] for root in ROOTS for colour in ROOTS]
    assert_zero_vector(matrix_vector(syndrome, centre_vector))

    det_leaf = determinant_3(leaf_frame)
    det_centre = determinant_3(centre_frame)
    assert det_leaf == gaussian(-1, -1)
    assert det_centre == gaussian(12)

    local_ranks = tuple(rank(one_mode_flattening(tensor, mode)) for mode in MODES)
    balanced_ranks = tuple(
        rank(balanced_flattening(tensor, modes)) for modes in ((0, 1), (0, 2), (0, 3))
    )
    assert local_ranks == (3, 3, 3, 3)
    assert balanced_ranks == (3, 3, 3)

    direct_epsilon = epsilon(tensor)
    expected_epsilon = 6 * det_centre * (det_leaf**3)
    assert direct_epsilon == gaussian(144, -144)
    assert direct_epsilon == expected_epsilon

    support_size = sum(not value.is_zero for value in tensor)
    assert support_size == 61

    print("standalone GLD72 Gaussian GHZ survivor audit: PASS")
    print("  permanent columns / nuisance rank:", len(nuisance_columns), nuisance_rank)
    print("  augmented rank for concrete tensor:", augmented_rank)
    print("  annihilator dimension / syndrome rank:", len(annihilator), syndrome_rank)
    print("  det(G) / det(A):", format_gaussian(det_leaf), format_gaussian(det_centre))
    print("  four local ranks:", local_ranks)
    print("  three balanced ranks:", balanced_ranks)
    print("  direct epsilon:", format_gaussian(direct_epsilon))
    print("  tensor support size:", support_size)
    print("  scope: fixed-star determinant-safe route refuted")
    print("  scope: graph/source integrability not proved")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
