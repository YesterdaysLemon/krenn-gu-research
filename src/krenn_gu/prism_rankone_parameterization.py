"""Parameterize all six free prism blocks as outer products.

On a generic six-block core branch every complement block has rank at most
one.  Writing ``X_e = u_e v_e^T`` replaces 54 entry variables and 54
determinantal equations by 36 factor variables.  This parameterization is
surjective onto the rank-at-most-one locus, including the zero matrix, so
emptiness of the resulting system is equivalent to emptiness of the generic
branch.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from prism_orbit_screen import (
    Polynomial,
    clean_polynomial,
    core_rank_one_audit,
    orbit_equations,
    prism_orbit_representatives,
    singular_program,
)
from search_witness import EquationSystem


def parameter_names() -> list[str]:
    return [
        *(f"u{index}" for index in range(18)),
        *(f"v{index}" for index in range(18)),
    ]


def parameterize_polynomial(polynomial: Polynomial) -> Polynomial:
    result: Polynomial = Counter()
    for monomial, coefficient in polynomial.items():
        factors: list[str] = []
        for variable in monomial:
            entry_index = int(variable[1:])
            block = entry_index // 9
            within_block = entry_index % 9
            row = within_block // 3
            column = within_block % 3
            factors.extend((f"u{3 * block + row}", f"v{3 * block + column}"))
        result[tuple(sorted(factors))] += coefficient
    return clean_polynomial(result)


def parameterized_orbit_equations(
    system: EquationSystem, pattern: tuple[int, ...]
) -> tuple[list[str], list[Polynomial]]:
    _, equations = orbit_equations(system, pattern)
    return parameter_names(), [
        parameterize_polynomial(equation) for equation in equations
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--characteristic", type=int, default=0)
    parser.add_argument("--algorithm", choices=("std", "slimgb"), default="slimgb")
    args = parser.parse_args()

    representatives = prism_orbit_representatives()
    pattern = representatives[args.index]
    audit = core_rank_one_audit(EquationSystem(6, 3), pattern)
    if not audit["passes"]:
        raise ValueError("orbit does not have the six-block rank-one core")
    names, equations = parameterized_orbit_equations(
        EquationSystem(6, 3), pattern
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        singular_program(
            args.index,
            names,
            equations,
            args.characteristic,
            "full",
            args.algorithm,
        ),
        encoding="utf-8",
    )
    print(
        f"wrote {args.output}: orbit={args.index} "
        f"variables={len(names)} equations={len(equations)}"
    )


if __name__ == "__main__":
    main()
