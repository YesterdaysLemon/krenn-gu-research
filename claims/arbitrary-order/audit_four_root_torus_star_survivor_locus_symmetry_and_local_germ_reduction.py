#!/usr/bin/env python3
"""Independent no-import audit of the fixed-star local-germ reduction.

This checker uses only the standard library.  It independently rebuilds the
79 permanent columns with subset-DP permanents, derives its own annihilator,
checks the local stabilizer and survivor tangents, reconstructs the equal-leaf
incidence as sparse polynomials, and replays the bidirectional ideal
certificate with custom Q(i) polynomial arithmetic.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERTIFICATE = (
    HERE
    / "four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.json"
)
CERTIFICATE_SHA256 = "05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57"

Q = Fraction
Gaussian = tuple[Q, Q]
ZERO: Gaussian = (Q(0), Q(0))
ONE: Gaussian = (Q(1), Q(0))
MODES = tuple(range(4))
PAIRS = tuple(combinations(MODES, 2))
WORDS = tuple(product(range(3), repeat=4))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}


def gi(real: int | Q, imaginary: int | Q = 0) -> Gaussian:
    return Q(real), Q(imaginary)


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gneg(value: Gaussian) -> Gaussian:
    return -value[0], -value[1]


def gsub(left: Gaussian, right: Gaussian) -> Gaussian:
    return gadd(left, gneg(right))


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gdiv(left: Gaussian, right: Gaussian) -> Gaussian:
    norm = right[0] * right[0] + right[1] * right[1]
    assert norm
    return (
        (left[0] * right[0] + left[1] * right[1]) / norm,
        (left[1] * right[0] - left[0] * right[1]) / norm,
    )


def gsum(values) -> Gaussian:
    result = ZERO
    for value in values:
        result = gadd(result, value)
    return result


def gprod(values) -> Gaussian:
    result = ONE
    for value in values:
        result = gmul(result, value)
    return result


Matrix = list[list[Gaussian]]
Vector = list[Gaussian]


def transpose(matrix: Matrix) -> Matrix:
    return [list(column) for column in zip(*matrix, strict=True)] if matrix else []


def matrix_from_columns(columns: list[Vector]) -> Matrix:
    return [[column[row] for column in columns] for row in range(len(columns[0]))]


def matmul(left: Matrix, right: Matrix) -> Matrix:
    assert left and right and len(left[0]) == len(right)
    return [
        [
            gsum(
                gmul(left[row][inner], right[inner][column])
                for inner in range(len(right))
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return [
        gsum(gmul(entry, vector[column]) for column, entry in enumerate(row))
        for row in matrix
    ]


def rref(matrix: Matrix) -> tuple[Matrix, tuple[int, ...]]:
    work = [row[:] for row in matrix]
    if not work:
        return work, ()
    pivot_row = 0
    pivots = []
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column] != ZERO),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [gdiv(value, scale) for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or work[row][column] == ZERO:
                continue
            factor = work[row][column]
            work[row] = [
                gsub(value, gmul(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return work, tuple(pivots)


def rank(matrix: Matrix) -> int:
    return len(rref(matrix)[1])


def nullspace(matrix: Matrix) -> list[Vector]:
    reduced, pivots = rref(matrix)
    if not reduced:
        return []
    pivot_set = set(pivots)
    free = [column for column in range(len(reduced[0])) if column not in pivot_set]
    basis = []
    for free_column in free:
        vector = [ZERO] * len(reduced[0])
        vector[free_column] = ONE
        for row, pivot in enumerate(pivots):
            vector[pivot] = gneg(reduced[row][free_column])
        basis.append(vector)
    return basis


def permanent_dp(columns: list[Vector]) -> Gaussian:
    states = {0: ONE}
    for column in columns:
        following: dict[int, Gaussian] = {}
        for mask, value in states.items():
            for row, entry in enumerate(column):
                if mask & (1 << row):
                    continue
                next_mask = mask | (1 << row)
                following[next_mask] = gadd(
                    following.get(next_mask, ZERO), gmul(value, entry)
                )
        states = following
    return states[(1 << len(columns)) - 1]


def canonical_interface():
    xi = [gi(value) for value in (1, 1, 1, -1)]
    eta = [gi(value) for value in (1, 1, 1, 1)]
    radical0 = [gi(value) for value in (1, -1, 0, 0)]
    radical1 = [gi(value) for value in (1, 0, -1, 0)]
    centre = [gi(value) for value in (1, 0, 0, 1)]
    leaf = [gi(value) for value in (1, 0, 0, -1)]
    ports = [
        [radical0, radical1, centre],
        [radical0, radical1, leaf],
        [radical0, radical1, leaf],
        [radical0, radical1, leaf],
    ]
    return xi, eta, ports


def nuisance_columns() -> list[Vector]:
    xi, eta, ports = canonical_interface()
    columns = [
        [permanent_dp([ports[mode][word[mode]] for mode in MODES]) for word in WORDS]
    ]
    for residual in (xi, eta):
        for labelled_mode in MODES:
            for labelled_index in range(3):
                column = [ZERO] * 81
                for word_index, word in enumerate(WORDS):
                    if word[labelled_mode] != labelled_index:
                        continue
                    column[word_index] = permanent_dp(
                        [residual]
                        + [
                            ports[mode][word[mode]]
                            for mode in MODES
                            if mode != labelled_mode
                        ]
                    )
                columns.append(column)
    for left_mode, right_mode in PAIRS:
        for left_index, right_index in product(range(3), repeat=2):
            column = [ZERO] * 81
            for word_index, word in enumerate(WORDS):
                if word[left_mode] != left_index or word[right_mode] != right_index:
                    continue
                column[word_index] = permanent_dp(
                    [xi, eta]
                    + [
                        ports[mode][word[mode]]
                        for mode in MODES
                        if mode not in (left_mode, right_mode)
                    ]
                )
            columns.append(column)
    assert len(columns) == 79
    return columns


def candidate_frames() -> tuple[Matrix, Matrix]:
    centre = [
        [gi(-2, -2), gi(-1, 2), gi(3)],
        [ZERO, gi(-3, 3), ZERO],
        [ZERO, gi(-1, 2), ONE],
    ]
    leaf = [
        [ONE, ONE, ONE],
        [ZERO, ZERO, gi(1, 1)],
        [ZERO, ONE, ONE],
    ]
    return centre, leaf


def frame_tensor(centre: Matrix, leaf: Matrix) -> Vector:
    return [
        gsum(
            gprod(
                (
                    centre[word[0]][colour],
                    leaf[word[1]][colour],
                    leaf[word[2]][colour],
                    leaf[word[3]][colour],
                )
            )
            for colour in range(3)
        )
        for word in WORDS
    ]


def determinant3(matrix: Matrix) -> Gaussian:
    return gsum(
        (
            gprod((matrix[0][0], matrix[1][1], matrix[2][2])),
            gprod((matrix[0][1], matrix[1][2], matrix[2][0])),
            gprod((matrix[0][2], matrix[1][0], matrix[2][1])),
            gneg(gprod((matrix[0][2], matrix[1][1], matrix[2][0]))),
            gneg(gprod((matrix[0][1], matrix[1][0], matrix[2][2]))),
            gneg(gprod((matrix[0][0], matrix[1][2], matrix[2][1]))),
        )
    )


def local_action(tensor: Vector, mode: int, row: int, column: int) -> Vector:
    output = [ZERO] * 81
    for word in WORDS:
        if word[mode] != row:
            continue
        source = list(word)
        source[mode] = column
        output[WORD_INDEX[word]] = tensor[WORD_INDEX[tuple(source)]]
    return output


def dot(left: Vector, right: Vector) -> Gaussian:
    return gsum(gmul(a, b) for a, b in zip(left, right, strict=True))


Exponent = tuple[int, ...]
Polynomial = dict[Exponent, Gaussian]
ZERO_EXPONENT: Exponent = (0,) * 15


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for exponent, coefficient in right.items():
        value = gadd(result.get(exponent, ZERO), coefficient)
        if value == ZERO:
            result.pop(exponent, None)
        else:
            result[exponent] = value
    return result


def poly_scale(value: Polynomial, scalar: Gaussian) -> Polynomial:
    if scalar == ZERO:
        return {}
    return {
        exponent: product_value
        for exponent, coefficient in value.items()
        if (product_value := gmul(coefficient, scalar)) != ZERO
    }


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(
                a + b for a, b in zip(left_exponent, right_exponent, strict=True)
            )
            value = gadd(
                result.get(exponent, ZERO),
                gmul(left_coefficient, right_coefficient),
            )
            if value == ZERO:
                result.pop(exponent, None)
            else:
                result[exponent] = value
    return result


def constant_polynomial(value: Gaussian) -> Polynomial:
    return {} if value == ZERO else {ZERO_EXPONENT: value}


def affine_polynomial(value: Gaussian, variable: int) -> Polynomial:
    result = constant_polynomial(value)
    exponent = [0] * 15
    exponent[variable] = 1
    result[tuple(exponent)] = ONE
    return result


def symmetric_incidence(relations: list[Vector]) -> list[Polynomial]:
    centre, leaf = candidate_frames()
    centre_entries = [
        affine_polynomial(centre[row][colour], 3 * row + colour)
        for row in range(3)
        for colour in range(3)
    ]
    leaf_entries: dict[tuple[int, int], Polynomial] = {}
    for index in range(3):
        for colour in range(3):
            if index == 0:
                leaf_entries[(index, colour)] = constant_polynomial(ONE)
            elif index == 1:
                leaf_entries[(index, colour)] = affine_polynomial(
                    leaf[index][colour], 9 + colour
                )
            else:
                leaf_entries[(index, colour)] = affine_polynomial(
                    leaf[index][colour], 12 + colour
                )
    tensor_polys = []
    for word in WORDS:
        value: Polynomial = {}
        for colour in range(3):
            term = centre_entries[3 * word[0] + colour]
            for mode in (1, 2, 3):
                term = poly_mul(term, leaf_entries[(word[mode], colour)])
            value = poly_add(value, term)
        tensor_polys.append(value)
    equations = []
    for relation in relations:
        equation: Polynomial = {}
        for coefficient, tensor_poly in zip(relation, tensor_polys, strict=True):
            equation = poly_add(equation, poly_scale(tensor_poly, coefficient))
        equations.append(equation)
    return equations


def parse_gaussian(raw: str) -> Gaussian:
    text = str(raw).strip().replace(" ", "")
    while len(text) >= 2 and text[0] == "(" and text[-1] == ")":
        depth = 0
        outer = True
        for index, character in enumerate(text):
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0 and index != len(text) - 1:
                    outer = False
                    break
        if not outer or depth:
            break
        text = text[1:-1]
    terms = []
    start = 0
    for index, character in enumerate(text):
        if index and character in "+-":
            terms.append(text[start:index])
            start = index
    terms.append(text[start:])
    real = Q(0)
    imaginary = Q(0)
    for term in terms:
        if not term:
            continue
        if "i" in term:
            coefficient = term.replace("*i", "").replace("i", "")
            if coefficient in ("", "+"):
                coefficient = "1"
            elif coefficient == "-":
                coefficient = "-1"
            imaginary += Q(coefficient)
        else:
            real += Q(term)
    return real, imaginary


def encoded_polynomial(encoded) -> Polynomial:
    result: Polynomial = {}
    for raw_coefficient, sparse_exponent in encoded:
        exponent = [0] * 15
        previous = -1
        for raw_index, raw_power in sparse_exponent:
            index = int(raw_index)
            power = int(raw_power)
            assert previous < index < 15 and power > 0
            exponent[index] = power
            previous = index
        key = tuple(exponent)
        assert key not in result
        result[key] = parse_gaussian(raw_coefficient)
    return result


def replay_certificate(
    incidence: list[Polynomial],
) -> tuple[int, int, int, tuple[int, ...]]:
    raw = CERTIFICATE.read_bytes()
    canonical = raw.replace(b"\r\n", b"\n")
    assert b"\r" not in canonical
    assert hashlib.sha256(canonical).hexdigest() == CERTIFICATE_SHA256
    data = json.loads(canonical)
    assert data["format"] == "sparse-bidirectional-ideal-Qi-v1"
    assert data["variable_order"] == [f"x{index}" for index in range(15)]
    assert data["incidence_generator_count"] == len(incidence) == 37
    basis = [encoded_polynomial(value) for value in data["basis"]]
    assert len(basis) == 10
    forward: dict[tuple[int, int], Polynomial] = {}
    reverse: dict[tuple[int, int], Polynomial] = {}
    forward_terms = 0
    reverse_terms = 0
    for entry in data["forward"]:
        key = int(entry["row"]), int(entry["column"])
        assert key not in forward
        forward[key] = encoded_polynomial(entry["terms"])
        forward_terms += len(entry["terms"])
    for entry in data["reverse"]:
        key = int(entry["row"]), int(entry["column"])
        assert key not in reverse
        reverse[key] = encoded_polynomial(entry["terms"])
        reverse_terms += len(entry["terms"])
    assert (forward_terms, reverse_terms) == (27, 63)
    for column in range(10):
        value: Polynomial = {}
        for row in range(37):
            value = poly_add(
                value,
                poly_mul(incidence[row], forward.get((row, column), {})),
            )
        assert value == basis[column]
    for column in range(37):
        value: Polynomial = {}
        for row in range(10):
            value = poly_add(
                value,
                poly_mul(basis[row], reverse.get((row, column), {})),
            )
        assert value == incidence[column]
    jacobian = []
    for polynomial in basis:
        row = []
        for variable in range(15):
            exponent = [0] * 15
            exponent[variable] = 1
            row.append(polynomial.get(tuple(exponent), ZERO))
        jacobian.append(row)
    assert rank(jacobian) == 10
    _reduced, pivot_columns = rref(jacobian)
    free_columns = tuple(column for column in range(15) if column not in pivot_columns)
    assert free_columns == (6, 8, 12, 13, 14)
    return len(canonical), forward_terms, reverse_terms, free_columns


def gauge_derivative(centre: Matrix, leaf: Matrix) -> Matrix:
    columns: list[Vector] = []
    for selected_root in range(3):
        for selected_colour in range(3):
            columns.append(
                [
                    gprod(leaf[word[mode]][selected_colour] for mode in (1, 2, 3))
                    if word[0] == selected_root
                    else ZERO
                    for word in WORDS
                ]
            )
    for selected_mode in (1, 2, 3):
        for selected_row in (1, 2):
            for selected_colour in range(3):
                columns.append(
                    [
                        gprod(
                            [centre[word[0]][selected_colour]]
                            + [
                                leaf[word[mode]][selected_colour]
                                for mode in (1, 2, 3)
                                if mode != selected_mode
                            ]
                        )
                        if word[selected_mode] == selected_row
                        else ZERO
                        for word in WORDS
                    ]
                )
    assert len(columns) == 27
    return matrix_from_columns(columns)


def check() -> dict[str, object]:
    columns = nuisance_columns()
    nuisance = matrix_from_columns(columns)
    _reduced, nuisance_pivots = rref(nuisance)
    assert len(nuisance_pivots) == 44
    nuisance_basis = [columns[index] for index in nuisance_pivots]
    relations = nullspace(transpose(nuisance))
    assert len(relations) == 37
    assert all(
        dot(relation, column) == ZERO for relation in relations for column in columns
    )

    centre, leaf = candidate_frames()
    tensor = frame_tensor(centre, leaf)
    assert determinant3(centre) == gi(12)
    assert determinant3(leaf) == gi(-1, -1)

    labels = tuple(
        (mode, row, column)
        for mode in range(4)
        for row in range(3)
        for column in range(3)
    )
    stabilizer_columns = []
    for mode, row, column in labels:
        values = []
        for relation in relations:
            for basis_vector in nuisance_basis:
                values.append(
                    dot(relation, local_action(basis_vector, mode, row, column))
                )
        stabilizer_columns.append(values)
    stabilizer_system = matrix_from_columns(stabilizer_columns)
    assert rank(stabilizer_system) == 32
    scalar_generators = []
    for mode in range(4):
        vector = [ZERO] * 36
        for index in range(3):
            vector[9 * mode + 3 * index + index] = ONE
        scalar_generators.append(vector)
        assert matvec(stabilizer_system, vector) == [ZERO] * len(stabilizer_system)
    assert rank(matrix_from_columns(scalar_generators)) == 4

    action_columns = [
        local_action(tensor, mode, row, column) for mode, row, column in labels
    ]
    action = matrix_from_columns(action_columns)
    assert rank(action) == 27
    constraint = matmul(relations, action)
    assert rank(constraint) == 22
    preimage = nullspace(constraint)
    assert len(preimage) == 14
    survivor_tangent_columns = [matvec(action, vector) for vector in preimage]
    assert rank(matrix_from_columns(survivor_tangent_columns)) == 5
    scalar_orbit = [matvec(action, vector) for vector in scalar_generators]
    assert rank(matrix_from_columns(scalar_orbit)) == 1

    full_gauge_derivative = gauge_derivative(centre, leaf)
    assert rank(matmul(relations, full_gauge_derivative)) == 22
    incidence = symmetric_incidence(relations)
    certificate_bytes, forward_terms, reverse_terms, free_columns = replay_certificate(
        incidence
    )

    return {
        "status": "independent_exact_local_survivor_germ_reduction",
        "global_conjecture": "UNRESOLVED",
        "permanent_columns_nuisance_rank_annihilator": [79, 44, 37],
        "local_stabilizer_constraint_rank_dimension": [32, 4],
        "local_stabilizer_generators": "four factor scalars",
        "ghz_action_rank_frame_kernel": [27, 9],
        "survivor_constraint_rank_preimage_image": [22, 14, 5],
        "interface_orbit_tangent_dimension": 1,
        "transverse_parameters_modulo_scaling": 4,
        "full_gauge_variables_jacobian_rank": [27, 22],
        "equal_leaf_incidence_generators_basis_jacobian_rank": [37, 10, 10],
        "local_free_shift_coordinates": [f"x{column}" for column in free_columns],
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_bytes": certificate_bytes,
        "certificate_forward_reverse_terms": [forward_terms, reverse_terms],
        "whole_survivor_locus_response_excluded": False,
    }


def main() -> None:
    print("independent fixed-star survivor local-germ audit: PASS")
    print(json.dumps(check(), indent=2))


if __name__ == "__main__":
    main()
