"""Independent audit of the simultaneous-low sensor-rank-three fixture."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product

Vector = tuple[int, ...]

PLANES: tuple[tuple[Vector, ...], ...] = (
    ((1, 0, 0, 1, 0, 0), (0, 1, 0, -1, 0, 0), (0, 0, 1, 1, 0, 0)),
    ((1, 0, 0, 0, 0, 0), (0, 1, 0, 1, 0, 0), (0, 0, 1, -1, -1, 1)),
    ((1, 0, 0, 1, 0, 0), (0, 1, 1, 0, 0, 0), (0, 0, 0, 0, 1, -1)),
    ((0, -1, 1, 0, 0, 0), (0, 1, 0, 1, 0, 0), (0, 0, 0, 0, 1, 1)),
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
    """Evaluate an integer covector."""
    return sum(x * y for x, y in zip(left, right, strict=True))


def permanent_value(factors: tuple[Vector, ...], vectors: tuple[Vector, ...]) -> int:
    """Evaluate a polarized four-factor product by a direct permanent sum."""
    result = 0
    for order in permutations(range(4)):
        term = 1
        for row, column in enumerate(order):
            term *= dot(factors[row], vectors[column])
        result += term
    return result


def evaluate_all(
    planes: tuple[tuple[Vector, ...], ...] = PLANES,
) -> dict[tuple[int, ...], tuple[int, ...]]:
    """Evaluate the independently factorized five-output tensor."""
    ledger = {}
    for word in product(range(3), repeat=4):
        vectors = tuple(planes[mode][word[mode]] for mode in range(4))
        ledger[word] = tuple(
            scalar * permanent_value(factors, vectors)
            for scalar, factors in FACTORS
        )
    return ledger


def rational_rank(rows: list[list[int]] | tuple[Vector, ...]) -> int:
    """Exact row rank using only standard-library rational arithmetic."""
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


def modular_rank(rows: list[list[int]], prime: int) -> int:
    """Row rank over one prime field for an independent reduction check."""
    matrix = [[value % prime for value in row] for row in rows if any(
        value % prime for value in row
    )]
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
        inverse = pow(matrix[result][column], prime - 2, prime)
        matrix[result] = [(value * inverse) % prime for value in matrix[result]]
        for row in range(len(matrix)):
            if row == result or not matrix[row][column]:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                (value - multiplier * pivot_entry) % prime
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
    """Compute a projection rank using the independent rational reducer."""
    rows = [[dot(covector, vector) for covector in phi] for vector in plane]
    return rational_rank(rows)


def flattening_rows(
    ledger: dict[tuple[int, ...], tuple[int, ...]],
    mode: int,
    output: int | None = None,
) -> list[list[int]]:
    """Build one input flattening, either D^*-valued or for one D slice."""
    rows = []
    outputs = range(3) if output is None else (output,)
    for colour in range(3):
        row = []
        for current_output in outputs:
            for other in product(range(3), repeat=3):
                word = []
                other_index = 0
                for current_mode in range(4):
                    if current_mode == mode:
                        word.append(colour)
                    else:
                        word.append(other[other_index])
                        other_index += 1
                row.append(ledger[tuple(word)][current_output + 2])
        rows.append(row)
    return rows


def combine(coefficients: Vector, plane: tuple[Vector, ...]) -> Vector:
    """Convert local coordinates into an ambient vector."""
    return tuple(
        sum(coefficients[source] * plane[source][coordinate] for source in range(3))
        for coordinate in range(6)
    )


def alternative_bases() -> tuple[tuple[Vector, ...], ...]:
    """Construct the pure-nonzero bases independently from integer matrices."""
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
    """Hash the canonical lexicographic exact ledger."""
    payload = ";".join(
        ",".join(str(value) for value in ledger[word])
        for word in product(range(3), repeat=4)
    )
    return sha256(payload.encode("ascii")).hexdigest()


def main() -> None:
    assert all(rational_rank(list(plane)) == 3 for plane in PLANES)
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

    output_rows = [list(values[2:]) for values in ledger.values()]
    output_rank = rational_rank(output_rows)
    input_ranks = tuple(
        rational_rank(flattening_rows(ledger, mode)) for mode in range(4)
    )
    slice_ranks = tuple(
        tuple(
            rational_rank(flattening_rows(ledger, mode, output))
            for mode in range(4)
        )
        for output in range(3)
    )
    assert output_rank == 3
    assert input_ranks == (3, 1, 1, 2)
    assert slice_ranks == ((1, 1, 1, 1),) * 3
    assert modular_rank(output_rows, 3) == 3
    assert tuple(
        modular_rank(flattening_rows(ledger, mode), 3) for mode in range(4)
    ) == input_ranks

    changed = alternative_bases()
    assert all(rational_rank(list(plane)) == 3 for plane in changed)
    changed_ledger = evaluate_all(changed)
    pure_values = tuple(changed_ledger[(colour,) * 4][colour + 2] for colour in range(3))
    assert pure_values == (4, -4, 4)
    assert all(values[0] == values[1] == 0 for values in changed_ledger.values())

    digest = ledger_hash(ledger)
    print("fixed-pair simultaneous-low sensor-rank-three no-import audit: PASS")
    print(f"  projection profiles: Phi1={profile1}, Phi2={profile2}")
    print(f"  exact five-word support: {support}")
    print(f"  output rank over Q/F3: {output_rank}/3")
    print(f"  input ranks over Q and F3: {input_ranks}")
    print(f"  slice multilinear ranks: {slice_ranks}")
    print(f"  alternative-basis pure values: {pure_values}")
    print(f"  81-by-5 ledger SHA-256: {digest}")


if __name__ == "__main__":
    main()
