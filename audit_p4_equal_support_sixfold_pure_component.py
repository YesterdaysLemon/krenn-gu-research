#!/usr/bin/env python3
"""Independent exact audit of the equal-support sixfold (C10) component.

Imports NOTHING from the primary verifier.  Recomputes every
coefficient with a subset-dynamic-programming permanent (never
itertools.permutations), rebuilds the family, charts, and universal
incidence data from scratch, and replays:

  * identical purity (closed forms and mixed-word flattening
    identities) symbolically over Q and at randomized parameter
    values modulo the two primes 10007 and 10009;
  * the pair profile (4,4,3,4,3,3) and the coordinate-plane facts
    modulo both primes;
  * the rank-six family tangent (thirteen directions including the
    projective torus) and the rank-THIRTEEN incidence Jacobian
    modulo both primes, by dual-number differentiation and modular
    elimination, recovering the same minors 1/324 and
    16866160640/6561;
  * the SLICE certificate modulo both primes: the eleven multi-flip
    equations are rebuilt via the DP permanent, shifted to the
    sample INSIDE Singular (a ring map, an independent construction
    path from the primary verifier's sympy-side expansion), cut by
    the same six integer hyperplanes, and given a `ds` standard
    basis in characteristic p.  Local dimension zero modulo p is a
    CONSISTENCY CHECK: the characteristic-zero run in the primary
    verifier is the certificate (a mod-p dimension does not imply
    the char-0 dimension; agreement at two independent primes
    corroborates it);
  * the tenth-component distinctness grounding in exact integer /
    small-rational arithmetic: the certificate point
    (b,e,k,m,r)=(2,3,5,7,11) restricts P4 to a nonzero pure tensor
    and has NO coordinate plane, while the C10 sample has exactly
    one (U3), and every C10 point has U3 = span(e2,e3).

The two audit primes 10007 and 10009 divide none of the denominators
or minor numerators relied on (324 = 2^2*3^4, 6561 = 3^8,
16866160640 = 2^12*5*7^7, anchor value 14, ratio denominator 3).
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

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md"
PRIMARY = ROOT / "verify_p4_equal_support_sixfold_pure_component.py"

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
FLATTENINGS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
PIVOTS = ((0, 2), (0, 2), (0, 2), (2, 3))
ANCHOR = (1, 0, 0, 0)

# sample (c0,c1,c2,t,v0,v1,v2,v3,x2,x3) and torus (1,1,1)
SAMPLE = (3, -2, 5, 2, 3, -7, 2, 5, -1, 4)
COORDINATE_POINT = (
    Fraction(7, 3), Fraction(0), Fraction(0), Fraction(-3),
    Fraction(-7, 3), Fraction(1, 3), Fraction(0), Fraction(2),
    Fraction(-7, 3), Fraction(-1, 6), Fraction(0), Fraction(-5),
    Fraction(0), Fraction(0), Fraction(0), Fraction(0),
)
EXPECTED_RATIOS = (Fraction(0), Fraction(0), Fraction(0), Fraction(-1, 3))
FAMILY_MINOR_ROWS = (0, 3, 5, 7, 9, 11)
FAMILY_MINOR_COLUMNS = (0, 1, 2, 3, 4, 5)
FAMILY_MINOR = Fraction(1, 324)
INCIDENCE_MINOR_ROWS = tuple(range(13))
INCIDENCE_MINOR_COLUMNS = (0, 1, 2, 3, 4, 6, 10, 12, 13, 14, 15, 16, 17)
INCIDENCE_MINOR = Fraction(16866160640, 6561)
SLICE_COEFFS = (
    (1, 2, -1, 3, 1, -2, 1, 1, -3, 2, 1, -1, 2, 1, -2, 3),
    (2, -1, 1, 1, -2, 3, 1, -1, 1, 1, -2, 1, 3, -1, 1, -2),
    (1, 1, 2, -3, 1, 1, -1, 2, 1, -2, 3, 1, -1, 1, 1, 2),
    (3, -2, 1, 1, 1, -1, 2, 1, -2, 1, 1, 3, 1, -1, 2, 1),
    (1, 3, -2, 1, 2, 1, 1, -1, 1, 2, -1, 1, 1, 2, -3, 1),
    (2, 1, 1, -1, 3, -2, 1, 1, 2, -1, 1, 1, -2, 3, 1, 1),
)
AUDIT_PRIMES = (10007, 10009)
RANDOM_TENSOR_TRIALS = 24
SINGULAR_TIMEOUT = 900
TENTH_POINT = (2, 3, 5, 7, 11)


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


def family_rows(c0, c1, c2, t, v0, v1, v2, v3, x2, x3):
    return (
        ((v0, -v1, 0, 0), (0, 0, 1, -c0)),
        ((0, 0, 1, -c1), (v0, v1, v2, v3)),
        ((0, 0, 1, -c2), (t * v0, t * v1, x2, x3)),
        ((0, 0, 1, 1), (0, 0, 1, -1)),
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
    """Universal chart planes for the pivots (02),(02),(02),(23)."""
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


def dual_chart_coordinates(values13, modulus):
    """Chart coordinates of the torus-scaled family over dual numbers.

    values13 = (c0,c1,c2,t,v0,v1,v2,v3,x2,x3,T0,T1,T2) as Duals.
    """
    scales = values13[10:] + (Dual(1, 0, modulus),)
    planes = []
    for plane in family_rows(*values13[:10]):
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
    for direction in range(13):
        values = tuple(
            Dual(value, 1 if index == direction else 0, modulus)
            for index, value in enumerate(base)
        )
        coordinates = dual_chart_coordinates(values, modulus)
        columns.append([entry.b for entry in coordinates])
    return [
        [columns[direction][row] for direction in range(13)]
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
        c0 = generator.randrange(modulus)
        c1 = generator.randrange(modulus)
        c2 = generator.randrange(modulus)
        t = generator.randrange(1, modulus)
        v0 = generator.randrange(1, modulus)
        v1 = generator.randrange(1, modulus)
        v2 = generator.randrange(modulus)
        v3 = generator.randrange(modulus)
        x2 = generator.randrange(modulus)
        x3 = generator.randrange(modulus)
        scales = tuple(
            generator.randrange(1, modulus) for _ in range(3)
        ) + (1,)
        rows = [
            [
                [entry * scale % modulus
                 for entry, scale in zip(row, scales)]
                for row in plane
            ]
            for plane in family_rows(c0, c1, c2, t, v0, v1, v2, v3, x2, x3)
        ]
        monomial = scales[0] * scales[1] * scales[2] % modulus
        for word in WORDS:
            value = permanent_dp(
                tuple(tuple(rows[mode][word[mode]]) for mode in range(4))
            ) % modulus
            if word == (1, 1, 1, 0):
                expected = (
                    -2 * t * v0 * v1 * (c0 - 1) * monomial
                ) % modulus
            elif word == (1, 1, 1, 1):
                expected = (
                    -2 * t * v0 * v1 * (c0 + 1) * monomial
                ) % modulus
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


def modular_coordinate_plane_facts(modulus):
    planes = [
        [[entry % modulus for entry in row] for row in plane]
        for plane in family_rows(*SAMPLE)
    ]

    def coordinate_plane(plane, pair):
        complement = tuple(i for i in range(4) if i not in pair)
        off_zero = all(
            plane[row][column] % modulus == 0
            for row in range(2)
            for column in complement
        )
        determinant = (
            plane[0][pair[0]] * plane[1][pair[1]]
            - plane[0][pair[1]] * plane[1][pair[0]]
        ) % modulus
        return off_zero and determinant != 0

    for mode in range(3):
        assert not any(
            coordinate_plane(planes[mode], pair) for pair in PAIRS
        )
    assert coordinate_plane(planes[3], (2, 3))


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
        "ideal J=I," + ",".join(f"s{index}" for index in range(6)) + ";"
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


# ------------------------- exact grounding ---------------------------


def integer_coordinate_plane_count(planes):
    count = 0
    for plane in planes:
        for pair in PAIRS:
            complement = tuple(i for i in range(4) if i not in pair)
            off_zero = all(
                plane[row][column] == 0
                for row in range(2)
                for column in complement
            )
            determinant = (
                plane[0][pair[0]] * plane[1][pair[1]]
                - plane[0][pair[1]] * plane[1][pair[0]]
            )
            if off_zero and determinant != 0:
                count += 1
                break
    return count


def tenth_planes_rows():
    b, e, k, m, r = TENTH_POINT
    return (
        ((1, -1, 0, 0), (0, 1, b, -b * k)),
        ((1, -1, 0, 0), (0, 1, e, -e * k)),
        ((1, 1, 0, 0), (0, 0, 1, k)),
        ((1, m, 0, 0), (0, r, 1, -k)),
    )


def main() -> None:
    started = time.time()

    # -------- symbolic purity replay with the subset-DP permanent ----
    c0, c1, c2, t = sp.symbols("c0 c1 c2 t")
    v0, v1, v2, v3 = sp.symbols("v0 v1 v2 v3")
    x2, x3 = sp.symbols("x2 x3")
    symbolic = tensor_dp(
        family_rows(c0, c1, c2, t, v0, v1, v2, v3, x2, x3)
    )
    assert sp.expand(
        symbolic[(1, 1, 1, 0)] + 2 * t * v0 * v1 * (c0 - 1)
    ) == 0
    assert sp.expand(
        symbolic[(1, 1, 1, 1)] + 2 * t * v0 * v1 * (c0 + 1)
    ) == 0
    for word in WORDS:
        if word not in ((1, 1, 1, 0), (1, 1, 1, 1)):
            assert sp.expand(symbolic[word]) == 0
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
    support = {word for word, value in point_tensor.items() if value != 0}
    assert support == {(1, 0, 0, 0), (1, 0, 0, 1)}
    assert point_tensor[(1, 0, 0, 0)] == Fraction(14)
    assert point_tensor[(1, 0, 0, 1)] == Fraction(-14, 3)
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

    # -------- tenth-component grounding, exact integers --------------
    tenth = tenth_planes_rows()
    b, e, k, m, r = TENTH_POINT
    tenth_tensor = tensor_dp(tenth)
    tenth_support = {
        word for word, value in tenth_tensor.items() if value != 0
    }
    assert tenth_support == {(1, 1, 0, 0), (1, 1, 0, 1)}
    assert tenth_tensor[(1, 1, 0, 0)] == -2 * b * e * k * (m + 1)
    assert tenth_tensor[(1, 1, 0, 1)] == -2 * k * (b * e * r + b + e)
    mixed_word_purity(tenth_tensor)
    assert integer_coordinate_plane_count(tenth) == 0
    assert integer_coordinate_plane_count(family_rows(*SAMPLE)) == 1

    # -------- modular replay at the two audit primes -----------------
    modular_results = {}
    for modulus in AUDIT_PRIMES:
        modular_purity_trials(modulus)
        profile = modular_pair_profile(modulus)
        assert profile == (4, 4, 3, 4, 3, 3)
        assert sum(profile) == 21
        modular_coordinate_plane_facts(modulus)

        tangent = modular_family_tangent(modulus)
        tangent_rank = modular_rank(tangent, modulus)
        assert tangent_rank == 6
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
        assert incidence_rank == 13      # tangent dimension seven mod p.
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
            "pair_profile": list(profile),
            "family_tangent_rank": tangent_rank,
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
            "profile, coordinate-plane facts, tangent and incidence "
            "Jacobians (dual numbers), and a two-prime Singular ds "
            "slice consistency check with the shift performed by a "
            "ring map inside Singular"
        ),
        "char0_slice_is_the_certificate": True,
        "modular_slice_is_consistency_check_only": True,
        "pure_coefficients": {
            "1110": "-2*t*v0*v1*(c0 - 1)",
            "1111": "-2*t*v0*v1*(c0 + 1)",
        },
        "chart_support": ["1000", "1001"],
        "chart_anchor_value": "14",
        "chart_ratios": [str(value) for value in EXPECTED_RATIOS],
        "coordinate_point": [str(value) for value in COORDINATE_POINT],
        "family_tangent_rank": 6,
        "family_tangent_minor": str(FAMILY_MINOR),
        "incidence_jacobian_rank": 13,
        "incidence_tangent_dimension": 7,
        "incidence_minor": str(INCIDENCE_MINOR),
        "pair_profile": [4, 4, 3, 4, 3, 3],
        "rank_sum": 21,
        "tenth_certificate_point": list(TENTH_POINT),
        "tenth_support": ["1100", "1101"],
        "tenth_coordinate_plane_count": 0,
        "c10_sample_coordinate_plane_count": 1,
        "modular_replay": {
            str(modulus): values
            for modulus, values in modular_results.items()
        },
        "component_dimension": 6,
        "certified_pure_component_orbit_count": 11,
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
    output_path = (
        ROOT / "tmp" / "p4_equal_support_sixfold_pure_component_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
