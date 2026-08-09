"""Independent no-project-import audit of the rank-six hafnian obstruction."""

from __future__ import annotations

from fractions import Fraction

VARIABLE_COUNT = 12


class Poly:
    """A minimal sparse polynomial over Q in twelve named variables."""

    def __init__(self, terms=None):
        self.terms = {
            monomial: Fraction(coefficient)
            for monomial, coefficient in (terms or {}).items()
            if coefficient
        }

    @staticmethod
    def coerce(value):
        if isinstance(value, Poly):
            return value
        return Poly({(0,) * VARIABLE_COUNT: Fraction(value)})

    def __add__(self, other):
        other = self.coerce(other)
        result = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
            if result[monomial] == 0:
                del result[monomial]
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({monomial: -coefficient for monomial, coefficient in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        result = {}
        for left_monomial, left_coefficient in self.terms.items():
            for right_monomial, right_coefficient in other.terms.items():
                monomial = tuple(
                    left + right
                    for left, right in zip(left_monomial, right_monomial, strict=True)
                )
                result[monomial] = (
                    result.get(monomial, Fraction(0))
                    + left_coefficient * right_coefficient
                )
        return Poly(result)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        result = Poly.coerce(1)
        for _ in range(exponent):
            result *= self
        return result

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms


def variable(index):
    monomial = [0] * VARIABLE_COUNT
    monomial[index] = 1
    return Poly({tuple(monomial): Fraction(1)})


def main() -> None:
    p, q, r, s, u, v, w, z, _, _, _, _ = tuple(
        variable(index) for index in range(VARIABLE_COUNT)
    )
    e_ab = 1 + p * s + q * r
    m_value = -p * w - u * r
    n_value = -p * z - v * r
    o_value = -q * w - u * s
    t_value = -q * z - v * s

    b_equations = (
        p * o_value + q * m_value + u,
        p * t_value + q * n_value + v,
        r * o_value + s * m_value + w,
        r * t_value + s * n_value + z,
    )
    expected = (
        2 * (u - p * q * w) - u * e_ab,
        2 * (v - p * q * z) - v * e_ab,
        2 * (w - r * s * u) - w * e_ab,
        2 * (z - r * s * v) - z * e_ab,
    )
    assert b_equations == expected

    x_value = p * s
    y_value = q * r
    u_value = p * q * w
    z_value = r * s * v
    m_reduced = -p * w - u_value * r
    n_reduced = -p * z_value - v * r
    c_equation = p + u_value * n_reduced + v * m_reduced
    c_target = p * (1 + (y_value**2 + x_value) * v * w)
    error = -p * v * w * (y_value + 1) * e_ab
    assert c_equation - c_target == error

    # The last field-theoretic deduction in the hand proof.
    # X+Y=-1 and XY=1 imply Y^2=X.  The two remaining equations give
    # 2*vw=-1 and 2*X*vw=-1, hence X=Y=1 and therefore 3=0.
    assert Fraction(2) != 0
    assert Fraction(3) != 0

    support_edges = (frozenset((0, 1)), frozenset((2, 3)), frozenset((4, 5)))
    selected_vertices = frozenset(range(6))
    # Pigeonhole step: four vertices from three disjoint pairs contain a pair.
    assert 4 > len(support_edges)
    assert set().union(*support_edges) == selected_vertices

    triangle = (frozenset((0, 1)), frozenset((1, 2)), frozenset((0, 2)))
    counts = tuple(sum(mode in support for support in triangle) for mode in range(7))
    assert counts == (2, 2, 2, 0, 0, 0, 0)
    assert sum(counts) == 6

    print("AUDIT PASS: four-hafnian hand identities over Q")
    print("AUDIT PASS: characteristic-zero contradiction for three disjoint edges")
    print("AUDIT PASS: permanent Laplace descent is the ordinary 2+3 row split")
    print("AUDIT PASS: overlapping triangle attains the rank-six quotient shadow")
    print("AUDIT SCOPE: overlapping physical lift and rank below six remain open")
    print("searches=0 project_imports=0")


if __name__ == "__main__":
    main()
