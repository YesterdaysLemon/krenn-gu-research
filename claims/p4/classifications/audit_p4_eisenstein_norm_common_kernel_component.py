#!/usr/bin/env python3
"""Independent modular audit of the Eisenstein-norm component."""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass


MODULUS = 101
BITS = tuple(itertools.product(range(2), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = ((0, 3), (0, 2), (1, 2), (2, 0))


def inv(value: int) -> int:
    return pow(value % MODULUS, MODULUS - 2, MODULUS)


@dataclass(frozen=True)
class Dual:
    value: int
    tangent: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", self.value % MODULUS)
        object.__setattr__(self, "tangent", self.tangent % MODULUS)

    def __add__(self, other: object) -> "Dual":
        rhs = as_dual(other)
        return Dual(self.value + rhs.value, self.tangent + rhs.tangent)

    __radd__ = __add__

    def __neg__(self) -> "Dual":
        return Dual(-self.value, -self.tangent)

    def __sub__(self, other: object) -> "Dual":
        return self + (-as_dual(other))

    def __rsub__(self, other: object) -> "Dual":
        return as_dual(other) - self

    def __mul__(self, other: object) -> "Dual":
        rhs = as_dual(other)
        return Dual(
            self.value * rhs.value,
            self.tangent * rhs.value + self.value * rhs.tangent,
        )

    __rmul__ = __mul__

    def __truediv__(self, other: object) -> "Dual":
        rhs = as_dual(other)
        inverse = inv(rhs.value)
        return Dual(
            self.value * inverse,
            (self.tangent * rhs.value - self.value * rhs.tangent) * inverse * inverse,
        )


def as_dual(value: object) -> Dual:
    return value if isinstance(value, Dual) else Dual(int(value))


def rank_mod(matrix: list[list[int]]) -> int:
    work = [[entry % MODULUS for entry in row] for row in matrix]
    rank = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = inv(work[rank][column])
        work[rank] = [(entry * scale) % MODULUS for entry in work[rank]]
        for row in range(len(work)):
            if row == rank or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % MODULUS
                for left, right in zip(work[row], work[rank])
            ]
        rank += 1
    return rank


def pivot_columns(matrix: list[list[int]]) -> tuple[int, ...]:
    work = [[entry % MODULUS for entry in row] for row in matrix]
    rank = 0
    pivots: list[int] = []
    for column in range(len(work[0]) if work else 0):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = inv(work[rank][column])
        work[rank] = [(entry * scale) % MODULUS for entry in work[rank]]
        for row in range(len(work)):
            if row == rank or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % MODULUS
                for left, right in zip(work[row], work[rank])
            ]
        pivots.append(column)
        rank += 1
    return tuple(pivots)


def determinant_mod(matrix: list[list[int]]) -> int:
    work = [[entry % MODULUS for entry in row] for row in matrix]
    result = 1
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        pivot_value = work[column][column]
        result = result * pivot_value % MODULUS
        scale = inv(pivot_value)
        for row in range(column + 1, len(work)):
            factor = work[row][column] * scale % MODULUS
            for entry in range(column, len(work)):
                work[row][entry] = (
                    work[row][entry] - factor * work[column][entry]
                ) % MODULUS
    return result % MODULUS


def subset_permanent(rows: list[tuple[int, ...]]) -> int:
    table = {0: 1}
    for row in rows:
        nxt: dict[int, int] = {}
        for mask, coefficient in table.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) == 0:
                    target = mask | (1 << column)
                    nxt[target] = (
                        nxt.get(target, 0) + coefficient * entry
                    ) % MODULUS
        table = nxt
    return table[15]


def pair_product(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        (left[i] * right[j] + left[j] * right[i]) % MODULUS
        for i, j in PAIRS
    )


def add(*rows: tuple[Dual, ...]) -> tuple[Dual, ...]:
    return tuple(sum((row[index] for row in rows), Dual(0)) for index in range(4))


def scale(value: Dual, row: tuple[Dual, ...]) -> tuple[Dual, ...]:
    return tuple(value * entry for entry in row)


def family_planes(parameters: list[Dual]) -> list[list[tuple[Dual, ...]]]:
    alpha, beta, r, gamma, t0, t1, t2 = parameters
    a = tuple(map(Dual, (1, 1, 0, 0)))
    c = tuple(map(Dual, (1, -1, 0, 0)))
    b = tuple(map(Dual, (0, 0, 1, 1)))
    b_bar = tuple(map(Dual, (0, 0, 1, -1)))
    m = add(scale(alpha, a), scale(beta, c), b)
    m_r = add(m, scale(r, c))
    d = add(scale(gamma, a), b)
    x0 = add(b, scale(-(alpha + gamma), a), scale(-(2 * beta + r), c))
    diagonal = (t0, t1, t2, Dual(1))
    return [
        [tuple(entry * diagonal[index] for index, entry in enumerate(row)) for row in plane]
        for plane in ((b_bar, x0), (m, a), (m_r, a), (c, d))
    ]


def det2(plane: list[tuple[Dual, ...]], columns: tuple[int, int]) -> Dual:
    i, j = columns
    return plane[0][i] * plane[1][j] - plane[0][j] * plane[1][i]


def plucker_ratios(planes: list[list[tuple[Dual, ...]]]) -> list[Dual]:
    result: list[Dual] = []
    for plane, pivot in zip(planes, PIVOTS):
        denominator = det2(plane, pivot)
        for pair in PAIRS:
            if set(pair) == set(pivot):
                continue
            result.append(det2(plane, pair) / denominator)
    return result


def normalize_plane(
    plane: list[tuple[int, ...]], pivot: tuple[int, int]
) -> list[tuple[int, ...]]:
    i, j = pivot
    a, b = plane[0][i] % MODULUS, plane[0][j] % MODULUS
    c, d = plane[1][i] % MODULUS, plane[1][j] % MODULUS
    determinant = (a * d - b * c) % MODULUS
    inverse = inv(determinant)
    left = ((d * inverse) % MODULUS, (-b * inverse) % MODULUS)
    right = ((-c * inverse) % MODULUS, (a * inverse) % MODULUS)
    return [
        tuple((left[0] * plane[0][k] + left[1] * plane[1][k]) % MODULUS for k in range(4)),
        tuple((right[0] * plane[0][k] + right[1] * plane[1][k]) % MODULUS for k in range(4)),
    ]


def chart_values(planes: list[list[tuple[int, ...]]]) -> list[int]:
    values: list[int] = []
    for plane, pivot in zip(planes, PIVOTS):
        normalized = normalize_plane(plane, pivot)
        nonpivots = [column for column in range(4) if column not in pivot]
        values.extend(
            normalized[row][column]
            for row in range(2)
            for column in nonpivots
        )
    return values


def generic_chart_planes(values: list[int]) -> tuple[list[list[tuple[int, ...]]], list[list[list[int | None]]]]:
    planes: list[list[tuple[int, ...]]] = []
    variables: list[list[list[int | None]]] = []
    index = 0
    for pivot in PIVOTS:
        rows = [[0] * 4 for _ in range(2)]
        row_variables: list[list[int | None]] = [[None] * 4 for _ in range(2)]
        for row, column in enumerate(pivot):
            rows[row][column] = 1
        nonpivots = [column for column in range(4) if column not in pivot]
        for row in range(2):
            for column in nonpivots:
                rows[row][column] = values[index] % MODULUS
                row_variables[row][column] = index
                index += 1
        planes.append([tuple(row) for row in rows])
        variables.append(row_variables)
    return planes, variables


def permanent_with_derivatives(
    rows: list[tuple[int, ...]], variables: list[list[int | None]]
) -> tuple[int, list[int]]:
    value = 0
    derivative = [0] * 16
    for permutation in itertools.permutations(range(4)):
        entries = [rows[row][permutation[row]] % MODULUS for row in range(4)]
        term = 1
        for entry in entries:
            term = term * entry % MODULUS
        value = (value + term) % MODULUS
        for row in range(4):
            variable = variables[row][permutation[row]]
            if variable is None:
                continue
            partial = 1
            for other in range(4):
                if other != row:
                    partial = partial * entries[other] % MODULUS
            derivative[variable] = (derivative[variable] + partial) % MODULUS
    return value, derivative


def main() -> None:
    base = [2, 1, 1, 1, 1, 1, 1]
    gamma_tangents = (-5 * inv(4), 9 * inv(4), 5 * inv(4))
    family_columns: list[list[int]] = []
    for direction in range(6):
        parameters: list[Dual] = []
        for index, value in enumerate(base):
            tangent = 0
            if direction < 3:
                tangent = int(index == direction)
                if index == 3:
                    tangent = gamma_tangents[direction]
            elif index == direction + 1:
                tangent = 1
            parameters.append(Dual(value, tangent))
        family_columns.append(
            [entry.tangent for entry in plucker_ratios(family_planes(parameters))]
        )
    family_jacobian = [
        [family_columns[column][row] for column in range(6)] for row in range(20)
    ]
    assert rank_mod(family_jacobian) == 5

    raw_dual = family_planes([Dual(value) for value in base])
    raw = [[tuple(entry.value for entry in row) for row in plane] for plane in raw_dual]
    order = (2, 0, 3, 1)
    scales = (2, 3, 5, 7)

    def transform(row: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(scales[index] * row[order[index]] % MODULUS for index in range(4))

    transformed = [[transform(row) for row in plane] for plane in raw]
    coefficients = {
        bits: subset_permanent([transformed[mode][bits[mode]] for mode in range(4)])
        for bits in BITS
    }
    support = {bits: value for bits, value in coefficients.items() if value}
    assert set(support) == {(1, 1, 1, 1)}

    pair_profile: list[int] = []
    for i, j in PAIRS:
        columns = [
            pair_product(transformed[i][left], transformed[j][right])
            for left, right in itertools.product(range(2), repeat=2)
        ]
        matrix = [[columns[column][row] for column in range(4)] for row in range(6)]
        pair_profile.append(rank_mod(matrix))
    assert pair_profile == [4, 4, 4, 3, 3, 3]

    values = chart_values(raw)
    planes, row_variables = generic_chart_planes(values)
    coefficient_data: dict[tuple[int, ...], tuple[int, list[int]]] = {}
    for bits in BITS:
        rows = [planes[mode][bits[mode]] for mode in range(4)]
        variables = [row_variables[mode][bits[mode]] for mode in range(4)]
        coefficient_data[bits] = permanent_with_derivatives(rows, variables)
    anchor = (0, 0, 0, 0)
    anchor_value, anchor_derivative = coefficient_data[anchor]
    assert anchor_value == (-2 * inv(3)) % MODULUS
    z = (0, -3 % MODULUS, 0, 0)
    incidence: list[list[int]] = []
    for bits in BITS:
        if bits == anchor:
            continue
        value, derivative = coefficient_data[bits]
        support_indices = [index for index, bit in enumerate(bits) if bit]
        monomial = 1
        for index in support_indices:
            monomial = monomial * z[index] % MODULUS
        row = [
            (derivative[index] - monomial * anchor_derivative[index]) % MODULUS
            for index in range(16)
        ]
        for variable in range(4):
            partial = 0
            if variable in support_indices:
                partial = 1
                for index in support_indices:
                    if index != variable:
                        partial = partial * z[index] % MODULUS
            row.append((-anchor_value * partial) % MODULUS)
        incidence.append(row)
    assert rank_mod(incidence) == 15
    columns = pivot_columns(incidence)
    assert len(columns) == 15
    incidence_minor = determinant_mod([[row[column] for column in columns] for row in incidence])
    assert incidence_minor != 0

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "Pluecker-dual tangent and independent modular incidence",
                "modulus": MODULUS,
                "source_order": order,
                "source_scales": scales,
                "family_tangent_rank": 5,
                "pure_support": ["1111"],
                "pair_profile": pair_profile,
                "incidence_columns": columns,
                "incidence_minor_mod_p": incidence_minor,
                "incidence_rank": 15,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
