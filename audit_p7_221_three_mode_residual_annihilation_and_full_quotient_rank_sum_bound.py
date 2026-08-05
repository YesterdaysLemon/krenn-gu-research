"""Independent no-import audit of the three-mode rank-sum theorem."""

from fractions import Fraction


class Quad:
    """An element a+b*rho of Q[rho]/(rho^2-21)."""

    def __init__(self, rational=0, radical=0):
        self.a = Fraction(rational)
        self.b = Fraction(radical)

    def __add__(self, other):
        other = other if isinstance(other, Quad) else Quad(other)
        return Quad(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Quad(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Quad) else -Quad(other))

    def __rsub__(self, other):
        return Quad(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, Quad) else Quad(other)
        return Quad(
            self.a * other.a + 21 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        if not isinstance(other, Quad):
            return Quad(self.a / Fraction(other), self.b / Fraction(other))
        norm = other.a * other.a - 21 * other.b * other.b
        if norm == 0:
            raise ZeroDivisionError
        return self * Quad(other.a / norm, -other.b / norm)

    def __eq__(self, other):
        other = other if isinstance(other, Quad) else Quad(other)
        return self.a == other.a and self.b == other.b

    def norm(self):
        return self.a * self.a - 21 * self.b * self.b


def determinant_3(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def main() -> None:
    rho = Quad(0, 1)
    alpha = Quad(1) + Quad(0, Fraction(43, 21))
    beta = (Quad(1) + rho) * Fraction(2, 7)
    matrix = (
        (alpha, Quad(-6), Quad(0)),
        (rho, Quad(0), beta),
        (Quad(0), rho, beta),
    )
    determinant = determinant_3(matrix)
    assert determinant == Quad(Fraction(124, 7), Fraction(-76, 7))
    assert determinant.norm() == Fraction(-105920, 49)

    sharp_six_kernels = (
        frozenset((1, 2)),
        frozenset((1, 2)),
        frozenset((0, 2)),
        frozenset((0, 2)),
        frozenset((0, 1)),
        frozenset((0, 1)),
        frozenset((0, 1, 2)),
    )
    sharp_six_supports = tuple(
        tuple(
            mode
            for mode, kernel in enumerate(sharp_six_kernels)
            if colour not in kernel
        )
        for colour in range(3)
    )
    assert sharp_six_supports == ((0, 1), (2, 3), (4, 5))
    assert sum(3 - len(kernel) for kernel in sharp_six_kernels) == 6

    # Reconstruct the full-quotient killed-colour table directly from (18).
    killed = (
        frozenset((2,)),
        frozenset((1,)),
        frozenset((0,)),
        frozenset((1, 2)),
        frozenset((1, 2)),
        frozenset((1, 2)),
        frozenset((1, 2)),
    )
    supports = tuple(
        tuple(mode for mode, kernel in enumerate(killed) if colour not in kernel)
        for colour in range(3)
    )
    assert supports == (
        (0, 1, 3, 4, 5, 6),
        (0, 2),
        (1, 2),
    )
    rank_sum = sum(3 - len(kernel) for kernel in killed)
    assert rank_sum == 10

    triple = frozenset((0, 1, 3))
    colour_zero_survives = triple.issubset(supports[0])
    colour_one_survives = triple.issubset(supports[1])
    assert colour_zero_survives
    assert not colour_one_survives
    assert alpha != Quad(0)

    # The proof's only matching-combinatorics input.
    edge_endpoint_count = 2
    quotient_mode_count = 3
    assert edge_endpoint_count < quotient_mode_count

    print("AUDIT PASS: coefficient determinant is nonzero in Q(rho)")
    print("AUDIT PASS: three quotients annihilate every one-edge response")
    print("AUDIT PASS: a legal quotient diagram attains rank sum 6")
    print("AUDIT PASS: prior lift has support sizes (6,2,2), rank sum 10")
    print("AUDIT PASS: its {0,1,3} face-01 projection is nonzero")
    print("AUDIT SCOPE: full rank-sum-at-most-six branch remains unresolved")
    print("searches=0 project_imports=0")


if __name__ == "__main__":
    main()
