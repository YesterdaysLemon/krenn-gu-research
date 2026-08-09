"""Verify the third-incidence shell above the unique legal P7 pair."""

from __future__ import annotations

import json

import sympy as sp

from verify_root_m7_endpoint_legal_certificate_hitting_minimum_two_exclusion import (
    add_support,
    legal_universe,
    original_data,
)
from verify_root_m7_one_edge_a10_shared_pure_mixed_factor_obstruction import (
    coefficient,
)

PAIR = ((3, 6, 0), (4, 5, 0))
OLD_CERTIFICATE = tuple(map(int, "0101122"))
NEW_CERTIFICATE = tuple(map(int, "0101112"))
UNIQUE_ESCAPE = (5, 5, 2)


def exact_quotient(numerator: sp.Expr, denominator: sp.Expr) -> sp.Expr | None:
    """Return the quotient in Q[all symbols], or None if division is not exact."""
    if denominator == 0:
        return None
    symbols = sorted(numerator.free_symbols | denominator.free_symbols, key=str)
    quotient, remainder = sp.div(numerator, denominator, *symbols, domain=sp.QQ)
    if sp.expand(remainder) != 0:
        return None
    return sp.expand(quotient)


def endpoint_polynomials(base, support):
    alpha, beta, variables, a, b, h = add_support(base, support)
    endpoint = {alpha[0]: 1, alpha[3]: 1, beta[0]: 1, beta[3]: -1}
    pure = tuple(
        sp.expand(coefficient((colour,) * 7, a, b, h).subs(endpoint))
        for colour in range(3)
    )
    old_mixed = sp.expand(coefficient(OLD_CERTIFICATE, a, b, h).subs(endpoint))
    new_mixed = sp.expand(coefficient(NEW_CERTIFICATE, a, b, h).subs(endpoint))
    return variables, a, b, h, pure, old_mixed, new_mixed


def verify() -> dict[str, object]:
    base = original_data()
    universe = legal_universe(base[6], base[7], base[8])
    assert len(universe) == 104
    assert all(edge in universe for edge in PAIR)
    third_edges = tuple(edge for edge in universe if edge not in PAIR)
    assert len(third_edges) == 102

    old_certificate_edges = []
    escape_edges = []
    for edge in third_edges:
        *_, pure, old_mixed, _new_mixed = endpoint_polynomials(base, PAIR + (edge,))
        pure_product = sp.expand(sp.prod(pure))
        quotient = exact_quotient(pure_product, old_mixed)
        if quotient is None:
            escape_edges.append(edge)
        else:
            assert sp.expand(pure_product - old_mixed * quotient) == 0
            old_certificate_edges.append(edge)

    assert len(old_certificate_edges) == 101
    assert escape_edges == [UNIQUE_ESCAPE]

    variables, _a, _b, _h, pure, old_mixed, new_mixed = endpoint_polynomials(
        base, PAIR + (UNIQUE_ESCAPE,)
    )
    p, q, epsilon = variables
    del epsilon
    x, y, z = base[3], base[4], base[5]
    alpha, beta = base[0], base[1]
    expected_pure = (
        beta[1] * x[0] * x[1] * x[2] * (x[3] * x[4] + p * q),
        -alpha[2] * sp.prod(y),
        alpha[1] * beta[2] * sp.prod(z),
    )
    assert all(sp.expand(actual - expected) == 0 for actual, expected in zip(pure, expected_pure))
    assert exact_quotient(sp.expand(sp.prod(pure)), old_mixed) is None

    expected_new = alpha[2] * x[0] * y[1] * y[3] * y[4] * z[2]
    assert sp.expand(new_mixed - expected_new) == 0
    pure_product = sp.expand(sp.prod(pure))
    quotient = exact_quotient(pure_product, new_mixed)
    assert quotient is not None
    expected_quotient = -(
        x[1]
        * x[2]
        * y[0]
        * y[2]
        * z[0]
        * z[1]
        * z[3]
        * z[4]
        * alpha[1]
        * beta[1]
        * beta[2]
        * (x[3] * x[4] + p * q)
    )
    assert sp.expand(quotient - expected_quotient) == 0
    assert sp.expand(pure_product - new_mixed * quotient) == 0

    return {
        "legal_universe_size": len(universe),
        "fixed_pair": [list(edge) for edge in PAIR],
        "third_incidence_supports_checked": len(third_edges),
        "old_certificate": "0101122",
        "old_certificate_supports": len(old_certificate_edges),
        "old_certificate_escapes": len(escape_edges),
        "unique_escape": list(UNIQUE_ESCAPE),
        "new_certificate": "0101112",
        "new_certificate_saturation_is_unit": True,
        "third_shell_survivors": 0,
    }


def main() -> None:
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "result": verify(),
                "all_endpoint_legal_triples_resolved": False,
                "arbitrary_support_full_p7_exists": None,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
