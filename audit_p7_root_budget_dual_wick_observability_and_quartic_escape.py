"""Independent no-import audit of the P7 dual-Wick observability boundary.

Rational forward-mode differentiation checks the dominance minor.  Separate
integer linear algebra checks the selector kernel and legal counterchannels.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import cache

EDGE_LIST = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
COMPLEMENT = (5, 4, 3, 2, 1, 0)
STAR = (
    (1, 1, 1, 0, 0, 0),
    (1, 0, 0, 1, 1, 0),
    (0, 1, 0, 1, 0, 1),
    (0, 0, 1, 0, 1, 1),
)


@dataclass(frozen=True)
class Jet:
    value: Fraction
    gradient: tuple[Fraction, ...]

    @staticmethod
    def constant(value, dimension: int) -> Jet:
        return Jet(Fraction(value), (Fraction(0),) * dimension)

    @staticmethod
    def variable(value, index: int, dimension: int) -> Jet:
        gradient = [Fraction(0)] * dimension
        gradient[index] = Fraction(1)
        return Jet(Fraction(value), tuple(gradient))

    @staticmethod
    def coerce(value, dimension: int) -> Jet:
        return value if isinstance(value, Jet) else Jet.constant(value, dimension)

    def __add__(self, other) -> Jet:
        other = self.coerce(other, len(self.gradient))
        return Jet(
            self.value + other.value,
            tuple(left + right for left, right in zip(self.gradient, other.gradient, strict=True)),
        )

    __radd__ = __add__

    def __neg__(self) -> Jet:
        return Jet(-self.value, tuple(-entry for entry in self.gradient))

    def __sub__(self, other) -> Jet:
        return self + (-self.coerce(other, len(self.gradient)))

    def __mul__(self, other) -> Jet:
        other = self.coerce(other, len(self.gradient))
        return Jet(
            self.value * other.value,
            tuple(
                self.value * right + left * other.value
                for left, right in zip(self.gradient, other.gradient, strict=True)
            ),
        )

    __rmul__ = __mul__


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    work = [row[:] for row in matrix]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next(row for row in range(column, len(work)) if work[row][column] != 0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        pivot_value = work[column][column]
        result *= pivot_value
        work[column] = [entry / pivot_value for entry in work[column]]
        for row in range(column + 1, len(work)):
            multiplier = work[row][column]
            if multiplier:
                work[row] = [
                    entry - multiplier * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[column], strict=True)
                ]
    return result


def dot(left, right):
    return sum(a * b for a, b in zip(left, right, strict=True))


def star_values(pair_vector):
    return tuple(dot(row, pair_vector) for row in STAR)


def top_value(pair_vector):
    return (
        pair_vector[0] * pair_vector[5]
        + pair_vector[1] * pair_vector[4]
        + pair_vector[2] * pair_vector[3]
    )


def channel_off_diagonal(left, right):
    return tuple(
        left[i] * right[j] + right[i] * left[j] for i, j in EDGE_LIST
    )


def permanent(matrix: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    @cache
    def recurse(rows: tuple[int, ...], columns: tuple[int, ...]) -> Fraction:
        if not rows:
            return Fraction(1)
        first = rows[0]
        total = Fraction(0)
        for position, column in enumerate(columns):
            total += matrix[first][column] * recurse(
                rows[1:], columns[:position] + columns[position + 1 :]
            )
        return total

    order = len(matrix)
    return recurse(tuple(range(order)), tuple(range(order)))


def dominance_jacobian() -> list[list[Fraction]]:
    # Parameter order: h, six B entries, four a entries, four b entries.
    point = (1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 2, 0, 1, 3, 1)
    dimension = len(point)
    variables = tuple(Jet.variable(value, index, dimension) for index, value in enumerate(point))
    h = variables[0]
    direct = variables[1:7]
    left = variables[7:11]
    right = variables[11:15]
    corrected = tuple(
        left[i] * right[j] + right[i] * left[j] for i, j in EDGE_LIST
    )
    present_pairs = tuple(h * direct[index] + corrected[index] for index in range(6))
    direct_top = top_value(direct)
    present_top = h * direct_top + sum(
        corrected[index] * direct[COMPLEMENT[index]] for index in range(6)
    )
    stars = tuple(
        sum(coefficient * direct[index] for index, coefficient in enumerate(row))
        for row in STAR
    )
    outputs = (h,) + present_pairs + (direct_top, present_top) + stars
    assert len(outputs) == 13
    return [list(output.gradient) for output in outputs]


def main() -> None:
    assert tuple(size for size in (0, 2, 4, 6) if 7 - size <= 5) == (2, 4, 6)
    assert tuple(size for size in (0, 2, 4, 6) if 2 + 7 - size <= 5) == (4, 6)
    assert tuple(size for size in (0, 2, 4, 6) if 7 - size <= 3) == (4, 6)
    assert tuple(size for size in (0, 2, 4, 6) if 4 + 7 - size <= 3) == ()

    jacobian = dominance_jacobian()
    minor = [row[:13] for row in jacobian]
    assert determinant(minor) == 360

    n_s = (-1, 1, 0, 0, 1, -1)
    n_t = (-1, 0, 1, 1, 0, -1)
    assert star_values(n_s) == (0, 0, 0, 0)
    assert star_values(n_t) == (0, 0, 0, 0)
    # The homogeneous top response on n(s,t) is
    # 2(s^2+s*t+t^2); audit three coefficients independently.
    assert top_value(n_s) == 2
    assert top_value(n_t) == 2
    assert top_value(tuple(left + right for left, right in zip(n_s, n_t, strict=True))) == 6

    # One additive complementary weight has vertex potentials (4,2,1,0).
    z_pairs = (1, 2, 3, 4, 5, 6)
    assert z_pairs[0] + z_pairs[5] == z_pairs[1] + z_pairs[4]
    assert z_pairs[1] + z_pairs[4] == z_pairs[2] + z_pairs[3]
    weight = (z_pairs[5], z_pairs[4], z_pairs[3], z_pairs[2], z_pairs[1], z_pairs[0])
    potentials = (4, 2, 1, 0)
    recovered_weight = tuple(potentials[left] + potentials[right] for left, right in EDGE_LIST)
    assert recovered_weight == weight
    assert dot(weight, n_s) == dot(weight, n_t) == 0
    nonadditive_weight = (1, 0, 0, 0, 0, 0)
    assert (dot(nonadditive_weight, n_s), dot(nonadditive_weight, n_t)) != (0, 0)

    b_zero = n_s
    b_one = n_t
    u_zero, v_zero = (1, 0, 0, -1), (0, -1, 1, 0)
    u_one, v_one = (1, 0, -1, 0), (0, -1, 0, 1)
    assert channel_off_diagonal(u_zero, v_zero) == b_zero
    assert channel_off_diagonal(u_one, v_one) == b_one
    residual_edge = Fraction(3)
    visible = []
    for pair_vector, u_vector, v_vector in (
        (b_zero, u_zero, v_zero),
        (b_one, u_one, v_one),
    ):
        corrected = channel_off_diagonal(
            tuple(-residual_edge * entry for entry in u_vector), v_vector
        )
        assert corrected == tuple(-residual_edge * entry for entry in pair_vector)
        present_pairs = tuple(
            residual_edge * direct + correction
            for direct, correction in zip(pair_vector, corrected, strict=True)
        )
        direct_top = top_value(pair_vector)
        present_top = residual_edge * direct_top + sum(
            corrected[index] * pair_vector[COMPLEMENT[index]] for index in range(6)
        )
        visible.append(
            (residual_edge, present_pairs, direct_top, present_top, star_values(pair_vector))
        )
    assert b_zero != b_one
    assert visible[0] == visible[1]
    assert visible[0] == (residual_edge, (0,) * 6, 2, -2 * residual_edge, (0,) * 4)

    identity = tuple(
        tuple(Fraction(int(row == column)) for column in range(4)) for row in range(4)
    )
    assert permanent(identity) == 1

    print("independent P7 root-budget observability audit: PASS")
    print("dominance_minor=360")
    print("star_kernel_and_additive_selector=PASS")
    print("legal_counterresponse_pair=PASS")
    print("q4_quartic_identity_permanent=1")
    print("enumerations=0")


if __name__ == "__main__":
    main()
