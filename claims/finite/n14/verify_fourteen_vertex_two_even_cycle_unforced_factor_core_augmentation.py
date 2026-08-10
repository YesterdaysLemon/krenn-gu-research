"""Independently reconstruct exact-support unforced-factor no-goods."""

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
import itertools
import json
import time
from pathlib import Path
from typing import Sequence

from pysat.formula import CNF
from pysat.solvers import Solver

from verify_fourteen_vertex_two_even_cycle_rule_cnf import (
    Factor,
    automorphisms,
    cycle_edge_set,
    cycles_for,
    edge_variable,
    parse_factor,
    transform_factor,
)

N = 14


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_support_no_goods(
    factors: Sequence[Factor],
    representative_id: dict[Factor, int],
    selectors: Sequence[int],
    actions: Sequence[dict[int, int]],
    eligible_edges: Sequence[tuple[int, int]],
) -> set[tuple[int, ...]]:
    first_orbit = representative_id.get(factors[0])
    if first_orbit is None:
        raise AssertionError("first factor is not a representative")
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
        for swap in (False, True):
            clause = [-selectors[first_orbit]]
            for old_role in (1, 2):
                new_role = 3 - old_role if swap else old_role
                for item in moved[old_role]:
                    clause.append(
                        -edge_variable(
                            new_role,
                            edge_id[item],
                            len(eligible_edges),
                        )
                    )
            normalized = tuple(
                sorted(set(clause), key=lambda item: (abs(item), item))
            )
            if len(normalized) != 15:
                raise AssertionError("support clause width changed")
            output.add(normalized)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("augmentation", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()

    manifest = json.loads(
        args.augmentation.read_text(encoding="utf-8")
    )
    if (
        manifest.get("status")
        != "verified_unforced_factor_exact_support_no_goods_appended"
    ):
        raise AssertionError("augmentation status changed")
    result_path = Path(manifest["compiled_result"])
    census_path = Path(manifest["census"])
    base_path = Path(manifest["base_cnf"])
    output_path = Path(manifest["output_cnf"])
    if (
        sha256(result_path) != manifest["compiled_result_sha256"]
        or sha256(census_path) != manifest["census_sha256"]
        or sha256(base_path) != manifest["base_cnf_sha256"]
        or sha256(output_path) != manifest["output_cnf_sha256"]
    ):
        raise AssertionError("augmentation source hash changed")
    result = json.loads(result_path.read_text(encoding="utf-8"))
    census = json.loads(census_path.read_text(encoding="utf-8"))
    lengths = tuple(map(int, result["partition"]))
    if (
        list(lengths) != manifest["partition"]
        or tuple(map(int, census["partition"])) != lengths
        or sum(lengths) != N
        or any(length % 2 for length in lengths)
    ):
        raise AssertionError("partition provenance changed")
    cycles = cycles_for(lengths)
    full_edges = cycle_edge_set(cycles)
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
    selectors = tuple(
        3 * len(eligible_edges) + 1 + index
        for index in range(len(representatives))
    )
    actions = automorphisms(cycles)
    if len(actions) != int(census["full_automorphisms"]):
        raise AssertionError("automorphism count changed")

    base = CNF(from_file=str(base_path))
    known = {
        tuple(
            sorted(
                set(map(int, clause)),
                key=lambda item: (abs(item), item),
            )
        )
        for clause in base.clauses
    }
    reconstructed: set[tuple[int, ...]] = set()
    records = manifest["certificate_records"]
    for record in records:
        certificate = Path(record["certificate"])
        audit_path = Path(record["audit"])
        if (
            record.get("mode")
            != "verified_unforced_factor_exact_support_core"
            or sha256(certificate) != record["certificate_sha256"]
            or sha256(audit_path) != record["audit_sha256"]
        ):
            raise AssertionError("certificate record hash changed")
        proof = json.loads(certificate.read_text(encoding="utf-8"))
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
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
            or audit.get("certificate_sha256") != sha256(certificate)
            or record.get("certificate_kind") != audit.get("status")
            or audit.get("status")
            not in {
                "unforced_factor_choice_dual_horn_base_core_verified",
                "unforced_factor_choice_dual_horn_lattice_core_verified",
                "one_extra_cycle_core_verified",
            }
        ):
            raise AssertionError("certificate audit changed")
        factors = tuple(
            parse_factor(proof["singleton_matchings"][key])
            for key in ("first", "second", "third")
        )
        clauses = exact_support_no_goods(
            factors,
            representative_id,
            selectors,
            actions,
            eligible_edges,
        )
        if (
            representative_id[factors[0]]
            != int(record["first_factor_orbit"])
            or len(clauses)
            != int(record["transported_exact_support_no_goods"])
        ):
            raise AssertionError("certificate transport count changed")
        new = clauses - known - reconstructed
        if len(new) != int(record["new_no_goods"]):
            raise AssertionError("certificate deduplication changed")
        reconstructed.update(new)

    stored = CNF(from_file=str(output_path))
    expected = [
        *base.clauses,
        *[list(clause) for clause in sorted(reconstructed)],
    ]
    if stored.clauses != expected:
        raise AssertionError("output CNF clause sequence changed")
    if (
        len(base.clauses) != int(manifest["base_clauses"])
        or len(reconstructed) != int(manifest["new_no_goods"])
        or len(stored.clauses) != int(manifest["output_clauses"])
    ):
        raise AssertionError("augmentation clause count changed")
    with Solver(
        name="cadical195", bootstrap_with=stored.clauses
    ) as solver:
        sat = solver.solve()
    payload = {
        "verified": True,
        "status": (
            "unforced_factor_exact_support_augmentation_reconstructed"
        ),
        "scope": (
            "all core and audit hashes, exact labelled support "
            "transport, deduplication, clause sequence, and SAT status"
        ),
        "augmentation": str(args.augmentation),
        "augmentation_sha256": sha256(args.augmentation),
        "partition": list(lengths),
        "certificates_replayed": len(records),
        "new_exact_support_no_goods": len(reconstructed),
        "output_cnf_variables": stored.nv,
        "output_cnf_clauses": len(stored.clauses),
        "independent_solver": "cadical195",
        "sat": sat,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
