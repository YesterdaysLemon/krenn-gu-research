#!/usr/bin/env python3
"""Independent modular audit of the common-kernel vertical component."""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = ((0, 2),) * 4
ALPHA = (0, 0, 0, 1)
SELECTED_ROWS = tuple(range(14))
SELECTED_COLUMNS = (0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 13, 14, 17, 19)
FREE_COLUMNS = (3, 11, 12, 15, 16, 18)
MODULUS = 101


def inv(value: int) -> int:
    return pow(value % MODULUS, MODULUS - 2, MODULUS)


def rank_mod(matrix: list[list[int]]) -> int:
    work = [[entry % MODULUS for entry in row] for row in matrix]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = inv(work[pivot_row][column])
        work[pivot_row] = [entry * scale % MODULUS for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % MODULUS
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
    return pivot_row


def determinant_mod(matrix: list[list[int]]) -> int:
    work = [[entry % MODULUS for entry in row] for row in matrix]
    determinant = 1
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        value = work[column][column]
        determinant = determinant * value % MODULUS
        scale = inv(value)
        for row in range(column + 1, len(work)):
            factor = work[row][column] * scale % MODULUS
            for index in range(column, len(work)):
                work[row][index] = (
                    work[row][index] - factor * work[column][index]
                ) % MODULUS
    return determinant % MODULUS


def solve_mod(matrix: list[list[int]], right: list[int]) -> list[int]:
    size = len(matrix)
    work = [
        [entry % MODULUS for entry in row] + [right[index] % MODULUS]
        for index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        scale = inv(work[column][column])
        work[column] = [entry * scale % MODULUS for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right_entry) % MODULUS
                for left, right_entry in zip(work[row], work[column], strict=True)
            ]
    return [work[index][-1] % MODULUS for index in range(size)]


@dataclass(frozen=True)
class Dual:
    value: int
    tangent: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", self.value % MODULUS)
        object.__setattr__(self, "tangent", self.tangent % MODULUS)

    @staticmethod
    def coerce(value: int | Dual) -> Dual:
        return value if isinstance(value, Dual) else Dual(value)

    def __add__(self, other: int | Dual) -> Dual:
        rhs = self.coerce(other)
        return Dual(self.value + rhs.value, self.tangent + rhs.tangent)

    __radd__ = __add__

    def __neg__(self) -> Dual:
        return Dual(-self.value, -self.tangent)

    def __sub__(self, other: int | Dual) -> Dual:
        return self + (-self.coerce(other))

    def __rsub__(self, other: int | Dual) -> Dual:
        return self.coerce(other) - self

    def __mul__(self, other: int | Dual) -> Dual:
        rhs = self.coerce(other)
        return Dual(
            self.value * rhs.value,
            self.value * rhs.tangent + self.tangent * rhs.value,
        )

    __rmul__ = __mul__

    def __truediv__(self, other: int | Dual) -> Dual:
        rhs = self.coerce(other)
        inverse = inv(rhs.value)
        return Dual(
            self.value * inverse,
            (self.tangent * rhs.value - self.value * rhs.tangent) * inverse * inverse,
        )


@dataclass(frozen=True)
class Jet2:
    constant: int
    linear: int = 0
    quadratic: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "constant", self.constant % MODULUS)
        object.__setattr__(self, "linear", self.linear % MODULUS)
        object.__setattr__(self, "quadratic", self.quadratic % MODULUS)

    @staticmethod
    def coerce(value: int | Jet2) -> Jet2:
        return value if isinstance(value, Jet2) else Jet2(value)

    def __add__(self, other: int | Jet2) -> Jet2:
        rhs = self.coerce(other)
        return Jet2(
            self.constant + rhs.constant,
            self.linear + rhs.linear,
            self.quadratic + rhs.quadratic,
        )

    __radd__ = __add__

    def __neg__(self) -> Jet2:
        return Jet2(-self.constant, -self.linear, -self.quadratic)

    def __sub__(self, other: int | Jet2) -> Jet2:
        return self + (-self.coerce(other))

    def __rsub__(self, other: int | Jet2) -> Jet2:
        return self.coerce(other) - self

    def __mul__(self, other: int | Jet2) -> Jet2:
        rhs = self.coerce(other)
        return Jet2(
            self.constant * rhs.constant,
            self.constant * rhs.linear + self.linear * rhs.constant,
            self.constant * rhs.quadratic
            + self.linear * rhs.linear
            + self.quadratic * rhs.constant,
        )

    __rmul__ = __mul__


def add(left, right, scale: int = 1):
    return tuple(left[index] + scale * right[index] for index in range(4))


def raw_family(p, q, phi, diagonal=(1, 1, 1, 1)):
    one = type(p)(1) if isinstance(p, Dual) else 1
    zero = type(p)(0) if isinstance(p, Dual) else 0
    x0 = (one, zero, zero, zero)
    x1 = (zero, one, zero, zero)
    x2 = (zero, zero, one, zero)
    x3 = (zero, zero, zero, one)
    a = add(x0, x1)
    a_bar = add(x0, x1, -1)
    b = add(x2, x3)
    b_bar = add(x2, x3, -1)
    planes = (
        (add(a_bar, b, p), add(b_bar, b, q)),
        (b, a),
        (b_bar, a),
        (a_bar, add(b, b_bar, phi)),
    )
    return tuple(
        tuple(
            tuple(row[column] * diagonal[column] for column in range(4))
            for row in plane
        )
        for plane in planes
    )


def subset_permanent(rows) -> int:
    state = {0: 1}
    for row in rows:
        updated: dict[int, int] = {}
        for mask, value in state.items():
            for coordinate, entry in enumerate(row):
                if mask & (1 << coordinate):
                    continue
                target = mask | (1 << coordinate)
                updated[target] = (updated.get(target, 0) + value * entry) % MODULUS
        state = updated
    return state.get(15, 0)


def subset_permanent_jet(rows) -> Jet2:
    state = {0: Jet2(1)}
    for row in rows:
        updated: dict[int, Jet2] = {}
        for mask, value in state.items():
            for coordinate, entry in enumerate(row):
                if mask & (1 << coordinate):
                    continue
                target = mask | (1 << coordinate)
                updated[target] = updated.get(target, Jet2(0)) + value * entry
        state = updated
    return state.get(15, Jet2(0))


def pair_product(left, right):
    return tuple((left[i] * right[j] + left[j] * right[i]) % MODULUS for i, j in PAIRS)


def normalized_chart_coordinates(parameters: list[Dual]) -> list[Dual]:
    p, q, phi, t0, t2 = parameters
    planes = raw_family(p, q, phi, (t0, Dual(1), t2, Dual(1)))
    result: list[Dual] = []
    for plane, pivot in zip(planes, PIVOTS, strict=True):
        a00, a01 = plane[0][pivot[0]], plane[0][pivot[1]]
        a10, a11 = plane[1][pivot[0]], plane[1][pivot[1]]
        determinant = a00 * a11 - a01 * a10
        inverse = (
            (a11 / determinant, -a01 / determinant),
            (-a10 / determinant, a00 / determinant),
        )
        normalized = [
            [
                inverse[row][0] * plane[0][column] + inverse[row][1] * plane[1][column]
                for column in range(4)
            ]
            for row in range(2)
        ]
        nonpivots = [column for column in range(4) if column not in pivot]
        result.extend(
            normalized[row][column] for row in range(2) for column in nonpivots
        )
    return result


def chart_planes(values):
    planes = []
    variables = []
    index = 0
    for pivot in PIVOTS:
        rows = [[0] * 4 for _ in range(2)]
        row_variables = [[None] * 4 for _ in range(2)]
        rows[0][pivot[0]] = 1
        rows[1][pivot[1]] = 1
        nonpivots = [column for column in range(4) if column not in pivot]
        for row in range(2):
            for column in nonpivots:
                rows[row][column] = values[index] % MODULUS
                row_variables[row][column] = index
                index += 1
        planes.append([tuple(row) for row in rows])
        variables.append(row_variables)
    return planes, variables


def permanent_with_derivatives(rows, row_variables):
    value = 0
    derivative = [0] * 16
    for permutation in itertools.permutations(range(4)):
        entries = [rows[row][permutation[row]] % MODULUS for row in range(4)]
        term = 1
        for entry in entries:
            term = term * entry % MODULUS
        value = (value + term) % MODULUS
        for row in range(4):
            variable = row_variables[row][permutation[row]]
            if variable is None:
                continue
            partial = 1
            for other in range(4):
                if other != row:
                    partial = partial * entries[other] % MODULUS
            derivative[variable] = (derivative[variable] + partial) % MODULUS
    return value, derivative


def incidence_jets(variables: list[Jet2]) -> list[Jet2]:
    chart_values = variables[:16]
    z_values = variables[16:]
    planes = []
    index = 0
    for pivot in PIVOTS:
        rows = [[Jet2(0) for _ in range(4)] for _ in range(2)]
        rows[0][pivot[0]] = Jet2(1)
        rows[1][pivot[1]] = Jet2(1)
        nonpivots = [column for column in range(4) if column not in pivot]
        for row in range(2):
            for column in nonpivots:
                rows[row][column] = chart_values[index]
                index += 1
        planes.append([tuple(row) for row in rows])

    tensor = {
        word: subset_permanent_jet([planes[mode][word[mode]] for mode in range(4)])
        for word in WORDS
    }
    equations = []
    for word in WORDS:
        if word == ALPHA:
            continue
        monomial = Jet2(1)
        for mode in range(4):
            if word[mode] != ALPHA[mode]:
                monomial = monomial * z_values[mode]
        equations.append(tensor[word] - tensor[ALPHA] * monomial)
    return equations


def audit_prime(prime: int) -> dict[str, object]:
    global MODULUS
    MODULUS = prime

    # Independent source permutation and unequal scaling replay the tensor,
    # pair profile, and three intrinsic relations.
    p, q, phi = 2, 3, 2
    planes = raw_family(p, q, phi)
    order = (2, 0, 3, 1)
    scales = (2, 3, 5, 7)

    def transform(row):
        return tuple(scales[index] * row[order[index]] % MODULUS for index in range(4))

    transformed = tuple(tuple(transform(row) for row in plane) for plane in planes)
    tensor = {
        word: subset_permanent([transformed[mode][word[mode]] for mode in range(4)])
        for word in WORDS
    }
    assert {word for word, value in tensor.items() if value} == {
        (0, 1, 1, 1),
        (1, 1, 1, 1),
    }

    pair_matrices = {}
    profile = []
    for edge in PAIRS:
        columns = [
            pair_product(transformed[edge[0]][left], transformed[edge[1]][right])
            for left, right in itertools.product(range(2), repeat=2)
        ]
        matrix = [[columns[column][row] for column in range(4)] for row in range(6)]
        pair_matrices[edge] = matrix
        profile.append(rank_mod(matrix))
    assert profile == [4, 4, 4, 3, 3, 3]

    relations = {
        (1, 2): (1, 0, 0, 0),
        (1, 3): (0, 0, 1, 0),
        (2, 3): (0, 0, 1, 0),
    }
    for edge, relation in relations.items():
        assert all(
            sum(row[column] * relation[column] for column in range(4)) % MODULUS == 0
            for row in pair_matrices[edge]
        )

    # Forward-dual family tangent in the literal (02) charts.
    base_parameters = [2, 3, 2, 1, 1]
    family_columns = []
    for direction in range(5):
        parameters = [
            Dual(value, int(index == direction))
            for index, value in enumerate(base_parameters)
        ]
        family_columns.append(
            [entry.tangent for entry in normalized_chart_coordinates(parameters)]
        )
    family_jacobian = [
        [family_columns[column][row] for column in range(5)] for row in range(16)
    ]
    assert rank_mod(family_jacobian) == 5
    family_minor = determinant_mod(
        [
            [family_jacobian[row][column] for column in range(5)]
            for row in (0, 1, 3, 7, 15)
        ]
    )
    assert family_minor == inv(72)

    chart_values = [
        entry.value
        for entry in normalized_chart_coordinates(
            [Dual(value) for value in base_parameters]
        )
    ]
    normalized, row_variables = chart_planes(chart_values)
    coefficient_data = {}
    for word in WORDS:
        coefficient_data[word] = permanent_with_derivatives(
            [normalized[mode][word[mode]] for mode in range(4)],
            [row_variables[mode][word[mode]] for mode in range(4)],
        )
    assert coefficient_data[ALPHA][0] == 2 % MODULUS
    assert coefficient_data[(1, 0, 0, 1)][0] == inv(3)
    assert all(
        value == 0
        for word, (value, _) in coefficient_data.items()
        if word not in {ALPHA, (1, 0, 0, 1)}
    )

    z_values = [inv(6), 0, 0, 0]
    incidence = []
    for word in WORDS:
        if word == ALPHA:
            continue
        differences = [mode for mode in range(4) if word[mode] != ALPHA[mode]]
        monomial = 1
        for mode in differences:
            monomial = monomial * z_values[mode] % MODULUS
        row = [
            (
                coefficient_data[word][1][index]
                - coefficient_data[ALPHA][1][index] * monomial
            )
            % MODULUS
            for index in range(16)
        ] + [0] * 4
        for mode in differences:
            derivative = 1
            for other in differences:
                if other != mode:
                    derivative = derivative * z_values[other] % MODULUS
            row[16 + mode] = -coefficient_data[ALPHA][0] * derivative % MODULUS
        incidence.append(row)

    assert rank_mod(incidence) == 14
    selected_matrix = [
        [incidence[row][column] for column in SELECTED_COLUMNS] for row in SELECTED_ROWS
    ]
    incidence_minor = determinant_mod(selected_matrix)
    assert incidence_minor == 1280 * inv(27) % MODULUS

    # Independent second-order implicit replay.  Free coordinates are
    # (g3,g11,g12,g15,z0,z2), with z2=h the excess direction.
    base_variables = chart_values + z_values

    def make_variables(first: list[int], second: list[int]) -> list[Jet2]:
        values = [Jet2(value) for value in base_variables]
        values[18] = Jet2(base_variables[18], 1, 0)
        for index, column in enumerate(SELECTED_COLUMNS):
            values[column] = Jet2(base_variables[column], first[index], second[index])
        return values

    initial = incidence_jets(make_variables([0] * 14, [0] * 14))
    first_residual = [initial[row].linear for row in SELECTED_ROWS]
    first_correction = solve_mod(
        selected_matrix, [(-value) % MODULUS for value in first_residual]
    )
    first_order = incidence_jets(make_variables(first_correction, [0] * 14))
    second_residual = [first_order[row].quadratic for row in SELECTED_ROWS]
    second_correction = solve_mod(
        selected_matrix, [(-value) % MODULUS for value in second_residual]
    )
    second_order = incidence_jets(make_variables(first_correction, second_correction))
    assert all(
        second_order[row].linear == 0 and second_order[row].quadratic == 0
        for row in SELECTED_ROWS
    )
    transverse_quadratic = second_order[14].quadratic
    assert transverse_quadratic == inv(6)

    return {
        "prime": prime,
        "pair_profile": profile,
        "family_rank": rank_mod(family_jacobian),
        "family_minor": family_minor,
        "incidence_rank": rank_mod(incidence),
        "incidence_minor": incidence_minor,
        "transverse_quadratic": transverse_quadratic,
    }


def main() -> None:
    results = [audit_prime(prime) for prime in (101, 103)]
    print(
        json.dumps(
            {
                "status": "audited",
                "arithmetic": "independent modular dual and second-order jets",
                "results": results,
                "role": "independent corroboration of the characteristic-zero proof",
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
