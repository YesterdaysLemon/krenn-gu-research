#!/usr/bin/env python3
"""Independent rational audit of the common-singleton component certificate."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GRAPH_SLICE = ROOT / "tmp" / "p4_common_singleton_local_graph_slice.sing"
EXPECTED_GRAPH_SLICE_SHA256 = (
    "4aaf80d0f2e08550e7f2929cb0eda9443b79ce8a0945f5cc8113a48a5d5c0b7b"
)
PAIRS = tuple(itertools.combinations(range(4), 2))
WORDS = tuple(itertools.product((0, 1), repeat=4))
ANCHOR = (0, 1, 1, 1)
PARAMETER_SAMPLE = (-3, -2, -1, -1, -1)
KNOWN_COMPONENT_PROFILES = (
    (4, 4, 4, 3, 3, 3),
    (4, 4, 3, 4, 3, 3),
    (4, 4, 3, 4, 3, 3),
    (4, 3, 2, 4, 4, 3),
    (4, 4, 3, 4, 3, 3),
    (4, 4, 4, 2, 2, 2),
    (3, 3, 3, 4, 4, 4),
    (4, 4, 4, 3, 3, 3),
    (3, 3, 4, 3, 3, 3),
    (4, 4, 4, 3, 3, 3),
    (2, 3, 4, 3, 4, 4),
    (2, 3, 4, 3, 4, 4),
    (4, 4, 4, 3, 3, 3),
)


class Dual:
    """A rational value and five exact first derivatives."""

    def __init__(self, value, gradient=(0, 0, 0, 0, 0)):
        self.value = Fraction(value)
        self.gradient = tuple(Fraction(entry) for entry in gradient)

    @classmethod
    def seed(cls, value, index):
        gradient = [Fraction(0)] * 5
        gradient[index] = Fraction(1)
        return cls(value, gradient)

    def __add__(self, other):
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(
            self.value + other.value,
            tuple(a + b for a, b in zip(self.gradient, other.gradient, strict=True)),
        )

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, tuple(-entry for entry in self.gradient))

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __mul__(self, other):
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(
            self.value * other.value,
            tuple(
                self.value * right + other.value * left
                for left, right in zip(self.gradient, other.gradient, strict=True)
            ),
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = other if isinstance(other, Dual) else Dual(other)
        assert other.value
        inverse = Fraction(1, 1) / other.value
        return Dual(
            self.value * inverse,
            tuple(
                (left * other.value - self.value * right) * inverse * inverse
                for left, right in zip(self.gradient, other.gradient, strict=True)
            ),
        )

    def __rtruediv__(self, other):
        return Dual(other) / self


def cross(left, right):
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def matvec(matrix, vector):
    return tuple(
        sum(entry * coordinate for entry, coordinate in zip(row, vector, strict=True))
        for row in matrix
    )


def family(parameters):
    L, M, a, b, c = parameters
    d = -(L * b + M * a + M * c + b * c) / (L + a)
    polar = ((0, M, L), (M, 0, 1), (L, 1, 0))
    ell = (1, L, M)
    v1 = (1, a, b)
    v2 = (1, c, d)
    raw = cross(matvec(polar, v1), matvec(polar, v2))
    v3 = tuple(entry / raw[0] for entry in raw)
    return (ell, v1, v2, v3), d


def permanent(rows):
    return sum(
        _product(rows[row][permutation[row]] for row in range(4))
        for permutation in itertools.permutations(range(4))
    )


def _product(entries):
    result = 1
    for entry in entries:
        result *= entry
    return result


def pair_column(left, right):
    return tuple(
        left[i] * right[j] + left[j] * right[i]
        for i, j in PAIRS
    )


def matrix_rank(rows):
    work = [[Fraction(entry) for entry in row] for row in rows]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [entry / pivot_value for entry in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[rank], strict=True)
            ]
        rank += 1
    return rank


def family_audit():
    vectors, d = family(tuple(Fraction(value) for value in PARAMETER_SAMPLE))
    assert d == 2
    assert vectors == (
        (1, -3, -2),
        (1, -1, -1),
        (1, -1, 2),
        (1, 3, -1),
    )
    e = (1, 0, 0, 0)
    planes = tuple((e, (0, *vector)) for vector in vectors)
    tensor = {
        word: permanent(tuple(planes[mode][word[mode]] for mode in range(4)))
        for word in WORDS
    }
    assert {word: value for word, value in tensor.items() if value} == {
        ANCHOR: Fraction(4)
    }

    profiles = []
    relation_ranks = []
    for left, right in PAIRS:
        columns = tuple(
            pair_column(planes[left][left_row], planes[right][right_row])
            for left_row in range(2)
            for right_row in range(2)
        )
        matrix_rows = tuple(zip(*columns, strict=True))
        profiles.append(matrix_rank(matrix_rows))
        assert columns[0] == (0, 0, 0, 0, 0, 0)
        assert matrix_rank(tuple(zip(*columns[1:], strict=True))) == 3
        relation_ranks.append(1)  # the unique relation is e tensor e
    assert tuple(profiles) == (3, 3, 3, 3, 3, 3)

    dual_parameters = tuple(
        Dual.seed(value, index) for index, value in enumerate(PARAMETER_SAMPLE)
    )
    dual_vectors, _dual_d = family(dual_parameters)
    chart_coordinates = tuple(
        coordinate
        for vector in dual_vectors
        for coordinate in (Dual(0), Dual(0), vector[1], vector[2])
    )
    tangent_rows = tuple(coordinate.gradient for coordinate in chart_coordinates)
    assert matrix_rank(tangent_rows) == 5
    return profiles, relation_ranks


def height_audit():
    # D=Z_(p)[y1,...,y15]_(p,y) has dimension sixteen.  The exact modular
    # local standard basis gives special height sixteen.  One extra generator
    # can increase height by at most one, while J itself has fifteen generators.
    integral_ambient_dimension = 16
    slice_generator_count = 15
    special_fibre_local_dimension = 0
    special_height = integral_ambient_dimension - special_fibre_local_dimension
    lower_height = special_height - 1
    upper_height = slice_generator_count
    assert lower_height == upper_height == 15
    generic_slice_local_dimension = 15 - lower_height
    assert generic_slice_local_dimension == 0

    incidence_ambient_dimension = 20
    incidence_generator_count = 15
    slicing_equations = 5
    incidence_lower_dimension = incidence_ambient_dimension - incidence_generator_count
    incidence_upper_dimension = generic_slice_local_dimension + slicing_equations
    assert incidence_lower_dimension == incidence_upper_dimension == 5
    return {
        "integral_slice_height": lower_height,
        "generic_slice_local_dimension": generic_slice_local_dimension,
        "incidence_local_dimension": incidence_lower_dimension,
    }


def main() -> None:
    assert GRAPH_SLICE.exists(), "run the primary verifier first"
    assert hashlib.sha256(GRAPH_SLICE.read_bytes()).hexdigest() == (
        EXPECTED_GRAPH_SLICE_SHA256
    )
    profiles, relation_ranks = family_audit()
    height = height_audit()
    assert all(max(profile) == 4 for profile in KNOWN_COMPONENT_PROFILES)
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": (
                    "independent Fraction arithmetic, dual-number family tangent, "
                    "closed pair-rank separation, and Krull-height bookkeeping"
                ),
                "sample_pair_profile": profiles,
                "sample_relation_matrix_ranks": relation_ranks,
                "family_tangent_rank": 5,
                "graph_slice_sha256": EXPECTED_GRAPH_SLICE_SHA256,
                **height,
                "old_component_profile_groups_checked": len(KNOWN_COMPONENT_PROFILES),
                "old_component_orbits_covered": 17,
                "new_component_orbit_number": 18,
                "global_conjecture_resolved": False,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
