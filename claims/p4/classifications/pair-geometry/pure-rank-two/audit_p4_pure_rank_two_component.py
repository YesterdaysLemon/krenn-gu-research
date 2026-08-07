#!/usr/bin/env python3
"""Independent finite-field audit of the P4 component certificate."""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_PURE_RANK_TWO_COMPONENT_THEOREM.md"
PRIMARY = ROOT / "verify_p4_pure_rank_two_component.py"
MODULUS = 101
VARIABLE_COUNT = 20


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Dual:
    value: int
    gradient: tuple[int, ...]

    @staticmethod
    def constant(value: int) -> "Dual":
        return Dual(value % MODULUS, (0,) * VARIABLE_COUNT)

    @staticmethod
    def variable(value: int, index: int) -> "Dual":
        gradient = [0] * VARIABLE_COUNT
        gradient[index] = 1
        return Dual(value % MODULUS, tuple(gradient))

    def __add__(self, other: int | "Dual") -> "Dual":
        other = lift(other)
        return Dual(
            (self.value + other.value) % MODULUS,
            tuple(
                (left + right) % MODULUS
                for left, right in zip(
                    self.gradient, other.gradient, strict=True
                )
            ),
        )

    __radd__ = __add__

    def __neg__(self) -> "Dual":
        return Dual(
            (-self.value) % MODULUS,
            tuple((-entry) % MODULUS for entry in self.gradient),
        )

    def __sub__(self, other: int | "Dual") -> "Dual":
        return self + (-lift(other))

    def __rsub__(self, other: int | "Dual") -> "Dual":
        return lift(other) - self

    def __mul__(self, other: int | "Dual") -> "Dual":
        other = lift(other)
        return Dual(
            self.value * other.value % MODULUS,
            tuple(
                (
                    self.value * right
                    + other.value * left
                ) % MODULUS
                for left, right in zip(
                    self.gradient, other.gradient, strict=True
                )
            ),
        )

    __rmul__ = __mul__

    def inverse(self) -> "Dual":
        inverse_value = pow(self.value, -1, MODULUS)
        scale = -inverse_value * inverse_value
        return Dual(
            inverse_value,
            tuple(scale * entry % MODULUS for entry in self.gradient),
        )

    def __truediv__(self, other: int | "Dual") -> "Dual":
        return self * lift(other).inverse()

    def __rtruediv__(self, other: int | "Dual") -> "Dual":
        return lift(other) * self.inverse()


def lift(value: int | Dual) -> Dual:
    return value if isinstance(value, Dual) else Dual.constant(value)


def permanent_dp(rows: list[list[Dual]]) -> Dual:
    table = {0: Dual.constant(1)}
    for row in rows:
        next_table: dict[int, Dual] = {}
        for mask, subtotal in table.items():
            for column in range(4):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_table[new_mask] = (
                    next_table.get(new_mask, Dual.constant(0))
                    + subtotal * row[column]
                )
        table = next_table
    return table[15]


def matrix_rank_mod(matrix: list[list[int]]) -> int:
    work = [[entry % MODULUS for entry in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(rank, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, MODULUS)
        work[rank] = [
            entry * inverse % MODULUS for entry in work[rank]
        ]
        for row in range(len(work)):
            if row == rank:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    (entry - scale * pivot_entry) % MODULUS
                    for entry, pivot_entry in zip(
                        work[row], work[rank], strict=True
                    )
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def determinant_mod(matrix: list[list[int]]) -> int:
    work = [[entry % MODULUS for entry in row] for row in matrix]
    determinant = 1
    for column in range(len(work)):
        pivot = next(
            (
                row
                for row in range(column, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % MODULUS
        inverse = pow(pivot_value, -1, MODULUS)
        for row in range(column + 1, len(work)):
            scale = work[row][column] * inverse % MODULUS
            for inner in range(column, len(work)):
                work[row][inner] = (
                    work[row][inner] - scale * work[column][inner]
                ) % MODULUS
    return determinant % MODULUS


def audit_incidence() -> tuple[int, int, list[int]]:
    point = (
        -1, -2, 1, 0,
        1, 0, 0, 1,
        0, 1, -1, 0,
        0, 1, 0, -1,
        -1, 1, 0, 0,
    )
    variables = [
        Dual.variable(value, index)
        for index, value in enumerate(point)
    ]
    (
        a, b, c, d, e, f, g, h,
        i, j, k, ell, m, n, o, p,
        z0, z1, z2, z3,
    ) = variables
    rows = (
        ((1, 0, a, b), (0, 1, c, d)),
        ((e, 1, 0, f), (g, 0, 1, h)),
        ((i, 1, 0, j), (k, 0, 1, ell)),
        ((1, m, n, 0), (0, o, p, 1)),
    )
    words = tuple(itertools.product((0, 1), repeat=4))
    coefficients = {
        word: permanent_dp(
            [
                [lift(entry) for entry in rows[mode][word[mode]]]
                for mode in range(4)
            ]
        )
        for word in words
    }
    anchor = (1, 0, 0, 0)
    ratios = (z0, z1, z2, z3)
    equations = []
    for word in words:
        if word == anchor:
            continue
        ratio_product = Dual.constant(1)
        for mode in range(4):
            if word[mode] != anchor[mode]:
                ratio_product *= ratios[mode]
        equations.append(
            coefficients[word] - coefficients[anchor] * ratio_product
        )
    assert coefficients[anchor].value == 2
    assert all(equation.value == 0 for equation in equations)
    jacobian = [list(equation.gradient) for equation in equations]
    rank = matrix_rank_mod(jacobian)
    pivot_columns = [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 18, 19]
    minor = [
        [row[column] for column in pivot_columns]
        for row in jacobian
    ]
    determinant = determinant_mod(minor)
    assert rank == 15
    assert determinant == (-4096) % MODULUS
    return rank, determinant, [
        coefficient.value for coefficient in coefficients.values()
    ]


def audit_family_tangent() -> tuple[int, int, list[int]]:
    parameter_values = (1, 1, 1, 1, 0)
    parameters = [
        Dual.variable(value, index)
        for index, value in enumerate(parameter_values)
    ]
    E, I, L, Q, C = parameters
    coordinates = (
        -Q * (C + E * I * L) / E,
        -C * Q - E * I * (L * Q + 1),
        C / E + I * L,
        C,
        L, 0, 0, E,
        0, E * I * L, -1 / I, 0,
        0, I, 0, -1 / E,
    )
    coordinate_duals = [lift(coordinate) for coordinate in coordinates]
    expected_values = (
        -1, -2, 1, 0,
        1, 0, 0, 1,
        0, 1, -1, 0,
        0, 1, 0, -1,
    )
    actual_values = tuple(
        coordinate.value for coordinate in coordinate_duals
    )
    assert actual_values == tuple(
        value % MODULUS for value in expected_values
    )
    jacobian = [
        list(coordinate.gradient[:5])
        for coordinate in coordinate_duals
    ]
    rank = matrix_rank_mod(jacobian)
    determinant = determinant_mod(jacobian[:5])
    assert rank == 5
    assert determinant == 2
    return rank, determinant, list(actual_values)


def main() -> None:
    incidence_rank, incidence_determinant, coefficients = audit_incidence()
    family_rank, family_determinant, coordinates = audit_family_tangent()
    nonzero_coefficients = {
        format(index, "04b"): value
        for index, value in enumerate(coefficients)
        if value
    }
    assert nonzero_coefficients == {
        "0000": -2 % MODULUS,
        "0100": -2 % MODULUS,
        "1000": 2,
        "1100": 2,
    }

    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": "forward-mode dual numbers and DP permanent",
        "modulus": MODULUS,
        "incidence_jacobian_rank": incidence_rank,
        "incidence_minor_determinant_mod_p": incidence_determinant,
        "expected_incidence_minor_determinant_mod_p": (-4096) % MODULUS,
        "family_tangent_rank": family_rank,
        "family_tangent_minor_determinant_mod_p": family_determinant,
        "chart_coordinates_mod_p": coordinates,
        "nonzero_tensor_coefficients_mod_p": nonzero_coefficients,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = ROOT / "tmp" / "p4_pure_rank_two_component_audit.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
