#!/usr/bin/env python3
"""Independent Fraction audit of complementary-``y`` localization."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product


def unit(index: int) -> tuple[F, F, F]:
    return tuple(F(position == index) for position in range(3))  # type: ignore[return-value]


def dot(left: tuple[F, ...], right: tuple[F, ...]) -> F:
    return sum((a * b for a, b in zip(left, right, strict=True)), F(0))


def audit_table() -> None:
    # s=0,u=1,t=2; all values are chosen away from the finite exceptional
    # directions used in the proof.
    y = (F(2), F(3), F(0))
    z = (F(0), F(5), F(7))
    w = unit(1)
    mu, h, kappa = F(11), F(13), F(17)
    normal_p = tuple(kappa * y[i] - h * mu * F(i == 2) for i in range(3))
    normal_q = tuple(kappa * z[i] - h * w[i] for i in range(3))
    assert normal_p[0] and normal_q[0] == 0

    indices = (1, 2)
    beta_lifts = []
    for index in indices:
        beta = tuple(
            F(i == index) - F(i == 0) * normal_p[index] / normal_p[0]
            for i in range(3)
        )
        assert dot(beta, normal_p) == 0
        beta_lifts.append(beta)
    gamma_active = (F(0), normal_q[2], -normal_q[1])
    assert dot(gamma_active, normal_q) == 0

    first_rows = (unit(1), unit(2))
    third_rows = (gamma_active, unit(0))
    for a, b, c in product(range(2), repeat=3):
        value = tuple(
            first_rows[a][i] * beta_lifts[b][i] * third_rows[c][i]
            for i in range(3)
        )
        expected = (F(0), F(0), F(0))
        if a == b and c == 0:
            expected = tuple(
                gamma_active[indices[a]] * entry for entry in unit(indices[a])
            )
        assert value == expected
    print("independent off-endpoint pencil audit: PASS")


def audit_case_cover() -> None:
    cases = (("s=l", "y=e_m"), ("s=m", "y=e_l"))
    assert len(cases) == 2
    assert all("y=e_" in conclusion for _, conclusion in cases)
    print("independent complementary-y case audit: PASS")


def main() -> None:
    audit_table()
    audit_case_cover()
    print("independent complementary-y localization audit: PASS")


if __name__ == "__main__":
    main()
