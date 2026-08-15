"""Independent no-import audit of the fixed pair-dimension-five boundary."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product

Vector = tuple[int, ...]
RationalVector = tuple[Fraction, ...]

EDGES = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
COMPLEMENT_INDEX = {
    edge: EDGES.index(tuple(sorted(set(range(4)) - set(edge))))
    for edge in EDGES
}
PERMUTATIONS_6 = list(permutations(range(6)))


def quadratic_product(left: Vector, right: Vector) -> Vector:
    """Multiply two first-four-variable forms in edge coordinates."""
    return tuple(
        left[first] * right[second] + left[second] * right[first]
        for first, second in EDGES
    )


def rational_rank(rows: list[list[int] | Vector]) -> int:
    """Compute exact row rank with a local Fraction implementation."""
    if not rows:
        return 0
    work = [[Fraction(value) for value in row] for row in rows]
    row_count = len(work)
    column_count = len(work[0])
    current = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(current, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[current], work[pivot] = work[pivot], work[current]
        pivot_value = work[current][column]
        work[current] = [value / pivot_value for value in work[current]]
        for row in range(row_count):
            if row == current or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * basis
                for value, basis in zip(work[row], work[current], strict=True)
            ]
        current += 1
        if current == row_count:
            break
    return current


def fixed_pair_audit() -> tuple[list[Vector], dict[str, object]]:
    """Reconstruct the fixed pair without importing the primary checker."""
    left = [
        (1, 0, 0, -1),
        (0, 1, 0, -1),
        (0, 0, 1, -1),
    ]
    right = [
        (0, 1, 1, 0),
        (1, 0, 1, 0),
        (0, 0, 1, -1),
    ]
    table = [[quadratic_product(u, v) for v in right] for u in left]
    d0 = (1, 1, 0, 0, -1, -1)
    d1 = (1, 0, -1, 1, 0, -1)
    d2 = (0, 0, 0, 0, 0, -2)
    m1 = (0, 1, -1, 0, 0, -1)
    m2 = (0, 0, 0, 1, -1, -1)
    assert table == [
        [d0, m1, m1],
        [m2, d1, m2],
        [m2, m1, d2],
    ]
    basis = [m1, m2, d0, d1, d2]
    assert rational_rank(basis) == 5
    relation = (0, 1, 1, 1, 1, 0)
    assert all(sum(a * b for a, b in zip(row, relation, strict=True)) == 0 for row in basis)
    return basis, {"product_table": table, "basis_rank": 5, "relation": relation}


def complement_quartic(quadratic: Vector) -> dict[int, int]:
    """Hodge-complement a quadratic using bit masks."""
    full_mask = (1 << 6) - 1
    result: dict[int, int] = {}
    for coefficient, (first, second) in zip(quadratic, EDGES, strict=True):
        if coefficient:
            mask = full_mask ^ ((1 << first) | (1 << second))
            result[mask] = coefficient
    return result


def multiply_linear_factors(factors: list[Vector]) -> dict[int, int]:
    """Multiply linear factors by a fresh sparse square-free routine."""
    state = {0: 1}
    for factor in factors:
        next_state: dict[int, int] = {}
        for mask, coefficient in state.items():
            for coordinate, value in enumerate(factor):
                bit = 1 << coordinate
                if not value or mask & bit:
                    continue
                next_mask = mask | bit
                next_state[next_mask] = next_state.get(next_mask, 0) + coefficient * value
        state = {mask: value for mask, value in next_state.items() if value}
    return state


def quartic_factor_audit(pair_basis: list[Vector]) -> dict[str, dict[int, int]]:
    """Independently check the two displayed factorized quartics."""
    x1 = (0, 1, 0, 0, 0, 0)
    x4 = (0, 0, 0, 0, 1, 0)
    x5 = (0, 0, 0, 0, 0, 1)
    ell1 = (-1, 0, -1, 1, 0, 0)
    x0 = (1, 0, 0, 0, 0, 0)
    ell2 = (0, -1, -1, 1, 0, 0)
    f1 = multiply_linear_factors([x1, x4, x5, ell1])
    f2 = multiply_linear_factors([x0, x4, x5, ell2])
    assert f1 == complement_quartic(pair_basis[0])
    assert f2 == complement_quartic(pair_basis[1])
    return {"F1": f1, "F2": f2}


def complement_pairing_row(residual: Vector, pair_basis: list[Vector]) -> list[int]:
    """Pair a stripped residual quadratic with the fixed pair basis."""
    return [
        sum(
            residual[index] * quadratic[COMPLEMENT_INDEX[edge]]
            for index, edge in enumerate(EDGES)
        )
        for quadratic in pair_basis
    ]


def missing_factor_table_audit(pair_basis: list[Vector]) -> dict[str, object]:
    """Rebuild all 16 ranks from the four explicit residual product spaces."""
    rows = ("x1", "x4", "x5", "ell1")
    columns = ("x0", "x4", "x5", "ell2")
    table = {row: {column: 0 for column in columns} for row in rows}

    residual_bases = {
        ("x1", "x0"): [(0, 0, 0, 0, 0, 1)],
        ("x1", "ell2"): [
            (0, 1, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 1),
        ],
        ("ell1", "x0"): [
            (0, 0, 0, 1, 1, 0),
            (0, 0, 0, 0, 0, 1),
        ],
        ("ell1", "ell2"): [
            (1, 0, 1, 0, 1, 0),
            (0, 1, 1, 1, 1, 1),
            (0, 0, 0, 0, 0, 1),
        ],
    }
    maps: dict[tuple[str, str], list[list[int]]] = {}
    for names, residual_basis in residual_bases.items():
        matrix = [
            complement_pairing_row(residual, pair_basis)
            for residual in residual_basis
        ]
        maps[names] = matrix
        table[names[0]][names[1]] = rational_rank(matrix)

    assert maps == {
        ("x1", "x0"): [[0, 0, 1, 1, 0]],
        ("x1", "ell2"): [[0, 0, -1, 1, 0], [0, 0, 1, 1, 0]],
        ("ell1", "x0"): [[0, 0, 1, -1, 0], [0, 0, 1, 1, 0]],
        ("ell1", "ell2"): [
            [0, 0, 0, 0, -2],
            [0, 0, 1, 1, 0],
            [0, 0, 1, 1, 0],
        ],
    }
    assert table == {
        "x1": {"x0": 1, "x4": 0, "x5": 0, "ell2": 2},
        "x4": {"x0": 0, "x4": 0, "x5": 0, "ell2": 0},
        "x5": {"x0": 0, "x4": 0, "x5": 0, "ell2": 0},
        "ell1": {"x0": 2, "x4": 0, "x5": 0, "ell2": 2},
    }
    return {"rank_table": table, "nonzero_maps": maps}


def modular_rank(rows: list[Vector], prime: int) -> int:
    """Compute row rank over one prime field without external algebra."""
    if not rows:
        return 0
    work = [[value % prime for value in row] for row in rows]
    row_count = len(work)
    column_count = len(work[0])
    current = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(current, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[current], work[pivot] = work[pivot], work[current]
        inverse = pow(work[current][column], -1, prime)
        work[current] = [(value * inverse) % prime for value in work[current]]
        for row in range(row_count):
            if row == current or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (value - factor * basis) % prime
                for value, basis in zip(work[row], work[current], strict=True)
            ]
        current += 1
        if current == row_count:
            break
    return current


def projective_covectors(prime: int) -> list[Vector]:
    """Enumerate all projective covectors of a four-space over F_p."""
    representatives: set[Vector] = set()
    for raw in product(range(prime), repeat=4):
        if not any(raw):
            continue
        pivot = next(value for value in raw if value)
        inverse = pow(pivot, -1, prime)
        representatives.add(tuple((value * inverse) % prime for value in raw))
    expected = (prime**4 - 1) // (prime - 1)
    assert len(representatives) == expected
    return sorted(representatives)


def hyperplane_basis(normal: Vector, prime: int) -> list[Vector]:
    """Construct a basis for one modular hyperplane."""
    pivot = next(index for index, value in enumerate(normal) if value)
    inverse = pow(normal[pivot], -1, prime)
    basis: list[Vector] = []
    for free in range(4):
        if free == pivot:
            continue
        vector = [0] * 4
        vector[free] = 1
        vector[pivot] = (-normal[free] * inverse) % prime
        assert sum(a * b for a, b in zip(normal, vector, strict=True)) % prime == 0
        basis.append(tuple(vector))
    assert modular_rank(basis, prime) == 3
    return basis


def hyperplane_product_audit() -> dict[str, object]:
    """Exhaust every projective hyperplane pair over F_5."""
    prime = 5
    normals = projective_covectors(prime)
    bases = {normal: hyperplane_basis(normal, prime) for normal in normals}
    histogram: Counter[int] = Counter()
    equality_pairs: list[tuple[Vector, Vector]] = []
    pair_count = 0
    for first_index, first in enumerate(normals):
        for second in normals[first_index:]:
            products = [
                tuple(value % prime for value in quadratic_product(left, right))
                for left in bases[first]
                for right in bases[second]
            ]
            dimension = modular_rank(products, prime)
            assert dimension >= 3
            histogram[dimension] += 1
            pair_count += 1
            if dimension == 3:
                equality_pairs.append((first, second))
                assert first == second
                assert sum(value != 0 for value in first) == 1

    coordinate_normals = {
        tuple(int(index == coordinate) for index in range(4))
        for coordinate in range(4)
    }
    assert {first for first, _ in equality_pairs} == coordinate_normals
    assert len(equality_pairs) == 4
    assert pair_count == len(normals) * (len(normals) + 1) // 2
    return {
        "field": prime,
        "projective_hyperplanes": len(normals),
        "unordered_pairs": pair_count,
        "dimension_histogram": dict(sorted(histogram.items())),
        "equality_pairs": equality_pairs,
    }


def sharpness_frames() -> list[list[Vector]]:
    """Define the six local colour frames independently."""
    return [
        [(1, 0, 0, -1, 0, 0), (0, 1, 0, -1, 0, 0), (0, 0, 1, -1, 0, 0)],
        [(0, 1, 1, 0, 0, 0), (1, 0, 1, 0, 0, 0), (0, 0, 1, -1, 0, 0)],
        [(0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 0, 1), (0, 1, -2, -1, 0, 0)],
        [(0, 0, 0, 0, 0, 1), (0, 1, -2, -1, 0, 0), (0, 0, 0, 0, 1, 0)],
        [(0, 1, -2, -1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 0, 1)],
        [(0, 2, 2, 0, 0, 0), (0, 2, 0, -2, 0, 0), (1, 1, 0, 0, 0, 0)],
    ]


def direct_permanent(rows: list[Vector]) -> int:
    """Compute a six-by-six permanent by all 720 assignments."""
    total = 0
    for assignment in PERMUTATIONS_6:
        term = 1
        for row, column in enumerate(assignment):
            term *= rows[row][column]
            if not term:
                break
        total += term
    return total


def factor_projection_matrix(frame: list[Vector], factors: list[Vector]) -> list[list[int]]:
    """Evaluate four covectors on three colour columns."""
    return [
        [sum(a * b for a, b in zip(factor, colour, strict=True)) for colour in frame]
        for factor in factors
    ]


def coefficient_audit() -> dict[str, object]:
    """Enumerate all words by direct permanents and recheck Hamming shells."""
    frames = sharpness_frames()
    assert [rational_rank([list(column) for column in zip(*frame, strict=True)]) for frame in frames] == [3] * 6

    factors_1 = [
        (0, 1, 0, 0, 0, 0),
        (0, 0, 0, 0, 1, 0),
        (0, 0, 0, 0, 0, 1),
        (-1, 0, -1, 1, 0, 0),
    ]
    factors_2 = [
        (1, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 1, 0),
        (0, 0, 0, 0, 0, 1),
        (0, -1, -1, 1, 0, 0),
    ]
    projection_ranks = {
        1: [rational_rank(factor_projection_matrix(frames[mode], factors_1)) for mode in range(2, 6)],
        2: [rational_rank(factor_projection_matrix(frames[mode], factors_2)) for mode in range(2, 6)],
    }
    assert projection_ranks == {1: [3, 3, 3, 1], 2: [2, 2, 2, 2]}

    coefficients: dict[tuple[int, ...], int] = {}
    for word in product(range(3), repeat=6):
        rows = [frames[mode][colour] for mode, colour in enumerate(word)]
        coefficients[word] = direct_permanent(rows)

    expected_nonzero = {
        "000000": -4,
        "000120": -4,
        "001110": -4,
        "001200": -4,
        "002010": -4,
        "002220": -4,
        "110001": 8,
        "110121": 8,
        "111111": 8,
        "111201": 8,
        "112011": 8,
        "112221": 8,
        "220002": -2,
        "220122": -2,
        "221112": -2,
        "221202": -2,
        "222012": -2,
        "222222": -2,
    }
    actual_nonzero = {
        "".join(map(str, word)): value
        for word, value in coefficients.items()
        if value
    }
    assert actual_nonzero == expected_nonzero

    standard_p3_support = set(permutations(range(3)))
    colour_permuted_p3_support = {
        (first, (second - 1) % 3, (third + 1) % 3)
        for first, second, third in standard_p3_support
    }
    middle_support = {
        tuple(int(entry) for entry in word[2:5])
        for word in expected_nonzero
    }
    assert colour_permuted_p3_support == middle_support

    canonical = "".join(
        "".join(map(str, word)) + ":" + str(coefficients[word]) + "\n"
        for word in sorted(coefficients)
    )
    digest = sha256(canonical.encode("ascii")).hexdigest()
    assert digest == "1360041c9a60d4451f58f18b978dfb30c86b707bb4fc7c860d7573d4686a7da8"

    distance_histogram: Counter[int] = Counter()
    for word, value in coefficients.items():
        if not value:
            continue
        distance = min(
            sum(entry != colour for entry in word)
            for colour in range(3)
        )
        distance_histogram[distance] += 1
    assert distance_histogram == {0: 3, 2: 9, 3: 6}

    hamming_one = set()
    for colour in range(3):
        for mode in range(6):
            for replacement in range(3):
                if replacement == colour:
                    continue
                word = [colour] * 6
                word[mode] = replacement
                hamming_one.add(tuple(word))
    assert len(hamming_one) == 36
    assert all(coefficients[word] == 0 for word in hamming_one)

    # In particular, all 6*3^(4) words with unequal pair colours vanish.
    pair_mixed = [word for word in coefficients if word[0] != word[1]]
    assert len(pair_mixed) == 6 * 3**4
    assert all(coefficients[word] == 0 for word in pair_mixed)

    return {
        "projection_ranks": projection_ranks,
        "colour_permuted_P3_support": sorted(colour_permuted_p3_support),
        "nonzero_coefficients": actual_nonzero,
        "zero_coefficients": 711,
        "distance_histogram": dict(sorted(distance_histogram.items())),
        "hamming_one_zeros": len(hamming_one),
        "pair_mixed_zeros": len(pair_mixed),
        "all_word_sha256": digest,
    }


def main() -> None:
    pair_basis, pair_ledger = fixed_pair_audit()
    quartic_ledger = quartic_factor_audit(pair_basis)
    missing_factor_ledger = missing_factor_table_audit(pair_basis)
    hyperplane_ledger = hyperplane_product_audit()
    coefficient_ledger = coefficient_audit()

    print("fixed pair-dimension-five independent no-import audit: PASS")
    print(f"  fixed pair: {pair_ledger}")
    print(f"  factorized quartics: {quartic_ledger}")
    print(f"  missing-factor ranks: {missing_factor_ledger['rank_table']}")
    print(f"  modular hyperplane audit: {hyperplane_ledger}")
    print(f"  projection ranks: {coefficient_ledger['projection_ranks']}")
    print(f"  nonzero coefficient count: {len(coefficient_ledger['nonzero_coefficients'])}")
    print(f"  zero coefficient count: {coefficient_ledger['zero_coefficients']}")
    print(f"  Hamming-distance ledger: {coefficient_ledger['distance_histogram']}")
    print(f"  Hamming-one zeros: {coefficient_ledger['hamming_one_zeros']}")
    print(f"  pair-mixed zeros: {coefficient_ledger['pair_mixed_zeros']}")
    print(f"  all-word SHA-256: {coefficient_ledger['all_word_sha256']}")


if __name__ == "__main__":
    main()
