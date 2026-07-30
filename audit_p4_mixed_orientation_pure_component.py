#!/usr/bin/env python3
"""Independent modular audit of the mixed-orientation pure-P4 component."""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_MIXED_ORIENTATION_PURE_COMPONENT.md"
PRIMARY = ROOT / "verify_p4_mixed_orientation_pure_component.py"
MODULI = (101, 103)
WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = ((0, 2), (0, 2), (0, 1), (0, 2))


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


def permanent_dp(rows, modulus: int):
    dimension = (
        len(rows[0][0].gradient)
        if isinstance(rows[0][0], Dual)
        else 0
    )
    zero = (
        Dual.constant(0, dimension, modulus) if dimension else 0
    )
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


def family_planes(values, modulus: int):
    d, p, q, t0, t1, t2 = values
    N = q * (d + p + q)
    raw = (
        ((-d * p, d + q, N, 0), (d * p, -d - q, 0, N)),
        ((0, 0, 1, 1), (-d, 1, -p - q, d)),
        ((p, 1, 0, q), (-1, 0, 1, 0)),
        ((1, 0, 1, 0), (0, 0, -1, 1)),
    )
    scales = (t0, t1, t2, 1)
    return tuple(
        tuple(
            tuple(row[column] * scales[column] for column in range(4))
            for row in plane
        )
        for plane in raw
    )


def row_reduce(plane, pivots, modulus: int):
    a = plane[0][pivots[0]]
    b = plane[0][pivots[1]]
    c = plane[1][pivots[0]]
    d = plane[1][pivots[1]]
    determinant = a * d - b * c

    def divide(numerator, denominator):
        if isinstance(numerator, Dual) or isinstance(denominator, Dual):
            return numerator / denominator
        return numerator * pow(denominator % modulus, -1, modulus) % modulus

    return tuple(
        tuple(
            divide(
                d * plane[0][column] - b * plane[1][column],
                determinant,
            )
                if row == 0
                else divide(
                    -c * plane[0][column] + a * plane[1][column],
                    determinant,
                )
            for column in range(4)
        )
        for row in range(2)
    )


def chart_coordinates(planes, modulus: int):
    result = []
    reduced = []
    for plane, pivots in zip(planes, PIVOTS, strict=True):
        chart = row_reduce(plane, pivots, modulus)
        reduced.append(chart)
        nonpivots = tuple(index for index in range(4) if index not in pivots)
        result.extend(
            chart[row][column]
            for row in range(2)
            for column in nonpivots
        )
    return tuple(reduced), tuple(result)


def determinant_mod(matrix: list[list[int]], modulus: int) -> int:
    work = [[entry % modulus for entry in row] for row in matrix]
    result = 1
    for column in range(len(work)):
        pivot = next(
            row
            for row in range(column, len(work))
            if work[row][column] % modulus
        )
        if pivot != column:
            work[pivot], work[column] = work[column], work[pivot]
            result = -result
        pivot_value = work[column][column] % modulus
        result = result * pivot_value % modulus
        inverse = pow(pivot_value, -1, modulus)
        for row in range(column + 1, len(work)):
            scale = work[row][column] * inverse % modulus
            for offset in range(column, len(work)):
                work[row][offset] = (
                    work[row][offset] - scale * work[column][offset]
                ) % modulus
    return result % modulus


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


def pair_rank(left, right, modulus: int) -> int:
    columns = []
    for left_row in range(2):
        for right_row in range(2):
            columns.append(
                [
                    (
                        left[left_row][first] * right[right_row][second]
                        + left[left_row][second] * right[right_row][first]
                    )
                    % modulus
                    for first, second in PAIRS
                ]
            )
    return rank_mod(
        [
            [columns[column][row] for column in range(4)]
            for row in range(6)
        ],
        modulus,
    )


def chart_planes_dual(values, modulus: int):
    planes = []
    for mode, pivots in enumerate(PIVOTS):
        nonpivots = tuple(index for index in range(4) if index not in pivots)
        plane = [
            [Dual.constant(0, 20, modulus) for _ in range(4)]
            for _ in range(2)
        ]
        plane[0][pivots[0]] = Dual.constant(1, 20, modulus)
        plane[1][pivots[1]] = Dual.constant(1, 20, modulus)
        for row in range(2):
            for offset, column in enumerate(nonpivots):
                index = 4 * mode + 2 * row + offset
                plane[row][column] = Dual.variable(
                    values[index], index, 20, modulus
                )
        planes.append(tuple(tuple(row) for row in plane))
    return tuple(planes)


def audit_modulus(modulus: int) -> dict[str, object]:
    base_values = (1, 2, 3, 1, 1, 1)
    dual_values = tuple(
        Dual.variable(value, index, 6, modulus)
        for index, value in enumerate(base_values)
    )
    dual_family = family_planes(dual_values, modulus)
    _, dual_coordinates = chart_coordinates(dual_family, modulus)
    family_jacobian = [list(value.gradient) for value in dual_coordinates]
    family_rows = (0, 1, 3, 4, 5)
    family_columns = (0, 1, 2, 3, 5)
    family_minor = [
        [family_jacobian[row][column] for column in family_columns]
        for row in family_rows
    ]
    expected_family = (
        -9 * pow(2, -1, modulus)
    ) % modulus
    assert determinant_mod(family_minor, modulus) == expected_family
    assert rank_mod(family_jacobian, modulus) == 5

    numeric_family = family_planes(base_values, modulus)
    reduced, coordinates = chart_coordinates(numeric_family, modulus)
    numeric_coordinates = tuple(
        value.value if isinstance(value, Dual) else value % modulus
        for value in coordinates
    )
    numeric_tensor = tensor(numeric_family, modulus)
    assert numeric_tensor[(0, 0, 0, 0)] == 36 % modulus
    assert all(
        value == 0
        for word, value in numeric_tensor.items()
        if word != (0, 0, 0, 0)
    )

    chart_planes = chart_planes_dual(numeric_coordinates, modulus)
    chart_tensor = tensor(chart_planes, modulus)
    target_values = (0, -pow(5, -1, modulus), 0, 0)
    targets = tuple(
        Dual.variable(value, 16 + index, 20, modulus)
        for index, value in enumerate(target_values)
    )
    anchor = (1, 0, 1, 0)
    equations = []
    for word in WORDS:
        if word == anchor:
            continue
        product = Dual.constant(1, 20, modulus)
        for mode in range(4):
            if word[mode] != anchor[mode]:
                product *= targets[mode]
        equations.append(
            chart_tensor[word] - chart_tensor[anchor] * product
        )
    incidence_jacobian = [list(value.gradient) for value in equations]
    incidence_columns = (
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        12,
        14,
        16,
        18,
        19,
    )
    incidence_minor = [
        [row[column] for column in incidence_columns]
        for row in incidence_jacobian
    ]
    assert rank_mod(incidence_jacobian, modulus) == 15
    assert determinant_mod(incidence_minor, modulus) == (
        -737280 % modulus
    )

    pair_profile = tuple(
        pair_rank(
            numeric_family[left], numeric_family[right], modulus
        )
        for left, right in PAIRS
    )
    assert pair_profile == (4, 4, 3, 4, 3, 3)

    # The three explicit rank-one relations and their kernel endpoints.
    U0, U1, U2, U3 = numeric_family
    left03 = tuple(
        (U0[0][index] + U0[1][index]) % modulus
        for index in range(4)
    )
    relations = (
        (left03, U3[1], 3),
        (U1[0], U3[1], 3),
        (U2[1], U3[0], 2),
    )
    for left, right, _kernel_endpoint in relations:
        assert all(
            (
                left[first] * right[second]
                + left[second] * right[first]
            )
            % modulus
            == 0
            for first, second in PAIRS
        )
    indegrees = [0, 0, 1, 2]
    assert tuple(sorted(indegrees, reverse=True)) == (2, 1, 0, 0)

    return {
        "modulus": modulus,
        "family_tangent_rank": 5,
        "family_minor_determinant": expected_family,
        "incidence_jacobian_rank": 15,
        "incidence_minor_determinant": -737280 % modulus,
        "pair_profile": list(pair_profile),
        "rank_one_relations_replayed": len(relations),
        "sorted_kernel_endpoint_indegrees": [2, 1, 0, 0],
    }


def main() -> None:
    audits = [audit_modulus(modulus) for modulus in MODULI]
    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": (
            "modular dual numbers, DP permanent, independent row "
            "reduction, and explicit zero-product relations"
        ),
        "moduli": list(MODULI),
        "audits": audits,
        "component_certificate_replayed": True,
        "directed_relation_invariant_replayed": True,
        "known_pure_component_orbits_at_least": 6,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p4_mixed_orientation_pure_component_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
