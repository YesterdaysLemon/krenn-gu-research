#!/usr/bin/env python3
"""Independent modular audit of the diagonal-quadric P4 component."""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass
from pathlib import Path


import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
THEOREM = HERE / "P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md"
PRIMARY = HERE / "verify_p4_diagonal_quadric_pure_component.py"
MODULI = (101, 103)
WORDS = tuple(itertools.product((0, 1), repeat=4))


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
            assert self.modulus == other.modulus
            assert len(self.gradient) == len(other.gradient)
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
            (-self.value) % self.modulus,
            tuple((-entry) % self.modulus for entry in self.gradient),
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
        inverse_value = pow(self.value, -1, self.modulus)
        scale = -inverse_value * inverse_value
        return Dual(
            inverse_value,
            tuple(
                scale * entry % self.modulus for entry in self.gradient
            ),
            self.modulus,
        )

    def __truediv__(self, other: int | "Dual") -> "Dual":
        return self * self.lift(other).inverse()

    def __rtruediv__(self, other: int | "Dual") -> "Dual":
        return self.lift(other) * self.inverse()


@dataclass(frozen=True)
class Jet:
    coefficients: tuple[int, int, int]
    modulus: int

    @staticmethod
    def affine(value: int, tangent: int, modulus: int) -> "Jet":
        return Jet((value % modulus, tangent % modulus, 0), modulus)

    def lift(self, other: int | "Jet") -> "Jet":
        if isinstance(other, Jet):
            assert self.modulus == other.modulus
            return other
        return Jet((other % self.modulus, 0, 0), self.modulus)

    def __add__(self, other: int | "Jet") -> "Jet":
        other = self.lift(other)
        return Jet(
            tuple(
                (left + right) % self.modulus
                for left, right in zip(
                    self.coefficients, other.coefficients, strict=True
                )
            ),
            self.modulus,
        )

    __radd__ = __add__

    def __neg__(self) -> "Jet":
        return Jet(
            tuple((-entry) % self.modulus for entry in self.coefficients),
            self.modulus,
        )

    def __sub__(self, other: int | "Jet") -> "Jet":
        return self + (-self.lift(other))

    def __rsub__(self, other: int | "Jet") -> "Jet":
        return self.lift(other) - self

    def __mul__(self, other: int | "Jet") -> "Jet":
        other = self.lift(other)
        result = [0, 0, 0]
        for left_degree, left in enumerate(self.coefficients):
            for right_degree, right in enumerate(other.coefficients):
                degree = left_degree + right_degree
                if degree <= 2:
                    result[degree] += left * right
        return Jet(
            tuple(entry % self.modulus for entry in result),
            self.modulus,
        )

    __rmul__ = __mul__


def permanent_dp_mod(rows: list[list[int]], modulus: int) -> int:
    table = {0: 1}
    for row in rows:
        next_table: dict[int, int] = {}
        for mask, subtotal in table.items():
            for column in range(4):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_table[new_mask] = (
                    next_table.get(new_mask, 0)
                    + subtotal * row[column]
                ) % modulus
        table = next_table
    return table[15]


def permanent_dp_generic(rows):
    table = {0: 1}
    for row in rows:
        next_table = {}
        for mask, subtotal in table.items():
            for column in range(4):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_table[new_mask] = (
                    next_table.get(new_mask, 0)
                    + subtotal * row[column]
                )
        table = next_table
    return table[15]


def matrix_rank_mod(matrix: list[list[int]], modulus: int) -> int:
    if not matrix:
        return 0
    work = [[entry % modulus for entry in row] for row in matrix]
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
        inverse = pow(work[rank][column], -1, modulus)
        work[rank] = [
            entry * inverse % modulus for entry in work[rank]
        ]
        for row in range(len(work)):
            if row == rank:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    (entry - scale * pivot_entry) % modulus
                    for entry, pivot_entry in zip(
                        work[row], work[rank], strict=True
                    )
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def determinant_mod(matrix: list[list[int]], modulus: int) -> int:
    work = [[entry % modulus for entry in row] for row in matrix]
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
        determinant = determinant * pivot_value % modulus
        inverse = pow(pivot_value, -1, modulus)
        for row in range(column + 1, len(work)):
            scale = work[row][column] * inverse % modulus
            if not scale:
                continue
            work[row] = [
                (entry - scale * pivot_entry) % modulus
                for entry, pivot_entry in zip(
                    work[row], work[column], strict=True
                )
            ]
    return determinant % modulus


def nullspace_mod(matrix: list[list[int]], modulus: int) -> list[list[int]]:
    work = [[entry % modulus for entry in row] for row in matrix]
    row = 0
    pivots: list[int] = []
    for column in range(len(work[0])):
        pivot = next(
            (
                candidate
                for candidate in range(row, len(work))
                if work[candidate][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = pow(work[row][column], -1, modulus)
        work[row] = [entry * inverse % modulus for entry in work[row]]
        for other in range(len(work)):
            if other == row:
                continue
            scale = work[other][column]
            if scale:
                work[other] = [
                    (entry - scale * pivot_entry) % modulus
                    for entry, pivot_entry in zip(
                        work[other], work[row], strict=True
                    )
                ]
        pivots.append(column)
        row += 1
        if row == len(work):
            break
    free = [
        column for column in range(len(work[0])) if column not in pivots
    ]
    basis = []
    for free_column in free:
        vector = [0] * len(work[0])
        vector[free_column] = 1
        for pivot_row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -work[pivot_row][free_column] % modulus
        basis.append(vector)
    return basis


def normal_form_mod(
    parameters: tuple[int, int, int, int, int, int], modulus: int
) -> tuple[list[list[int]], ...]:
    A, B, C, E, F, H = (entry % modulus for entry in parameters)
    return (
        [[E, -F, -F, -E], [A, -B, B, A]],
        [[1, 0, 0, -1], [A, C + B, C - B, A]],
        [[H + E, F, F, H - E], [0, 1, -1, 0]],
        [[1, 0, 0, 1], [0, 1, 1, 0]],
    )


def coefficients_mod(
    planes: tuple[list[list[int]], ...], modulus: int
) -> dict[tuple[int, ...], int]:
    return {
        word: permanent_dp_mod(
            [planes[mode][word[mode]] for mode in range(4)],
            modulus,
        )
        for word in WORDS
    }


def psi_mod(
    parameters: tuple[int, int, int, int, int, int], modulus: int
) -> int:
    A, B, C, E, F, H = parameters
    return (
        A**3 * F**3
        + A**2 * C * F**2 * H
        - A * B**2 * F * H**2
        - A * C**2 * E**2 * F
        + A * C**2 * F * H**2
        - B**2 * C * E**2 * H
    ) % modulus


def row_reduce_01_mod(matrix: list[list[int]], modulus: int) -> list[list[int]]:
    a, b = matrix[0][0] % modulus, matrix[0][1] % modulus
    c, d = matrix[1][0] % modulus, matrix[1][1] % modulus
    determinant = (a * d - b * c) % modulus
    inverse = pow(determinant, -1, modulus)
    left = (
        (d * inverse % modulus, -b * inverse % modulus),
        (-c * inverse % modulus, a * inverse % modulus),
    )
    return [
        [
            sum(left[row][inner] * matrix[inner][column] for inner in range(2))
            % modulus
            for column in range(4)
        ]
        for row in range(2)
    ]


def row_reduce_01_dual(matrix: list[list[Dual]]) -> list[list[Dual]]:
    a, b = matrix[0][0], matrix[0][1]
    c, d = matrix[1][0], matrix[1][1]
    inverse_det = (a * d - b * c).inverse()
    left = (
        (d * inverse_det, -b * inverse_det),
        (-c * inverse_det, a * inverse_det),
    )
    return [
        [
            sum(
                (left[row][inner] * matrix[inner][column] for inner in range(2)),
                Dual.constant(0, len(a.gradient), a.modulus),
            )
            for column in range(4)
        ]
        for row in range(2)
    ]


def diagonal_quadric_dimension_mod(
    plane: list[list[int]], modulus: int
) -> int:
    line = nullspace_mod(plane, modulus)
    assert len(line) == 2
    first, second = line
    restriction = [
        [first[index] * first[index] % modulus for index in range(4)],
        [
            2 * first[index] * second[index] % modulus
            for index in range(4)
        ],
        [second[index] * second[index] % modulus for index in range(4)],
    ]
    return 4 - matrix_rank_mod(restriction, modulus)


def audit_modulus(modulus: int) -> dict:
    coefficient_checks = 0
    for parameters in (
        (2, 3, 5, 7, 11, 13),
        (1, 1, 0, 2, 1, 1),
    ):
        A, B, C, E, F, H = parameters
        planes = normal_form_mod(parameters, modulus)
        actual = coefficients_mod(planes, modulus)
        expected = {
            (0, 1, 0, 0): -4 * F * (A * F + C * H),
            (0, 1, 0, 1): -4 * (A * F * H + C * E**2),
            (1, 1, 0, 0): 4 * (A * C * F + B**2 * H),
            (1, 1, 0, 1): 4 * A * (A * F + C * H),
        }
        assert all(
            actual[word] == expected.get(word, 0) % modulus for word in WORDS
        )
        active = [
            [actual[(0, 1, 0, 0)], actual[(0, 1, 0, 1)]],
            [actual[(1, 1, 0, 0)], actual[(1, 1, 0, 1)]],
        ]
        assert determinant_mod(active, modulus) == (
            -16 * psi_mod(parameters, modulus)
        ) % modulus
        coefficient_checks += len(WORDS)

    point_planes = normal_form_mod((1, 1, 0, 2, 1, 1), modulus)
    point_reduced = tuple(
        row_reduce_01_mod(plane, modulus) for plane in point_planes
    )
    point_chart = tuple(
        entry
        for plane in point_reduced
        for entry in (plane[0][2], plane[0][3], plane[1][2], plane[1][3])
    )
    inv3 = pow(3, -1, modulus)
    expected_chart = (
        -2,
        -3,
        -3,
        -4,
        0,
        -1,
        -1,
        2,
        2 * inv3,
        -inv3,
        -1,
        0,
        0,
        1,
        1,
        0,
    )
    assert point_chart == tuple(entry % modulus for entry in expected_chart)
    point = (*point_chart, 3 * pow(2, -1, modulus) % modulus, 0, 0, 1)

    dimension = 20
    variables = [
        Dual.variable(value, index, dimension, modulus)
        for index, value in enumerate(point)
    ]
    chart_planes = []
    for mode in range(4):
        a, b, c, d = variables[4 * mode : 4 * mode + 4]
        chart_planes.append(((1, 0, a, b), (0, 1, c, d)))
    tensor = {
        word: permanent_dp_generic(
            [list(chart_planes[mode][word[mode]]) for mode in range(4)]
        )
        for word in WORDS
    }
    anchor = (0, 1, 0, 0)
    z = variables[16:]
    equations: list[Dual] = []
    equation_words = []
    for word in WORDS:
        if word == anchor:
            continue
        ratio = Dual.constant(1, dimension, modulus)
        for mode in range(4):
            if word[mode] != anchor[mode]:
                ratio *= z[mode]
        equations.append(tensor[word] - tensor[anchor] * ratio)
        equation_words.append(word)
    assert all(equation.value == 0 for equation in equations)
    jacobian = [list(equation.gradient) for equation in equations]
    assert matrix_rank_mod(jacobian, modulus) == 14
    minor_rows = (0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14)
    minor_columns = (0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 15, 17, 18)
    minor = [
        [jacobian[row][column] for column in minor_columns]
        for row in minor_rows
    ]
    expected_minor = 1048576 * pow(243, -1, modulus) % modulus
    assert determinant_mod(minor, modulus) == expected_minor

    tangent = (
        15,
        21,
        21,
        33,
        -11,
        11,
        15,
        -21,
        4,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    cokernel = (9, 0, 6, 0, 0, 0, 0, -6, 0, -4, 0, 0, 0, 0, 0)
    assert all(
        sum(row[column] * tangent[column] for column in range(20))
        % modulus
        == 0
        for row in jacobian
    )
    assert all(
        sum(cokernel[row] * jacobian[row][column] for row in range(15))
        % modulus
        == 0
        for column in range(20)
    )

    jet_variables = [
        Jet.affine(value, tangent[index], modulus)
        for index, value in enumerate(point)
    ]
    jet_planes = []
    for mode in range(4):
        a, b, c, d = jet_variables[4 * mode : 4 * mode + 4]
        jet_planes.append(((1, 0, a, b), (0, 1, c, d)))
    jet_tensor = {
        word: permanent_dp_generic(
            [list(jet_planes[mode][word[mode]]) for mode in range(4)]
        )
        for word in WORDS
    }
    jet_z = jet_variables[16:]
    quadratic_terms = []
    for word in WORDS:
        if word == anchor:
            continue
        ratio = Jet.affine(1, 0, modulus)
        for mode in range(4):
            if word[mode] != anchor[mode]:
                ratio *= jet_z[mode]
        equation = jet_tensor[word] - jet_tensor[anchor] * ratio
        assert equation.coefficients[0] == 0
        assert equation.coefficients[1] == 0
        quadratic_terms.append(equation.coefficients[2])
    quadratic_obstruction = sum(
        coefficient * term
        for coefficient, term in zip(
            cokernel, quadratic_terms, strict=True
        )
    ) % modulus
    assert quadratic_obstruction == -132 % modulus

    # Independent dual-number reconstruction of the family tangent minor.
    family_dimension = 5
    A = Dual.variable(1, 0, family_dimension, modulus)
    C = Dual.variable(0, 1, family_dimension, modulus)
    E = Dual.variable(2, 2, family_dimension, modulus)
    t0 = Dual.variable(1, 3, family_dimension, modulus)
    t1 = Dual.variable(1, 4, family_dimension, modulus)
    half = pow(2, -1, modulus)
    H = Dual(
        1,
        (1, -3 * half % modulus, 0, 0, 0),
        modulus,
    )
    one = Dual.constant(1, family_dimension, modulus)
    zero = Dual.constant(0, family_dimension, modulus)
    raw_family = (
        [[E, -one, -one, -E], [A, -one, one, A]],
        [[one, zero, zero, -one], [A, C + one, C - one, A]],
        [[H + E, one, one, H - E], [zero, one, -one, zero]],
        [[one, zero, zero, one], [zero, one, one, zero]],
    )
    scales = (t0, t1, one, one)
    scaled_family = tuple(
        [
            [row[column] * scales[column] for column in range(4)]
            for row in plane
        ]
        for plane in raw_family
    )
    reduced_family = tuple(
        row_reduce_01_dual(plane) for plane in scaled_family
    )
    family_coordinates = [
        entry
        for plane in reduced_family
        for entry in (plane[0][2], plane[0][3], plane[1][2], plane[1][3])
    ]
    tangent_rows = (0, 1, 2, 3, 6)
    family_minor = [
        list(family_coordinates[row].gradient) for row in tangent_rows
    ]
    assert determinant_mod(family_minor, modulus) == -24 % modulus

    new_dimensions = tuple(
        diagonal_quadric_dimension_mod(plane, modulus)
        for plane in point_planes
    )
    assert new_dimensions == (1, 1, 1, 2)

    # A generic point of the old chart retains three block-line planes.
    a, d, e, h, n = (2, 3, 5, 7, 11)
    D = (d + h * n * e) % modulus
    known_planes = (
        [
            [1, 0, a, h * (a - n)],
            [0, 1, D * pow(h, -1, modulus), d],
        ],
        [[e, 1, 0, 0], [0, 0, 1, h]],
        [[0, 1, 0, h * n * e], [-pow(n, -1, modulus), 0, 1, 0]],
        [[1, 0, n, 0], [0, 0, -pow(h, -1, modulus), 1]],
    )
    known_dimensions = tuple(
        diagonal_quadric_dimension_mod(plane, modulus)
        for plane in known_planes[1:]
    )
    assert all(dimension >= 2 for dimension in known_dimensions)

    return {
        "modulus": modulus,
        "normal_form_coefficient_checks": coefficient_checks,
        "incidence_jacobian_rank": 14,
        "incidence_minor_determinant": expected_minor,
        "quadratic_tangent_obstruction": quadratic_obstruction,
        "family_tangent_minor_determinant": -24 % modulus,
        "new_point_diagonal_quadric_dimensions": list(new_dimensions),
        "known_component_block_dimensions": list(known_dimensions),
    }


def main() -> None:
    audits = [audit_modulus(modulus) for modulus in MODULI]
    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": (
            "DP permanent, modular dual numbers, second-order jets, "
            "and diagonal-quadric rank"
        ),
        "moduli": list(MODULI),
        "audits": audits,
        "component_certificate_replayed": True,
        "distinct_component_invariant_replayed": True,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = REPO_ROOT / "tmp" / "p4_diagonal_quadric_pure_component_audit.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
