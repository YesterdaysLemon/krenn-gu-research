#!/usr/bin/env python3
"""Independent modular audit of the coincident-support rank-one star."""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = ((0, 1), (0, 1), (0, 1), (0, 2))
ALPHA = (0, 0, 0, 0)
SELECTED_ROWS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 14)
SELECTED_COLUMNS = (0, 1, 2, 4, 5, 6, 7, 8, 10, 12, 13, 14, 19)
FREE_COLUMNS = (3, 9, 11, 15, 16, 17, 18)
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

    def __truediv__(self, other: int | Jet2) -> Jet2:
        rhs = self.coerce(other)
        inverse_constant = inv(rhs.constant)
        inverse_linear = -rhs.linear * inverse_constant**2
        inverse_quadratic = (
            rhs.linear**2 * inverse_constant**3 - rhs.quadratic * inverse_constant**2
        )
        return self * Jet2(inverse_constant, inverse_linear, inverse_quadratic)


def add(left, right, scale=1):
    return tuple(left[index] + scale * right[index] for index in range(4))


def raw_family(p, q, kappa, ell, diagonal=(1, 1, 1, 1)):
    one = Jet2(1) if isinstance(p, Jet2) else 1
    zero = Jet2(0) if isinstance(p, Jet2) else 0
    x0 = (one, zero, zero, zero)
    x1 = (zero, one, zero, zero)
    x2 = (zero, zero, one, zero)
    x3 = (zero, zero, zero, one)
    a = add(x0, x1)
    c = add(x0, x1, -1)
    b = add(x2, x3)
    d = add(x2, x3, -1)
    planes = (
        (add(a, b, p), add(c, b, q)),
        (a, c),
        (c, add(b, a, kappa)),
        (add(a, c, ell), d),
    )
    return tuple(
        tuple(
            tuple(row[column] * diagonal[column] for column in range(4))
            for row in plane
        )
        for plane in planes
    )


def subset_permanent(rows):
    zero = Jet2(0) if isinstance(rows[0][0], Jet2) else 0
    one = Jet2(1) if isinstance(rows[0][0], Jet2) else 1
    state = {0: one}
    for row in rows:
        updated = {}
        for mask, value in state.items():
            for coordinate, entry in enumerate(row):
                if mask & (1 << coordinate):
                    continue
                target = mask | (1 << coordinate)
                updated[target] = updated.get(target, zero) + value * entry
        state = updated
    return state.get(15, zero)


def pair_product(left, right):
    return tuple((left[i] * right[j] + left[j] * right[i]) % MODULUS for i, j in PAIRS)


def normalized_chart_coordinates(parameters: list[Jet2]) -> list[Jet2]:
    p, q, kappa, ell, t0, t2 = parameters
    planes = raw_family(
        p,
        q,
        kappa,
        ell,
        (t0, Jet2(1), t2, Jet2(1)),
    )
    result: list[Jet2] = []
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
    index = 0
    for pivot in PIVOTS:
        rows = [[Jet2(0) for _ in range(4)] for _ in range(2)]
        rows[0][pivot[0]] = Jet2(1)
        rows[1][pivot[1]] = Jet2(1)
        nonpivots = [column for column in range(4) if column not in pivot]
        for row in range(2):
            for column in nonpivots:
                rows[row][column] = values[index]
                index += 1
        planes.append([tuple(row) for row in rows])
    return planes


def incidence_jets(variables: list[Jet2]) -> list[Jet2]:
    planes = chart_planes(variables[:16])
    z_values = variables[16:]
    tensor = {
        word: subset_permanent([planes[mode][word[mode]] for mode in range(4)])
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

    p, q, kappa, ell = 2, 3, 1, 2
    planes = raw_family(p, q, kappa, ell)
    tensor = {
        word: subset_permanent([planes[mode][word[mode]] for mode in range(4)])
        for word in WORDS
    }
    expected_support = {
        (0, 0, 1, 0): 4 * p,
        (0, 1, 1, 0): -4 * ell * p,
        (1, 0, 1, 0): 4 * q,
        (1, 1, 1, 0): -4 * ell * q,
    }
    assert all(
        value % MODULUS == expected_support.get(word, 0) % MODULUS
        for word, value in tensor.items()
    )

    pair_matrices = {}
    profile = []
    for edge in PAIRS:
        columns = [
            pair_product(planes[edge[0]][left], planes[edge[1]][right])
            for left, right in itertools.product(range(2), repeat=2)
        ]
        matrix = [[columns[column][row] for column in range(4)] for row in range(6)]
        pair_matrices[edge] = matrix
        profile.append(rank_mod(matrix))
    assert profile == [3, 4, 4, 3, 3, 4]

    relations = {
        (0, 1): (1, -q * inv(p), -p * inv(q), 1),
        (1, 2): (1, 0, 0, 0),
        (1, 3): (ell, 0, 1, 0),
    }
    for edge, relation in relations.items():
        assert all(
            sum(row[column] * relation[column] for column in range(4)) % MODULUS == 0
            for row in pair_matrices[edge]
        )

    base_parameters = [2, 3, 1, 2, 1, 1]
    family_columns = []
    for direction in range(6):
        parameters = [
            Jet2(value, int(index == direction))
            for index, value in enumerate(base_parameters)
        ]
        family_columns.append(
            [entry.linear for entry in normalized_chart_coordinates(parameters)]
        )
    family_jacobian = [
        [family_columns[column][row] for column in range(6)] for row in range(16)
    ]
    assert rank_mod(family_jacobian) == 6
    family_minor = determinant_mod(
        [
            [family_jacobian[row][column] for column in range(6)]
            for row in (0, 1, 2, 8, 10, 12)
        ]
    )
    assert family_minor == -5 * inv(72) % MODULUS

    chart_values = [
        entry.constant
        for entry in normalized_chart_coordinates(
            [Jet2(value) for value in base_parameters]
        )
    ]
    z_values = [-inv(5) % MODULUS, -3 % MODULUS, 1, 0]
    base_variables = chart_values + z_values
    base_equations = incidence_jets([Jet2(value) for value in base_variables])
    assert all(equation.constant == 0 for equation in base_equations)

    incidence_columns = []
    for direction in range(20):
        variables = [
            Jet2(value, int(index == direction))
            for index, value in enumerate(base_variables)
        ]
        incidence_columns.append(
            [equation.linear for equation in incidence_jets(variables)]
        )
    incidence = [
        [incidence_columns[column][row] for column in range(20)] for row in range(15)
    ]
    assert rank_mod(incidence) == 13
    selected_matrix = [
        [incidence[row][column] for column in SELECTED_COLUMNS] for row in SELECTED_ROWS
    ]
    incidence_minor = determinant_mod(selected_matrix)
    assert incidence_minor == 100 % MODULUS

    def make_variables(first: list[int], second: list[int]) -> list[Jet2]:
        values = [Jet2(value) for value in base_variables]
        values[18] = Jet2(base_variables[18], 1, 0)
        for index, column in enumerate(SELECTED_COLUMNS):
            values[column] = Jet2(base_variables[column], first[index], second[index])
        return values

    initial = incidence_jets(make_variables([0] * 13, [0] * 13))
    first_residual = [initial[row].linear for row in SELECTED_ROWS]
    first_correction = solve_mod(
        selected_matrix, [(-value) % MODULUS for value in first_residual]
    )
    first_order = incidence_jets(make_variables(first_correction, [0] * 13))
    second_residual = [first_order[row].quadratic for row in SELECTED_ROWS]
    second_correction = solve_mod(
        selected_matrix, [(-value) % MODULUS for value in second_residual]
    )
    second_order = incidence_jets(make_variables(first_correction, second_correction))
    assert all(
        second_order[row].linear == 0 and second_order[row].quadratic == 0
        for row in SELECTED_ROWS
    )
    omitted_quadratics = [second_order[row].quadratic for row in (9, 13)]
    assert omitted_quadratics == [7 * inv(60) % MODULUS, -7 * inv(20) % MODULUS]

    # Directly replay the mixed-chain vertical boundary at [r:s]=[0:1].
    a, c = planes[1]
    b = add((0, 0, 1, 0), (0, 0, 0, 1))
    d = add((0, 0, 1, 0), (0, 0, 0, 1), -1)
    target = (
        (add(a, b, p), add(c, b, q)),
        (a, c),
        (c, b),
        (c, d),
    )
    target_tensor = {
        word: subset_permanent([target[mode][word[mode]] for mode in range(4)])
        for word in WORDS
    }
    target_expected = {
        (0, 1, 1, 0): -4 * p,
        (1, 1, 1, 0): -4 * q,
    }
    assert all(
        value % MODULUS == target_expected.get(word, 0) % MODULUS
        for word, value in target_tensor.items()
    )

    return {
        "prime": prime,
        "pair_profile": profile,
        "family_rank": rank_mod(family_jacobian),
        "family_minor": family_minor,
        "incidence_rank": rank_mod(incidence),
        "incidence_minor": incidence_minor,
        "omitted_quadratics": omitted_quadratics,
        "vertical_boundary": True,
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
