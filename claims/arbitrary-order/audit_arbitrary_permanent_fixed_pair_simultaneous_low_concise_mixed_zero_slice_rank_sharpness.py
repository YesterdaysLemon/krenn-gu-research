"""Independent no-import audit of the concise simultaneous-low fixture."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product

Vector = tuple[int, ...]

PLANES: tuple[tuple[Vector, ...], ...] = (
    ((0, 1, 0, 0, -1, 0), (0, 0, 1, 0, -1, 0), (0, 0, 0, 1, 1, 0)),
    ((1, 0, 0, 0, 0, 1), (0, 1, 0, 0, 1, 0), (0, 0, 1, 0, 0, 1)),
    ((1, 0, 0, 0, 0, -1), (0, 0, 1, 0, 1, 0), (0, 0, 0, 1, -1, 0)),
    ((1, 1, 0, 0, 0, 0), (0, 0, 1, 1, 0, 0), (1, 0, -1, 0, -1, 1)),
)

COORDINATES = tuple(tuple(int(i == j) for i in range(6)) for j in range(6))
X0, X1, X2, X3, X4, X5 = COORDINATES


def add(*vectors: Vector) -> Vector:
    """Add integer covectors."""
    return tuple(sum(vector[index] for vector in vectors) for index in range(6))


def scale(value: int, vector: Vector) -> Vector:
    """Scale an integer covector."""
    return tuple(value * entry for entry in vector)


ELL1 = add(X3, scale(-1, X2), scale(-1, X0))
ELL2 = add(X3, scale(-1, X2), scale(-1, X1))
FACTORS: tuple[tuple[int, tuple[Vector, ...]], ...] = (
    (1, (X4, X5, X1, ELL1)),
    (1, (X4, X5, X0, ELL2)),
    (1, (X4, X5, add(X1, X2), add(X3, scale(-1, X0)))),
    (1, (X4, X5, add(X0, X2), add(X3, scale(-1, X1)))),
    (-2, (X4, X5, X0, X1)),
)
PHI1 = (X1, X4, X5, ELL1)
PHI2 = (X0, X4, X5, ELL2)


def dot(left: Vector, right: Vector) -> int:
    """Evaluate one covector."""
    return sum(x * y for x, y in zip(left, right, strict=True))


def permanent_value(factors: tuple[Vector, ...], vectors: tuple[Vector, ...]) -> int:
    """Evaluate one factorized quartic by a direct permanent sum."""
    result = 0
    for order in permutations(range(4)):
        term = 1
        for row, column in enumerate(order):
            term *= dot(factors[row], vectors[column])
        result += term
    return result


def ledger(
    planes: tuple[tuple[Vector, ...], ...] = PLANES,
) -> dict[tuple[int, ...], tuple[int, ...]]:
    """Evaluate all five factorized tensors on all local words."""
    result = {}
    for word in product(range(3), repeat=4):
        vectors = tuple(planes[mode][word[mode]] for mode in range(4))
        result[word] = tuple(
            scalar * permanent_value(factors, vectors)
            for scalar, factors in FACTORS
        )
    return result


def rational_rank(rows: list[list[int]] | tuple[Vector, ...]) -> int:
    """Exact rank by custom rational Gaussian elimination."""
    matrix = [list(map(Fraction, row)) for row in rows if any(row)]
    if not matrix:
        return 0
    result = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(result, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[result], matrix[pivot] = matrix[pivot], matrix[result]
        pivot_value = matrix[result][column]
        matrix[result] = [value / pivot_value for value in matrix[result]]
        for row in range(len(matrix)):
            if row == result or not matrix[row][column]:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(
                    matrix[row],
                    matrix[result],
                    strict=True,
                )
            ]
        result += 1
        if result == len(matrix):
            break
    return result


def projection_rank(phi: tuple[Vector, ...], plane: tuple[Vector, ...]) -> int:
    """Compute one projection rank independently."""
    return rational_rank([
        [dot(covector, vector) for covector in phi]
        for vector in plane
    ])


def tensor_entry(
    data: dict[tuple[int, ...], tuple[int, ...]],
    index: tuple[int, ...],
) -> int:
    """Read one D^*-valued five-way tensor entry."""
    return data[index[:4]][index[4] + 2]


def flattening_rank(
    data: dict[tuple[int, ...], tuple[int, ...]],
    left_axes: tuple[int, ...],
) -> int:
    """Compute a five-way matrix flattening rank."""
    right_axes = tuple(axis for axis in range(5) if axis not in left_axes)
    rows = []
    for left_index in product(range(3), repeat=len(left_axes)):
        row = []
        for right_index in product(range(3), repeat=len(right_axes)):
            index = [0] * 5
            for axis, value in zip(left_axes, left_index, strict=True):
                index[axis] = value
            for axis, value in zip(right_axes, right_index, strict=True):
                index[axis] = value
            row.append(tensor_entry(data, tuple(index)))
        rows.append(row)
    return rational_rank(rows)


def slice_rank(
    data: dict[tuple[int, ...], tuple[int, ...]],
    output: int,
    mode: int,
) -> int:
    """Compute one fixed-slice mode-flattening rank."""
    rows = []
    for colour in range(3):
        row = []
        for other in product(range(3), repeat=3):
            word = []
            other_index = 0
            for current_mode in range(4):
                if current_mode == mode:
                    word.append(colour)
                else:
                    word.append(other[other_index])
                    other_index += 1
            row.append(data[tuple(word)][output + 2])
        rows.append(row)
    return rational_rank(rows)


def combine(coefficients: Vector, plane: tuple[Vector, ...]) -> Vector:
    """Convert coordinates in a plane basis to an ambient vector."""
    return tuple(
        sum(coefficients[source] * plane[source][coordinate] for source in range(3))
        for coordinate in range(6)
    )


def pure_bases() -> tuple[tuple[Vector, ...], ...]:
    """Reconstruct the four alternative colour bases."""
    coordinates = (
        ((-1, 1, 1), (0, -1, 0), (0, 0, 1)),
        ((0, 1, 0), (1, -1, -1), (0, 0, 1)),
        ((-1, 1, 0), (1, 1, -1), (1, 0, 1)),
        ((0, 1, 1), (-1, -1, 0), (1, 1, -1)),
    )
    return tuple(
        tuple(combine(coordinates[mode][colour], PLANES[mode]) for colour in range(3))
        for mode in range(4)
    )


def ledger_hash(data: dict[tuple[int, ...], tuple[int, ...]]) -> str:
    """Hash the canonical exact ledger."""
    payload = ";".join(
        ",".join(str(value) for value in data[word])
        for word in product(range(3), repeat=4)
    )
    return sha256(payload.encode("ascii")).hexdigest()


def main() -> None:
    assert all(rational_rank(list(plane)) == 3 for plane in PLANES)
    profile1 = tuple(projection_rank(PHI1, plane) for plane in PLANES)
    profile2 = tuple(projection_rank(PHI2, plane) for plane in PLANES)
    assert profile1 == (2, 2, 2, 2)
    assert profile2 == (1, 3, 2, 2)

    data = ledger()
    assert all(values[0] == values[1] == 0 for values in data.values())
    assert data[(0, 0, 2, 1)][2:] == (-2, 0, 0)
    assert data[(0, 0, 1, 1)][2:] == (0, -2, 0)
    assert data[(0, 0, 1, 0)][2:] == (0, 0, -2)

    single_ranks = tuple(flattening_rank(data, (axis,)) for axis in range(5))
    pair_ranks = {
        axes: flattening_rank(data, axes)
        for axes in combinations(range(5), 2)
    }
    assert single_ranks == (3, 3, 3, 3, 3)
    assert pair_ranks == {
        (0, 1): 8,
        (0, 2): 7,
        (0, 3): 8,
        (0, 4): 6,
        (1, 2): 8,
        (1, 3): 9,
        (1, 4): 8,
        (2, 3): 8,
        (2, 4): 8,
        (3, 4): 6,
    }
    slice_ranks = tuple(
        tuple(slice_rank(data, output, mode) for mode in range(4))
        for output in range(3)
    )
    assert slice_ranks == ((2, 3, 3, 2), (2, 2, 3, 2), (2, 3, 2, 2))

    changed = pure_bases()
    assert all(rational_rank(list(plane)) == 3 for plane in changed)
    changed_data = ledger(changed)
    pure_values = tuple(changed_data[(colour,) * 4][colour + 2] for colour in range(3))
    assert pure_values == (2, 2, -2)
    assert all(values[0] == values[1] == 0 for values in changed_data.values())

    digest = ledger_hash(data)
    print("fixed-pair concise simultaneous-low no-import audit: PASS")
    print(f"  projection profiles: Phi1={profile1}, Phi2={profile2}")
    print(f"  five single-factor ranks: {single_ranks}")
    print(f"  ten two-factor ranks: {pair_ranks}")
    print(f"  fixed-slice multilinear ranks: {slice_ranks}")
    print("  five-way tensor-rank lower bound: 9")
    print(f"  alternative-basis pure values: {pure_values}")
    print(f"  81-by-5 ledger SHA-256: {digest}")


if __name__ == "__main__":
    main()
