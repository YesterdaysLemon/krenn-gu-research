"""Partial matrix-core identities for every normalized prism orbit."""

from __future__ import annotations

import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

from collections import Counter

from krenn_gu.prism_orbit_screen import (
    Polynomial,
    clean_polynomial,
    multiply_polynomials,
)


def partial_core_audit(
    names: list[str], equations: list[Polynomial]
) -> dict[str, object]:
    equations_by_linear_variable: dict[str, Polynomial] = {}
    for equation in equations:
        linear_terms = [
            monomial
            for monomial, coefficient in equation.items()
            if len(monomial) == 1 and coefficient
        ]
        if len(linear_terms) != 1:
            continue
        variable = linear_terms[0][0]
        if variable in equations_by_linear_variable:
            return {"passes": False, "reason": "repeated linear variable"}
        equations_by_linear_variable[variable] = equation

    blocks: list[dict[str, object]] = []
    for block_index in range(6):
        block_lambda: Polynomial | None = None
        remainders: dict[tuple[int, int], Polynomial] = {}
        missing: list[tuple[int, int]] = []
        for row in range(3):
            for column in range(3):
                variable = f"x{9 * block_index + 3 * row + column}"
                equation = equations_by_linear_variable.get(variable)
                if equation is None:
                    missing.append((row, column))
                    continue
                coefficient: Polynomial = Counter()
                remainder: Polynomial = Counter()
                for monomial, value in equation.items():
                    if variable in monomial:
                        reduced = list(monomial)
                        reduced.remove(variable)
                        coefficient[tuple(reduced)] += value
                    else:
                        remainder[monomial] += value
                coefficient = clean_polynomial(coefficient)
                remainder = clean_polynomial(remainder)
                if block_lambda is None:
                    block_lambda = coefficient
                elif coefficient != block_lambda:
                    return {
                        "passes": False,
                        "reason": "entry-dependent lambda",
                        "block": block_index,
                    }
                terms = [
                    monomial
                    for monomial, value in remainder.items()
                    if value
                ]
                if len(terms) != 1:
                    return {
                        "passes": False,
                        "reason": "remainder is not monomial",
                        "block": block_index,
                        "entry": (row, column),
                    }
                remainders[(row, column)] = remainder
        if block_lambda is None:
            return {
                "passes": False,
                "reason": "block has no linear equations",
                "block": block_index,
            }
        if len(missing) > 1:
            return {
                "passes": False,
                "reason": "block misses more than one entry",
                "block": block_index,
                "missing": missing,
            }
        full_rank_one_remainder = not missing
        if full_rank_one_remainder:
            for first_row in range(3):
                for second_row in range(first_row + 1, 3):
                    for first_column in range(3):
                        for second_column in range(first_column + 1, 3):
                            minor = multiply_polynomials(
                                remainders[(first_row, first_column)],
                                remainders[(second_row, second_column)],
                            )
                            minor.subtract(
                                multiply_polynomials(
                                    remainders[(first_row, second_column)],
                                    remainders[(second_row, first_column)],
                                )
                            )
                            if clean_polynomial(minor):
                                full_rank_one_remainder = False
        blocks.append(
            {
                "lambda": block_lambda,
                "remainders": remainders,
                "missing": missing,
                "forces_rank_one_when_generic": (
                    not missing and full_rank_one_remainder
                ),
            }
        )
    return {
        "passes": True,
        "linear_variables": len(equations_by_linear_variable),
        "blocks": blocks,
        "rank_one_blocks": {
            index
            for index, block in enumerate(blocks)
            if block["forces_rank_one_when_generic"]
        },
    }
