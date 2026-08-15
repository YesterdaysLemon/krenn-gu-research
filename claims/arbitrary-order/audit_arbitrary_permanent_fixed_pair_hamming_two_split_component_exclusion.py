"""Independent no-import audit of the fixed-pair Hamming-two exclusions."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product

Vector = tuple[int, ...]

EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
COMPLEMENT = (5, 4, 3, 2, 1, 0)
M1 = (0, 1, -1, 0, 0, -1)
M2 = (0, 0, 0, 1, -1, -1)
D0 = (1, 1, 0, 0, -1, -1)
D1 = (1, 0, -1, 1, 0, -1)
D2 = (0, 0, 0, 0, 0, -2)
PAIR_BASIS = (M1, M2, D0, D1, D2)
PERMUTATIONS_6 = list(permutations(range(6)))


def quadratic_product(left: Vector, right: Vector) -> Vector:
    """Multiply first-four-coordinate forms in edge coordinates."""
    return tuple(
        left[first] * right[second] + left[second] * right[first]
        for first, second in EDGES
    )


def complement_pair(quadratic: Vector, residual: Vector) -> int:
    """Pair quadratics by four-variable edge complementation."""
    return sum(
        quadratic[index] * residual[COMPLEMENT[index]]
        for index in range(6)
    )


def rational_rank(rows: list[list[int]] | list[Vector]) -> int:
    """Compute exact rank by local Fraction elimination."""
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


def modular_rank(rows: list[Vector], prime: int) -> int:
    """Compute rank over a prime field with separate modular elimination."""
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


def sparse_linear(vector: Vector) -> dict[int, int]:
    """Encode one linear form by square-free bit masks."""
    return {
        1 << index: value
        for index, value in enumerate(vector)
        if value
    }


def sparse_multiply(
    left: dict[int, int],
    right: dict[int, int],
    modulus: int | None = None,
) -> dict[int, int]:
    """Multiply sparse square-free polynomials, optionally modulo a prime."""
    result: dict[int, int] = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            value = result.get(mask, 0) + left_value * right_value
            result[mask] = value % modulus if modulus else value
    return {mask: value for mask, value in result.items() if value}


def sparse_product(
    polynomials: list[dict[int, int]],
    modulus: int | None = None,
) -> dict[int, int]:
    """Multiply a list of sparse polynomials."""
    result = {0: 1}
    for polynomial in polynomials:
        result = sparse_multiply(result, polynomial, modulus)
    return result


def factorization_audit() -> dict[str, dict[int, int]]:
    """Reconstruct all five factorized quartics by independent sparse products."""
    x0 = (1, 0, 0, 0, 0, 0)
    x1 = (0, 1, 0, 0, 0, 0)
    x2 = (0, 0, 1, 0, 0, 0)
    x3 = (0, 0, 0, 1, 0, 0)
    x4 = (0, 0, 0, 0, 1, 0)
    x5 = (0, 0, 0, 0, 0, 1)
    frames = {
        "m1": [x4, x5, x1, tuple(x3[i] - x2[i] - x0[i] for i in range(6))],
        "m2": [x4, x5, x0, tuple(x3[i] - x2[i] - x1[i] for i in range(6))],
        "d0": [x4, x5, tuple(x1[i] + x2[i] for i in range(6)), tuple(x3[i] - x0[i] for i in range(6))],
        "d1": [x4, x5, tuple(x0[i] + x2[i] for i in range(6)), tuple(x3[i] - x1[i] for i in range(6))],
        "d2": [x4, x5, x0, x1],
    }
    quadratic_vectors = {"m1": M1, "m2": M2, "d0": D0, "d1": D1, "d2": D2}
    full_mask = (1 << 6) - 1
    ledgers: dict[str, dict[int, int]] = {}
    for name, frame in frames.items():
        actual = sparse_product([sparse_linear(vector) for vector in frame])
        if name == "d2":
            actual = {mask: -2 * value for mask, value in actual.items()}
        expected = {}
        for coefficient, (first, second) in zip(quadratic_vectors[name], EDGES, strict=True):
            if coefficient:
                expected[full_mask ^ ((1 << first) | (1 << second))] = coefficient
        assert actual == expected
        ledgers[name] = actual
    return ledgers


def hamming_combinatorics_audit() -> dict[str, object]:
    """Audit the H2-alone singleton argument and the affine radius-two slice."""
    singleton_histogram: Counter[int] = Counter()
    nonconstant = 0
    for word in product(range(3), repeat=3):
        counts = Counter(word)
        if len(counts) == 1:
            continue
        singleton = next(colour for colour, count in counts.items() if count == 1)
        full_word = (singleton, singleton, *word, singleton)
        distance = sum(colour != singleton for colour in full_word)
        assert distance == 2
        singleton_histogram[singleton] += 1
        nonconstant += 1
    assert nonconstant == 24

    affine_slice_distances = Counter()
    for second, third in product(range(3), repeat=2):
        if (second, third) == (2, 2):
            continue
        distance = int(second != 2) + int(third != 2)
        assert distance in (1, 2)
        affine_slice_distances[distance] += 1
    assert affine_slice_distances == {1: 4, 2: 4}
    return {
        "common_nonconstant_triples": nonconstant,
        "singleton_colour_histogram": dict(sorted(singleton_histogram.items())),
        "affine_slice_distance_histogram": dict(sorted(affine_slice_distances.items())),
    }


def finite_field_affine_audit() -> dict[str, object]:
    """Exhaust the affine identities and d2 reference tensor over F_5."""
    prime = 5
    identity_cases = 0
    for s, z0, z1, z2 in product(range(prime), repeat=4):
        z3 = (z0 - z1 + z2) % prime
        h = (0, 1, s, (1 + s) % prime)
        z = (z0, z1, z2, z3)
        residual = quadratic_product(h, z)
        values = tuple(complement_pair(q, residual) % prime for q in PAIR_BASIS)
        expected = (
            0,
            0,
            2 * (1 + s) * z2,
            2 * s * z3,
            -2 * z0,
        )
        assert values == tuple(value % prime for value in expected)
        identity_cases += 1
    assert identity_cases == prime**4

    full_mask = (1 << 6) - 1
    d2_polynomial = {(1 << 2) | (1 << 3): -2 % prime}
    reference_cases = 0
    permanent_support = set(permutations(range(3)))
    for s_values in product(range(prime), repeat=3):
        x4 = (0, 0, 0, 0, 1, 0)
        x5 = (0, 0, 0, 0, 0, 1)
        frames = [
            (x4, x5, (0, 1, s, (1 + s) % prime, 0, 0))
            for s in s_values
        ]
        for word in product(range(3), repeat=3):
            for z0, z1, z2 in product(range(prime), repeat=3):
                z3 = (z0 - z1 + z2) % prime
                z = (z0, z1, z2, z3, 0, 0)
                value = sparse_product([
                    d2_polynomial,
                    *(sparse_linear(frames[mode][word[mode]]) for mode in range(3)),
                    sparse_linear(z),
                ], prime).get(full_mask, 0)
                expected = -2 * z0 if word in permanent_support else 0
                assert value == expected % prime
                reference_cases += 1
    assert reference_cases == prime**3 * 3**3 * prime**3
    return {
        "field": prime,
        "affine_identity_cases": identity_cases,
        "d2_reference_tensor_cases": reference_cases,
    }


def slice_space_audit() -> dict[str, object]:
    """Exhaust the P3 slice-space ranks over F_5."""
    prime = 5
    histogram: Counter[int] = Counter()
    for a0, a1, a2 in product(range(prime), repeat=3):
        matrix = (
            (0, a2, a1),
            (a2, 0, a0),
            (a1, a0, 0),
        )
        matrix_rank = modular_rank(list(matrix), prime)
        histogram[matrix_rank] += 1
        if (a0, a1, a2) != (0, 0, 0):
            assert matrix_rank >= 2
    assert histogram[0] == 1
    assert histogram[1] == 0
    return {"field": prime, "rank_histogram": dict(sorted(histogram.items()))}


def sharp_frames() -> list[list[Vector]]:
    """Return the prior six-mode sharp fixture."""
    x4 = (0, 0, 0, 0, 1, 0)
    x5 = (0, 0, 0, 0, 0, 1)
    h = (0, 1, -2, -1, 0, 0)
    return [
        [(1, 0, 0, -1, 0, 0), (0, 1, 0, -1, 0, 0), (0, 0, 1, -1, 0, 0)],
        [(0, 1, 1, 0, 0, 0), (1, 0, 1, 0, 0, 0), (0, 0, 1, -1, 0, 0)],
        [x4, x5, h],
        [x5, h, x4],
        [h, x4, x5],
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


def fixture_audit() -> dict[str, object]:
    """Check family inclusion and all coefficients by direct permanents."""
    frames = sharp_frames()
    assert [rational_rank([list(row) for row in zip(*frame, strict=True)]) for frame in frames] == [3] * 6
    assert all(-z[0] + z[1] - z[2] + z[3] == 0 for z in frames[5])

    h = frames[2][2][:4]
    pairing_matrix = [
        [complement_pair(q, quadratic_product(h, z[:4])) for z in frames[5]]
        for q in PAIR_BASIS
    ]
    assert pairing_matrix == [
        [0, 0, 0],
        [0, 0, 0],
        [-4, 0, 0],
        [0, 8, 0],
        [0, 0, -2],
    ]

    coefficients = {}
    for word in product(range(3), repeat=6):
        coefficients[word] = direct_permanent([
            frames[mode][colour]
            for mode, colour in enumerate(word)
        ])
    canonical = "".join(
        "".join(map(str, word)) + ":" + str(coefficients[word]) + "\n"
        for word in sorted(coefficients)
    )
    digest = sha256(canonical.encode("ascii")).hexdigest()
    assert digest == "1360041c9a60d4451f58f18b978dfb30c86b707bb4fc7c860d7573d4686a7da8"

    shell_histogram: Counter[int] = Counter()
    for word, value in coefficients.items():
        if value:
            anchor = (word[0],) * 6
            shell_histogram[sum(a != b for a, b in zip(word, anchor, strict=True))] += 1
    assert shell_histogram == {0: 3, 2: 9, 3: 6}
    return {
        "pairing_matrix": pairing_matrix,
        "shell_histogram": dict(sorted(shell_histogram.items())),
        "all_word_sha256": digest,
    }


def main() -> None:
    quartics = factorization_audit()
    hamming = hamming_combinatorics_audit()
    affine = finite_field_affine_audit()
    slices = slice_space_audit()
    fixture = fixture_audit()

    print("fixed-pair Hamming-two split-component independent audit: PASS")
    print(f"  factorized quartics: {quartics}")
    print(f"  Hamming combinatorics: {hamming}")
    print(f"  exhaustive affine audit: {affine}")
    print(f"  exhaustive P3 slice ranks: {slices}")
    print(f"  sharp fixture pairing matrix: {fixture['pairing_matrix']}")
    print(f"  sharp fixture shell histogram: {fixture['shell_histogram']}")
    print(f"  sharp fixture SHA-256: {fixture['all_word_sha256']}")


if __name__ == "__main__":
    main()
