"""Primary exact checks for the fixed-pair Hamming-two split exclusions."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product

import sympy as sp

Vector = tuple[sp.Expr, ...]
Polynomial = dict[int, sp.Expr]

EDGES = list(combinations(range(4), 2))
COMPLEMENT_INDEX = {
    edge: EDGES.index(tuple(sorted(set(range(4)) - set(edge))))
    for edge in EDGES
}
FULL_MASK = (1 << 6) - 1

M1 = (0, 1, -1, 0, 0, -1)
M2 = (0, 0, 0, 1, -1, -1)
D0 = (1, 1, 0, 0, -1, -1)
D1 = (1, 0, -1, 1, 0, -1)
D2 = (0, 0, 0, 0, 0, -2)
PAIR_BASIS = (M1, M2, D0, D1, D2)


def square_free_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply sparse polynomials in the six-variable square-free algebra."""
    result: Polynomial = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(result.get(mask, 0) + left_value * right_value)
    return {mask: value for mask, value in result.items() if value != 0}


def product_of(polynomials: list[Polynomial]) -> Polynomial:
    """Multiply a list of sparse square-free polynomials."""
    result: Polynomial = {0: sp.Integer(1)}
    for polynomial in polynomials:
        result = square_free_multiply(result, polynomial)
    return result


def linear_form(vector: Vector | tuple[int, ...]) -> Polynomial:
    """Encode one degree-one form."""
    return {
        1 << index: sp.sympify(value)
        for index, value in enumerate(vector)
        if value != 0
    }


def quadratic_polynomial(vector: tuple[int, ...]) -> Polynomial:
    """Encode a first-four-variable quadratic in the fixed edge order."""
    return {
        (1 << first) | (1 << second): sp.Integer(value)
        for value, (first, second) in zip(vector, EDGES, strict=True)
        if value
    }


def complement_quartic(vector: tuple[int, ...]) -> Polynomial:
    """Complement a fixed quadratic inside six variables."""
    return {
        FULL_MASK ^ mask: value
        for mask, value in quadratic_polynomial(vector).items()
    }


def quadratic_product(left: Vector, right: Vector) -> Vector:
    """Multiply two first-four-coordinate forms in edge coordinates."""
    return tuple(
        sp.expand(left[first] * right[second] + left[second] * right[first])
        for first, second in EDGES
    )


def complement_pair(quadratic: tuple[int, ...], residual: Vector) -> sp.Expr:
    """Pair two four-variable quadratics by edge complementation."""
    return sp.expand(
        sum(
            quadratic[index] * residual[COMPLEMENT_INDEX[edge]]
            for index, edge in enumerate(EDGES)
        )
    )


def rank(matrix: list[list[sp.Expr]] | list[tuple[int, ...]]) -> int:
    """Return exact matrix rank."""
    return sp.Matrix(matrix).rank()


def assert_factorized_quartics() -> dict[str, Polynomial]:
    """Check the five displayed complementary quartic factorizations."""
    x0 = (1, 0, 0, 0, 0, 0)
    x1 = (0, 1, 0, 0, 0, 0)
    x2 = (0, 0, 1, 0, 0, 0)
    x3 = (0, 0, 0, 1, 0, 0)
    x4 = (0, 0, 0, 0, 1, 0)
    x5 = (0, 0, 0, 0, 0, 1)

    factors = {
        "m1": [x4, x5, x1, tuple(x3[i] - x2[i] - x0[i] for i in range(6))],
        "m2": [x4, x5, x0, tuple(x3[i] - x2[i] - x1[i] for i in range(6))],
        "d0": [
            x4,
            x5,
            tuple(x1[i] + x2[i] for i in range(6)),
            tuple(x3[i] - x0[i] for i in range(6)),
        ],
        "d1": [
            x4,
            x5,
            tuple(x0[i] + x2[i] for i in range(6)),
            tuple(x3[i] - x1[i] for i in range(6)),
        ],
        "d2": [x4, x5, x0, x1],
    }
    vectors = {"m1": M1, "m2": M2, "d0": D0, "d1": D1, "d2": D2}
    ledgers: dict[str, Polynomial] = {}
    for name, factor_frame in factors.items():
        factorized = product_of([linear_form(factor) for factor in factor_frame])
        if name == "d2":
            factorized = {mask: -2 * value for mask, value in factorized.items()}
        expected = complement_quartic(vectors[name])
        assert factorized == expected
        ledgers[name] = expected
    return ledgers


def assert_affine_identities() -> dict[str, sp.Expr]:
    """Derive all five pairings on the affine h(s),Z family symbolically."""
    s, z0, z1, z2 = sp.symbols("s z0 z1 z2")
    z3 = z0 - z1 + z2
    h = (0, 1, s, 1 + s)
    z = (z0, z1, z2, z3)
    residual = quadratic_product(h, z)
    values = {
        "m1": sp.factor(complement_pair(M1, residual)),
        "m2": sp.factor(complement_pair(M2, residual)),
        "d0": sp.factor(complement_pair(D0, residual)),
        "d1": sp.factor(complement_pair(D1, residual)),
        "d2": sp.factor(complement_pair(D2, residual)),
    }
    assert values == {
        "m1": 0,
        "m2": 0,
        "d0": 2 * z2 * (s + 1),
        "d1": 2 * s * (z0 - z1 + z2),
        "d2": -2 * z0,
    }
    return values


def permanent_3(columns: list[Vector]) -> sp.Expr:
    """Compute the three-by-three permanent with the vectors as columns."""
    return sp.expand(
        sum(
            sp.prod(columns[column][permutation[column]] for column in range(3))
            for permutation in permutations(range(3))
        )
    )


def assert_common_plane_factorization() -> dict[str, object]:
    """Check the reference-basis P3 support and Hamming-two singleton map."""
    standard = [
        (sp.Integer(1), sp.Integer(0), sp.Integer(0)),
        (sp.Integer(0), sp.Integer(1), sp.Integer(0)),
        (sp.Integer(0), sp.Integer(0), sp.Integer(1)),
    ]
    tensor = {
        word: permanent_3([standard[colour] for colour in word])
        for word in product(range(3), repeat=3)
    }
    support = {word for word, value in tensor.items() if value}
    assert support == set(permutations(range(3)))

    singleton_witnesses: dict[tuple[int, ...], int] = {}
    for word in product(range(3), repeat=3):
        if word[0] == word[1] == word[2]:
            continue
        counts = Counter(word)
        singleton = next(colour for colour, count in counts.items() if count == 1)
        full_word = (singleton, singleton, *word, singleton)
        assert sum(colour != singleton for colour in full_word) == 2
        singleton_witnesses[word] = singleton
    assert len(singleton_witnesses) == 24
    return {
        "P3_support": sorted(support),
        "nonconstant_triples_mapped_to_H2": len(singleton_witnesses),
    }


def assert_affine_d2_factorization() -> dict[str, object]:
    """Expand the d2 component on all affine reference-basis words."""
    s2, s3, s4, z0, z1, z2 = sp.symbols("s2 s3 s4 z0 z1 z2")
    z3 = z0 - z1 + z2
    x4 = (0, 0, 0, 0, 1, 0)
    x5 = (0, 0, 0, 0, 0, 1)
    h2 = (0, 1, s2, 1 + s2, 0, 0)
    h3 = (0, 1, s3, 1 + s3, 0, 0)
    h4 = (0, 1, s4, 1 + s4, 0, 0)
    z = (z0, z1, z2, z3, 0, 0)
    frames = [(x4, x5, h2), (x4, x5, h3), (x4, x5, h4)]

    ledger: dict[tuple[int, int, int], sp.Expr] = {}
    for word in product(range(3), repeat=3):
        value = product_of([
            quadratic_polynomial(D2),
            *(linear_form(frames[mode][word[mode]]) for mode in range(3)),
            linear_form(z),
        ]).get(FULL_MASK, 0)
        predicted = -2 * z0 if word in set(permutations(range(3))) else 0
        assert sp.expand(value - predicted) == 0
        ledger[word] = sp.expand(value)

    radius_entries = {}
    for second in range(3):
        for third in range(3):
            if (second, third) == (2, 2):
                continue
            distance = int(second != 2) + int(third != 2)
            assert distance in (1, 2)
            radius_entries[(2, second, third)] = distance
    assert len(radius_entries) == 8
    return {
        "reference_tensor": ledger,
        "colour_2_slice_entries_in_radius": radius_entries,
    }


def assert_slice_rank_obstruction() -> dict[str, object]:
    """Check the exact principal minors excluding rank-one P3 slices."""
    a0, a1, a2 = sp.symbols("a0 a1 a2")
    matrix = sp.Matrix([
        [0, a2, a1],
        [a2, 0, a0],
        [a1, a0, 0],
    ])
    minors = {
        "01": sp.factor(matrix.extract((0, 1), (0, 1)).det()),
        "02": sp.factor(matrix.extract((0, 2), (0, 2)).det()),
        "12": sp.factor(matrix.extract((1, 2), (1, 2)).det()),
    }
    assert minors == {"01": -a2**2, "02": -a1**2, "12": -a0**2}
    return {"slice_matrix": matrix, "principal_minors": minors}


def sharp_fixture_frames() -> list[list[tuple[int, ...]]]:
    """Return all six frames of the previous Hamming-one sharp fixture."""
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


def fixture_coefficient(frames: list[list[tuple[int, ...]]], word: tuple[int, ...]) -> int:
    """Compute one fixture coefficient by exact square-free multiplication."""
    return int(product_of([
        linear_form(frames[mode][colour])
        for mode, colour in enumerate(word)
    ]).get(FULL_MASK, 0))


def assert_sharp_fixture() -> dict[str, object]:
    """Reconstruct the affine-family fixture, ranks, shells, and table hash."""
    frames = sharp_fixture_frames()
    assert [sp.Matrix(frame).T.rank() for frame in frames] == [3] * 6

    z_normal = sp.Matrix([[-1, 1, -1, 1, 0, 0]])
    assert z_normal * sp.Matrix(frames[5]).T == sp.zeros(1, 3)

    h = tuple(sp.Integer(value) for value in frames[2][2][:4])
    pair_matrix = []
    for quadratic in PAIR_BASIS:
        row = []
        for z in frames[5]:
            residual = quadratic_product(h, tuple(map(sp.Integer, z[:4])))
            row.append(int(complement_pair(quadratic, residual)))
        pair_matrix.append(row)
    assert pair_matrix == [
        [0, 0, 0],
        [0, 0, 0],
        [-4, 0, 0],
        [0, 8, 0],
        [0, 0, -2],
    ]

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
        1: [rank([[sum(a * b for a, b in zip(factor, colour, strict=True)) for colour in frames[mode]] for factor in factors_1]) for mode in range(2, 6)],
        2: [rank([[sum(a * b for a, b in zip(factor, colour, strict=True)) for colour in frames[mode]] for factor in factors_2]) for mode in range(2, 6)],
    }
    assert projection_ranks == {1: [3, 3, 3, 1], 2: [2, 2, 2, 2]}

    coefficients = {
        word: fixture_coefficient(frames, word)
        for word in product(range(3), repeat=6)
    }
    canonical = "".join(
        "".join(map(str, word)) + ":" + str(coefficients[word]) + "\n"
        for word in sorted(coefficients)
    )
    digest = sha256(canonical.encode("ascii")).hexdigest()
    assert digest == "1360041c9a60d4451f58f18b978dfb30c86b707bb4fc7c860d7573d4686a7da8"

    shell_histogram: Counter[int] = Counter()
    for word, value in coefficients.items():
        if not value:
            continue
        anchor = (word[0],) * 6
        shell_histogram[sum(a != b for a, b in zip(word, anchor, strict=True))] += 1
    assert shell_histogram == {0: 3, 2: 9, 3: 6}
    return {
        "pairing_matrix": pair_matrix,
        "projection_ranks": projection_ranks,
        "shell_histogram": dict(sorted(shell_histogram.items())),
        "all_word_sha256": digest,
    }


def main() -> None:
    quartics = assert_factorized_quartics()
    affine = assert_affine_identities()
    common = assert_common_plane_factorization()
    affine_d2 = assert_affine_d2_factorization()
    slices = assert_slice_rank_obstruction()
    fixture = assert_sharp_fixture()

    print("fixed-pair Hamming-two split-component primary checks: PASS")
    print(f"  factorized quartics: {quartics}")
    print(f"  affine identities: {affine}")
    print(f"  common-plane H2 map: {common}")
    print(f"  affine d2 radius entries: {affine_d2['colour_2_slice_entries_in_radius']}")
    print(f"  P3 slice principal minors: {slices['principal_minors']}")
    print(f"  sharp fixture pairing matrix: {fixture['pairing_matrix']}")
    print(f"  sharp fixture projection ranks: {fixture['projection_ranks']}")
    print(f"  sharp fixture shell histogram: {fixture['shell_histogram']}")
    print(f"  sharp fixture SHA-256: {fixture['all_word_sha256']}")


if __name__ == "__main__":
    main()
