"""Verify exclusion of all endpoint-legal three-incidence P7 supports."""

from __future__ import annotations

import json
from itertools import combinations

import sympy as sp

from verify_root_m7_endpoint_legal_certificate_hitting_minimum_two_exclusion import (
    add_support,
    legal_universe,
    original_data,
)
from verify_root_m7_one_edge_a10_shared_pure_mixed_factor_obstruction import (
    coefficient,
)

OLD_WORDS = tuple(
    tuple(map(int, word))
    for word in ("0000102", "1112101", "1112220", "0101010", "1010220", "0101122")
)
FINAL_WORD = tuple(map(int, "2002000"))
RELATIVE_SURVIVORS = (
    ((0, 3, 1), (3, 4, 1), (4, 0, 1)),
    ((0, 4, 1), (3, 0, 1), (4, 3, 1)),
    ((0, 5, 0), (3, 6, 0), (4, 2, 0)),
    ((0, 6, 0), (3, 2, 0), (4, 5, 0)),
    ((1, 4, 1), (4, 5, 1), (5, 1, 1)),
    ((1, 4, 1), (4, 5, 1), (6, 1, 1)),
    ((2, 3, 1), (3, 4, 1), (4, 2, 1)),
    ((2, 4, 1), (3, 2, 1), (4, 3, 1)),
    ((3, 6, 0), (4, 5, 0), (5, 5, 2)),
)


def exact_quotient(numerator: sp.Expr, denominator: sp.Expr) -> sp.Expr | None:
    if denominator == 0:
        return None
    symbols = sorted(numerator.free_symbols | denominator.free_symbols, key=str)
    quotient, remainder = sp.div(numerator, denominator, *symbols, domain=sp.QQ)
    return sp.expand(quotient) if sp.expand(remainder) == 0 else None


def support_data(base, support):
    alpha, beta, variables, a, b, h = add_support(base, support)
    endpoint = {alpha[0]: 1, alpha[3]: 1, beta[0]: 1, beta[3]: -1}
    pure = tuple(
        sp.expand(coefficient((colour,) * 7, a, b, h).subs(endpoint))
        for colour in range(3)
    )
    return variables, a, b, h, endpoint, sp.expand(sp.prod(pure))


def verify() -> dict[str, object]:
    base = original_data()
    universe = legal_universe(base[6], base[7], base[8])
    assert len(universe) == 104

    first_certificate_counts = [0] * len(OLD_WORDS)
    relative_survivors = []
    checked = 0
    for support in combinations(universe, 3):
        checked += 1
        _variables, a, b, h, endpoint, pure_product = support_data(base, support)
        for index, word in enumerate(OLD_WORDS):
            mixed = sp.expand(coefficient(word, a, b, h).subs(endpoint))
            quotient = exact_quotient(pure_product, mixed)
            if quotient is not None:
                assert sp.expand(pure_product - mixed * quotient) == 0
                first_certificate_counts[index] += 1
                break
        else:
            relative_survivors.append(support)

    assert checked == 182_104
    assert first_certificate_counts == [179_884, 1_768, 326, 5, 0, 112]
    assert tuple(relative_survivors) == RELATIVE_SURVIVORS

    final_quotients = []
    for support in relative_survivors:
        _variables, a, b, h, endpoint, pure_product = support_data(base, support)
        mixed = sp.expand(coefficient(FINAL_WORD, a, b, h).subs(endpoint))
        quotient = exact_quotient(pure_product, mixed)
        assert quotient is not None
        assert sp.expand(pure_product - mixed * quotient) == 0
        final_quotients.append(quotient)
    assert len(final_quotients) == 9 and all(quotient != 0 for quotient in final_quotients)

    return {
        "legal_universe_size": len(universe),
        "three_incidence_supports_checked": checked,
        "old_certificate_words": ["".join(map(str, word)) for word in OLD_WORDS],
        "old_first_certificate_counts": first_certificate_counts,
        "relative_survivors": len(relative_survivors),
        "relative_survivor_supports": [[list(edge) for edge in support] for support in relative_survivors],
        "final_certificate": "2002000",
        "final_certificate_supports": len(final_quotients),
        "full_triple_shell_survivors": 0,
    }


def main() -> None:
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "result": verify(),
                "fixed_support_triple_shell_resolved": True,
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
