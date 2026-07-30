#!/usr/bin/env python3
"""Independent exact combinatorial audit of the q5_221 star obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_STAR_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(poly):
    return {
        monomial: coefficient
        for monomial, coefficient in poly.items()
        if coefficient
    }


def constant(value: int):
    return {} if value == 0 else {(): value}


def variable(name: str):
    return {(name,): 1}


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return clean(result)


def scale(coefficient: int, polynomial):
    return clean(
        {
            monomial: coefficient * value
            for monomial, value in polynomial.items()
        }
    )


def multiply(*polynomials):
    result = constant(1)
    for polynomial in polynomials:
        product = {}
        for left_monomial, left_coefficient in result.items():
            for right_monomial, right_coefficient in polynomial.items():
                monomial = tuple(
                    sorted(left_monomial + right_monomial)
                )
                product[monomial] = (
                    product.get(monomial, 0)
                    + left_coefficient * right_coefficient
                )
        result = clean(product)
    return result


def parity(permutation) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def determinant(matrix):
    size = len(matrix)
    result = {}
    for permutation in itertools.permutations(range(size)):
        term = multiply(
            *(
                matrix[row][permutation[row]]
                for row in range(size)
            )
        )
        result = add(result, scale(parity(permutation), term))
    return result


def cofactor(matrix, row: int, column: int):
    minor = [
        [
            value
            for column_index, value in enumerate(source_row)
            if column_index != column
        ]
        for row_index, source_row in enumerate(matrix)
        if row_index != row
    ]
    return scale((-1) ** (row + column), determinant(minor))


def vector_add(*vectors):
    return tuple(
        add(*(vector[index] for vector in vectors))
        for index in range(len(vectors[0]))
    )


def vector_scale(polynomial, vector):
    return tuple(multiply(polynomial, coordinate) for coordinate in vector)


def tensor_coefficients(maps):
    order = len(maps)
    result = {}
    for target_index in itertools.product(range(3), repeat=order):
        coefficient = {}
        for permutation in itertools.permutations(range(order)):
            coefficient = add(
                coefficient,
                multiply(
                    *(
                        maps[mode][target_index[mode]][source_index]
                        for mode, source_index in enumerate(permutation)
                    )
                ),
            )
        if coefficient:
            result[target_index] = coefficient
    return result


def format_polynomial(poly) -> str:
    if not poly:
        return "0"
    pieces = []
    for monomial, coefficient in sorted(poly.items()):
        factor = "*".join(monomial)
        if factor:
            pieces.append(f"{coefficient}*{factor}")
        else:
            pieces.append(str(coefficient))
    return " + ".join(pieces)


def main() -> None:
    zero = constant(0)
    one = constant(1)
    minus_one = constant(-1)
    names = ("q10", "q20", "q01", "q21", "q02", "q12")
    q10, q20, q01, q21, q02, q12 = map(variable, names)
    cross_matrix = (
        (zero, q10, q20),
        (q01, zero, q21),
        (q02, q12, zero),
    )
    cross_determinant = determinant(cross_matrix)
    expected_determinant = add(
        multiply(q10, q21, q02),
        multiply(q20, q01, q12),
    )
    assert cross_determinant == expected_determinant
    central_h1_numerator = cofactor(cross_matrix, 1, 0)
    assert central_h1_numerator == multiply(q20, q12)

    # Independent exact expansion of the Q_12 sign chart.
    zero3 = (zero, zero, zero)
    u0_3 = (one, one, zero)
    h0_3 = (one, minus_one, zero)
    third = (zero, zero, one)
    q12_maps = (
        (zero3, third, h0_3),
        (third, u0_3, third),
        (zero3, u0_3, third),
    )
    q12_coefficients = tensor_coefficients(q12_maps)
    assert q12_coefficients == {(1, 1, 1): constant(2)}

    # Independent polynomial expansion of the rank-one Q_20 chart.
    ell = variable("ell")
    plane_a = variable("plane_a")
    plane_b = variable("plane_b")
    h0_20 = (one, zero, zero)
    u1_20 = (zero, one, one)
    h1_20 = (zero, one, minus_one)
    q20_maps = (
        (h1_20, u1_20, h0_20),
        (
            vector_add(h1_20, vector_scale(ell, u1_20)),
            zero3,
            vector_add(
                vector_scale(plane_a, h1_20),
                vector_scale(plane_b, u1_20),
            ),
        ),
        (
            zero3,
            zero3,
            vector_add(u1_20, vector_scale(ell, h1_20)),
        ),
    )
    q20_coefficients = tensor_coefficients(q20_maps)
    expected_q20 = add(
        scale(-2, multiply(plane_a, ell)),
        scale(2, plane_b),
    )
    assert q20_coefficients == {(2, 2, 2): expected_q20}

    # The decisive T2 coefficient is audited without dividing by det M:
    # gamma denotes the nonzero h1 numerator q20*q12 at the centre.
    leaf0_scale = variable("leaf0")
    leaf1_scale = variable("leaf1")
    leaf2_scale = variable("leaf2")
    central_h0 = variable("central_h0")
    central_h1 = variable("central_h1")
    h0_4 = (one, minus_one, zero, zero)
    u0_4 = (one, one, zero, zero)
    u1_4 = (zero, zero, one, one)
    h1_4 = (zero, zero, one, minus_one)
    shear_scale = variable("shear")
    shear_h1 = variable("shear_h1")
    shear_u1 = variable("shear_u1")
    leaf1_row = vector_add(
        vector_scale(leaf1_scale, u0_4),
        vector_scale(
            shear_scale,
            vector_add(
                vector_scale(shear_h1, h1_4),
                vector_scale(shear_u1, u1_4),
            ),
        ),
    )
    selected_rows = (
        vector_scale(leaf0_scale, h1_4),
        leaf1_row,
        vector_scale(leaf2_scale, u0_4),
        vector_add(
            vector_scale(central_h0, h0_4),
            vector_scale(central_h1, h1_4),
        ),
    )
    forbidden_coefficient = {}
    for permutation in itertools.permutations(range(4)):
        forbidden_coefficient = add(
            forbidden_coefficient,
            multiply(
                *(
                    selected_rows[mode][source_index]
                    for mode, source_index in enumerate(permutation)
                )
            ),
        )
    expected_forbidden = scale(
        -4,
        multiply(
            leaf0_scale,
            leaf1_scale,
            leaf2_scale,
            central_h1,
        ),
    )
    assert forbidden_coefficient == expected_forbidden

    output = {
        "audited": True,
        "method": "independent exact polynomial permutation expansion",
        "central_zero_diagonal_determinant": format_polynomial(
            cross_determinant
        ),
        "central_h1_cofactor_numerator": format_polynomial(
            central_h1_numerator
        ),
        "Q12_nonzero_coefficients": {
            str(key): format_polynomial(value)
            for key, value in q12_coefficients.items()
        },
        "Q20_nonzero_coefficients": {
            str(key): format_polynomial(value)
            for key, value in q20_coefficients.items()
        },
        "forced_forbidden_T2_coefficient": format_polynomial(
            forbidden_coefficient
        ),
        "leaf1_shear_cancels": all(
            not any(name.startswith("shear") for name in monomial)
            for monomial in forbidden_coefficient
        ),
        "exact_star_excluded": True,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_star_obstruction_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
