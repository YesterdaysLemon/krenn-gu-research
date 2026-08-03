"""Independent stdlib audit for exceptional P7 restricted Hessians."""

from fractions import Fraction
from itertools import combinations


def poly_clean(poly):
    return {key: value for key, value in poly.items() if value}


def poly_const(value):
    value = Fraction(value)
    return {} if not value else {(0, 0): value}


def poly_var(which):
    return {(1, 0) if which == 0 else (0, 1): Fraction(1)}


def poly_add(left, right):
    result = dict(left)
    for key, value in right.items():
        result[key] = result.get(key, Fraction(0)) + value
    return poly_clean(result)


def poly_scale(value, poly):
    return poly_clean({key: Fraction(value) * item for key, item in poly.items()})


def poly_mul(left, right):
    result = {}
    for (i, j), x in left.items():
        for (k, ell), y in right.items():
            key = (i + k, j + ell)
            result[key] = result.get(key, Fraction(0)) + x * y
    return poly_clean(result)


class Rat:
    def __init__(self, numerator, denominator=None):
        self.numerator = numerator
        self.denominator = denominator if denominator is not None else poly_const(1)

    @classmethod
    def constant(cls, value):
        return cls(poly_const(value))

    def __add__(self, other):
        other = as_rat(other)
        return Rat(
            poly_add(
                poly_mul(self.numerator, other.denominator),
                poly_mul(other.numerator, self.denominator),
            ),
            poly_mul(self.denominator, other.denominator),
        )

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return Rat(poly_scale(-1, self.numerator), self.denominator)

    def __sub__(self, other):
        return self + (-as_rat(other))

    def __rsub__(self, other):
        return as_rat(other) - self

    def __mul__(self, other):
        other = as_rat(other)
        return Rat(
            poly_mul(self.numerator, other.numerator),
            poly_mul(self.denominator, other.denominator),
        )

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        other = as_rat(other)
        return Rat(
            poly_mul(self.numerator, other.denominator),
            poly_mul(self.denominator, other.numerator),
        )

    def __rtruediv__(self, other):
        return as_rat(other) / self

    def __eq__(self, other):
        other = as_rat(other)
        return poly_mul(self.numerator, other.denominator) == poly_mul(
            other.numerator, self.denominator
        )


def as_rat(value):
    return value if isinstance(value, Rat) else Rat.constant(value)


def det2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def det3(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def restriction(outside, clique_size, skipped=frozenset()):
    size = len(outside)
    matrix = [[Rat.constant(0) for _ in range(size)] for _ in range(size)]
    for i, value in enumerate(outside):
        matrix[i][i] = value + clique_size * value / (2 * (1 - value))
    for i, j in combinations(range(size), 2):
        if (i, j) in skipped:
            continue
        weight = outside[i] * outside[j] / (4 - 2 * (outside[i] + outside[j]))
        matrix[i][i] = matrix[i][i] + weight
        matrix[j][j] = matrix[j][j] + weight
        matrix[i][j] = matrix[j][i] = weight
    return matrix


def main():
    b = Rat(poly_var(0))
    c = Rat(poly_var(1))

    k5 = restriction([b, -1 - b], 5)
    assert det2(k5) == 15 * b * (b + 1) / ((b - 1) * (b + 2))

    d = -b - c
    k4 = restriction([b, c, d], 4)
    cubic = 3 * b * c * d + 2 * (b * c + b * d + c * d) + 12
    denominator = (
        (b - 1)
        * (b + 2)
        * (c - 1)
        * (c + 2)
        * (b + c + 1)
        * (b + c - 2)
    )
    assert det3(k4) == 18 * b * c * (b + c) * cubic / denominator

    one_wall = restriction([b, 2 - b, Rat.constant(-2)], 4, frozenset({(0, 1)}))
    projection = [[1, 0], [-1, 0], [0, 1]]
    reduced = [
        [
            sum(
                (
                    as_rat(projection[i][row])
                    * one_wall[i][j]
                    * projection[j][col]
                    for i in range(3)
                    for j in range(3)
                )
                ,
                Rat.constant(0),
            )
            for col in range(2)
        ]
        for row in range(2)
    ]
    assert det2(reduced) == -96 / ((b - 4) * (b + 2))

    # Direct Fraction audit of the K_(1,2) endpoint coefficient.
    outside = [Fraction(4), Fraction(-2), Fraction(-2)]
    skipped = {(0, 1), (0, 2)}
    numeric = [[Fraction(0) for _ in range(3)] for _ in range(3)]
    for i, value in enumerate(outside):
        numeric[i][i] = value + 4 * value / (2 * (1 - value))
    for i, j in combinations(range(3), 2):
        if (i, j) in skipped:
            continue
        weight = outside[i] * outside[j] / (4 - 2 * (outside[i] + outside[j]))
        numeric[i][i] += weight
        numeric[j][j] += weight
        numeric[i][j] = numeric[j][i] = weight
    vector = [Fraction(1), Fraction(-1), Fraction(-1)]
    value = sum(
        vector[i] * numeric[i][j] * vector[j]
        for i in range(3)
        for j in range(3)
    )
    assert value == -4

    print("AUDIT PASS: independent bivariate rational arithmetic rebuilds K5 exclusion")
    print("AUDIT PASS: midpoint K4 determinant has exactly the retained cubic numerator")
    print("AUDIT PASS: one-outside-wall and K_(1,2) endpoint coefficients are nonzero")
    print("imports_from_primary=0 imports_from_project=0 imports_from_sympy=0")
    print("searches=0 finite_fields=0 numerical_points=0 wall_enumerations=0")
    print("SCOPE: K4 cubic, K3, bipartite walls, P7, and global Krenn-Gu unresolved")


if __name__ == "__main__":
    main()
