#!/usr/bin/env python3
"""Independent Q(omega) audit for the S2CA mixed support-one exclusion."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product


@dataclass(frozen=True)
class Cyclo:
    """Element a+b*omega of Q(omega), with omega^2+omega+1=0."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    @classmethod
    def make(cls, value: int | Fraction | Cyclo) -> Cyclo:
        if isinstance(value, cls):
            return value
        return cls(Fraction(value), Fraction(0))

    def __add__(self, other: int | Fraction | Cyclo) -> Cyclo:
        rhs = self.make(other)
        return Cyclo(self.a + rhs.a, self.b + rhs.b)

    __radd__ = __add__

    def __neg__(self) -> Cyclo:
        return Cyclo(-self.a, -self.b)

    def __sub__(self, other: int | Fraction | Cyclo) -> Cyclo:
        return self + (-self.make(other))

    def __rsub__(self, other: int | Fraction | Cyclo) -> Cyclo:
        return self.make(other) - self

    def __mul__(self, other: int | Fraction | Cyclo) -> Cyclo:
        rhs = self.make(other)
        return Cyclo(
            self.a * rhs.a - self.b * rhs.b,
            self.a * rhs.b + self.b * rhs.a - self.b * rhs.b,
        )

    __rmul__ = __mul__

    def inverse(self) -> Cyclo:
        norm = self.a * self.a - self.a * self.b + self.b * self.b
        if not norm:
            raise ZeroDivisionError
        return Cyclo((self.a - self.b) / norm, -self.b / norm)

    def __truediv__(self, other: int | Fraction | Cyclo) -> Cyclo:
        return self * self.make(other).inverse()

    def __bool__(self) -> bool:
        return bool(self.a or self.b)


ZERO = Cyclo()
ONE = Cyclo(Fraction(1))
OMEGA = Cyclo(Fraction(0), Fraction(1))
OMEGA2 = OMEGA * OMEGA
N = 3
W_DIM = 9
Vector = tuple[Cyclo, ...]


def zero_vector(size: int) -> Vector:
    return (ZERO,) * size


def unit(size: int, index: int) -> Vector:
    return tuple(ONE if i == index else ZERO for i in range(size))


def add(left: Vector, right: Vector, scale: Cyclo = ONE) -> Vector:
    return tuple(a + scale * b for a, b in zip(left, right, strict=True))


def scale(value: Cyclo, vector: Vector) -> Vector:
    return tuple(value * entry for entry in vector)


def join(*vectors: Vector) -> Vector:
    return tuple(entry for vector in vectors for entry in vector)


def rank(columns: list[Vector]) -> int:
    if not columns:
        return 0
    matrix = [list(row) for row in zip(*columns, strict=True)]
    rows, cols = len(matrix), len(matrix[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next(
            (row for row in range(pivot_row, rows) if matrix[row][col]), None
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][col]
        matrix[pivot_row] = [entry / pivot_value for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][col]:
                continue
            factor = matrix[row][col]
            matrix[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def outer3(a: Vector, b: Vector, c: Vector) -> Vector:
    # Reverse third/second/first storage relative to the primary replay.
    return tuple(a[i] * b[j] * c[k] for k, j, i in product(range(N), repeat=3))


def c_tensor(C: tuple[Vector, ...], c: Vector) -> Vector:
    return tuple(C[i][j] * c[k] for k, j, i in product(range(N), repeat=3))


def derivative(
    x: Vector,
    y: Vector,
    w: Vector,
    C: tuple[Vector, ...],
    a: Vector,
    b: Vector,
    c: Vector,
) -> Vector:
    first = outer3(a, y, w)
    second = outer3(x, b, w)
    third = c_tensor(C, c)
    return tuple(
        left - middle + right
        for left, middle, right in zip(first, second, third, strict=True)
    )


def source_unit(block: int, colour: int) -> Vector:
    return unit(W_DIM, block * N + colour)


def polarized(a: Vector, b: Vector, c: Vector) -> Vector:
    vectors = (a, b, c)
    out = zero_vector(N**3)
    for order in permutations(range(3)):
        left = vectors[order[0]][0:N]
        middle = vectors[order[1]][N : 2 * N]
        right = vectors[order[2]][2 * N : 3 * N]
        out = add(out, outer3(left, middle, right))
    return out


def audit_mixed_four_space() -> None:
    zero = zero_vector(N)
    for d, s, t in permutations(range(N)):
        x = unit(N, s)
        y = add(unit(N, d), unit(N, t))
        b = add(unit(N, d), unit(N, t), Cyclo(Fraction(-1)))
        w = add(unit(N, s), unit(N, t))
        C = tuple(
            tuple(
                ONE if (i == d and j == d) or (i == t and j == s) else ZERO
                for j in range(N)
            )
            for i in range(N)
        )
        derivative_columns = []
        for block in range(3):
            for colour in range(N):
                entries = [zero, zero, zero]
                entries[block] = unit(N, colour)
                derivative_columns.append(derivative(x, y, w, C, *entries))
        assert rank(derivative_columns) == 8

        syzygy = join(x, y, zero)
        vertical = join(zero, zero, unit(N, d))
        split = join(zero, scale(Cyclo(Fraction(-1)), unit(N, s)), zero)
        fourth = join(scale(Cyclo(Fraction(2)), unit(N, t)), b, unit(N, t))
        K = [syzygy, vertical, split, fourth]
        assert rank(K) == 4
        assert [
            rank([vector[block * N : (block + 1) * N] for vector in K])
            for block in range(3)
        ] == [2, 3, 2]
        images = [
            derivative(x, y, w, C, vector[:3], vector[3:6], vector[6:])
            for vector in K
        ]
        assert rank(images) == 3
        assert not any(images[0])

        box = [
            outer3(unit(N, i), unit(N, j), unit(N, k))
            for i in (s, t)
            for j in range(N)
            for k in (d, t)
        ]
        assert rank(box) == 12
        assert rank(box + images[1:]) == 15


def audit_resonance_and_collapse() -> None:
    assert OMEGA2 + OMEGA + ONE == ZERO
    for d, s, t in permutations(range(N)):
        del s
        x = source_unit(0, t)
        y = source_unit(1, t)
        z = source_unit(2, t)
        v = add(add(x, y), z)
        u = add(add(x, scale(OMEGA, y)), scale(OMEGA2, z))
        target_t = outer3(unit(N, t), unit(N, t), unit(N, t))
        target_d = outer3(unit(N, d), unit(N, d), unit(N, d))

        assert not any(polarized(u, v, v))
        assert not any(polarized(u, u, v))
        assert polarized(v, v, v) == scale(Cyclo(Fraction(6)), target_t)

        p_d = scale(Cyclo(Fraction(2)), u)
        p_t = add(scale(Cyclo(Fraction(3)), u), scale(Cyclo(Fraction(5)), v))
        assert not any(polarized(u, p_d, v))
        assert not any(polarized(u, p_t, v))
        assert not any(polarized(v, p_d, v))
        assert polarized(v, p_t, v) == scale(Cyclo(Fraction(30)), target_t)

        tangent = [
            polarized(source_unit(block, colour), v, v)
            for block in range(3)
            for colour in range(N)
        ]
        first_map = [
            polarized(v, u, source_unit(block, colour))
            for block in range(3)
            for colour in range(N)
        ]
        second_map = [
            polarized(u, u, source_unit(block, colour))
            for block in range(3)
            for colour in range(N)
        ]
        assert rank(tangent) == 7
        assert rank(tangent + first_map + second_map) == 7
        assert rank(tangent + [target_d]) == 8

        stacked = [
            join(first_map[index], second_map[index]) for index in range(W_DIM)
        ]
        assert rank(stacked) == 8
        first_at_v = polarized(v, u, v)
        second_at_v = polarized(u, u, v)
        assert not any(first_at_v)
        assert not any(second_at_v)


def audit_scalar_kernel() -> None:
    alpha, beta, gamma = ONE, OMEGA, OMEGA2
    rows = [
        (alpha, beta, gamma),
        (beta * gamma, alpha * gamma, alpha * beta),
    ]
    assert sum(rows[0], ZERO) == ZERO
    assert sum(rows[1], ZERO) == ZERO
    assert rank([tuple(row[index] for row in rows) for index in range(3)]) == 2
    assert all(sum(row, ZERO) == ZERO for row in rows)


def main() -> None:
    audit_mixed_four_space()
    audit_resonance_and_collapse()
    audit_scalar_kernel()
    print(
        "S2CA independent audit passed: reverse derivative box, custom "
        "Q(omega), all colour permutations, resonance, tangent separation, "
        "and one-dimensional dual-row kernel."
    )


if __name__ == "__main__":
    main()
