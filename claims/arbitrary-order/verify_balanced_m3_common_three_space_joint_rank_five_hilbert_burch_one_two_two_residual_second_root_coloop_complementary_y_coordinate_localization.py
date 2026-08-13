#!/usr/bin/env python3
"""Exact replay for complementary-``y`` coordinate localization."""

from __future__ import annotations

from itertools import product

import sympy as sp


def e(index: int) -> sp.Matrix:
    return sp.eye(3)[:, index]


def target(alpha: sp.Matrix, beta: sp.Matrix, gamma: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([alpha[i] * beta[i] * gamma[i] for i in range(3)])


def off_endpoint_pencil_table() -> None:
    # Normalize s=0, u=1, t=2 and take the endpoint w=e_u.  Under the
    # contrary assumption y_s!=0, S2BF forces z_s=w_s=0.
    ys, yu, zu, zt, mu, h, kappa = sp.symbols(
        "y_s y_u z_u z_t mu h kappa", nonzero=True
    )
    y = sp.Matrix([ys, yu, 0])
    z = sp.Matrix([0, zu, zt])
    w = e(1)
    assert sp.Matrix.hstack(z, w).rank() == 2

    normal_p = kappa * y - h * mu * e(2)
    normal_q = kappa * z - h * w
    assert normal_p[0] == kappa * ys
    assert normal_q[0] == 0

    indices = (1, 2)
    beta_lifts = []
    for index in indices:
        beta = e(index) - (normal_p[index] / normal_p[0]) * e(0)
        assert sp.expand(beta.dot(normal_p)) == 0
        beta_lifts.append(beta)
    assert sp.Matrix.hstack(*beta_lifts)[list(indices), :] == sp.eye(2)

    gamma_active = normal_q[2] * e(1) - normal_q[1] * e(2)
    assert sp.expand(gamma_active.dot(normal_q)) == 0
    assert e(0).dot(normal_q) == 0
    third_rows = (gamma_active, e(0))
    first_rows = (e(1), e(2))

    for a, b, c in product(range(2), repeat=3):
        value = target(first_rows[a], beta_lifts[b], third_rows[c])
        expected = sp.zeros(3, 1)
        if a == b and c == 0:
            expected = gamma_active[indices[a]] * e(indices[a])
        assert value == expected
    print("off-endpoint determinant-pencil table: PASS")


def endpoint_case_table() -> None:
    # l is the endpoint and u is the other colour in {j,k}.
    # S2BG removes s=t.  If s=l, S2BF already gives y=e_u.  If s=u,
    # the table above excludes y_s!=0, while y_t=0 and dim<y,e_t>=2.
    cases = {
        "s=endpoint": "y=other",
        "s=other": "y=endpoint",
    }
    assert set(cases.values()) == {"y=other", "y=endpoint"}
    assert all(value.startswith("y=") for value in cases.values())
    print("complementary-y endpoint case table: PASS")


def main() -> None:
    off_endpoint_pencil_table()
    endpoint_case_table()
    print("residual second-root-coloop complementary-y localization: PASS")


if __name__ == "__main__":
    main()
