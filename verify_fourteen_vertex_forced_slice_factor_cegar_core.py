"""Independently replay a minimized C4+C4+C6 factor-CEGAR core."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable

from pysat.solvers import Solver


CYCLES = (
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (8, 9, 10, 11, 12, 13),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def equation_indices(item: object) -> set[int]:
    output: set[int] = set()
    if isinstance(item, dict):
        for key, value in item.items():
            if key.endswith("equation_index") and isinstance(
                value, int
            ):
                output.add(int(value))
            else:
                output.update(equation_indices(value))
    elif isinstance(item, list):
        for value in item:
            output.update(equation_indices(value))
    return output


def colouring(equation: int) -> tuple[int, ...]:
    return tuple(
        (equation // (3**vertex)) % 3 for vertex in range(14)
    )


def local_code(equation: int, cycle: tuple[int, ...]) -> int:
    row = colouring(equation)
    return sum(
        row[vertex] * (3**position)
        for position, vertex in enumerate(cycle)
    )


def relation_ids(clauses: Iterable[Iterable[int]]) -> list[int]:
    return sorted(
        {
            abs(int(literal)) - 1
            for clause in clauses
            for literal in clause
        }
    )


def solve(clauses: list[list[int]], solver_name: str) -> bool:
    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        return bool(solver.solve())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("core", type=Path)
    parser.add_argument(
        "--solver",
        default="glucose4",
        choices=("cadical195", "glucose4", "maplechrono"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    core = json.loads(args.core.read_text(encoding="utf-8"))
    if (
        core.get("status")
        != "UNSAT_irredundant_factor_cegar_transport_core"
    ):
        raise AssertionError("input is not a factor-CEGAR core")

    certificate_path = Path(core["certificate"])
    certificate_audit_path = Path(core["certificate_audit"])
    forced_path = Path(core["forced_cycle_analysis"])
    if sha256(certificate_path) != core["certificate_sha256"]:
        raise AssertionError("factor-CEGAR certificate hash changed")
    if (
        sha256(certificate_audit_path)
        != core["certificate_audit_sha256"]
    ):
        raise AssertionError("factor-CEGAR audit hash changed")
    if sha256(forced_path) != core["forced_cycle_analysis_sha256"]:
        raise AssertionError("forced-cycle analysis hash changed")

    certificate = json.loads(
        certificate_path.read_text(encoding="utf-8")
    )
    full_audit = json.loads(
        certificate_audit_path.read_text(encoding="utf-8")
    )
    forced = json.loads(forced_path.read_text(encoding="utf-8"))
    if (
        certificate.get("status") != "UNSAT"
        or full_audit.get("verified") is not True
        or full_audit.get("certificate_sha256")
        != core["certificate_sha256"]
    ):
        raise AssertionError(
            "source full factor-CEGAR proof is not independently verified"
        )
    if (
        certificate["singleton_matchings"]
        != core["singleton_matchings"]
    ):
        raise AssertionError("core singleton support changed")

    factor_clauses = [
        list(map(int, clause))
        for clause in certificate["factor_clauses"]
    ]
    learned_clauses = [
        list(map(int, clause))
        for clause in certificate["learned_clauses"]
    ]
    factor_indices = list(
        map(int, core["core_factor_clause_indices"])
    )
    learned_indices = list(
        map(int, core["core_learned_clause_indices"])
    )
    rebuilt_clauses = [
        factor_clauses[index] for index in factor_indices
    ]
    rebuilt_clauses.extend(
        learned_clauses[index] for index in learned_indices
    )
    if rebuilt_clauses != [
        list(map(int, clause)) for clause in core["core_clauses"]
    ]:
        raise AssertionError("core clauses changed")
    for index in learned_indices:
        if learned_clauses[index] != list(
            map(
                int,
                certificate["branches"][index]["blocking_clause"],
            )
        ):
            raise AssertionError(
                "learned core clause no longer matches its branch"
            )

    if solve(rebuilt_clauses, args.solver):
        raise AssertionError("core clauses unexpectedly became SAT")
    for excluded in range(len(rebuilt_clauses)):
        trial = (
            rebuilt_clauses[:excluded]
            + rebuilt_clauses[excluded + 1 :]
        )
        if not solve(trial, args.solver):
            raise AssertionError(
                "core is not deletion-irredundant"
            )

    required_relations = relation_ids(rebuilt_clauses)
    if required_relations != list(
        map(int, core["required_relation_ids"])
    ):
        raise AssertionError("required core relation IDs changed")
    semantic_equations: set[int] = set()
    for index in factor_indices:
        semantic_equations.add(
            int(
                certificate["factor_clause_origins"][index][
                    "equation_index"
                ]
            )
        )
    for relation_id in required_relations:
        relation = certificate["factor_relations"][relation_id]
        if int(relation["relation_id"]) != relation_id:
            raise AssertionError("factor relation indexing changed")
        semantic_equations.add(
            int(relation["origin"]["equation_index"])
        )
    for index in learned_indices:
        semantic_equations.update(
            equation_indices(
                certificate["branches"][index]["certificate"]
            )
        )
    if sorted(semantic_equations) != list(
        map(int, core["semantic_core_equations"])
    ):
        raise AssertionError("semantic core equations changed")

    forced_cycle = tuple(map(int, certificate["forced_cycle"]))
    if forced_cycle not in CYCLES:
        raise AssertionError("forced cycle is not a full component")
    forced_cycle_index = CYCLES.index(forced_cycle)
    if forced_cycle_index != int(core["forced_cycle_index"]):
        raise AssertionError("forced cycle index changed")
    forced_codes = sorted(
        {
            local_code(equation, forced_cycle)
            for equation in semantic_equations
        }
    )
    if forced_codes != list(
        map(int, core["forced_local_codes_used"])
    ):
        raise AssertionError("forced local codes changed")

    activation_equations = set(semantic_equations)
    premises = []
    for code in forced_codes:
        base = int(
            certificate["forcing_base_equations_by_local_code"][
                str(code)
            ]
        )
        if local_code(base, forced_cycle) != code:
            raise AssertionError("forcing base local code changed")
        activation_equations.add(base)
        selected = []
        for cycle_index, cycle in enumerate(CYCLES):
            if cycle_index == forced_cycle_index:
                continue
            code_at_base = local_code(base, cycle)
            conditional = forced[
                "conditional_fork_certificates_by_cycle"
            ][cycle_index].get(str(code_at_base))
            if conditional is None:
                raise AssertionError(
                    "conditional forcing premise disappeared"
                )
            equations = sorted(equation_indices(conditional))
            activation_equations.update(equations)
            selected.append(
                {
                    "cycle_index": cycle_index,
                    "local_code": code_at_base,
                    "equations": equations,
                }
            )
        premises.append(
            {
                "forced_local_code": code,
                "forcing_base_equation": base,
                "conditional_forks": selected,
            }
        )
    if premises != core["forcing_premises"]:
        raise AssertionError("forcing premises changed")
    if sorted(activation_equations) != list(
        map(int, core["activation_equations"])
    ):
        raise AssertionError("transport activation equations changed")

    payload = {
        "verified": True,
        "status": "factor_cegar_transport_core_verified",
        "scope": core["scope"],
        "core": str(args.core),
        "core_sha256": sha256(args.core),
        "certificate": str(certificate_path),
        "certificate_sha256": sha256(certificate_path),
        "source_full_certificate_verified": True,
        "core_factor_clauses": len(factor_indices),
        "core_learned_clauses": len(learned_indices),
        "core_clauses": len(rebuilt_clauses),
        "core_relations": len(required_relations),
        "activation_equations": len(activation_equations),
        "independent_solver": args.solver,
        "independent_unsat": True,
        "deletion_irredundant": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
