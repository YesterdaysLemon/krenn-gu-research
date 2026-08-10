"""Append exact-support no-goods from verified unforced factor cores.

Each input core proves one fixed labelled singleton-factor support
impossible.  This augmentation deliberately transports only by exact
full-factor automorphisms and by swapping singleton roles 1 and 2.  It
does not make the broader activation-mask transport assumption used by
the simple factor-fork compiler.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Sequence

from pysat.formula import CNF

from analyze_fourteen_vertex_two_even_cycle_rule_sat import (
    Factor,
    edge_variable,
    parse_factor,
    transform_factor,
)
from explore_fourteen_vertex_equality_factor_family import (
    N,
    contiguous_cycles,
    full_automorphisms,
)
from explore_random_even_cycle_forks import cycle_edges


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_path(path: Path) -> Path:
    return path.with_name(f"{path.stem}_verified.json")


def exact_support_no_goods(
    factors: Sequence[Factor],
    representative_id: dict[Factor, int],
    selector_variables: Sequence[int],
    actions: Sequence[dict[int, int]],
    eligible_edges: Sequence[tuple[int, int]],
) -> set[tuple[int, ...]]:
    first_orbit = representative_id.get(factors[0])
    if first_orbit is None:
        raise AssertionError(
            "source first factor is not its pinned representative"
        )
    selector = selector_variables[first_orbit]
    edge_id = {
        item: index for index, item in enumerate(eligible_edges)
    }
    output = set()
    for action in actions:
        moved = tuple(
            transform_factor(factor, action) for factor in factors
        )
        if moved[0] != factors[0]:
            continue
        for permutation in ((0, 1, 2), (0, 2, 1)):
            clause = [-selector]
            for old_role in (1, 2):
                new_role = permutation[old_role]
                clause.extend(
                    -edge_variable(
                        new_role,
                        edge_id[item],
                        len(eligible_edges),
                    )
                    for item in moved[old_role]
                )
            normalized = tuple(
                sorted(set(clause), key=lambda item: (abs(item), item))
            )
            if len(normalized) != 15:
                raise AssertionError(
                    "exact support no-good lost a singleton edge"
                )
            output.add(normalized)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--compiled-result", type=Path, required=True)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument(
        "--unforced-factor-core",
        type=Path,
        action="append",
        default=[],
    )
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = json.loads(
        args.compiled_result.read_text(encoding="utf-8")
    )
    census = json.loads(args.census.read_text(encoding="utf-8"))
    lengths = tuple(map(int, result["partition"]))
    if (
        tuple(map(int, census["partition"])) != lengths
        or sum(lengths) != N
        or any(length % 2 for length in lengths)
    ):
        raise AssertionError("all-even partition provenance changed")
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    representatives = tuple(
        parse_factor(row["representative"])
        for row in census["factor_orbits"]
    )
    representative_id = {
        factor: index for index, factor in enumerate(representatives)
    }
    edge_variables = 3 * len(eligible_edges)
    selectors = tuple(
        edge_variables + 1 + index
        for index in range(len(representatives))
    )
    actions = full_automorphisms(cycles)
    if len(actions) != int(census["full_automorphisms"]):
        raise AssertionError("full-factor automorphism count changed")

    cnf = CNF(from_file=str(args.base_cnf))
    known = {
        tuple(
            sorted(
                set(map(int, clause)),
                key=lambda item: (abs(item), item),
            )
        )
        for clause in cnf.clauses
    }
    base_clauses = len(cnf.clauses)
    added: set[tuple[int, ...]] = set()
    records = []
    for core_path in args.unforced_factor_core:
        proof = json.loads(core_path.read_text(encoding="utf-8"))
        audit_file = audit_path(core_path)
        audit = json.loads(audit_file.read_text(encoding="utf-8"))
        proof_is_factor_choice_core = (
            proof.get("status") == "UNSAT"
            and not proof.get("necessary_conditions_only")
            and proof.get("dual_horn_core") is not None
        )
        proof_is_one_extra_core = (
            proof.get("status") == "one_extra_cycle_core"
            and proof.get("certificate") is not None
        )
        if (
            not (
                proof_is_factor_choice_core
                or proof_is_one_extra_core
            )
            or tuple(map(int, proof["full_cycle_type"])) != lengths
            or audit.get("verified") is not True
            or audit.get("certificate_sha256") != sha256(core_path)
            or audit.get("status")
            not in {
                "unforced_factor_choice_dual_horn_base_core_verified",
                "unforced_factor_choice_dual_horn_lattice_core_verified",
                "one_extra_cycle_core_verified",
            }
        ):
            raise AssertionError(
                f"unforced factor core is not verified: {core_path}"
            )
        factors = tuple(
            parse_factor(proof["singleton_matchings"][key])
            for key in ("first", "second", "third")
        )
        if (
            any(len(factor) != N // 2 for factor in factors)
            or set().union(*map(set, factors)) & full_edges
            or len(set().union(*map(set, factors))) != 3 * (N // 2)
        ):
            raise AssertionError("fixed singleton support changed")
        clauses = exact_support_no_goods(
            factors,
            representative_id,
            selectors,
            actions,
            eligible_edges,
        )
        new = clauses - known - added
        added.update(new)
        records.append(
            {
                "mode": "verified_unforced_factor_exact_support_core",
                "certificate_kind": audit["status"],
                "certificate": str(core_path),
                "certificate_sha256": sha256(core_path),
                "audit": str(audit_file),
                "audit_sha256": sha256(audit_file),
                "first_factor_orbit": representative_id[factors[0]],
                "transported_exact_support_no_goods": len(clauses),
                "new_no_goods": len(new),
            }
        )

    for clause in sorted(added):
        cnf.append(list(clause))
    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    cnf.to_file(str(args.output_cnf))
    payload = {
        "status": "verified_unforced_factor_exact_support_no_goods_appended",
        "partition": list(lengths),
        "compiled_result": str(args.compiled_result),
        "compiled_result_sha256": sha256(args.compiled_result),
        "census": str(args.census),
        "census_sha256": sha256(args.census),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "base_clauses": base_clauses,
        "certificate_records": records,
        "new_no_goods": len(added),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "output_clauses": len(cnf.clauses),
        "exploratory_until_independently_reconstructed": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
