"""Primary exact checks for the concise simultaneous-low sharpness fixture."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product

import sympy as sp

Vector = tuple[int, ...]
Polynomial = dict[int, int]

EDGES = tuple(combinations(range(4), 2))
FULL_MASK = 63
OUTPUTS = (
    (0, 1, -1, 0, 0, -1),
    (0, 0, 0, 1, -1, -1),
    (1, 1, 0, 0, -1, -1),
    (1, 0, -1, 1, 0, -1),
    (0, 0, 0, 0, 0, -2),
)
PLANES: tuple[tuple[Vector, ...], ...] = (
    ((0, 1, 0, 0, -1, 0), (0, 0, 1, 0, -1, 0), (0, 0, 0, 1, 1, 0)),
    ((1, 0, 0, 0, 0, 1), (0, 1, 0, 0, 1, 0), (0, 0, 1, 0, 0, 1)),
    ((1, 0, 0, 0, 0, -1), (0, 0, 1, 0, 1, 0), (0, 0, 0, 1, -1, 0)),
    ((1, 1, 0, 0, 0, 0), (0, 0, 1, 1, 0, 0), (1, 0, -1, 0, -1, 1)),
)
PHI1 = (
    (0, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 0),
    (0, 0, 0, 0, 0, 1),
    (-1, 0, -1, 1, 0, 0),
)
PHI2 = (
    (1, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 0),
    (0, 0, 0, 0, 0, 1),
    (0, -1, -1, 1, 0, 0),
)


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply in the square-free algebra."""
    result: Polynomial = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = result.get(mask, 0) + left_value * right_value
    return {mask: value for mask, value in result.items() if value}


def coefficient(quadratic: Vector, vectors: tuple[Vector, ...]) -> int:
    """Extract the coefficient of x0...x5 from q times four forms."""
    polynomial = {
        (1 << first) | (1 << second): value
        for value, (first, second) in zip(quadratic, EDGES, strict=True)
        if value
    }
    for vector in vectors:
        polynomial = multiply(
            polynomial,
            {1 << index: value for index, value in enumerate(vector) if value},
        )
    return polynomial.get(FULL_MASK, 0)


def ledger(
    planes: tuple[tuple[Vector, ...], ...] = PLANES,
) -> dict[tuple[int, ...], tuple[int, ...]]:
    """Evaluate the complete exact 81-by-5 sensor ledger."""
    return {
        word: tuple(
            coefficient(
                quadratic,
                tuple(planes[mode][word[mode]] for mode in range(4)),
            )
            for quadratic in OUTPUTS
        )
        for word in product(range(3), repeat=4)
    }


def projection_rank(phi: tuple[Vector, ...], plane: tuple[Vector, ...]) -> int:
    """Return the exact factor-projection rank."""
    return sp.Matrix([
        [sum(covector[i] * vector[i] for i in range(6)) for covector in phi]
        for vector in plane
    ]).rank()


def tensor_entry(
    data: dict[tuple[int, ...], tuple[int, ...]],
    index: tuple[int, ...],
) -> int:
    """Read a five-way D^*-valued tensor entry."""
    return data[index[:4]][index[4] + 2]


def flattening_rank(
    data: dict[tuple[int, ...], tuple[int, ...]],
    left_axes: tuple[int, ...],
) -> int:
    """Rank a selected-factor versus complementary-factor flattening."""
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
    return sp.Matrix(rows).rank()


def slice_mode_rank(
    data: dict[tuple[int, ...], tuple[int, ...]],
    output: int,
    mode: int,
) -> int:
    """Rank one mode flattening of a fixed output slice."""
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
    return sp.Matrix(rows).rank()


def combine(coefficients: Vector, plane: tuple[Vector, ...]) -> Vector:
    """Convert local coordinates to an ambient vector."""
    return tuple(
        sum(coefficients[source] * plane[source][coordinate] for source in range(3))
        for coordinate in range(6)
    )


def pure_bases() -> tuple[tuple[Vector, ...], ...]:
    """Construct the alternative bases with nonzero pure values."""
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
    """Hash the canonical lexicographic ledger."""
    payload = ";".join(
        ",".join(str(value) for value in data[word])
        for word in product(range(3), repeat=4)
    )
    return sha256(payload.encode("ascii")).hexdigest()


def main() -> None:
    assert [sp.Matrix(plane).rank() for plane in PLANES] == [3, 3, 3, 3]
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
        tuple(slice_mode_rank(data, output, mode) for mode in range(4))
        for output in range(3)
    )
    assert slice_ranks == ((2, 3, 3, 2), (2, 2, 3, 2), (2, 3, 2, 2))

    changed = pure_bases()
    assert [sp.Matrix(plane).rank() for plane in changed] == [3, 3, 3, 3]
    changed_data = ledger(changed)
    pure_values = tuple(changed_data[(colour,) * 4][colour + 2] for colour in range(3))
    assert pure_values == (2, 2, -2)
    assert all(values[0] == values[1] == 0 for values in changed_data.values())

    digest = ledger_hash(data)
    print("fixed-pair concise simultaneous-low sharpness primary checks: PASS")
    print(f"  projection profiles: Phi1={profile1}, Phi2={profile2}")
    print(f"  five single-factor ranks: {single_ranks}")
    print(f"  ten two-factor ranks: {pair_ranks}")
    print(f"  fixed-slice multilinear ranks: {slice_ranks}")
    print("  five-way tensor-rank lower bound: 9")
    print(f"  alternative-basis pure values: {pure_values}")
    print(f"  81-by-5 ledger SHA-256: {digest}")


if __name__ == "__main__":
    main()
