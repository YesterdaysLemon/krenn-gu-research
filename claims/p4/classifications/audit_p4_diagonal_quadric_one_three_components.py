#!/usr/bin/env python3
"""Independent modular audit of the three 1+3 pure-P4 components."""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

ROOT = HERE
THEOREM = HERE / "P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md"
PRIMARY = HERE / "verify_p4_diagonal_quadric_one_three_components.py"
MODULI = (101, 103)
WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = ((0, 2), (0, 1), (0, 1), (1, 2))


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
        other = self.lift(other)
        return self * other.inverse()

    def __rtruediv__(self, other: int | "Dual") -> "Dual":
        return self.lift(other) * self.inverse()


def permanent_dp(rows):
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


def coefficients_generic(planes):
    return {
        word: permanent_dp(
            [planes[mode][word[mode]] for mode in range(4)]
        )
        for word in WORDS
    }


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
    assert matrix and len(matrix) == len(matrix[0])
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
            if scale:
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
    pivots = []
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


def raw_planes_generic(S, D, G, T):
    P = G - T
    Q = D - S
    return (
        [[2, P + Q, Q - P, 0], [0, 0, 1, 1]],
        [[0, 1, -1, 0], [1, 0, S, D]],
        [[1, 0, G, T], [0, 1, 0, -1]],
        [[0, 1, 1, 0], [0, 1, 0, 1]],
    )


def branch_planes_generic(branch: str, S, D, G, scales=(1, 1, 1)):
    T = {
        "L1": -D + G + S,
        "L2": D + G - S,
        "L3": -D - G - S,
    }[branch]
    raw = raw_planes_generic(S, D, G, T)
    all_scales = (*scales, 1)
    return tuple(
        [
            [
                row[column] * all_scales[column]
                for column in range(4)
            ]
            for row in plane
        ]
        for plane in raw
    )


def row_reduce_numeric(plane, pivots, modulus: int):
    a = plane[0][pivots[0]] % modulus
    b = plane[0][pivots[1]] % modulus
    c = plane[1][pivots[0]] % modulus
    d = plane[1][pivots[1]] % modulus
    inverse_det = pow((a * d - b * c) % modulus, -1, modulus)
    left = (
        (d * inverse_det % modulus, -b * inverse_det % modulus),
        (-c * inverse_det % modulus, a * inverse_det % modulus),
    )
    return [
        [
            sum(
                left[row][inner] * plane[inner][column]
                for inner in range(2)
            )
            % modulus
            for column in range(4)
        ]
        for row in range(2)
    ]


def row_reduce_dual(plane, pivots):
    a = plane[0][pivots[0]]
    b = plane[0][pivots[1]]
    c = plane[1][pivots[0]]
    d = plane[1][pivots[1]]
    inverse_det = (a * d - b * c).inverse()
    left = (
        (d * inverse_det, -b * inverse_det),
        (-c * inverse_det, a * inverse_det),
    )
    zero = Dual.constant(0, len(a.gradient), a.modulus)
    return [
        [
            sum(
                (
                    left[row][inner] * plane[inner][column]
                    for inner in range(2)
                ),
                zero,
            )
            for column in range(4)
        ]
        for row in range(2)
    ]


def chart_coordinates_generic(planes):
    coordinates = []
    for plane, pivots in zip(planes, PIVOTS, strict=True):
        nonpivots = tuple(index for index in range(4) if index not in pivots)
        coordinates.extend(
            plane[row][column]
            for row in range(2)
            for column in nonpivots
        )
    return tuple(coordinates)


def chart_planes_generic(variables):
    planes = []
    for mode, pivots in enumerate(PIVOTS):
        nonpivots = tuple(index for index in range(4) if index not in pivots)
        zero = variables[0] * 0
        one = zero + 1
        plane = [[zero for _ in range(4)] for _ in range(2)]
        plane[0][pivots[0]] = one
        plane[1][pivots[1]] = one
        entries = variables[4 * mode : 4 * mode + 4]
        for row in range(2):
            for offset, column in enumerate(nonpivots):
                plane[row][column] = entries[2 * row + offset]
        planes.append(plane)
    return tuple(planes)


def diagonal_jump_signature_mod(planes, modulus: int) -> tuple[int, int]:
    two_two = 0
    one_three = 0
    for plane in planes:
        line = nullspace_mod(plane, modulus)
        assert len(line) == 2
        first, second = line
        restriction = [
            [first[index] ** 2 % modulus for index in range(4)],
            [
                2 * first[index] * second[index] % modulus
                for index in range(4)
            ],
            [second[index] ** 2 % modulus for index in range(4)],
        ]
        quadrics = nullspace_mod(restriction, modulus)
        if len(quadrics) == 1:
            continue
        assert len(quadrics) == 2
        in_coordinate_hyperplane = any(
            all(vector[index] == 0 for vector in quadrics)
            for index in range(4)
        )
        if in_coordinate_hyperplane:
            one_three += 1
        else:
            two_two += 1
    return two_two, one_three


def pair_profile_mod(planes, modulus: int) -> tuple[int, ...]:
    squarefree_pairs = tuple(itertools.combinations(range(4), 2))
    profile = []
    for left_mode, right_mode in PAIRS:
        products = []
        for left_row in range(2):
            for right_row in range(2):
                products.append(
                    [
                        (
                            planes[left_mode][left_row][i]
                            * planes[right_mode][right_row][j]
                            + planes[left_mode][left_row][j]
                            * planes[right_mode][right_row][i]
                        )
                        % modulus
                        for i, j in squarefree_pairs
                    ]
                )
        profile.append(matrix_rank_mod(products, modulus))
    return tuple(profile)


def known_samples_mod(modulus: int):
    a, d, e, h, n = (2, 3, 5, 7, 11)
    cap_d = (d + h * n * e) % modulus
    first = (
        [
            [1, 0, a, h * (a - n)],
            [0, 1, cap_d * pow(h, -1, modulus), d],
        ],
        [[e, 1, 0, 0], [0, 0, 1, h]],
        [
            [0, 1, 0, h * n * e],
            [-pow(n, -1, modulus), 0, 1, 0],
        ],
        [[1, 0, n, 0], [0, 0, -pow(h, -1, modulus), 1]],
    )
    second = (
        [[2, -1, -1, -2], [1, -1, 1, 1]],
        [[1, 0, 0, -1], [1, 1, -1, 1]],
        [[3, 1, 1, -1], [0, 1, -1, 0]],
        [[1, 0, 0, 1], [0, 1, 1, 0]],
    )
    return first, second


def audit_modulus(modulus: int) -> dict:
    # Independently replay the cubic line-to-diagonal-quadric map.
    r = (2, 3, 5, 7)
    s = (11, 13, 17, 19)
    plucker = {
        (i, j): (r[i] * s[j] - r[j] * s[i]) % modulus
        for i, j in PAIRS
    }
    restriction = [
        [r[index] ** 2 % modulus for index in range(4)],
        [2 * r[index] * s[index] % modulus for index in range(4)],
        [s[index] ** 2 % modulus for index in range(4)],
    ]
    diagonal = []
    for omitted in range(4):
        complement = tuple(index for index in range(4) if index != omitted)
        product = 1
        for pair in itertools.combinations(complement, 2):
            product = product * plucker[tuple(sorted(pair))] % modulus
        diagonal.append((-1) ** omitted * product % modulus)
        minor = [
            [restriction[row][column] for column in complement]
            for row in range(3)
        ]
        assert (
            (-1) ** omitted * determinant_mod(minor, modulus)
            - 2 * diagonal[-1]
        ) % modulus == 0
    assert all(
        sum(restriction[row][column] * diagonal[column] for column in range(4))
        % modulus
        == 0
        for row in range(3)
    )

    # Double contraction via the independent DP permanent.
    standard = [
        [int(row == column) for column in range(4)] for row in range(4)
    ]
    y1 = [0, 1, -1, 0]
    y2 = [0, 1, 0, -1]
    double = [
        [
            permanent_dp([standard[row], y1, y2, standard[column]])
            % modulus
            for column in range(4)
        ]
        for row in range(4)
    ]
    expected_double = [
        [0, 1, -1, -1],
        [1, 0, 0, 0],
        [-1, 0, 0, 0],
        [-1, 0, 0, 0],
    ]
    assert double == [
        [entry % modulus for entry in row] for row in expected_double
    ]
    assert matrix_rank_mod(double, modulus) == 2

    # Raw coefficient formula and split active determinant.
    S0, D0, G0, T0 = (2, 3, 5, 7)
    raw = raw_planes_generic(S0, D0, G0, T0)
    tensor = {
        word: value % modulus
        for word, value in coefficients_generic(raw).items()
    }
    expected = {
        (0, 1, 0, 0): 2 * D0 * (D0 + G0 - S0 + T0),
        (0, 1, 0, 1): (
            D0**2
            + 2 * D0 * G0
            + 2 * D0 * T0
            + G0**2
            - 2 * G0 * T0
            - S0**2
            + T0**2
        ),
        (1, 1, 0, 0): D0 + G0 + S0 + T0,
        (1, 1, 0, 1): D0 + G0 + S0 + T0,
    }
    assert all(
        tensor[word] == expected.get(word, 0) % modulus for word in WORDS
    )
    active = [
        [tensor[(0, 1, 0, 0)], tensor[(0, 1, 0, 1)]],
        [tensor[(1, 1, 0, 0)], tensor[(1, 1, 0, 1)]],
    ]
    split = (
        (D0 - G0 - S0 + T0)
        * (D0 + G0 - S0 - T0)
        * (D0 + G0 + S0 + T0)
    )
    assert determinant_mod(active, modulus) == split % modulus

    samples = {"L1": (1, 3, 4), "L2": (1, 3, 4), "L3": (1, 2, 3)}
    family_certificates = {
        "L1": ((0, 3, 4, 5, 8), (0, 1, 2, 4, 5), -2),
        "L2": ((1, 3, 4, 6, 8), (0, 1, 2, 4, 5), -1),
        "L3": ((0, 1, 3, 4, 5), (0, 1, 2, 4, 5), 5),
    }
    incidence_columns = {
        "L1": (0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 14, 17, 18, 19),
        "L2": (0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 14, 17, 18, 19),
        "L3": (0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 14, 16, 17, 18),
    }
    incidence_determinants = {
        "L1": 163840,
        "L2": 6193152,
        "L3": -737280,
    }
    expected_signatures = {
        "known_first": (2, 1),
        "known_second": (1, 0),
        "L1": (1, 1),
        "L2": (0, 2),
        "L3": (0, 1),
    }
    branch_audits = {}
    numeric_branches = {}
    for branch, values in samples.items():
        dimension = 6
        dual_variables = [
            Dual.variable(value, index, dimension, modulus)
            for index, value in enumerate((*values, 1, 1, 1))
        ]
        S, D, G, t0, t1, t2 = dual_variables
        dual_planes = branch_planes_generic(
            branch, S, D, G, (t0, t1, t2)
        )
        dual_reduced = tuple(
            row_reduce_dual(plane, pivots)
            for plane, pivots in zip(dual_planes, PIVOTS, strict=True)
        )
        dual_coordinates = chart_coordinates_generic(dual_reduced)
        family_jacobian = [
            list(coordinate.gradient) for coordinate in dual_coordinates
        ]
        rows, columns, expected_family_det = family_certificates[branch]
        family_minor = [
            [family_jacobian[row][column] for column in columns]
            for row in rows
        ]
        assert matrix_rank_mod(family_jacobian, modulus) == 5
        assert determinant_mod(family_minor, modulus) == (
            expected_family_det % modulus
        )

        numeric_planes = branch_planes_generic(branch, *values)
        numeric_planes = tuple(
            [[entry % modulus for entry in row] for row in plane]
            for plane in numeric_planes
        )
        numeric_branches[branch] = numeric_planes
        reduced = tuple(
            row_reduce_numeric(plane, pivots, modulus)
            for plane, pivots in zip(numeric_planes, PIVOTS, strict=True)
        )
        coordinates = chart_coordinates_generic(reduced)
        reduced_tensor = {
            word: value % modulus
            for word, value in coefficients_generic(reduced).items()
        }
        anchor = (0, 0, 0, 0)
        assert reduced_tensor[anchor] != 0
        ratios = []
        for mode in range(4):
            adjacent = list(anchor)
            adjacent[mode] = 1
            ratios.append(
                reduced_tensor[tuple(adjacent)]
                * pow(reduced_tensor[anchor], -1, modulus)
                % modulus
            )
        point = (*coordinates, *ratios)
        incidence_dimension = 20
        variables = [
            Dual.variable(value, index, incidence_dimension, modulus)
            for index, value in enumerate(point)
        ]
        universal_planes = chart_planes_generic(variables[:16])
        universal_tensor = coefficients_generic(universal_planes)
        z = variables[16:]
        equations = []
        for word in WORDS:
            if word == anchor:
                continue
            ratio = Dual.constant(1, incidence_dimension, modulus)
            for mode in range(4):
                if word[mode]:
                    ratio *= z[mode]
            equations.append(
                universal_tensor[word] - universal_tensor[anchor] * ratio
            )
        assert all(equation.value == 0 for equation in equations)
        incidence_jacobian = [
            list(equation.gradient) for equation in equations
        ]
        columns = incidence_columns[branch]
        incidence_minor = [
            [row[column] for column in columns]
            for row in incidence_jacobian
        ]
        assert matrix_rank_mod(incidence_jacobian, modulus) == 15
        assert determinant_mod(incidence_minor, modulus) == (
            incidence_determinants[branch] % modulus
        )

        signature = diagonal_jump_signature_mod(numeric_planes, modulus)
        assert signature == expected_signatures[branch]
        profile = pair_profile_mod(numeric_planes, modulus)
        assert profile == (4, 4, 3, 4, 3, 3)
        branch_audits[branch] = {
            "family_tangent_rank": 5,
            "family_minor_determinant": expected_family_det % modulus,
            "incidence_jacobian_rank": 15,
            "incidence_minor_determinant": (
                incidence_determinants[branch] % modulus
            ),
            "jump_signature_two_two_one_three": list(signature),
            "pair_profile": list(profile),
        }

    first_known, second_known = known_samples_mod(modulus)
    all_samples = {
        "known_first": first_known,
        "known_second": second_known,
        **numeric_branches,
    }
    signatures = {
        name: diagonal_jump_signature_mod(planes, modulus)
        for name, planes in all_samples.items()
    }
    assert signatures == expected_signatures
    assert len(set(signatures.values())) == 5
    assert pair_profile_mod(first_known, modulus) == (4, 4, 4, 3, 3, 3)
    assert pair_profile_mod(second_known, modulus) == (4, 4, 3, 4, 3, 3)

    return {
        "modulus": modulus,
        "cubic_diagonal_quadric_map_replayed": True,
        "double_contraction_rank": 2,
        "raw_coefficient_checks": len(WORDS),
        "split_determinant_replayed": True,
        "branches": branch_audits,
        "all_five_jump_signatures": {
            name: list(signature) for name, signature in signatures.items()
        },
    }


def main() -> None:
    audits = [audit_modulus(modulus) for modulus in MODULI]
    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": (
            "DP permanent, modular dual numbers, mixed Grassmann charts, "
            "and modular diagonal-quadric ranks"
        ),
        "moduli": list(MODULI),
        "audits": audits,
        "three_component_certificates_replayed": True,
        "five_orbit_jump_invariant_replayed": True,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p4_diagonal_quadric_one_three_components_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
