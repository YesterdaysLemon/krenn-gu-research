"""Verify the fourth-incidence shell above the nine relative P7 triples."""

from __future__ import annotations

import json

import sympy as sp

from verify_root_m7_all_endpoint_legal_three_incidence_supports_exclusion import (
    FINAL_WORD,
    RELATIVE_SURVIVORS,
    exact_quotient,
    support_data,
)
from verify_root_m7_endpoint_legal_certificate_hitting_minimum_two_exclusion import (
    legal_universe,
    original_data,
)
from verify_root_m7_one_edge_a10_shared_pure_mixed_factor_obstruction import (
    coefficient,
)

REPLACEMENT_WORDS = tuple(tuple(map(int, word)) for word in ("0220212", "0210220"))
ESCAPES = (
    ((0, 3, 1), (3, 4, 1), (4, 0, 1), (5, 1, 0)),
    ((0, 4, 1), (3, 0, 1), (4, 3, 1), (5, 1, 0)),
    ((0, 5, 0), (3, 6, 0), (4, 2, 0), (5, 1, 0)),
    ((0, 6, 0), (3, 2, 0), (4, 5, 0), (5, 1, 0)),
    ((1, 4, 1), (4, 5, 1), (5, 1, 0), (5, 1, 1)),
    ((1, 4, 1), (4, 5, 1), (5, 1, 0), (6, 1, 1)),
    ((2, 3, 1), (3, 4, 1), (4, 2, 1), (5, 1, 0)),
    ((2, 4, 1), (3, 2, 1), (4, 3, 1), (5, 1, 0)),
    ((3, 6, 0), (4, 5, 0), (5, 1, 0), (5, 5, 2)),
    ((3, 6, 0), (4, 5, 0), (5, 5, 2), (6, 3, 2)),
)


def candidate_supports(universe):
    return tuple(
        sorted(
            {
                tuple(sorted(triple + (edge,)))
                for triple in RELATIVE_SURVIVORS
                for edge in universe
                if edge not in triple
            }
        )
    )


def verify() -> dict[str, object]:
    base = original_data()
    universe = legal_universe(base[6], base[7], base[8])
    candidates = candidate_supports(universe)
    assert len(universe) == 104
    assert len(candidates) == 908

    retained = []
    escapes = []
    for support in candidates:
        _variables, a, b, h, endpoint, pure_product = support_data(base, support)
        mixed = sp.expand(coefficient(FINAL_WORD, a, b, h).subs(endpoint))
        quotient = exact_quotient(pure_product, mixed)
        if quotient is None:
            escapes.append(support)
        else:
            assert sp.expand(pure_product - mixed * quotient) == 0
            retained.append(support)
    assert len(retained) == 898
    assert tuple(escapes) == ESCAPES

    replacement_counts = [0] * len(REPLACEMENT_WORDS)
    for support in escapes:
        _variables, a, b, h, endpoint, pure_product = support_data(base, support)
        for index, word in enumerate(REPLACEMENT_WORDS):
            mixed = sp.expand(coefficient(word, a, b, h).subs(endpoint))
            quotient = exact_quotient(pure_product, mixed)
            if quotient is not None:
                assert sp.expand(pure_product - mixed * quotient) == 0
                replacement_counts[index] += 1
                break
        else:
            raise AssertionError(f"replacement certificate missing for {support}")
    assert replacement_counts == [8, 2]

    return {
        "legal_universe_size": len(universe),
        "relative_triple_count": len(RELATIVE_SURVIVORS),
        "raw_triple_edge_pairs": len(RELATIVE_SURVIVORS) * (len(universe) - 3),
        "distinct_four_incidence_supports": len(candidates),
        "retained_2002000_certificates": len(retained),
        "relative_escapes": len(escapes),
        "relative_escape_supports": [[list(edge) for edge in support] for support in escapes],
        "replacement_certificates": ["0220212", "0210220"],
        "replacement_certificate_counts": replacement_counts,
        "relative_fourth_shell_survivors": 0,
    }


def main() -> None:
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "result": verify(),
                "all_endpoint_legal_quadruples_resolved": False,
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
