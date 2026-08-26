#!/usr/bin/env python3
"""Independent no-import audit of the GLD74 full-fibre q0 obstruction.

This checker deliberately uses only the standard library.  It rebuilds the
literal-Delta 81-by-79 permanent map, solves its 35-dimensional Gaussian
fibre, derives the q0 response quotient by a reversed fibre-variable order,
replays the sparse Q(i) unit certificates with custom polynomial arithmetic,
and independently checks the three-point rank-one locus on the raw sign
plane.  It does not import the primary verifier or any repository module.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE_PATH = HERE / (
    "four_root_torus_star_gaussian_survivor_full_coefficient_fibre_"
    "first_response_nonextension_certificates.json"
)
CERTIFICATE_SHA256 = "7bb2dc47270a2c2e9b87c722aace298e63a6691a7979d86564425aac760a748f"

Q = Fraction
Gaussian = tuple[Fraction, Fraction]
ZERO: Gaussian = (Q(0), Q(0))
ONE: Gaussian = (Q(1), Q(0))
MODES = tuple(range(4))
PAIRS = tuple(combinations(MODES, 2))
LOCAL_INDICES = tuple(product(range(3), repeat=4))
LOCAL_INDEX = {word: index for index, word in enumerate(LOCAL_INDICES)}
PERMUTATIONS_3 = tuple(permutations(range(3)))
PERMUTATIONS_4 = tuple(permutations(range(4)))

# The certificate is stored in t0,...,t34,a,b order.  This audit uses the
# complete reverse order b,a,t34,...,t0 for both fibre variables and chart
# variables, and reverses certificate exponents before multiplication.
ORIGINAL_VARIABLES = tuple([f"t{index}" for index in range(35)] + ["a", "b"])
REVERSED_VARIABLES = tuple(["b", "a"] + [f"t{index}" for index in range(34, -1, -1)])
assert len(ORIGINAL_VARIABLES) == len(REVERSED_VARIABLES) == 37
assert REVERSED_VARIABLES == tuple(reversed(ORIGINAL_VARIABLES))


def gi(real: int | Fraction, imaginary: int | Fraction = 0) -> Gaussian:
    return Q(real), Q(imaginary)


PROJECTIVE_ESCAPE_WITNESSES = (
    (
        -1,
        1,
        {13: gi(-1), 15: gi(1), 22: gi(1), 24: gi(-1), 31: gi(-1), 33: gi(1)},
    ),
    (
        1,
        -1,
        {
            9: gi(0, -1),
            10: gi(-1),
            11: gi(0, 1),
            14: gi(1),
            18: gi(0, 1),
            19: gi(1),
            20: gi(0, -1),
            23: gi(-1),
            27: gi(0, -1),
            28: gi(-1),
            29: gi(0, 1),
            32: gi(1),
        },
    ),
    (
        -1,
        -1,
        {
            9: gi(1),
            10: gi(-1),
            11: gi(-1),
            14: gi(1),
            18: gi(-1),
            19: gi(1),
            20: gi(1),
            23: gi(-1),
            27: gi(1),
            28: gi(-1),
            29: gi(-1),
            32: gi(1),
        },
    ),
)

SIGN_FIBRE_BASIS = (
    {
        9: gi(Q(1, 6)),
        11: gi(Q(-1, 6)),
        18: gi(Q(-1, 6)),
        20: gi(Q(1, 6)),
        27: gi(Q(1, 6)),
        29: gi(Q(-1, 6)),
    },
    {
        10: gi(Q(1, 6)),
        14: gi(Q(-1, 6)),
        19: gi(Q(-1, 6)),
        23: gi(Q(1, 6)),
        28: gi(Q(1, 6)),
        32: gi(Q(-1, 6)),
    },
    {
        13: gi(Q(1, 6)),
        15: gi(Q(-1, 6)),
        22: gi(Q(-1, 6)),
        24: gi(Q(1, 6)),
        31: gi(Q(1, 6)),
        33: gi(Q(-1, 6)),
    },
)


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
    assert norm != 0
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


def raw_descriptors():
    descriptors = [("q",)]
    descriptors.extend(
        ("residual", residual, mode, colour)
        for residual in range(2)
        for mode in range(4)
        for colour in range(3)
    )
    descriptors.extend(
        ("pair", modes, colours)
        for modes in combinations(range(4), 2)
        for colours in product(range(3), repeat=2)
    )
    assert len(descriptors) == 79
    return tuple(descriptors)


def permute_raw_descriptor(descriptor, mode_permutation):
    if descriptor[0] == "q":
        return descriptor
    if descriptor[0] == "residual":
        _tag, residual, mode, colour = descriptor
        return "residual", residual, mode_permutation[mode], colour
    _tag, modes, colours = descriptor
    transported = sorted(
        zip(
            (mode_permutation[modes[0]], mode_permutation[modes[1]]),
            colours,
            strict=True,
        )
    )
    return (
        "pair",
        tuple(mode for mode, _colour in transported),
        tuple(colour for _mode, colour in transported),
    )


def permute_raw_vector(vector, mode_permutation):
    descriptors = raw_descriptors()
    index = {descriptor: position for position, descriptor in enumerate(descriptors)}
    # This is the transpose/contragredient convention used by the raw
    # coefficient columns.  Sign eigenvectors have the same eigenvalue under
    # the inverse action, but the orientation is retained explicitly here.
    return [
        vector[index[permute_raw_descriptor(descriptor, mode_permutation)]]
        for descriptor in descriptors
    ]


def matrix_transpose(matrix: list[list[Gaussian]]) -> list[list[Gaussian]]:
    return [list(column) for column in zip(*matrix)]


def matrix_multiply(
    left: list[list[Gaussian]], right: list[list[Gaussian]]
) -> list[list[Gaussian]]:
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


def matrix_vector(
    matrix: list[list[Gaussian]], vector: list[Gaussian]
) -> list[Gaussian]:
    return [
        gsum(gmul(value, vector[column]) for column, value in enumerate(row))
        for row in matrix
    ]


def matrix_inverse(matrix: list[list[Gaussian]]) -> list[list[Gaussian]]:
    size = len(matrix)
    work = [
        row_values[:] + [ONE if row == column else ZERO for column in range(size)]
        for row, row_values in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column] != ZERO),
            None,
        )
        assert pivot is not None
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [gdiv(value, scale) for value in work[column]]
        for row in range(size):
            if row == column or work[row][column] == ZERO:
                continue
            factor = work[row][column]
            work[row] = [
                gsub(value, gmul(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[column], strict=True)
            ]
    return [row[size:] for row in work]


def rank(matrix: list[list[Gaussian]]) -> int:
    if not matrix:
        return 0
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column] != ZERO),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [gdiv(value, scale) for value in work[pivot_row]]
        for row in range(pivot_row + 1, rows):
            if row == pivot_row or work[row][column] == ZERO:
                continue
            factor = work[row][column]
            work[row] = [
                gsub(value, gmul(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def determinant(matrix: list[list[Gaussian]]) -> Gaussian:
    assert matrix and len(matrix) == len(matrix[0])
    work = [row[:] for row in matrix]
    result = ONE
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column] != ZERO),
            None,
        )
        if pivot is None:
            return ZERO
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = gneg(result)
        scale = work[column][column]
        result = gmul(result, scale)
        for row in range(column + 1, len(work)):
            if work[row][column] == ZERO:
                continue
            factor = gdiv(work[row][column], scale)
            work[row] = [
                gsub(value, gmul(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[column], strict=True)
            ]
    return result


def pivot_columns(matrix: list[list[Gaussian]]) -> tuple[int, ...]:
    if not matrix:
        return ()
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    pivots = []
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column] != ZERO),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [gdiv(value, scale) for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or work[row][column] == ZERO:
                continue
            factor = work[row][column]
            work[row] = [
                gsub(value, gmul(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return tuple(pivots)


def affine_fibre(
    columns: list[list[Gaussian]], target: list[Gaussian]
) -> tuple[list[Gaussian], list[list[Gaussian]], tuple[int, ...], tuple[int, ...]]:
    """Exact RREF solve with free columns in ascending order."""

    row_count = len(target)
    column_count = len(columns)
    work = [
        [columns[column][row] for column in range(column_count)] + [target[row]]
        for row in range(row_count)
    ]
    pivot_row = 0
    pivots = []
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column] != ZERO),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [gdiv(value, scale) for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or work[row][column] == ZERO:
                continue
            factor = work[row][column]
            work[row] = [
                gsub(value, gmul(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
    assert all(work[row][-1] == ZERO for row in range(pivot_row, row_count))
    pivot_set = set(pivots)
    free = tuple(column for column in range(column_count) if column not in pivot_set)
    particular = [ZERO] * column_count
    for row, pivot in enumerate(pivots):
        particular[pivot] = work[row][-1]
    kernels = []
    for free_column in free:
        vector = [ZERO] * column_count
        vector[free_column] = ONE
        for row, pivot in enumerate(pivots):
            vector[pivot] = gneg(work[row][free_column])
        kernels.append(vector)
    return particular, kernels, tuple(pivots), free


def vector(*entries: int) -> list[Gaussian]:
    return [gi(entry) for entry in entries]


def permutation_sign(sigma: tuple[int, ...]) -> int:
    inversions = sum(
        sigma[left] > sigma[right]
        for left in range(len(sigma))
        for right in range(left + 1, len(sigma))
    )
    return -1 if inversions % 2 else 1


def permanent4(columns: list[list[Gaussian]]) -> Gaussian:
    assert len(columns) == 4
    return gsum(
        gprod(columns[mode][sigma[mode]] for mode in MODES) for sigma in PERMUTATIONS_4
    )


def determinant3(matrix: list[list[Gaussian]]) -> Gaussian:
    return gsum(
        gmul(
            gi(permutation_sign(sigma)),
            gprod(matrix[row][sigma[row]] for row in range(3)),
        )
        for sigma in PERMUTATIONS_3
    )


def canonical_torus_star():
    xi = vector(1, 1, 1, -1)
    eta = vector(1, 1, 1, 1)
    radical0 = vector(1, -1, 0, 0)
    radical1 = vector(1, 0, -1, 0)
    centre = vector(1, 0, 0, 1)
    leaf = vector(1, 0, 0, -1)
    ports = [
        [radical0, radical1, centre],
        [radical0, radical1, leaf],
        [radical0, radical1, leaf],
        [radical0, radical1, leaf],
    ]
    return xi, eta, ports


def build_q_layer_columns(
    xi: list[Gaussian],
    eta: list[Gaussian],
    ports: list[list[list[Gaussian]]],
) -> list[list[Gaussian]]:
    columns = [
        [
            permanent4([ports[mode][word[mode]] for mode in MODES])
            for word in LOCAL_INDICES
        ]
    ]
    for residual in (xi, eta):
        for labelled_mode in MODES:
            for labelled_index in range(3):
                column = [ZERO] * len(LOCAL_INDICES)
                for row, word in enumerate(LOCAL_INDICES):
                    if word[labelled_mode] != labelled_index:
                        continue
                    companion = [
                        residual,
                        *[
                            ports[mode][word[mode]]
                            for mode in MODES
                            if mode != labelled_mode
                        ],
                    ]
                    column[row] = permanent4(companion)
                columns.append(column)
    for left_mode, right_mode in PAIRS:
        for left_index, right_index in product(range(3), repeat=2):
            column = [ZERO] * len(LOCAL_INDICES)
            for row, word in enumerate(LOCAL_INDICES):
                if word[left_mode] != left_index or word[right_mode] != right_index:
                    continue
                companions = [
                    xi,
                    eta,
                    *[
                        ports[mode][word[mode]]
                        for mode in MODES
                        if mode not in (left_mode, right_mode)
                    ],
                ]
                column[row] = permanent4(companions)
            columns.append(column)
    assert len(columns) == 79
    return columns


def matrix_from_columns(columns: list[list[Gaussian]]) -> list[list[Gaussian]]:
    return [[column[row] for column in columns] for row in range(len(columns[0]))]


def frame_tensor(
    centre: list[list[Gaussian]], leaf: list[list[Gaussian]]
) -> list[Gaussian]:
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
        for word in LOCAL_INDICES
    ]


def act_on_tensor(
    tensor: list[Gaussian],
    maps: tuple[list[list[Gaussian]], ...],
) -> list[Gaussian]:
    return [
        gsum(
            gprod(
                [maps[mode][output[mode]][source[mode]] for mode in MODES]
                + [tensor[LOCAL_INDEX[source]]]
            )
            for source in LOCAL_INDICES
        )
        for output in LOCAL_INDICES
    ]


def transform_ports(
    ports: list[list[list[Gaussian]]],
    inverse_frames: tuple[list[list[Gaussian]], ...],
) -> list[list[list[Gaussian]]]:
    transformed = []
    for port, inverse in zip(ports, inverse_frames, strict=True):
        matrix = [[port[column][row] for column in range(3)] for row in range(4)]
        new_matrix = matrix_multiply(matrix, matrix_transpose(inverse))
        transformed.append(
            [[new_matrix[row][column] for row in range(3 + 1)] for column in range(3)]
        )
    return transformed


def target_delta() -> list[Gaussian]:
    return [
        ONE if word[0] == word[1] == word[2] == word[3] else ZERO
        for word in LOCAL_INDICES
    ]


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for offset in range(1, len(vertices)):
        second = vertices[offset]
        remainder = vertices[1:offset] + vertices[offset + 1 :]
        for matching in perfect_matchings(remainder):
            yield ((first, second),) + matching


def q0_response_maps(
    xi: list[Gaussian],
    eta: list[Gaussian],
    transformed_ports: list[list[list[Gaussian]]],
) -> list[list[list[Gaussian]]]:
    """Build four 78-by-79 q0-root cofactor maps by reversed matching logic."""

    matchings = tuple(perfect_matchings(tuple(range(10))))
    assert len(matchings) == 945
    mixed_words = tuple(word for word in LOCAL_INDICES if len(set(word)) != 1)
    pair_offset = {pair: index for index, pair in enumerate(PAIRS)}
    eta_fixed = eta
    ports_fixed = transformed_ports
    response_maps = []
    for root in range(4):
        varied_edge = (root, 4)
        root_matchings = tuple(
            matching for matching in matchings if varied_edge in matching
        )
        assert len(root_matchings) == 105
        rows = []
        for word in mixed_words:
            row = [ZERO] * 79
            for matching in root_matchings:
                complement = tuple(edge for edge in matching if edge != varied_edge)
                if any(right < 4 for _left, right in complement):
                    continue
                raw_edges = [edge for edge in complement if edge[0] >= 5]
                assert len(raw_edges) == 1
                raw_left, raw_right = raw_edges[0]
                fixed = ONE
                for left, right in complement:
                    if left >= 4:
                        continue
                    if right == 5:
                        fixed = gmul(fixed, eta_fixed[left])
                    else:
                        fixed = gmul(
                            fixed,
                            ports_fixed[right - 6][word[right - 6]][left],
                        )
                if raw_left == 5:
                    port = raw_right - 6
                    raw_index = 1 + 3 * port + word[port]
                else:
                    assert raw_left >= 6
                    left_port = raw_left - 6
                    right_port = raw_right - 6
                    raw_index = (
                        25
                        + 9 * pair_offset[(left_port, right_port)]
                        + 3 * word[left_port]
                        + word[right_port]
                    )
                row[raw_index] = gadd(row[raw_index], fixed)
            rows.append(row)
        response_maps.append(rows)
    return response_maps


def project_response(
    response: list[list[Gaussian]],
    pivot_rows: tuple[int, ...],
    quotient_rows: tuple[int, ...],
    correction: list[list[Gaussian]],
) -> list[list[Gaussian]]:
    output = []
    for other_index, row_index in enumerate(quotient_rows):
        row = []
        for column in range(len(response[0])):
            row.append(
                gsub(
                    response[row_index][column],
                    gsum(
                        gmul(
                            correction[other_index][inner],
                            response[pivot_rows[inner]][column],
                        )
                        for inner in range(len(pivot_rows))
                    ),
                )
            )
        output.append(row)
    return output


def response_on_affine(
    raw_response: list[list[Gaussian]],
    affine_columns: list[list[Gaussian]],
) -> list[list[Gaussian]]:
    """Evaluate a raw 79-column response on [particular | reversed kernel]."""

    return [
        [
            gsum(
                gmul(raw_response[row][raw_column], affine_column[raw_column])
                for raw_column in range(79)
            )
            for affine_column in affine_columns
        ]
        for row in range(len(raw_response))
    ]


def parse_gaussian(raw: str) -> Gaussian:
    text = str(raw).strip().replace(" ", "")
    while len(text) >= 2 and text[0] == "(" and text[-1] == ")":
        depth = 0
        balanced = True
        for index, character in enumerate(text):
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0 and index != len(text) - 1:
                    balanced = False
                    break
        if not balanced or depth != 0:
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


Exponent = tuple[int, ...]
Polynomial = dict[Exponent, Gaussian]
ZERO_EXPONENT: Exponent = (0,) * 37
ONE_POLYNOMIAL: Polynomial = {ZERO_EXPONENT: ONE}


def polynomial_add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for exponent, coefficient in right.items():
        value = gadd(result.get(exponent, ZERO), coefficient)
        if value == ZERO:
            result.pop(exponent, None)
        else:
            result[exponent] = value
    return result


def polynomial_neg(value: Polynomial) -> Polynomial:
    return {exponent: gneg(coefficient) for exponent, coefficient in value.items()}


def polynomial_sub(left: Polynomial, right: Polynomial) -> Polynomial:
    return polynomial_add(left, polynomial_neg(right))


def polynomial_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_exp, left_coefficient in left.items():
        for right_exp, right_coefficient in right.items():
            exponent = tuple(left_exp[index] + right_exp[index] for index in range(37))
            coefficient = gmul(left_coefficient, right_coefficient)
            result[exponent] = gadd(result.get(exponent, ZERO), coefficient)
            if result[exponent] == ZERO:
                del result[exponent]
    return result


def polynomial_variable(index: int) -> Polynomial:
    exponent = [0] * 37
    exponent[index] = 1
    return {tuple(exponent): ONE}


def affine_polynomial(coefficients: list[Gaussian], constant: Gaussian) -> Polynomial:
    """Build z(t) in reversed coordinates b,a,t34,...,t0."""

    result: Polynomial = {}
    if constant != ZERO:
        result[ZERO_EXPONENT] = constant
    for local_parameter, coefficient in enumerate(coefficients):
        if coefficient == ZERO:
            continue
        exponent = [0] * 37
        exponent[2 + local_parameter] = 1
        exponent = tuple(exponent)
        result[exponent] = gadd(result.get(exponent, ZERO), coefficient)
    return {exponent: value for exponent, value in result.items() if value != ZERO}


def certificate_multiplier(encoded) -> Polynomial:
    result: Polynomial = {}
    seen = set()
    for raw_coefficient, raw_sparse_exponent in encoded:
        coefficient = parse_gaussian(raw_coefficient)
        assert coefficient != ZERO
        exponent = [0] * 37
        for raw_index, raw_power in raw_sparse_exponent:
            raw_index = int(raw_index)
            raw_power = int(raw_power)
            assert 0 <= raw_index < 37 and raw_power > 0
            assert raw_index not in seen
            seen.add(raw_index)
            # Certificate exponents are original t0,...,t34,a,b; reverse
            # into the audit's b,a,t34,...,t0 coordinates.
            exponent[36 - raw_index] = raw_power
        key = tuple(exponent)
        result[key] = gadd(result.get(key, ZERO), coefficient)
    return {exponent: value for exponent, value in result.items() if value != ZERO}


def polynomial_generators(coefficient_rows):
    z_rows = []
    for row in coefficient_rows:
        z_rows.append(
            [
                affine_polynomial(
                    [row[column][34 - index] for index in range(35)],
                    row[column][35],
                )
                for column in range(3)
            ]
        )
    a = polynomial_variable(1)
    b = polynomial_variable(0)
    first = []
    second = []
    for z0, z1, z2 in z_rows:
        first.extend(
            (
                polynomial_sub(polynomial_mul(a, z0), z1),
                polynomial_sub(polynomial_mul(b, z0), z2),
            )
        )
        second.extend(
            (
                z0,
                polynomial_sub(polynomial_mul(b, z1), z2),
            )
        )
    assert len(first) == len(second) == 130
    return {"z0_nonzero": first, "z0_zero_z1_nonzero": second}


def replay_certificates(coefficient_rows):
    raw = CERTIFICATE_PATH.read_bytes()
    canonical = raw.replace(b"\r\n", b"\n")
    assert b"\r" not in canonical
    assert hashlib.sha256(canonical).hexdigest() == CERTIFICATE_SHA256
    data = json.loads(canonical)
    assert data["format"] == "sparse-nullstellensatz-Qi-v1"
    assert tuple(data["variable_order"]) == ORIGINAL_VARIABLES
    assert tuple(reversed(data["variable_order"])) == REVERSED_VARIABLES
    assert data["generator_order"] == "quotient_row_then_equation"
    assert set(data["charts"]) == {
        "z0_nonzero",
        "z0_zero_z1_nonzero",
    }
    generators = polynomial_generators(coefficient_rows)
    term_counts = {}
    for chart_name, chart_generators in generators.items():
        encoded_generators = data["charts"][chart_name]
        assert len(chart_generators) == len(encoded_generators) == 130
        total: Polynomial = {}
        term_count = 0
        for generator, encoded in zip(
            chart_generators, encoded_generators, strict=True
        ):
            term_count += len(encoded)
            total = polynomial_add(
                total,
                polynomial_mul(certificate_multiplier(encoded), generator),
            )
        assert total == ONE_POLYNOMIAL, chart_name
        term_counts[chart_name] = term_count
    assert term_counts == {"z0_nonzero": 42, "z0_zero_z1_nonzero": 35}
    assert data["profiles"] == {
        "z0_nonzero": {
            "nonzero_ideal_generators": 126,
            "original_generator_rows": 130,
        },
        "z0_zero_z1_nonzero": {
            "nonzero_ideal_generators": 126,
            "original_generator_rows": 130,
        },
    }
    return len(canonical), term_counts


def gaussian_serial(value: Gaussian) -> str:
    return (
        f"{value[0].numerator}/{value[0].denominator},"
        f"{value[1].numerator}/{value[1].denominator}"
    )


def coefficient_fingerprint(coefficient_rows) -> str:
    fields = []
    for row in coefficient_rows:
        for form in row:
            # Canonical fingerprint is in the certificate's original t-order,
            # even though the audit's internal rows are reversed.
            canonical = [form[34 - index] for index in range(35)]
            canonical.append(form[35])
            fields.extend(gaussian_serial(value) for value in canonical)
    return hashlib.sha256("\n".join(fields).encode()).hexdigest()


def check() -> dict[str, object]:
    centre = [
        [gi(-2, -2), gi(-1, 2), gi(3)],
        [gi(0), gi(-3, 3), gi(0)],
        [gi(0), gi(-1, 2), gi(1)],
    ]
    leaf = [
        [gi(1), gi(1), gi(1)],
        [gi(0), gi(0), gi(1, 1)],
        [gi(0), gi(1), gi(1)],
    ]
    assert determinant3(centre) == gi(12)
    assert determinant3(leaf) == gi(-1, -1)
    frames = (centre, leaf, leaf, leaf)
    inverse_frames = tuple(matrix_inverse(frame) for frame in frames)
    survivor = frame_tensor(centre, leaf)
    target = target_delta()
    assert act_on_tensor(survivor, inverse_frames) == target

    xi, eta, ports = canonical_torus_star()
    original_columns = build_q_layer_columns(xi, eta, ports)
    assert rank(matrix_from_columns(original_columns)) == 44
    original_coefficients, _original_kernel, pivots_original, _free_original = (
        affine_fibre(original_columns, survivor)
    )
    assert len(pivots_original) == 44
    assert matrix_from_columns(original_columns)
    assert (
        matrix_vector(matrix_from_columns(original_columns), original_coefficients)
        == survivor
    )

    transformed_ports = transform_ports(ports, inverse_frames)
    transformed_columns = build_q_layer_columns(xi, eta, transformed_ports)
    transformed_target = target
    particular, kernels, pivots, free = affine_fibre(
        transformed_columns, transformed_target
    )
    assert len(pivots) == 44 and len(free) == 35
    assert (
        matrix_vector(matrix_from_columns(transformed_columns), particular)
        == transformed_target
    )
    for kernel_vector in kernels:
        assert (
            matrix_vector(matrix_from_columns(transformed_columns), kernel_vector)
            == [ZERO] * 81
        )

    # Reverse the original ascending free-column order for the polynomial
    # parameters.  The fibre itself is unchanged.
    ordered_kernels = [kernels[index] for index in range(34, -1, -1)]
    response_maps = q0_response_maps(xi, eta, transformed_ports)
    mixed_rows = tuple(
        row for row, word in enumerate(LOCAL_INDICES) if len(set(word)) != 1
    )
    constant_columns = [transformed_columns[0], *transformed_columns[13:25]]
    constant_mixed = [
        [column[row] for column in constant_columns] for row in mixed_rows
    ]
    assert rank(constant_mixed) == 13
    pivot_rows = pivot_columns(matrix_transpose(constant_mixed))
    assert len(pivot_rows) == 13
    quotient_pivot = determinant([constant_mixed[row] for row in pivot_rows])
    assert quotient_pivot == gi(Q(8, 27), Q(8, 27))
    quotient_rows = tuple(row for row in range(78) if row not in set(pivot_rows))
    assert len(quotient_rows) == 65
    pivot_inverse = matrix_inverse([constant_mixed[row] for row in pivot_rows])
    correction = matrix_multiply(
        [constant_mixed[row] for row in quotient_rows],
        pivot_inverse,
    )

    affine_columns = [particular, *ordered_kernels]
    projected_response_maps = [
        project_response(response, pivot_rows, quotient_rows, correction)
        for response in response_maps
    ]
    projected = [
        response_on_affine(response, affine_columns)
        for response in projected_response_maps
    ]
    relation = [
        [
            gsum((projected[root][row][column] for root in range(3)))
            for column in range(36)
        ]
        for row in range(65)
    ]
    relation = [
        [gsub(relation[row][column], projected[3][row][column]) for column in range(36)]
        for row in range(65)
    ]
    assert all(value == ZERO for row in relation for value in row)

    coefficient_rows = [
        [
            [projected[column][row][parameter] for parameter in range(1, 36)]
            + [projected[column][row][0]]
            for column in range(3)
        ]
        for row in range(65)
    ]

    # Independently recover the sign-plane response matrix.  The basis is
    # given in the certificate's original t-order, whereas coefficient_rows
    # retains the audit's reversed internal order.
    sign_fibre_vectors = []
    sign_raw_vectors = []
    for sparse_basis_vector in SIGN_FIBRE_BASIS:
        fibre_vector = [ZERO] * 35
        for index, value in sparse_basis_vector.items():
            fibre_vector[index] = value
        sign_fibre_vectors.append(fibre_vector)
        raw_vector = [
            gsum(
                gmul(kernels[index][row], fibre_vector[index])
                for index in range(35)
            )
            for row in range(79)
        ]
        assert raw_vector != [ZERO] * 79
        assert (
            matrix_vector(matrix_from_columns(transformed_columns), raw_vector)
            == [ZERO] * 81
        )
        for sigma in permutations((1, 2, 3)):
            sign = gi(permutation_sign(sigma))
            transported = permute_raw_vector(raw_vector, (0, *sigma))
            assert transported == [gmul(sign, value) for value in raw_vector]
        sign_raw_vectors.append(raw_vector)
    assert rank(matrix_from_columns(sign_raw_vectors)) == 3

    sign_images = []
    for response_column in range(3):
        image = []
        for row in range(65):
            image_row = []
            for fibre_vector in sign_fibre_vectors:
                image_row.append(
                    gsum(
                        gmul(
                            coefficient_rows[row][response_column][34 - index],
                            fibre_vector[index],
                        )
                        for index in range(35)
                    )
                )
            image.append(image_row)
        sign_images.append(image)
    sign_output_basis = sign_images[0]
    assert rank(sign_output_basis) == 3
    expected_sign_coordinate_matrices = (
        [[ONE, ZERO, ZERO], [ZERO, ONE, ZERO], [ZERO, ZERO, ONE]],
        [
            [gi(0, 1), gi(1, 1), ZERO],
            [gi(1, -1), gi(0, -1), ZERO],
            [ZERO, ZERO, gi(-1)],
        ],
        [[gi(-1), ZERO, ZERO], [ZERO, gi(-1), ZERO], [ZERO, ZERO, ONE]],
    )
    for image, coordinates in zip(
        sign_images, expected_sign_coordinate_matrices, strict=True
    ):
        assert matrix_multiply(sign_output_basis, coordinates) == image

    # Hence for sign coordinates (u,v,w) the three response columns are the
    # columns of
    # [[u, i*u+(1+i)*v, -u],
    #  [v, (1-i)*u-i*v, -v],
    #  [w, -w, w]].
    # Its nonzero 2-minors generate
    # ((u+v)(u-i*v), u*w, v*w).  The elementary projective split w!=0 / w=0
    # gives exactly [0:0:1], [i:1:0], and [1:-1:0], with distinct linear
    # factors over Q(i), so this three-point scheme is reduced.

    # Reynolds-average the complete raw kernel and the affine section using
    # the standard-library raw action above.  This independently reconstructs
    # the eight-dimensional invariant fibre used by the GLD78 principal-open
    # obstruction.
    def reynolds(vector):
        transported = [
            permute_raw_vector(vector, (0, *sigma))
            for sigma in permutations((1, 2, 3))
        ]
        return [
            gdiv(gsum(values), gi(6))
            for values in zip(*transported, strict=True)
        ]

    invariant_candidates = [
        [gmul(gi(6), value) for value in reynolds(kernel_vector)]
        for kernel_vector in kernels
    ]
    invariant_indices = (0, 7, 8, 9, 10, 12, 13, 16)
    invariant_raw = [invariant_candidates[index] for index in invariant_indices]
    assert rank(matrix_from_columns(invariant_candidates)) == 8
    assert rank(matrix_from_columns(invariant_raw)) == 8
    invariant_basis_rows = (0, 1, 8, 9, 10, 12, 13, 16)
    invariant_fibre = [
        [raw_vector[free[row]] for raw_vector in invariant_raw]
        for row in range(35)
    ]
    invariant_basis_pivot = determinant(
        [invariant_fibre[row] for row in invariant_basis_rows]
    )
    assert invariant_basis_pivot == gi(0, 1008)
    for raw_vector in invariant_raw:
        assert all(
            permute_raw_vector(raw_vector, (0, *sigma)) == raw_vector
            for sigma in permutations((1, 2, 3))
        )

    averaged_particular = reynolds(particular)
    assert (
        matrix_vector(matrix_from_columns(transformed_columns), averaged_particular)
        == transformed_target
    )
    assert all(
        permute_raw_vector(averaged_particular, (0, *sigma))
        == averaged_particular
        for sigma in permutations((1, 2, 3))
    )

    invariant_profiles = []
    invariant_expected = (
        (
            (2, 3, 6, 14, 15, 16, 18, 19, 67),
            gi(Q(6574160, 27), Q(1735448, 9)),
        ),
        (
            (2, 3, 6, 14, 15, 16, 18, 19, 22),
            gi(Q(153664, 9), Q(44480, 3)),
        ),
        (
            (2, 3, 6, 14, 15, 16, 18, 19, 67),
            gi(Q(-29451260, 81), Q(3419540, 81)),
        ),
    )
    for (a, b, _sparse_vector), (selected_rows, expected_determinant) in zip(
        PROJECTIVE_ESCAPE_WITNESSES, invariant_expected, strict=True
    ):
        operator_columns = []
        for raw_vector in invariant_raw:
            z0, z1, z2 = (
                matrix_vector(response, raw_vector)
                for response in projected_response_maps[:3]
            )
            operator_columns.append(
                [gsub(gmul(gi(a), z0[row]), z1[row]) for row in range(65)]
                + [gsub(gmul(gi(b), z0[row]), z2[row]) for row in range(65)]
            )
        operator = matrix_from_columns(operator_columns)
        c0, c1, c2 = (
            matrix_vector(response, averaged_particular)
            for response in projected_response_maps[:3]
        )
        affine_column = [
            gsub(gmul(gi(a), c0[row]), c1[row]) for row in range(65)
        ] + [gsub(gmul(gi(b), c0[row]), c2[row]) for row in range(65)]
        augmented = [
            row + [affine_column[index]] for index, row in enumerate(operator)
        ]
        selected = [augmented[row] for row in selected_rows]
        selected_operator = [row[:8] for row in selected]
        selected_determinant = determinant(selected)
        assert rank(operator) == 8
        assert rank(augmented) == 9
        assert rank(selected_operator) == 8
        assert selected_determinant == expected_determinant != ZERO, (
            selected_determinant,
            expected_determinant,
        )
        invariant_profiles.append(
            {
                "chart_ratios": [a, b],
                "operator_augmented_ranks": [8, 9],
                "selected_rows": list(selected_rows),
                "selected_determinant": gaussian_serial(selected_determinant),
            }
        )

    escape_profiles = []
    for a, b, sparse_vector in PROJECTIVE_ESCAPE_WITNESSES:
        vector = [ZERO] * 35
        for index, value in sparse_vector.items():
            vector[index] = value
        raw_direction = [
            gsum(gmul(kernels[index][row], vector[index]) for index in range(35))
            for row in range(79)
        ]
        assert raw_direction != [ZERO] * 79
        assert (
            matrix_vector(matrix_from_columns(transformed_columns), raw_direction)
            == [ZERO] * 81
        )

        linear_columns = []
        for column in range(3):
            linear_columns.append(
                [
                    gsum(
                        gmul(
                            coefficient_rows[row][column][34 - index],
                            vector[index],
                        )
                        for index in range(35)
                    )
                    for row in range(65)
                ]
            )
        z0, z1, z2 = linear_columns
        assert z0 != [ZERO] * 65
        assert z1 == [gmul(gi(a), value) for value in z0]
        assert z2 == [gmul(gi(b), value) for value in z0]
        assert rank(
            [[z0[row], z1[row], z2[row]] for row in range(65)]
        ) == 1

        proportionality_rows = []
        for row in range(65):
            proportionality_rows.append(
                [
                    gsub(
                        gmul(gi(a), coefficient_rows[row][0][34 - index]),
                        coefficient_rows[row][1][34 - index],
                    )
                    for index in range(35)
                ]
            )
        for row in range(65):
            proportionality_rows.append(
                [
                    gsub(
                        gmul(gi(b), coefficient_rows[row][0][34 - index]),
                        coefficient_rows[row][2][34 - index],
                    )
                    for index in range(35)
                ]
            )
        assert rank(proportionality_rows) == 34
        escape_profiles.append(
            {
                "column_ratios": [1, a, b],
                "support_size": len(sparse_vector),
                "proportionality_rank_nullity": [34, 1],
            }
        )

    certificate_bytes, term_counts = replay_certificates(coefficient_rows)
    point_rows = [
        coefficient_rows[row][column] for row in range(65) for column in (0, 1)
    ]
    coefficient_rank = rank([row[:35] for row in point_rows])
    augmented_rank = rank(point_rows)
    assert (coefficient_rank, augmented_rank) == (35, 36)
    fingerprint = coefficient_fingerprint(coefficient_rows)
    assert (
        fingerprint
        == "17c10d8e04a4e29b073914919beb0a99ff77735be12cc16f095e07ef7549452e"
    )

    return {
        "status": "exact_full_coefficient_fibre_first_response_nonextension",
        "global_conjecture": "UNRESOLVED",
        "transformed_permanent_map_shape": [81, 79],
        "transformed_permanent_map_rank": 44,
        "affine_fibre_dimension": 35,
        "q0_constant_full_mixed_ranks": [13, 13],
        "q0_quotient_pivot_rows": list(pivot_rows),
        "q0_quotient_pivot": gaussian_serial(quotient_pivot),
        "q0_quotient_matrix_shape": [65, 3],
        "projective_raw_fibre_escape_profiles": escape_profiles,
        "raw_fibre_sign_dimension": 3,
        "sign_plane_rank_one_ideal": [
            "(u+v)*(u-i*v)",
            "u*w",
            "v*w",
        ],
        "sign_plane_reduced_projective_point_count": 3,
        "sign_boundary_invariant_open_profiles": invariant_profiles,
        "sign_boundary_invariant_basis_fibre_rows": list(invariant_basis_rows),
        "sign_boundary_invariant_basis_pivot": gaussian_serial(
            invariant_basis_pivot
        ),
        "sign_boundary_invariant_principal_open_obstruction": True,
        "boundary_outside_sign_plane_classified": False,
        "projective_escape_is_not_affine_response_lift": True,
        "reverse_variable_order": list(REVERSED_VARIABLES),
        "rank_at_most_one_projective_cover": [
            "z0_nonzero",
            "z0_zero_z1_nonzero",
            "z0_equals_z1_equals_zero",
        ],
        "nullstellensatz_multiplier_terms": term_counts,
        "coordinate_direction_coefficient_augmented_ranks": [
            coefficient_rank,
            augmented_rank,
        ],
        "quotient_affine_coefficient_sha256": fingerprint,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_bytes": certificate_bytes,
        "full_raw_coefficient_fibre_excluded_at_q0_first_response": True,
        "whole_ghz_survivor_locus_excluded": False,
        "root_order_four_maximality_certified": False,
        "fifth_root_excluded": False,
        "graph_witness_proved": False,
    }


def main() -> None:
    result = check()
    print("GLD74 full coefficient-fibre first-response obstruction: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
