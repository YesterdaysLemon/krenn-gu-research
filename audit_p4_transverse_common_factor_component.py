#!/usr/bin/env python3
"""Independent modular audit of the transverse common-factor component."""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass


BITS = tuple(itertools.product(range(2), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
TRIPLES = tuple(itertools.combinations(range(4), 3))
PIVOTS = ((2, 1), (0, 2), (0, 2), (2, 0))
DEGREE_TWO_MASKS = (3, 5, 9, 6, 10, 12)
DEGREE_THREE_MASKS = (14, 13, 11, 7)
MODULUS = 101


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
            (self.tangent * rhs.value - self.value * rhs.tangent)
            * inverse
            * inverse,
        )

    def __rtruediv__(self, other: object) -> "Dual":
        return as_dual(other) / self


def as_dual(value: object) -> Dual:
    return value if isinstance(value, Dual) else Dual(int(value))


@dataclass(frozen=True)
class Jet2:
    constant: int
    linear: int = 0
    quadratic: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "constant", self.constant % MODULUS)
        object.__setattr__(self, "linear", self.linear % MODULUS)
        object.__setattr__(self, "quadratic", self.quadratic % MODULUS)

    def __add__(self, other: object) -> "Jet2":
        rhs = as_jet(other)
        return Jet2(
            self.constant + rhs.constant,
            self.linear + rhs.linear,
            self.quadratic + rhs.quadratic,
        )

    __radd__ = __add__

    def __neg__(self) -> "Jet2":
        return Jet2(-self.constant, -self.linear, -self.quadratic)

    def __sub__(self, other: object) -> "Jet2":
        return self + (-as_jet(other))

    def __rsub__(self, other: object) -> "Jet2":
        return as_jet(other) - self

    def __mul__(self, other: object) -> "Jet2":
        rhs = as_jet(other)
        return Jet2(
            self.constant * rhs.constant,
            self.constant * rhs.linear + self.linear * rhs.constant,
            self.constant * rhs.quadratic
            + self.linear * rhs.linear
            + self.quadratic * rhs.constant,
        )

    __rmul__ = __mul__


def as_jet(value: object) -> Jet2:
    return value if isinstance(value, Jet2) else Jet2(int(value))


def rank_mod(matrix: list[list[int]]) -> int:
    work = [[entry % MODULUS for entry in row] for row in matrix]
    if not work:
        return 0
    rank = 0
    columns = len(work[0])
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]), None
        )
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
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]), None
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        pivot_value = work[column][column]
        result = result * pivot_value % MODULUS
        pivot_inverse = inv(pivot_value)
        for row in range(column + 1, len(work)):
            factor = work[row][column] * pivot_inverse % MODULUS
            for entry in range(column, len(work)):
                work[row][entry] = (
                    work[row][entry] - factor * work[column][entry]
                ) % MODULUS
    return result % MODULUS


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
            if row == column:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (left - factor * pivot_entry) % MODULUS
                    for left, pivot_entry in zip(work[row], work[column])
                ]
    return [work[index][-1] for index in range(size)]


def subset_product(rows: list[tuple[int, ...]]) -> dict[int, int]:
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
    return table


def subset_product_jet(rows: list[tuple[Jet2, ...]]) -> dict[int, Jet2]:
    table = {0: Jet2(1)}
    for row in rows:
        nxt: dict[int, Jet2] = {}
        for mask, coefficient in table.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) == 0:
                    target = mask | (1 << column)
                    nxt[target] = nxt.get(target, Jet2(0)) + coefficient * entry
        table = nxt
    return table


def subset_permanent(rows: list[tuple[int, ...]]) -> int:
    return subset_product(rows).get(15, 0)


def pair_product(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    table = subset_product([left, right])
    return tuple(table.get(mask, 0) for mask in DEGREE_TWO_MASKS)


def triple_covector(rows: list[tuple[int, ...]]) -> tuple[int, ...]:
    table = subset_product(rows)
    return tuple(table.get(mask, 0) for mask in DEGREE_THREE_MASKS)


def add(
    left: tuple[object, ...], right: tuple[object, ...], scale: object = 1
) -> tuple[object, ...]:
    return tuple(x + scale * y for x, y in zip(left, right))


def scale_row(row: tuple[object, ...], scale: object) -> tuple[object, ...]:
    return tuple(scale * entry for entry in row)


def raw_family_planes(parameters: list[Dual]) -> list[list[tuple[Dual, ...]]]:
    r, k, t0, t1, t2 = parameters
    a = tuple(Dual(value) for value in (1, 1, 0, 0))
    c = tuple(Dual(value) for value in (1, -1, 0, 0))
    b = tuple(Dual(value) for value in (0, 0, 1, 1))
    m = add(b, c)
    m_r = add(b, c, 1 + r)
    d = (Dual(0), (r + 2) * (k + 1), Dual(1), k)
    n = (-(k - 1) * (r + 2), Dual(0), Dual(-1), k)
    diagonal = (t0, t1, t2, Dual(1))
    raw = ((n, c), (a, m), (a, m_r), (d, c))
    return [
        [tuple(entry * diagonal[column] for column, entry in enumerate(row)) for row in plane]
        for plane in raw
    ]


def normalized_chart_coordinates(parameters: list[Dual]) -> list[Dual]:
    coordinates: list[Dual] = []
    for plane, pivot in zip(raw_family_planes(parameters), PIVOTS):
        a00, a01 = plane[0][pivot[0]], plane[0][pivot[1]]
        a10, a11 = plane[1][pivot[0]], plane[1][pivot[1]]
        determinant = a00 * a11 - a01 * a10
        inverse = (
            (a11 / determinant, -a01 / determinant),
            (-a10 / determinant, a00 / determinant),
        )
        normalized = [
            [
                inverse[row][0] * plane[0][column]
                + inverse[row][1] * plane[1][column]
                for column in range(4)
            ]
            for row in range(2)
        ]
        nonpivots = [column for column in range(4) if column not in pivot]
        coordinates.extend(
            normalized[row][column]
            for row in range(2)
            for column in nonpivots
        )
    return coordinates


def chart_planes(values: list[int]) -> tuple[list[list[tuple[int, ...]]], list[list[list[int | None]]]]:
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


def incidence_jets(variables: list[Jet2]) -> list[Jet2]:
    chart_values = variables[:16]
    z_values = variables[16:]
    planes: list[list[tuple[Jet2, ...]]] = []
    index = 0
    for pivot in PIVOTS:
        rows = [[Jet2(0) for _ in range(4)] for _ in range(2)]
        for row, column in enumerate(pivot):
            rows[row][column] = Jet2(1)
        nonpivots = [column for column in range(4) if column not in pivot]
        for row in range(2):
            for column in nonpivots:
                rows[row][column] = chart_values[index]
                index += 1
        planes.append([tuple(row) for row in rows])

    coefficients: dict[tuple[int, int, int, int], Jet2] = {}
    for bits in BITS:
        rows = [planes[mode][bits[mode]] for mode in range(4)]
        coefficients[bits] = subset_product_jet(rows).get(15, Jet2(0))
    alpha = (1, 1, 1, 1)
    equations: list[Jet2] = []
    for bits in BITS:
        if bits == alpha:
            continue
        monomial = Jet2(1)
        for mode, bit in enumerate(bits):
            if bit == 0:
                monomial = monomial * z_values[mode]
        equations.append(coefficients[bits] - coefficients[alpha] * monomial)
    return equations


def audit_prime(prime: int) -> dict[str, object]:
    global MODULUS
    MODULUS = prime
    base = [-4 * inv(3), 2, 1, 1, 1]

    # Independent transformed replay of the exact graph and cubic spans.
    raw_dual = raw_family_planes([Dual(value) for value in base])
    raw = [[tuple(entry.value for entry in row) for row in plane] for plane in raw_dual]
    order = (2, 0, 3, 1)
    scales = (2, 3, 5, 7)

    def transform(row: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(
            scales[index] * row[order[index]] % MODULUS for index in range(4)
        )

    planes = [[transform(row) for row in plane] for plane in raw]
    coefficients = {
        bits: subset_permanent([planes[mode][bits[mode]] for mode in range(4)])
        for bits in BITS
    }
    support = {bits: value for bits, value in coefficients.items() if value}
    assert set(support) == {(1, 1, 1, 1)}

    pair_matrices: dict[tuple[int, int], list[list[int]]] = {}
    pair_profile: list[int] = []
    for edge in PAIRS:
        columns = [
            pair_product(planes[edge[0]][left], planes[edge[1]][right])
            for left, right in itertools.product(range(2), repeat=2)
        ]
        matrix = [[columns[column][row] for column in range(4)] for row in range(6)]
        pair_matrices[edge] = matrix
        pair_profile.append(rank_mod(matrix))
    assert pair_profile == [3, 3, 4, 3, 3, 3]

    explicit_relations = {
        (0, 1): (0, 0, 1, 0),
        (0, 2): (0, 0, 1, 0),
        (1, 2): (0, -1, 1, 0),
        (1, 3): (0, 1, 0, 0),
        (2, 3): (0, 1, 0, 0),
    }
    for edge, relation in explicit_relations.items():
        assert all(
            sum(row[column] * relation[column] for column in range(4))
            % MODULUS
            == 0
            for row in pair_matrices[edge]
        )

    triple_ranks: dict[str, int] = {}
    for triple in TRIPLES:
        columns = []
        for local_bits in itertools.product(range(2), repeat=3):
            if local_bits == (1, 1, 1):
                continue
            columns.append(
                triple_covector(
                    [
                        planes[triple[index]][local_bits[index]]
                        for index in range(3)
                    ]
                )
            )
        matrix = [[columns[column][row] for column in range(7)] for row in range(4)]
        triple_ranks["".join(map(str, triple))] = rank_mod(matrix)
    assert set(triple_ranks.values()) == {2}

    # Forward-dual family tangent in the nontrivial Grassmann charts.
    family_columns: list[list[int]] = []
    for direction in range(5):
        parameters = [
            Dual(value, int(index == direction)) for index, value in enumerate(base)
        ]
        family_columns.append(
            [entry.tangent for entry in normalized_chart_coordinates(parameters)]
        )
    family_jacobian = [
        [family_columns[column][row] for column in range(5)] for row in range(16)
    ]
    assert rank_mod(family_jacobian) == 5

    # Literal-chart permanent derivatives give an independent incidence rank.
    chart_values = [
        entry.value
        for entry in normalized_chart_coordinates([Dual(value) for value in base])
    ]
    normalized_planes, row_variables = chart_planes(chart_values)
    coefficient_data: dict[tuple[int, int, int, int], tuple[int, list[int]]] = {}
    for bits in BITS:
        coefficient_data[bits] = permanent_with_derivatives(
            [normalized_planes[mode][bits[mode]] for mode in range(4)],
            [row_variables[mode][bits[mode]] for mode in range(4)],
        )
    assert coefficient_data[(1, 1, 1, 1)][0] == 4 % MODULUS
    assert all(
        value == 0
        for bits, (value, _) in coefficient_data.items()
        if bits != (1, 1, 1, 1)
    )

    incidence: list[list[int]] = []
    for bits in BITS:
        if bits == (1, 1, 1, 1):
            continue
        row = list(coefficient_data[bits][1]) + [0] * 4
        zero_positions = [index for index, bit in enumerate(bits) if bit == 0]
        if len(zero_positions) == 1:
            row[16 + zero_positions[0]] = -coefficient_data[(1, 1, 1, 1)][0]
        incidence.append([entry % MODULUS for entry in row])
    assert rank_mod(incidence) == 14

    selected_rows = (0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14)
    selected_columns = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 16, 17, 19)
    selected_minor = determinant_mod(
        [[incidence[row][column] for column in selected_columns] for row in selected_rows]
    )
    assert selected_minor == (-131072) % MODULUS

    # The five visible family directions lie in the six-dimensional kernel.
    family_lift = [row + [0] * 0 for row in family_jacobian] + [[0] * 5 for _ in range(4)]
    for incidence_row in incidence:
        for direction in range(5):
            assert (
                sum(
                    incidence_row[index] * family_lift[index][direction]
                    for index in range(20)
                )
                % MODULUS
                == 0
            )
    assert 20 - rank_mod(incidence) == 6

    # Independent second-order implicit replay.  The fourteen selected rows
    # define a smooth sixfold, but the omitted 1001 equation has coefficient
    # 12 along the sixth implicit direction z2=h after solving the selected
    # equations through order two.
    base_variables = chart_values + [0, 0, 0, 0]
    selected_matrix = [
        [incidence[row][column] for column in selected_columns]
        for row in selected_rows
    ]

    def make_variables(first: list[int], second: list[int]) -> list[Jet2]:
        values = [Jet2(value) for value in base_variables]
        values[18] = Jet2(0, 1, 0)
        for index, column in enumerate(selected_columns):
            values[column] = Jet2(base_variables[column], first[index], second[index])
        return values

    zero = [0] * 14
    initial = incidence_jets(make_variables(zero, zero))
    first_residual = [initial[row].linear for row in selected_rows]
    first_correction = solve_mod(
        selected_matrix, [(-value) % MODULUS for value in first_residual]
    )
    first_order = incidence_jets(make_variables(first_correction, zero))
    second_residual = [first_order[row].quadratic for row in selected_rows]
    second_correction = solve_mod(
        selected_matrix, [(-value) % MODULUS for value in second_residual]
    )
    second_order = incidence_jets(
        make_variables(first_correction, second_correction)
    )
    assert all(
        second_order[row].linear == 0 and second_order[row].quadratic == 0
        for row in selected_rows
    )
    transverse_quadratic = second_order[9].quadratic
    assert transverse_quadratic == 12 % MODULUS

    return {
        "prime": prime,
        "pure_support": {"1111": support[(1, 1, 1, 1)]},
        "pair_profile": pair_profile,
        "triple_span_ranks": triple_ranks,
        "family_tangent_rank": rank_mod(family_jacobian),
        "incidence_rank": rank_mod(incidence),
        "selected_incidence_minor": selected_minor,
        "transverse_quadratic_obstruction": transverse_quadratic,
    }


def main() -> None:
    audits = [audit_prime(prime) for prime in (101, 103)]
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent subset-DP and forward-dual replay",
                "component": "transverse binary-polarity common-factor component",
                "audits": audits,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
