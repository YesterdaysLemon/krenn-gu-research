#!/usr/bin/env python3
"""Independent modular audit of the embedded-P3 pure-P4 component."""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_EMBEDDED_P3_PURE_COMPONENT.md"
PRIMARY = ROOT / "verify_p4_embedded_p3_pure_component.py"
MODULI = (101, 103)
WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = ((0, 1), (1, 2), (1, 2), (1, 2))
ANCHOR = (0, 0, 1, 0)
MINOR_ROWS = tuple(range(14))
MINOR_COLUMNS = (
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    16,
    18,
    19,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Dual:
    value: int
    gradient: tuple[int, ...]
    modulus: int

    @staticmethod
    def constant(value: int, dimension: int, modulus: int) -> "Dual":
        return Dual(value % modulus, (0,) * dimension, modulus)

    @staticmethod
    def variable(
        value: int, index: int, dimension: int, modulus: int
    ) -> "Dual":
        gradient = [0] * dimension
        gradient[index] = 1
        return Dual(value % modulus, tuple(gradient), modulus)

    def lift(self, other: int | "Dual") -> "Dual":
        if isinstance(other, Dual):
            return other
        return Dual.constant(other, len(self.gradient), self.modulus)

    def __add__(self, other: int | "Dual") -> "Dual":
        other = self.lift(other)
        return Dual(
            (self.value + other.value) % self.modulus,
            tuple(
                (left + right) % self.modulus
                for left, right in zip(
                    self.gradient, other.gradient, strict=True
                )
            ),
            self.modulus,
        )

    __radd__ = __add__

    def __neg__(self) -> "Dual":
        return Dual(
            -self.value % self.modulus,
            tuple(-entry % self.modulus for entry in self.gradient),
            self.modulus,
        )

    def __sub__(self, other: int | "Dual") -> "Dual":
        return self + (-self.lift(other))

    def __rsub__(self, other: int | "Dual") -> "Dual":
        return self.lift(other) - self

    def __mul__(self, other: int | "Dual") -> "Dual":
        other = self.lift(other)
        return Dual(
            self.value * other.value % self.modulus,
            tuple(
                (
                    self.value * right
                    + other.value * left
                )
                % self.modulus
                for left, right in zip(
                    self.gradient, other.gradient, strict=True
                )
            ),
            self.modulus,
        )

    __rmul__ = __mul__

    def inverse(self) -> "Dual":
        inverse = pow(self.value, -1, self.modulus)
        return Dual(
            inverse,
            tuple(
                -entry * inverse * inverse % self.modulus
                for entry in self.gradient
            ),
            self.modulus,
        )

    def __truediv__(self, other: int | "Dual") -> "Dual":
        return self * self.lift(other).inverse()

    def __rtruediv__(self, other: int | "Dual") -> "Dual":
        return self.lift(other) * self.inverse()


def rational(numerator: int, denominator: int, modulus: int) -> int:
    return numerator * pow(denominator, -1, modulus) % modulus


def permanent_dp(rows, modulus: int):
    dimension = (
        len(rows[0][0].gradient)
        if isinstance(rows[0][0], Dual)
        else 0
    )
    zero = Dual.constant(0, dimension, modulus) if dimension else 0
    one = Dual.constant(1, dimension, modulus) if dimension else 1
    values = [zero] * 16
    values[0] = one
    for row in rows:
        updated = [zero] * 16
        for mask, value in enumerate(values):
            for column in range(4):
                bit = 1 << column
                if mask & bit == 0:
                    updated[mask | bit] = (
                        updated[mask | bit] + value * row[column]
                    )
        values = updated
    return values[15]


def tensor(planes, modulus: int):
    return {
        word: permanent_dp(
            tuple(planes[mode][word[mode]] for mode in range(4)),
            modulus,
        )
        for word in WORDS
    }


def chart_planes(variables, modulus: int):
    dimension = len(variables[0].gradient)
    zero = Dual.constant(0, dimension, modulus)
    one = Dual.constant(1, dimension, modulus)
    result = []
    for mode, pivots in enumerate(PIVOTS):
        nonpivots = tuple(index for index in range(4) if index not in pivots)
        plane = [[zero for _ in range(4)] for _ in range(2)]
        plane[0][pivots[0]] = one
        plane[1][pivots[1]] = one
        entries = variables[4 * mode : 4 * mode + 4]
        for row in range(2):
            for offset, column in enumerate(nonpivots):
                plane[row][column] = entries[2 * row + offset]
        result.append(tuple(tuple(row) for row in plane))
    return tuple(result)


def family_coordinates(parameters):
    r, s, t, u, cap_a, cap_b = parameters
    return (
        r,
        t,
        s,
        u,
        0,
        -1 / cap_b,
        0,
        -cap_a / cap_b,
        0,
        1 / cap_b,
        0,
        -cap_a / cap_b,
        0,
        -1 / cap_b,
        0,
        cap_a / cap_b,
    )


def rank_mod(matrix: list[list[int]], modulus: int) -> int:
    work = [[entry % modulus for entry in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, modulus)
        work[pivot_row] = [
            value * inverse % modulus for value in work[pivot_row]
        ]
        for row in range(len(work)):
            if row != pivot_row and work[row][column]:
                scale = work[row][column]
                work[row] = [
                    (left - scale * right) % modulus
                    for left, right in zip(
                        work[row], work[pivot_row], strict=True
                    )
                ]
        pivot_row += 1
    return pivot_row


def determinant_mod(matrix: list[list[int]], modulus: int) -> int:
    work = [[entry % modulus for entry in row] for row in matrix]
    result = 1
    for column in range(len(work)):
        pivot = next(
            row
            for row in range(column, len(work))
            if work[row][column]
        )
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        pivot_value = work[column][column]
        result = result * pivot_value % modulus
        inverse = pow(pivot_value, -1, modulus)
        for row in range(column + 1, len(work)):
            scale = work[row][column] * inverse % modulus
            for offset in range(column, len(work)):
                work[row][offset] = (
                    work[row][offset] - scale * work[column][offset]
                ) % modulus
    return result % modulus


def pair_profile(planes, modulus: int) -> tuple[int, ...]:
    result = []
    for left, right in PAIRS:
        columns = []
        for left_row in range(2):
            for right_row in range(2):
                columns.append(
                    tuple(
                        (
                            planes[left][left_row][first]
                            * planes[right][right_row][second]
                            + planes[left][left_row][second]
                            * planes[right][right_row][first]
                        )
                        % modulus
                        for first, second in PAIRS
                    )
                )
        matrix = [
            [columns[column][row] for column in range(4)]
            for row in range(6)
        ]
        result.append(rank_mod(matrix, modulus))
    return tuple(result)


def audit_modulus(modulus: int) -> dict[str, object]:
    sample = (
        rational(3, 2, modulus),
        rational(1, 2, modulus),
        1,
        2,
        2,
        3,
    )
    parameter_duals = tuple(
        Dual.variable(value, index, 6, modulus)
        for index, value in enumerate(sample)
    )
    family_dual_coordinates = family_coordinates(parameter_duals)
    family_jacobian = [
        list(value.gradient)
        if isinstance(value, Dual)
        else [0] * 6
        for value in family_dual_coordinates
    ]
    assert rank_mod(family_jacobian, modulus) == 6
    family_minor = [
        family_jacobian[row] for row in (0, 1, 2, 3, 5, 7)
    ]
    expected_family_minor = -pow(3, -3, modulus) % modulus
    assert determinant_mod(family_minor, modulus) == expected_family_minor

    chart_values = tuple(
        value.value if isinstance(value, Dual) else value % modulus
        for value in family_dual_coordinates
    )
    target_values = (0, 2, 0, 0)
    all_values = chart_values + target_values
    variables = tuple(
        Dual.variable(value, index, 20, modulus)
        for index, value in enumerate(all_values)
    )
    planes = chart_planes(variables[:16], modulus)
    restricted = tensor(planes, modulus)
    target_variables = variables[16:]

    equations = []
    for word in WORDS:
        if word == ANCHOR:
            continue
        product = Dual.constant(1, 20, modulus)
        for mode in range(4):
            if word[mode] != ANCHOR[mode]:
                product *= target_variables[mode]
        equations.append(restricted[word] - restricted[ANCHOR] * product)
    assert all(equation.value == 0 for equation in equations)

    jacobian = [list(equation.gradient) for equation in equations]
    assert rank_mod(jacobian, modulus) == 14
    selected = [
        [jacobian[row][column] for column in MINOR_COLUMNS]
        for row in MINOR_ROWS
    ]
    expected_incidence_minor = rational(114688, 2187, modulus)
    assert determinant_mod(selected, modulus) == expected_incidence_minor

    numeric_planes = tuple(
        tuple(
            tuple(entry.value for entry in row)
            for row in plane
        )
        for plane in planes
    )
    profile = pair_profile(numeric_planes, modulus)
    assert profile == (4, 4, 4, 2, 2, 2)

    numeric_tensor = {
        word: value.value for word, value in restricted.items()
    }
    nonzero = {
        "".join(map(str, word)): value
        for word, value in numeric_tensor.items()
        if value
    }
    assert nonzero == {
        "0010": -2 * pow(3, -1, modulus) % modulus,
        "0110": -4 * pow(3, -1, modulus) % modulus,
    }

    return {
        "modulus": modulus,
        "family_tangent_rank": 6,
        "family_minor": expected_family_minor,
        "incidence_rank": 14,
        "incidence_minor": expected_incidence_minor,
        "pair_profile": list(profile),
        "nonzero_tensor_entries": nonzero,
    }


def main() -> None:
    audits = [audit_modulus(modulus) for modulus in MODULI]
    result = {
        "verified": True,
        "scope": "independent one-point modular audit; no search",
        "method": "DP permanent, forward-mode dual numbers, and modular row reduction",
        "moduli": list(MODULI),
        "audits": audits,
        "dependencies": {
            THEOREM.name: sha256(THEOREM),
            PRIMARY.name: sha256(PRIMARY),
        },
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
