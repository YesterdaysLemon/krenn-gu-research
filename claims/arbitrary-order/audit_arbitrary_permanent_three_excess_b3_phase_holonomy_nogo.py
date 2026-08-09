"""Independent no-import audit of the B3 phase chart action and countermodel."""

from __future__ import annotations


Permutation = tuple[int, int, int]
Quadratic = tuple[int, int]


def compose(left: Permutation, right: Permutation) -> Permutation:
    return (left[right[0]], left[right[1]], left[right[2]])


def multiply(left: Quadratic, right: Quadratic) -> Quadratic:
    """Multiply a+b*s and c+d*s in Q[s]/(s^2-3)."""
    return (left[0] * right[0] + 3 * left[1] * right[1], left[0] * right[1] + left[1] * right[0])


def add(left: Quadratic, right: Quadratic) -> Quadratic:
    return (left[0] + right[0], left[1] + right[1])


def main() -> None:
    identity = (0, 1, 2)
    t12 = (1, 0, 2)
    t13 = (2, 1, 0)
    t23 = (0, 2, 1)
    r123 = (1, 2, 0)
    r132 = (2, 0, 1)
    group = (identity, t12, t13, t23, r123, r132)

    assert compose(t12, t13) == r132
    assert compose(t12, t23) == r123
    assert compose(r123, t12) == t13
    assert compose(r123, r123) == r132
    assert compose(r123, r132) == identity

    commuting_with_t12 = {perm for perm in group if compose(perm, t12) == compose(t12, perm)}
    commuting_with_r123 = {
        perm for perm in group if compose(perm, r123) == compose(r123, perm)
    }
    assert commuting_with_t12 == {identity, t12}
    assert commuting_with_r123 == {identity, r123, r132}

    # theta=-2+sqrt(3), theta^-1=-2-sqrt(3).
    one = (1, 0)
    theta = (-2, 1)
    theta_inverse = (-2, -1)
    assert multiply(theta, theta_inverse) == one
    total = (0, 0)
    for term in (one, one, one, one, theta, theta_inverse):
        total = add(total, term)
    assert total == (0, 0)
    assert multiply(theta, theta_inverse) == multiply(multiply(one, one), one)

    # The C2 switch ratio is one.  The C3 ratios theta, theta^-2, theta
    # are all different from -1.  theta^-2=(theta_inverse)^2.
    theta_inverse_squared = multiply(theta_inverse, theta_inverse)
    assert one != (-1, 0)
    assert theta != (-1, 0)
    assert theta_inverse_squared != (-1, 0)

    print("independent no-import B3 phase-holonomy audit: PASS")


if __name__ == "__main__":
    main()
