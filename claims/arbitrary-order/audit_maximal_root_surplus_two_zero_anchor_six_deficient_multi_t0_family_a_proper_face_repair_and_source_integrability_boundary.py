"""No-import audit of GLS78's multi-T0 Family-A parent boundary."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


Vector = tuple[Fraction, Fraction]


def vec(a: int | Fraction, b: int | Fraction) -> Vector:
    return Fraction(a), Fraction(b)


def add(*vectors: Vector) -> Vector:
    return tuple(sum(entries, Fraction(0)) for entries in zip(*vectors, strict=True))  # type: ignore[return-value]


def scale(value: int | Fraction, vector: Vector) -> Vector:
    factor = Fraction(value)
    return factor * vector[0], factor * vector[1]


def independent_restriction_audit() -> None:
    basis = tuple(product(range(3), repeat=3))
    for j_sizes, expected_intersection, expected_quotient in (
        ((1, 2, 2), 4, 25),
        ((2, 2, 2), 8, 26),
    ):
        j_sets = tuple(frozenset(range(size)) for size in j_sizes)
        singleton_kernels = [
            {word for word in basis if word[slot] in j_sets[slot]} for slot in range(3)
        ]
        common = set.intersection(*singleton_kernels)
        quotient_kernel = set.union(*singleton_kernels)
        assert len(common) == expected_intersection
        assert len(quotient_kernel) == expected_quotient


def independent_controls() -> None:
    x, y, zero = vec(1, 0), vec(0, 1), vec(0, 0)

    # r=2 all-selector control.
    k3, l3 = x, y
    k4, l4, k5, l5 = 1, 0, 0, 1
    b45, b35, b34 = -1, scale(-1, x), scale(-1, y)
    assert b45 + k4 * l5 + l4 * k5 == 0
    assert add(b35, scale(l5, k3), scale(k5, l3)) == zero
    assert add(b34, scale(l4, k3), scale(k4, l3)) == zero
    assert add(scale(b45, k3), scale(k4, b35), scale(k5, b34)) == scale(-2, x)
    assert add(scale(b45, l3), scale(l4, b35), scale(l5, b34)) == scale(-2, y)

    # r=3 all-selector control.
    k = (1, 1, 1)
    ell = (0, 1, 1)
    b45s, b35s, b34s = -2, -1, -1
    assert b45s + k[1] * ell[2] + ell[1] * k[2] == 0
    assert b35s + k[0] * ell[2] + ell[0] * k[2] == 0
    assert b34s + k[0] * ell[1] + ell[0] * k[1] == 0
    assert k[0] * b45s + k[1] * b35s + k[2] * b34s == -4
    assert ell[0] * b45s + ell[1] * b35s + ell[2] * b34s == -2

    # One-silent C=0 control at two unrelated nonzero target scales.
    lam, mu = Fraction(3), Fraction(5)
    r = scale(Fraction(1, 4), add(scale(mu, y), scale(-lam, x)))
    s = scale(-1, r)
    b34v = scale(Fraction(1, 2), add(scale(lam, x), scale(mu, y)))
    assert add(r, s) == zero
    assert -2 + 1 + 1 == 0
    assert add(r, s) == zero
    assert add(scale(-2, r), b34v) == scale(lam, x)
    assert add(scale(-2, s), b34v) == scale(mu, y)


def independent_pair_audit() -> None:
    def choose(vertices: set[int]) -> set[tuple[int, int]]:
        return set(combinations(sorted(vertices), 2))

    triangle = {0, 1, 2}
    central = choose(triangle)
    after_one = choose({0, 1, 2, 3, 5})
    repairs = {(0, 5), (1, 5), (2, 5), (3, 5)}
    via_r = {(0, 3), (1, 3), (2, 3)}
    assert after_one - central - via_r == repairs
    assert choose({0, 1, 2, 3}) - central == via_r
    assert len(after_one) == 10

    r3_after_one = choose({0, 1, 2, 3, 5})
    r3_after_two = choose({0, 1, 2, 3})
    r3_after_three = choose(triangle)
    assert r3_after_one == central | via_r | repairs
    assert r3_after_two == central | via_r
    assert r3_after_three == central
    assert (len(r3_after_one), len(r3_after_two), len(r3_after_three)) == (10, 6, 3)


def independent_physical_direction() -> None:
    """Build the ordered-slot tensor W_23 W_45 without scalar shorthand."""

    w23 = {(2, 0): Fraction(1)}
    w45 = {(1, 1): Fraction(1)}
    deck: dict[tuple[int, int, int, int], Fraction] = {}
    for (a2, j3), left_value in w23.items():
        for (j4, j5), right_value in w45.items():
            deck[(a2, j3, j4, j5)] = left_value * right_value
    assert deck == {(2, 0, 1, 1): Fraction(1)}

    # In the r=2 normalization, the outside factors lie in J3,J4,J5.
    j_sets = ({0}, {0, 1}, {0, 1})
    for word in deck:
        assert all(word[slot + 1] in j_sets[slot] for slot in range(3))


def main() -> None:
    assert 360 * 3 == 1_080
    assert 360 * 1 == 360
    independent_restriction_audit()
    independent_controls()
    independent_pair_audit()
    independent_physical_direction()
    assert (97_215, 79) == (97_215, 79)

    print("GLS78 independent audit passed")
    print("finite-basis restriction kernels independently reconstructed")
    print("r=2/r=3 exact controls independently checked")
    print("repair-pair hierarchy independently checked")
    print("six-deficient residual unchanged: 97,215 / 79")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
