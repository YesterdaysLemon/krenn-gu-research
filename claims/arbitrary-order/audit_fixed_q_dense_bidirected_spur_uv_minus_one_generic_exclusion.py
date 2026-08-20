"""Recursive-permanent audit of the GLD32 generic uv=-1 divisor detector."""

from __future__ import annotations

import sympy as sp

from audit_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion import (
    equation as audit_equation,
)
from verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion import (
    U,
    V,
    W,
    Z,
    equation as direct_equation,
)
from verify_fixed_q_dense_bidirected_spur_uv_minus_one_generic_exclusion import (
    KEYS,
    MULTIPLIERS,
)


def main():
    substitutions = {V: -1 / U}
    combined, rhs = {}, 0
    for row_key, multiplier in zip(KEYS, MULTIPLIERS, strict=True):
        audit_row, audit_rhs = audit_equation(*row_key)
        direct_row, direct_rhs = direct_equation(*row_key)
        assert all(
            sp.expand(audit_row.get(index, 0) - direct_row.get(index, 0)) == 0
            for index in set(audit_row) | set(direct_row)
        )
        assert sp.expand(audit_rhs - direct_rhs) == 0
        for index, coefficient in audit_row.items():
            combined[index] = sp.factor(
                combined.get(index, 0) + multiplier * coefficient.subs(substitutions)
            )
        rhs = sp.factor(rhs + multiplier * audit_rhs.subs(substitutions))
    combined = {index: value for index, value in combined.items() if value != 0}
    detector = -2 * U * W * Z**2 * (U - 1) * (Z - 1) * (Z + 1) * (W * Z - 2)
    assert not combined
    assert sp.factor(rhs - detector) == 0
    print("PASS: recursive-permanent audit derives all 14 GLD32 rows and the divisor detector")


if __name__ == "__main__":
    main()
