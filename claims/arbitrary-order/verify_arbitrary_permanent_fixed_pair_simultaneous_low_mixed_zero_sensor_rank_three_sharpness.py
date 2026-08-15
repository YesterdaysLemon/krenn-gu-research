"""Exact primary checks for the simultaneous-low sensor-rank-three fixture."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product

import sympy as sp

Vector = tuple[int, ...]
Polynomial = dict[int, int]

EDGES = tuple(combinations(range(4), 2))
FULL_MASK = (1 << 6) - 1

M1 = (0, 1, -1, 0, 0, -1)
M2 = (0, 0, 0, 1, -1, -1)
D0 = (1, 1, 0, 0, -1, -1)
D1 = (1, 0, -1, 1, 0, -1)
D2 = (0, 0, 0, 0, 0, -2)
OUTPUTS = (M1, M2, D0, D1, D2)

PLANES: tuple[tuple[Vector, ...], ...] = (
    ((1, 0, 0, 1, 0, 0), (0, 1, 0, -1, 0, 0), (0, 0, 1, 1, 0, 0)),
    ((1, 0, 0, 0, 0, 0), (0, 1, 0, 1, 0, 0), (0, 0, 1, -1, -1, 1)),
    ((1, 0, 0, 1, 0, 0), (0, 1, 1, 0, 0, 0), (0, 0, 0, 0, 1, -1)),
    ((0, -1, 1, 0, 0, 0), (0, 1, 0, 1, 0, 0), (0, 0, 0, 0, 1, 1)),
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
    """Multiply sparse polynomials in the six-variable square-free algebra."""
    result: Polynomial = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = result.get(mask, 0) + left_value * right_value
    return {mask: value for mask, value in result.items() if value}


def coefficient(quadratic: Vector, vectors: tuple[Vector, ...]) -> int:
    """Extract the full square-free coefficient of q times four forms."""
    polynomial = {
        (1 << first) | (1 << second): value
        for value, (first, second) in zip(quadratic, EDGES, strict=True)
        if value
    }
    for vector in vectors:
        linear = {1 << index: value for index, value in enumerate(vector) if value}
        polynomial = multiply(polynomial, linear)
    return polynomial.get(FULL_MASK, 0)


def evaluate_all(
    planes: tuple[tuple[Vector, ...], ...] = PLANES,
) -> dict[tuple[int, ...], tuple[int, ...]]:
    """Evaluate all 81 words against the five fixed pair outputs."""
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
    """Return the exact rank of a factor projection on a plane."""
    matrix = sp.Matrix([
        [sum(covector[i] * vector[i] for i in range(6)) for covector in phi]
        for vector in plane
    ])
    return matrix.rank()


def input_flattening_rank(
    ledger: dict[tuple[int, ...], tuple[int, ...]],
    mode: int,
) -> int:
    """Rank one input mode against the other inputs and D output."""
    rows = []
    for colour in range(3):
        row = []
        for output in range(3):
            for other in product(range(3), repeat=3):
                word = []
                other_index = 0
                for current_mode in range(4):
                    if current_mode == mode:
                        word.append(colour)
                    else:
                        word.append(other[other_index])
                        other_index += 1
                row.append(ledger[tuple(word)][output + 2])
        rows.append(row)
    return sp.Matrix(rows).rank()


def slice_mode_ranks(
    ledger: dict[tuple[int, ...], tuple[int, ...]],
    output: int,
) -> tuple[int, ...]:
    """Return the four multilinear ranks of one fixed D-output slice."""
    ranks = []
    for mode in range(4):
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
                row.append(ledger[tuple(word)][output + 2])
            rows.append(row)
        ranks.append(sp.Matrix(rows).rank())
    return tuple(ranks)


def combine(coefficients: Vector, plane: tuple[Vector, ...]) -> Vector:
    """Form an ambient vector from coordinates in one displayed plane basis."""
    return tuple(
        sum(coefficients[source] * plane[source][coordinate] for source in range(3))
        for coordinate in range(6)
    )


def transformed_planes() -> tuple[tuple[Vector, ...], ...]:
    """Return the alternative bases with all three pure values nonzero."""
    coordinates = (
        ((0, 0, 1), (0, 1, 0), (1, 0, 0)),
        ((0, 0, 1), (1, 0, 1), (0, 1, 1)),
        ((0, 0, 1), (1, 0, 1), (0, 1, 1)),
        ((0, 1, 0), (1, 0, 0), (1, 0, 1)),
    )
    return tuple(
        tuple(combine(coordinates[mode][colour], PLANES[mode]) for colour in range(3))
        for mode in range(4)
    )


def ledger_hash(ledger: dict[tuple[int, ...], tuple[int, ...]]) -> str:
    """Hash the canonical lexicographic 81-by-5 integer ledger."""
    payload = ";".join(
        ",".join(str(value) for value in ledger[word])
        for word in product(range(3), repeat=4)
    )
    return sha256(payload.encode("ascii")).hexdigest()


def main() -> None:
    assert [sp.Matrix(plane).rank() for plane in PLANES] == [3, 3, 3, 3]

    profile1 = tuple(projection_rank(PHI1, plane) for plane in PLANES)
    profile2 = tuple(projection_rank(PHI2, plane) for plane in PLANES)
    assert profile1 == (1, 3, 2, 2)
    assert profile2 == (2, 2, 3, 1)

    ledger = evaluate_all()
    assert all(values[0] == values[1] == 0 for values in ledger.values())
    support = {word: values[2:] for word, values in ledger.items() if any(values[2:])}
    assert support == {
        (0, 2, 2, 0): (0, 4, 4),
        (0, 2, 2, 1): (0, 0, -4),
        (1, 2, 2, 0): (0, -4, 0),
        (2, 2, 2, 0): (0, 4, 0),
        (2, 2, 2, 1): (4, 0, 0),
    }

    output_rank = sp.Matrix([values[2:] for values in ledger.values()]).rank()
    input_ranks = tuple(input_flattening_rank(ledger, mode) for mode in range(4))
    slice_ranks = tuple(slice_mode_ranks(ledger, output) for output in range(3))
    assert output_rank == 3
    assert input_ranks == (3, 1, 1, 2)
    assert slice_ranks == ((1, 1, 1, 1),) * 3

    changed = transformed_planes()
    assert [sp.Matrix(plane).rank() for plane in changed] == [3, 3, 3, 3]
    changed_ledger = evaluate_all(changed)
    pure_values = tuple(changed_ledger[(colour,) * 4][colour + 2] for colour in range(3))
    assert pure_values == (4, -4, 4)
    assert all(values[0] == values[1] == 0 for values in changed_ledger.values())

    digest = ledger_hash(ledger)
    print("fixed-pair simultaneous-low sensor-rank-three primary checks: PASS")
    print(f"  projection profiles: Phi1={profile1}, Phi2={profile2}")
    print(f"  nonzero D^*-valued words: {support}")
    print(f"  output rank: {output_rank}")
    print(f"  input flattening ranks: {input_ranks}")
    print(f"  slice multilinear ranks: {slice_ranks}")
    print("  tensor rank: 3 (three displayed rank-one slices and output-rank lower bound)")
    print(f"  alternative-basis pure values: {pure_values}")
    print(f"  81-by-5 ledger SHA-256: {digest}")


if __name__ == "__main__":
    main()
