#!/usr/bin/env python3
"""Independent exact audit of the split-pair (F12) twelfth component.

Imports NOTHING from the primary verifier.  Recomputes every
coefficient with a subset-dynamic-programming permanent (never
itertools.permutations), rebuilds the family, charts, and universal
incidence data from scratch, and replays:

  * the free-chart three-word structure and the identical two-word
    tied purity (closed forms and mixed-word flattening identities)
    symbolically over Q and at randomized parameter values modulo
    the two primes 10007 and 10009;
  * the pair profile (3,3,3,4,3,3) with rank sum 19 and the
    split-plane facts (U0 and U3 meet both P01 and span(e2,e3);
    the middle planes and every plane of the thirteenth's sample
    do not meet two complementary coordinate planes) exactly and
    modulo both primes;
  * the rank-five family tangent (seven directions including the
    projective torus) and the rank-FOURTEEN incidence Jacobian
    modulo both primes, by dual-number differentiation and modular
    elimination, recovering the same minors -1 and 28311552000;
  * the SLICE certificate modulo both primes: the eleven multi-flip
    equations are rebuilt via the DP permanent, shifted to the
    sample INSIDE Singular (a ring map, an independent construction
    path from the primary verifier's sympy-side expansion), cut by
    the same five integer hyperplanes, and given a `ds` standard
    basis in characteristic p.  Local dimension zero modulo p is a
    CONSISTENCY CHECK: the characteristic-zero run in the primary
    verifier is the certificate (a mod-p dimension does not imply
    the char-0 dimension; agreement at two independent primes
    corroborates it);
  * the distinctness groundings in exact rational arithmetic: all
    eight documented rank-sum-21 fivefold samples (fraction rank),
    and the thirteenth's certificate sample re-verified as a
    nonzero pure single-word tuple with no split plane.

The two audit primes 10007 and 10009 divide none of the numbers
relied on (anchor -100 = -2^2*5^2, second word -32 = -2^5, ratio
8/25, family minor -1, incidence minor 28311552000 = 2^23*3^3*5^3,
and the small sample denominators 6, 4, 28, 5, 3, 2).
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import subprocess
import time
from fractions import Fraction
from pathlib import Path

import sympy as sp

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
THEOREM = HERE / "P4_SPLIT_PAIR_PURE_COMPONENT.md"
PRIMARY = HERE / "verify_p4_split_pair_pure_component.py"

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
FLATTENINGS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
PIVOTS = ((0, 2), (0, 1), (0, 1), (0, 2))
ANCHOR = (0, 0, 0, 0)
COMPLEMENTARY_SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))

# sample (p2,p3,q2,k) and torus (1,1,1); q3 = -k(p2+q2)-p3 = -15.
SAMPLE = (3, -1, 5, 2)
COORDINATE_POINT = tuple(
    Fraction(value)
    for value in (1, 0, 0, -2, 3, -1, 3, -1, 5, -15, 5, -15, 1, 0, 0, 2)
)
EXPECTED_RATIOS = (Fraction(8, 25), Fraction(1), Fraction(1), Fraction(0))
FAMILY_MINOR_ROWS = (0, 3, 4, 5, 8)
FAMILY_MINOR_COLUMNS = (0, 1, 2, 3, 4)
FAMILY_MINOR = Fraction(-1)
INCIDENCE_MINOR_ROWS = (0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14)
INCIDENCE_MINOR_COLUMNS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 19)
INCIDENCE_MINOR = Fraction(28311552000)
SLICE_COEFFS = (
    (1, 2, -1, 3, 1, -2, 1, 1, -3, 2, 1, -1, 2, 1, -2, 3),
    (2, -1, 1, 1, -2, 3, 1, -1, 1, 1, -2, 1, 3, -1, 1, -2),
    (1, 1, 2, -3, 1, 1, -1, 2, 1, -2, 3, 1, -1, 1, 1, 2),
    (3, -2, 1, 1, 1, -1, 2, 1, -2, 1, 1, 3, 1, -1, 2, 1),
    (1, 3, -2, 1, 2, 1, 1, -1, 1, 2, -1, 1, 1, 2, -3, 1),
)
AUDIT_PRIMES = (10007, 10009)
RANDOM_TENSOR_TRIALS = 24
SINGULAR_TIMEOUT = 900
THIRTEENTH_SAMPLE = (
    ((1, 1, 0, 0), (1, 0, -1, 7)),
    ((1, -1, 0, 0), (0, 1, 2, -10)),
    ((1, -1, 0, 0), (0, 1, 3, -15)),
    ((1, 1, 0, 0), (0, Fraction(1, 6), 1, 7)),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_dp(rows):
    """Subset-DP permanent over any commutative ring."""
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


def family_rows(p2, p3, q2, k):
    q3 = -k * (p2 + q2) - p3
    return (
        ((1, 1, 0, 0), (0, 0, 1, -k)),
        ((1, -1, 0, 0), (0, 1, p2, p3)),
        ((1, -1, 0, 0), (0, 1, q2, q3)),
        ((1, 1, 0, 0), (0, 0, 1, k)),
    )


def free_family_rows(p2, p3, q2, q3, k):
    return (
        ((1, 1, 0, 0), (0, 0, 1, -k)),
        ((1, -1, 0, 0), (0, 1, p2, p3)),
        ((1, -1, 0, 0), (0, 1, q2, q3)),
        ((1, 1, 0, 0), (0, 0, 1, k)),
    )


def tensor_dp(planes):
    return {
        word: permanent_dp(
            tuple(tuple(planes[mode][word[mode]]) for mode in range(4))
        )
        for word in WORDS
    }


def mixed_word_purity(tensor, expander=lambda value: value):
    """All 2x2 flattening minors via the mixed-word swap identities."""
    for left, _right in FLATTENINGS:
        for word_a in WORDS:
            for word_b in WORDS:
                mixed_a = tuple(
                    word_a[i] if i in left else word_b[i] for i in range(4)
                )
                mixed_b = tuple(
                    word_b[i] if i in left else word_a[i] for i in range(4)
                )
                value = expander(
                    tensor[word_a] * tensor[word_b]
                    - tensor[mixed_a] * tensor[mixed_b]
                )
                assert value == 0, (left, word_a, word_b, value)


def chart_planes(entries16):
    """Universal chart planes for the pivots (02),(01),(01),(02)."""
    planes = []
    for mode, pivots in enumerate(PIVOTS):
        nonpivots = tuple(i for i in range(4) if i not in pivots)
        plane = [[0] * 4 for _ in range(2)]
        plane[0][pivots[0]] = 1
        plane[1][pivots[1]] = 1
        chunk = entries16[4 * mode: 4 * mode + 4]
        for row in range(2):
            for offset, column in enumerate(nonpivots):
                plane[row][column] = chunk[2 * row + offset]
        planes.append(plane)
    return planes


def fraction_chart_coordinates(scales=(1, 1, 1)):
    """Chart coordinates of the sample family over exact Fractions."""
    full = tuple(Fraction(s) for s in scales) + (Fraction(1),)
    planes = [
        [[Fraction(entry) * full[column] for column, entry in enumerate(row)]
         for row in plane]
        for plane in family_rows(*SAMPLE)
    ]
    coordinates = []
    for plane, pivots in zip(planes, PIVOTS):
        a = plane[0][pivots[0]]
        b = plane[0][pivots[1]]
        c = plane[1][pivots[0]]
        d = plane[1][pivots[1]]
        determinant = a * d - b * c
        inverse = (
            (d / determinant, -b / determinant),
            (-c / determinant, a / determinant),
        )
        nonpivots = tuple(i for i in range(4) if i not in pivots)
        for row in range(2):
            for column in nonpivots:
                coordinates.append(
                    inverse[row][0] * plane[0][column]
                    + inverse[row][1] * plane[1][column]
                )
    return tuple(coordinates)


def multi_flip_data():
    """(word, flips) for the eleven ratio-eliminated equations."""
    data = []
    for word in WORDS:
        flips = tuple(m for m in range(4) if word[m] != ANCHOR[m])
        if len(flips) >= 2:
            data.append((word, flips))
    assert len(data) == 11
    return tuple(data)


def single_flip(mode):
    return tuple(
        (1 - ANCHOR[i]) if i == mode else ANCHOR[i] for i in range(4)
    )


def rmul_row(left, right):
    return [
        left[a] * right[b] + left[b] * right[a] for a, b in PAIRS
    ]


def fraction_rank(matrix):
    """Row-echelon rank over exact Fractions (own elimination)."""
    work = [[Fraction(entry) for entry in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column] != 0),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        head = work[rank][column]
        work[rank] = [value / head for value in work[rank]]
        for row in range(rows):
            if row == rank or work[row][column] == 0:
                continue
            scale = work[row][column]
            work[row] = [
                left - scale * right
                for left, right in zip(work[row], work[rank])
            ]
        rank += 1
    return rank


def fraction_pair_profile(planes):
    profile = []
    for a, b in PAIRS:
        rows = []
        for i in range(2):
            for j in range(2):
                rows.append(rmul_row(planes[a][i], planes[b][j]))
        profile.append(fraction_rank(rows))
    return tuple(profile)


def meets_pair(plane, pair):
    """U cap span(e_pair) != 0 over Fractions."""
    complement = tuple(i for i in range(4) if i not in pair)
    block = [[plane[r][c] for c in complement] for r in range(2)]
    return fraction_rank(block) <= 1


def meets_two_complementary(plane):
    return any(
        meets_pair(plane, pair) and meets_pair(plane, complement)
        for pair, complement in COMPLEMENTARY_SPLITS
    )


def fivefold_samples():
    samples = {}
    samples["first"] = (
        ((1, 0, -1, -2), (0, 1, 1, 0)), ((1, 1, 0, 0), (0, 0, 1, 1)),
        ((0, 1, 0, 1), (-1, 0, 1, 0)), ((1, 0, 1, 0), (0, 0, -1, 1)),
    )
    samples["dq"] = (
        ((2, -1, -1, -2), (1, -1, 1, 1)), ((1, 0, 0, -1), (1, 1, -1, 1)),
        ((3, 1, 1, -1), (0, 1, -1, 0)), ((1, 0, 0, 1), (0, 1, 1, 0)),
    )
    samples["L1"] = (
        ((2, 4, 0, 0), (0, 0, 1, 1)), ((0, 1, -1, 0), (1, 0, 1, 3)),
        ((1, 0, 4, 2), (0, 1, 0, -1)), ((0, 1, 1, 0), (0, 1, 0, 1)),
    )
    samples["L2"] = (
        ((2, 0, 4, 0), (0, 0, 1, 1)), ((0, 1, -1, 0), (1, 0, 1, 3)),
        ((1, 0, 4, 6), (0, 1, 0, -1)), ((0, 1, 1, 0), (0, 1, 0, 1)),
    )
    samples["L3"] = (
        ((2, 10, -8, 0), (0, 0, 1, 1)), ((0, 1, -1, 0), (1, 0, 1, 2)),
        ((1, 0, 3, -6), (0, 1, 0, -1)), ((0, 1, 1, 0), (0, 1, 0, 1)),
    )
    dd, pp, qq = 2, 3, 5
    n6 = qq * (dd + pp + qq)
    samples["sixth"] = (
        ((-dd * pp, dd + qq, n6, 0), (dd * pp, -dd - qq, 0, n6)),
        ((0, 0, 1, 1), (-dd, 1, -pp - qq, dd)),
        ((pp, 1, 0, qq), (-1, 0, 1, 0)), ((1, 0, 1, 0), (0, 0, -1, 1)),
    )
    a8 = Fraction(-12)
    b8 = Fraction(-10)
    f8 = Fraction(3, 4)
    ph8 = Fraction(-5, 28)
    j8 = f8 + b8 * ph8 ** 2
    kap8 = ph8 * (b8 * f8 + 1)
    eta8 = -(b8 * f8 + 1)
    samples["eighth"] = (
        ((0, 0, 1, -1), (a8 + b8, a8 - b8, 0, 2)),
        ((-a8 * f8 + 1, -a8 * f8 - 1, f8 + ph8, f8 - ph8), (1, 1, 0, 0)),
        ((-a8 * j8 + eta8, -a8 * j8 - eta8, j8 + kap8, j8 - kap8),
         (1, 1, 0, 0)),
        ((1, -1, 0, 0), (0, 0, 1, 1)),
    )
    d9, v90, v91, v92, x91, x92 = 2, 3, 5, 7, 11, -4
    x90 = Fraction(-(d9 * v90 * x91 + v91 * x92), d9 * v91)
    c9 = (-d9 * v91, -d9 * v90, v91, v91)
    k19 = (-c9[1], c9[0], 0, 0)
    k29 = (-c9[2], 0, c9[0], 0)
    k39 = (-c9[3], 0, 0, c9[0])
    al9, be9 = Fraction(2, 3), Fraction(-1, 2)
    samples["ninth"] = (
        (tuple(k19[j] + al9 * k39[j] for j in range(4)),
         tuple(k29[j] + be9 * k39[j] for j in range(4))),
        ((0, 0, 1, -1), (v90, v91, v92, -v92)),
        ((1, 0, -d9, 0), (x90, x91, x92, 0)),
        ((0, 0, 1, 1), (1, 0, d9, 0)),
    )
    return samples


# ------------------------- modular machinery -------------------------


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
        return Dual(inverse, -self.b * inverse * inverse, self.modulus)


def modular_fraction(value, modulus):
    fraction = Fraction(value)
    return (
        fraction.numerator
        * pow(fraction.denominator, -1, modulus)
        % modulus
    )


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


def dual_chart_coordinates(values7, modulus):
    """Chart coordinates of the torus-scaled family over dual numbers.

    values7 = (p2,p3,q2,k,T0,T1,T2) as Duals.
    """
    scales = values7[4:] + (Dual(1, 0, modulus),)
    planes = []
    for plane in family_rows(*values7[:4]):
        planes.append(
            [
                [
                    (
                        entry
                        if isinstance(entry, Dual)
                        else Dual(entry, 0, modulus)
                    )
                    * scales[column]
                    for column, entry in enumerate(row)
                ]
                for row in plane
            ]
        )
    zero = Dual(0, 0, modulus)
    coordinates = []
    for plane, pivots in zip(planes, PIVOTS):
        a = plane[0][pivots[0]]
        b = plane[0][pivots[1]]
        c = plane[1][pivots[0]]
        d = plane[1][pivots[1]]
        determinant = a * d - b * c
        inverse = determinant.inv()
        inverse_rows = (
            (d * inverse, zero - b * inverse),
            (zero - c * inverse, a * inverse),
        )
        nonpivots = tuple(i for i in range(4) if i not in pivots)
        for row in range(2):
            for column in nonpivots:
                coordinates.append(
                    inverse_rows[row][0] * plane[0][column]
                    + inverse_rows[row][1] * plane[1][column]
                )
    return coordinates


def modular_family_tangent(modulus):
    base = tuple(SAMPLE) + (1, 1, 1)
    columns = []
    for direction in range(7):
        values = tuple(
            Dual(value, 1 if index == direction else 0, modulus)
            for index, value in enumerate(base)
        )
        coordinates = dual_chart_coordinates(values, modulus)
        columns.append([entry.b for entry in coordinates])
    return [
        [columns[direction][row] for direction in range(7)]
        for row in range(16)
    ]


def modular_incidence_jacobian(modulus):
    point = tuple(
        modular_fraction(value, modulus)
        for value in COORDINATE_POINT + EXPECTED_RATIOS
    )
    jacobian_columns = []
    for direction in range(20):
        duals = [
            Dual(value, 1 if index == direction else 0, modulus)
            for index, value in enumerate(point)
        ]
        planes = chart_planes(duals[:16])
        ratio_values = duals[16:]
        values = {
            word: permanent_dp(
                tuple(tuple(planes[mode][word[mode]]) for mode in range(4))
            )
            for word in WORDS
        }
        column = []
        for word in WORDS:
            if word == ANCHOR:
                continue
            monomial = Dual(1, 0, modulus)
            for mode in range(4):
                if word[mode] != ANCHOR[mode]:
                    monomial = monomial * ratio_values[mode]
            equation = values[word] - values[ANCHOR] * monomial
            if direction == 0:
                assert equation.a == 0
            column.append(equation.b)
        jacobian_columns.append(column)
    return [
        [jacobian_columns[direction][row] for direction in range(20)]
        for row in range(15)
    ]


def modular_purity_trials(modulus):
    """Randomized replay of the identical-purity closed forms mod p."""
    generator = random.Random(20260804 + modulus)
    for _trial in range(RANDOM_TENSOR_TRIALS):
        p2 = generator.randrange(modulus)
        p3 = generator.randrange(modulus)
        q2 = generator.randrange(modulus)
        k = generator.randrange(1, modulus)
        q3 = (-k * (p2 + q2) - p3) % modulus
        scales = tuple(
            generator.randrange(1, modulus) for _ in range(3)
        ) + (1,)
        rows = [
            [
                [entry * scale % modulus
                 for entry, scale in zip(row, scales)]
                for row in plane
            ]
            for plane in family_rows(p2, p3, q2, k)
        ]
        monomial = scales[0] * scales[1] * scales[2] % modulus
        for word in WORDS:
            value = permanent_dp(
                tuple(tuple(rows[mode][word[mode]]) for mode in range(4))
            ) % modulus
            if word == (0, 1, 1, 0):
                expected = 2 * (p2 * q3 + p3 * q2) * monomial % modulus
            elif word == (1, 1, 1, 0):
                expected = (-2 * k * (p2 + q2)) * monomial % modulus
            else:
                expected = 0
            assert value == expected


def modular_pair_profile(modulus):
    planes = [
        [[entry % modulus for entry in row] for row in plane]
        for plane in family_rows(*SAMPLE)
    ]
    profile = []
    for a, b in PAIRS:
        rows = []
        for i in range(2):
            for j in range(2):
                left = planes[a][i]
                right = planes[b][j]
                rows.append(
                    [
                        (left[p] * right[q] + left[q] * right[p]) % modulus
                        for p, q in PAIRS
                    ]
                )
        profile.append(modular_rank(rows, modulus))
    return tuple(profile)


def modular_split_facts(modulus):
    def meets(plane, pair):
        complement = tuple(i for i in range(4) if i not in pair)
        block = [
            [plane[r][c] % modulus for c in complement] for r in range(2)
        ]
        return modular_rank(block, modulus) <= 1

    planes = family_rows(*SAMPLE)
    for mode in (0, 3):
        assert meets(planes[mode], (0, 1))
        assert meets(planes[mode], (2, 3))
    for mode in (1, 2):
        assert meets(planes[mode], (0, 1))
        for pair, complement in COMPLEMENTARY_SPLITS:
            assert not (
                meets(planes[mode], pair)
                and meets(planes[mode], complement)
            )
    thirteenth = [
        [[modular_fraction(entry, modulus) for entry in row]
         for row in plane]
        for plane in THIRTEENTH_SAMPLE
    ]
    for plane in thirteenth:
        assert meets(plane, (0, 1))
        for pair, complement in COMPLEMENTARY_SPLITS:
            assert not (meets(plane, pair) and meets(plane, complement))


def modular_slice(modulus, word_polynomials, zvars):
    """Replay the slice mod p; the shift happens INSIDE Singular.

    CONSISTENCY CHECK ONLY: the characteristic-zero standard basis in
    the primary verifier is the certificate; a modular local dimension
    zero corroborates it at an independent prime.
    """
    names = {
        word: "tw" + "".join(str(bit) for bit in word) for word in WORDS
    }
    lines = [
        f"ring R={modulus},({','.join(str(z) for z in zvars)}),ds;"
    ]
    for word in WORDS:
        polynomial = str(word_polynomials[word]).replace("**", "^")
        lines.append(f"poly {names[word]}={polynomial};")
    generators = []
    for word, flips in multi_flip_data():
        rhs = "*".join(names[single_flip(mode)] for mode in flips)
        generators.append(
            f"{names[word]}*{names[ANCHOR]}^{len(flips) - 1}-{rhs}"
        )
    lines.append("ideal I0=" + ",".join(generators) + ";")
    shift_images = []
    for z, value in zip(zvars, COORDINATE_POINT):
        if value == 0:
            shift_images.append(str(z))
        elif value > 0:
            shift_images.append(f"{z}+{value}")
        else:
            shift_images.append(f"{z}-{-value}")
    lines.append("ideal M=" + ",".join(shift_images) + ";")
    lines.append("map phi=R,M;")
    lines.append("ideal I=phi(I0);")
    for index, row in enumerate(SLICE_COEFFS):
        form = "+".join(
            f"({coefficient})*{z}" for coefficient, z in zip(row, zvars)
        )
        lines.append(f"poly s{index}={form};")
    lines.append(
        "ideal J=I,"
        + ",".join(f"s{index}" for index in range(len(SLICE_COEFFS)))
        + ";"
    )
    lines.append("option(redSB);")
    lines.append("ideal G=std(J);")
    lines.append('"AUDIT_SLICE_DIM:"+string(dim(G));')
    lines.append("quit;")
    program = "\n".join(lines)
    start = time.time()
    try:
        completed = subprocess.run(
            ("Singular", "-q"),
            input=program,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=SINGULAR_TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise AssertionError(
            "Singular mod-%d slice timed out after %ss: dimension "
            "recorded as null, replay NOT completed"
            % (modulus, SINGULAR_TIMEOUT)
        ) from exc
    elapsed = time.time() - start
    assert completed.returncode == 0, (
        completed.returncode,
        completed.stdout[-800:],
        completed.stderr[-800:],
    )
    markers = [
        line
        for line in completed.stdout.splitlines()
        if line.startswith("AUDIT_SLICE_DIM:")
    ]
    assert len(markers) == 1, completed.stdout[-800:]
    return int(markers[0].split(":", 1)[1].strip()), elapsed


def main() -> None:
    started = time.time()

    # -------- symbolic purity replay with the subset-DP permanent ----
    p2, p3, q2, q3, k = sp.symbols("p2 p3 q2 q3 k")
    free = tensor_dp(free_family_rows(p2, p3, q2, q3, k))
    assert sp.expand(free[(0, 1, 1, 0)] - 2 * (p2 * q3 + p3 * q2)) == 0
    assert sp.expand(
        free[(1, 1, 1, 0)] - ((p3 + q3) - k * (p2 + q2))
    ) == 0
    assert sp.expand(
        free[(0, 1, 1, 1)] - ((p3 + q3) + k * (p2 + q2))
    ) == 0
    for word in WORDS:
        if word not in ((0, 1, 1, 0), (1, 1, 1, 0), (0, 1, 1, 1)):
            assert sp.expand(free[word]) == 0, word
    symbolic = tensor_dp(family_rows(p2, p3, q2, k))
    assert sp.expand(
        symbolic[(0, 1, 1, 0)]
        - 2 * (p2 * (-k * (p2 + q2) - p3) + p3 * q2)
    ) == 0
    assert sp.expand(symbolic[(1, 1, 1, 0)] + 2 * k * (p2 + q2)) == 0
    for word in WORDS:
        if word not in ((0, 1, 1, 0), (1, 1, 1, 0)):
            assert sp.expand(symbolic[word]) == 0, word
    mixed_word_purity(symbolic, expander=sp.expand)

    # -------- exact chart coordinates and point tensor over Q --------
    coordinates = fraction_chart_coordinates()
    assert coordinates == COORDINATE_POINT
    point_planes = chart_planes(list(COORDINATE_POINT))
    point_tensor = {
        word: permanent_dp(
            tuple(tuple(point_planes[mode][word[mode]]) for mode in range(4))
        )
        for word in WORDS
    }
    for word in WORDS:
        if word[3] == 1:
            expected = Fraction(0)
        elif word[0] == 0:
            expected = Fraction(-100)
        else:
            expected = Fraction(-32)
        assert point_tensor[word] == expected, word
    ratios = tuple(
        point_tensor[single_flip(mode)] / point_tensor[ANCHOR]
        for mode in range(4)
    )
    assert ratios == EXPECTED_RATIOS
    # The eleven multi-flip identities vanish at the point (exact).
    for word, flips in multi_flip_data():
        lhs = point_tensor[word] * point_tensor[ANCHOR] ** (len(flips) - 1)
        rhs = Fraction(1)
        for mode in flips:
            rhs *= point_tensor[single_flip(mode)]
        assert lhs - rhs == 0

    # -------- exact distinctness groundings --------------------------
    sample_planes = [
        [[Fraction(entry) for entry in row] for row in plane]
        for plane in family_rows(*SAMPLE)
    ]
    profile = fraction_pair_profile(sample_planes)
    assert profile == (3, 3, 3, 4, 3, 3)
    assert sum(profile) == 19
    for mode in (0, 3):
        assert meets_pair(sample_planes[mode], (0, 1))
        assert meets_pair(sample_planes[mode], (2, 3))
    for mode in (1, 2):
        assert not meets_two_complementary(sample_planes[mode])

    fivefold_rank_sums = {}
    for name, rows in fivefold_samples().items():
        planes = [
            [[Fraction(entry) for entry in row] for row in plane]
            for plane in rows
        ]
        total = sum(fraction_pair_profile(planes))
        fivefold_rank_sums[name] = int(total)
        assert total == 21, (name, total)
    assert len(fivefold_rank_sums) == 8

    thirteenth = [
        [[Fraction(entry) for entry in row] for row in plane]
        for plane in THIRTEENTH_SAMPLE
    ]
    thirteenth_tensor = tensor_dp(thirteenth)
    support = {
        word for word, value in thirteenth_tensor.items() if value != 0
    }
    assert support == {(0, 1, 1, 0)}
    assert thirteenth_tensor[(0, 1, 1, 0)] == Fraction(-120)
    mixed_word_purity(thirteenth_tensor)
    for plane in thirteenth:
        assert meets_pair(plane, (0, 1))
        assert not meets_two_complementary(plane)

    # -------- modular replay at the two audit primes -----------------
    modular_results = {}
    for modulus in AUDIT_PRIMES:
        modular_purity_trials(modulus)
        profile_p = modular_pair_profile(modulus)
        assert profile_p == (3, 3, 3, 4, 3, 3)
        assert sum(profile_p) == 19
        modular_split_facts(modulus)

        tangent = modular_family_tangent(modulus)
        tangent_rank = modular_rank(tangent, modulus)
        assert tangent_rank == 5
        tangent_params_rank = modular_rank(
            [row[:4] for row in tangent], modulus
        )
        assert tangent_params_rank == 4
        tangent_minor = modular_determinant(
            [
                [tangent[row][column] for column in FAMILY_MINOR_COLUMNS]
                for row in FAMILY_MINOR_ROWS
            ],
            modulus,
        )
        assert tangent_minor == modular_fraction(FAMILY_MINOR, modulus)

        incidence = modular_incidence_jacobian(modulus)
        incidence_rank = modular_rank(incidence, modulus)
        assert incidence_rank == 14      # tangent dimension six mod p.
        incidence_minor = modular_determinant(
            [
                [incidence[row][column] for column in INCIDENCE_MINOR_COLUMNS]
                for row in INCIDENCE_MINOR_ROWS
            ],
            modulus,
        )
        assert incidence_minor == modular_fraction(INCIDENCE_MINOR, modulus)

        modular_results[modulus] = {
            "purity_trials": RANDOM_TENSOR_TRIALS,
            "pair_profile": list(profile_p),
            "family_tangent_rank": tangent_rank,
            "family_tangent_rank_parameters_only": tangent_params_rank,
            "family_tangent_minor": tangent_minor,
            "incidence_jacobian_rank": incidence_rank,
            "incidence_minor": incidence_minor,
        }

    # -------- modular slice replay (consistency check) ---------------
    zvars = sp.symbols("Z0:16")
    universal = chart_planes(list(zvars))
    word_polynomials = {
        word: sp.expand(
            permanent_dp(
                tuple(tuple(universal[mode][word[mode]]) for mode in range(4))
            )
        )
        for word in WORDS
    }
    for modulus in AUDIT_PRIMES:
        dimension, seconds = modular_slice(modulus, word_polynomials, zvars)
        assert dimension == 0
        modular_results[modulus]["slice_local_dimension"] = dimension
        modular_results[modulus]["slice_singular_seconds"] = round(
            seconds, 2
        )

    result = {
        "audited": True,
        "independent_of_primary_imports": True,
        "field": "Q",
        "method": (
            "subset-DP permanent, independently reconstructed exact "
            "chart/point data, two-prime modular replay of purity, "
            "profile, split-plane facts, tangent and incidence "
            "Jacobians (dual numbers), and a two-prime Singular ds "
            "slice consistency check with the shift performed by a "
            "ring map inside Singular"
        ),
        "char0_slice_is_the_certificate": True,
        "modular_slice_is_consistency_check_only": True,
        "free_chart_words": {
            "0110": "2*(p2*q3 + p3*q2)",
            "1110": "(p3 + q3) - k*(p2 + q2)",
            "0111": "(p3 + q3) + k*(p2 + q2)",
        },
        "pure_coefficients_on_tie": {
            "0110": "2*(p2*q3 + p3*q2), q3 = -k*(p2+q2)-p3",
            "1110": "-2*k*(p2 + q2)",
        },
        "chart_support": "the eight words with bit3=0 (values -100/-32)",
        "chart_anchor": "0000",
        "chart_anchor_value": "-100",
        "chart_ratios": [str(value) for value in EXPECTED_RATIOS],
        "coordinate_point": [str(value) for value in COORDINATE_POINT],
        "family_tangent_rank": 5,
        "family_tangent_minor": str(FAMILY_MINOR),
        "incidence_jacobian_rank": 14,
        "incidence_tangent_dimension": 6,
        "incidence_minor": str(INCIDENCE_MINOR),
        "pair_profile": [3, 3, 3, 4, 3, 3],
        "rank_sum": 19,
        "fivefold_sample_rank_sums": fivefold_rank_sums,
        "split_pair_facts": (
            "U0 and U3 meet both P01 and span(e2,e3); middle planes do "
            "not meet two complementary coordinate planes"
        ),
        "thirteenth_sample_support": ["0110"],
        "thirteenth_sample_value": "-120",
        "thirteenth_sample_no_split_plane": True,
        "modular_replay": {
            str(modulus): values
            for modulus, values in modular_results.items()
        },
        "component_dimension": 5,
        "certified_pure_component_orbit_count": 13,
        "generic_H31_excluded": False,
        "generic_weighted_H22_excluded": False,
        "all_pure_components_classified": False,
        "global_problem_resolved": False,
        "elapsed_seconds": round(time.time() - started, 2),
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = REPO_ROOT / "tmp" / "p4_split_pair_pure_component_audit.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
