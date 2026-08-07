#!/usr/bin/env python3
"""Independent exact audit of the all-rank-one triangle component.

Imports nothing from the primary verifier.  Uses a subset-DP
permanent, separately rebuilds the exact rational family and the
universal incidence Jacobian over Q, and additionally replays both
Jacobians modulo the primes 101 and 103 with dual-number
differentiation and modular elimination.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md"
PRIMARY = ROOT / "verify_p4_all_rank_one_triangle_pure_component.py"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = ((1, 2), (1, 2), (0, 1), (0, 2))
SAMPLE_P = 2
SAMPLE_Q = 3
FAMILY_MINOR_ROWS = (0, 1, 2, 3, 4)
INCIDENCE_COLUMNS = (0, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 17, 18, 19)
AUDIT_PRIMES = (101, 103)
RANDOM_TENSOR_TRIALS = 24


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_dp(rows):
    states = {0: rows[0][0] * 0 + 1}
    for row in rows:
        updated = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                new_mask = mask | bit
                updated[new_mask] = updated.get(new_mask, 0) + value * entry
        states = updated
    return states[(1 << len(rows)) - 1]


def tensor(planes):
    return {
        word: sp.expand(
            permanent_dp(
                tuple(
                    tuple(planes[mode].row(word[mode]))
                    for mode in range(4)
                )
            )
        )
        for word in WORDS
    }


def family_rows(p, q):
    return (
        (
            (p * q + 1, 1, p, p * q + 1),
            (q + 1, 0, 1, q),
        ),
        ((p, 1, 0, 0), (0, 0, 1, -1)),
        ((1, 0, -1, 0), (-p, 1, 0, 0)),
        ((0, 0, 1, 1), (1, 0, 1, 0)),
    )


def make_family(p, q, scales=(1, 1, 1)):
    full_scales = tuple(scales) + (1,)
    return tuple(
        sp.Matrix(
            [
                [
                    entry * scale
                    for entry, scale in zip(row, full_scales, strict=True)
                ]
                for row in plane
            ]
        )
        for plane in family_rows(p, q)
    )


def reduce_planes(planes):
    reduced = []
    coordinates = []
    for plane, pivots in zip(planes, PIVOTS, strict=True):
        chart = sp.simplify(plane[:, pivots].inv() * plane)
        nonpivots = tuple(index for index in range(4) if index not in pivots)
        reduced.append(chart)
        coordinates.extend(
            chart[row, column]
            for row in range(2)
            for column in nonpivots
        )
    return tuple(reduced), tuple(coordinates)


def chart_planes(variables):
    planes = []
    for mode, pivots in enumerate(PIVOTS):
        nonpivots = tuple(index for index in range(4) if index not in pivots)
        plane = sp.zeros(2, 4)
        plane[0, pivots[0]] = 1
        plane[1, pivots[1]] = 1
        entries = variables[4 * mode : 4 * mode + 4]
        for row in range(2):
            for offset, column in enumerate(nonpivots):
                plane[row, column] = entries[2 * row + offset]
        planes.append(plane)
    return tuple(planes)


def pair_matrix(left, right):
    rows = []
    for i in range(2):
        for j in range(2):
            rows.append(
                [
                    left[i, a] * right[j, b] + left[i, b] * right[j, a]
                    for a, b in PAIRS
                ]
            )
    return sp.Matrix(rows)


def diagonal_quadric_jump(plane):
    first, second = plane.nullspace()
    restriction = sp.Matrix(
        (
            tuple(first[index] ** 2 for index in range(4)),
            tuple(
                2 * first[index] * second[index] for index in range(4)
            ),
            tuple(second[index] ** 2 for index in range(4)),
        )
    )
    quadrics = restriction.nullspace()
    if len(quadrics) == 1:
        return None
    assert len(quadrics) == 2
    one_three = any(
        all(vector[index] == 0 for vector in quadrics)
        for index in range(4)
    )
    return "1+3" if one_three else "2+2"


# ------------------------- modular replay ---------------------------


class Dual:
    """Dual numbers a + b*eps over F_modulus for derivative replay."""

    __slots__ = ("a", "b", "modulus")

    def __init__(self, a, b, modulus):
        self.a = a % modulus
        self.b = b % modulus
        self.modulus = modulus

    def _coerce(self, other):
        if isinstance(other, Dual):
            return other
        return Dual(other, 0, self.modulus)

    def __add__(self, other):
        other = self._coerce(other)
        return Dual(self.a + other.a, self.b + other.b, self.modulus)

    __radd__ = __add__

    def __sub__(self, other):
        other = self._coerce(other)
        return Dual(self.a - other.a, self.b - other.b, self.modulus)

    def __rsub__(self, other):
        return self._coerce(other) - self

    def __mul__(self, other):
        other = self._coerce(other)
        return Dual(
            self.a * other.a,
            self.a * other.b + self.b * other.a,
            self.modulus,
        )

    __rmul__ = __mul__

    def __neg__(self):
        return Dual(-self.a, -self.b, self.modulus)

    def inv(self):
        inverse = pow(self.a, -1, self.modulus)
        return Dual(
            inverse, -self.b * inverse * inverse, self.modulus
        )


def modular_fraction(value, modulus):
    rational = sp.Rational(value)
    return (
        int(rational.p) * pow(int(rational.q), -1, modulus) % modulus
    )


def dual_chart_coordinates(p, q, scales, modulus):
    """Chart coordinates of the scaled family over dual numbers."""
    zero = Dual(0, 0, modulus)
    one = Dual(1, 0, modulus)
    full_scales = scales + (one,)
    planes = []
    for plane in family_rows(p, q):
        planes.append(
            [
                [
                    (
                        entry
                        if isinstance(entry, Dual)
                        else Dual(entry, 0, modulus)
                    )
                    * full_scales[column]
                    for column, entry in enumerate(row)
                ]
                for row in plane
            ]
        )
    coordinates = []
    for plane, pivots in zip(planes, PIVOTS, strict=True):
        a = plane[0][pivots[0]]
        b = plane[0][pivots[1]]
        c = plane[1][pivots[0]]
        d = plane[1][pivots[1]]
        determinant = a * d - b * c
        inverse = determinant.inv()
        inv_rows = (
            (d * inverse, zero - b * inverse),
            (zero - c * inverse, a * inverse),
        )
        nonpivots = tuple(
            index for index in range(4) if index not in pivots
        )
        for row in range(2):
            for column in nonpivots:
                coordinates.append(
                    inv_rows[row][0] * plane[0][column]
                    + inv_rows[row][1] * plane[1][column]
                )
    return coordinates


def modular_rank_and_minor(matrix, rows, columns, modulus):
    minor = [[matrix[r][c] % modulus for c in columns] for r in rows]
    determinant = modular_determinant(minor, modulus)
    rank = modular_rank(matrix, modulus)
    return rank, determinant


def modular_determinant(matrix, modulus):
    work = [row[:] for row in matrix]
    size = len(work)
    result = 1
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if work[row][column] % modulus
            ),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[pivot], work[column] = work[column], work[pivot]
            result = -result
        value = work[column][column] % modulus
        result = result * value % modulus
        inverse = pow(value, -1, modulus)
        for row in range(column + 1, size):
            scale = work[row][column] * inverse % modulus
            if not scale:
                continue
            for offset in range(column, size):
                work[row][offset] = (
                    work[row][offset] - scale * work[column][offset]
                ) % modulus
    return result % modulus


def modular_rank(matrix, modulus):
    work = [[entry % modulus for entry in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, modulus)
        work[rank] = [value * inverse % modulus for value in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                (left - scale * right) % modulus
                for left, right in zip(work[row], work[rank])
            ]
        rank += 1
    return rank


def modular_family_tangent(modulus):
    base = (SAMPLE_P, SAMPLE_Q, 1, 1, 1)
    columns = []
    for direction in range(5):
        values = [
            Dual(value, 1 if index == direction else 0, modulus)
            for index, value in enumerate(base)
        ]
        coordinates = dual_chart_coordinates(
            values[0], values[1], (values[2], values[3], values[4]),
            modulus,
        )
        columns.append([entry.b for entry in coordinates])
    return [
        [columns[direction][row] for direction in range(5)]
        for row in range(16)
    ]


def modular_incidence_jacobian(point, anchor, modulus):
    jacobian_columns = []
    for direction in range(20):
        duals = [
            Dual(value, 1 if index == direction else 0, modulus)
            for index, value in enumerate(point)
        ]
        plane_values = duals[:16]
        ratio_values = duals[16:]
        planes = []
        for mode, pivots in enumerate(PIVOTS):
            nonpivots = tuple(
                index for index in range(4) if index not in pivots
            )
            plane = [
                [Dual(0, 0, modulus) for _ in range(4)] for _ in range(2)
            ]
            plane[0][pivots[0]] = Dual(1, 0, modulus)
            plane[1][pivots[1]] = Dual(1, 0, modulus)
            entries = plane_values[4 * mode : 4 * mode + 4]
            for row in range(2):
                for offset, column in enumerate(nonpivots):
                    plane[row][column] = entries[2 * row + offset]
            planes.append(plane)
        values = {}
        for word in WORDS:
            values[word] = permanent_dp(
                tuple(tuple(planes[mode][word[mode]]) for mode in range(4))
            )
        column = []
        for word in WORDS:
            if word == anchor:
                continue
            monomial = Dual(1, 0, modulus)
            for mode in range(4):
                if word[mode] != anchor[mode]:
                    monomial = monomial * ratio_values[mode]
            equation = values[word] - values[anchor] * monomial
            if direction == 0:
                assert equation.a == 0
            column.append(equation.b)
        jacobian_columns.append(column)
    return [
        [jacobian_columns[direction][row] for direction in range(20)]
        for row in range(15)
    ]


def modular_random_tensor_checks(modulus):
    generator = random.Random(20260804 + modulus)
    for _trial in range(RANDOM_TENSOR_TRIALS):
        p = generator.randrange(modulus)
        q = generator.randrange(modulus)
        scales = tuple(
            generator.randrange(1, modulus) for _ in range(3)
        ) + (1,)
        rows = [
            [
                [entry * scale % modulus
                 for entry, scale in zip(row, scales)]
                for row in plane
            ]
            for plane in family_rows(p, q)
        ]
        for word in WORDS:
            value = permanent_dp(
                tuple(tuple(rows[mode][word[mode]]) for mode in range(4))
            ) % modulus
            if word == (1, 1, 1, 1):
                expected = (
                    -2 * scales[0] * scales[1] * scales[2]
                ) % modulus
                assert value == expected
            else:
                assert value == 0


def main() -> None:
    p, q, t0, t1, t2 = sp.symbols("p q t0 t1 t2")

    # Single-word identity, replayed with the subset-DP permanent.
    scaled = make_family(p, q, (t0, t1, t2))
    coefficients = tensor(scaled)
    assert sp.factor(
        coefficients[(1, 1, 1, 1)] + 2 * t0 * t1 * t2
    ) == 0
    assert all(
        value == 0
        for word, value in coefficients.items()
        if word != (1, 1, 1, 1)
    )

    # Zero products and supports with independent code.
    plain = make_family(p, q)
    zero_pairs = (
        (tuple(plain[1].row(0)), tuple(plain[2].row(1))),
        (tuple(plain[1].row(1)), tuple(plain[3].row(0))),
        (tuple(plain[2].row(0)), tuple(plain[3].row(1))),
    )
    for left, right in zero_pairs:
        assert all(
            sp.expand(left[i] * right[j] + left[j] * right[i]) == 0
            for i, j in PAIRS
        )
    supports = tuple(
        tuple(index for index, value in enumerate(left) if value != 0)
        for left, _right in zero_pairs
    )
    assert supports == ((0, 1), (2, 3), (0, 2))

    sample = {p: SAMPLE_P, q: SAMPLE_Q, t0: 1, t1: 1, t2: 1}
    point_planes = tuple(plane.subs(sample) for plane in scaled)
    assert all(plane.rank() == 2 for plane in point_planes)

    # Exact family tangent replay.
    reduced, coordinates = reduce_planes(scaled)
    jacobian = sp.Matrix(coordinates).jacobian(
        (p, q, t0, t1, t2)
    ).subs(sample)
    family_minor = jacobian.extract(
        FAMILY_MINOR_ROWS, tuple(range(5))
    ).det()
    assert jacobian.rank() == 5
    assert family_minor == -1

    # Exact universal incidence replay.
    plane_variables = sp.symbols("u0:16")
    target_variables = sp.symbols("v0:4")
    universal_tensor = tensor(chart_planes(plane_variables))
    reduced_point = tuple(plane.subs(sample) for plane in reduced)
    point_tensor = tensor(reduced_point)
    anchor = (0, 1, 1, 0)
    assert point_tensor[anchor] != 0
    ratios = []
    for mode in range(4):
        adjacent = list(anchor)
        adjacent[mode] = 1 - adjacent[mode]
        ratios.append(
            sp.nsimplify(
                point_tensor[tuple(adjacent)] / point_tensor[anchor]
            )
        )
    assert ratios == [sp.Rational(-1, 2), 0, 0, 0]
    equations = []
    for word in WORDS:
        if word == anchor:
            continue
        monomial = sp.prod(
            target_variables[mode]
            for mode in range(4)
            if word[mode] != anchor[mode]
        )
        equations.append(
            sp.expand(
                universal_tensor[word] - universal_tensor[anchor] * monomial
            )
        )
    all_variables = (*plane_variables, *target_variables)
    coordinate_point = tuple(
        sp.nsimplify(sp.cancel(value.subs(sample)))
        for value in coordinates
    )
    point = coordinate_point + tuple(ratios)
    substitution = dict(zip(all_variables, point, strict=True))
    assert all(equation.subs(substitution) == 0 for equation in equations)
    incidence = sp.Matrix(equations).jacobian(all_variables).subs(
        substitution
    )
    incidence_minor = incidence[:, INCIDENCE_COLUMNS].det()
    assert incidence.rank() == 15
    assert incidence_minor == 860160

    # Invariants: profile, all-rank-one triangle, orientations, jumps.
    profile = []
    triangle = {}
    for a, b in PAIRS:
        matrix = pair_matrix(point_planes[a], point_planes[b])
        rank = matrix.rank()
        profile.append(rank)
        if rank == 3:
            relation = matrix.T.nullspace()
            assert len(relation) == 1
            two_by_two = sp.Matrix(2, 2, tuple(relation[0]))
            triangle[(a, b)] = two_by_two
    assert tuple(profile) == (4, 4, 4, 3, 3, 3)
    assert sorted(triangle) == [(1, 2), (1, 3), (2, 3)]
    heads = {}
    for (a, b), two_by_two in triangle.items():
        assert two_by_two.rank() == 1
        row, column = next(
            (i, j)
            for i in range(2)
            for j in range(2)
            if two_by_two[i, j] != 0
        )
        left_vector = two_by_two[:, column].T * point_planes[a]
        right_vector = two_by_two[row, :] * point_planes[b]
        left_kernel = (
            sp.Matrix.vstack(left_vector, point_planes[a].row(0)).rank()
            == 1
        )
        right_kernel = (
            sp.Matrix.vstack(right_vector, point_planes[b].row(0)).rank()
            == 1
        )
        assert left_kernel != right_kernel
        heads[(a, b)] = a if left_kernel else b
    assert heads == {(1, 2): 1, (1, 3): 3, (2, 3): 2}
    jumps = [
        jump
        for plane in point_planes
        if (jump := diagonal_quadric_jump(plane)) is not None
    ]
    assert jumps.count("2+2") == 1
    assert jumps.count("1+3") == 2

    # Modular replay at two primes: dual-number Jacobians, modular
    # elimination, and randomized single-word corroboration.
    modular_results = {}
    for modulus in AUDIT_PRIMES:
        tangent = modular_family_tangent(modulus)
        tangent_rank, tangent_minor = modular_rank_and_minor(
            tangent, FAMILY_MINOR_ROWS, tuple(range(5)), modulus
        )
        assert tangent_rank == 5
        assert tangent_minor == (-1) % modulus
        incidence_point = tuple(
            modular_fraction(value, modulus) for value in point
        )
        incidence_matrix = modular_incidence_jacobian(
            incidence_point, anchor, modulus
        )
        incidence_rank, incidence_det = modular_rank_and_minor(
            incidence_matrix,
            tuple(range(15)),
            INCIDENCE_COLUMNS,
            modulus,
        )
        assert incidence_rank == 15
        assert incidence_det == 860160 % modulus
        modular_random_tensor_checks(modulus)
        modular_results[modulus] = {
            "family_tangent_rank": tangent_rank,
            "family_tangent_minor": tangent_minor,
            "incidence_jacobian_rank": incidence_rank,
            "incidence_minor": incidence_det,
            "random_tensor_trials": RANDOM_TENSOR_TRIALS,
        }

    result = {
        "audited": True,
        "independent_of_primary_imports": True,
        "field": "Q",
        "method": (
            "subset-DP permanent, independently reconstructed exact "
            "family/incidence Jacobians, and two-prime dual-number "
            "modular replay"
        ),
        "pure_coefficient_1111": "-2*t0*t1*t2",
        "family_free": True,
        "family_tangent_rank": 5,
        "family_tangent_minor": str(family_minor),
        "incidence_jacobian_rank": 15,
        "incidence_minor": str(incidence_minor),
        "pair_profile": list(profile),
        "rank_three_edges": [[1, 2], [1, 3], [2, 3]],
        "relation_ranks": [1, 1, 1],
        "orientation_heads": {"12": 1, "13": 3, "23": 2},
        "jump_signature": [1, 2],
        "zero_product_supports": [
            "".join(map(str, pair)) for pair in supports
        ],
        "modular_replay": {
            str(modulus): values
            for modulus, values in modular_results.items()
        },
        "component_dimension": 5,
        "certified_pure_component_orbit_count": 9,
        "generic_H31_excluded": False,
        "generic_weighted_H22_excluded": False,
        "all_pure_components_classified": False,
        "global_problem_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p4_all_rank_one_triangle_pure_component_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
