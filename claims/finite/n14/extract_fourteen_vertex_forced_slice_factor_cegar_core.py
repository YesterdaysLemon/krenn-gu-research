"""Extract a small transport core from a verified factor-CEGAR proof.

The fixed-support factor CEGAR may contain tens of thousands of clauses,
even when its contradiction uses only a handful.  Transporting every
equation in that proof fixes nearly the entire singleton support.  This
script guards the factor clauses, asks a SAT solver for an UNSAT core,
makes that core deletion-irredundant, and retains only the colouring
equations needed to replay:

* the core factor-choice clauses;
* the core exact-lattice blocking clauses; and
* the conditional forks forcing the selected cycle at the local codes
  used by the core.

The resulting activation mask is usually much shorter and therefore
transports to many more supports.  A separate verifier must replay the
artifact before it is used as a rule.
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

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])


import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable

from pysat.solvers import Solver

from analyze_fourteen_vertex_c4_c4_c6_transport_rules import (
    CYCLES,
    certificate_equations,
    indexed_colouring,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_path(path: Path) -> Path:
    return path.with_name(f"{path.stem}_verified.json")


def guarded_core(
    clauses: list[list[int]], solver_name: str
) -> list[int]:
    base_variable = max(
        (abs(literal) for clause in clauses for literal in clause),
        default=0,
    )
    assumptions = [
        base_variable + 1 + index
        for index in range(len(clauses))
    ]
    with Solver(name=solver_name) as solver:
        for assumption, clause in zip(
            assumptions, clauses, strict=True
        ):
            solver.add_clause([*clause, -assumption])
        if solver.solve(assumptions=assumptions):
            raise AssertionError(
                "verified factor-CEGAR clauses unexpectedly became SAT"
            )
        raw_core = solver.get_core()
        if raw_core is None:
            raise AssertionError("solver did not return an UNSAT core")
        core = sorted(
            assumption - (base_variable + 1)
            for assumption in raw_core
        )

        # A single deletion pass is sufficient: once deleting a clause
        # makes a monotone CNF SAT, deleting still more cannot restore
        # UNSAT.
        position = 0
        while position < len(core):
            trial = core[:position] + core[position + 1 :]
            trial_assumptions = [
                assumptions[index] for index in trial
            ]
            if not solver.solve(assumptions=trial_assumptions):
                core = trial
            else:
                position += 1
    return core


def relation_ids(clauses: Iterable[Iterable[int]]) -> list[int]:
    return sorted(
        {
            abs(int(literal)) - 1
            for clause in clauses
            for literal in clause
        }
    )


def local_code(equation: int, cycle: tuple[int, ...]) -> int:
    colouring = indexed_colouring(equation)
    return sum(
        colouring[vertex] * (3**position)
        for position, vertex in enumerate(cycle)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument(
        "--audit",
        type=Path,
        help="independent full-certificate audit; defaults beside input",
    )
    parser.add_argument(
        "--solver",
        default="cadical195",
        choices=("cadical195", "glucose4", "maplechrono"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    certificate = json.loads(
        args.certificate.read_text(encoding="utf-8")
    )
    if certificate.get("status") != "UNSAT":
        raise AssertionError("factor-CEGAR certificate is not UNSAT")
    full_audit_path = args.audit or audit_path(args.certificate)
    full_audit = json.loads(
        full_audit_path.read_text(encoding="utf-8")
    )
    if (
        full_audit.get("verified") is not True
        or full_audit.get("certificate_sha256")
        != sha256(args.certificate)
    ):
        raise AssertionError(
            "independent full factor-CEGAR audit is missing or stale"
        )

    factor_clauses = [
        list(map(int, clause))
        for clause in certificate["factor_clauses"]
    ]
    learned_clauses = [
        list(map(int, clause))
        for clause in certificate["learned_clauses"]
    ]
    if len(learned_clauses) != len(certificate["branches"]):
        raise AssertionError("learned clauses and branches diverged")
    all_clauses = factor_clauses + learned_clauses
    core_indices = guarded_core(all_clauses, args.solver)
    factor_count = len(factor_clauses)
    core_factor_indices = [
        index for index in core_indices if index < factor_count
    ]
    core_learned_indices = [
        index - factor_count
        for index in core_indices
        if index >= factor_count
    ]
    core_clauses = [all_clauses[index] for index in core_indices]

    for branch_index in core_learned_indices:
        branch = certificate["branches"][branch_index]
        if list(map(int, branch["blocking_clause"])) != (
            learned_clauses[branch_index]
        ):
            raise AssertionError(
                "core learned clause changed from its branch"
            )

    required_relations = relation_ids(core_clauses)
    semantic_equations: set[int] = set()
    for index in core_factor_indices:
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
            raise AssertionError("factor relation IDs changed")
        semantic_equations.add(
            int(relation["origin"]["equation_index"])
        )
    for index in core_learned_indices:
        semantic_equations.update(
            certificate_equations(
                certificate["branches"][index]["certificate"]
            )
        )

    forced_cycle = tuple(map(int, certificate["forced_cycle"]))
    try:
        forced_cycle_index = CYCLES.index(forced_cycle)
    except ValueError as error:
        raise AssertionError("forced cycle is not a full component") from error
    forced_codes = sorted(
        {
            local_code(equation, forced_cycle)
            for equation in semantic_equations
        }
    )

    forced_path = Path(certificate["forced_cycle_analysis"])
    forced = json.loads(forced_path.read_text(encoding="utf-8"))
    activation_equations = set(semantic_equations)
    premises = []
    for code in forced_codes:
        base = int(
            certificate["forcing_base_equations_by_local_code"][
                str(code)
            ]
        )
        if local_code(base, forced_cycle) != code:
            raise AssertionError("forcing base has the wrong local code")
        activation_equations.add(base)
        selected = []
        for cycle_index, cycle in enumerate(CYCLES):
            if cycle_index == forced_cycle_index:
                continue
            code_at_base = local_code(base, cycle)
            certificate_by_code = forced[
                "conditional_fork_certificates_by_cycle"
            ][cycle_index]
            conditional = certificate_by_code.get(str(code_at_base))
            if conditional is None:
                raise AssertionError(
                    "forcing base lacks a conditional fork premise"
                )
            equations = sorted(
                certificate_equations(conditional)
            )
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

    payload = {
        "status": "UNSAT_irredundant_factor_cegar_transport_core",
        "scope": (
            "a transport core for one independently verified fixed "
            "C4+C4+C6 support proof"
        ),
        "certificate": str(args.certificate),
        "certificate_sha256": sha256(args.certificate),
        "certificate_audit": str(full_audit_path),
        "certificate_audit_sha256": sha256(full_audit_path),
        "forced_cycle_analysis": str(forced_path),
        "forced_cycle_analysis_sha256": sha256(forced_path),
        "singleton_matchings": certificate["singleton_matchings"],
        "original_factor_clauses": factor_count,
        "original_learned_clauses": len(learned_clauses),
        "core_solver": args.solver,
        "core_unsat": True,
        "core_deletion_irredundant": True,
        "core_factor_clause_indices": core_factor_indices,
        "core_learned_clause_indices": core_learned_indices,
        "core_clauses": core_clauses,
        "required_relation_ids": required_relations,
        "semantic_core_equations": sorted(semantic_equations),
        "forced_cycle_index": forced_cycle_index,
        "forced_local_codes_used": forced_codes,
        "forcing_premises": premises,
        "activation_equations": sorted(activation_equations),
        "activation_equation_count": len(activation_equations),
        "independently_verified": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
