"""Append transported, independently verified hard-support certificates.

Simple factor forks are compiled by
``analyze_fourteen_vertex_c4_c4_c6_rule_sat.py``.  This companion handles
the two richer fixed-support mechanisms used by incremental CEGAR:

* verified double-pair forks; and
* verified forced-slice factor-choice UNSAT certificates.

For each proof, all equation colourings used by the proof are collected.
Any replacement support with the same singleton activation masks in those
equations has the identical proof, so negating that exact mask gives a
sound transport no-good.
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

from pysat.formula import CNF

from analyze_fourteen_vertex_c4_c4_c6_transport_rules import (
    ELIGIBLE_EDGES,
    certificate_equations,
    full_automorphisms,
    indexed_colouring,
    parse_factor,
)
from run_fourteen_vertex_c4_c4_c6_rule_sat_incremental import (
    certificate_no_goods,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_path(path: Path) -> Path:
    return path.with_name(f"{path.stem}_verified.json")


def verified_audit(path: Path) -> dict[str, object]:
    audit_file = audit_path(path)
    audit = json.loads(audit_file.read_text(encoding="utf-8"))
    if audit.get("verified") is not True:
        raise AssertionError(f"certificate audit failed: {audit_file}")
    return {
        "certificate": str(path),
        "certificate_sha256": sha256(path),
        "audit": str(audit_file),
        "audit_sha256": sha256(audit_file),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument(
        "--census",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_4_6_factor_orbit_census.json"
        ),
    )
    parser.add_argument(
        "--double-pair",
        type=Path,
        action="append",
        default=[],
    )
    parser.add_argument(
        "--factor-cegar",
        type=Path,
        action="append",
        default=[],
    )
    parser.add_argument(
        "--factor-cegar-core",
        type=Path,
        action="append",
        default=[],
        help=(
            "independently verified irredundant core extracted from a "
            "forced-slice factor-CEGAR proof"
        ),
    )
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    census = json.loads(args.census.read_text(encoding="utf-8"))
    representatives = tuple(
        parse_factor(row["representative"])
        for row in census["factor_orbits"]
    )
    representative_id = {
        factor: index for index, factor in enumerate(representatives)
    }
    edge_variable_count = 3 * len(ELIGIBLE_EDGES)
    selector_variables = tuple(
        edge_variable_count + 1 + index
        for index in range(len(representatives))
    )
    actions = full_automorphisms()
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
    records = []
    added: set[tuple[int, ...]] = set()

    for path in args.double_pair:
        proof = json.loads(path.read_text(encoding="utf-8"))
        if proof.get("status") != "even_cycle_double_pair_fork":
            raise AssertionError(f"double-pair proof is not closed: {path}")
        record = {
            "mode": "verified_double_pair",
            **verified_audit(path),
        }
        factors = tuple(
            parse_factor(proof["singleton_matchings"][key])
            for key in ("first", "second", "third")
        )
        equations = sorted(
            certificate_equations(proof["certificate"])
        )
        clauses = certificate_no_goods(
            factors,
            tuple(indexed_colouring(value) for value in equations),
            representative_id,
            selector_variables,
            actions,
        )
        new = clauses - known - added
        added.update(new)
        record["equations"] = len(equations)
        record["new_no_goods"] = len(new)
        records.append(record)

    for path in args.factor_cegar:
        proof = json.loads(path.read_text(encoding="utf-8"))
        if proof.get("status") != "UNSAT":
            raise AssertionError(f"factor CEGAR is not closed: {path}")
        record = {
            "mode": "verified_forced_slice_factor_cegar",
            **verified_audit(path),
        }
        factors = tuple(
            parse_factor(proof["singleton_matchings"][key])
            for key in ("first", "second", "third")
        )
        equations = {
            int(value)
            for value in proof[
                "forcing_base_equations_by_local_code"
            ].values()
        }
        equations.update(
            int(row["equation_index"])
            for row in proof["factor_clause_origins"]
        )
        equations.update(
            int(row["certificate"]["target_equation_index"])
            for row in proof["branches"]
            if row["certificate"]["certificate_mode"]
            == "isolated_factor_lattice_class"
        )
        forced_path = Path(proof["forced_cycle_analysis"])
        forced = json.loads(forced_path.read_text(encoding="utf-8"))
        equations.update(
            certificate_equations(
                forced["conditional_fork_certificates_by_cycle"]
            )
        )
        colourings = tuple(
            indexed_colouring(value)
            for value in sorted(
                equations,
                key=lambda item: (
                    item * 2_654_435_761
                )
                & 0xFFFFFFFF,
            )
        )
        clauses = certificate_no_goods(
            factors,
            colourings,
            representative_id,
            selector_variables,
            actions,
        )
        new = clauses - known - added
        added.update(new)
        record["equations"] = len(equations)
        record["new_no_goods"] = len(new)
        records.append(record)

    for path in args.factor_cegar_core:
        core = json.loads(path.read_text(encoding="utf-8"))
        if (
            core.get("status")
            != "UNSAT_irredundant_factor_cegar_transport_core"
        ):
            raise AssertionError(
                f"factor CEGAR core is not closed: {path}"
            )
        record = {
            "mode": (
                "verified_forced_slice_factor_cegar_transport_core"
            ),
            **verified_audit(path),
        }
        factors = tuple(
            parse_factor(core["singleton_matchings"][key])
            for key in ("first", "second", "third")
        )
        equations = list(map(int, core["activation_equations"]))
        clauses = certificate_no_goods(
            factors,
            tuple(indexed_colouring(value) for value in equations),
            representative_id,
            selector_variables,
            actions,
        )
        new = clauses - known - added
        added.update(new)
        record["core_clauses"] = len(core["core_clauses"])
        record["core_relations"] = len(
            core["required_relation_ids"]
        )
        record["equations"] = len(equations)
        record["new_no_goods"] = len(new)
        records.append(record)

    for clause in sorted(added):
        cnf.append(list(clause))
    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    cnf.to_file(str(args.output_cnf))
    payload = {
        "status": "verified_hard_certificate_no_goods_appended",
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "base_clauses": base_clauses,
        "certificate_records": records,
        "new_no_goods": len(added),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "output_clauses": len(cnf.clauses),
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
