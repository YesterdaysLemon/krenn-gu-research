"""Test whether the normalized K3,3 contradiction is visible in supports.

Every nonconstant equation in this stratum is either ``ab = 0`` or
``ab + cd = 0``.  Over a field, the latter implies that ``ab`` is nonzero
exactly when ``cd`` is nonzero.  This script encodes those implications as
SAT clauses and asks whether any quadratic term in a constant equation can
be nonzero.
"""

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

import argparse
from collections import Counter
from dataclasses import dataclass
from itertools import product

import numpy as np

from krenn_gu.generate_prism_singular import amplitude_polynomial
from krenn_gu.search_prism_stratum import K33_MATCHINGS, normalized_stratum
from krenn_gu.search_witness import EquationSystem


Clause = tuple[int, ...]


@dataclass(frozen=True)
class EquationClauses:
    colouring: tuple[int, ...]
    equation: Counter[tuple[str, ...]]
    clauses: tuple[Clause, ...]


@dataclass(frozen=True)
class ConstantEquation:
    colouring: tuple[int, ...]
    equation: Counter[tuple[str, ...]]
    terms: tuple[tuple[int, int], ...]


def variable_number(name: str) -> int:
    return int(name[1:]) + 1


def product_implies_product(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[Clause, Clause]:
    a, b = left
    c, d = right
    return (-a, -b, c), (-a, -b, d)


def equation_clauses(
    equation: Counter[tuple[str, ...]],
) -> tuple[Clause, ...]:
    terms = [
        tuple(variable_number(name) for name in monomial)
        for monomial, coefficient in equation.items()
        if coefficient
    ]
    if len(terms) == 1:
        a, b = terms[0]
        return ((-a, -b),)
    if len(terms) == 2:
        left, right = terms
        return (
            *product_implies_product(left, right),
            *product_implies_product(right, left),
        )
    raise ValueError(f"unexpected nonconstant equation: {equation}")


def build_problem() -> tuple[
    list[EquationClauses], list[ConstantEquation]
]:
    system = EquationSystem(6, 3)
    fixed, active = normalized_stratum(system, K33_MATCHINGS)
    indices = np.flatnonzero(active)
    variable_names = {
        int(flat_index): f"x{index}"
        for index, flat_index in enumerate(indices)
    }

    groups: list[EquationClauses] = []
    raw_constant_equations: list[
        tuple[tuple[int, ...], Counter[tuple[str, ...]]]
    ] = []
    for raw_colouring in system.colourings:
        colouring = tuple(int(value) for value in raw_colouring)
        if len(set(colouring)) == 1:
            continue
        equation = amplitude_polynomial(
            system, fixed, variable_names, colouring
        )
        if not equation:
            continue
        if () in equation:
            raw_constant_equations.append((colouring, equation))
        else:
            groups.append(
                EquationClauses(
                    colouring, equation, equation_clauses(equation)
                )
            )

    constant_terms = [
        ConstantEquation(
            colouring,
            equation,
            tuple(
                tuple(variable_number(name) for name in monomial)
                for monomial in equation
                if monomial
            ),
        )
        for colouring, equation in raw_constant_equations
    ]
    return groups, constant_terms


def simplify(
    clauses: tuple[Clause, ...], assignment: dict[int, bool]
) -> tuple[tuple[Clause, ...] | None, dict[int, bool]]:
    while True:
        residual: list[Clause] = []
        units: list[int] = []
        for clause in clauses:
            unresolved: list[int] = []
            satisfied = False
            for literal in clause:
                value = assignment.get(abs(literal))
                if value is None:
                    unresolved.append(literal)
                elif value == (literal > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            if not unresolved:
                return None, assignment
            residual.append(tuple(unresolved))
            if len(unresolved) == 1:
                units.append(unresolved[0])
        if not units:
            return tuple(residual), assignment
        for literal in units:
            variable = abs(literal)
            value = literal > 0
            previous = assignment.get(variable)
            if previous is not None and previous != value:
                return None, assignment
            assignment[variable] = value
        clauses = tuple(residual)


def solve(
    clauses: tuple[Clause, ...], assignment: dict[int, bool] | None = None
) -> dict[int, bool] | None:
    residual, assignment = simplify(clauses, dict(assignment or {}))
    if residual is None:
        return None
    if not residual:
        return assignment

    scores: Counter[int] = Counter()
    for clause in residual:
        for literal in clause:
            scores[abs(literal)] += 1
    variable = max(scores, key=scores.get)
    for value in (True, False):
        branch = solve(residual, assignment | {variable: value})
        if branch is not None:
            return branch
    return None


def clauses_for(groups: list[EquationClauses]) -> tuple[Clause, ...]:
    return tuple(clause for group in groups for clause in group.clauses)


def minimize_unsatisfiable_groups(
    groups: list[EquationClauses], assumptions: tuple[Clause, ...]
) -> list[EquationClauses]:
    active = list(groups)
    granularity = 2
    while len(active) >= 2:
        chunk_size = (len(active) + granularity - 1) // granularity
        reduced = False
        for start in range(0, len(active), chunk_size):
            candidate = active[:start] + active[start + chunk_size :]
            if solve(clauses_for(candidate) + assumptions) is None:
                active = candidate
                granularity = max(2, granularity - 1)
                reduced = True
                break
        if reduced:
            continue
        if granularity >= len(active):
            break
        granularity = min(len(active), granularity * 2)

    # Make the result one-deletion-minimal; ddmin need not guarantee this
    # when several equations have overlapping clause sets.
    index = 0
    while index < len(active):
        candidate = active[:index] + active[index + 1 :]
        if solve(clauses_for(candidate) + assumptions) is None:
            active = candidate
        else:
            index += 1
    return active


def equation_text(equation: Counter[tuple[str, ...]]) -> str:
    terms = ["*".join(monomial) if monomial else "1" for monomial in equation]
    return " + ".join(terms)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--show-cores",
        action="store_true",
        help="print one-deletion-minimal support cores for all 27 choices",
    )
    args = parser.parse_args()

    groups, constant_equations = build_problem()
    clauses = clauses_for(groups)
    print(
        f"{len(groups)} equations, {len(clauses)} support clauses, "
        f"{len(constant_equations)} constant equations"
    )
    satisfiable_choices: list[tuple[int, ...]] = []
    for choices in product(range(3), repeat=len(constant_equations)):
        selected_terms = [
            constant_equations[equation_index].terms[term_index]
            for equation_index, term_index in enumerate(choices)
        ]
        assumptions = tuple(
            (variable,) for term in selected_terms for variable in term
        )
        model = solve(clauses + assumptions)
        if model is not None:
            satisfiable_choices.append(choices)
        elif args.show_cores:
            core = minimize_unsatisfiable_groups(groups, assumptions)
            print(f"\nchoice {choices}: {len(core)}-equation core")
            print(f"  assume nonzero: {selected_terms}")
            for group in core:
                print(
                    f"  {group.colouring}: "
                    f"{equation_text(group.equation)} = 0"
                )
    print(
        "support certificate: "
        + (
            "SUCCESS"
            if not satisfiable_choices
            else f"not sufficient ({len(satisfiable_choices)}/27 choices SAT)"
        )
    )
    if satisfiable_choices:
        print(f"first satisfiable term choices: {satisfiable_choices[0]}")


if __name__ == "__main__":
    main()
