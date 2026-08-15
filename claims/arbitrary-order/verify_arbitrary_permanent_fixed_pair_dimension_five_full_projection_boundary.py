"""Primary exact checks for the fixed pair-dimension-five boundary."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product

import sympy as sp

Polynomial = dict[int, sp.Expr]
Vector = tuple[int, ...]

VARIABLE_COUNT = 6
FULL_MASK = (1 << VARIABLE_COUNT) - 1
EDGES_4 = list(combinations(range(4), 2))
EDGE_MASKS_4 = [(1 << first) | (1 << second) for first, second in EDGES_4]


def square_free_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply in the square-free algebra on six variables."""
    result: Polynomial = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(
                result.get(mask, sp.Integer(0)) + left_value * right_value
            )
    return {mask: value for mask, value in result.items() if value != 0}


def product_of(polynomials: list[Polynomial]) -> Polynomial:
    """Multiply a list of square-free polynomials."""
    result: Polynomial = {0: sp.Integer(1)}
    for polynomial in polynomials:
        result = square_free_multiply(result, polynomial)
    return result


def linear_form(vector: tuple[sp.Expr, ...] | Vector) -> Polynomial:
    """Encode a coordinate vector as a degree-one square-free form."""
    return {
        1 << index: sp.sympify(value)
        for index, value in enumerate(vector)
        if value != 0
    }


def quadratic_vector(polynomial: Polynomial) -> tuple[sp.Expr, ...]:
    """Read the first-four-variable quadratic in the fixed edge order."""
    return tuple(polynomial.get(mask, sp.Integer(0)) for mask in EDGE_MASKS_4)


def polynomial_from_quadratic(vector: tuple[sp.Expr, ...] | Vector) -> Polynomial:
    """Encode a quadratic coefficient vector in the fixed edge order."""
    return {
        mask: sp.sympify(value)
        for mask, value in zip(EDGE_MASKS_4, vector, strict=True)
        if value != 0
    }


def dot(left: tuple[sp.Expr, ...] | Vector, right: tuple[sp.Expr, ...] | Vector) -> sp.Expr:
    """Return an exact coordinate dot product."""
    return sp.expand(sum(a * b for a, b in zip(left, right, strict=True)))


def fixed_pair() -> tuple[list[Vector], list[Vector]]:
    """Return the two fixed local colour frames."""
    left = [
        (1, 0, 0, -1, 0, 0),
        (0, 1, 0, -1, 0, 0),
        (0, 0, 1, -1, 0, 0),
    ]
    right = [
        (0, 1, 1, 0, 0, 0),
        (1, 0, 1, 0, 0, 0),
        (0, 0, 1, -1, 0, 0),
    ]
    return left, right


def assert_fixed_pair_algebra() -> tuple[list[tuple[int, ...]], dict[str, object]]:
    """Check the nine products, five-space, radical, and annihilator."""
    left, right = fixed_pair()
    products = [
        [
            tuple(int(value) for value in quadratic_vector(product_of([
                linear_form(left_colour),
                linear_form(right_colour),
            ])))
            for right_colour in right
        ]
        for left_colour in left
    ]

    diagonal = [
        (1, 1, 0, 0, -1, -1),
        (1, 0, -1, 1, 0, -1),
        (0, 0, 0, 0, 0, -2),
    ]
    mixed = [
        (0, 1, -1, 0, 0, -1),
        (0, 0, 0, 1, -1, -1),
    ]
    expected = [
        [diagonal[0], mixed[0], mixed[0]],
        [mixed[1], diagonal[1], mixed[1]],
        [mixed[1], mixed[0], diagonal[2]],
    ]
    assert products == expected

    basis = [mixed[0], mixed[1], *diagonal]
    basis_matrix = sp.Matrix(basis)
    assert basis_matrix.rank() == 5
    assert sp.Matrix(mixed).rank() == 2
    annihilator = sp.Matrix((0, 1, 1, 1, 1, 0))
    assert basis_matrix * annihilator == sp.zeros(5, 1)
    assert len(basis_matrix.nullspace()) == 1

    return basis, {
        "edge_order": EDGES_4,
        "product_table": products,
        "basis_rank": basis_matrix.rank(),
        "mixed_rank": sp.Matrix(mixed).rank(),
        "annihilator": tuple(annihilator),
    }


def hodge_complement(quadratic: Polynomial) -> Polynomial:
    """Complement a first-four-variable quadratic inside six variables."""
    return {FULL_MASK ^ mask: value for mask, value in quadratic.items()}


def permanent(matrix: list[list[sp.Expr]]) -> sp.Expr:
    """Compute a small permanent by direct permutation expansion."""
    size = len(matrix)
    return sp.expand(
        sum(
            sp.prod(matrix[row][permutation[row]] for row in range(size))
            for permutation in permutations(range(size))
        )
    )


def assert_mixed_quartics(basis: list[tuple[int, ...]]) -> dict[str, object]:
    """Check both factorized Hodge quartics and their four-linear tensors."""
    x1 = (0, 1, 0, 0, 0, 0)
    x4 = (0, 0, 0, 0, 1, 0)
    x5 = (0, 0, 0, 0, 0, 1)
    ell1 = (-1, 0, -1, 1, 0, 0)
    x0 = (1, 0, 0, 0, 0, 0)
    ell2 = (0, -1, -1, 1, 0, 0)
    factor_frames = [(x1, x4, x5, ell1), (x0, x4, x5, ell2)]

    quartic_ledgers: list[dict[int, sp.Expr]] = []
    for mixed, factors in zip(basis[:2], factor_frames, strict=True):
        hodge = hodge_complement(polynomial_from_quadratic(mixed))
        factorized = product_of([linear_form(factor) for factor in factors])
        assert hodge == factorized

        # Equality on all coordinate inputs checks every entry of the
        # four-linear tensor, including all repeated-coordinate zeros.
        for coordinate_tuple in product(range(6), repeat=4):
            local_forms = [
                linear_form(tuple(int(index == coordinate) for index in range(6)))
                for coordinate in coordinate_tuple
            ]
            left_value = product_of([
                polynomial_from_quadratic(mixed),
                *local_forms,
            ]).get(FULL_MASK, sp.Integer(0))
            evaluation = [
                [factor[coordinate] for coordinate in coordinate_tuple]
                for factor in factors
            ]
            assert left_value == permanent(evaluation)
        quartic_ledgers.append(hodge)

    return {
        "F1": quartic_ledgers[0],
        "F2": quartic_ledgers[1],
        "coordinate_tensor_entries_checked": 2 * 6**4,
    }


def kernel_basis(normals: tuple[Vector, Vector]) -> list[tuple[sp.Expr, ...]]:
    """Return an exact basis for the common kernel of two covectors."""
    return [tuple(vector) for vector in sp.Matrix(normals).nullspace()]


def fourfold_products(basis: list[tuple[sp.Expr, ...]]) -> list[Polynomial]:
    """Generate the fourth product power of a linear subspace."""
    encoded = [linear_form(vector) for vector in basis]
    return [
        product_of([encoded[index] for index in indices])
        for indices in combinations_with_replacement(range(len(encoded)), 4)
    ]


def pairing_row(
    quartic: Polynomial,
    pair_basis: list[tuple[int, ...]],
) -> list[sp.Expr]:
    """Pair one quartic with the fixed quadratic basis."""
    return [
        product_of([
            polynomial_from_quadratic(quadratic),
            quartic,
        ]).get(FULL_MASK, sp.Integer(0))
        for quadratic in pair_basis
    ]


def assert_missing_factor_table(
    pair_basis: list[tuple[int, ...]],
) -> dict[str, object]:
    """Generate all 16 common-kernel product spaces and rank their maps."""
    normals_1 = {
        "x1": (0, 1, 0, 0, 0, 0),
        "x4": (0, 0, 0, 0, 1, 0),
        "x5": (0, 0, 0, 0, 0, 1),
        "ell1": (-1, 0, -1, 1, 0, 0),
    }
    normals_2 = {
        "x0": (1, 0, 0, 0, 0, 0),
        "x4": (0, 0, 0, 0, 1, 0),
        "x5": (0, 0, 0, 0, 0, 1),
        "ell2": (0, -1, -1, 1, 0, 0),
    }
    expected = {
        "x1": {"x0": 1, "x4": 0, "x5": 0, "ell2": 2},
        "x4": {"x0": 0, "x4": 0, "x5": 0, "ell2": 0},
        "x5": {"x0": 0, "x4": 0, "x5": 0, "ell2": 0},
        "ell1": {"x0": 2, "x4": 0, "x5": 0, "ell2": 2},
    }

    ranks: dict[str, dict[str, int]] = {}
    generated_dimensions: dict[tuple[str, str], int] = {}
    for first_name, first_normal in normals_1.items():
        ranks[first_name] = {}
        for second_name, second_normal in normals_2.items():
            basis = kernel_basis((first_normal, second_normal))
            products_4 = fourfold_products(basis)
            degree_4_masks = [
                sum(1 << index for index in support)
                for support in combinations(range(6), 4)
            ]
            product_matrix = sp.Matrix([
                [polynomial.get(mask, sp.Integer(0)) for mask in degree_4_masks]
                for polynomial in products_4
            ])
            map_matrix = sp.Matrix([
                pairing_row(polynomial, pair_basis)
                for polynomial in products_4
            ])
            ranks[first_name][second_name] = map_matrix.rank()
            generated_dimensions[(first_name, second_name)] = product_matrix.rank()

    assert ranks == expected

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
    complement_index = {
        edge: EDGES_4.index(tuple(sorted(set(range(4)) - set(edge))))
        for edge in EDGES_4
    }
    exact_maps: dict[tuple[str, str], list[list[int]]] = {}
    for names, residual_basis in residual_bases.items():
        matrix = [
            [
                sum(
                    residual[index] * quadratic[complement_index[edge]]
                    for index, edge in enumerate(EDGES_4)
                )
                for quadratic in pair_basis
            ]
            for residual in residual_basis
        ]
        exact_maps[names] = matrix

    expected_maps = {
        ("x1", "x0"): [[0, 0, 1, 1, 0]],
        ("x1", "ell2"): [[0, 0, -1, 1, 0], [0, 0, 1, 1, 0]],
        ("ell1", "x0"): [[0, 0, 1, -1, 0], [0, 0, 1, 1, 0]],
        ("ell1", "ell2"): [
            [0, 0, 0, 0, -2],
            [0, 0, 1, 1, 0],
            [0, 0, 1, 1, 0],
        ],
    }
    assert exact_maps == expected_maps
    for names, matrix in exact_maps.items():
        first_name, second_name = names
        assert sp.Matrix(matrix).rank() == expected[first_name][second_name]

    return {
        "rank_table": ranks,
        "fourfold_product_dimensions": generated_dimensions,
        "nonzero_rank_maps": exact_maps,
    }


def assert_hyperplane_product_samples() -> dict[str, object]:
    """Replay the proportional dimension formula and independent lower bound."""
    edge_masks = EDGE_MASKS_4

    def product_space_rank(left_basis: list[sp.Matrix], right_basis: list[sp.Matrix]) -> int:
        vectors = []
        for left in left_basis:
            for right in right_basis:
                polynomial = square_free_multiply(
                    linear_form(tuple(left)),
                    linear_form(tuple(right)),
                )
                vectors.append([polynomial.get(mask, 0) for mask in edge_masks])
        return sp.Matrix(vectors).rank()

    proportional: dict[int, int] = {}
    for support_size in range(1, 5):
        normal = tuple(
            index + 1 if index < support_size else 0
            for index in range(4)
        )
        basis = sp.Matrix([normal]).nullspace()
        actual = product_space_rank(basis, basis)
        assert actual == 2 + support_size
        proportional[support_size] = actual

    independent_normals = [
        ((1, 0, 0, 0), (0, 1, 0, 0)),
        ((1, 1, 0, 0), (0, 1, 1, 0)),
        ((1, 2, 3, 4), (2, -1, 1, 3)),
    ]
    independent_ranks = []
    for first, second in independent_normals:
        left_basis = sp.Matrix([first]).nullspace()
        right_basis = sp.Matrix([second]).nullspace()
        actual = product_space_rank(left_basis, right_basis)
        assert actual >= 4
        independent_ranks.append(actual)

    return {
        "proportional_support_to_dimension": proportional,
        "independent_sample_ranks": independent_ranks,
    }


def sharpness_frames() -> list[list[Vector]]:
    """Return all six ordered colour frames of the Hamming-one model."""
    left, right = fixed_pair()
    x4 = (0, 0, 0, 0, 1, 0)
    x5 = (0, 0, 0, 0, 0, 1)
    h = (0, 1, -2, -1, 0, 0)
    b0 = (0, 2, 2, 0, 0, 0)
    b1 = (0, 2, 0, -2, 0, 0)
    b2 = (1, 1, 0, 0, 0, 0)
    return [
        left,
        right,
        [x4, x5, h],
        [x5, h, x4],
        [h, x4, x5],
        [b0, b1, b2],
    ]


def projection_matrix(frame: list[Vector], factors: list[Vector]) -> sp.Matrix:
    """Evaluate one factor frame on one local colour frame."""
    return sp.Matrix([
        [dot(factor, colour) for colour in frame]
        for factor in factors
    ])


def tensor_coefficient(frames: list[list[Vector]], word: tuple[int, ...]) -> int:
    """Compute one six-mode coefficient by square-free subset multiplication."""
    polynomial = product_of([
        linear_form(frames[mode][colour])
        for mode, colour in enumerate(word)
    ])
    return int(polynomial.get(FULL_MASK, 0))


def assert_sharpness_model(pair_basis: list[tuple[int, ...]]) -> dict[str, object]:
    """Check local ranks, projections, and every one of the 729 coefficients."""
    frames = sharpness_frames()
    assert [sp.Matrix(frame).T.rank() for frame in frames] == [3] * 6

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
    projection_matrices = {
        1: [projection_matrix(frames[mode], factors_1) for mode in range(2, 6)],
        2: [projection_matrix(frames[mode], factors_2) for mode in range(2, 6)],
    }
    projection_ranks = {
        key: [matrix.rank() for matrix in matrices]
        for key, matrices in projection_matrices.items()
    }
    assert projection_ranks == {1: [3, 3, 3, 1], 2: [2, 2, 2, 2]}

    # The three constant complementary products are diagonal duals on B.
    constant_pairing = []
    for colour in range(3):
        quartic = product_of([
            linear_form(frames[mode][colour])
            for mode in range(2, 6)
        ])
        constant_pairing.append([
            int(value) for value in pairing_row(quartic, pair_basis)
        ])
    assert constant_pairing == [
        [0, 0, -4, 0, 0],
        [0, 0, 0, 8, 0],
        [0, 0, 0, 0, -2],
    ]

    coefficients = {
        word: tensor_coefficient(frames, word)
        for word in product(range(3), repeat=6)
    }
    permitted_triples = {
        (0, 0, 0),
        (0, 1, 2),
        (1, 1, 1),
        (1, 2, 0),
        (2, 0, 1),
        (2, 2, 2),
    }
    permanent_support_3 = set(permutations(range(3)))
    colour_permuted_support = {
        (first, (second - 1) % 3, (third + 1) % 3)
        for first, second, third in permanent_support_3
    }
    assert colour_permuted_support == permitted_triples
    pure_values = {0: -4, 1: 8, 2: -2}
    for word, value in coefficients.items():
        predicted = (
            pure_values[word[0]]
            if word[0] == word[1] == word[5]
            and word[2:5] in permitted_triples
            else 0
        )
        assert value == predicted

    canonical = "".join(
        "".join(map(str, word)) + ":" + str(coefficients[word]) + "\n"
        for word in sorted(coefficients)
    )
    digest = sha256(canonical.encode("ascii")).hexdigest()
    assert digest == "1360041c9a60d4451f58f18b978dfb30c86b707bb4fc7c860d7573d4686a7da8"

    nonzero = {word: value for word, value in coefficients.items() if value}
    assert len(nonzero) == 18
    distance_histogram: Counter[int] = Counter()
    for word in nonzero:
        distance = min(
            sum(entry != colour for entry in word)
            for colour in range(3)
        )
        distance_histogram[distance] += 1
    assert distance_histogram == {0: 3, 2: 9, 3: 6}

    hamming_one_words: set[tuple[int, ...]] = set()
    for colour in range(3):
        for mode in range(6):
            for replacement in range(3):
                if replacement == colour:
                    continue
                word = [colour] * 6
                word[mode] = replacement
                hamming_one_words.add(tuple(word))
    assert len(hamming_one_words) == 36
    assert all(coefficients[word] == 0 for word in hamming_one_words)

    return {
        "projection_matrices": projection_matrices,
        "projection_ranks": projection_ranks,
        "constant_pairing_on_B": constant_pairing,
        "colour_permuted_P3_support": sorted(colour_permuted_support),
        "nonzero_coefficients": nonzero,
        "zero_coefficients": 729 - len(nonzero),
        "distance_histogram": dict(sorted(distance_histogram.items())),
        "hamming_one_zeros": len(hamming_one_words),
        "all_word_sha256": digest,
    }


def main() -> None:
    pair_basis, pair_ledger = assert_fixed_pair_algebra()
    quartic_ledger = assert_mixed_quartics(pair_basis)
    hyperplane_ledger = assert_hyperplane_product_samples()
    missing_factor_ledger = assert_missing_factor_table(pair_basis)
    sharpness_ledger = assert_sharpness_model(pair_basis)

    print("fixed pair-dimension-five full-projection primary checks: PASS")
    print(f"  fixed pair: {pair_ledger}")
    print(f"  mixed quartics: {quartic_ledger}")
    print(f"  hyperplane samples: {hyperplane_ledger}")
    print(f"  missing-factor ranks: {missing_factor_ledger['rank_table']}")
    print(f"  exact nonzero rank maps: {missing_factor_ledger['nonzero_rank_maps']}")
    print(f"  projection ranks: {sharpness_ledger['projection_ranks']}")
    print(f"  nonzero coefficient count: {len(sharpness_ledger['nonzero_coefficients'])}")
    print(f"  zero coefficient count: {sharpness_ledger['zero_coefficients']}")
    print(f"  Hamming-distance ledger: {sharpness_ledger['distance_histogram']}")
    print(f"  Hamming-one zeros: {sharpness_ledger['hamming_one_zeros']}")
    print(f"  all-word SHA-256: {sharpness_ledger['all_word_sha256']}")


if __name__ == "__main__":
    main()
