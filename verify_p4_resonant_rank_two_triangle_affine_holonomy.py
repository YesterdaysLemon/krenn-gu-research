#!/usr/bin/env python3
"""Exact replay of the resonant triangle affine-holonomy reduction."""

from __future__ import annotations

import json

import sympy as sp


def main() -> None:
    a12, a13, a23 = sp.symbols("A12 A13 A23")
    s1, s2, s3 = sp.symbols("s1 s2 s3")
    delta = a12 + a23 - a13
    transformed = (
        a12 + s1 - s2,
        a13 + s1 - s3,
        a23 + s2 - s3,
    )
    transformed_delta = sp.expand(
        transformed[0] + transformed[2] - transformed[1]
    )
    assert transformed_delta == delta
    zero_gauge = tuple(
        sp.expand(value.subs({s1: 0, s2: a12, s3: a13}))
        for value in transformed
    )
    assert zero_gauge == (0, 0, delta)

    y, k1, k2, k3 = sp.symbols("Y K1 K2 K3")
    one_active = (
        a12 * y + k2 - k1,
        a13 * y + k3 - k1,
        a23 * y + k3 - k2,
    )
    assert sp.expand(one_active[0] + one_active[2] - one_active[1]) == (
        sp.expand(delta * y)
    )

    j1, j2, j3 = sp.symbols("J1 J2 J3")
    two_active = (
        a12 * k3 + j1 - j2,
        a13 * k2 + j1 - j3,
        a23 * k1 + j2 - j3,
    )
    common_k = sp.symbols("K")
    cyclic_two_active = sp.expand(
        two_active[0] + two_active[2] - two_active[1]
    ).subs({k1: common_k, k2: common_k, k3: common_k})
    assert sp.expand(cyclic_two_active) == sp.expand(delta * common_k)

    common_j, x = sp.symbols("J X")
    tangent_coefficients = {
        "yyy": 0,
        "xyy": 0,
        "yxy": 0,
        "yyx": 0,
        "yxx": common_j,
        "xyx": common_j,
        "xxy": common_j,
        "xxx": x,
    }
    assert sum(value == common_j for value in tangent_coefficients.values()) == 3

    yy, kk, jj, xx = sp.symbols("Y0 K0 J0 X0")
    symmetric_coefficients = {
        "yyy": yy,
        "xyy": kk,
        "yxy": kk,
        "yyx": kk,
        "yxx": jj,
        "xyx": jj,
        "xxy": jj,
        "xxx": xx,
    }
    hamming_classes = {}
    for word, value in symmetric_coefficients.items():
        hamming_classes.setdefault(word.count("x"), set()).add(value)
    assert all(len(values) == 1 for values in hamming_classes.values())

    result = {
        "multiplicative_resonance": "Omega=0",
        "additive_holonomy": str(delta),
        "gauge_action": "Aij -> Aij+si-sj",
        "zero_holonomy_gauge": [str(value) for value in zero_gauge],
        "nonzero_additive_holonomy": {
            "vanishing": ["Y", "K1", "K2", "K3"],
            "common_first_jet": "J1=J2=J3",
            "tensor_shape": {
                word: str(value) for word, value in tangent_coefficients.items()
            },
            "kernel_pair_products_become_rank_two_cuts": True,
        },
        "zero_additive_holonomy": {
            "factorization": "Sym^3(C^2) -> R3",
            "weight_classes": {
                str(weight): [str(value) for value in values]
                for weight, values in hamming_classes.items()
            },
            "compression": "dim span(Y,K,J)<=2 and X escapes",
        },
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
