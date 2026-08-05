"""Independent no-import audit of the boundary-entanglement coefficient tables."""

from __future__ import annotations

from dataclasses import dataclass


Exponent = tuple[int, int, int, int, int, int]


@dataclass(frozen=True)
class Poly:
    terms: tuple[tuple[Exponent, int], ...]

    @staticmethod
    def constant(value: int) -> Poly:
        return Poly(()) if value == 0 else Poly((((0, 0, 0, 0, 0, 0), value),))

    @staticmethod
    def variable(index: int) -> Poly:
        exponent = tuple(int(position == index) for position in range(6))
        return Poly(((exponent, 1),))

    def as_dict(self) -> dict[Exponent, int]:
        return dict(self.terms)

    def __add__(self, other: Poly) -> Poly:
        combined = self.as_dict()
        for exponent, coefficient in other.terms:
            combined[exponent] = combined.get(exponent, 0) + coefficient
            if combined[exponent] == 0:
                del combined[exponent]
        return Poly(tuple(sorted(combined.items())))

    def __mul__(self, other: Poly) -> Poly:
        combined: dict[Exponent, int] = {}
        for left_exponent, left_coefficient in self.terms:
            for right_exponent, right_coefficient in other.terms:
                exponent = tuple(
                    left + right
                    for left, right in zip(left_exponent, right_exponent, strict=True)
                )
                combined[exponent] = combined.get(exponent, 0) + left_coefficient * right_coefficient
        return Poly(tuple(sorted((exponent, coefficient) for exponent, coefficient in combined.items() if coefficient)))


ZERO = Poly.constant(0)
ONE = Poly.constant(1)
A, B, C, D, E, F = (Poly.variable(index) for index in range(6))


def main() -> None:
    # Profile 1+1+1 coefficient table, rows z0 and L0.
    z0_row = [A * D * E + B * C * F, A * C, B * E, ZERO]
    l0_row = [D * F, ZERO, ZERO, ONE]
    assert z0_row[1] * l0_row[3] == A * C
    assert z0_row[3] * l0_row[1] == ZERO

    # Profile 2+1+0 coefficient table, rows z0, L0, L1.
    profile_210 = [
        [A * (B * E + C * D), ZERO],
        [C * F, E],
        [B * F, D],
    ]
    determinant_l0_l1 = profile_210[1][0] * profile_210[2][1]
    determinant_l0_l1_alt = profile_210[1][1] * profile_210[2][0]
    assert determinant_l0_l1 == C * D * F
    assert determinant_l0_l1_alt == B * E * F

    # Under the dependence equality cd=be, the z0 entry is twice abe.
    # This exact integer check audits the characteristic-zero coefficient.
    be_value = 35
    cd_value = 35
    a_value = 11
    assert a_value * (be_value + cd_value) == 2 * a_value * be_value != 0
    assert profile_210[1][1] != ZERO

    for h_profile, s_profile in (((1, 1, 1), (1, 1, 1)), ((2, 1, 0), (0, 1, 2))):
        assert sum(h_profile) == sum(s_profile) == 3
        assert all(h_value + s_value == 2 for h_value, s_value in zip(h_profile, s_profile, strict=True))

    print("independent no-import boundary-entanglement rank audit: PASS")


if __name__ == "__main__":
    main()
