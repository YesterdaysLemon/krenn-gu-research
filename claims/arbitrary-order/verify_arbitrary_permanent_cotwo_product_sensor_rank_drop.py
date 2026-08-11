"""Primary exact checks for the co-two permanent product-sensor theorem."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
from math import comb

import sympy as sp

SquareFree = dict[int, int]


def masks_of_degree(r: int, degree: int) -> list[int]:
    """Return square-free monomial masks in lexicographic support order."""
    return [
        sum(1 << index for index in support)
        for support in combinations(range(r), degree)
    ]


def square_free_multiply(left: SquareFree, right: SquareFree) -> SquareFree:
    """Multiply in K[x_0,...,x_(r-1)]/(x_0^2,...,x_(r-1)^2)."""
    result: SquareFree = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = result.get(mask, 0) + left_value * right_value
    return {mask: value for mask, value in result.items() if value}


def product_of(forms: list[SquareFree]) -> SquareFree:
    """Multiply a list of square-free forms exactly."""
    result: SquareFree = {0: 1}
    for form in forms:
        result = square_free_multiply(result, form)
    return result


def linear_form(coefficients: list[int]) -> SquareFree:
    """Encode a degree-one form."""
    return {
        1 << index: coefficient
        for index, coefficient in enumerate(coefficients)
        if coefficient
    }


def assert_perfect_complement_pairing() -> dict[int, int]:
    """Check the degree-two/degree-(r-2) complement pairing."""
    ledger: dict[int, int] = {}
    for r in range(3, 9):
        rows = masks_of_degree(r, 2)
        columns = masks_of_degree(r, r - 2)
        full_mask = (1 << r) - 1
        matrix = sp.Matrix(
            [
                [int((row & column) == 0 and (row | column) == full_mask)
                 for column in columns]
                for row in rows
            ]
        )
        rank = matrix.rank()
        assert rank == comb(r, 2)
        assert all(sum(matrix[row, column] for column in range(len(columns))) == 1
                   for row in range(len(rows)))
        ledger[r] = rank
    return ledger


def multiplication_matrix(coefficients: list[int]) -> sp.Matrix:
    """Matrix of v -> uv from degree one to degree two."""
    r = len(coefficients)
    return sp.Matrix(
        [
            [
                coefficients[right] if column == left
                else coefficients[left] if column == right
                else 0
                for column in range(r)
            ]
            for left, right in combinations(range(r), 2)
        ]
    )


def assert_symbolic_annihilator_minors() -> dict[str, sp.Expr]:
    """Check the exact minors behind the degree-one annihilator lemma."""
    r = 7
    u = sp.symbols("u0:7", nonzero=True)

    one_support = multiplication_matrix([u[0], 0, 0, 0, 0, 0, 0])
    one_rows = [list(combinations(range(r), 2)).index((0, index))
                for index in range(1, r)]
    one_minor = sp.factor(one_support.extract(one_rows, range(1, r)).det())
    assert one_minor == u[0] ** (r - 1)

    two_support = multiplication_matrix([u[0], u[1], 0, 0, 0, 0, 0])
    two_minor = sp.factor(two_support.extract(one_rows, range(1, r)).det())
    assert two_minor == u[0] ** (r - 1)
    assert two_support * sp.Matrix([u[0], -u[1], 0, 0, 0, 0, 0]) == sp.zeros(
        comb(r, 2), 1
    )

    general = multiplication_matrix(list(u))
    pairs = list(combinations(range(r), 2))
    full_rows = [
        pairs.index((0, 1)),
        pairs.index((0, 2)),
        pairs.index((1, 2)),
        *(pairs.index((0, index)) for index in range(3, r)),
    ]
    full_minor = sp.factor(general.extract(full_rows, range(r)).det())
    assert full_minor == -2 * u[0] ** (r - 2) * u[1] * u[2]
    return {
        "support_1": one_minor,
        "support_2": two_minor,
        "support_at_least_3": full_minor,
    }


def exponent_triples(degree: int):
    """Yield all exponents of ternary monomials of fixed degree."""
    for first in range(degree + 1):
        for second in range(degree - first + 1):
            yield first, second, degree - first - second


def moment_sensor_rank(r: int) -> int:
    """Rank the moment-curve common-plane sensor over the integers."""
    degree = r - 2
    rows = masks_of_degree(r, degree)
    forms = [
        linear_form([1 for _ in range(r)]),
        linear_form([index for index in range(r)]),
        linear_form([index * index for index in range(r)]),
    ]
    columns: list[list[int]] = []
    for exponents in exponent_triples(degree):
        factors = [
            form
            for form, exponent in zip(forms, exponents, strict=True)
            for _ in range(exponent)
        ]
        value = product_of(factors)
        columns.append([value.get(mask, 0) for mask in rows])
    matrix = sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))
    return matrix.rank()


def assert_moment_curve_full_sensors() -> dict[int, int]:
    """Check properness charts through r=8."""
    ledger: dict[int, int] = {}
    for r in range(3, 9):
        rank = moment_sensor_rank(r)
        assert rank == comb(r, 2)
        ledger[r] = rank
    return ledger


def cyclic_block_planes() -> list[list[SquareFree]]:
    """Return the six local planes in the P6 two-block sharpness model."""
    planes: list[list[SquareFree]] = []
    for block_start in (0, 3):
        for mode_offset in range(3):
            planes.append(
                [
                    {1 << (block_start + (colour + mode_offset) % 3): 1}
                    for colour in range(3)
                ]
            )
    return planes


def tensor_coefficient(planes: list[list[SquareFree]], word: tuple[int, ...]) -> int:
    """Return the square-free top coefficient for one coordinate word."""
    top_mask = (1 << len(planes)) - 1
    value = product_of([planes[mode][colour] for mode, colour in enumerate(word)])
    return value.get(top_mask, 0)


def product_sensor_rank(
    planes: list[list[SquareFree]], selected_modes: tuple[int, ...]
) -> int:
    """Compute the exact product span of selected local planes."""
    r = len(planes)
    rows = masks_of_degree(r, len(selected_modes))
    columns = []
    for word in product(range(3), repeat=len(selected_modes)):
        value = product_of(
            [planes[mode][colour] for mode, colour in zip(selected_modes, word, strict=True)]
        )
        columns.append([value.get(mask, 0) for mask in rows])
    matrix = sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))
    return matrix.rank()


def assert_p6_block_boundary() -> dict[str, object]:
    """Check the exact P6 model showing rank drop alone is insufficient."""
    planes = cyclic_block_planes()
    words = list(product(range(3), repeat=6))
    coefficients = {word: tensor_coefficient(planes, word) for word in words}

    pure_values = [coefficients[(colour,) * 6] for colour in range(3)]
    assert pure_values == [1, 1, 1]
    nonzero_words = [word for word, value in coefficients.items() if value]
    assert len(nonzero_words) == 36
    assert sum(len(set(word)) > 1 for word in nonzero_words) == 33

    left_words = list(product(range(3), repeat=3))
    right_words = list(product(range(3), repeat=3))
    flattening = sp.Matrix(
        [
            [coefficients[left + right] for right in right_words]
            for left in left_words
        ]
    )
    assert flattening.rank() == 1

    sensor_ranks = {
        selected: product_sensor_rank(planes, selected)
        for selected in combinations(range(6), 4)
    }
    assert max(sensor_ranks.values()) == 9
    assert Counter(sensor_ranks.values()) == Counter({3: 6, 9: 9})

    omitted = (0, 3)
    complement = tuple(index for index in range(6) if index not in omitted)
    pair_rank = product_sensor_rank(planes, omitted)
    complement_rank = product_sensor_rank(planes, complement)
    assert pair_rank == complement_rank == 9
    assert pair_rank + complement_rank == comb(6, 2) + 3
    return {
        "pure_values": pure_values,
        "nonzero_words": len(nonzero_words),
        "mixed_nonzero_words": 33,
        "three_by_three_flattening_rank": 1,
        "four_mode_sensor_histogram": dict(sorted(Counter(sensor_ranks.values()).items())),
        "sharp_dimension_sum": pair_rank + complement_rank,
    }


def main() -> None:
    pairings = assert_perfect_complement_pairing()
    annihilators = assert_symbolic_annihilator_minors()
    moment = assert_moment_curve_full_sensors()
    p6 = assert_p6_block_boundary()
    print("arbitrary permanent co-two product-sensor primary checks: PASS")
    print(f"  perfect complement-pairing ranks: {pairings}")
    print(f"  symbolic annihilator minors: {annihilators}")
    print(f"  moment-curve full-sensor ranks: {moment}")
    print(f"  P6 block boundary: {p6}")


if __name__ == "__main__":
    main()
