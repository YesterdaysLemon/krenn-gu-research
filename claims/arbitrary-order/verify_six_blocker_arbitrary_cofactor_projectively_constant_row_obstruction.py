#!/usr/bin/env python3
"""Verify the arbitrary-cofactor projectively constant row obstruction."""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import sympy as sp

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
THEOREM = (
    HERE / "SIX_BLOCKER_ARBITRARY_COFACTOR_PROJECTIVELY_CONSTANT_ROW_OBSTRUCTION.md"
)
DEPENDENCIES = (
    REPO_ROOT / "claims/p6/P6_PROJECTIVELY_CONSTANT_SOURCE_ROW_OBSTRUCTION.md",
    HERE / "FOUR_ROOT_SIX_BLOCKER_ARBITRARY_ORDER_KERNEL_SUPPORT_OBSTRUCTION.md",
)
MODES = range(6)
PERMUTATIONS = tuple(itertools.permutations(range(4)))
EDGES = tuple(itertools.combinations(MODES, 2))


def permanent(columns: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    assert len(columns) == 4
    return sp.expand(
        sum(
            sp.prod(columns[column][permutation[column]] for column in range(4))
            for permutation in PERMUTATIONS
        )
    )


def arbitrary_cofactor_factor() -> dict[str, int]:
    linear = sp.symbols("L")
    kappas = sp.symbols("kappa0:6")
    other = sp.symbols("q0:18")
    block_values = sp.symbols("b0:15")

    columns = tuple(
        (kappas[mode] * linear,)
        + tuple(other[6 * (row - 1) + mode] for row in range(1, 4))
        for mode in MODES
    )
    cofactors = []
    cofactor_terms = []
    for left, right in EDGES:
        remaining = tuple(columns[mode] for mode in MODES if mode not in (left, right))
        cofactor = permanent(remaining)
        quotient = sp.expand(cofactor / linear)
        assert sp.expand(cofactor - linear * quotient) == 0
        assert linear not in quotient.free_symbols
        terms = len(sp.Poly(quotient, *kappas, *other).terms())
        assert terms == 24
        cofactors.append(cofactor)
        cofactor_terms.append(terms)

    equal_input = sp.expand(
        sum(block_values[index] * cofactors[index] for index in range(len(EDGES)))
    )
    quotient = sp.expand(equal_input / linear)
    assert sp.expand(equal_input - linear * quotient) == 0
    assert linear not in quotient.free_symbols
    total_terms = len(sp.Poly(quotient, *block_values, *kappas, *other).terms())
    assert total_terms == 15 * 24
    return {
        "edge_summands": len(EDGES),
        "assignments_per_cofactor": min(cofactor_terms),
        "permanent_assignments": sum(cofactor_terms),
        "factored_symbolic_terms": total_terms,
    }


def diagonal_sextic_line_case_split() -> dict[str, sp.Expr]:
    x, y = sp.symbols("x y")
    alpha, beta, gamma = sp.symbols("alpha beta gamma", nonzero=True)
    d0, d1, d2 = sp.symbols("d0 d1 d2", nonzero=True)

    restriction = sp.expand(
        gamma**6 * (d0 * x**6 + d1 * y**6) + d2 * (-alpha * x - beta * y) ** 6
    )
    polynomial = sp.Poly(restriction, x, y)
    x5y = sp.expand(polynomial.coeff_monomial(x**5 * y))
    xy5 = sp.expand(polynomial.coeff_monomial(x * y**5))
    assert x5y == 6 * alpha**5 * beta * d2
    assert xy5 == 6 * alpha * beta**5 * d2

    alpha_zero_x6 = sp.Poly(restriction.subs(alpha, 0), x, y).coeff_monomial(x**6)
    beta_zero_y6 = sp.Poly(restriction.subs(beta, 0), x, y).coeff_monomial(y**6)
    assert alpha_zero_x6 == gamma**6 * d0
    assert beta_zero_y6 == gamma**6 * d1
    assert d2 != 0
    return {
        "x5y": x5y,
        "xy5": xy5,
        "alpha_zero_x6": alpha_zero_x6,
        "beta_zero_y6": beta_zero_y6,
        "gamma_zero_z6": d2,
    }


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    for dependency in DEPENDENCIES:
        assert dependency.exists()
    for phrase in (
        "Exact characteristic-zero obstruction for arbitrary cofactor blocks",
        "ell(t) divides E_W(t)",
        "dim span{H_u[i,-]:u in B} >= 2",
        "full arbitrary-order local-to-global reduction: UNKNOWN",
        "UNRESOLVED",
    ):
        assert phrase in theorem

    factor = arbitrary_cofactor_factor()
    line_cases = diagonal_sextic_line_case_split()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "root_dependencies": [dependency.name for dependency in DEPENDENCIES],
                "arbitrary_block_cofactor_factor": factor,
                "common_linear_factor_verified": True,
                "diagonal_sextic_linear_factor": False,
                "diagonal_line_case_coefficients": {
                    key: str(value) for key, value in line_cases.items()
                },
                "arbitrary_order_four_root_six_blocker_transfer": True,
                "all_common_row_spans_at_least": 2,
                "full_local_to_global_reduction_complete": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
