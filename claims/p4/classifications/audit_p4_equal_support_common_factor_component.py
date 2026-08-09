#!/usr/bin/env python3
"""Independent modular audit for the equal-support common-factor component."""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass


MODULUS = 101
BITS = tuple(itertools.product(range(2), repeat=4))
PIVOTS = ((0, 1), (0, 1), (0, 1), (0, 2))


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

    def __rtruediv__(self, other: object) -> "Dual":
        return as_dual(other) / self


def as_dual(value: object) -> Dual:
    return value if isinstance(value, Dual) else Dual(int(value))


def rank_mod(matrix: list[list[int]]) -> int:
    work = [[entry % MODULUS for entry in row] for row in matrix]
    if not work:
        return 0
    rank = 0
    columns = len(work[0])
    for column in range(columns):
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
        if rank == len(work):
            break
    return rank


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
                work[row][entry] = (work[row][entry] - factor * work[column][entry]) % MODULUS
    return result % MODULUS


def subset_permanent(rows: list[tuple[int, ...]]) -> int:
    table = {0: 1}
    for row in rows:
        nxt: dict[int, int] = {}
        for mask, coefficient in table.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) == 0:
                    target = mask | (1 << column)
                    nxt[target] = (nxt.get(target, 0) + coefficient * entry) % MODULUS
        table = nxt
    return table[15]


def pair_product(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        (left[i] * right[j] + left[j] * right[i]) % MODULUS
        for i, j in itertools.combinations(range(4), 2)
    )


def family_chart_coordinates(parameters: list[Dual]) -> list[Dual]:
    p, q, r, t0, t1, t2 = parameters
    two = Dual(2)
    return [
        t2 * (p + q) / (two * t0),
        (p + q) / (two * t0),
        t2 * (p - q) / (two * t1),
        (p - q) / (two * t1),
        t2 / (two * t0),
        1 / (two * t0),
        -t2 / (two * t1),
        -1 / (two * t1),
        t2 / (two * r * t0),
        1 / (two * r * t0),
        -t2 / (two * r * t1),
        -1 / (two * r * t1),
        -t1 / t0,
        0,
        0,
        -1 / t2,
    ]


def chart_planes(values: list[int]) -> list[list[tuple[int, ...]]]:
    planes: list[list[tuple[int, ...]]] = []
    index = 0
    for pivot in PIVOTS:
        rows = [[0] * 4 for _ in range(2)]
        for row, column in enumerate(pivot):
            rows[row][column] = 1
        nonpivots = [column for column in range(4) if column not in pivot]
        for row in range(2):
            for column in nonpivots:
                rows[row][column] = values[index] % MODULUS
                index += 1
        planes.append([tuple(row) for row in rows])
    return planes


def permanent_with_derivatives(
    rows: list[tuple[int, ...]], row_variables: list[list[int | None]]
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
            variable = row_variables[row][permutation[row]]
            if variable is None:
                continue
            partial = 1
            for other in range(4):
                if other != row:
                    partial = partial * entries[other] % MODULUS
            derivative[variable] = (derivative[variable] + partial) % MODULUS
    return value, derivative


def main() -> None:
    # Independent source permutation and unequal diagonal scaling at the
    # rational component point p=1,q=2,r=2.
    a = (1, 1, 0, 0)
    a_bar = (1, -1, 0, 0)
    b = (0, 0, 1, 1)
    b_bar = (0, 0, 1, -1)

    def add(left: tuple[int, ...], right: tuple[int, ...], scale: int = 1) -> tuple[int, ...]:
        return tuple((x + scale * y) % MODULUS for x, y in zip(left, right))

    raw_planes = (
        (add(a, b), add(a_bar, b, 2)),
        (a, add(a_bar, b)),
        (a, add(b, a_bar, 2)),
        (b_bar, a_bar),
    )
    order = (2, 0, 3, 1)
    scales = (2, 3, 5, 7)

    def transform(row: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(scales[index] * row[order[index]] % MODULUS for index in range(4))

    planes = tuple(tuple(transform(row) for row in plane) for plane in raw_planes)
    coefficients = {
        bits: subset_permanent([planes[mode][bits[mode]] for mode in range(4)])
        for bits in BITS
    }
    support = {bits: value for bits, value in coefficients.items() if value}
    assert set(support) == {(0, 1, 1, 1), (1, 1, 1, 1)}

    pair_ranks = []
    for i, j in itertools.combinations(range(4), 2):
        columns = [
            pair_product(planes[i][left], planes[j][right])
            for left, right in itertools.product(range(2), repeat=2)
        ]
        matrix = [[columns[column][row] for column in range(4)] for row in range(6)]
        pair_ranks.append(rank_mod(matrix))
    assert pair_ranks == [4, 4, 4, 3, 3, 3]

    # Forward-dual family tangent over F_101.
    base = [1, 2, 2, 1, 1, 1]
    family_columns: list[list[int]] = []
    for direction in range(6):
        parameters = [Dual(value, int(index == direction)) for index, value in enumerate(base)]
        family_columns.append(
            [as_dual(entry).tangent for entry in family_chart_coordinates(parameters)]
        )
    family_jacobian = [
        [family_columns[column][row] for column in range(6)] for row in range(16)
    ]
    assert rank_mod(family_jacobian) == 6

    # Independent incidence Jacobian.  Chart variables occur as literal
    # matrix entries, so permanent derivatives are reconstructed directly.
    chart_values = [
        as_dual(entry).value
        for entry in family_chart_coordinates([Dual(value) for value in base])
    ]
    normalized_planes = chart_planes(chart_values)
    row_variables: list[list[list[int | None]]] = []
    variable = 0
    for pivot in PIVOTS:
        variables = [[None] * 4 for _ in range(2)]
        nonpivots = [column for column in range(4) if column not in pivot]
        for row in range(2):
            for column in nonpivots:
                variables[row][column] = variable
                variable += 1
        row_variables.append(variables)

    tensor_data: dict[tuple[int, ...], tuple[int, list[int]]] = {}
    for bits in BITS:
        tensor_data[bits] = permanent_with_derivatives(
            [normalized_planes[mode][bits[mode]] for mode in range(4)],
            [row_variables[mode][bits[mode]] for mode in range(4)],
        )
    alpha = (0, 0, 0, 0)
    alpha_value, alpha_derivative = tensor_data[alpha]
    z = [(-2 * inv(5)) % MODULUS, -1 % MODULUS, -1 % MODULUS, 0]
    incidence: list[list[int]] = []
    incidence_bits: list[tuple[int, ...]] = []
    for bits in BITS:
        if bits == alpha:
            continue
        incidence_bits.append(bits)
        value, derivative = tensor_data[bits]
        monomial = 1
        for index, bit in enumerate(bits):
            if bit:
                monomial = monomial * z[index] % MODULUS
        row = [
            (derivative[index] - monomial * alpha_derivative[index]) % MODULUS
            for index in range(16)
        ]
        for index in range(4):
            if not bits[index]:
                row.append(0)
                continue
            other_product = 1
            for other, bit in enumerate(bits):
                if bit and other != index:
                    other_product = other_product * z[other] % MODULUS
            row.append((-alpha_value * other_product) % MODULUS)
        incidence.append(row)
    assert rank_mod(incidence) == 14

    selected_rows = [index for index, bits in enumerate(incidence_bits) if bits != (1, 1, 1, 0)]
    selected_columns = [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 17, 19]
    minor = [
        [incidence[row][column] for column in selected_columns]
        for row in selected_rows
    ]
    expected_minor = (-9 * inv(2)) % MODULUS
    assert determinant_mod(minor) == expected_minor

    print(
        json.dumps(
            {
                "status": "pass",
                "audit_field": "F_101",
                "source_order": list(order),
                "source_scales": list(scales),
                "pure_support": {str(bits): value for bits, value in support.items()},
                "pair_profile": pair_ranks,
                "family_tangent_rank": rank_mod(family_jacobian),
                "incidence_rank": rank_mod(incidence),
                "incidence_minor": determinant_mod(minor),
                "permanent": "subset DP and direct product derivatives",
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
